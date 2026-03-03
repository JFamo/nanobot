# nanobot — Claude Instructions

## Auto-commit policy

After making any substantial change, automatically commit without asking. Use conventional prefixes (`fix:`, `feat:`, `chore:`, `refactor:`).

## Quick reference

```bash
# Run a single command
nanobot agent -m "Hello"

# Start the gateway (HTTP API + channels + cron)
nanobot gateway --api-key <key>

# Build Docker image (from ../fairy-bot-e2e/ for e2e testing)
make build
```

## Gateway architecture

`nanobot gateway` starts:
1. An **aiohttp HTTP server** on port 18790 (`POST /agent/run` with bearer auth)
2. The **agent loop** (`AgentLoop.run()`) — connects MCP servers, processes messages
3. **Channel managers** (telegram relay, etc.)
4. **CronService** + **HeartbeatService**

All four run under `asyncio.gather`. If any raises an unhandled exception the entire gateway exits (restart policy: `unless-stopped`).

The log line `"Gateway HTTP API listening on port 18790"` appears immediately after the HTTP server binds, before MCP init. This is the correct health signal — docker status `running` lags behind.

## Cron jobs

- Jobs are persisted to `~/.nanobot/cron/jobs.json`
- `CronService` loads them at startup and runs them in-memory
- When a job fires, `on_cron_job` calls `agent.process_direct()` with:
  - **Session key**: `{channel}:{chat_id}` (the user's real session, so the agent has personality and history)
  - **Message**: `[SCHEDULED REMINDER] A reminder you scheduled is now due. Deliver this message to the user in your own voice: {original_message}`
- `every_seconds` is for recurring jobs only; use `at` with an ISO datetime for one-time reminders

## Common crash causes in e2e

| Symptom | Root cause | Fix |
|---|---|---|
| Gateway exits ~300ms after start | MCP host unreachable (e.g. `charlotte`) | Set `CHARLOTTE_MCP_URL=` in `.env.test` |
| Gateway exits, telegram relay log shows `nanobot-coordinator` | Wrong coordinator hostname | Set `NANOBOT_COORDINATOR_URL=http://e2e-coordinator:8000` |
| `NameError: cannot access free variable 'logger'` | `logger` imported inside `if verbose:` block but used outside | Import `from loguru import logger` before the `if verbose:` check in `gateway()` |
| ConnectError on chat after container shows "running" | HTTP server not yet bound | Wait for log line `"Gateway HTTP API listening on port"` instead of sleeping |

## E2E testing

Tests live in `../fairy-bot-e2e/`. After nanobot changes:

```bash
cd ../fairy-bot-e2e
make build   # rebuilds nanobot:latest
make up      # restarts stack
make test    # runs Playwright tests
```

Use `bot-helpers.ts` functions (`waitForBotHealthy`, `getContainerLogs`, etc.) — see `fairy-bot-e2e/CLAUDE.md` for the full reference.
