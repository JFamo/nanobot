---
name: gog
description: Google Workspace actions via internal coordinator endpoints (Gmail, Calendar, Drive).
---

# Google Workspace Actions

Use internal coordinator endpoints for Gmail, Calendar, and Drive operations. OAuth is handled centrally — you never manage tokens.

## Environment

Two env vars are injected automatically:
- `COORDINATOR_URL` — base URL of control server (e.g. `http://nanobot-coordinator:8000`)
- `INTERNAL_SERVICE_TOKEN` — bearer token for internal auth

## Gmail: Send Email

```bash
node -e "
const axios = require('axios');
axios.post(process.env.COORDINATOR_URL + '/internal/google/gmail/send', {
  user_id: '<user_id>',
  to: 'recipient@example.com',
  subject: 'Hello from nanobot',
  body: 'This is the email body.'
}, {
  headers: { 'Authorization': 'Bearer ' + process.env.INTERNAL_SERVICE_TOKEN }
}).then(r => console.log(JSON.stringify(r.data)))
  .catch(e => console.error(e.response?.data || e.message));
"
```

Response: `{"success": true, "message_id": "...", "thread_id": "..."}`

## Drive: Upload File

```bash
node -e "
const axios = require('axios');
const fs = require('fs');
const fileBuffer = fs.readFileSync('/path/to/file.pdf').toString('base64');
axios.post(process.env.COORDINATOR_URL + '/internal/google/drive/upload', {
  user_id: '<user_id>',
  file_name: 'report.pdf',
  mime_type: 'application/pdf',
  file_buffer: fileBuffer
}, {
  headers: { 'Authorization': 'Bearer ' + process.env.INTERNAL_SERVICE_TOKEN }
}).then(r => console.log(JSON.stringify(r.data)))
  .catch(e => console.error(e.response?.data || e.message));
"
```

Response: `{"success": true, "file_id": "...", "web_view_link": "..."}`

## Calendar: Create Event

```bash
node -e "
const axios = require('axios');
axios.post(process.env.COORDINATOR_URL + '/internal/google/calendar/create-event', {
  user_id: '<user_id>',
  summary: 'Team standup',
  start: '2026-03-02T10:00:00Z',
  end: '2026-03-02T10:30:00Z',
  attendees: ['alice@example.com', 'bob@example.com']
}, {
  headers: { 'Authorization': 'Bearer ' + process.env.INTERNAL_SERVICE_TOKEN }
}).then(r => console.log(JSON.stringify(r.data)))
  .catch(e => console.error(e.response?.data || e.message));
"
```

Response: `{"success": true, "event_id": "...", "html_link": "..."}`

## Notes

- Replace `<user_id>` with the authenticated user's ID (provided by the coordinator when invoking the agent).
- All datetime fields use ISO 8601 format with timezone (prefer UTC with `Z` suffix).
- If a call fails with 401, the user has not linked their Google account yet.
- Confirm with the user before sending emails or creating calendar events.
- Use `exec` to run node one-liners. axios is available via `require('axios')` in any node script.
