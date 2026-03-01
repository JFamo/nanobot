"""Telegram relay channel implementation using HTTP API to coordinator service."""

from __future__ import annotations

import asyncio
from typing import Any

import httpx
from loguru import logger

from nanobot.bus.events import OutboundMessage
from nanobot.bus.queue import MessageBus
from nanobot.channels.base import BaseChannel
from nanobot.config.schema import TelegramRelayConfig


class TelegramRelayChannel(BaseChannel):
    """
    Telegram relay channel that sends messages via HTTP API to a coordinator service.
    
    This channel does not receive messages directly - it only sends outbound messages
    via HTTP POST to the coordinator service, which handles the actual Telegram bot.
    """
    
    name = "telegram_relay"
    
    def __init__(self, config: TelegramRelayConfig, bus: MessageBus):
        super().__init__(config, bus)
        self.config: TelegramRelayConfig = config
        self._client: httpx.AsyncClient | None = None
    
    async def start(self) -> None:
        """Start the relay channel (no-op for relay mode)."""
        if not self.config.coordinator_url:
            logger.error("Telegram relay coordinator_url not configured")
            return
        
        if not self.config.bot_id:
            logger.error("Telegram relay bot_id not configured")
            return
        
        self._running = True
        
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0, connect=10.0),
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10)
        )
        
        logger.info(
            "Telegram relay channel started (coordinator: {}, bot_id: {})",
            self.config.coordinator_url,
            self.config.bot_id
        )
        
        while self._running:
            await asyncio.sleep(1)
    
    async def stop(self) -> None:
        """Stop the relay channel."""
        self._running = False
        
        if self._client:
            await self._client.aclose()
            self._client = None
        
        logger.info("Telegram relay channel stopped")
    
    async def send(self, msg: OutboundMessage) -> None:
        """
        Send a message through the coordinator HTTP API.
        
        Args:
            msg: The message to send.
        """
        if not self._client:
            logger.warning("Telegram relay channel not running")
            return
        
        if not msg.content:
            logger.debug("Skipping empty message")
            return
        
        url = f"{self.config.coordinator_url}/api/v1/bots/{self.config.bot_id}/telegram/send"
        payload = {"message": msg.content}
        
        retry_count = 0
        max_retries = 3
        base_delay = 1.0
        
        while retry_count <= max_retries:
            try:
                logger.debug("Sending message to coordinator: {}", url)
                
                response = await self._client.post(
                    url,
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success") and data.get("message_sent"):
                        telegram_user_id = data.get("telegram_user_id")
                        logger.info(
                            "Message sent successfully via telegram_relay to user {}",
                            telegram_user_id
                        )
                        return
                    else:
                        logger.error(
                            "Coordinator returned success=false: {}",
                            data
                        )
                        return
                
                elif response.status_code == 404:
                    logger.error(
                        "Bot not linked (404): bot_id '{}' not found or not linked to Telegram user. "
                        "Please link the bot via the coordinator service.",
                        self.config.bot_id
                    )
                    return
                
                elif response.status_code >= 500:
                    if retry_count < max_retries:
                        delay = base_delay * (2 ** retry_count)
                        logger.warning(
                            "Coordinator server error ({}), retrying in {}s (attempt {}/{})",
                            response.status_code,
                            delay,
                            retry_count + 1,
                            max_retries
                        )
                        await asyncio.sleep(delay)
                        retry_count += 1
                        continue
                    else:
                        logger.error(
                            "Coordinator server error ({}) after {} retries: {}",
                            response.status_code,
                            max_retries,
                            response.text
                        )
                        return
                
                else:
                    logger.error(
                        "Unexpected response from coordinator ({}): {}",
                        response.status_code,
                        response.text
                    )
                    return
            
            except httpx.ConnectError as e:
                if retry_count < max_retries:
                    delay = base_delay * (2 ** retry_count)
                    logger.warning(
                        "Connection error to coordinator, retrying in {}s (attempt {}/{}): {}",
                        delay,
                        retry_count + 1,
                        max_retries,
                        e
                    )
                    await asyncio.sleep(delay)
                    retry_count += 1
                    continue
                else:
                    logger.error(
                        "Failed to connect to coordinator after {} retries: {}",
                        max_retries,
                        e
                    )
                    return
            
            except httpx.TimeoutException as e:
                if retry_count < max_retries:
                    delay = base_delay * (2 ** retry_count)
                    logger.warning(
                        "Timeout connecting to coordinator, retrying in {}s (attempt {}/{}): {}",
                        delay,
                        retry_count + 1,
                        max_retries,
                        e
                    )
                    await asyncio.sleep(delay)
                    retry_count += 1
                    continue
                else:
                    logger.error(
                        "Coordinator timeout after {} retries: {}",
                        max_retries,
                        e
                    )
                    return
            
            except Exception as e:
                logger.error(
                    "Unexpected error sending message via telegram_relay: {}",
                    e
                )
                return
