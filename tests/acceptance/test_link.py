"""Acceptance tests for Link."""

import time

from hyphen import Link, QrCode, QrCodesResponse, ShortCode, ShortCodesResponse


class TestLinkAcceptance:
    """Acceptance tests for Link service."""

    def test_create_and_delete_short_code(
        self, api_key: str, organization_id: str, link_domain: str
    ) -> None:
        """Test creating and deleting a short code."""
        link = Link(organization_id=organization_id, api_key=api_key)
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
        link.delete_short_code(result.code)

    def test_get_short_code(
        self, api_key: str, organization_id: str, link_domain: str
    ) -> None:
        """Test getting a short code by code."""
        link = Link(organization_id=organization_id, api_key=api_key)
        unique_id = str(int(time.time() * 1000))

        # Create
        created = link.create_short_code(
            long_url=f"https://example.com/test-{unique_id}",
            domain=link_domain,
        )

        try:
            # Get
            result = link.get_short_code(created.code)

            assert isinstance(result, ShortCode)
            assert result.code == created.code
            assert result.id == created.id
        finally:
            # Cleanup
            link.delete_short_code(created.code)

    def test_get_short_codes(
        self, api_key: str, organization_id: str
    ) -> None:
        """Test listing short codes."""
        link = Link(organization_id=organization_id, api_key=api_key)

        result = link.get_short_codes()

        assert isinstance(result, ShortCodesResponse)
        assert result.total >= 0
        assert isinstance(result.data, list)

    def test_update_short_code(
        self, api_key: str, organization_id: str, link_domain: str
    ) -> None:
        """Test updating a short code."""
        link = Link(organization_id=organization_id, api_key=api_key)
        unique_id = str(int(time.time() * 1000))

        # Create
        created = link.create_short_code(
            long_url=f"https://example.com/test-{unique_id}",
            domain=link_domain,
            options={"title": "Original Title"},
        )

        try:
            # Update
            result = link.update_short_code(
                created.code,
                {"title": "Updated Title"},
            )

            assert isinstance(result, ShortCode)
            assert result.title == "Updated Title"
        finally:
            # Cleanup
            link.delete_short_code(created.code)

    def test_get_tags(self, api_key: str, organization_id: str) -> None:
        """Test getting all tags."""
        link = Link(organization_id=organization_id, api_key=api_key)

        result = link.get_tags()

        assert isinstance(result, list)

    def test_create_and_delete_qr_code(
        self, api_key: str, organization_id: str, link_domain: str
    ) -> None:
        """Test creating and deleting a QR code."""
        link = Link(organization_id=organization_id, api_key=api_key)
        unique_id = str(int(time.time() * 1000))

        # Create short code first
        short_code = link.create_short_code(
            long_url=f"https://example.com/qr-test-{unique_id}",
            domain=link_domain,
        )

        try:
            # Create QR code
            qr = link.create_qr_code(
                short_code.code,
                options={"title": f"Test QR {unique_id}"},
            )

            assert isinstance(qr, QrCode)
            assert qr.id != ""

            # Delete QR code
            link.delete_qr_code(short_code.code, qr.id)
        finally:
            # Cleanup short code
            link.delete_short_code(short_code.code)

    def test_get_qr_codes(
        self, api_key: str, organization_id: str, link_domain: str
    ) -> None:
        """Test listing QR codes for a short code."""
        link = Link(organization_id=organization_id, api_key=api_key)
        unique_id = str(int(time.time() * 1000))

        # Create short code
        short_code = link.create_short_code(
            long_url=f"https://example.com/qr-list-{unique_id}",
            domain=link_domain,
        )

        try:
            result = link.get_qr_codes(short_code.code)

            assert isinstance(result, QrCodesResponse)
            assert result.total >= 0
        finally:
            # Cleanup
            link.delete_short_code(short_code.code)
