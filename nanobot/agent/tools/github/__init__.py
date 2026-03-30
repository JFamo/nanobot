"""GitHub tools — repos, issues, pull requests, users, and gists."""

from nanobot.agent.tools.github.gists import (
    GitHubCreateGistTool,
    GitHubGetGistTool,
    GitHubListGistsTool,
)
from nanobot.agent.tools.github.issues import (
    GitHubCloseIssueTool,
    GitHubCommentIssueTool,
    GitHubCreateIssueTool,
    GitHubGetIssueTool,
    GitHubListIssuesTool,
    GitHubUpdateIssueTool,
)
from nanobot.agent.tools.github.pull_requests import (
    GitHubCommentPrTool,
    GitHubCreatePrTool,
    GitHubGetPrTool,
    GitHubListPrsTool,
    GitHubMergePrTool,
)
from nanobot.agent.tools.github.repos import (
    GitHubCreateRepoTool,
    GitHubGetRepoTool,
    GitHubListReposTool,
    GitHubSearchReposTool,
    GitHubStarRepoTool,
    GitHubUnstarRepoTool,
)
from nanobot.agent.tools.github.users import (
    GitHubGetMeTool,
    GitHubGetUserTool,
)

__all__ = [
    "GitHubListReposTool",
    "GitHubGetRepoTool",
    "GitHubCreateRepoTool",
    "GitHubSearchReposTool",
    "GitHubStarRepoTool",
    "GitHubUnstarRepoTool",
    "GitHubListIssuesTool",
    "GitHubGetIssueTool",
    "GitHubCreateIssueTool",
    "GitHubUpdateIssueTool",
    "GitHubCommentIssueTool",
    "GitHubCloseIssueTool",
    "GitHubListPrsTool",
    "GitHubGetPrTool",
    "GitHubCreatePrTool",
    "GitHubCommentPrTool",
    "GitHubMergePrTool",
    "GitHubGetMeTool",
    "GitHubGetUserTool",
    "GitHubListGistsTool",
    "GitHubCreateGistTool",
    "GitHubGetGistTool",
]
