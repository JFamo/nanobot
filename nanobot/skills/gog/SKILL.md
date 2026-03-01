---
name: gog
description: Google Workspace actions (Gmail, Calendar, Drive) via the google tool. Use for sending emails, creating calendar events, or uploading files to Drive.
always: true
---

# Google Workspace (gog)

You can send emails, create calendar events, and upload files to Google Drive using the **`google` tool**.

## How to use

**ALWAYS use the native `google` tool** — call it directly as a tool call with the parameters below. **NEVER use `exec`, `node -e`, axios, curl, or any shell command for Google actions.** The native tool handles authentication and avoids shell-escaping issues with special characters.

Call the `google` tool with `action` set to one of:
- `gmail_send` — send an email
- `calendar_create_event` — create a calendar event
- `drive_upload` — upload a file to Google Drive

Authentication is fully automatic. **Never ask the user for credentials, tokens, bot_id, user_id, or coordinator URL.**

---

## Gmail: Send Email

**Required parameters**: `action`, `to`, `subject`, `body`

Example:
```json
{
  "action": "gmail_send",
  "to": "recipient@example.com",
  "subject": "Meeting follow-up",
  "body": "Thanks for attending the meeting today."
}
```

---

## Calendar: Create Event

**Required parameters**: `action`, `summary`, `start`, `end`
**Optional**: `attendees`, `location`, `event_description`

All times must be ISO 8601 with timezone offset.

Example:
```json
{
  "action": "calendar_create_event",
  "summary": "Team standup",
  "start": "2026-03-06T18:00:00-05:00",
  "end": "2026-03-06T20:00:00-05:00",
  "attendees": ["alice@example.com"],
  "location": "Boston, MA",
  "event_description": "Weekly sync"
}
```

**Timezone conversions**:
- EST = `-05:00`
- CST = `-06:00`
- PST = `-08:00`
- UTC = `Z`

---

## Drive: Upload File

**Required parameters**: `action`, `file_name`, `mime_type`, `file_path`

Example:
```json
{
  "action": "drive_upload",
  "file_name": "report.pdf",
  "mime_type": "application/pdf",
  "file_path": "/path/to/report.pdf"
}
```

---

## Error handling

| Error | Meaning | What to do |
|-------|---------|------------|
| Google account not linked | 404 from coordinator | Tell user to link their Google account in bot settings |
| Token expired / revoked | 401 / 403 | Tell user to re-link their Google account |
| Request timed out | Network issue | Retry once; if it persists, report the error |

---

## Before you act

1. Gather all the required information from the user's message.
2. **Confirm the action with the user** before calling the tool — repeat back the key details.
3. Call the `google` tool.
4. Report the result (share event link, confirm email was sent, etc.).
