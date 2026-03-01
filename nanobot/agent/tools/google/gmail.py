"""Gmail send tool — send emails via the coordinator API."""

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
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "to": {
                    "type": "string",
                    "description": "Recipient email address.",
                },
                "subject": {
                    "type": "string",
                    "description": "Email subject line.",
                },
                "body": {
                    "type": "string",
                    "description": "Email body text.",
                },
            },
            "required": ["to", "subject", "body"],
        }

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
