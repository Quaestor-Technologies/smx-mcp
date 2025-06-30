from __future__ import annotations

from typing import Any
import pytest
from aioresponses import aioresponses
import datetime as dt

from src._client import StandardMetrics


@pytest.fixture
def api_client() -> StandardMetrics:
    """Create a StandardMetrics client for testing."""
    return StandardMetrics()


def _build_paginated_mock_response(response: list[dict[str, Any]]) -> dict[str, Any]:
    """Build a paginated mock response."""
    return {
        "results": response,
        "count": len(response),
    }


@pytest.fixture
def mock_token_response(
    aioresponses: aioresponses,
    mock_token_response: dict[str, Any],
) -> None:
    """Mock token response."""
    aioresponses.post(  # type: ignore
        "https://api.standardmetrics.io/o/token/",
        payload=mock_token_response,
    )


@pytest.mark.asyncio
async def test_get_company_metrics(
    api_client: StandardMetrics,
    sample_metric_data: dict[str, Any],
    mock_token_response: None,
    aioresponses: aioresponses,
) -> None:
    """Test get_company_metrics method."""
    aioresponses.get(  # type: ignore
        "https://api.standardmetrics.io/v1/metrics/?company_id=company_123&page=1&page_size=100",
        payload=_build_paginated_mock_response([sample_metric_data]),
    )
    async with api_client:
        result = await api_client.get_company_metrics("company_123")

    assert result.count == 1
    assert len(result.results) == 1
    assert result.results[0].value == sample_metric_data["value"]
    assert result.results[0].category == sample_metric_data["category"]
    expected_date = dt.datetime.strptime(
        sample_metric_data["date"], "%Y-%m-%dT%H:%M:%SZ"
    ).replace(tzinfo=dt.timezone.utc)
    assert result.results[0].date.timestamp() == expected_date.timestamp()


@pytest.mark.asyncio
async def test_get_metrics_options(
    api_client: StandardMetrics,
    sample_metric_option_data: dict[str, Any],
    mock_token_response: None,
    aioresponses: aioresponses,
) -> None:
    """Test get_metrics_options method."""
    aioresponses.get(  # type: ignore
        "https://api.standardmetrics.io/v1/metrics/options/?page=1&page_size=100",
        payload=_build_paginated_mock_response([sample_metric_option_data]),
    )
    async with api_client:
        result = await api_client.get_metrics_options()
    assert result.count == 1
    assert len(result.results) == 1
    assert result.results[0].category_name == sample_metric_option_data["category_name"]
    assert result.results[0].is_standard == sample_metric_option_data["is_standard"]
    assert result.results[0].type == sample_metric_option_data["type"]


@pytest.mark.asyncio
async def test_list_budgets(
    api_client: StandardMetrics,
    sample_budget_data: dict[str, Any],
    mock_token_response: None,
    aioresponses: aioresponses,
) -> None:
    """Test list_budgets method."""
    aioresponses.get(  # type: ignore
        "https://api.standardmetrics.io/v1/budgets/?page=1&page_size=100",
        payload=_build_paginated_mock_response([sample_budget_data]),
    )
    async with api_client:
        result = await api_client.list_budgets()
    assert result.count == 1
    assert len(result.results) == 1
    assert result.results[0].name == sample_budget_data["name"]
    assert result.results[0].company == sample_budget_data["company"]
    assert result.results[0].company_slug == sample_budget_data["company_slug"]
