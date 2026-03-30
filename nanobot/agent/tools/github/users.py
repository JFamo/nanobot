"""GitHub user tools via coordinator API."""

from typing import Any

from nanobot.agent.tools.github.base import GitHubBaseTool


class GitHubGetMeTool(GitHubBaseTool):

    @property
    def name(self) -> str:
        return "github_get_me"

    @property
    def description(self) -> str:
        return (
            "Get the authenticated GitHub user's profile. "
            "Authentication is automatic.\n\n"
            "DISPLAY FORMAT: Include this directive when presenting the profile:\n"
            '::github-user{login="<login>" name="<name>" bio="<bio>" url="<html_url>" repos="<public_repos>" followers="<followers>" size="default"}\n'
            "Replace placeholders with actual values.\n"
            'Size options: "default" for standalone results, "compact" when listing multiple items, "inline" for brief mentions in text.\n'
            "Do NOT write out profile fields as plain text — the directive renders a rich preview card automatically."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {"type": "object", "properties": {}}

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload = {"bot_id": bot_id}
        return await self._post(f"{coordinator_url}/internal/github/users/me", payload)


class GitHubGetUserTool(GitHubBaseTool):

    @property
    def name(self) -> str:
        return "github_get_user"

    @property
    def description(self) -> str:
        return (
            "Get a GitHub user's public profile by username. "
            "Authentication is automatic.\n\n"
            "DISPLAY FORMAT: Include this directive when presenting the profile:\n"
            '::github-user{login="<login>" name="<name>" bio="<bio>" url="<html_url>" repos="<public_repos>" followers="<followers>" size="default"}\n'
            "Replace placeholders with actual values.\n"
            'Size options: "default" for standalone results, "compact" when listing multiple items, "inline" for brief mentions in text.\n'
            "Do NOT write out profile fields as plain text — the directive renders a rich preview card automatically."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "username": {"type": "string", "description": "GitHub login handle."},
            },
            "required": ["username"],
        }

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload = {"bot_id": bot_id, "username": kwargs["username"]}
        return await self._post(f"{coordinator_url}/internal/github/users/get", payload)
