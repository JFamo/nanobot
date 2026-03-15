"""X retweet tools — retweet and undo retweet via coordinator API."""

from typing import Any

from nanobot.agent.tools.x.base import XBaseTool


class XRetweetTool(XBaseTool):

    @property
    def name(self) -> str:
        return "x_retweet"

    @property
    def description(self) -> str:
        return (
            "Retweet a tweet on X. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id. "
            "This action requires user confirmation. The UI shows a preview — do not repeat the action details in your response."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "tweet_id": {"type": "string", "description": "The ID of the tweet to retweet."},
            },
            "required": ["tweet_id"],
        }

    @property
    def requires_confirmation(self) -> bool:
        return True

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload = {"bot_id": bot_id, "tweet_id": kwargs["tweet_id"]}
        return await self._post(f"{coordinator_url}/internal/x/retweets/retweet", payload)


class XUndoRetweetTool(XBaseTool):

    @property
    def name(self) -> str:
        return "x_undo_retweet"

    @property
    def description(self) -> str:
        return (
            "Undo a retweet on X. Authentication is automatic. "
            "This action requires user confirmation. The UI shows a preview — do not repeat the action details in your response."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "tweet_id": {"type": "string", "description": "The ID of the tweet to un-retweet."},
            },
            "required": ["tweet_id"],
        }

    @property
    def requires_confirmation(self) -> bool:
        return True

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload = {"bot_id": bot_id, "tweet_id": kwargs["tweet_id"]}
        return await self._post(f"{coordinator_url}/internal/x/retweets/undo", payload)
