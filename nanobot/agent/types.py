"""Shared types for the agent subsystem."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class PendingAction:
    """A tool call that requires user confirmation before execution."""

    action_id: str
    tool_call_id: str
    tool_name: str
    arguments: dict[str, Any]


@dataclass
class AgentResponse:
    """Structured response from the agent, including any pending confirmation actions."""

    content: str
    pending_actions: list[PendingAction] = field(default_factory=list)
