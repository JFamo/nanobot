"""Shared helpers for X (Twitter) tools."""

import os
from typing import Any

from nanobot.agent.tools.base import Tool
from nanobot import coordinator


class XBaseTool(Tool):
    """
    Abstract base for X tools.

    Provides the coordinator URL / bot ID resolution and the shared
    HTTP POST helper that every X tool needs.
    """

    def _env(self) -> tuple[str, str] | str:
        """Return (coordinator_url, bot_id) or an error string."""
        coordinator_url = os.environ.get("COORDINATOR_URL")
        bot_id = os.environ.get("BOT_ID")
        if not coordinator_url:
            return "Error: COORDINATOR_URL environment variable is not set."
        if not bot_id:
            return "Error: BOT_ID environment variable is not set."
        return coordinator_url, bot_id

    @staticmethod
    async def _post(url: str, payload: dict[str, Any]) -> str:
        return await coordinator.client.post(url, payload)
