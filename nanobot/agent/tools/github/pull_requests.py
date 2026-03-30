"""GitHub pull request tools via coordinator API."""

from typing import Any

from nanobot.agent.tools.github.base import GitHubBaseTool


class GitHubListPrsTool(GitHubBaseTool):

    @property
    def name(self) -> str:
        return "github_list_prs"

    @property
    def description(self) -> str:
        return (
            "List pull requests in a GitHub repository. "
            "Authentication is automatic.\n\n"
            "DISPLAY FORMAT: Include a directive for EACH pull request in your response:\n"
            '::github-pr{title="<title>" state="<state>" number="#<number>" repo="<owner>/<repo>" author="<user.login>" url="<html_url>" size="compact"}\n'
            "Use compact size when listing multiple pull requests. Replace placeholders with actual values.\n"
            'Size options: "default" for standalone results, "compact" when listing multiple items, "inline" for brief mentions in text.\n'
            "Do NOT write out pull request details as plain text — the directive renders a rich preview card automatically."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "owner": {"type": "string", "description": "Repository owner."},
                "repo": {"type": "string", "description": "Repository name."},
                "state": {"type": "string", "description": "open, closed, or all (optional)."},
                "per_page": {
                    "type": "integer",
                    "description": "Maximum pull requests per page.",
                    "default": 10,
                },
            },
            "required": ["owner", "repo"],
        }

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload: dict[str, Any] = {
            "bot_id": bot_id,
            "owner": kwargs["owner"],
            "repo": kwargs["repo"],
            "per_page": kwargs.get("per_page", 10),
        }
        if kwargs.get("state") is not None:
            payload["state"] = kwargs["state"]
        return await self._post(f"{coordinator_url}/internal/github/prs/list", payload)


class GitHubGetPrTool(GitHubBaseTool):

    @property
    def name(self) -> str:
        return "github_get_pr"

    @property
    def description(self) -> str:
        return (
            "Get a single GitHub pull request by number. "
            "Authentication is automatic.\n\n"
            "DISPLAY FORMAT: Include this directive when presenting the pull request:\n"
            '::github-pr{title="<title>" state="<state>" number="#<number>" repo="<owner>/<repo>" author="<user.login>" url="<html_url>" size="default"}\n'
            "Replace placeholders with actual values.\n"
            'Size options: "default" for standalone results, "compact" when listing multiple items, "inline" for brief mentions in text.\n'
            "Do NOT write out pull request details as plain text — the directive renders a rich preview card automatically."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "owner": {"type": "string", "description": "Repository owner."},
                "repo": {"type": "string", "description": "Repository name."},
                "pr_number": {"type": "integer", "description": "Pull request number."},
            },
            "required": ["owner", "repo", "pr_number"],
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
            "pr_number": kwargs["pr_number"],
        }
        return await self._post(f"{coordinator_url}/internal/github/prs/get", payload)


class GitHubCreatePrTool(GitHubBaseTool):

    @property
    def name(self) -> str:
        return "github_create_pr"

    @property
    def description(self) -> str:
        return (
            "Open a new pull request in a GitHub repository. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id. "
            "This action requires user confirmation. The UI automatically shows a preview card — "
            "do not repeat the pull request details in your response; a brief intro line is sufficient."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "owner": {"type": "string", "description": "Repository owner."},
                "repo": {"type": "string", "description": "Repository name."},
                "title": {"type": "string", "description": "Pull request title."},
                "head": {"type": "string", "description": "Branch name or user:branch for the changes."},
                "base": {"type": "string", "description": "Branch to merge into."},
                "body": {"type": "string", "description": "Description in Markdown (optional)."},
            },
            "required": ["owner", "repo", "title", "head", "base"],
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
            "owner": kwargs["owner"],
            "repo": kwargs["repo"],
            "title": kwargs["title"],
            "head": kwargs["head"],
            "base": kwargs["base"],
        }
        if kwargs.get("body") is not None:
            payload["body"] = kwargs["body"]
        return await self._post(f"{coordinator_url}/internal/github/prs/create", payload)


class GitHubCommentPrTool(GitHubBaseTool):

    @property
    def name(self) -> str:
        return "github_comment_pr"

    @property
    def description(self) -> str:
        return (
            "Add a comment to a GitHub pull request. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id. "
            "This action requires user confirmation. The UI automatically shows a preview card — "
            "do not repeat the comment body in your response; a brief intro line is sufficient."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "owner": {"type": "string", "description": "Repository owner."},
                "repo": {"type": "string", "description": "Repository name."},
                "pr_number": {"type": "integer", "description": "Pull request number."},
                "body": {"type": "string", "description": "Comment text in Markdown."},
            },
            "required": ["owner", "repo", "pr_number", "body"],
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
            "pr_number": kwargs["pr_number"],
            "body": kwargs["body"],
        }
        return await self._post(f"{coordinator_url}/internal/github/prs/comment", payload)


class GitHubMergePrTool(GitHubBaseTool):

    @property
    def name(self) -> str:
        return "github_merge_pr"

    @property
    def description(self) -> str:
        return (
            "Merge a GitHub pull request. "
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
                "pr_number": {"type": "integer", "description": "Pull request number."},
                "merge_method": {
                    "type": "string",
                    "description": "merge, squash, or rebase.",
                    "default": "merge",
                },
            },
            "required": ["owner", "repo", "pr_number"],
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
            "owner": kwargs["owner"],
            "repo": kwargs["repo"],
            "pr_number": kwargs["pr_number"],
            "merge_method": kwargs.get("merge_method", "merge"),
        }
        return await self._post(f"{coordinator_url}/internal/github/prs/merge", payload)
