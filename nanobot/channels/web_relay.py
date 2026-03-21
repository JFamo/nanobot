"""Web relay channel implementation using HTTP API to coordinator service."""

from __future__ import annotations

import asyncio

import httpx
from loguru import logger

from nanobot.bus.events import OutboundMessage
from nanobot.bus.queue import MessageBus
from nanobot.channels.base import BaseChannel
from nanobot.config.schema import WebRelayConfig
from nanobot.coordinator.client import auth_headers


class WebRelayChannel(BaseChannel):
    """
    Web relay channel that sends messages via HTTP API to a coordinator service,
    which pushes them to connected browser clients over a persistent SSE connection.

    This channel does not receive messages directly — it only sends outbound messages
    via HTTP POST to the coordinator's /web/push endpoint.
    """

    name = "web_relay"

    def __init__(self, config: WebRelayConfig, bus: MessageBus):
        super().__init__(config, bus)
        self.config: WebRelayConfig = config
        self._client: httpx.AsyncClient | None = None

    async def start(self) -> None:
        if not self.config.coordinator_url:
            logger.error("Web relay coordinator_url not configured")
            return

        if not self.config.bot_id:
            logger.error("Web relay bot_id not configured")
            return

        self._running = True
        self._client = httpx.AsyncClient(
            headers=auth_headers(),
            timeout=httpx.Timeout(30.0, connect=10.0),
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10),
        )

        logger.info(
            "Web relay channel started (coordinator: {}, bot_id: {})",
            self.config.coordinator_url,
            self.config.bot_id,
        )

        while self._running:
            await asyncio.sleep(1)

    async def stop(self) -> None:
        self._running = False

        if self._client:
            await self._client.aclose()
            self._client = None

        logger.info("Web relay channel stopped")

    async def send(self, msg: OutboundMessage) -> None:
        if not self._client:
            logger.warning("Web relay channel not running")
            return

        if not msg.content:
            logger.debug("Skipping empty message")
            return

        url = f"{self.config.coordinator_url}/api/v1/bots/{self.config.bot_id}/web/push"
        payload = {"message": msg.content, "chat_id": msg.chat_id}

        retry_count = 0
        max_retries = 3
        base_delay = 1.0

        while retry_count <= max_retries:
            try:
                logger.debug("Sending message to coordinator web/push: {}", url)

                response = await self._client.post(url, json=payload)

                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        message_id = data.get("message_id")
                        logger.info(
                            "Message sent successfully via web_relay (message_id: {})",
                            message_id,
                        )
                        return
                    else:
                        logger.error(
                            "Coordinator returned success=false: {}",
                            data,
                        )
                        return

                elif response.status_code == 404:
                    logger.error(
                        "Bot not found (404): bot_id '{}' not found on coordinator.",
                        self.config.bot_id,
                    )
                    return

                elif response.status_code >= 500:
                    if retry_count < max_retries:
                        delay = base_delay * (2**retry_count)
                        logger.warning(
                            "Coordinator server error ({}), retrying in {}s (attempt {}/{})",
                            response.status_code,
                            delay,
                            retry_count + 1,
                            max_retries,
                        )
                        await asyncio.sleep(delay)
                        retry_count += 1
                        continue
                    else:
                        logger.error(
                            "Coordinator server error ({}) after {} retries: {}",
                            response.status_code,
                            max_retries,
                            response.text,
                        )
                        return

                else:
                    logger.error(
                        "Unexpected response from coordinator ({}): {}",
                        response.status_code,
                        response.text,
                    )
                    return

            except httpx.ConnectError as e:
                if retry_count < max_retries:
                    delay = base_delay * (2**retry_count)
                    logger.warning(
                        "Connection error to coordinator, retrying in {}s (attempt {}/{}): {}",
                        delay,
                        retry_count + 1,
                        max_retries,
                        e,
                    )
                    await asyncio.sleep(delay)
                    retry_count += 1
                    continue
                else:
                    logger.error(
                        "Failed to connect to coordinator after {} retries: {}",
                        max_retries,
                        e,
                    )
                    return

            except httpx.TimeoutException as e:
                if retry_count < max_retries:
                    delay = base_delay * (2**retry_count)
                    logger.warning(
                        "Timeout connecting to coordinator, retrying in {}s (attempt {}/{}): {}",
                        delay,
                        retry_count + 1,
                        max_retries,
                        e,
                    )
                    await asyncio.sleep(delay)
                    retry_count += 1
                    continue
                else:
                    logger.error(
                        "Coordinator timeout after {} retries: {}",
                        max_retries,
                        e,
                    )
                    return

            except Exception as e:
                logger.error(
                    "Unexpected error sending message via web_relay: {}",
                    e,
                )
                return
