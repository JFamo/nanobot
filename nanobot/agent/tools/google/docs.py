"""Google Docs tools — create, get, append, and insert text via the coordinator API."""

from typing import Any

from nanobot.agent.tools.google.base import GoogleBaseTool


class GoogleDocsCreateTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "docs_create"

    @property
    def description(self) -> str:
        return (
            "Create a new Google Doc with a given title. Returns the document ID and URL. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Title for the new Google Doc.",
                },
            },
            "required": ["title"],
        }

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload = {"bot_id": bot_id, "title": kwargs["title"]}
        return await self._post(f"{coordinator_url}/internal/google/docs/create", payload)


class GoogleDocsGetTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "docs_get"

    @property
    def description(self) -> str:
        return (
            "Read the plain text content of a Google Doc by its document ID. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "document_id": {
                    "type": "string",
                    "description": "The Google Doc document ID (from the URL).",
                },
            },
            "required": ["document_id"],
        }

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload = {"bot_id": bot_id, "document_id": kwargs["document_id"]}
        return await self._post(f"{coordinator_url}/internal/google/docs/get", payload)


class GoogleDocsAppendTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "docs_append"

    @property
    def description(self) -> str:
        return (
            "Append text to the end of a Google Doc. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "document_id": {
                    "type": "string",
                    "description": "The Google Doc document ID.",
                },
                "text": {
                    "type": "string",
                    "description": "Text to append at the end of the document.",
                },
            },
            "required": ["document_id", "text"],
        }

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload = {
            "bot_id": bot_id,
            "document_id": kwargs["document_id"],
            "text": kwargs["text"],
        }
        return await self._post(f"{coordinator_url}/internal/google/docs/append", payload)


class GoogleDocsInsertTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "docs_insert"

    @property
    def description(self) -> str:
        return (
            "Insert text at a specific character index in a Google Doc. "
            "Use docs_get first to determine the correct index position. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "document_id": {
                    "type": "string",
                    "description": "The Google Doc document ID.",
                },
                "text": {
                    "type": "string",
                    "description": "Text to insert.",
                },
                "index": {
                    "type": "integer",
                    "description": "1-based character index in the document where text will be inserted.",
                },
            },
            "required": ["document_id", "text", "index"],
        }

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload = {
            "bot_id": bot_id,
            "document_id": kwargs["document_id"],
            "text": kwargs["text"],
            "index": kwargs["index"],
        }
        return await self._post(f"{coordinator_url}/internal/google/docs/insert", payload)
