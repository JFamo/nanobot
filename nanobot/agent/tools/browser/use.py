"""browser_use tool — full interactive browsing via coordinator + Browserbase."""

from typing import Any

from nanobot.agent.tools.browser.base import BrowserBaseTool


class BrowserUseTool(BrowserBaseTool):

    @property
    def name(self) -> str:
        return "browser_use"

    @property
    def description(self) -> str:
        return (
            "Interact with a web page using a real browser. You can navigate, click, "
            "type, scroll, read content, fill forms, log in to sites, and perform any "
            "browser action. The browser remembers your login sessions and cookies "
            "across uses — you do not need to re-authenticate on sites you have "
            "previously logged into.\n\n"
            "Provide a natural-language description of what you want to do in the "
            "browser as the 'task' parameter. Optionally provide a starting 'url'."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "task": {
                    "type": "string",
                    "description": (
                        "Natural-language description of what to do in the browser, "
                        "e.g. 'Search for recent news about AI safety' or "
                        "'Log in to GitHub and check my notifications'."
                    ),
                },
                "url": {
                    "type": "string",
                    "description": "Optional starting URL to navigate to before performing the task.",
                },
            },
            "required": ["task"],
        }

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload: dict[str, Any] = {
            "bot_id": bot_id,
            "task": kwargs["task"],
        }
        if kwargs.get("url"):
            payload["url"] = kwargs["url"]
        return await self._post(f"{coordinator_url}/internal/browser/use", payload)
