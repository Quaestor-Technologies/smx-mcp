from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Any, Self, final

import aiohttp

if TYPE_CHECKING:
    from types import TracebackType

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

type _Json = dict[str, _Json | list[_Json] | str | int | float | bool | None]

_BASE_URL = "https://api.standardmetrics.com"


@final
class StandardMetrics:
    """Client for interacting with the Standard Metrics REST API."""

    _session: aiohttp.ClientSession | None = None

    def __init__(
        self,
        api_key: str,
        *,
        timeout: float = 10.0,
        base_url: str = _BASE_URL,
    ) -> None:
        """Initialize the StandardMetrics client.

        Args:
            api_key: The API key to use for the client.
            timeout: The timeout to use for the client.
            base_url: The base URL to use for the client.
        """
        self.api_key = api_key
        self.timeout = timeout
        self.base_url = base_url

    async def __aenter__(self) -> Self:
        self._session = aiohttp.ClientSession(
            base_url=self.base_url,
            timeout=aiohttp.ClientTimeout(total=self.timeout),
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if self._session is not None:
            await self._session.close()

    async def request(
        self,
        method: str,
        endpoint: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> _Json:
        """Make a request to the Standard Metrics API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint (without leading slash)
            params: Query parameters
            json: JSON data to send in request body
            data: Form data to send in request body

        Returns:
            JSON response from the API

        Raises:
            RuntimeError: If the client is not properly initialized
            aiohttp.ClientError: If the request fails
        """
        if self._session is None:
            raise RuntimeError("Client must be used as an async context manager")

        response = await self._session.request(
            method=method.upper(),
            url=endpoint,
            params=params,
            json=json,
            data=data,
        )
        response.raise_for_status()
        return await response.json()

    async def list_companies(
        self,
        *,
        page: int = 1,
        page_size: int = 100,
    ) -> PaginatedCompanies:
        """List all companies associated with your firm."""
        params: dict[str, Any] = {"page": page, "page_size": page_size}
        response = await self.request("GET", "v1/companies/", params=params)
        return PaginatedCompanies.model_validate(response)

    async def get_company(self, company_id: str) -> Company:
        """Get a specific company by ID."""
        response = await self.request("GET", f"v1/companies/{company_id}/")
        return Company.model_validate(response)

    async def search_companies(
        self,
        *,
        name_contains: str | None = None,
        sector: str | None = None,
        city: str | None = None,
        page: int = 1,
        page_size: int = 100,
    ) -> PaginatedCompanies:
        """Search companies by various criteria."""
        params: dict[str, Any] = {"page": page, "page_size": page_size}
        if name_contains:
            params["name_contains"] = name_contains
        if sector:
            params["sector"] = sector
        if city:
            params["city"] = city
        response = await self.request("GET", "v1/companies/", params=params)
        return PaginatedCompanies.model_validate(response)

    async def get_company_metrics(
        self,
        company_id: str,
        *,
        from_date: str | None = None,
        to_date: str | None = None,
        category: str | None = None,
        cadence: str | None = None,
        include_budgets: bool = False,
        page: int = 1,
        page_size: int = 100,
    ) -> PaginatedMetricData:
        """Get metrics for a specific company."""
        params: dict[str, Any] = {
            "company_id": company_id,
            "page": page,
            "page_size": page_size,
        }

        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if category:
            params["category"] = category
        if cadence:
            params["cadence"] = cadence
        if include_budgets:
            params["include_budgets"] = "1"

        response = await self.request("GET", "v1/metrics/", params=params)
        return PaginatedMetricData.model_validate(response)

    async def get_metrics_options(
        self,
        *,
        category_name: str | None = None,
        is_standard: bool | None = None,
        page: int = 1,
        page_size: int = 100,
    ) -> PaginatedMetricOptions:
        """Get available metric categories and options."""
        params: dict[str, Any] = {"page": page, "page_size": page_size}
        if category_name:
            params["category_name"] = category_name
        if is_standard is not None:
            params["is_standard"] = is_standard
        response = await self.request("GET", "v1/metrics/options/", params=params)
        return PaginatedMetricOptions.model_validate(response)

    async def list_budgets(
        self,
        *,
        company_slug: str | None = None,
        company_id: str | None = None,
        page: int = 1,
        page_size: int = 100,
    ) -> PaginatedBudgets:
        """List all budgets associated with your firm."""
        params: dict[str, Any] = {"page": page, "page_size": page_size}
        if company_slug:
            params["company_slug"] = company_slug
        if company_id:
            params["company_id"] = company_id
        response = await self.request("GET", "v1/budgets/", params=params)
        return PaginatedBudgets.model_validate(response)

    async def get_custom_columns(
        self,
        *,
        company_slug: str | None = None,
        company_id: str | None = None,
        page: int = 1,
        page_size: int = 100,
    ) -> PaginatedCustomColumns:
        """Get custom column data for companies."""
        params: dict[str, Any] = {"page": page, "page_size": page_size}
        if company_slug:
            params["company_slug"] = company_slug
        if company_id:
            params["company_id"] = company_id
        response = await self.request("GET", "v1/custom-columns/", params=params)
        return PaginatedCustomColumns.model_validate(response)

    async def get_custom_column_options(
        self,
        *,
        page: int = 1,
        page_size: int = 100,
    ) -> PaginatedCustomColumnOptions:
        """Get all custom columns and their available options."""
        params: dict[str, Any] = {"page": page, "page_size": page_size}
        response = await self.request("GET", "v1/custom-columns/options/", params=params)
        return PaginatedCustomColumnOptions.model_validate(response)

    async def list_documents(
        self,
        *,
        company_id: str | None = None,
        parse_state: str | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        source: str | None = None,
        page: int = 1,
        page_size: int = 100,
    ) -> PaginatedDocuments:
        """List all documents associated with your firm."""
        params: dict[str, Any] = {"page": page, "page_size": page_size}
        if company_id:
            params["company_id"] = company_id
        if parse_state:
            params["parse_state"] = parse_state
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if source:
            params["source"] = source
        response = await self.request("GET", "v1/documents/", params=params)
        return PaginatedDocuments.model_validate(response)

    async def list_funds(
        self,
        *,
        page: int = 1,
        page_size: int = 100,
    ) -> PaginatedFunds:
        """List all funds associated with the firm."""
        params: dict[str, Any] = {"page": page, "page_size": page_size}
        response = await self.request("GET", "v1/funds/", params=params)
        return PaginatedFunds.model_validate(response)

    async def list_information_requests(
        self,
        *,
        name: str | None = None,
        page: int = 1,
        page_size: int = 100,
    ) -> PaginatedInformationRequests:
        """List all information requests associated with the firm."""
        params: dict[str, Any] = {"page": page, "page_size": page_size}
        if name:
            params["name"] = name
        response = await self.request("GET", "v1/information-requests/", params=params)
        return PaginatedInformationRequests.model_validate(response)

    async def list_information_reports(
        self,
        *,
        company_id: str | None = None,
        information_request_id: str | None = None,
        page: int = 1,
        page_size: int = 100,
    ) -> PaginatedInformationReports:
        """List all information reports associated with the firm."""
        params: dict[str, Any] = {"page": page, "page_size": page_size}
        if company_id:
            params["company_id"] = company_id
        if information_request_id:
            params["information_request_id"] = information_request_id
        response = await self.request("GET", "v1/information-reports/", params=params)
        return PaginatedInformationReports.model_validate(response)

    async def list_notes(
        self,
        *,
        company_slug: str | None = None,
        company_id: str | None = None,
        sort_by: str | None = None,
        page: int = 1,
        page_size: int = 100,
    ) -> PaginatedNotes:
        """List all notes associated with a specific company."""
        params: dict[str, Any] = {"page": page, "page_size": page_size}
        if company_slug:
            params["company_slug"] = company_slug
        if company_id:
            params["company_id"] = company_id
        if sort_by:
            params["sort_by"] = sort_by
        response = await self.request("GET", "v1/notes/", params=params)
        return PaginatedNotes.model_validate(response)

    async def list_users(
        self,
        *,
        email: str | None = None,
        page: int = 1,
        page_size: int = 100,
    ) -> PaginatedUsers:
        """List all users associated with your firm."""
        params: dict[str, Any] = {"page": page, "page_size": page_size}
        if email:
            params["email"] = email
        response = await self.request("GET", "v1/users/", params=params)
        return PaginatedUsers.model_validate(response)

    async def get_portfolio_summary(self) -> PortfolioSummary:
        """Get a comprehensive portfolio summary including companies, funds, and key metrics."""
        companies = await self.list_companies(page_size=1000)
        funds = await self.list_funds(page_size=1000)

        portfolio_metrics: dict[str, Any] = {}
        company_results = companies.results[:10]  # Limit to first 10

        for company in company_results:
            try:
                if company.id:
                    metrics = await self.get_company_metrics(company.id, page_size=50)
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

    async def get_company_performance(
        self,
        company_id: str,
        *,
        months: int = 12,
    ) -> CompanyPerformance:
        """Get comprehensive performance data for a specific company."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months * 30)

        company = await self.get_company(company_id)
        metrics = await self.get_company_metrics(
            company_id,
            from_date=start_date.strftime("%Y-%m-%d"),
            to_date=end_date.strftime("%Y-%m-%d"),
        )
        budgets = await self.list_budgets(company_id=company_id)
        notes = await self.list_notes(company_id=company_id)
        custom_columns = await self.get_custom_columns(company_id=company_id)

        return CompanyPerformance(
            company=company,
            metrics=metrics.results,
            budgets=budgets.results,
            notes=notes.results,
            custom_columns=custom_columns.results,
            performance_period=f"{months} months",
            date_range={
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d"),
            },
        )

    async def get_company_financial_summary(
        self,
        company_id: str,
        *,
        months: int = 12,
    ) -> FinancialSummary:
        """Get a financial summary for a company including key metrics over time."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=months * 30)

        company = await self.get_company(company_id)
        metrics = await self.get_company_metrics(
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
            date_range={
                "start": start_date.strftime("%Y-%m-%d"),
                "end": end_date.strftime("%Y-%m-%d"),
            },
        )
