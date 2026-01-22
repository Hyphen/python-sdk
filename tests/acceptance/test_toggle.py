"""Acceptance tests for FeatureToggle."""

import time

import pytest

from hyphen import FeatureToggle, ToggleContext
from tests.acceptance.testutil import Target, ToggleAdmin


@pytest.fixture
def admin() -> ToggleAdmin:
    """Create a ToggleAdmin instance."""
    return ToggleAdmin()


class TestToggleAcceptance:
    """Acceptance tests for Toggle service."""

    # NOTE: Tests that create toggles dynamically may experience ephemeral failures
    # due to a backend caching issue: https://github.com/Hyphen/apix/issues/1670

    def test_get_boolean_returns_true_when_toggle_default_is_true(
        self,
        admin: ToggleAdmin,
        public_api_key: str,
        application_id: str,
        toggle_base_url: str,
    ) -> None:
        """Test GetBoolean returns true when toggle default is true."""
        if not admin.is_configured():
            pytest.skip(f"Toggle admin not configured: missing {admin.missing_config()}")

        toggle_key = f"test-bool-true-{int(time.time() * 1000)}"
        admin.create_boolean_toggle(toggle_key, True)
        try:
            toggle = FeatureToggle(
                application_id=application_id,
                api_key=public_api_key,
                base_url=toggle_base_url,
            )

            result = toggle.get_boolean(toggle_key, default=False)

            # May fail due to backend caching issue (see note above)
            assert result is True
        finally:
            admin.delete_toggle(toggle_key)

    def test_get_boolean_returns_false_when_toggle_default_is_false(
        self,
        admin: ToggleAdmin,
        public_api_key: str,
        application_id: str,
        toggle_base_url: str,
    ) -> None:
        """Test GetBoolean returns false when toggle default is false."""
        if not admin.is_configured():
            pytest.skip(f"Toggle admin not configured: missing {admin.missing_config()}")

        toggle_key = f"test-bool-false-{int(time.time() * 1000)}"
        admin.create_boolean_toggle(toggle_key, False)
        try:
            toggle = FeatureToggle(
                application_id=application_id,
                api_key=public_api_key,
                base_url=toggle_base_url,
            )

            result = toggle.get_boolean(toggle_key, default=True)

            # May fail due to backend caching issue (see note above)
            assert result is False
        finally:
            admin.delete_toggle(toggle_key)

    def test_get_boolean_returns_default_for_nonexistent_toggle(
        self, public_api_key: str, application_id: str, toggle_base_url: str
    ) -> None:
        """Test get_boolean returns default for nonexistent toggle."""
        toggle = FeatureToggle(
            application_id=application_id,
            api_key=public_api_key,
            base_url=toggle_base_url,
        )

        result = toggle.get_boolean("nonexistent-toggle-abc123", default=True)

        assert result is True

    def test_get_string_returns_configured_value(
        self,
        admin: ToggleAdmin,
        public_api_key: str,
        application_id: str,
        toggle_base_url: str,
    ) -> None:
        """Test GetString returns configured value."""
        if not admin.is_configured():
            pytest.skip(f"Toggle admin not configured: missing {admin.missing_config()}")

        toggle_key = f"test-string-{int(time.time() * 1000)}"
        expected_value = "the-configured-string-value"
        admin.create_string_toggle(toggle_key, expected_value)
        try:
            toggle = FeatureToggle(
                application_id=application_id,
                api_key=public_api_key,
                base_url=toggle_base_url,
            )

            result = toggle.get_string(toggle_key, default="a-default-value")

            # May fail due to backend caching issue (see note above)
            assert result == expected_value
        finally:
            admin.delete_toggle(toggle_key)

    def test_get_string_returns_default_for_nonexistent_toggle(
        self, public_api_key: str, application_id: str, toggle_base_url: str
    ) -> None:
        """Test get_string returns default for nonexistent toggle."""
        toggle = FeatureToggle(
            application_id=application_id,
            api_key=public_api_key,
            base_url=toggle_base_url,
        )

        result = toggle.get_string("nonexistent-toggle-abc123", default="fallback")

        assert result == "fallback"

    def test_get_number_returns_configured_value(
        self,
        admin: ToggleAdmin,
        public_api_key: str,
        application_id: str,
        toggle_base_url: str,
    ) -> None:
        """Test GetNumber returns configured value."""
        if not admin.is_configured():
            pytest.skip(f"Toggle admin not configured: missing {admin.missing_config()}")

        toggle_key = f"test-number-{int(time.time() * 1000)}"
        expected_value = 42.5
        admin.create_number_toggle(toggle_key, expected_value)
        try:
            toggle = FeatureToggle(
                application_id=application_id,
                api_key=public_api_key,
                base_url=toggle_base_url,
            )

            result = toggle.get_number(toggle_key, default=0.0)

            # May fail due to backend caching issue (see note above)
            assert result == expected_value
        finally:
            admin.delete_toggle(toggle_key)

    def test_get_number_returns_default_for_nonexistent_toggle(
        self, public_api_key: str, application_id: str, toggle_base_url: str
    ) -> None:
        """Test get_number returns default for nonexistent toggle."""
        toggle = FeatureToggle(
            application_id=application_id,
            api_key=public_api_key,
            base_url=toggle_base_url,
        )

        result = toggle.get_number("nonexistent-toggle-abc123", default=42)

        assert result == 42

    def test_get_object_returns_default_for_nonexistent_toggle(
        self, public_api_key: str, application_id: str, toggle_base_url: str
    ) -> None:
        """Test get_object returns default for nonexistent toggle."""
        toggle = FeatureToggle(
            application_id=application_id,
            api_key=public_api_key,
            base_url=toggle_base_url,
        )

        result = toggle.get_object("nonexistent-toggle-abc123", default={"key": "value"})

        assert result == {"key": "value"}

    def test_evaluate_returns_toggles(
        self, public_api_key: str, application_id: str, toggle_base_url: str
    ) -> None:
        """Test that evaluate returns toggle evaluations."""
        toggle = FeatureToggle(
            application_id=application_id,
            api_key=public_api_key,
            base_url=toggle_base_url,
        )

        result = toggle.evaluate()

        assert result is not None
        assert hasattr(result, "toggles")
        assert isinstance(result.toggles, dict)

    def test_evaluate_with_targeting_context(
        self, public_api_key: str, application_id: str, toggle_base_url: str
    ) -> None:
        """Test evaluate with targeting context."""
        toggle = FeatureToggle(
            application_id=application_id,
            api_key=public_api_key,
            base_url=toggle_base_url,
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
        self, public_api_key: str, application_id: str, toggle_base_url: str
    ) -> None:
        """Test get_toggles with multiple toggle names."""
        toggle = FeatureToggle(
            application_id=application_id,
            api_key=public_api_key,
            base_url=toggle_base_url,
        )

        result = toggle.get_toggles(["toggle-a", "toggle-b", "toggle-c"])

        assert isinstance(result, dict)

    def test_get_boolean_returns_targeted_value_when_user_id_matches(
        self,
        admin: ToggleAdmin,
        public_api_key: str,
        application_id: str,
        toggle_base_url: str,
    ) -> None:
        """Test GetBoolean returns targeted value when user.id matches."""
        if not admin.is_configured():
            pytest.skip(f"Toggle admin not configured: missing {admin.missing_config()}")

        toggle_key = f"test-targeting-user-{int(time.time() * 1000)}"
        # JSONLogic: if user.id == "the-vip-user", return true
        targets = [
            Target(logic='{"==": [{"var": "user.id"}, "the-vip-user"]}', value=True)
        ]
        admin.create_boolean_toggle_with_targets(toggle_key, False, targets)
        try:
            toggle = FeatureToggle(
                application_id=application_id,
                api_key=public_api_key,
                base_url=toggle_base_url,
            )

            # With matching user ID
            result_with_match = toggle.get_boolean(
                toggle_key,
                default=False,
                context=ToggleContext(user={"id": "the-vip-user"}),
            )

            # With non-matching user ID
            result_without_match = toggle.get_boolean(
                toggle_key,
                default=False,
                context=ToggleContext(user={"id": "a-regular-user"}),
            )

            # May fail due to backend caching issue (see note above)
            assert result_with_match is True, "should return targeted value for matching user"
            assert result_without_match is False, "should return default value for non-matching user"
        finally:
            admin.delete_toggle(toggle_key)

    def test_get_string_returns_targeted_value_based_on_custom_attribute(
        self,
        admin: ToggleAdmin,
        public_api_key: str,
        application_id: str,
        toggle_base_url: str,
    ) -> None:
        """Test GetString returns targeted value based on custom attribute."""
        if not admin.is_configured():
            pytest.skip(f"Toggle admin not configured: missing {admin.missing_config()}")

        toggle_key = f"test-targeting-attr-{int(time.time() * 1000)}"
        # JSONLogic: if customAttributes.plan == "premium", return "the-premium-feature-value"
        targets = [
            Target(
                logic='{"==": [{"var": "customAttributes.plan"}, "premium"]}',
                value="the-premium-feature-value",
            )
        ]
        admin.create_string_toggle_with_targets(toggle_key, "the-default-feature-value", targets)
        try:
            toggle = FeatureToggle(
                application_id=application_id,
                api_key=public_api_key,
                base_url=toggle_base_url,
            )

            # With matching custom attribute
            result_premium = toggle.get_string(
                toggle_key,
                default="a-fallback",
                context=ToggleContext(custom_attributes={"plan": "premium"}),
            )

            # With non-matching custom attribute
            result_free = toggle.get_string(
                toggle_key,
                default="a-fallback",
                context=ToggleContext(custom_attributes={"plan": "free"}),
            )

            # May fail due to backend caching issue (see note above)
            assert result_premium == "the-premium-feature-value", "should return targeted value for premium plan"
            assert result_free == "the-default-feature-value", "should return default value for free plan"
        finally:
            admin.delete_toggle(toggle_key)

    def test_get_boolean_returns_targeted_value_based_on_targeting_key(
        self,
        admin: ToggleAdmin,
        public_api_key: str,
        application_id: str,
        toggle_base_url: str,
    ) -> None:
        """Test GetBoolean returns targeted value based on targeting key."""
        if not admin.is_configured():
            pytest.skip(f"Toggle admin not configured: missing {admin.missing_config()}")

        toggle_key = f"test-targeting-key-{int(time.time() * 1000)}"
        # JSONLogic: if targetingKey == "the-beta-tester", return true
        targets = [
            Target(logic='{"==": [{"var": "targetingKey"}, "the-beta-tester"]}', value=True)
        ]
        admin.create_boolean_toggle_with_targets(toggle_key, False, targets)
        try:
            toggle = FeatureToggle(
                application_id=application_id,
                api_key=public_api_key,
                base_url=toggle_base_url,
            )

            # With matching targeting key
            result_beta = toggle.get_boolean(
                toggle_key,
                default=False,
                context=ToggleContext(targeting_key="the-beta-tester"),
            )

            # With non-matching targeting key
            result_regular = toggle.get_boolean(
                toggle_key,
                default=False,
                context=ToggleContext(targeting_key="a-regular-user"),
            )

            # May fail due to backend caching issue (see note above)
            assert result_beta is True, "should return targeted value for beta tester"
            assert result_regular is False, "should return default value for regular user"
        finally:
            admin.delete_toggle(toggle_key)
