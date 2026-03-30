"""GitHub gist tools via coordinator API."""

from typing import Any

from nanobot.agent.tools.github.base import GitHubBaseTool


class GitHubListGistsTool(GitHubBaseTool):

    @property
    def name(self) -> str:
        return "github_list_gists"

    @property
    def description(self) -> str:
        return (
            "List gists for the authenticated GitHub user. "
            "Authentication is automatic.\n\n"
            "DISPLAY FORMAT: Include a directive for EACH gist in your response:\n"
            '::github-gist{description="<description>" files="<filenames>" url="<html_url>" size="compact"}\n'
            "Use compact size when listing multiple gists. Replace placeholders with actual values.\n"
            'Size options: "default" for standalone results, "compact" when listing multiple items, "inline" for brief mentions in text.\n'
            "Do NOT write out gist details as plain text — the directive renders a rich preview card automatically."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "per_page": {
                    "type": "integer",
                    "description": "Maximum gists per page.",
                    "default": 10,
                },
            },
        }

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload: dict[str, Any] = {
            "bot_id": bot_id,
            "per_page": kwargs.get("per_page", 10),
        }
        return await self._post(f"{coordinator_url}/internal/github/gists/list", payload)


class GitHubCreateGistTool(GitHubBaseTool):

    @property
    def name(self) -> str:
        return "github_create_gist"

    @property
    def description(self) -> str:
        return (
            "Create a new GitHub gist with one or more files. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id. "
            "This action requires user confirmation. The UI automatically shows a preview card — "
            "do not repeat file contents in your response; a brief intro line is sufficient."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "description": {"type": "string", "description": "Gist description."},
                "files": {
                    "type": "object",
                    "description": "Map of filename to file content.",
                    "additionalProperties": {"type": "string"},
                },
                "public": {"type": "boolean", "description": "Whether the gist is public (optional)."},
            },
            "required": ["description", "files"],
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
            "description": kwargs["description"],
            "files": kwargs["files"],
        }
        if kwargs.get("public") is not None:
            payload["public"] = kwargs["public"]
        return await self._post(f"{coordinator_url}/internal/github/gists/create", payload)


class GitHubGetGistTool(GitHubBaseTool):

    @property
    def name(self) -> str:
        return "github_get_gist"

    @property
    def description(self) -> str:
        return (
            "Get a GitHub gist by ID. "
            "Authentication is automatic.\n\n"
            "DISPLAY FORMAT: Include this directive when presenting the gist:\n"
            '::github-gist{description="<description>" files="<filenames>" url="<html_url>" size="default"}\n'
            "Replace placeholders with actual values.\n"
            'Size options: "default" for standalone results, "compact" when listing multiple items, "inline" for brief mentions in text.\n'
            "Do NOT write out gist file contents as plain text — the directive renders a rich preview card automatically."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "gist_id": {"type": "string", "description": "The gist ID."},
            },
            "required": ["gist_id"],
        }

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload = {"bot_id": bot_id, "gist_id": kwargs["gist_id"]}
        return await self._post(f"{coordinator_url}/internal/github/gists/get", payload)
