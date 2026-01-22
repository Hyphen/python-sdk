"""Toggle admin utility for acceptance tests.

Provides methods to create and delete toggles via the Hyphen Management API.
This is used for test setup and teardown in acceptance tests.
"""

import os
from dataclasses import dataclass, field
from typing import Any

import requests


@dataclass
class Target:
    """Represents a targeting rule for a toggle."""

    logic: str  # JSONLogic expression
    value: Any  # Value to return if logic evaluates to true


@dataclass
class ToggleAdmin:
    """Provides methods to create and delete toggles via the Hyphen Management API."""

    api_key: str = field(default_factory=lambda: os.environ.get("HYPHEN_API_KEY", ""))
    organization_id: str = field(
        default_factory=lambda: os.environ.get("HYPHEN_ORGANIZATION_ID", "")
    )
    project_id: str = field(
        default_factory=lambda: os.environ.get("HYPHEN_PROJECT_ID", "")
    )
    base_url: str = field(default_factory=lambda: _get_base_url())

    def is_configured(self) -> bool:
        """Return True if all required environment variables are set."""
        return bool(self.api_key and self.organization_id and self.project_id)

    def missing_config(self) -> list[str]:
        """Return list of missing configuration items."""
        missing = []
        if not self.api_key:
            missing.append("HYPHEN_API_KEY")
        if not self.organization_id:
            missing.append("HYPHEN_ORGANIZATION_ID")
        if not self.project_id:
            missing.append("HYPHEN_PROJECT_ID")
        return missing

    def create_boolean_toggle(self, key: str, default_value: bool) -> None:
        """Create a boolean toggle with the given key and default value."""
        self._create_toggle(key, "boolean", default_value, None)

    def create_string_toggle(self, key: str, default_value: str) -> None:
        """Create a string toggle with the given key and default value."""
        self._create_toggle(key, "string", default_value, None)

    def create_number_toggle(self, key: str, default_value: float) -> None:
        """Create a number toggle with the given key and default value."""
        self._create_toggle(key, "number", default_value, None)

    def create_boolean_toggle_with_targets(
        self, key: str, default_value: bool, targets: list[Target]
    ) -> None:
        """Create a boolean toggle with targeting rules."""
        self._create_toggle(key, "boolean", default_value, targets)

    def create_string_toggle_with_targets(
        self, key: str, default_value: str, targets: list[Target]
    ) -> None:
        """Create a string toggle with targeting rules."""
        self._create_toggle(key, "string", default_value, targets)

    def _create_toggle(
        self,
        key: str,
        toggle_type: str,
        default_value: Any,
        targets: list[Target] | None,
    ) -> None:
        """Create a toggle via the Management API."""
        url = (
            f"{self.base_url}/api/organizations/{self.organization_id}"
            f"/projects/{self.project_id}/toggles/"
        )

        target_list = []
        if targets:
            target_list = [{"logic": t.logic, "value": t.value} for t in targets]

        req_body = {
            "key": key,
            "type": toggle_type,
            "targets": target_list,
            "defaultValue": default_value,
            "description": "Created by acceptance test",
        }

        response = requests.post(
            url,
            json=req_body,
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
            },
            timeout=30,
        )

        if response.status_code not in (200, 201):
            raise RuntimeError(f"Unexpected status code: {response.status_code}")

    def delete_toggle(self, key: str) -> None:
        """Delete a toggle by its key."""
        url = (
            f"{self.base_url}/api/organizations/{self.organization_id}"
            f"/projects/{self.project_id}/toggles/{key}"
        )

        response = requests.delete(
            url,
            headers={"x-api-key": self.api_key},
            timeout=30,
        )

        if response.status_code not in (200, 204, 404):
            raise RuntimeError(f"Unexpected status code: {response.status_code}")


def _get_base_url() -> str:
    """Get the base URL based on HYPHEN_DEV environment variable."""
    if os.environ.get("HYPHEN_DEV", "").lower() == "true":
        return "https://dev-api.hyphen.ai"
    return "https://api.hyphen.ai"
