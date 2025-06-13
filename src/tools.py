from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any

from src.server import mcp

from ._client import StandardMetrics

if TYPE_CHECKING:
    from ._types import (
        Company,
        CompanyPerformance,
        FinancialSummary,
        MetricData,
        PaginatedBudgets,
        PaginatedCompanies,
        PaginatedCustomColumnOptions,
        PaginatedCustomColumns,
        PaginatedDocuments,
        PaginatedFunds,
        PaginatedInformationReports,
        PaginatedInformationRequests,
        PaginatedMetricData,
        PaginatedMetricOptions,
        PaginatedNotes,
        PaginatedUsers,
        PortfolioSummary,
    )


def _get_api_key() -> str:
    """Get API key from environment variable."""
    api_key = os.getenv("STANDARD_METRICS_API_KEY")
    if not api_key:
        raise ValueError("STANDARD_METRICS_API_KEY environment variable must be set")
    return api_key


@mcp.tool
async def list_companies(
    page: int = 1,
    page_size: int = 100,
) -> PaginatedCompanies:
    """List all companies associated with your firm.

    Args:
        page: Page number for pagination
        page_size: Number of companies per page
    """
    async with StandardMetrics(_get_api_key()) as client:
        return await client.list_companies(page=page, page_size=page_size)


@mcp.tool
async def get_company(company_id: str) -> Company:
    """Get a specific company by ID.

    Args:
        company_id: The unique identifier for the company
    """
    async with StandardMetrics(_get_api_key()) as client:
        return await client.get_company(company_id)


@mcp.tool
async def search_companies(
    name_contains: str | None = None,
    sector: str | None = None,
    city: str | None = None,
    page: int = 1,
    page_size: int = 100,
) -> PaginatedCompanies:
    """Search companies by various criteria.

    Args:
        name_contains: Filter companies containing this text in their name
        sector: Filter companies by sector
        city: Filter companies by city
        page: Page number for pagination
        page_size: Number of companies per page
    """
    async with StandardMetrics(_get_api_key()) as client:
        return await client.search_companies(
            name_contains=name_contains,
            sector=sector,
            city=city,
            page=page,
            page_size=page_size,
        )


@mcp.tool
async def get_company_metrics(
    company_id: str,
    from_date: str | None = None,
    to_date: str | None = None,
    category: str | None = None,
    cadence: str | None = None,
    include_budgets: bool = False,
    page: int = 1,
    page_size: int = 100,
) -> PaginatedMetricData:
    """Get metrics for a specific company.

    Args:
        company_id: The unique identifier for the company
        from_date: Start date for metrics (YYYY-MM-DD format)
        to_date: End date for metrics (YYYY-MM-DD format)
        category: Filter by metric category
        cadence: Filter by metric cadence (daily, monthly, etc.)
        include_budgets: Include budget metrics in results
        page: Page number for pagination
        page_size: Number of metrics per page
    """
    async with StandardMetrics(_get_api_key()) as client:
        return await client.get_company_metrics(
            company_id,
            from_date=from_date,
            to_date=to_date,
            category=category,
            cadence=cadence,
            include_budgets=include_budgets,
            page=page,
            page_size=page_size,
        )


@mcp.tool
async def get_metrics_options(
    category_name: str | None = None,
    is_standard: bool | None = None,
    page: int = 1,
    page_size: int = 100,
) -> PaginatedMetricOptions:
    """Get available metric categories and options.

    Args:
        category_name: Filter by specific category name
        is_standard: Filter by standard vs custom metrics
        page: Page number for pagination
        page_size: Number of options per page
    """
    async with StandardMetrics(_get_api_key()) as client:
        return await client.get_metrics_options(
            category_name=category_name,
            is_standard=is_standard,
            page=page,
            page_size=page_size,
        )


@mcp.tool
async def list_budgets(
    company_slug: str | None = None,
    company_id: str | None = None,
    page: int = 1,
    page_size: int = 100,
) -> PaginatedBudgets:
    """List all budgets associated with your firm.

    Args:
        company_slug: Filter by company slug
        company_id: Filter by company ID
        page: Page number for pagination
        page_size: Number of budgets per page
    """
    async with StandardMetrics(_get_api_key()) as client:
        return await client.list_budgets(
            company_slug=company_slug,
            company_id=company_id,
            page=page,
            page_size=page_size,
        )


@mcp.tool
async def get_custom_columns(
    company_slug: str | None = None,
    company_id: str | None = None,
    page: int = 1,
    page_size: int = 100,
) -> PaginatedCustomColumns:
    """Get custom column data for companies.

    Args:
        company_slug: Filter by company slug
        company_id: Filter by company ID
        page: Page number for pagination
        page_size: Number of custom columns per page
    """
    async with StandardMetrics(_get_api_key()) as client:
        return await client.get_custom_columns(
            company_slug=company_slug,
            company_id=company_id,
            page=page,
            page_size=page_size,
        )


@mcp.tool
async def get_custom_column_options(
    page: int = 1,
    page_size: int = 100,
) -> PaginatedCustomColumnOptions:
    """Get all custom columns and their available options.

    Args:
        page: Page number for pagination
        page_size: Number of options per page
    """
    async with StandardMetrics(_get_api_key()) as client:
        return await client.get_custom_column_options(page=page, page_size=page_size)


@mcp.tool
async def list_documents(
    company_id: str | None = None,
    parse_state: str | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
    source: str | None = None,
    page: int = 1,
    page_size: int = 100,
) -> PaginatedDocuments:
    """List all documents associated with your firm.

    Args:
        company_id: Filter by company ID
        parse_state: Filter by document parse state
        from_date: Start date filter (YYYY-MM-DD format)
        to_date: End date filter (YYYY-MM-DD format)
        source: Filter by document source
        page: Page number for pagination
        page_size: Number of documents per page
    """
    async with StandardMetrics(_get_api_key()) as client:
        return await client.list_documents(
            company_id=company_id,
            parse_state=parse_state,
            from_date=from_date,
            to_date=to_date,
            source=source,
            page=page,
            page_size=page_size,
        )


@mcp.tool
async def list_funds(
    page: int = 1,
    page_size: int = 100,
) -> PaginatedFunds:
    """List all funds associated with the firm.

    Args:
        page: Page number for pagination
        page_size: Number of funds per page
    """
    async with StandardMetrics(_get_api_key()) as client:
        return await client.list_funds(page=page, page_size=page_size)


@mcp.tool
async def list_information_requests(
    name: str | None = None,
    page: int = 1,
    page_size: int = 100,
) -> PaginatedInformationRequests:
    """List all information requests associated with the firm.

    Args:
        name: Filter by request name
        page: Page number for pagination
        page_size: Number of requests per page
    """
    async with StandardMetrics(_get_api_key()) as client:
        return await client.list_information_requests(name=name, page=page, page_size=page_size)


@mcp.tool
async def list_information_reports(
    company_id: str | None = None,
    information_request_id: str | None = None,
    page: int = 1,
    page_size: int = 100,
) -> PaginatedInformationReports:
    """List all information reports associated with the firm.

    Args:
        company_id: Filter by company ID
        information_request_id: Filter by information request ID
        page: Page number for pagination
        page_size: Number of reports per page
    """
    async with StandardMetrics(_get_api_key()) as client:
        return await client.list_information_reports(
            company_id=company_id,
            information_request_id=information_request_id,
            page=page,
            page_size=page_size,
        )


@mcp.tool
async def list_notes(
    company_slug: str | None = None,
    company_id: str | None = None,
    sort_by: str | None = None,
    page: int = 1,
    page_size: int = 100,
) -> PaginatedNotes:
    """List all notes associated with a specific company.

    Args:
        company_slug: Filter by company slug
        company_id: Filter by company ID
        sort_by: Sort notes by specific field
        page: Page number for pagination
        page_size: Number of notes per page
    """
    async with StandardMetrics(_get_api_key()) as client:
        return await client.list_notes(
            company_slug=company_slug,
            company_id=company_id,
            sort_by=sort_by,
            page=page,
            page_size=page_size,
        )


@mcp.tool
async def list_users(
    email: str | None = None,
    page: int = 1,
    page_size: int = 100,
) -> PaginatedUsers:
    """List all users associated with your firm.

    Args:
        email: Filter by user email
        page: Page number for pagination
        page_size: Number of users per page
    """
    async with StandardMetrics(_get_api_key()) as client:
        return await client.list_users(email=email, page=page, page_size=page_size)


@mcp.tool
async def get_portfolio_summary() -> PortfolioSummary:
    """Get a comprehensive portfolio summary including companies, funds, and key metrics."""
    async with StandardMetrics(_get_api_key()) as client:
        return await client.get_portfolio_summary()


@mcp.tool
async def get_company_performance(
    company_id: str,
    months: int = 12,
) -> CompanyPerformance:
    """Get comprehensive performance data for a specific company.

    Args:
        company_id: The unique identifier for the company
        months: Number of months of historical data to include
    """
    async with StandardMetrics(_get_api_key()) as client:
        return await client.get_company_performance(company_id, months=months)


@mcp.tool
async def get_company_financial_summary(
    company_id: str,
    months: int = 12,
) -> FinancialSummary:
    """Get a financial summary for a company including key metrics over time.

    Args:
        company_id: The unique identifier for the company
        months: Number of months of historical data to include
    """
    async with StandardMetrics(_get_api_key()) as client:
        return await client.get_company_financial_summary(company_id, months=months)


@mcp.tool
async def find_company_by_name(name: str) -> Company | None:
    """Find a company by name (case-insensitive search).

    Args:
        name: The company name to search for
    """
    async with StandardMetrics(_get_api_key()) as client:
        companies = await client.search_companies(name_contains=name, page_size=1000)
        return next(
            (company for company in companies.results if company.name.lower() == name.lower()),
            None,
        )


@mcp.tool
async def get_company_recent_metrics(
    company_id: str,
    category: str | None = None,
    limit: int = 10,
) -> list[MetricData]:
    """Get the most recent metrics for a company.

    Args:
        company_id: The unique identifier for the company
        category: Filter by specific metric category
        limit: Maximum number of recent metrics to return
    """
    async with StandardMetrics(_get_api_key()) as client:
        metrics = await client.get_company_metrics(company_id, category=category, page_size=limit)
        return sorted(metrics.results, key=lambda x: x.date, reverse=True)


@mcp.tool
async def get_companies_by_sector(sector: str) -> list[Company]:
    """Get all companies in a specific sector.

    Args:
        sector: The sector to filter companies by
    """
    async with StandardMetrics(_get_api_key()) as client:
        companies = await client.search_companies(sector=sector, page_size=1000)
        return companies.results


@mcp.tool
async def get_company_notes_summary(company_id: str) -> dict[str, Any]:
    """Get a summary of notes for a company.

    Args:
        company_id: The unique identifier for the company
    """
    async with StandardMetrics(_get_api_key()) as client:
        notes = await client.list_notes(company_id=company_id, page_size=1000)
        return {
            "total_notes": len(notes.results),
            "recent_notes": sorted(notes.results, key=lambda x: x.created_at or "", reverse=True)[
                :5
            ],
            "authors": list({note.author for note in notes.results if note.author}),
        }
