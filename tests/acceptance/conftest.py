"""Fixtures for acceptance tests."""

import os

import pytest


def _require_env(name: str) -> str:
    """Get required environment variable or skip test."""
    value = os.environ.get(name)
    if not value:
        pytest.skip(f"Missing required environment variable: {name}")
    return value


def _is_dev_mode() -> bool:
    """Check if HYPHEN_DEV is set to true."""
    return os.environ.get("HYPHEN_DEV", "").lower() == "true"


# Dev URLs
DEV_TOGGLE_URL = "https://dev-horizon.hyphen.ai"
DEV_NETINFO_URL = "https://dev.net.info"
DEV_LINK_URL = "https://dev-api.hyphen.ai"

# Production URLs
PROD_TOGGLE_URL = "https://toggle.hyphen.cloud"
PROD_NETINFO_URL = "https://net.info"
PROD_LINK_URL = "https://api.hyphen.ai"


@pytest.fixture
def public_api_key() -> str:
    """Public API key for Toggle service."""
    return _require_env("HYPHEN_PUBLIC_API_KEY")


@pytest.fixture
def application_id() -> str:
    """Application ID for Toggle evaluations."""
    return _require_env("HYPHEN_APPLICATION_ID")


@pytest.fixture
def api_key() -> str:
    """API key for authenticated services."""
    return _require_env("HYPHEN_API_KEY")


@pytest.fixture
def organization_id() -> str:
    """Organization ID."""
    return _require_env("HYPHEN_ORGANIZATION_ID")


@pytest.fixture
def link_domain() -> str:
    """Domain for short codes."""
    return _require_env("HYPHEN_LINK_DOMAIN")


@pytest.fixture
def toggle_base_url() -> str:
    """Base URL for Toggle service."""
    return DEV_TOGGLE_URL if _is_dev_mode() else PROD_TOGGLE_URL


@pytest.fixture
def netinfo_base_url() -> str:
    """Base URL for NetInfo service."""
    return DEV_NETINFO_URL if _is_dev_mode() else PROD_NETINFO_URL


@pytest.fixture
def link_base_url() -> str:
    """Base URL for Link service."""
    return DEV_LINK_URL if _is_dev_mode() else PROD_LINK_URL
