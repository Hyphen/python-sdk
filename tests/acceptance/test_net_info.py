"""Acceptance tests for NetInfo."""

from hyphen import IpInfo, IpInfoError, NetInfo


class TestNetInfoAcceptance:
    """Acceptance tests for NetInfo service."""

    def test_get_ip_info_valid_ip(self, api_key: str, netinfo_base_url: str) -> None:
        """Test get_ip_info with a valid IP address."""
        net_info = NetInfo(api_key=api_key, base_url=netinfo_base_url)

        result = net_info.get_ip_info("8.8.8.8")

        assert isinstance(result, IpInfo)
        assert result.ip == "8.8.8.8"
        assert result.location is not None
        assert result.location.country != ""

    def test_get_ip_info_cloudflare_dns(self, api_key: str, netinfo_base_url: str) -> None:
        """Test get_ip_info with Cloudflare DNS."""
        net_info = NetInfo(api_key=api_key, base_url=netinfo_base_url)

        result = net_info.get_ip_info("1.1.1.1")

        assert isinstance(result, IpInfo)
        assert result.ip == "1.1.1.1"
        assert result.location is not None

    def test_get_ip_infos_multiple(self, api_key: str, netinfo_base_url: str) -> None:
        """Test get_ip_infos with multiple IP addresses."""
        net_info = NetInfo(api_key=api_key, base_url=netinfo_base_url)

        result = net_info.get_ip_infos(["8.8.8.8", "1.1.1.1"])

        assert len(result) == 2
        assert all(isinstance(r, (IpInfo, IpInfoError)) for r in result)

    def test_get_ip_infos_empty_raises_error(self, api_key: str, netinfo_base_url: str) -> None:
        """Test get_ip_infos with empty array raises error."""
        import pytest

        net_info = NetInfo(api_key=api_key, base_url=netinfo_base_url)

        with pytest.raises(ValueError):
            net_info.get_ip_infos([])
