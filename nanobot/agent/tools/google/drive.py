"""Google Drive tools — upload, list, get, download, create folder, delete, share, search."""

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
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id. "
            "This action requires user confirmation. The UI automatically shows a preview card with file name and path — "
            "do not repeat those parameters or include display directives in your response; a brief intro line is sufficient."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_name": {"type": "string", "description": "Name for the uploaded file."},
                "mime_type": {"type": "string", "description": "MIME type, e.g. application/pdf."},
                "file_path": {"type": "string", "description": "Path to the local file to upload."},
                "folder_id": {
                    "type": "string",
                    "description": "Optional Google Drive folder ID to upload into.",
                },
            },
            "required": ["file_name", "mime_type", "file_path"],
        }

    @property
    def requires_confirmation(self) -> bool:
        return True

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env

        path = Path(kwargs["file_path"])
        if not path.is_file():
            return f"Error: File not found: {kwargs['file_path']}"

        file_buffer = base64.b64encode(path.read_bytes()).decode()
        payload: dict[str, Any] = {
            "bot_id": bot_id,
            "file_name": kwargs["file_name"],
            "mime_type": kwargs["mime_type"],
            "file_buffer": file_buffer,
        }
        if kwargs.get("folder_id"):
            payload["folder_id"] = kwargs["folder_id"]
        return await self._post(f"{coordinator_url}/internal/google/drive/upload", payload)


class GoogleDriveListTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "drive_list"

    @property
    def description(self) -> str:
        return (
            "List files in Google Drive, optionally filtering by query or folder. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id.\n\n"
            "DISPLAY FORMAT: Include a directive for EACH file in your response:\n"
            '::google-drive{name="<file_name>" url="<webViewLink>" type="file" size="compact"}\n'
            "Use compact size when listing multiple files. For folders use type=\"folder\". Replace placeholders with actual values.\n"
            'Size options: "default" for standalone results, "compact" when listing multiple items, "inline" for brief mentions in text.'
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Drive query filter, e.g. \"mimeType='application/pdf'\".",
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of files to return (default 20).",
                    "default": 20,
                },
                "folder_id": {
                    "type": "string",
                    "description": "Only list files inside this folder ID.",
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
        for key in ("query", "max_results", "folder_id"):
            if kwargs.get(key) is not None:
                payload[key] = kwargs[key]
        return await self._post(f"{coordinator_url}/internal/google/drive/list", payload)


class GoogleDriveGetTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "drive_get"

    @property
    def description(self) -> str:
        return (
            "Get metadata for a Google Drive file by ID (name, type, size, owner, link). "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id.\n\n"
            "DISPLAY FORMAT: Include this directive when presenting file details:\n"
            '::google-drive{name="<file_name>" url="<webViewLink>" type="file" size="default"}\n'
            "Replace placeholders with actual values. For folders use type=\"folder\".\n"
            'Size options: "default" for standalone results, "compact" when listing multiple items, "inline" for brief mentions in text.'
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_id": {
                    "type": "string",
                    "description": "The Google Drive file ID.",
                },
            },
            "required": ["file_id"],
        }

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload = {"bot_id": bot_id, "file_id": kwargs["file_id"]}
        return await self._post(f"{coordinator_url}/internal/google/drive/get", payload)


class GoogleDriveDownloadTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "drive_download"

    @property
    def description(self) -> str:
        return (
            "Download a Google Drive file. Returns the file content as base64. "
            "Google Docs/Sheets/Slides are automatically exported as text/CSV. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_id": {
                    "type": "string",
                    "description": "The Google Drive file ID to download.",
                },
            },
            "required": ["file_id"],
        }

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload = {"bot_id": bot_id, "file_id": kwargs["file_id"]}
        return await self._post(f"{coordinator_url}/internal/google/drive/download", payload)


class GoogleDriveCreateFolderTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "drive_create_folder"

    @property
    def description(self) -> str:
        return (
            "Create a folder in Google Drive. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id. "
            "This action requires user confirmation. The UI automatically shows a preview card with folder name — "
            "do not repeat those parameters or include display directives in your response; a brief intro line is sufficient."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "folder_name": {
                    "type": "string",
                    "description": "Name for the new folder.",
                },
                "parent_folder_id": {
                    "type": "string",
                    "description": "Optional parent folder ID to create the folder inside.",
                },
            },
            "required": ["folder_name"],
        }

    @property
    def requires_confirmation(self) -> bool:
        return True

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload: dict[str, Any] = {"bot_id": bot_id, "folder_name": kwargs["folder_name"]}
        if kwargs.get("parent_folder_id"):
            payload["parent_folder_id"] = kwargs["parent_folder_id"]
        return await self._post(f"{coordinator_url}/internal/google/drive/create-folder", payload)


class GoogleDriveDeleteTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "drive_delete"

    @property
    def description(self) -> str:
        return (
            "Move a Google Drive file to trash. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id. "
            "This action requires user confirmation. The UI shows a preview — do not repeat the action details in your response."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_id": {
                    "type": "string",
                    "description": "The Google Drive file ID to trash.",
                },
            },
            "required": ["file_id"],
        }

    @property
    def requires_confirmation(self) -> bool:
        return True

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload = {"bot_id": bot_id, "file_id": kwargs["file_id"]}
        return await self._post(f"{coordinator_url}/internal/google/drive/delete", payload)


class GoogleDriveShareTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "drive_share"

    @property
    def description(self) -> str:
        return (
            "Share a Google Drive file with a specific email address. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id. "
            "This action requires user confirmation. The UI shows a preview — do not repeat the action details in your response."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "file_id": {
                    "type": "string",
                    "description": "The Google Drive file ID to share.",
                },
                "email": {
                    "type": "string",
                    "description": "Email address of the person to share with.",
                },
                "role": {
                    "type": "string",
                    "description": "Permission role: 'reader', 'commenter', or 'writer'.",
                    "enum": ["reader", "commenter", "writer"],
                    "default": "reader",
                },
            },
            "required": ["file_id", "email"],
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
            "file_id": kwargs["file_id"],
            "email": kwargs["email"],
        }
        if kwargs.get("role"):
            payload["role"] = kwargs["role"]
        return await self._post(f"{coordinator_url}/internal/google/drive/share", payload)


class GoogleDriveSearchTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "drive_search"

    @property
    def description(self) -> str:
        return (
            "Search for files in Google Drive using Drive query syntax, "
            "e.g. \"name contains 'report'\" or \"mimeType='application/pdf'\". "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id.\n\n"
            "DISPLAY FORMAT: Include a directive for EACH matching file in your response:\n"
            '::google-drive{name="<file_name>" url="<webViewLink>" type="file" size="compact"}\n'
            "Use compact size when listing multiple results. For folders use type=\"folder\". Replace placeholders with actual values.\n"
            'Size options: "default" for standalone results, "compact" when listing multiple items, "inline" for brief mentions in text.'
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Drive query string, e.g. \"name contains 'budget'\".",
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results (default 20).",
                    "default": 20,
                },
            },
            "required": ["query"],
        }

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload: dict[str, Any] = {"bot_id": bot_id, "query": kwargs["query"]}
        if kwargs.get("max_results"):
            payload["max_results"] = kwargs["max_results"]
        return await self._post(f"{coordinator_url}/internal/google/drive/search", payload)
