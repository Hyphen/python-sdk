"""Tests for feature toggle."""

import os
from unittest.mock import Mock, patch

import pytest

from hyphen import FeatureToggle


def test_feature_toggle_init_with_params() -> None:
    """Test FeatureToggle initialization with parameters."""
    toggle = FeatureToggle(application_id="app_123", api_key="key_123")
    assert toggle.application_id == "app_123"


def test_feature_toggle_init_with_env() -> None:
    """Test FeatureToggle initialization with environment variables."""
    with patch.dict(
        os.environ,
        {
            "HYPHEN_APPLICATION_ID": "app_env",
            "HYPHEN_API_KEY": "key_env",
        },
    ):
        toggle = FeatureToggle()
        assert toggle.application_id == "app_env"


def test_feature_toggle_init_missing_app_id() -> None:
    """Test FeatureToggle raises error when application ID is missing."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="Application ID is required"):
            FeatureToggle(api_key="test_key")


def test_feature_toggle_init_missing_api_key() -> None:
    """Test FeatureToggle raises error when API key is missing."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="API key is required"):
            FeatureToggle(application_id="app_123")


def test_feature_toggle_prefers_public_api_key() -> None:
    """Test FeatureToggle uses HYPHEN_PUBLIC_API_KEY if available."""
    with patch.dict(
        os.environ,
        {
            "HYPHEN_APPLICATION_ID": "app_env",
            "HYPHEN_PUBLIC_API_KEY": "public_key",
        },
    ):
        toggle = FeatureToggle()
        assert toggle.client.api_key == "public_key"


@patch("hyphen.feature_toggle.BaseClient")
def test_get_toggle(mock_client_class: Mock) -> None:
    """Test get_toggle method."""
    mock_client = Mock()
    mock_client.get.return_value = {"value": True}
    mock_client_class.return_value = mock_client

    toggle = FeatureToggle(application_id="app_123", api_key="key_123")
    result = toggle.get_toggle("test-toggle")

    assert result is True
    mock_client.get.assert_called_once_with("/api/applications/app_123/toggles/test-toggle")


@patch("hyphen.feature_toggle.BaseClient")
def test_get_toggles(mock_client_class: Mock) -> None:
    """Test get_toggles method."""
    mock_client = Mock()
    mock_client.get.return_value = [
        {"name": "toggle1", "value": True},
        {"name": "toggle2", "value": 42},
    ]
    mock_client_class.return_value = mock_client

    toggle = FeatureToggle(application_id="app_123", api_key="key_123")
    result = toggle.get_toggles(["toggle1", "toggle2"])

    assert result == {"toggle1": True, "toggle2": 42}
    mock_client.get.assert_called_once()
