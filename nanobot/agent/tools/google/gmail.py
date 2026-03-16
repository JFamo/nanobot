"""Gmail tools — send, list, get, search, reply, trash, draft, and labels via coordinator API."""

from typing import Any

from nanobot.agent.tools.google.base import GoogleBaseTool


class GmailSendTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "gmail_send"

    @property
    def description(self) -> str:
        return (
            "Send an email via Gmail. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id. "
            "This action requires user confirmation. The UI automatically shows a preview card with to, subject, and body — "
            "do not repeat those parameters or include display directives in your response; a brief intro line (e.g. \"Here's the email:\") is sufficient."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "to": {"type": "string", "description": "Recipient email address."},
                "subject": {"type": "string", "description": "Email subject line."},
                "body": {"type": "string", "description": "Email body text."},
            },
            "required": ["to", "subject", "body"],
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
            "to": kwargs["to"],
            "subject": kwargs["subject"],
            "body": kwargs["body"],
        }
        return await self._post(f"{coordinator_url}/internal/google/gmail/send", payload)


class GmailListTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "gmail_list"

    @property
    def description(self) -> str:
        return (
            "List emails in the Gmail inbox. Optionally filter by query or label. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id.\n\n"
            "DISPLAY FORMAT: Include a directive for EACH email in your response:\n"
            '::gmail{subject="<subject>" from="<sender>" date="<date>" snippet="<snippet>" url="https://mail.google.com/mail/u/0/#inbox/<message_id>" size="compact"}\n'
            "Use compact size when listing multiple emails. Replace placeholders with actual values. Use each message's ID for the url.\n"
            'Size options: "default" for standalone results, "compact" when listing multiple items, "inline" for brief mentions in text.\n'
            "Do NOT write out email details as text, markdown tables, or bullet lists — the directive renders a rich preview card automatically. "
            "Only add a brief natural-language intro before the directives."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Gmail search query to filter messages, e.g. 'is:unread' or 'from:boss@company.com'.",
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of messages to return (default 20).",
                    "default": 20,
                },
                "label_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Filter by label IDs, e.g. ['INBOX', 'UNREAD'].",
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
        if kwargs.get("query"):
            payload["query"] = kwargs["query"]
        if kwargs.get("max_results"):
            payload["max_results"] = kwargs["max_results"]
        if kwargs.get("label_ids"):
            payload["label_ids"] = kwargs["label_ids"]
        return await self._post(f"{coordinator_url}/internal/google/gmail/list", payload)


class GmailGetTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "gmail_get"

    @property
    def description(self) -> str:
        return (
            "Get the full content of a specific Gmail message by its ID, including subject, sender, and body. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id.\n\n"
            "DISPLAY FORMAT: Include this directive when presenting the email:\n"
            '::gmail{subject="<subject>" from="<sender>" to="<recipient>" date="<date>" body="<body_truncated_300_chars_no_quotes>" url="https://mail.google.com/mail/u/0/#inbox/<message_id>" size="default"}\n'
            "Replace placeholders with actual values. Truncate body to ~300 characters and remove any double-quote characters. Use the message ID for the url.\n"
            'Size options: "default" for standalone results, "compact" when listing multiple items, "inline" for brief mentions in text.\n'
            "Do NOT write out email body or details as text — the directive renders a rich preview card automatically. "
            "Only add a brief natural-language intro before the directive."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "message_id": {
                    "type": "string",
                    "description": "The Gmail message ID to retrieve.",
                },
            },
            "required": ["message_id"],
        }

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload = {"bot_id": bot_id, "message_id": kwargs["message_id"]}
        return await self._post(f"{coordinator_url}/internal/google/gmail/get", payload)


class GmailSearchTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "gmail_search"

    @property
    def description(self) -> str:
        return (
            "Search Gmail messages using Gmail's search query syntax "
            "(e.g. 'from:alice subject:invoice has:attachment'). "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id.\n\n"
            "DISPLAY FORMAT: Include a directive for EACH matching email in your response:\n"
            '::gmail{subject="<subject>" from="<sender>" date="<date>" snippet="<snippet>" url="https://mail.google.com/mail/u/0/#inbox/<message_id>" size="compact"}\n'
            "Use compact size when listing multiple results. Replace placeholders with actual values. Use each message's ID for the url.\n"
            'Size options: "default" for standalone results, "compact" when listing multiple items, "inline" for brief mentions in text.\n'
            "Do NOT write out email details as text — the directive renders a rich preview card automatically. "
            "Only add a brief natural-language intro before the directives."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Gmail search query string, e.g. 'from:boss@company.com is:unread'.",
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return (default 20).",
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
        return await self._post(f"{coordinator_url}/internal/google/gmail/search", payload)


class GmailReplyTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "gmail_reply"

    @property
    def description(self) -> str:
        return (
            "Reply to an existing Gmail thread. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id. "
            "This action requires user confirmation. The UI automatically shows a preview card with thread, to, subject, and body — "
            "do not repeat those parameters or include display directives in your response; a brief intro line is sufficient."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "thread_id": {
                    "type": "string",
                    "description": "The Gmail thread ID to reply to.",
                },
                "message_id": {
                    "type": "string",
                    "description": "The Gmail message ID being replied to (used for threading headers).",
                },
                "to": {
                    "type": "string",
                    "description": "Recipient email address for the reply.",
                },
                "subject": {
                    "type": "string",
                    "description": "Subject line (typically 'Re: original subject').",
                },
                "body": {
                    "type": "string",
                    "description": "Reply body text.",
                },
            },
            "required": ["thread_id", "message_id", "to", "subject", "body"],
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
            "thread_id": kwargs["thread_id"],
            "message_id": kwargs["message_id"],
            "to": kwargs["to"],
            "subject": kwargs["subject"],
            "body": kwargs["body"],
        }
        return await self._post(f"{coordinator_url}/internal/google/gmail/reply", payload)


class GmailTrashTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "gmail_trash"

    @property
    def description(self) -> str:
        return (
            "Move a Gmail message to the trash. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id. "
            "This action requires user confirmation. The UI shows a preview — do not repeat the action details in your response."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "message_id": {
                    "type": "string",
                    "description": "The Gmail message ID to trash.",
                },
            },
            "required": ["message_id"],
        }

    @property
    def requires_confirmation(self) -> bool:
        return True

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload = {"bot_id": bot_id, "message_id": kwargs["message_id"]}
        return await self._post(f"{coordinator_url}/internal/google/gmail/trash", payload)


class GmailCreateDraftTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "gmail_create_draft"

    @property
    def description(self) -> str:
        return (
            "Create a Gmail draft email without sending it. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id. "
            "This action requires user confirmation. The UI automatically shows a preview card with to, subject, and body — "
            "do not repeat those parameters or include display directives in your response; a brief intro line is sufficient."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "to": {"type": "string", "description": "Recipient email address."},
                "subject": {"type": "string", "description": "Email subject line."},
                "body": {"type": "string", "description": "Draft body text."},
            },
            "required": ["to", "subject", "body"],
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
            "to": kwargs["to"],
            "subject": kwargs["subject"],
            "body": kwargs["body"],
        }
        return await self._post(f"{coordinator_url}/internal/google/gmail/create-draft", payload)


class GmailListLabelsTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "gmail_list_labels"

    @property
    def description(self) -> str:
        return (
            "List all Gmail labels (folders) including system labels like INBOX, SENT, and UNREAD. "
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
        return await self._post(f"{coordinator_url}/internal/google/gmail/list-labels", payload)
