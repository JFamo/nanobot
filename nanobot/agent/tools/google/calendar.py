"""Google Calendar tools — create, list, get, update, delete events, list calendars."""

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
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id.\n\n"
            "DISPLAY FORMAT: Always include this directive in your response so the UI renders a preview card:\n"
            '::google-calendar-event{title="<event_title>" date="<start_time_iso>" url="<htmlLink>" size="default"}\n'
            "Replace placeholders with actual values. Use the htmlLink from the response for the url.\n"
            'Size options: "default" for standalone results, "compact" when listing multiple items, "inline" for brief mentions in text.'
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "summary": {"type": "string", "description": "Event title."},
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
                "location": {"type": "string", "description": "Event location."},
                "event_description": {"type": "string", "description": "Event description."},
                "calendar_id": {
                    "type": "string",
                    "description": "Calendar ID to create the event in (default 'primary').",
                    "default": "primary",
                },
            },
            "required": ["summary", "start", "end"],
        }

    @property
    def requires_confirmation(self) -> bool:
        return True

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
        if kwargs.get("calendar_id"):
            payload["calendar_id"] = kwargs["calendar_id"]
        return await self._post(
            f"{coordinator_url}/internal/google/calendar/create-event", payload
        )


class GoogleCalendarListEventsTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "calendar_list_events"

    @property
    def description(self) -> str:
        return (
            "List Google Calendar events, optionally filtered by time range or search query. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id.\n\n"
            "DISPLAY FORMAT: Include a directive for EACH event in your response:\n"
            '::google-calendar-event{title="<event_title>" date="<start_time_iso>" url="<htmlLink>" size="compact"}\n'
            "Use compact size when listing multiple events. Replace placeholders with actual values from each event.\n"
            'Size options: "default" for standalone results, "compact" when listing multiple items, "inline" for brief mentions in text.'
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "time_min": {
                    "type": "string",
                    "description": "Earliest event end time, RFC3339, e.g. '2026-03-01T00:00:00Z'.",
                },
                "time_max": {
                    "type": "string",
                    "description": "Latest event start time, RFC3339, e.g. '2026-03-31T23:59:59Z'.",
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of events to return (default 20).",
                    "default": 20,
                },
                "query": {
                    "type": "string",
                    "description": "Free text search terms to filter events.",
                },
                "calendar_id": {
                    "type": "string",
                    "description": "Calendar ID to list events from (default 'primary').",
                    "default": "primary",
                },
            },
            "required": [],
        }

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload: dict[str, Any] = {"bot_id": bot_id}
        for key in ("time_min", "time_max", "max_results", "query", "calendar_id"):
            if kwargs.get(key) is not None:
                payload[key] = kwargs[key]
        return await self._post(
            f"{coordinator_url}/internal/google/calendar/list-events", payload
        )


class GoogleCalendarGetEventTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "calendar_get_event"

    @property
    def description(self) -> str:
        return (
            "Get details of a specific Google Calendar event by ID. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id.\n\n"
            "DISPLAY FORMAT: Include this directive when presenting event details:\n"
            '::google-calendar-event{title="<event_title>" date="<start_time_iso>" url="<htmlLink>" size="default"}\n'
            "Replace placeholders with actual values. Use the htmlLink from the response for the url.\n"
            'Size options: "default" for standalone results, "compact" when listing multiple items, "inline" for brief mentions in text.'
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "event_id": {
                    "type": "string",
                    "description": "The Google Calendar event ID.",
                },
                "calendar_id": {
                    "type": "string",
                    "description": "Calendar ID (default 'primary').",
                    "default": "primary",
                },
            },
            "required": ["event_id"],
        }

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload: dict[str, Any] = {"bot_id": bot_id, "event_id": kwargs["event_id"]}
        if kwargs.get("calendar_id"):
            payload["calendar_id"] = kwargs["calendar_id"]
        return await self._post(
            f"{coordinator_url}/internal/google/calendar/get-event", payload
        )


class GoogleCalendarUpdateEventTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "calendar_update_event"

    @property
    def description(self) -> str:
        return (
            "Update an existing Google Calendar event. Only provided fields are changed. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id.\n\n"
            "DISPLAY FORMAT: Include this directive when confirming the update:\n"
            '::google-calendar-event{title="<event_title>" date="<start_time_iso>" url="<htmlLink>" size="default"}\n'
            "Replace placeholders with actual values. Use the htmlLink from the response for the url.\n"
            'Size options: "default" for standalone results, "compact" when listing multiple items, "inline" for brief mentions in text.'
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "event_id": {
                    "type": "string",
                    "description": "The Google Calendar event ID to update.",
                },
                "calendar_id": {
                    "type": "string",
                    "description": "Calendar ID (default 'primary').",
                    "default": "primary",
                },
                "summary": {"type": "string", "description": "New event title."},
                "start": {
                    "type": "string",
                    "description": "New start time in ISO 8601 with timezone.",
                },
                "end": {
                    "type": "string",
                    "description": "New end time in ISO 8601 with timezone.",
                },
                "attendees": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Updated list of attendee email addresses.",
                },
                "location": {"type": "string", "description": "New event location."},
                "description": {"type": "string", "description": "New event description."},
            },
            "required": ["event_id"],
        }

    @property
    def requires_confirmation(self) -> bool:
        return True

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload: dict[str, Any] = {"bot_id": bot_id, "event_id": kwargs["event_id"]}
        for key in ("calendar_id", "summary", "start", "end", "attendees", "location", "description"):
            if kwargs.get(key) is not None:
                payload[key] = kwargs[key]
        return await self._post(
            f"{coordinator_url}/internal/google/calendar/update-event", payload
        )


class GoogleCalendarDeleteEventTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "calendar_delete_event"

    @property
    def description(self) -> str:
        return (
            "Delete a Google Calendar event. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "event_id": {
                    "type": "string",
                    "description": "The Google Calendar event ID to delete.",
                },
                "calendar_id": {
                    "type": "string",
                    "description": "Calendar ID (default 'primary').",
                    "default": "primary",
                },
            },
            "required": ["event_id"],
        }

    @property
    def requires_confirmation(self) -> bool:
        return True

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload: dict[str, Any] = {"bot_id": bot_id, "event_id": kwargs["event_id"]}
        if kwargs.get("calendar_id"):
            payload["calendar_id"] = kwargs["calendar_id"]
        return await self._post(
            f"{coordinator_url}/internal/google/calendar/delete-event", payload
        )


class GoogleCalendarListCalendarsTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "calendar_list_calendars"

    @property
    def description(self) -> str:
        return (
            "List all Google Calendars the user has access to. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {},
            "required": [],
        }

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload = {"bot_id": bot_id}
        return await self._post(
            f"{coordinator_url}/internal/google/calendar/list-calendars", payload
        )
