"""browser_search tool — web search via coordinator + Browserbase."""

from typing import Any

from nanobot.agent.tools.browser.base import BrowserBaseTool


class BrowserSearchTool(BrowserBaseTool):

    @property
    def name(self) -> str:
        return "browser_search"

    @property
    def description(self) -> str:
        return (
            "Search the web using a real browser. Returns search results for the "
            "given query. The browser remembers your login sessions and cookies "
            "across uses."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query.",
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results to return (default 10).",
                    "default": 10,
                },
            },
            "required": ["query"],
        }

    @property
    def read_only(self) -> bool:
        return True

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload: dict[str, Any] = {
            "bot_id": bot_id,
            "query": kwargs["query"],
        }
        if kwargs.get("max_results"):
            payload["max_results"] = kwargs["max_results"]
        return await self._post(f"{coordinator_url}/internal/browser/search", payload)
