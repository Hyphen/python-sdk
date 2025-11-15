"""Tests for NetInfo."""

from unittest.mock import Mock, patch

from hyphen import NetInfo


@patch("hyphen.net_info.BaseClient")
def test_get_ip_info(mock_client_class: Mock) -> None:
    """Test get_ip_info method."""
    mock_client = Mock()
    mock_client.get.return_value = {
        "ip": "8.8.8.8",
        "country": "US",
        "city": "Mountain View",
    }
    mock_client_class.return_value = mock_client

    net_info = NetInfo(api_key="key_123")
    result = net_info.get_ip_info("8.8.8.8")

    assert result["ip"] == "8.8.8.8"
    assert result["country"] == "US"
    mock_client.get.assert_called_once_with("/api/net-info/ip/8.8.8.8")


@patch("hyphen.net_info.BaseClient")
def test_get_ip_infos(mock_client_class: Mock) -> None:
    """Test get_ip_infos method."""
    mock_client = Mock()
    mock_client.post.return_value = [
        {"ip": "8.8.8.8", "country": "US"},
        {"ip": "1.1.1.1", "country": "AU"},
    ]
    mock_client_class.return_value = mock_client

    net_info = NetInfo(api_key="key_123")
    result = net_info.get_ip_infos(["8.8.8.8", "1.1.1.1"])

    assert len(result) == 2
    assert result[0]["ip"] == "8.8.8.8"
    assert result[1]["ip"] == "1.1.1.1"
    mock_client.post.assert_called_once_with(
        "/api/net-info/ips",
        data={"ips": ["8.8.8.8", "1.1.1.1"]}
    )
