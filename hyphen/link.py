"""Link short code service for Hyphen SDK."""

import os
from datetime import datetime
from typing import Any, Dict, List, Optional, cast

from hyphen.base_client import BaseClient
from hyphen.types import (
    CreateQrCodeOptions,
    CreateShortCodeOptions,
    QrCode,
    QrCodesResponse,
    ShortCode,
    ShortCodesResponse,
    UpdateShortCodeOptions,
)


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
        options: Optional[CreateShortCodeOptions] = None,
    ) -> ShortCode:
        """
        Create a new short code.

        Args:
            long_url: The full URL to shorten
            domain: Domain to use for the short code
            options: Optional parameters like tags, title, etc.

        Returns:
            ShortCode object containing the created short code information

        Raises:
            requests.HTTPError: If the request fails
        """
        endpoint = f"/api/organizations/{self.organization_id}/link/codes"
        data: Dict[str, Any] = {
            "long_url": long_url,
            "domain": domain,
        }
        if options:
            data.update(options)

        response = self.client.post(endpoint, data=data)
        return ShortCode.from_dict(response)

    def update_short_code(
        self,
        code: str,
        options: UpdateShortCodeOptions,
    ) -> ShortCode:
        """
        Update an existing short code.

        Args:
            code: The code identifier for the short code to update
            options: Parameters to update (title, tags, long_url, etc.)

        Returns:
            ShortCode object containing the updated short code information

        Raises:
            requests.HTTPError: If the request fails
        """
        endpoint = f"/api/organizations/{self.organization_id}/link/codes/{code}"
        response = self.client.put(endpoint, data=cast(Dict[str, Any], options))
        return ShortCode.from_dict(response)

    def get_short_code(self, code: str) -> ShortCode:
        """
        Get a specific short code by its identifier.

        Args:
            code: The code identifier for the short code to retrieve

        Returns:
            ShortCode object containing the short code information

        Raises:
            requests.HTTPError: If the request fails
        """
        endpoint = f"/api/organizations/{self.organization_id}/link/codes/{code}"
        response = self.client.get(endpoint)
        return ShortCode.from_dict(response)

    def get_short_codes(
        self,
        title: Optional[str] = None,
        tags: Optional[List[str]] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> ShortCodesResponse:
        """
        Get a list of short codes with optional filtering.

        Args:
            title: Optional title to filter short codes
            tags: Optional list of tags to filter short codes
            page_number: Optional page number for pagination
            page_size: Optional page size for pagination

        Returns:
            ShortCodesResponse with paginated list of short codes

        Raises:
            requests.HTTPError: If the request fails
        """
        endpoint = f"/api/organizations/{self.organization_id}/link/codes"
        params: Dict[str, Any] = {}

        if title:
            params["title"] = title
        if tags:
            params["tags"] = ",".join(tags)
        if page_number is not None:
            params["pageNum"] = page_number
        if page_size is not None:
            params["pageSize"] = page_size

        response = self.client.get(endpoint, params=params if params else None)
        return ShortCodesResponse.from_dict(response)

    def get_tags(self) -> List[str]:
        """
        Get all tags for the organization.

        Returns:
            List of tag strings

        Raises:
            requests.HTTPError: If the request fails
        """
        endpoint = f"/api/organizations/{self.organization_id}/link/tags"
        response = self.client.get(endpoint)
        return list(response) if response else []

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

        return dict(self.client.get(endpoint, params=params if params else None))

    def delete_short_code(self, code: str) -> None:
        """
        Delete a short code.

        Args:
            code: The code identifier for the short code to delete

        Raises:
            requests.HTTPError: If the request fails
        """
        endpoint = f"/api/organizations/{self.organization_id}/link/codes/{code}"
        self.client.delete(endpoint)

    def create_qr_code(
        self,
        code: str,
        options: Optional[CreateQrCodeOptions] = None,
    ) -> QrCode:
        """
        Create a QR code for a short code.

        Args:
            code: The code identifier for the short code
            options: Optional parameters (title, backgroundColor, color, size, logo)

        Returns:
            QrCode object containing the QR code information

        Raises:
            requests.HTTPError: If the request fails
        """
        endpoint = f"/api/organizations/{self.organization_id}/link/codes/{code}/qr"
        data: Dict[str, Any] = {}
        if options:
            # Convert snake_case to camelCase for API
            for key, value in options.items():
                if key == "background_color":
                    data["backgroundColor"] = value
                else:
                    data[key] = value
        response = self.client.post(endpoint, data=data)
        return QrCode.from_dict(response)

    def get_qr_code(self, code: str, qr_id: str) -> QrCode:
        """
        Get a specific QR code by its ID.

        Args:
            code: The code identifier for the short code
            qr_id: The ID of the QR code to retrieve

        Returns:
            QrCode object containing the QR code information

        Raises:
            requests.HTTPError: If the request fails
        """
        endpoint = f"/api/organizations/{self.organization_id}/link/codes/{code}/qr/{qr_id}"
        response = self.client.get(endpoint)
        return QrCode.from_dict(response)

    def get_qr_codes(
        self,
        code: str,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> QrCodesResponse:
        """
        Get all QR codes for a short code.

        Args:
            code: The code identifier for the short code
            page_number: Optional page number for pagination
            page_size: Optional page size for pagination

        Returns:
            QrCodesResponse with paginated list of QR codes

        Raises:
            requests.HTTPError: If the request fails
        """
        endpoint = f"/api/organizations/{self.organization_id}/link/codes/{code}/qr"
        params: Dict[str, Any] = {}
        if page_number is not None:
            params["pageNum"] = page_number
        if page_size is not None:
            params["pageSize"] = page_size

        response = self.client.get(endpoint, params=params if params else None)
        return QrCodesResponse.from_dict(response)

    def delete_qr_code(self, code: str, qr_id: str) -> None:
        """
        Delete a QR code.

        Args:
            code: The code identifier for the short code
            qr_id: The ID of the QR code to delete

        Raises:
            requests.HTTPError: If the request fails
        """
        endpoint = f"/api/organizations/{self.organization_id}/link/codes/{code}/qr/{qr_id}"
        self.client.delete(endpoint)
