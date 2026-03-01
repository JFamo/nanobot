"""Google Calendar tool — create calendar events via the coordinator API."""

from typing import Any

from nanobot.agent.tools.google.base import GoogleBaseTool


class GoogleCalendarCreateEventTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "calendar_create_event"

    @property
    def description(self) -> str:
        return (
            "Create a Google Calendar event. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "summary": {
                    "type": "string",
                    "description": "Event title.",
                },
                "start": {
                    "type": "string",
                    "description": "Start time in ISO 8601 with timezone, e.g. 2026-03-06T18:00:00-05:00.",
                },
                "end": {
                    "type": "string",
                    "description": "End time in ISO 8601 with timezone.",
                },
                "attendees": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of attendee email addresses.",
                },
                "location": {
                    "type": "string",
                    "description": "Event location.",
                },
                "event_description": {
                    "type": "string",
                    "description": "Event description.",
                },
            },
            "required": ["summary", "start", "end"],
        }

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env

        payload: dict[str, Any] = {
            "bot_id": bot_id,
            "summary": kwargs["summary"],
            "start": kwargs["start"],
            "end": kwargs["end"],
        }
        if kwargs.get("attendees"):
            payload["attendees"] = kwargs["attendees"]
        if kwargs.get("location"):
            payload["location"] = kwargs["location"]
        if kwargs.get("event_description"):
            payload["description"] = kwargs["event_description"]

        return await self._post(
            f"{coordinator_url}/internal/google/calendar/create-event", payload
        )
