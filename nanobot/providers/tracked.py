"""Wrapper around LLMProvider that automatically reports token usage to the coordinator."""

import asyncio
from typing import Any

from nanobot.coordinator.client import report_usage
from nanobot.providers.base import LLMProvider, LLMResponse


def _fire_usage_report(response: LLMResponse, *, model: str, source: str) -> None:
    """Schedule an async usage report if the response contains token counts."""
    if response.usage:
        asyncio.create_task(report_usage(
            prompt_tokens=response.usage.get("prompt_tokens", 0),
            completion_tokens=response.usage.get("completion_tokens", 0),
            model=model,
            source=source,
        ))


async def tracked_chat(
    provider: LLMProvider,
    *,
    messages: list[dict[str, Any]],
    source: str = "agent_loop",
    model: str | None = None,
    tools: list[dict[str, Any]] | None = None,
    max_tokens: int = 4096,
    temperature: float = 0.7,
    reasoning_effort: str | None = None,
    tool_choice: str | dict[str, Any] | None = None,
) -> LLMResponse:
    """Call provider.chat and fire-and-forget report usage to the coordinator."""
    response = await provider.chat(
        messages=messages,
        tools=tools,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        reasoning_effort=reasoning_effort,
        tool_choice=tool_choice,
    )
    _fire_usage_report(response, model=model or "", source=source)
    return response


async def tracked_chat_with_retry(
    provider: LLMProvider,
    *,
    messages: list[dict[str, Any]],
    source: str = "agent_loop",
    model: str | None = None,
    tools: list[dict[str, Any]] | None = None,
    max_tokens: object = LLMProvider._SENTINEL,
    temperature: object = LLMProvider._SENTINEL,
    reasoning_effort: object = LLMProvider._SENTINEL,
    tool_choice: str | dict[str, Any] | None = None,
    retry_mode: str = "standard",
    on_retry_wait: Any = None,
) -> LLMResponse:
    """Call provider.chat_with_retry and fire-and-forget report usage."""
    response = await provider.chat_with_retry(
        messages=messages,
        tools=tools,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        reasoning_effort=reasoning_effort,
        tool_choice=tool_choice,
        retry_mode=retry_mode,
        on_retry_wait=on_retry_wait,
    )
    _fire_usage_report(response, model=model or "", source=source)
    return response


async def tracked_chat_stream_with_retry(
    provider: LLMProvider,
    *,
    messages: list[dict[str, Any]],
    source: str = "agent_loop",
    model: str | None = None,
    tools: list[dict[str, Any]] | None = None,
    max_tokens: object = LLMProvider._SENTINEL,
    temperature: object = LLMProvider._SENTINEL,
    reasoning_effort: object = LLMProvider._SENTINEL,
    tool_choice: str | dict[str, Any] | None = None,
    on_content_delta: Any = None,
    retry_mode: str = "standard",
    on_retry_wait: Any = None,
) -> LLMResponse:
    """Call provider.chat_stream_with_retry and fire-and-forget report usage."""
    response = await provider.chat_stream_with_retry(
        messages=messages,
        tools=tools,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        reasoning_effort=reasoning_effort,
        tool_choice=tool_choice,
        on_content_delta=on_content_delta,
        retry_mode=retry_mode,
        on_retry_wait=on_retry_wait,
    )
    _fire_usage_report(response, model=model or "", source=source)
    return response
