from __future__ import annotations

from typing import Any
import pytest
from aioresponses import aioresponses
from fastmcp import Client, FastMCP
from src.server import mcp
import json


def _build_paginated_mock_response(response: list[dict[str, Any]]) -> dict[str, Any]:
    """Build a paginated mock response."""
    return {
        "results": response,
        "count": len(response),
        "next": None,
        "previous": None,
    }


@pytest.fixture
def mcp_server() -> FastMCP[Any]:
    """Return the MCP server instance for testing."""
    return mcp


@pytest.fixture
def mock_token_response_fixture(
    aioresponses: aioresponses,
    mock_token_response: dict[str, Any],
) -> None:
    """Mock token response."""
    aioresponses.post(  # type: ignore
        "https://api.standardmetrics.io/o/token/",
        payload=mock_token_response,
    )


@pytest.mark.asyncio
async def test_list_companies(
    mcp_server: FastMCP[Any],
    sample_company_data: dict[str, Any],
    mock_token_response_fixture: None,
    aioresponses: aioresponses,
) -> None:
    """Test list_companies tool."""
    aioresponses.get(  # type: ignore
        "https://api.standardmetrics.io/v1/companies/?page=1&page_size=100",
        payload=_build_paginated_mock_response([sample_company_data]),
    )

    async with Client(mcp_server) as client:
        result = await client.call_tool("list_companies", {"page": 1, "per_page": 100})

        data = json.loads(result[0].text)

        assert data["count"] == 1
        assert len(data["results"]) == 1
        assert data["results"][0]["id"] == "company_123"
        assert data["results"][0]["name"] == "Test Company Inc."


@pytest.mark.asyncio
async def test_get_company(
    mcp_server: FastMCP[Any],
    sample_company_data: dict[str, Any],
    mock_token_response_fixture: None,
    aioresponses: aioresponses,
) -> None:
    """Test get_company tool."""
    aioresponses.get(  # type: ignore
        "https://api.standardmetrics.io/v1/companies/?page=1&page_size=100",
        payload=_build_paginated_mock_response([sample_company_data]),
    )

    async with Client(mcp_server) as client:
        result = await client.call_tool("get_company", {"company_id": "company_123"})

        data = json.loads(result[0].text)

        assert data["id"] == "company_123"
        assert data["name"] == "Test Company Inc."
        assert data["city"] == "San Francisco"


@pytest.mark.asyncio
async def test_get_metrics_options(
    mcp_server: FastMCP[Any],
    sample_metric_option_data: dict[str, Any],
    mock_token_response_fixture: None,
    aioresponses: aioresponses,
) -> None:
    """Test get_metrics_options tool."""
    aioresponses.get(  # type: ignore
        "https://api.standardmetrics.io/v1/metrics/options/?page=1&page_size=100",
        payload=_build_paginated_mock_response([sample_metric_option_data]),
    )

    async with Client(mcp_server) as client:
        result = await client.call_tool("get_metrics_options", {})

        data = json.loads(result[0].text)

        assert data["count"] == 1
        assert len(data["results"]) == 1
        assert data["results"][0]["category_name"] == "revenue"


@pytest.mark.asyncio
async def test_list_budgets(
    mcp_server: FastMCP[Any],
    sample_budget_data: dict[str, Any],
    mock_token_response_fixture: None,
    aioresponses: aioresponses,
) -> None:
    """Test list_budgets tool."""
    aioresponses.get(  # type: ignore
        "https://api.standardmetrics.io/v1/budgets/?company_slug=test-company&company_id=company_123&page=1&page_size=20",
        payload=_build_paginated_mock_response([sample_budget_data]),
    )

    async with Client(mcp_server) as client:
        result = await client.call_tool(
            "list_budgets",
            {
                "company_slug": "test-company",
                "company_id": "company_123",
                "page": 1,
                "per_page": 20,
            },
        )

        data = json.loads(result[0].text)

        assert data["count"] == 1
        assert len(data["results"]) == 1
        assert data["results"][0]["name"] == "Test Budget"
        assert data["results"][0]["company"] == "company_123"


@pytest.mark.asyncio
async def test_search_companies_by_name(
    mcp_server: FastMCP[Any],
    mock_token_response_fixture: None,
    aioresponses: aioresponses,
) -> None:
    """Test search_companies tool with name filtering."""
    companies = [
        {
            "id": "company_123",
            "name": "Test Company Inc.",
            "slug": "test-company",
            "city": "San Francisco",
            "sector": "B2B Software",
        },
        {
            "id": "company_456",
            "name": "Another Corp",
            "slug": "another-corp",
            "city": "New York",
            "sector": "Fintech",
        },
        {
            "id": "company_789",
            "name": "Test Labs LLC",
            "slug": "test-labs",
            "city": "Boston",
            "sector": "Health Technology",
        },
    ]

    aioresponses.get(  # type: ignore
        "https://api.standardmetrics.io/v1/companies/?page=1&page_size=100",
        payload=_build_paginated_mock_response(companies),
    )

    async with Client(mcp_server) as client:
        result = await client.call_tool("search_companies", {"name_contains": "Test"})

        data = json.loads(result[0].text)

        assert len(data) == 2
        assert all("Test" in company["name"] for company in data)
        company_names = [company["name"] for company in data]
        assert "Test Company Inc." in company_names
        assert "Test Labs LLC" in company_names


@pytest.mark.asyncio
async def test_search_companies_multiple_filters(
    mcp_server: FastMCP[Any],
    mock_token_response_fixture: None,
    aioresponses: aioresponses,
) -> None:
    """Test search_companies tool with multiple filters combined."""
    companies = [
        {
            "id": "company_123",
            "name": "Tech Startup Inc.",
            "slug": "tech-startup",
            "city": "San Francisco",
            "sector": "B2B Software",
        },
        {
            "id": "company_456",
            "name": "Tech Corp NYC",
            "slug": "tech-corp-nyc",
            "city": "New York",
            "sector": "B2B Software",
        },
        {
            "id": "company_789",
            "name": "SF Health Tech",
            "slug": "sf-health",
            "city": "San Francisco",
            "sector": "Health Technology",
        },
        {
            "id": "company_101",
            "name": "Tech Solutions SF",
            "slug": "tech-solutions",
            "city": "San Francisco",
            "sector": "B2B Software",
        },
    ]

    aioresponses.get(  # type: ignore
        "https://api.standardmetrics.io/v1/companies/?page=1&page_size=100",
        payload=_build_paginated_mock_response(companies),
    )

    async with Client(mcp_server) as client:
        result = await client.call_tool(
            "search_companies",
            {
                "name_contains": "Tech",
                "city": "San Francisco",
                "sector": "B2B Software",
            },
        )

        data = json.loads(result[0].text)

        assert len(data) == 2
        assert all("Tech" in company["name"] for company in data)
        assert all(company["city"] == "San Francisco" for company in data)
        assert all(company["sector"] == "B2B Software" for company in data)
        company_names = [company["name"] for company in data]
        assert "Tech Startup Inc." in company_names
        assert "Tech Solutions SF" in company_names
