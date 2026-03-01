"""Google Workspace tools — Gmail, Calendar, Drive, Docs, Sheets, and Contacts."""

from nanobot.agent.tools.google.calendar import (
    GoogleCalendarCreateEventTool,
    GoogleCalendarDeleteEventTool,
    GoogleCalendarGetEventTool,
    GoogleCalendarListCalendarsTool,
    GoogleCalendarListEventsTool,
    GoogleCalendarUpdateEventTool,
)
from nanobot.agent.tools.google.contacts import (
    GoogleContactsCreateTool,
    GoogleContactsDeleteTool,
    GoogleContactsGetTool,
    GoogleContactsListTool,
    GoogleContactsSearchTool,
    GoogleContactsUpdateTool,
)
from nanobot.agent.tools.google.docs import (
    GoogleDocsAppendTool,
    GoogleDocsCreateTool,
    GoogleDocsGetTool,
    GoogleDocsInsertTool,
)
from nanobot.agent.tools.google.drive import (
    GoogleDriveCreateFolderTool,
    GoogleDriveDeleteTool,
    GoogleDriveDownloadTool,
    GoogleDriveGetTool,
    GoogleDriveListTool,
    GoogleDriveSearchTool,
    GoogleDriveShareTool,
    GoogleDriveUploadTool,
)
from nanobot.agent.tools.google.gmail import (
    GmailCreateDraftTool,
    GmailGetTool,
    GmailListLabelsTool,
    GmailListTool,
    GmailReplyTool,
    GmailSearchTool,
    GmailSendTool,
    GmailTrashTool,
)
from nanobot.agent.tools.google.sheets import (
    GoogleSheetsAppendRowsTool,
    GoogleSheetsClearRangeTool,
    GoogleSheetsCreateTool,
    GoogleSheetsGetTool,
    GoogleSheetsReadRangeTool,
    GoogleSheetsWriteRangeTool,
)

__all__ = [
    # Gmail
    "GmailSendTool",
    "GmailListTool",
    "GmailGetTool",
    "GmailSearchTool",
    "GmailReplyTool",
    "GmailTrashTool",
    "GmailCreateDraftTool",
    "GmailListLabelsTool",
    # Calendar
    "GoogleCalendarCreateEventTool",
    "GoogleCalendarListEventsTool",
    "GoogleCalendarGetEventTool",
    "GoogleCalendarUpdateEventTool",
    "GoogleCalendarDeleteEventTool",
    "GoogleCalendarListCalendarsTool",
    # Drive
    "GoogleDriveUploadTool",
    "GoogleDriveListTool",
    "GoogleDriveGetTool",
    "GoogleDriveDownloadTool",
    "GoogleDriveCreateFolderTool",
    "GoogleDriveDeleteTool",
    "GoogleDriveShareTool",
    "GoogleDriveSearchTool",
    # Docs
    "GoogleDocsCreateTool",
    "GoogleDocsGetTool",
    "GoogleDocsAppendTool",
    "GoogleDocsInsertTool",
    # Sheets
    "GoogleSheetsCreateTool",
    "GoogleSheetsGetTool",
    "GoogleSheetsReadRangeTool",
    "GoogleSheetsWriteRangeTool",
    "GoogleSheetsAppendRowsTool",
    "GoogleSheetsClearRangeTool",
    # Contacts
    "GoogleContactsListTool",
    "GoogleContactsGetTool",
    "GoogleContactsCreateTool",
    "GoogleContactsUpdateTool",
    "GoogleContactsDeleteTool",
    "GoogleContactsSearchTool",
]
