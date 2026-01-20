"""Acceptance tests for NetInfo."""

from hyphen import IpInfo, IpInfoError, NetInfo


class TestNetInfoAcceptance:
    """Acceptance tests for NetInfo service."""

    def test_get_ip_info_valid_ip(self, api_key: str) -> None:
        """Test get_ip_info with a valid IP address."""
        net_info = NetInfo(api_key=api_key)

        result = net_info.get_ip_info("8.8.8.8")

        assert isinstance(result, IpInfo)
        assert result.ip == "8.8.8.8"
        assert result.ip_type == "ipv4"
        assert result.location is not None
        assert result.location.country == "United States"

    def test_get_ip_info_ipv6(self, api_key: str) -> None:
        """Test get_ip_info with an IPv6 address."""
        net_info = NetInfo(api_key=api_key)

        result = net_info.get_ip_info("2001:4860:4860::8888")

        assert isinstance(result, IpInfo)
        assert result.ip_type == "ipv6"

    def test_get_ip_info_invalid_ip(self, api_key: str) -> None:
        """Test get_ip_info with an invalid IP address."""
        net_info = NetInfo(api_key=api_key)

        result = net_info.get_ip_info("invalid-ip")

        assert isinstance(result, IpInfoError)
        assert result.error_message != ""

    def test_get_ip_infos_multiple(self, api_key: str) -> None:
        """Test get_ip_infos with multiple IP addresses."""
        net_info = NetInfo(api_key=api_key)

        result = net_info.get_ip_infos(["8.8.8.8", "1.1.1.1"])

        assert len(result) == 2
        assert all(isinstance(r, (IpInfo, IpInfoError)) for r in result)

    def test_get_ip_infos_mixed_valid_invalid(self, api_key: str) -> None:
        """Test get_ip_infos with mix of valid and invalid IPs."""
        net_info = NetInfo(api_key=api_key)

        result = net_info.get_ip_infos(["8.8.8.8", "invalid-ip"])

        assert len(result) == 2
        # First should be valid
        assert isinstance(result[0], IpInfo)
        # Second should be error
        assert isinstance(result[1], IpInfoError)
