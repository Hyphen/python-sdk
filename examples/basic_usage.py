"""Basic usage examples for the Hyphen Python SDK."""

import os

from hyphen import FeatureToggle, Link, NetInfo, QrSize


def feature_toggle_example():
    """Example of using FeatureToggle."""
    print("\n=== Feature Toggle Example ===")

    # Initialize with environment variables
    # Requires: HYPHEN_APPLICATION_ID and HYPHEN_API_KEY or HYPHEN_PUBLIC_API_KEY
    toggle = FeatureToggle()

    # Get a single toggle
    value = toggle.get_toggle("hyphen-sdk-boolean")
    print(f"Toggle 'hyphen-sdk-boolean': {value}")

    # Get multiple toggles
    toggles = toggle.get_toggles(["hyphen-sdk-boolean", "hyphen-sdk-number", "hyphen-sdk-string"])
    print(f"Multiple toggles: {toggles}")


def net_info_example():
    """Example of using NetInfo."""
    print("\n=== NetInfo Example ===")

    # Initialize with environment variables or explicit API key
    net_info = NetInfo()

    # Get info for a single IP
    ip_info = net_info.get_ip_info("8.8.8.8")
    print(f"IP Info for 8.8.8.8: {ip_info}")

    # Get info for multiple IPs
    ips = ["8.8.8.8", "1.1.1.1"]
    ip_infos = net_info.get_ip_infos(ips)
    print(f"Multiple IP Infos: {ip_infos}")


def link_example():
    """Example of using Link."""
    print("\n=== Link Example ===")

    # Initialize with environment variables
    # Requires: HYPHEN_ORGANIZATION_ID and HYPHEN_API_KEY
    link = Link()

    # Create a short code
    response = link.create_short_code(
        long_url="https://hyphen.ai",
        domain=os.environ.get("HYPHEN_LINK_DOMAIN", "test.h4n.link"),
        options={"tags": ["sdk-test", "example"]},
    )
    print(f"Created short code: {response}")

    # Get all short codes with tags
    codes = link.get_short_codes(tags=["sdk-test"])
    print(f"Short codes with 'sdk-test' tag: {len(codes)} found")

    # Create a QR code
    if response and "code" in response:
        qr_response = link.create_qr_code(
            code=response["code"],
            options={
                "title": "Example QR Code",
                "size": QrSize.MEDIUM,
                "backgroundColor": "#ffffff",
                "color": "#000000",
            },
        )
        print(f"Created QR code: {qr_response}")


if __name__ == "__main__":
    print("Hyphen Python SDK - Basic Usage Examples")
    print("=========================================")

    # Check for required environment variables
    required_vars = {
        "FeatureToggle": ["HYPHEN_APPLICATION_ID", "HYPHEN_API_KEY"],
        "NetInfo": ["HYPHEN_API_KEY"],
        "Link": ["HYPHEN_ORGANIZATION_ID", "HYPHEN_API_KEY"],
    }

    print("\nNote: These examples require environment variables to be set:")
    for service, vars in required_vars.items():
        print(f"  {service}: {', '.join(vars)}")

    # Run examples if environment variables are set
    try:
        if os.environ.get("HYPHEN_APPLICATION_ID"):
            feature_toggle_example()
        else:
            print("\nSkipping FeatureToggle example (HYPHEN_APPLICATION_ID not set)")

        if os.environ.get("HYPHEN_API_KEY"):
            net_info_example()
        else:
            print("\nSkipping NetInfo example (HYPHEN_API_KEY not set)")

        if os.environ.get("HYPHEN_ORGANIZATION_ID"):
            link_example()
        else:
            print("\nSkipping Link example (HYPHEN_ORGANIZATION_ID not set)")

    except Exception as e:
        print(f"\nError running examples: {e}")
        print("Make sure your API credentials are correct and have the necessary permissions.")
