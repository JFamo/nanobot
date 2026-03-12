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
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id.\n\n"
            "DISPLAY FORMAT: Always include this directive in your response so the UI renders a preview card:\n"
            '::google-doc{url="<document_url>" title="<document_title>" size="default"}\n'
            "Replace <document_url> and <document_title> with actual values from the response.\n"
            'Size options: "default" for standalone results, "compact" when listing multiple items, "inline" for brief mentions in text.'
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

    @property
    def requires_confirmation(self) -> bool:
        return True

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
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id.\n\n"
            "DISPLAY FORMAT: Include this directive when referencing the document:\n"
            '::google-doc{url="https://docs.google.com/document/d/<document_id>/edit" title="<document_title>" size="default"}\n'
            "Replace <document_id> and <document_title> with actual values.\n"
            'Size options: "default" for standalone results, "compact" when listing multiple items, "inline" for brief mentions in text.'
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
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id.\n\n"
            "DISPLAY FORMAT: Include this directive when confirming the update:\n"
            '::google-doc{url="https://docs.google.com/document/d/<document_id>/edit" title="<document_title>" size="default"}\n'
            "Replace <document_id> and <document_title> with actual values.\n"
            'Size options: "default" for standalone results, "compact" when listing multiple items, "inline" for brief mentions in text.'
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

    @property
    def requires_confirmation(self) -> bool:
        return True

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
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id.\n\n"
            "DISPLAY FORMAT: Include this directive when confirming the update:\n"
            '::google-doc{url="https://docs.google.com/document/d/<document_id>/edit" title="<document_title>" size="default"}\n'
            "Replace <document_id> and <document_title> with actual values.\n"
            'Size options: "default" for standalone results, "compact" when listing multiple items, "inline" for brief mentions in text.'
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

    @property
    def requires_confirmation(self) -> bool:
        return True

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
