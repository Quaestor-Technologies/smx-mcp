import asyncio
import datetime as dt
from datetime import datetime, timedelta
from typing import Any

from ._client import StandardMetrics
from ._types import (
    Company,
    CompanyPerformance,
    CompanySector,
    DateRange,
    DocumentParseState,
    DocumentSource,
    FinancialSummary,
    MetricCadence,
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
from .server import mcp

_CONCURRENT_REQUEST_LIMIT = 10


async def _get_company(standard_metrics: StandardMetrics, company_id: str) -> Company:
    page = 1
    # TODO: Add filtering on company id to to our public companies endpoint.
    while companies := await standard_metrics.get_companies(page=page, page_size=100):
        for company in companies.results:
            if company.id == company_id:
                return company
        page += 1
    raise ValueError(f"Company with ID {company_id} not found")


@mcp.tool
async def list_companies(
    page: int = 1,
    per_page: int = 100,
) -> PaginatedCompanies:
    """List all companies associated with your firm.

    Args:
        page: Page number for pagination (default: 1)
        per_page: Results per page (default: 100, max: 100)
    """
    async with StandardMetrics() as client:
        return await client.get_companies(page=page, page_size=per_page)


@mcp.tool
async def get_company(company_id: str) -> Company:
    """Get a specific company by ID.

    Args:
        company_id: The unique identifier for the company
    """
    async with StandardMetrics() as client:
        return await _get_company(client, company_id)


@mcp.tool
async def search_companies(
    name_contains: str | None = None,
    sector: CompanySector | None = None,
    city: str | None = None,
    page: int = 1,
    per_page: int = 100,
) -> list[Company]:
    """Search companies by various criteria.

    Args:
        name_contains: Filter companies containing this text in their name
        sector: Filter companies by sector
        city: Filter companies by city
        page: Page number for pagination (default: 1)
        per_page: Results per page (default: 100, max: 100)
    """
    async with StandardMetrics() as client:
        results = (await client.get_companies(page=page, page_size=per_page)).results
        if sector:
            results = [c for c in results if c.sector == sector]
        if city:
            results = [c for c in results if c.city == city]
        if name_contains:
            results = [c for c in results if name_contains.lower() in c.name.lower()]
        return results


@mcp.tool
async def get_company_metrics(
    company_id: str,
    from_date: dt.date | None = None,
    to_date: dt.date | None = None,
    category: str | None = None,
    cadence: MetricCadence | None = None,
    include_budgets: bool = False,
    page: int = 1,
    per_page: int = 100,
) -> PaginatedMetricData:
    """Get metrics for a specific company.

    Args:
        company_id: The unique identifier for the company
        from_date: Start date for metrics (inclusive)
        to_date: End date for metrics (inclusive)
        category: Filter by metric category
        cadence: Filter by metric cadence (daily, monthly, etc.)
        include_budgets: Include budget metrics in results
        page: Page number for pagination (default: 1)
        per_page: Results per page (default: 100, max: 100)
    """
    async with StandardMetrics() as client:
        return await client.get_company_metrics(
            company_id,
            from_date=from_date,
            to_date=to_date,
            category=category,
            cadence=cadence,
            include_budgets=include_budgets,
            page=page,
            page_size=per_page,
        )


@mcp.tool
async def get_metrics_options(
    category_name: str | None = None,
    is_standard: bool | None = None,
    page: int = 1,
    per_page: int = 100,
) -> PaginatedMetricOptions:
    """Get available metric categories and options.

    Args:
        category_name: Filter by specific category name
        is_standard: Filter by standard vs custom metrics
        page: Page number for pagination (default: 1)
        per_page: Results per page (default: 100, max: 100)
    """
    async with StandardMetrics() as client:
        return await client.get_metrics_options(
            category_name=category_name,
            is_standard=is_standard,
            page=page,
            page_size=per_page,
        )


@mcp.tool
async def list_budgets(
    company_slug: str | None = None,
    company_id: str | None = None,
    page: int = 1,
    per_page: int = 100,
) -> PaginatedBudgets:
    """List all budgets associated with your firm.

    Args:
        company_slug: Filter by company slug
        company_id: Filter by company ID
        page: Page number for pagination (default: 1)
        per_page: Results per page (default: 100, max: 100)
    """
    async with StandardMetrics() as client:
        return await client.list_budgets(
            company_slug=company_slug,
            company_id=company_id,
            page=page,
            page_size=per_page,
        )


@mcp.tool
async def get_custom_columns(
    company_slug: str | None = None,
    company_id: str | None = None,
    page: int = 1,
    per_page: int = 100,
) -> PaginatedCustomColumns:
    """Get custom column data for companies.

    Args:
        company_slug: Filter by company slug
        company_id: Filter by company ID
        page: Page number for pagination (default: 1)
        per_page: Results per page (default: 30, max: 100)
    """
    async with StandardMetrics() as client:
        return await client.get_custom_columns(
            company_slug=company_slug,
            company_id=company_id,
            page=page,
            page_size=per_page,
        )


@mcp.tool
async def get_custom_column_options(
    page: int = 1,
    per_page: int = 100,
) -> PaginatedCustomColumnOptions:
    """Get all custom columns and their available options.

    Args:
        page: Page number for pagination (default: 1)
        per_page: Results per page (default: 100, max: 100)
    """
    async with StandardMetrics() as client:
        return await client.get_custom_column_options(page=page, page_size=per_page)


@mcp.tool
async def list_documents(
    company_id: str | None = None,
    parse_state: DocumentParseState | None = None,
    from_date: dt.date | None = None,
    to_date: dt.date | None = None,
    source: DocumentSource | None = None,
    page: int = 1,
    per_page: int = 100,
) -> PaginatedDocuments:
    """List all documents associated with your firm.

    Args:
        company_id: Filter by company ID
        parse_state: Filter by document parse state
        from_date: Start date filter (inclusive)
        to_date: End date filter (inclusive)
        source: Filter by document source
        page: Page number for pagination (default: 1)
        per_page: Results per page (default: 100, max: 100)
    """
    async with StandardMetrics() as client:
        return await client.list_documents(
            company_id=company_id,
            parse_state=parse_state,
            from_date=from_date,
            to_date=to_date,
            source=source,
            page=page,
            page_size=per_page,
        )


@mcp.tool
async def list_funds(
    page: int = 1,
    per_page: int = 100,
) -> PaginatedFunds:
    """List all funds associated with the firm.

    Args:
        page: Page number for pagination (default: 1)
        per_page: Results per page (default: 100, max: 100)
    """
    async with StandardMetrics() as client:
        return await client.list_funds(page=page, page_size=per_page)


@mcp.tool
async def list_information_requests(
    name: str | None = None,
    page: int = 1,
    per_page: int = 100,
) -> PaginatedInformationRequests:
    """List all information requests associated with the firm.

    Args:
        name: Filter by request name
        page: Page number for pagination (default: 1)
        per_page: Results per page (default: 100, max: 100)
    """
    async with StandardMetrics() as client:
        return await client.list_information_requests(name=name, page=page, page_size=per_page)


@mcp.tool
async def list_information_reports(
    company_id: str | None = None,
    information_request_id: str | None = None,
    page: int = 1,
    per_page: int = 100,
) -> PaginatedInformationReports:
    """List all information reports associated with the firm.

    Args:
        company_id: Filter by company ID
        information_request_id: Filter by information request ID
        page: Page number for pagination (default: 1)
        per_page: Results per page (default: 100, max: 100)
    """
    async with StandardMetrics() as client:
        return await client.list_information_reports(
            company_id=company_id,
            information_request_id=information_request_id,
            page=page,
            page_size=per_page,
        )


@mcp.tool
async def list_notes(
    company_slug: str | None = None,
    company_id: str | None = None,
    sort_by: str | None = None,
    page: int = 1,
    per_page: int = 100,
) -> PaginatedNotes:
    """List all notes associated with a specific company.

    Args:
        company_slug: Filter by company slug
        company_id: Filter by company ID
        sort_by: Sort notes by specific field
        page: Page number for pagination (default: 1)
        per_page: Results per page (default: 100, max: 100)
    """
    async with StandardMetrics() as client:
        return await client.list_notes(
            company_slug=company_slug,
            company_id=company_id,
            sort_by=sort_by,
            page=page,
            page_size=per_page,
        )


@mcp.tool
async def list_users(
    email: str | None = None,
    page: int = 1,
    per_page: int = 100,
) -> PaginatedUsers:
    """List all users associated with your firm.

    Args:
        email: Filter by user email
        page: Page number for pagination (default: 1)
        per_page: Results per page (default: 100, max: 100)
    """
    async with StandardMetrics() as client:
        return await client.list_users(email=email, page=page, page_size=per_page)


async def _fetch_company_metrics_batch(
    companies: list[Company], client: StandardMetrics, metrics_per_company: int
) -> list[PaginatedMetricData | BaseException]:
    """Fetch metrics for multiple companies concurrently with rate limiting."""
    semaphore = asyncio.Semaphore(_CONCURRENT_REQUEST_LIMIT)

    async def fetch_with_rate_limit(company: Company) -> PaginatedMetricData:
        async with semaphore:
            return await client.get_company_metrics(company.id, page_size=metrics_per_company)

    return await asyncio.gather(
        *[fetch_with_rate_limit(company) for company in companies],
        return_exceptions=True,
    )


async def _build_portfolio_metrics(
    companies: list[Company],
    client: StandardMetrics,
    include_metrics: bool,
    metrics_per_company: int,
) -> dict[str, Any]:
    """Build portfolio metrics dictionary for all companies."""
    if not include_metrics:
        return {
            company.name: {
                "company_info": company.model_dump(),
                "recent_metrics": [],
            }
            for company in companies
        }

    metrics_results = await _fetch_company_metrics_batch(companies, client, metrics_per_company)

    portfolio_metrics: dict[str, Any] = {}
    for company, result in zip(companies, metrics_results, strict=True):
        if isinstance(result, BaseException):
            portfolio_metrics[company.name] = {
                "company_info": company.model_dump(),
                "error": str(result),
            }
        else:
            portfolio_metrics[company.name] = {
                "company_info": company.model_dump(),
                "recent_metrics": [m.model_dump() for m in result.results],
            }

    return portfolio_metrics


@mcp.tool
async def get_portfolio_summary(
    company_ids: list[str] | None = None,
    max_companies: int | None = None,
    include_metrics: bool = True,
    metrics_per_company: int = 50,
) -> PortfolioSummary:
    """Get a comprehensive portfolio summary including companies, funds, and key metrics.

    Args:
        company_ids: Specific company IDs to include (if None, includes all companies)
        max_companies: Maximum number of companies to include metrics for (if None, includes all)
        include_metrics: Whether to fetch metrics for each company (default: True)
        metrics_per_company: Number of recent metrics to fetch per company (default: 50) (up to 100)
    """

    async with StandardMetrics() as client:
        # TODO: Add filtering to this endpoint so actually get **all** the companies we want.
        companies = await client.get_companies(page_size=100)
        funds = await client.list_funds(page_size=100)

        if company_ids:
            company_results = [c for c in companies.results if c.id in company_ids]
        else:
            company_results = companies.results

        if max_companies:
            company_results = company_results[:max_companies]

        portfolio_metrics = await _build_portfolio_metrics(
            company_results, client, include_metrics, metrics_per_company
        )
        return PortfolioSummary(
            total_companies=len(company_results),
            total_funds=len(funds.results),
            companies=company_results,
            funds=funds.results,
            portfolio_metrics=portfolio_metrics,
        )


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
    async with StandardMetrics() as client:
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=months * 30)

        company = await _get_company(client, company_id)
        results = await asyncio.gather(
            client.get_company_metrics(
                company_id,
                from_date=start_date,
                to_date=end_date,
            ),
            client.list_budgets(company_id=company_id),
            client.list_notes(company_id=company_id),
            client.get_custom_columns(company_id=company_id),
        )
        metrics, budgets, notes, custom_columns = results

        return CompanyPerformance(
            company=company,
            metrics=metrics.results,
            budgets=budgets.results,
            notes=notes.results,
            custom_columns=custom_columns.results,
            performance_period=f"{months} months",
            date_range=DateRange(start=start_date, end=end_date),
        )


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
    async with StandardMetrics() as client:
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=months * 30)
        companies, metrics = await asyncio.gather(
            client.get_companies(),
            client.get_company_metrics(
                company_id,
                from_date=start_date,
                to_date=end_date,
            ),
        )

        for company in companies.results:
            if company.id == company_id:
                break
        else:
            raise ValueError(f"Company with ID {company_id} not found")

        metrics_results = metrics.results

        metrics_by_category: dict[str, list[MetricData]] = {}
        for metric in metrics_results:
            category = metric.category or "unknown"
            if category not in metrics_by_category:
                metrics_by_category[category] = []
            metrics_by_category[category].append(metric)

        latest_metrics: dict[str, MetricData] = {}
        for category, category_metrics in metrics_by_category.items():
            if category_metrics:
                sorted_metrics = sorted(category_metrics, key=lambda x: x.date, reverse=True)
                latest_metrics[category] = sorted_metrics[0]

        return FinancialSummary(
            company=company,
            period=f"{months} months",
            total_metrics=len(metrics_results),
            metrics_by_category={k: len(v) for k, v in metrics_by_category.items()},
            latest_metrics=latest_metrics,
            date_range=DateRange(start=start_date, end=end_date),
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
    async with StandardMetrics() as client:
        metrics = await client.get_company_metrics(company_id, category=category, page_size=limit)
        return sorted(metrics.results, key=lambda x: x.date, reverse=True)


@mcp.tool
async def get_company_notes_summary(company_id: str, recent_notes_limit: int = 5) -> dict[str, Any]:
    """Get a summary of notes for a company.

    Args:
        company_id: The unique identifier for the company
        recent_notes_limit: The number of recent notes to return.
            Max 100.
    """
    if recent_notes_limit > 100:
        raise ValueError("recent_notes_limit must be less than 100")

    async with StandardMetrics() as client:
        notes = await client.list_notes(company_id=company_id, page_size=100)
        return {
            "total_notes": len(notes.results),
            "recent_notes": sorted(notes.results, key=lambda x: x.created_at or "", reverse=True)[
                :recent_notes_limit
            ],
            "authors": list({note.author for note in notes.results if note.author}),
        }
