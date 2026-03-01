---
name: gog
description: Google Workspace actions (Gmail, Calendar, Drive) via coordinator. Use for sending emails, creating calendar events, or uploading files to Drive.
---

# Google Workspace (gog)

This skill lets you send emails, create calendar events, and upload files to Google Drive on behalf of the user.

## IMPORTANT: How this skill works

This is **not** a native tool. You execute it by running Node.js one-liners with the `exec` tool.

All required connection details are already available as environment variables — **never ask the user for any of these**:

| Variable | What it is |
|----------|------------|
| `process.env.COORDINATOR_URL` | Base URL of the coordinator server |
| `process.env.BOT_ID` | Your bot identity (used to look up the user's Google account) |

If the user's Google account is not linked yet, you will receive a `404` error. Tell the user to link their Google account via the bot configuration and do not retry.

---

## Before you act

1. Gather all required information from the user's message (see each section below).
2. **Always confirm the action with the user** before executing — repeat back the key details.
3. Use `exec` to run the node one-liner.
4. Report back the result clearly (e.g., share the calendar event link, confirm email was sent).

---

## Gmail: Send Email

**Required**: `to`, `subject`, `body`

```bash
node -e "
const axios = require('axios');
axios.post(process.env.COORDINATOR_URL + '/internal/google/gmail/send', {
  bot_id: process.env.BOT_ID,
  to: 'recipient@example.com',
  subject: 'Subject here',
  body: 'Email body here.'
}).then(r => console.log(JSON.stringify(r.data)))
  .catch(e => console.error(e.response?.data || e.message));
"
```

Response: `{"success": true, "message_id": "...", "thread_id": "..."}`

---

## Calendar: Create Event

**Required**: `summary`, `start`, `end`  
**Optional**: `attendees` (array of emails), `location` (string), `description` (string)

All times must be ISO 8601 with timezone (e.g., `2026-03-01T21:00:00-05:00` for 9 PM EST).

```bash
node -e "
const axios = require('axios');
axios.post(process.env.COORDINATOR_URL + '/internal/google/calendar/create-event', {
  bot_id: process.env.BOT_ID,
  summary: 'Team standup',
  start: '2026-03-02T10:00:00Z',
  end: '2026-03-02T10:30:00Z',
  attendees: ['alice@example.com', 'bob@example.com'],
  location: 'New York, NY',
  description: 'Weekly sync'
}).then(r => console.log(JSON.stringify(r.data)))
  .catch(e => console.error(e.response?.data || e.message));
"
```

Response: `{"success": true, "event_id": "...", "html_link": "...", "summary": "..."}`

**Timezone tip**: Convert user-provided times to ISO 8601 with explicit offset. For example:
- 9 PM EST → `T21:00:00-05:00`
- 9 PM PST → `T21:00:00-08:00`
- 9 PM UTC → `T21:00:00Z`

---

## Drive: Upload File

**Required**: `file_name`, `mime_type`, `file_buffer` (base64-encoded content)

```bash
node -e "
const axios = require('axios');
const fs = require('fs');
const fileBuffer = fs.readFileSync('/path/to/file.pdf').toString('base64');
axios.post(process.env.COORDINATOR_URL + '/internal/google/drive/upload', {
  bot_id: process.env.BOT_ID,
  file_name: 'report.pdf',
  mime_type: 'application/pdf',
  file_buffer: fileBuffer
}).then(r => console.log(JSON.stringify(r.data)))
  .catch(e => console.error(e.response?.data || e.message));
"
```

Response: `{"success": true, "file_id": "...", "web_view_link": "..."}`

---

## Error handling

| Error | Meaning | What to do |
|-------|---------|------------|
| `404` | Google account not linked for this bot | Tell user to link their Google account in bot settings |
| `401` / `403` | Google token expired or revoked | Tell user to re-link their Google account |
| Network error | Coordinator unreachable | Retry once; if it persists, report the error |

---

## Workflow examples

### "Send an email to john@example.com saying the meeting is at 3pm"

1. Confirm: "I'll send an email to john@example.com with subject '...' and body '...'. Shall I proceed?"
2. On confirmation, run the Gmail one-liner.
3. Report: "Email sent successfully."

### "Create a calendar event for our team lunch tomorrow at noon for 1 hour"

1. Determine the date and timezone from context (check memory or ask once if unknown).
2. Confirm: "I'll create 'Team Lunch' on [date] from 12:00 PM to 1:00 PM [timezone]. Should I add any attendees?"
3. Run the Calendar one-liner.
4. Report: "Event created! Here's the link: [html_link]"
