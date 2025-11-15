"""Link short code service for Hyphen SDK."""

import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from hyphen.base_client import BaseClient


class QrSize:
    """QR code size constants."""

    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class Link:
    """Client for short code and QR code management in Hyphen."""

    def __init__(
        self,
        organization_id: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: str = "https://api.hyphen.ai",
    ):
        """
        Initialize the Link client.

        Args:
            organization_id: Organization ID. If not provided, will check
                HYPHEN_ORGANIZATION_ID env var.
            api_key: API key for authentication. If not provided, will check
                HYPHEN_API_KEY env var.
            base_url: Base URL for the Hyphen API.
        """
        self.organization_id = organization_id or os.environ.get("HYPHEN_ORGANIZATION_ID")
        if not self.organization_id:
            raise ValueError(
                "Organization ID is required. Provide it as a parameter or set "
                "HYPHEN_ORGANIZATION_ID environment variable."
            )

        self.client = BaseClient(api_key=api_key, base_url=base_url)

    def create_short_code(
        self,
        long_url: str,
        domain: str,
        options: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new short code.

        Args:
            long_url: The full URL to shorten
            domain: Domain to use for the short code
            options: Optional parameters like tags, title, etc.

        Returns:
            Dictionary containing the created short code information

        Raises:
            requests.HTTPError: If the request fails
        """
        endpoint = f"/api/organizations/{self.organization_id}/link/codes"
        data = {
            "long_url": long_url,
            "domain": domain,
        }
        if options:
            data.update(options)

        return self.client.post(endpoint, data=data)

    def update_short_code(
        self,
        code: str,
        options: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Update an existing short code.

        Args:
            code: The code identifier for the short code to update
            options: Parameters to update (title, tags, long_url, etc.)

        Returns:
            Dictionary containing the updated short code information

        Raises:
            requests.HTTPError: If the request fails
        """
        endpoint = f"/api/organizations/{self.organization_id}/link/codes/{code}"
        return self.client.put(endpoint, data=options)

    def get_short_code(self, code: str) -> Dict[str, Any]:
        """
        Get a specific short code by its identifier.

        Args:
            code: The code identifier for the short code to retrieve

        Returns:
            Dictionary containing the short code information

        Raises:
            requests.HTTPError: If the request fails
        """
        endpoint = f"/api/organizations/{self.organization_id}/link/codes/{code}"
        return self.client.get(endpoint)

    def get_short_codes(
        self,
        title: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get a list of short codes with optional filtering.

        Args:
            title: Optional title to filter short codes
            tags: Optional list of tags to filter short codes

        Returns:
            List of dictionaries containing short code information

        Raises:
            requests.HTTPError: If the request fails
        """
        endpoint = f"/api/organizations/{self.organization_id}/link/codes"
        params: Dict[str, Any] = {}

        if title:
            params["title"] = title
        if tags:
            params["tags"] = ",".join(tags)

        return self.client.get(endpoint, params=params if params else None)

    def get_tags(self) -> List[str]:
        """
        Get all tags for the organization.

        Returns:
            List of tag strings

        Raises:
            requests.HTTPError: If the request fails
        """
        endpoint = f"/api/organizations/{self.organization_id}/link/tags"
        return self.client.get(endpoint)

    def get_short_code_stats(
        self,
        code: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """
        Get statistics for a short code.

        Args:
            code: The code identifier for the short code
            start_date: Optional start date for the stats
            end_date: Optional end date for the stats

        Returns:
            Dictionary containing statistics information

        Raises:
            requests.HTTPError: If the request fails
        """
        endpoint = f"/api/organizations/{self.organization_id}/link/codes/{code}/stats"
        params: Dict[str, Any] = {}

        if start_date:
            params["start_date"] = start_date.isoformat()
        if end_date:
            params["end_date"] = end_date.isoformat()

        return self.client.get(endpoint, params=params if params else None)

    def delete_short_code(self, code: str) -> Any:
        """
        Delete a short code.

        Args:
            code: The code identifier for the short code to delete

        Returns:
            Response data (may be None for successful deletion)

        Raises:
            requests.HTTPError: If the request fails
        """
        endpoint = f"/api/organizations/{self.organization_id}/link/codes/{code}"
        return self.client.delete(endpoint)

    def create_qr_code(
        self,
        code: str,
        options: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Create a QR code for a short code.

        Args:
            code: The code identifier for the short code
            options: Optional parameters (title, backgroundColor, color, size, logo)

        Returns:
            Dictionary containing the QR code information

        Raises:
            requests.HTTPError: If the request fails
        """
        endpoint = f"/api/organizations/{self.organization_id}/link/codes/{code}/qr"
        data = options or {}
        return self.client.post(endpoint, data=data)

    def get_qr_code(self, code: str, qr_id: str) -> Dict[str, Any]:
        """
        Get a specific QR code by its ID.

        Args:
            code: The code identifier for the short code
            qr_id: The ID of the QR code to retrieve

        Returns:
            Dictionary containing the QR code information

        Raises:
            requests.HTTPError: If the request fails
        """
        endpoint = f"/api/organizations/{self.organization_id}/link/codes/{code}/qr/{qr_id}"
        return self.client.get(endpoint)

    def get_qr_codes(self, code: str) -> List[Dict[str, Any]]:
        """
        Get all QR codes for a short code.

        Args:
            code: The code identifier for the short code

        Returns:
            List of dictionaries containing QR code information

        Raises:
            requests.HTTPError: If the request fails
        """
        endpoint = f"/api/organizations/{self.organization_id}/link/codes/{code}/qr"
        return self.client.get(endpoint)

    def delete_qr_code(self, code: str, qr_id: str) -> Any:
        """
        Delete a QR code.

        Args:
            code: The code identifier for the short code
            qr_id: The ID of the QR code to delete

        Returns:
            Response data (may be None for successful deletion)

        Raises:
            requests.HTTPError: If the request fails
        """
        endpoint = f"/api/organizations/{self.organization_id}/link/codes/{code}/qr/{qr_id}"
        return self.client.delete(endpoint)
