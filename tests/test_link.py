"""Tests for Link."""

import os
from datetime import datetime
from unittest.mock import Mock, patch

import pytest

from hyphen import Link


def test_link_init_with_params() -> None:
    """Test Link initialization with parameters."""
    link = Link(organization_id="org_123", api_key="key_123")
    assert link.organization_id == "org_123"


def test_link_init_with_env() -> None:
    """Test Link initialization with environment variables."""
    with patch.dict(
        os.environ,
        {
            "HYPHEN_ORGANIZATION_ID": "org_env",
            "HYPHEN_API_KEY": "key_env",
        },
    ):
        link = Link()
        assert link.organization_id == "org_env"


def test_link_init_missing_org_id() -> None:
    """Test Link raises error when organization ID is missing."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="Organization ID is required"):
            Link(api_key="test_key")


@patch("hyphen.link.BaseClient")
def test_create_short_code(mock_client_class: Mock) -> None:
    """Test create_short_code method."""
    mock_client = Mock()
    mock_client.post.return_value = {"code": "abc123", "short_url": "https://test.h4n.link/abc123"}
    mock_client_class.return_value = mock_client

    link = Link(organization_id="org_123", api_key="key_123")
    result = link.create_short_code(
        long_url="https://hyphen.ai",
        domain="test.h4n.link",
        options={"tags": ["test"]},
    )

    assert result["code"] == "abc123"
    mock_client.post.assert_called_once()


@patch("hyphen.link.BaseClient")
def test_update_short_code(mock_client_class: Mock) -> None:
    """Test update_short_code method."""
    mock_client = Mock()
    mock_client.put.return_value = {"code": "abc123", "title": "Updated"}
    mock_client_class.return_value = mock_client

    link = Link(organization_id="org_123", api_key="key_123")
    result = link.update_short_code("abc123", {"title": "Updated"})

    assert result["title"] == "Updated"
    mock_client.put.assert_called_once_with(
        "/api/organizations/org_123/link/codes/abc123",
        data={"title": "Updated"}
    )


@patch("hyphen.link.BaseClient")
def test_get_short_code(mock_client_class: Mock) -> None:
    """Test get_short_code method."""
    mock_client = Mock()
    mock_client.get.return_value = {"code": "abc123", "long_url": "https://hyphen.ai"}
    mock_client_class.return_value = mock_client

    link = Link(organization_id="org_123", api_key="key_123")
    result = link.get_short_code("abc123")

    assert result["code"] == "abc123"
    mock_client.get.assert_called_once_with("/api/organizations/org_123/link/codes/abc123")


@patch("hyphen.link.BaseClient")
def test_get_short_codes(mock_client_class: Mock) -> None:
    """Test get_short_codes method."""
    mock_client = Mock()
    mock_client.get.return_value = [{"code": "abc123"}, {"code": "def456"}]
    mock_client_class.return_value = mock_client

    link = Link(organization_id="org_123", api_key="key_123")
    result = link.get_short_codes(title="Test", tags=["tag1", "tag2"])

    assert len(result) == 2
    mock_client.get.assert_called_once()


@patch("hyphen.link.BaseClient")
def test_get_tags(mock_client_class: Mock) -> None:
    """Test get_tags method."""
    mock_client = Mock()
    mock_client.get.return_value = ["tag1", "tag2", "tag3"]
    mock_client_class.return_value = mock_client

    link = Link(organization_id="org_123", api_key="key_123")
    result = link.get_tags()

    assert len(result) == 3
    assert "tag1" in result
    mock_client.get.assert_called_once_with("/api/organizations/org_123/link/tags")


@patch("hyphen.link.BaseClient")
def test_get_short_code_stats(mock_client_class: Mock) -> None:
    """Test get_short_code_stats method."""
    mock_client = Mock()
    mock_client.get.return_value = {"clicks": 100, "unique_clicks": 50}
    mock_client_class.return_value = mock_client

    link = Link(organization_id="org_123", api_key="key_123")
    start = datetime(2023, 1, 1)
    end = datetime(2023, 12, 31)
    result = link.get_short_code_stats("abc123", start_date=start, end_date=end)

    assert result["clicks"] == 100
    mock_client.get.assert_called_once()


@patch("hyphen.link.BaseClient")
def test_delete_short_code(mock_client_class: Mock) -> None:
    """Test delete_short_code method."""
    mock_client = Mock()
    mock_client.delete.return_value = None
    mock_client_class.return_value = mock_client

    link = Link(organization_id="org_123", api_key="key_123")
    result = link.delete_short_code("abc123")

    assert result is None
    mock_client.delete.assert_called_once_with("/api/organizations/org_123/link/codes/abc123")


@patch("hyphen.link.BaseClient")
def test_create_qr_code(mock_client_class: Mock) -> None:
    """Test create_qr_code method."""
    mock_client = Mock()
    mock_client.post.return_value = {"qr_id": "qr_123", "url": "https://example.com/qr.png"}
    mock_client_class.return_value = mock_client

    link = Link(organization_id="org_123", api_key="key_123")
    result = link.create_qr_code("abc123", options={"title": "My QR"})

    assert result["qr_id"] == "qr_123"
    mock_client.post.assert_called_once()


@patch("hyphen.link.BaseClient")
def test_get_qr_code(mock_client_class: Mock) -> None:
    """Test get_qr_code method."""
    mock_client = Mock()
    mock_client.get.return_value = {"qr_id": "qr_123"}
    mock_client_class.return_value = mock_client

    link = Link(organization_id="org_123", api_key="key_123")
    result = link.get_qr_code("abc123", "qr_123")

    assert result["qr_id"] == "qr_123"
    mock_client.get.assert_called_once_with("/api/organizations/org_123/link/codes/abc123/qr/qr_123")


@patch("hyphen.link.BaseClient")
def test_get_qr_codes(mock_client_class: Mock) -> None:
    """Test get_qr_codes method."""
    mock_client = Mock()
    mock_client.get.return_value = [{"qr_id": "qr_123"}, {"qr_id": "qr_456"}]
    mock_client_class.return_value = mock_client

    link = Link(organization_id="org_123", api_key="key_123")
    result = link.get_qr_codes("abc123")

    assert len(result) == 2
    mock_client.get.assert_called_once_with("/api/organizations/org_123/link/codes/abc123/qr")


@patch("hyphen.link.BaseClient")
def test_delete_qr_code(mock_client_class: Mock) -> None:
    """Test delete_qr_code method."""
    mock_client = Mock()
    mock_client.delete.return_value = None
    mock_client_class.return_value = mock_client

    link = Link(organization_id="org_123", api_key="key_123")
    result = link.delete_qr_code("abc123", "qr_123")

    assert result is None
    mock_client.delete.assert_called_once_with("/api/organizations/org_123/link/codes/abc123/qr/qr_123")
