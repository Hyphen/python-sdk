# Acceptance Tests

Integration tests that run against the real Hyphen API.

## Required Environment Variables

### Toggle Tests
- `HYPHEN_PUBLIC_API_KEY`: Public API key for Toggle service (starts with `public_`)
- `HYPHEN_APPLICATION_ID`: Application ID for Toggle evaluations

### NetInfo Tests
- `HYPHEN_API_KEY`: API key for NetInfo service

### Link Tests
- `HYPHEN_API_KEY`: API key for Link service
- `HYPHEN_ORGANIZATION_ID`: Organization ID
- `HYPHEN_LINK_DOMAIN`: Domain for short codes (e.g., `test.h4n.link`)

## Running Tests

Run all acceptance tests:
```bash
pytest tests/acceptance/ -v
```

Run specific test suites:
```bash
pytest tests/acceptance/test_toggle.py -v
pytest tests/acceptance/test_net_info.py -v
pytest tests/acceptance/test_link.py -v
```

Tests are excluded from normal test runs (require `tests/acceptance/` path).
