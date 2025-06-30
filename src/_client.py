from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, Self, final

import aiohttp

from src import version

from ._auth import get_auth_headers
from ._settings import settings
from ._types import (
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
)

if TYPE_CHECKING:
    import datetime as dt
    from types import TracebackType


type HttpMethod = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]
type _Json = dict[str, _Json | list[_Json] | str | int | float | bool | None]


@final
class StandardMetrics:
    """Client for interacting with the Standard Metrics REST API using OAuth2."""

    _session: aiohttp.ClientSession | None = None

    def __init__(
        self,
        *,
        timeout: float | None = None,
        base_url: str | None = None,
    ) -> None:
        """Initialize the StandardMetrics client.

        Args:
            timeout: The timeout to use for the client. If None, will use settings.
            base_url: The base URL to use for the client. If None, will use settings.
        """
        self.timeout = timeout or settings.request_timeout
        self.base_url = base_url or settings.smx_base_url

        if not settings.smx_client_id or not settings.smx_client_secret:
            raise ValueError(
                "OAuth2 credentials required: SMX_CLIENT_ID and SMX_CLIENT_SECRET "
                "environment variables must be set"
            )

    async def __aenter__(self) -> Self:
        self._session = aiohttp.ClientSession(
            base_url=self.base_url,
            timeout=aiohttp.ClientTimeout(total=self.timeout),
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

    async def _request(
        self,
        method: HttpMethod,
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

        auth_headers = await get_auth_headers()
        user_agent = f"smx-mcp/{version.__version__}"
        headers = {**auth_headers, "User-Agent": user_agent}
        response = await self._session.request(
            method=method.upper(),
            url=endpoint,
            params=params,
            json=json,
            data=data,
            headers=headers,
        )
        response.raise_for_status()
        return await response.json()

    async def get_companies(
        self,
        *,
        page: int = 1,
        page_size: int = 100,
    ) -> PaginatedCompanies:
        """Get all companies associated with your firm."""
        params: dict[str, Any] = {"page": page, "page_size": page_size}
        response = await self._request("GET", "v1/companies/", params=params)
        return PaginatedCompanies.model_validate(response)

    async def get_company_metrics(
        self,
        company_id: str,
        *,
        from_date: dt.date | None = None,
        to_date: dt.date | None = None,
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
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date:
            params["to"] = to_date.strftime("%Y-%m-%d")
        if category:
            params["category"] = category
        if cadence:
            params["cadence"] = cadence
        if include_budgets:
            params["include_budgets"] = "1"

        response = await self._request("GET", "v1/metrics/", params=params)
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
        response = await self._request("GET", "v1/metrics/options/", params=params)
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
        response = await self._request("GET", "v1/budgets/", params=params)
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
        response = await self._request("GET", "v1/custom-columns/", params=params)
        return PaginatedCustomColumns.model_validate(response)

    async def get_custom_column_options(
        self,
        *,
        page: int = 1,
        page_size: int = 100,
    ) -> PaginatedCustomColumnOptions:
        """Get all custom columns and their available options."""
        params: dict[str, Any] = {"page": page, "page_size": page_size}
        response = await self._request("GET", "v1/custom-columns/options/", params=params)
        return PaginatedCustomColumnOptions.model_validate(response)

    async def list_documents(
        self,
        *,
        company_id: str | None = None,
        parse_state: str | None = None,
        from_date: dt.date | None = None,
        to_date: dt.date | None = None,
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
            params["from"] = from_date.strftime("%Y-%m-%d")
        if to_date:
            params["to"] = to_date.strftime("%Y-%m-%d")
        if source:
            params["source"] = source
        response = await self._request("GET", "v1/documents/", params=params)
        return PaginatedDocuments.model_validate(response)

    async def list_funds(
        self,
        *,
        page: int = 1,
        page_size: int = 100,
    ) -> PaginatedFunds:
        """List all funds associated with the firm."""
        params: dict[str, Any] = {"page": page, "page_size": page_size}
        response = await self._request("GET", "v1/funds/", params=params)
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
        response = await self._request("GET", "v1/information-requests/", params=params)
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
        response = await self._request("GET", "v1/information-reports/", params=params)
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
        response = await self._request("GET", "v1/notes/", params=params)
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
        response = await self._request("GET", "v1/users/", params=params)
        return PaginatedUsers.model_validate(response)
