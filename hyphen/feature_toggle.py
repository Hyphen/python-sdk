"""Feature Toggle management for Hyphen SDK."""

import os
from typing import Any, Dict, List, Optional, Union

from hyphen.base_client import BaseClient


class FeatureToggle:
    """Client for managing feature toggles in Hyphen."""

    def __init__(
        self,
        application_id: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: str = "https://api.hyphen.ai",
    ):
        """
        Initialize the FeatureToggle client.

        Args:
            application_id: Application ID. If not provided, will check
                HYPHEN_APPLICATION_ID env var.
            api_key: API key for authentication. If not provided, will check
                HYPHEN_API_KEY or HYPHEN_PUBLIC_API_KEY env var.
            base_url: Base URL for the Hyphen API.
        """
        # Try to get API key from different sources
        resolved_api_key = (
            api_key
            or os.environ.get("HYPHEN_API_KEY")
            or os.environ.get("HYPHEN_PUBLIC_API_KEY")
        )

        self.application_id = application_id or os.environ.get("HYPHEN_APPLICATION_ID")
        if not self.application_id:
            raise ValueError(
                "Application ID is required. Provide it as a parameter or set "
                "HYPHEN_APPLICATION_ID environment variable."
            )

        self.client = BaseClient(api_key=resolved_api_key, base_url=base_url)

    def get_toggle(self, toggle_name: str) -> Union[bool, int, float, str, Dict[str, Any]]:
        """
        Get a single feature toggle by name.

        Args:
            toggle_name: Name of the toggle to retrieve

        Returns:
            The toggle value (can be boolean, number, string, or JSON object)

        Raises:
            requests.HTTPError: If the request fails
        """
        endpoint = f"/api/applications/{self.application_id}/toggles/{toggle_name}"
        response = self.client.get(endpoint)

        # Return the value from the response
        if isinstance(response, dict) and "value" in response:
            return response["value"]
        return response

    def get_toggles(
        self, toggle_names: List[str]
    ) -> Dict[str, Union[bool, int, float, str, Dict[str, Any]]]:
        """
        Get multiple feature toggles by their names.

        Args:
            toggle_names: List of toggle names to retrieve

        Returns:
            Dictionary mapping toggle names to their values

        Raises:
            requests.HTTPError: If the request fails
        """
        endpoint = f"/api/applications/{self.application_id}/toggles"
        params = {"names": ",".join(toggle_names)}
        response = self.client.get(endpoint, params=params)

        # Parse the response and return a dictionary of toggle names to values
        if isinstance(response, list):
            return {item["name"]: item["value"] for item in response}
        elif isinstance(response, dict):
            # If the response is already a dict, return it as-is
            return response
        return {}
