"""Acceptance tests for Link."""

import time

import pytest

from hyphen import Link, QrCode, QrCodesResponse, ShortCode, ShortCodesResponse


class TestLinkAcceptance:
    """Acceptance tests for Link service."""

    def test_create_and_delete_short_code(
        self, api_key: str, organization_id: str, link_domain: str, link_base_url: str
    ) -> None:
        """Test creating and deleting a short code."""
        link = Link(organization_id=organization_id, api_key=api_key, base_url=link_base_url)
        unique_id = str(int(time.time() * 1000))

        # Create
        result = link.create_short_code(
            long_url=f"https://example.com/test-{unique_id}",
            domain=link_domain,
            options={"title": f"Test Short Code {unique_id}"},
        )

        assert isinstance(result, ShortCode)
        assert result.id != ""
        assert result.code != ""
        assert result.domain == link_domain

        # Cleanup
        link.delete_short_code(result.id)

    def test_get_short_code(
        self, api_key: str, organization_id: str, link_domain: str, link_base_url: str
    ) -> None:
        """Test getting a short code by ID."""
        link = Link(organization_id=organization_id, api_key=api_key, base_url=link_base_url)
        unique_id = str(int(time.time() * 1000))

        # Create
        created = link.create_short_code(
            long_url=f"https://example.com/test-{unique_id}",
            domain=link_domain,
        )

        # Get
        result = link.get_short_code(created.id)

        assert isinstance(result, ShortCode)
        assert result.code == created.code
        assert result.id == created.id

        # Cleanup
        link.delete_short_code(created.id)

    def test_get_short_codes(
        self, api_key: str, organization_id: str, link_base_url: str
    ) -> None:
        """Test listing short codes."""
        link = Link(organization_id=organization_id, api_key=api_key, base_url=link_base_url)

        result = link.get_short_codes()

        assert isinstance(result, ShortCodesResponse)
        assert result.total >= 0
        assert isinstance(result.data, list)

    def test_update_short_code(
        self, api_key: str, organization_id: str, link_domain: str, link_base_url: str
    ) -> None:
        """Test updating a short code."""
        link = Link(organization_id=organization_id, api_key=api_key, base_url=link_base_url)
        unique_id = str(int(time.time() * 1000))

        # Create
        created = link.create_short_code(
            long_url=f"https://example.com/test-{unique_id}",
            domain=link_domain,
            options={"title": "Original Title"},
        )

        # Update
        result = link.update_short_code(
            created.id,
            {"title": "Updated Title"},
        )

        assert isinstance(result, ShortCode)
        assert result.title == "Updated Title"

        # Cleanup
        link.delete_short_code(created.id)

    def test_get_tags(self, api_key: str, organization_id: str, link_base_url: str) -> None:
        """Test getting all tags."""
        link = Link(organization_id=organization_id, api_key=api_key, base_url=link_base_url)

        result = link.get_tags()

        assert isinstance(result, list)

    def test_create_and_delete_qr_code(
        self, api_key: str, organization_id: str, link_domain: str, link_base_url: str
    ) -> None:
        """Test creating and deleting a QR code."""
        link = Link(organization_id=organization_id, api_key=api_key, base_url=link_base_url)
        unique_id = str(int(time.time() * 1000))

        # Create short code first
        short_code = link.create_short_code(
            long_url=f"https://example.com/qr-test-{unique_id}",
            domain=link_domain,
        )

        # Create QR code
        qr = link.create_qr_code(
            short_code.id,
            options={"title": f"Test QR {unique_id}"},
        )

        assert isinstance(qr, QrCode)
        assert qr.id != ""

        # Delete QR code
        link.delete_qr_code(short_code.id, qr.id)
        # Cleanup short code
        link.delete_short_code(short_code.id)

    def test_get_qr_codes(
        self, api_key: str, organization_id: str, link_domain: str, link_base_url: str
    ) -> None:
        """Test listing QR codes for a short code."""
        link = Link(organization_id=organization_id, api_key=api_key, base_url=link_base_url)
        unique_id = str(int(time.time() * 1000))

        # Create short code
        short_code = link.create_short_code(
            long_url=f"https://example.com/qr-list-{unique_id}",
            domain=link_domain,
        )

        result = link.get_qr_codes(short_code.id)

        assert isinstance(result, QrCodesResponse)
        assert result.total >= 0

        # Cleanup
        link.delete_short_code(short_code.id)
