# Hyphen Python SDK

The official Python SDK for [Hyphen](https://hyphen.ai) - providing feature toggles, IP geolocation, and link shortening services.

## Installation

```bash
pip install hyphen
```

For development:
```bash
pip install hyphen[dev]
```

## Quick Start

### Environment Variables

You can set API credentials using environment variables:

```bash
export HYPHEN_API_KEY="your_api_key"
export HYPHEN_PUBLIC_API_KEY="your_public_api_key"
export HYPHEN_APPLICATION_ID="your_application_id"
export HYPHEN_ORGANIZATION_ID="your_organization_id"
```

## Feature Toggles

Manage feature flags for your application.

* [Website](https://hyphen.ai)
* [Guides](https://docs.hyphen.ai)

### Get a Single Toggle

```python
from hyphen import FeatureToggle

toggle = FeatureToggle(
    application_id='your_application_id',
    api_key='your_api_key',
)

value = toggle.get_toggle('hyphen-sdk-boolean')
print('Toggle value:', value)
```

### Get Multiple Toggles

```python
from hyphen import FeatureToggle

toggle = FeatureToggle(
    application_id='your_application_id',
    api_key='your_api_key',
)

toggles = toggle.get_toggles(['hyphen-sdk-boolean', 'hyphen-sdk-number', 'hyphen-sdk-string'])
print('Toggles:', toggles)
```

Toggles support multiple data types:
- Boolean: `True` or `False`
- Number: `42` (int or float)
- String: `"Hello World!"`
- JSON: `{"id": "Hello World!"}`

## NetInfo - IP Geolocation

Look up IP address geolocation information.

* [Website](https://hyphen.ai)
* [Guides](https://docs.hyphen.ai)

### Get Single IP Information

```python
from hyphen import NetInfo

net_info = NetInfo(api_key='your_api_key')

ip_info = net_info.get_ip_info('8.8.8.8')
print('IP Info:', ip_info)
```

### Get Multiple IP Information

```python
from hyphen import NetInfo

net_info = NetInfo(api_key='your_api_key')

ips = ['8.8.8.8', '1.1.1.1']
ip_infos = net_info.get_ip_infos(ips)
print('IP Infos:', ip_infos)
```

## Link - Short Code Service

Create and manage short URLs and QR codes.

* [Website](https://hyphen.ai/link)
* [Guides](https://docs.hyphen.ai/docs/create-short-link)
* [API Reference](https://docs.hyphen.ai/reference/post_api-organizations-organizationid-link-codes)

### Creating a Short Code

```python
from hyphen import Link

link = Link(
    organization_id='your_organization_id',
    api_key='your_api_key',
)

response = link.create_short_code(
    long_url='https://hyphen.ai',
    domain='test.h4n.link',
    options={
        'tags': ['sdk-test', 'unit-test'],
    }
)
print('Short Code Response:', response)
```

### Updating a Short Code

```python
from hyphen import Link

link = Link(
    organization_id='your_organization_id',
    api_key='your_api_key',
)

response = link.update_short_code(
    code='code_1234567890',
    options={
        'title': 'Updated Short Code',
        'tags': ['sdk-test', 'unit-test'],
        'long_url': 'https://hyphen.ai/updated',
    }
)
print('Update Response:', response)
```

### Getting a Short Code

```python
from hyphen import Link

link = Link(
    organization_id='your_organization_id',
    api_key='your_api_key',
)

response = link.get_short_code('code_1234567890')
print('Short Code:', response)
```

### Getting Short Codes

```python
from hyphen import Link

link = Link(
    organization_id='your_organization_id',
    api_key='your_api_key',
)

response = link.get_short_codes(
    title='My Short Codes',
    tags=['sdk-test', 'unit-test']
)
print('Short Codes:', response)
```

### Getting Organization Tags

```python
from hyphen import Link

link = Link(
    organization_id='your_organization_id',
    api_key='your_api_key',
)

tags = link.get_tags()
print('Tags:', tags)
```

### Get Short Code Stats

```python
from hyphen import Link
from datetime import datetime

link = Link(
    organization_id='your_organization_id',
    api_key='your_api_key',
)

stats = link.get_short_code_stats(
    code='code_1234567890',
    start_date=datetime(2023, 1, 1),
    end_date=datetime(2023, 12, 31)
)
print('Stats:', stats)
```

### Deleting a Short Code

```python
from hyphen import Link

link = Link(
    organization_id='your_organization_id',
    api_key='your_api_key',
)

response = link.delete_short_code('code_1234567890')
print('Delete Response:', response)
```

### Creating a QR Code

```python
from hyphen import Link, QrSize

link = Link(
    organization_id='your_organization_id',
    api_key='your_api_key',
)

response = link.create_qr_code(
    code='code_1234567890',
    options={
        'title': 'My QR Code',
        'backgroundColor': '#ffffff',
        'color': '#000000',
        'size': QrSize.MEDIUM,
    }
)
print('QR Code:', response)
```

### Get QR Code by ID

```python
from hyphen import Link

link = Link(
    organization_id='your_organization_id',
    api_key='your_api_key',
)

response = link.get_qr_code('code_1234567890', 'qr_1234567890')
print('QR Code:', response)
```

### Get QR Codes for a Short Code

```python
from hyphen import Link

link = Link(
    organization_id='your_organization_id',
    api_key='your_api_key',
)

response = link.get_qr_codes('code_1234567890')
print('QR Codes:', response)
```

### Deleting a QR Code

```python
from hyphen import Link

link = Link(
    organization_id='your_organization_id',
    api_key='your_api_key',
)

response = link.delete_qr_code('code_1234567890', 'qr_1234567890')
print('Delete Response:', response)
```

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/Hyphen/python-sdk.git
cd python-sdk

# Install dependencies
pip install -e ".[dev]"
```

### Testing

Create a `.env` file with your test credentials:

```bash
HYPHEN_PUBLIC_API_KEY=your_public_api_key
HYPHEN_API_KEY=your_api_key
HYPHEN_APPLICATION_ID=your_application_id
HYPHEN_LINK_DOMAIN=your_link_domain
HYPHEN_ORGANIZATION_ID=your_organization_id
```

Run tests:

```bash
pytest
```

### Linting

```bash
ruff check hyphen tests
```

### Type Checking

```bash
mypy hyphen
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes and commit them with clear messages:
   - `feat: describe the feature`
   - `fix: describe the bug fix`
   - `chore: describe maintenance task`
4. Run tests and linting to ensure quality
5. Push your changes to your forked repository
6. Create a pull request to the main repository

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Copyright © 2024 Hyphen, Inc. All rights reserved.
