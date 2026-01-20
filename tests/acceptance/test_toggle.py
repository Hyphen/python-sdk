"""Acceptance tests for FeatureToggle."""

from hyphen import FeatureToggle, ToggleContext


class TestToggleAcceptance:
    """Acceptance tests for Toggle service."""

    def test_evaluate_returns_toggles(
        self, public_api_key: str, application_id: str
    ) -> None:
        """Test that evaluate returns toggle evaluations."""
        toggle = FeatureToggle(
            application_id=application_id,
            api_key=public_api_key,
        )

        result = toggle.evaluate()

        assert result is not None
        assert hasattr(result, "toggles")
        assert isinstance(result.toggles, dict)

    def test_get_boolean_with_default(
        self, public_api_key: str, application_id: str
    ) -> None:
        """Test get_boolean returns default for nonexistent toggle."""
        toggle = FeatureToggle(
            application_id=application_id,
            api_key=public_api_key,
        )

        result = toggle.get_boolean("nonexistent-toggle-abc123", default=True)

        assert result is True

    def test_get_string_with_default(
        self, public_api_key: str, application_id: str
    ) -> None:
        """Test get_string returns default for nonexistent toggle."""
        toggle = FeatureToggle(
            application_id=application_id,
            api_key=public_api_key,
        )

        result = toggle.get_string("nonexistent-toggle-abc123", default="fallback")

        assert result == "fallback"

    def test_get_number_with_default(
        self, public_api_key: str, application_id: str
    ) -> None:
        """Test get_number returns default for nonexistent toggle."""
        toggle = FeatureToggle(
            application_id=application_id,
            api_key=public_api_key,
        )

        result = toggle.get_number("nonexistent-toggle-abc123", default=42)

        assert result == 42

    def test_get_object_with_default(
        self, public_api_key: str, application_id: str
    ) -> None:
        """Test get_object returns default for nonexistent toggle."""
        toggle = FeatureToggle(
            application_id=application_id,
            api_key=public_api_key,
        )

        result = toggle.get_object("nonexistent-toggle-abc123", default={"key": "value"})

        assert result == {"key": "value"}

    def test_evaluate_with_targeting_context(
        self, public_api_key: str, application_id: str
    ) -> None:
        """Test evaluate with targeting context."""
        toggle = FeatureToggle(
            application_id=application_id,
            api_key=public_api_key,
        )
        context = ToggleContext(
            targeting_key="test-user-123",
            ip_address="8.8.8.8",
            custom_attributes={"plan": "premium"},
        )

        result = toggle.evaluate(context)

        assert result is not None
        assert isinstance(result.toggles, dict)

    def test_get_toggles_multiple(
        self, public_api_key: str, application_id: str
    ) -> None:
        """Test get_toggles with multiple toggle names."""
        toggle = FeatureToggle(
            application_id=application_id,
            api_key=public_api_key,
        )

        result = toggle.get_toggles(["toggle-a", "toggle-b", "toggle-c"])

        assert isinstance(result, dict)
