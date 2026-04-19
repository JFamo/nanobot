---
name: web
description: Web navigation and search using charlotte MCP for basic browsing and browser_use for complex interactive tasks.
always: true
---

# Web Browsing

You have two web access methods. Choose the right one for the task:

## Basic browsing — charlotte (`mcp_charlotte_*`)

Use charlotte for **simple, fast operations**: searching the web and reading page content.

### Search

```
mcp_charlotte_fetch url="https://duckduckgo.com/?q={url-encoded query}"
```

Parse the returned HTML for result titles, URLs, and snippets. Follow up by fetching individual result pages as needed.

### Fetching pages

```
mcp_charlotte_fetch url="https://example.com"
```

## Complex interactive browsing — `browser_use`

Use `browser_use` for tasks that require **real browser interaction**: logging into sites, filling forms, clicking buttons, navigating multi-step flows, interacting with JavaScript-heavy pages, or any task where you need persistent login state.

The browser **remembers your login sessions and cookies** across uses — you do not need to re-authenticate on sites you have previously logged into.

```
browser_use task="Log in to GitHub and check my notifications"
```

```
browser_use task="Fill out the contact form with the provided details" url="https://example.com/contact"
```

```
browser_use task="Navigate through the checkout flow and extract the order summary" url="https://shop.example.com/cart"
```

The `task` parameter is a natural-language description of what to do. The `url` parameter is optional — provide it when you know the starting page.

## When to use which

| Task | Tool |
|------|------|
| Search the web | `mcp_charlotte_fetch` (DuckDuckGo) |
| Read a static page | `mcp_charlotte_fetch` |
| Log in to a site | `browser_use` |
| Fill out a form | `browser_use` |
| Click through a multi-page flow | `browser_use` |
| Interact with a JavaScript-heavy app | `browser_use` |
| Any task needing persistent login state | `browser_use` |

## Rules

- Use `mcp_charlotte_*` for basic search and page fetching. Use `browser_use` for anything interactive or requiring login.
- Do not use the built-in `web_search` or `web_fetch` tools.
- Do not narrate intermediate steps or tool calls to the user. Silently perform all operations, then respond only with the final answer.
- If charlotte is unavailable, fall back to `browser_use` for all web tasks.
