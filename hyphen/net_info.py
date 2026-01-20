"""NetInfo for IP geolocation in Hyphen SDK."""


from hyphen.base_client import BaseClient
from hyphen.types import IpInfo, IpInfoError


class NetInfo:
    """Client for IP geolocation services in Hyphen."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://api.hyphen.ai",
    ):
        """
        Initialize the NetInfo client.

        Args:
            api_key: API key for authentication. If not provided, will check HYPHEN_API_KEY env var.
            base_url: Base URL for the Hyphen API.
        """
        self.client = BaseClient(api_key=api_key, base_url=base_url)

    def get_ip_info(self, ip_address: str) -> IpInfo | IpInfoError:
        """
        Get geolocation information for a single IP address.

        Args:
            ip_address: IP address to look up

        Returns:
            IpInfo with geolocation data, or IpInfoError if lookup failed

        Raises:
            requests.HTTPError: If the request fails
        """
        endpoint = f"/api/net-info/ip/{ip_address}"
        response = self.client.get(endpoint)
        if "errorMessage" in response:
            return IpInfoError.from_dict(response)
        return IpInfo.from_dict(response)

    def get_ip_infos(self, ip_addresses: list[str]) -> list[IpInfo | IpInfoError]:
        """
        Get geolocation information for multiple IP addresses.

        Args:
            ip_addresses: List of IP addresses to look up

        Returns:
            List of IpInfo or IpInfoError objects for each IP

        Raises:
            requests.HTTPError: If the request fails
        """
        endpoint = "/api/net-info/ips"
        data = {"ips": ip_addresses}
        response = self.client.post(endpoint, data=data)
        results: list[IpInfo | IpInfoError] = []
        for item in response:
            if "errorMessage" in item:
                results.append(IpInfoError.from_dict(item))
            else:
                results.append(IpInfo.from_dict(item))
        return results
