"""Unit tests for the tool confirmation security framework."""

from pathlib import Path

import pytest

from nanobot.agent.types import AgentResponse, PendingAction
from nanobot.agent.tools.filesystem import EditFileTool, ListDirTool, ReadFileTool, WriteFileTool
from nanobot.agent.tools.google import (
    GmailCreateDraftTool,
    GmailGetTool,
    GmailListLabelsTool,
    GmailListTool,
    GmailReplyTool,
    GmailSearchTool,
    GmailSendTool,
    GmailTrashTool,
    GoogleCalendarCreateEventTool,
    GoogleCalendarDeleteEventTool,
    GoogleCalendarGetEventTool,
    GoogleCalendarListCalendarsTool,
    GoogleCalendarListEventsTool,
    GoogleCalendarUpdateEventTool,
    GoogleContactsCreateTool,
    GoogleContactsDeleteTool,
    GoogleContactsGetTool,
    GoogleContactsListTool,
    GoogleContactsSearchTool,
    GoogleContactsUpdateTool,
    GoogleDocsAppendTool,
    GoogleDocsCreateTool,
    GoogleDocsGetTool,
    GoogleDocsInsertTool,
    GoogleDriveCreateFolderTool,
    GoogleDriveDeleteTool,
    GoogleDriveDownloadTool,
    GoogleDriveGetTool,
    GoogleDriveListTool,
    GoogleDriveSearchTool,
    GoogleDriveShareTool,
    GoogleDriveUploadTool,
    GoogleSheetsAppendRowsTool,
    GoogleSheetsClearRangeTool,
    GoogleSheetsCreateTool,
    GoogleSheetsGetTool,
    GoogleSheetsReadRangeTool,
    GoogleSheetsWriteRangeTool,
)
from nanobot.agent.tools.shell import ExecTool
from nanobot.agent.tools.web import WebFetchTool
from nanobot.agent.tools.x import (
    XAddListMemberTool,
    XBookmarkTweetTool,
    XCreateListTool,
    XDeleteListTool,
    XDeleteTweetTool,
    XFollowUserTool,
    XGetBookmarksTool,
    XGetDmConversationTool,
    XGetDmEventsTool,
    XGetLikedTweetsTool,
    XGetListTool,
    XGetMeTool,
    XGetOwnedListsTool,
    XGetTweetTool,
    XGetUserByIdTool,
    XGetUserByUsernameTool,
    XGetUserMentionsTool,
    XGetUserTweetsTool,
    XGetFollowersTool,
    XGetFollowingTool,
    XLikeTweetTool,
    XPostTweetTool,
    XRemoveBookmarkTool,
    XRemoveListMemberTool,
    XRetweetTool,
    XSearchTweetsTool,
    XSendDmTool,
    XUndoRetweetTool,
    XUnfollowUserTool,
    XUnlikeTweetTool,
)

# Tools that require user confirmation before execution (mutating/sensitive actions)
CONFIRMATION_REQUIRED_TOOLS = [
    # Google
    GmailSendTool,
    GmailReplyTool,
    GmailTrashTool,
    GmailCreateDraftTool,
    GoogleCalendarCreateEventTool,
    GoogleCalendarUpdateEventTool,
    GoogleCalendarDeleteEventTool,
    GoogleDriveUploadTool,
    GoogleDriveCreateFolderTool,
    GoogleDriveDeleteTool,
    GoogleDriveShareTool,
    GoogleDocsCreateTool,
    GoogleDocsAppendTool,
    GoogleDocsInsertTool,
    GoogleSheetsCreateTool,
    GoogleSheetsWriteRangeTool,
    GoogleSheetsAppendRowsTool,
    GoogleSheetsClearRangeTool,
    GoogleContactsCreateTool,
    GoogleContactsUpdateTool,
    GoogleContactsDeleteTool,
    # X
    XPostTweetTool,
    XDeleteTweetTool,
    XLikeTweetTool,
    XUnlikeTweetTool,
    XRetweetTool,
    XUndoRetweetTool,
    XFollowUserTool,
    XUnfollowUserTool,
    XBookmarkTweetTool,
    XRemoveBookmarkTool,
    XCreateListTool,
    XDeleteListTool,
    XAddListMemberTool,
    XRemoveListMemberTool,
    XSendDmTool,
    # Local
    ExecTool,
    WriteFileTool,
    EditFileTool,
]

# Read-only tools (should NOT require confirmation)
READ_ONLY_TOOLS = [
    # Google
    GmailListTool,
    GmailGetTool,
    GmailSearchTool,
    GmailListLabelsTool,
    GoogleCalendarListEventsTool,
    GoogleCalendarGetEventTool,
    GoogleCalendarListCalendarsTool,
    GoogleDriveListTool,
    GoogleDriveGetTool,
    GoogleDriveDownloadTool,
    GoogleDriveSearchTool,
    GoogleDocsGetTool,
    GoogleSheetsGetTool,
    GoogleSheetsReadRangeTool,
    GoogleContactsListTool,
    GoogleContactsGetTool,
    GoogleContactsSearchTool,
    # X
    XGetTweetTool,
    XSearchTweetsTool,
    XGetUserTweetsTool,
    XGetUserMentionsTool,
    XGetLikedTweetsTool,
    XGetMeTool,
    XGetUserByIdTool,
    XGetUserByUsernameTool,
    XGetFollowersTool,
    XGetFollowingTool,
    XGetBookmarksTool,
    XGetListTool,
    XGetOwnedListsTool,
    XGetDmEventsTool,
    XGetDmConversationTool,
    # Local
    ReadFileTool,
    ListDirTool,
    WebFetchTool,
]


def _instantiate_tool(cls):
    """Instantiate a tool with the correct constructor arguments."""
    if cls in (ReadFileTool, WriteFileTool, EditFileTool, ListDirTool):
        return cls(workspace=Path("/tmp"))
    if cls is ExecTool:
        return ExecTool(working_dir="/tmp")
    return cls()


class TestToolClassification:
    """Tests for tool confirmation classification."""

    def test_exactly_39_tools_require_confirmation(self):
        """Verify exactly 39 tools have requires_confirmation=True."""
        assert len(CONFIRMATION_REQUIRED_TOOLS) == 39
        requiring = [
            cls for cls in CONFIRMATION_REQUIRED_TOOLS
            if _instantiate_tool(cls).requires_confirmation
        ]
        assert len(requiring) == 39, (
            f"Expected 39 tools with requires_confirmation=True, got {len(requiring)}. "
            f"Missing: {[c.__name__ for c in CONFIRMATION_REQUIRED_TOOLS if c not in requiring]}"
        )

    def test_read_only_tools_do_not_require_confirmation(self):
        """Verify read-only tools have requires_confirmation=False."""
        for cls in READ_ONLY_TOOLS:
            tool = _instantiate_tool(cls)
            assert not tool.requires_confirmation, (
                f"{cls.__name__} should not require confirmation (read-only)"
            )

    def test_total_confirmation_count_matches_expected(self):
        """Verify total tools and that exactly 39 require confirmation."""
        all_tools = CONFIRMATION_REQUIRED_TOOLS + READ_ONLY_TOOLS
        assert len(all_tools) == 39 + len(READ_ONLY_TOOLS)
        requiring = sum(
            1 for cls in all_tools
            if _instantiate_tool(cls).requires_confirmation
        )
        assert requiring == 39


class TestAgentResponse:
    """Tests for AgentResponse dataclass."""

    def test_construct_with_content_and_pending_actions(self):
        """AgentResponse can be constructed with content and pending_actions."""
        action = PendingAction(
            action_id="a1",
            tool_call_id="tc1",
            tool_name="write_file",
            arguments={"path": "/tmp/x", "content": "hello"},
        )
        resp = AgentResponse(content="Done", pending_actions=[action])
        assert resp.content == "Done"
        assert len(resp.pending_actions) == 1
        assert resp.pending_actions[0].tool_name == "write_file"

    def test_pending_actions_defaults_to_empty_list(self):
        """pending_actions defaults to empty list when not provided."""
        resp = AgentResponse(content="Hello")
        assert resp.content == "Hello"
        assert resp.pending_actions == []


class TestPendingAction:
    """Tests for PendingAction dataclass."""

    def test_stores_all_fields_correctly(self):
        """PendingAction stores action_id, tool_call_id, tool_name, and arguments."""
        action = PendingAction(
            action_id="act-123",
            tool_call_id="call-456",
            tool_name="exec",
            arguments={"command": "ls -la"},
        )
        assert action.action_id == "act-123"
        assert action.tool_call_id == "call-456"
        assert action.tool_name == "exec"
        assert action.arguments == {"command": "ls -la"}
