"""Google Drive tool — upload files via the coordinator API."""

import base64
from pathlib import Path
from typing import Any

from nanobot.agent.tools.google.base import GoogleBaseTool


class GoogleDriveUploadTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "drive_upload"

    @property
    def description(self) -> str:
        return (
            "Upload a file to Google Drive. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_name": {
                    "type": "string",
                    "description": "Name for the uploaded file.",
                },
                "mime_type": {
                    "type": "string",
                    "description": "MIME type, e.g. application/pdf.",
                },
                "file_path": {
                    "type": "string",
                    "description": "Path to the local file to upload.",
                },
            },
            "required": ["file_name", "mime_type", "file_path"],
        }

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env

        path = Path(kwargs["file_path"])
        if not path.is_file():
            return f"Error: File not found: {kwargs['file_path']}"

        file_buffer = base64.b64encode(path.read_bytes()).decode()
        payload = {
            "bot_id": bot_id,
            "file_name": kwargs["file_name"],
            "mime_type": kwargs["mime_type"],
            "file_buffer": file_buffer,
        }
        return await self._post(f"{coordinator_url}/internal/google/drive/upload", payload)
