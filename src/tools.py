from datetime import datetime, timedelta
from typing import Any

from ._client import StandardMetrics
from ._types import (
    Company,
    CompanyPerformance,
    DateRange,
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
from .server import mcp


async def _get_company(standard_metrics: StandardMetrics, company_id: str) -> Company:
    page = 1
    # TODO: Add filtering on compaony id to to our public companies endpoint.
    while companies := await standard_metrics.list_companies(page=page, page_size=100):
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
        return await client.list_companies(page=page, page_size=per_page)


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
    sector: str | None = None,
    city: str | None = None,
    page: int = 1,
    per_page: int = 30,
) -> PaginatedCompanies:
    """Search companies by various criteria.

    Args:
        name_contains: Filter companies containing this text in their name
        sector: Filter companies by sector
        city: Filter companies by city
        page: Page number for pagination (default: 1)
        per_page: Results per page (default: 100, max: 100)
    """
    async with StandardMetrics() as client:
        return await client.search_companies(
            name_contains=name_contains,
            sector=sector,
            city=city,
            page=page,
            page_size=per_page,
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
    per_page: int = 100,
) -> PaginatedMetricData:
    """Get metrics for a specific company.

    Args:
        company_id: The unique identifier for the company
        from_date: Start date for metrics (YYYY-MM-DD format)
        to_date: End date for metrics (YYYY-MM-DD format)
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
        per_page: Results per page (defau       lt: 100, max: 100)
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
    per_page: int = 30,
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
    parse_state: str | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
    source: str | None = None,
    page: int = 1,
    per_page: int = 30,
) -> PaginatedDocuments:
    """List all documents associated with your firm.

    Args:
        company_id: Filter by company ID
        parse_state: Filter by document parse state
        from_date: Start date filter (YYYY-MM-DD format)
        to_date: End date filter (YYYY-MM-DD format)
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
    per_page: int = 30,
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
    per_page: int = 30,
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
    per_page: int = 30,
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
    per_page: int = 30,
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
    per_page: int = 30,
) -> PaginatedUsers:
    """List all users associated with your firm.

    Args:
        email: Filter by user email
        page: Page number for pagination (default: 1)
        per_page: Results per page (default: 100, max: 100)
    """
    async with StandardMetrics() as client:
        return await client.list_users(email=email, page=page, page_size=per_page)


@mcp.tool
async def get_portfolio_summary() -> PortfolioSummary:
    """Get a comprehensive portfolio summary including companies, funds, and key metrics."""
    async with StandardMetrics() as client:
        companies = await client.list_companies(page_size=1000)
        funds = await client.list_funds(page_size=1000)

        portfolio_metrics: dict[str, Any] = {}
        company_results = companies.results[:10]  # Limit to first 10

        for company in company_results:
            try:
                if company.id:
                    metrics = await client.get_company_metrics(company.id, page_size=50)
                    portfolio_metrics[company.name] = {
                        "company_info": company.model_dump(),
                        "recent_metrics": [m.model_dump() for m in metrics.results],
                    }
            except Exception as e:
                portfolio_metrics[company.name] = {
                    "company_info": company.model_dump(),
                    "error": str(e),
                }

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
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months * 30)

        company = await _get_company(client, company_id)
        metrics = await client.get_company_metrics(
            company_id,
            from_date=start_date.strftime("%Y-%m-%d"),
            to_date=end_date.strftime("%Y-%m-%d"),
        )
        budgets = await client.list_budgets(company_id=company_id)
        notes = await client.list_notes(company_id=company_id)
        custom_columns = await client.get_custom_columns(company_id=company_id)

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
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months * 30)

        companies = await client.list_companies()
        for company in companies.results:
            if company.id == company_id:
                break
        else:
            raise ValueError(f"Company with ID {company_id} not found")

        metrics = await client.get_company_metrics(
            company_id,
            from_date=start_date.strftime("%Y-%m-%d"),
            to_date=end_date.strftime("%Y-%m-%d"),
        )
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
async def find_company_by_name(name: str) -> Company | None:
    """Find a company by name (case-insensitive search).

    Args:
        name: The company name to search for
    """
    async with StandardMetrics() as client:
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
    async with StandardMetrics() as client:
        metrics = await client.get_company_metrics(company_id, category=category, page_size=limit)
        return sorted(metrics.results, key=lambda x: x.date, reverse=True)


@mcp.tool
async def get_companies_by_sector(sector: str) -> list[Company]:
    """Get all companies in a specific sector.

    Args:
        sector: The sector to filter companies by
    """
    async with StandardMetrics() as client:
        companies = await client.search_companies(sector=sector, page_size=1000)
        return companies.results


@mcp.tool
async def get_company_notes_summary(company_id: str) -> dict[str, Any]:
    """Get a summary of notes for a company.

    Args:
        company_id: The unique identifier for the company
    """
    async with StandardMetrics() as client:
        notes = await client.list_notes(company_id=company_id, page_size=1000)
        return {
            "total_notes": len(notes.results),
            "recent_notes": sorted(notes.results, key=lambda x: x.created_at or "", reverse=True)[
                :5
            ],
            "authors": list({note.author for note in notes.results if note.author}),
        }
