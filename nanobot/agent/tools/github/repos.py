"""GitHub repository tools via coordinator API."""

from typing import Any

from nanobot.agent.tools.github.base import GitHubBaseTool


class GitHubListReposTool(GitHubBaseTool):

    @property
    def name(self) -> str:
        return "github_list_repos"

    @property
    def description(self) -> str:
        return (
            "List repositories accessible to the authenticated GitHub user. "
            "Authentication is automatic.\n\n"
            "DISPLAY FORMAT: Include a directive for EACH repository in your response:\n"
            '::github-repo{name="<full_name>" description="<description>" stars="<stargazers_count>" language="<language>" url="<html_url>" size="compact"}\n'
            "Use compact size when listing multiple repositories. Replace placeholders with actual values.\n"
            'Size options: "default" for standalone results, "compact" when listing multiple items, "inline" for brief mentions in text.\n'
            "Do NOT write out repository details as plain text — the directive renders a rich preview card automatically."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "sort": {
                    "type": "string",
                    "description": "Sort field (e.g. updated, created, pushed, full_name).",
                    "default": "updated",
                },
                "per_page": {
                    "type": "integer",
                    "description": "Maximum repositories per page.",
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
            "sort": kwargs.get("sort", "updated"),
            "per_page": kwargs.get("per_page", 10),
        }
        return await self._post(f"{coordinator_url}/internal/github/repos/list", payload)


class GitHubGetRepoTool(GitHubBaseTool):

    @property
    def name(self) -> str:
        return "github_get_repo"

    @property
    def description(self) -> str:
        return (
            "Get full metadata for a GitHub repository by owner and name. "
            "Authentication is automatic.\n\n"
            "DISPLAY FORMAT: Include this directive when presenting the repository:\n"
            '::github-repo{name="<full_name>" description="<description>" stars="<stargazers_count>" language="<language>" url="<html_url>" size="default"}\n'
            "Replace placeholders with actual values.\n"
            'Size options: "default" for standalone results, "compact" when listing multiple items, "inline" for brief mentions in text.\n'
            "Do NOT write out repository details as plain text — the directive renders a rich preview card automatically."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "owner": {"type": "string", "description": "Repository owner (user or organization)."},
                "repo": {"type": "string", "description": "Repository name."},
            },
            "required": ["owner", "repo"],
        }

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload = {
            "bot_id": bot_id,
            "owner": kwargs["owner"],
            "repo": kwargs["repo"],
        }
        return await self._post(f"{coordinator_url}/internal/github/repos/get", payload)


class GitHubCreateRepoTool(GitHubBaseTool):

    @property
    def name(self) -> str:
        return "github_create_repo"

    @property
    def description(self) -> str:
        return (
            "Create a new GitHub repository for the authenticated user. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id. "
            "This action requires user confirmation. The UI automatically shows a preview card — "
            "do not repeat the repository details or include display directives in your response; a brief intro line is sufficient."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Repository name."},
                "description": {"type": "string", "description": "Short description (optional)."},
                "private": {"type": "boolean", "description": "Whether the repository is private (optional)."},
            },
            "required": ["name"],
        }

    @property
    def requires_confirmation(self) -> bool:
        return True

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload: dict[str, Any] = {"bot_id": bot_id, "name": kwargs["name"]}
        if kwargs.get("description") is not None:
            payload["description"] = kwargs["description"]
        if kwargs.get("private") is not None:
            payload["private"] = kwargs["private"]
        return await self._post(f"{coordinator_url}/internal/github/repos/create", payload)


class GitHubSearchReposTool(GitHubBaseTool):

    @property
    def name(self) -> str:
        return "github_search_repos"

    @property
    def description(self) -> str:
        return (
            "Search GitHub repositories with a query string. "
            "Authentication is automatic.\n\n"
            "DISPLAY FORMAT: Include a directive for EACH matching repository in your response:\n"
            '::github-repo{name="<full_name>" description="<description>" stars="<stargazers_count>" language="<language>" url="<html_url>" size="compact"}\n'
            "Use compact size when listing multiple repositories. Replace placeholders with actual values.\n"
            'Size options: "default" for standalone results, "compact" when listing multiple items, "inline" for brief mentions in text.\n'
            "Do NOT write out repository details as plain text — the directive renders a rich preview card automatically."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "GitHub search query for repositories."},
                "per_page": {
                    "type": "integer",
                    "description": "Maximum results per page.",
                    "default": 10,
                },
            },
            "required": ["query"],
        }

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload: dict[str, Any] = {
            "bot_id": bot_id,
            "query": kwargs["query"],
            "per_page": kwargs.get("per_page", 10),
        }
        return await self._post(f"{coordinator_url}/internal/github/repos/search", payload)


class GitHubStarRepoTool(GitHubBaseTool):

    @property
    def name(self) -> str:
        return "github_star_repo"

    @property
    def description(self) -> str:
        return (
            "Star a GitHub repository. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id. "
            "This action requires user confirmation. The UI shows a preview — do not repeat the action details in your response."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "owner": {"type": "string", "description": "Repository owner."},
                "repo": {"type": "string", "description": "Repository name."},
            },
            "required": ["owner", "repo"],
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
            "owner": kwargs["owner"],
            "repo": kwargs["repo"],
        }
        return await self._post(f"{coordinator_url}/internal/github/repos/star", payload)


class GitHubUnstarRepoTool(GitHubBaseTool):

    @property
    def name(self) -> str:
        return "github_unstar_repo"

    @property
    def description(self) -> str:
        return (
            "Remove your star from a GitHub repository. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id. "
            "This action requires user confirmation. The UI shows a preview — do not repeat the action details in your response."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "owner": {"type": "string", "description": "Repository owner."},
                "repo": {"type": "string", "description": "Repository name."},
            },
            "required": ["owner", "repo"],
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
            "owner": kwargs["owner"],
            "repo": kwargs["repo"],
        }
        return await self._post(f"{coordinator_url}/internal/github/repos/unstar", payload)
