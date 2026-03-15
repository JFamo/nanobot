"""Google Contacts tools — list, get, create, update, delete, search via coordinator API."""

from typing import Any

from nanobot.agent.tools.google.base import GoogleBaseTool


class GoogleContactsListTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "contacts_list"

    @property
    def description(self) -> str:
        return (
            "List the user's Google Contacts. Returns names, emails, and phone numbers. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id.\n\n"
            "DISPLAY FORMAT: Include a directive for EACH contact in your response:\n"
            '::google-contact{name="<full_name>" email="<email>" phone="<phone>" size="compact"}\n'
            "Use compact size when listing multiple contacts. Omit email or phone if not available. Replace placeholders with actual values.\n"
            'Size options: "default" for standalone results, "compact" when listing multiple items, "inline" for brief mentions in text.'
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of contacts to return (default 50).",
                    "default": 50,
                },
            },
            "required": [],
        }

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload: dict[str, Any] = {"bot_id": bot_id}
        if kwargs.get("max_results"):
            payload["max_results"] = kwargs["max_results"]
        return await self._post(f"{coordinator_url}/internal/google/contacts/list", payload)


class GoogleContactsGetTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "contacts_get"

    @property
    def description(self) -> str:
        return (
            "Get a specific Google Contact by resource name (e.g. 'people/c12345'). "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id.\n\n"
            "DISPLAY FORMAT: Include this directive when presenting contact details:\n"
            '::google-contact{name="<full_name>" email="<email>" phone="<phone>" size="default"}\n'
            "Replace placeholders with actual values. Omit email or phone if not available.\n"
            'Size options: "default" for standalone results, "compact" when listing multiple items, "inline" for brief mentions in text.'
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "resource_name": {
                    "type": "string",
                    "description": "The contact resource name, e.g. 'people/c1234567890'.",
                },
            },
            "required": ["resource_name"],
        }

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload = {"bot_id": bot_id, "resource_name": kwargs["resource_name"]}
        return await self._post(f"{coordinator_url}/internal/google/contacts/get", payload)


class GoogleContactsCreateTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "contacts_create"

    @property
    def description(self) -> str:
        return (
            "Create a new Google Contact. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id. "
            "This action requires user confirmation. The UI automatically shows a preview card with name, email, phone, etc. — "
            "do not repeat those parameters or include display directives in your response; a brief intro line is sufficient."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "given_name": {
                    "type": "string",
                    "description": "Contact's first name.",
                },
                "family_name": {
                    "type": "string",
                    "description": "Contact's last name.",
                },
                "email": {
                    "type": "string",
                    "description": "Contact's email address.",
                },
                "phone": {
                    "type": "string",
                    "description": "Contact's phone number.",
                },
                "organization": {
                    "type": "string",
                    "description": "Contact's organization/company name.",
                },
                "title": {
                    "type": "string",
                    "description": "Contact's job title.",
                },
            },
            "required": ["given_name"],
        }

    @property
    def requires_confirmation(self) -> bool:
        return True

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload: dict[str, Any] = {"bot_id": bot_id, "given_name": kwargs["given_name"]}
        for key in ("family_name", "email", "phone", "organization", "title"):
            if kwargs.get(key):
                payload[key] = kwargs[key]
        return await self._post(f"{coordinator_url}/internal/google/contacts/create", payload)


class GoogleContactsUpdateTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "contacts_update"

    @property
    def description(self) -> str:
        return (
            "Update an existing Google Contact. Only provided fields are changed. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id. "
            "This action requires user confirmation. The UI automatically shows a preview card with the updated contact details — "
            "do not repeat those parameters or include display directives in your response; a brief intro line is sufficient."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "resource_name": {
                    "type": "string",
                    "description": "The contact resource name, e.g. 'people/c1234567890'.",
                },
                "given_name": {"type": "string", "description": "New first name."},
                "family_name": {"type": "string", "description": "New last name."},
                "email": {"type": "string", "description": "New email address."},
                "phone": {"type": "string", "description": "New phone number."},
                "organization": {"type": "string", "description": "New organization name."},
                "title": {"type": "string", "description": "New job title."},
            },
            "required": ["resource_name"],
        }

    @property
    def requires_confirmation(self) -> bool:
        return True

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload: dict[str, Any] = {"bot_id": bot_id, "resource_name": kwargs["resource_name"]}
        for key in ("given_name", "family_name", "email", "phone", "organization", "title"):
            if kwargs.get(key) is not None:
                payload[key] = kwargs[key]
        return await self._post(f"{coordinator_url}/internal/google/contacts/update", payload)


class GoogleContactsDeleteTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "contacts_delete"

    @property
    def description(self) -> str:
        return (
            "Delete a Google Contact by resource name. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id. "
            "This action requires user confirmation. The UI shows a preview — do not repeat the action details in your response."
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "resource_name": {
                    "type": "string",
                    "description": "The contact resource name to delete, e.g. 'people/c1234567890'.",
                },
            },
            "required": ["resource_name"],
        }

    @property
    def requires_confirmation(self) -> bool:
        return True

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload = {"bot_id": bot_id, "resource_name": kwargs["resource_name"]}
        return await self._post(f"{coordinator_url}/internal/google/contacts/delete", payload)


class GoogleContactsSearchTool(GoogleBaseTool):

    @property
    def name(self) -> str:
        return "contacts_search"

    @property
    def description(self) -> str:
        return (
            "Search Google Contacts by name, email, phone number, or other fields. "
            "Authentication is automatic — never ask the user for credentials, tokens, or bot_id.\n\n"
            "DISPLAY FORMAT: Include a directive for EACH matching contact in your response:\n"
            '::google-contact{name="<full_name>" email="<email>" phone="<phone>" size="compact"}\n'
            "Use compact size when listing multiple results. Omit email or phone if not available. Replace placeholders with actual values.\n"
            'Size options: "default" for standalone results, "compact" when listing multiple items, "inline" for brief mentions in text.'
        )

    @property
    def parameters(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query, e.g. a name, email address, or company.",
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of results (default 20).",
                    "default": 20,
                },
            },
            "required": ["query"],
        }

    async def execute(self, **kwargs: Any) -> str:
        env = self._env()
        if isinstance(env, str):
            return env
        coordinator_url, bot_id = env
        payload: dict[str, Any] = {"bot_id": bot_id, "query": kwargs["query"]}
        if kwargs.get("max_results"):
            payload["max_results"] = kwargs["max_results"]
        return await self._post(f"{coordinator_url}/internal/google/contacts/search", payload)
