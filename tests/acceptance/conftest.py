"""Fixtures for acceptance tests."""

import os

import pytest


def _require_env(name: str) -> str:
    """Get required environment variable or skip test."""
    value = os.environ.get(name)
    if not value:
        pytest.skip(f"Missing required environment variable: {name}")
    return value


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
