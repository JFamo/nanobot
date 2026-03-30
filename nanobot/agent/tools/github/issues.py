"""GitHub issue tools via coordinator API."""

from typing import Any

from nanobot.agent.tools.github.base import GitHubBaseTool


class GitHubListIssuesTool(GitHubBaseTool):

    @property
    def name(self) -> str:
        return "github_list_issues"

    @property
    def description(self) -> str:
        return (
            "List issues in a GitHub repository. "
            "Authentication is automatic.\n\n"
            "DISPLAY FORMAT: Include a directive for EACH issue in your response:\n"
            '::github-issue{title="<title>" state="<state>" number="#<number>" repo="<owner>/<repo>" author="<user.login>" url="<html_url>" labels="<labels>" size="compact"}\n'
            "Use compact size when listing multiple issues. Replace placeholders with actual values.\n"
            'Size options: "default" for standalone results, "compact" when listing multiple items, "inline" for brief mentions in text.\n'
            "Do NOT write out issue details as plain text — the directive renders a rich preview card automatically."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "owner": {"type": "string", "description": "Repository owner."},
                "repo": {"type": "string", "description": "Repository name."},
                "state": {
                    "type": "string",
                    "description": "Issue state filter: open, closed, or all.",
                    "default": "open",
                },
                "per_page": {
                    "type": "integer",
                    "description": "Maximum issues per page.",
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
            "state": kwargs.get("state", "open"),
            "per_page": kwargs.get("per_page", 10),
        }
        return await self._post(f"{coordinator_url}/internal/github/issues/list", payload)


class GitHubGetIssueTool(GitHubBaseTool):

    @property
    def name(self) -> str:
        return "github_get_issue"

    @property
    def description(self) -> str:
        return (
            "Get a single GitHub issue by number. "
            "Authentication is automatic.\n\n"
            "DISPLAY FORMAT: Include this directive when presenting the issue:\n"
            '::github-issue{title="<title>" state="<state>" number="#<number>" repo="<owner>/<repo>" author="<user.login>" url="<html_url>" labels="<labels>" size="default"}\n'
            "Replace placeholders with actual values.\n"
            'Size options: "default" for standalone results, "compact" when listing multiple items, "inline" for brief mentions in text.\n'
            "Do NOT write out issue details as plain text — the directive renders a rich preview card automatically."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "owner": {"type": "string", "description": "Repository owner."},
                "repo": {"type": "string", "description": "Repository name."},
                "issue_number": {"type": "integer", "description": "Issue number."},
            },
            "required": ["owner", "repo", "issue_number"],
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
            "issue_number": kwargs["issue_number"],
        }
        return await self._post(f"{coordinator_url}/internal/github/issues/get", payload)


class GitHubCreateIssueTool(GitHubBaseTool):

    @property
    def name(self) -> str:
        return "github_create_issue"

    @property
    def description(self) -> str:
        return (
            "Create a new issue in a GitHub repository. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id. "
            "This action requires user confirmation. The UI automatically shows a preview card — "
            "do not repeat the issue details or include display directives in your response; a brief intro line is sufficient."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "owner": {"type": "string", "description": "Repository owner."},
                "repo": {"type": "string", "description": "Repository name."},
                "title": {"type": "string", "description": "Issue title."},
                "body": {"type": "string", "description": "Issue body in Markdown (optional)."},
                "labels": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Label names to apply (optional).",
                },
            },
            "required": ["owner", "repo", "title"],
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
        }
        if kwargs.get("body") is not None:
            payload["body"] = kwargs["body"]
        if kwargs.get("labels") is not None:
            payload["labels"] = kwargs["labels"]
        return await self._post(f"{coordinator_url}/internal/github/issues/create", payload)


class GitHubUpdateIssueTool(GitHubBaseTool):

    @property
    def name(self) -> str:
        return "github_update_issue"

    @property
    def description(self) -> str:
        return (
            "Update an existing GitHub issue (title, body, or state). "
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
                "issue_number": {"type": "integer", "description": "Issue number."},
                "title": {"type": "string", "description": "New title (optional)."},
                "body": {"type": "string", "description": "New body (optional)."},
                "state": {"type": "string", "description": "open or closed (optional)."},
            },
            "required": ["owner", "repo", "issue_number"],
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
            "issue_number": kwargs["issue_number"],
        }
        if kwargs.get("title") is not None:
            payload["title"] = kwargs["title"]
        if kwargs.get("body") is not None:
            payload["body"] = kwargs["body"]
        if kwargs.get("state") is not None:
            payload["state"] = kwargs["state"]
        return await self._post(f"{coordinator_url}/internal/github/issues/update", payload)


class GitHubCommentIssueTool(GitHubBaseTool):

    @property
    def name(self) -> str:
        return "github_comment_issue"

    @property
    def description(self) -> str:
        return (
            "Add a comment to a GitHub issue. "
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
                "issue_number": {"type": "integer", "description": "Issue number."},
                "body": {"type": "string", "description": "Comment text in Markdown."},
            },
            "required": ["owner", "repo", "issue_number", "body"],
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
            "issue_number": kwargs["issue_number"],
            "body": kwargs["body"],
        }
        return await self._post(f"{coordinator_url}/internal/github/issues/comment", payload)


class GitHubCloseIssueTool(GitHubBaseTool):

    @property
    def name(self) -> str:
        return "github_close_issue"

    @property
    def description(self) -> str:
        return (
            "Close a GitHub issue. "
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
                "issue_number": {"type": "integer", "description": "Issue number."},
            },
            "required": ["owner", "repo", "issue_number"],
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
            "issue_number": kwargs["issue_number"],
        }
        return await self._post(f"{coordinator_url}/internal/github/issues/close", payload)
