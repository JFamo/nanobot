---
name: web
description: Web navigation, search, and interactive browsing using persistent browser sessions.
always: true
---

# Web Browsing

All web access uses the `browser_use` and `browser_search` tools. These tools control a real browser that **remembers your login sessions and cookies** — you do not need to re-authenticate on sites you have previously logged into.

## Searching the web

Use `browser_search` for web searches:

```
browser_search query="your search query" max_results=10
```

## Interactive browsing

Use `browser_use` for any interactive web task — reading pages, filling forms, clicking buttons, logging in, navigating multi-page flows:

```
browser_use task="Go to example.com and extract the main article text" url="https://example.com"
```

```
browser_use task="Log in to GitHub with the credentials on screen and check notifications"
```

```
browser_use task="Navigate to the pricing page and extract the plan details" url="https://example.com"
```

The `task` parameter is a natural-language description of what to do. The `url` parameter is optional — provide it when you know the starting page.

## Rules

- Always use `browser_use` or `browser_search` for all web tasks — never the built-in `web_search` or `web_fetch`.
- Do not narrate intermediate steps or tool calls to the user. Silently perform all search and fetch operations, then respond only with the final answer.
- The browser persists login state. If you have previously logged into a site, you are still logged in.
- For simple searches, prefer `browser_search`. For everything else (reading pages, interacting with forms, navigating dynamic sites), use `browser_use`.
