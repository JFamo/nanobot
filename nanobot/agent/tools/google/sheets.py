"""Google Sheets tools — create, get, read, write, append, clear via the coordinator API."""

from typing import Any

from nanobot.agent.tools.google.base import GoogleBaseTool


class GoogleSheetsCreateTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "sheets_create"

    @property
    def description(self) -> str:
        return (
            "Create a new Google Spreadsheet with a given title. Returns the spreadsheet ID and URL. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Title for the new spreadsheet.",
                },
            },
            "required": ["title"],
        }

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload = {"bot_id": bot_id, "title": kwargs["title"]}
        return await self._post(f"{coordinator_url}/internal/google/sheets/create", payload)


class GoogleSheetsGetTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "sheets_get"

    @property
    def description(self) -> str:
        return (
            "Get metadata for a Google Spreadsheet, including sheet names and dimensions. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "spreadsheet_id": {
                    "type": "string",
                    "description": "The Google Spreadsheet ID (from the URL).",
                },
            },
            "required": ["spreadsheet_id"],
        }

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload = {"bot_id": bot_id, "spreadsheet_id": kwargs["spreadsheet_id"]}
        return await self._post(f"{coordinator_url}/internal/google/sheets/get", payload)


class GoogleSheetsReadRangeTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "sheets_read_range"

    @property
    def description(self) -> str:
        return (
            "Read cell values from a range in a Google Spreadsheet using A1 notation "
            "(e.g. 'Sheet1!A1:D10'). Returns a 2D array of values. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "spreadsheet_id": {
                    "type": "string",
                    "description": "The Google Spreadsheet ID.",
                },
                "range_notation": {
                    "type": "string",
                    "description": "A1 notation range, e.g. 'Sheet1!A1:D10' or 'A1:B5'.",
                },
            },
            "required": ["spreadsheet_id", "range_notation"],
        }

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload = {
            "bot_id": bot_id,
            "spreadsheet_id": kwargs["spreadsheet_id"],
            "range_notation": kwargs["range_notation"],
        }
        return await self._post(f"{coordinator_url}/internal/google/sheets/read-range", payload)


class GoogleSheetsWriteRangeTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "sheets_write_range"

    @property
    def description(self) -> str:
        return (
            "Write data to a range in a Google Spreadsheet. "
            "Provide values as a 2D array (rows of columns). "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "spreadsheet_id": {
                    "type": "string",
                    "description": "The Google Spreadsheet ID.",
                },
                "range_notation": {
                    "type": "string",
                    "description": "A1 notation of the top-left cell to start writing, e.g. 'Sheet1!A1'.",
                },
                "values": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {},
                    },
                    "description": "2D array of values to write. Each inner array is a row.",
                },
            },
            "required": ["spreadsheet_id", "range_notation", "values"],
        }

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload = {
            "bot_id": bot_id,
            "spreadsheet_id": kwargs["spreadsheet_id"],
            "range_notation": kwargs["range_notation"],
            "values": kwargs["values"],
        }
        return await self._post(f"{coordinator_url}/internal/google/sheets/write-range", payload)


class GoogleSheetsAppendRowsTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "sheets_append_rows"

    @property
    def description(self) -> str:
        return (
            "Append rows to a Google Spreadsheet after the last row with data. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "spreadsheet_id": {
                    "type": "string",
                    "description": "The Google Spreadsheet ID.",
                },
                "range_notation": {
                    "type": "string",
                    "description": "A1 notation of the table range, e.g. 'Sheet1!A1'. Data is appended after the last row.",
                },
                "values": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {},
                    },
                    "description": "2D array of rows to append.",
                },
            },
            "required": ["spreadsheet_id", "range_notation", "values"],
        }

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload = {
            "bot_id": bot_id,
            "spreadsheet_id": kwargs["spreadsheet_id"],
            "range_notation": kwargs["range_notation"],
            "values": kwargs["values"],
        }
        return await self._post(f"{coordinator_url}/internal/google/sheets/append-rows", payload)


class GoogleSheetsClearRangeTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "sheets_clear_range"

    @property
    def description(self) -> str:
        return (
            "Clear all values in a range of a Google Spreadsheet (does not delete the cells). "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "spreadsheet_id": {
                    "type": "string",
                    "description": "The Google Spreadsheet ID.",
                },
                "range_notation": {
                    "type": "string",
                    "description": "A1 notation range to clear, e.g. 'Sheet1!A1:D10'.",
                },
            },
            "required": ["spreadsheet_id", "range_notation"],
        }

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload = {
            "bot_id": bot_id,
            "spreadsheet_id": kwargs["spreadsheet_id"],
            "range_notation": kwargs["range_notation"],
        }
        return await self._post(f"{coordinator_url}/internal/google/sheets/clear-range", payload)
