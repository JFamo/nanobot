"""Google Workspace tool — send emails, create calendar events, upload to Drive."""

import json
import os
from typing import Any

import httpx

from nanobot.agent.tools.base import Tool


class GoogleTool(Tool):
    """
    Native tool for Google Workspace actions via the coordinator API.

    Wraps the coordinator's /internal/google/* endpoints so the agent
    can call it directly instead of crafting exec one-liners.
    """

    @property
    def name(self) -> str:
        return "google"

    @property
    def description(self) -> str:
        return (
            "Perform Google Workspace actions: send emails (gmail_send), "
            "create calendar events (calendar_create_event), or upload files to Drive (drive_upload). "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["gmail_send", "calendar_create_event", "drive_upload"],
                    "description": "Which Google action to perform."
                },
                "to": {
                    "type": "string",
                    "description": "(gmail_send) Recipient email address."
                },
                "subject": {
                    "type": "string",
                    "description": "(gmail_send) Email subject line."
                },
                "body": {
                    "type": "string",
                    "description": "(gmail_send) Email body text."
                },
                "summary": {
                    "type": "string",
                    "description": "(calendar_create_event) Event title."
                },
                "start": {
                    "type": "string",
                    "description": "(calendar_create_event) Start time in ISO 8601 with timezone, e.g. 2026-03-06T18:00:00-05:00."
                },
                "end": {
                    "type": "string",
                    "description": "(calendar_create_event) End time in ISO 8601 with timezone."
                },
                "attendees": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "(calendar_create_event, optional) List of attendee email addresses."
                },
                "location": {
                    "type": "string",
                    "description": "(calendar_create_event, optional) Event location."
                },
                "event_description": {
                    "type": "string",
                    "description": "(calendar_create_event, optional) Event description."
                },
                "file_name": {
                    "type": "string",
                    "description": "(drive_upload) Name for the uploaded file."
                },
                "mime_type": {
                    "type": "string",
                    "description": "(drive_upload) MIME type, e.g. application/pdf."
                },
                "file_path": {
                    "type": "string",
                    "description": "(drive_upload) Path to the local file to upload."
                },
            },
            "required": ["action"],
        }

    async def execute(self, **kwargs: Any) -> str:
        coordinator_url = os.environ.get("COORDINATOR_URL")
        bot_id = os.environ.get("BOT_ID")

        if not coordinator_url:
            return "Error: COORDINATOR_URL environment variable is not set."
        if not bot_id:
            return "Error: BOT_ID environment variable is not set."

        action = kwargs.get("action")
        if action == "gmail_send":
            return await self._gmail_send(coordinator_url, bot_id, kwargs)
        elif action == "calendar_create_event":
            return await self._calendar_create_event(coordinator_url, bot_id, kwargs)
        elif action == "drive_upload":
            return await self._drive_upload(coordinator_url, bot_id, kwargs)
        else:
            return f"Error: Unknown action '{action}'."

    async def _gmail_send(self, url: str, bot_id: str, p: dict) -> str:
        for field in ("to", "subject", "body"):
            if not p.get(field):
                return f"Error: '{field}' is required for gmail_send."

        payload = {
            "bot_id": bot_id,
            "to": p["to"],
            "subject": p["subject"],
            "body": p["body"],
        }
        return await self._post(f"{url}/internal/google/gmail/send", payload)

    async def _calendar_create_event(self, url: str, bot_id: str, p: dict) -> str:
        for field in ("summary", "start", "end"):
            if not p.get(field):
                return f"Error: '{field}' is required for calendar_create_event."

        payload: dict[str, Any] = {
            "bot_id": bot_id,
            "summary": p["summary"],
            "start": p["start"],
            "end": p["end"],
        }
        if p.get("attendees"):
            payload["attendees"] = p["attendees"]
        if p.get("location"):
            payload["location"] = p["location"]
        if p.get("event_description"):
            payload["description"] = p["event_description"]

        return await self._post(f"{url}/internal/google/calendar/create-event", payload)

    async def _drive_upload(self, url: str, bot_id: str, p: dict) -> str:
        for field in ("file_name", "mime_type", "file_path"):
            if not p.get(field):
                return f"Error: '{field}' is required for drive_upload."

        import base64
        from pathlib import Path

        path = Path(p["file_path"])
        if not path.is_file():
            return f"Error: File not found: {p['file_path']}"

        file_buffer = base64.b64encode(path.read_bytes()).decode()
        payload = {
            "bot_id": bot_id,
            "file_name": p["file_name"],
            "mime_type": p["mime_type"],
            "file_buffer": file_buffer,
        }
        return await self._post(f"{url}/internal/google/drive/upload", payload)

    @staticmethod
    async def _post(url: str, payload: dict) -> str:
        """HTTP POST to the coordinator API."""
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.post(url, json=payload)
        except httpx.ConnectError:
            return "Error: Could not connect to coordinator. Is COORDINATOR_URL correct?"
        except httpx.TimeoutException:
            return "Error: Request timed out after 30 seconds."
        except httpx.HTTPError as exc:
            return f"Error: HTTP request failed: {exc}"

        try:
            data = resp.json()
        except Exception:
            return f"Error: Non-JSON response (status {resp.status_code}): {resp.text[:500]}"

        if resp.is_success and data.get("success"):
            return json.dumps(data, indent=2)

        detail = data.get("detail") or data.get("error") or json.dumps(data)
        return f"Error (HTTP {resp.status_code}): {detail}"
