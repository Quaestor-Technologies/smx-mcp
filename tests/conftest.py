from __future__ import annotations

from typing import Any
from collections.abc import Generator
import pytest


@pytest.fixture(autouse=True)
def setup_test_env(monkeypatch: pytest.MonkeyPatch) -> Generator[None]:
    """Set up test environment variables."""
    monkeypatch.setenv("SMX_CLIENT_ID", "test_client_id")
    monkeypatch.setenv("SMX_CLIENT_SECRET", "test_client_secret")
    monkeypatch.setenv("STANDARD_METRICS_BASE_URL", "https://api.standardmetrics.io")
    monkeypatch.setenv("SMX_TOKEN_BASE_URL", "https://api.standardmetrics.io")

    from src import _settings, _auth, _client

    test_settings = _settings.Settings()
    monkeypatch.setattr(_settings, "settings", test_settings)
    monkeypatch.setattr(_auth, "settings", test_settings)
    monkeypatch.setattr(_client, "settings", test_settings)

    yield


@pytest.fixture
def mock_token_response() -> dict[str, Any]:
    """Mock OAuth2 token response."""
    return {
        "access_token": "test_access_token_12345",
        "token_type": "Bearer",
        "expires_in": 3600,
        "scope": "read write",
    }


@pytest.fixture
def sample_company_data() -> dict[str, Any]:
    """Sample company data for testing."""
    return {
        "id": "company_123",
        "name": "Test Company Inc.",
        "slug": "test-company",
        "description": "A test company for testing purposes",
        "city": "San Francisco",
        "sector": "B2B Software",
        "website": "https://testcompany.com",
        "status": "active",
    }


@pytest.fixture
def sample_metric_data() -> dict[str, Any]:
    """Sample metric data for testing."""
    return {
        "value": "1000000",
        "company_id": "company_123",
        "category": "revenue",
        "date": "2024-01-01T00:00:00Z",
        "metric_cadence": "month",
        "currency": "USD",
        "is_budget_metric": "false",
        "category_id": "cat_123",
        "updated_at": "2024-01-15T10:30:00Z",
    }


@pytest.fixture
def sample_paginated_response() -> dict[str, Any]:
    """Sample paginated response structure."""
    return {
        "results": [],
        "count": 0,
        "next": None,
        "previous": None,
    }


@pytest.fixture
def sample_metric_option_data() -> dict[str, Any]:
    """Sample metric option data for testing."""
    return {
        "id": "option_123",
        "name": "Revenue",
        "category_name": "revenue",
        "category_id": "cat_revenue_123",
        "is_standard": True,
        "type": "number",
        "is_point_in_time": False,
        "is_archived": False,
        "is_multiple": False,
        "choices": None,
    }


@pytest.fixture
def sample_budget_data() -> dict[str, Any]:
    """Sample budget data for testing."""
    return {
        "id": "budget_123",
        "name": "Test Budget",
        "description": "Test description",
        "date": "2024-01-01T00:00:00Z",
        "company": "company_123",
        "company_slug": "test-company",
        "color": "#000000",
    }
