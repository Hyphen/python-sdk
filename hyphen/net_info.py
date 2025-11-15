"""NetInfo for IP geolocation in Hyphen SDK."""

from typing import Any, Dict, List, Optional

from hyphen.base_client import BaseClient


class NetInfo:
    """Client for IP geolocation services in Hyphen."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.hyphen.ai",
    ):
        """
        Initialize the NetInfo client.

        Args:
            api_key: API key for authentication. If not provided, will check HYPHEN_API_KEY env var.
            base_url: Base URL for the Hyphen API.
        """
        self.client = BaseClient(api_key=api_key, base_url=base_url)

    def get_ip_info(self, ip_address: str) -> Dict[str, Any]:
        """
        Get geolocation information for a single IP address.

        Args:
            ip_address: IP address to look up

        Returns:
            Dictionary containing IP geolocation information

        Raises:
            requests.HTTPError: If the request fails
        """
        endpoint = f"/api/net-info/ip/{ip_address}"
        return self.client.get(endpoint)

    def get_ip_infos(self, ip_addresses: List[str]) -> List[Dict[str, Any]]:
        """
        Get geolocation information for multiple IP addresses.

        Args:
            ip_addresses: List of IP addresses to look up

        Returns:
            List of dictionaries containing IP geolocation information

        Raises:
            requests.HTTPError: If the request fails
        """
        endpoint = "/api/net-info/ips"
        data = {"ips": ip_addresses}
        return self.client.post(endpoint, data=data)
