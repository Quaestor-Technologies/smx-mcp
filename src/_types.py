from __future__ import annotations

import datetime as dt
import enum
from typing import Any

import pydantic


class DocumentParseState(enum.StrEnum):
    NOT_STARTED = "not-started"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    NEEDS_INPUT = "needs-input"
    NOT_PARSEABLE = "not-parseable"


class DocumentSource(enum.StrEnum):
    INFORMATION_REQUEST = "information-request"
    IMPLEMENTATION = "implementation"
    UPLOAD = "upload"


class CompanySector(enum.StrEnum):
    B2B_SOFTWARE = "B2B Software"
    DIRECT_TO_CONSUMER = "Direct-to-consumer"
    CONSUMER_INTERNET_MOBILE = "Consumer Internet/Mobile"
    AR_VR = "AR/VR"
    LIFE_SCIENCES = "Life Sciences"
    HEALTH_TECHNOLOGY = "Health Technology"
    HARDWARE = "Hardware"
    EDTECH = "Edtech"
    MEDIA = "Media"
    FINTECH = "Fintech"
    GOVTECH = "Govtech"
    CRYPTO_BLOCKCHAIN = "Crypto/blockchain"
    OTHER = "Other"
    LOGISTICS = "Logistics"
    INSURTECH = "Insurtech"
    SOFTWARE_INFRASTRUCTURE = "Software Infrastructure"
    SECURITY = "Security"
    ARTIFICIAL_INTELLIGENCE = "Artificial Intelligence"
    AG_TECH = "AG-Tech"
    SUSTAINABILITY = "Sustainability"
    GAMING = "Gaming"


class MetricCategory(enum.StrEnum):
    CUSTOM = "custom"
    CASH_IN_BANK = "cash_in_bank"
    NET_BURN = "net_burn"
    RUNWAY = "runway"
    REVENUE = "revenue"
    GROSS_MARGIN = "gross_margin"
    TOTAL_OPERATING_EXPENSES = "total_operating_expenses"
    NET_INCOME = "net_income"
    COST_OF_GOODS_SOLD = "cost_of_goods_sold"
    GROSS_PROFIT = "gross_profit"
    NET_OPERATING_PROFIT = "net_operating_profit"
    NET_OTHER_INCOME = "net_other_income"
    NET_PROFIT = "net_profit"
    CASH_RECEIPTS = "cash_receipts"
    CASH_PAYMENTS = "cash_payments"
    NET_ASSETS = "net_assets"
    ASSETS = "assets"
    LIABILITIES = "liabilities"
    EQUITY = "equity"
    HEADCOUNT = "headcount"
    EBITDA = "ebitda"


class MetricCadence(enum.StrEnum):
    POINT_IN_TIME = "point_in_time"
    DAY = "day"
    WEEK = "week"
    MONTH = "month"
    QUARTER = "quarter"
    HALF_YEAR = "half_year"
    YEAR = "year"


class Company(pydantic.BaseModel):
    id: str
    name: str
    slug: str | None = None
    description: str | None = None
    city: str | None = None
    sector: CompanySector | None = None
    firm_sector: str | None = None
    fiscal_year_end: str | None = pydantic.Field(
        None,
        description="MM/DD format",
    )
    website: str | None = None
    logo_url: str | None = None
    status: str | None = None
    investment_lead_id: str | None = None
    invested_fund_ids: list[str] | None = None
    unique_ref: str | None = None


class Fund(pydantic.BaseModel):
    id: str
    name: str
    size: str
    vintage: int
    currency: str


class Budget(pydantic.BaseModel):
    id: str
    name: str | None = None
    color: str | None = None
    description: str | None = None
    date: dt.datetime
    company: str
    company_slug: str


class Metric(pydantic.BaseModel):
    value: str
    company_id: str
    category: MetricCategory
    date: str
    metric_cadence: MetricCadence
    currency: str | None = "USD"
    is_budget_metric: str | None = "false"
    budget_id: str | None = None


class MetricData(pydantic.BaseModel):
    value: str | None = None
    currency: str | None = None
    converted_value: str | None = None
    preferred_currency: str | None = None
    date: dt.datetime
    category: str | None = None
    category_type: str | None = None
    category_id: str
    cadence: str | None = None
    is_budget_metric: bool | None = None
    budget_id: str | None = None
    custom_metric: str | None = None
    fx_rate: float | None = None
    detailed_source: str | None = None
    updated_at: dt.datetime
    company_id: str
    deleted_at: str | None = None


class MetricOption(pydantic.BaseModel):
    category_name: str
    category_id: str
    is_standard: bool
    type: str
    is_point_in_time: bool
    is_archived: bool
    description: str = ""
    is_multiple: bool
    choices: list[str] | None = None


class CustomColumn(pydantic.BaseModel):
    id: str
    name: str
    type: str
    value: Any | None = None
    company: dict[str, Any]


class Option(pydantic.BaseModel):
    id: str
    value: str
    color: str


class CustomColumnOption(pydantic.BaseModel):
    id: str
    name: str
    type: str
    options: list[Option] | None = None


class Document(pydantic.BaseModel):
    id: str
    name: str
    link: str
    company_id: str
    parse_state: str
    parsed_at: dt.datetime | None = None
    uploaded_at: dt.datetime
    source: str


class Note(pydantic.BaseModel):
    id: str | None = None
    note: str
    author_id: str
    company_id: str | None = None
    company_slug: str | None = None
    author: str | None = None
    email: str | None = None
    created_at: dt.datetime | None = None


class User(pydantic.BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    role: str | None = None


class InformationRequest(pydantic.BaseModel):
    id: str
    name: str
    description: str | None = None
    due_date: dt.datetime | None = None
    status: str | None = None
    company_ids: list[str] = []


class InformationReport(pydantic.BaseModel):
    id: str
    information_request_id: str
    company_id: str
    status: str
    submitted_at: dt.datetime | None = None
    documents: list[dict[str, str]] = []
    metrics: list[dict[str, str]] = []


class PortfolioSummary(pydantic.BaseModel):
    total_companies: int
    total_funds: int
    companies: list[Company]
    funds: list[Fund]
    portfolio_metrics: dict[str, Any]


class CompanyPerformance(pydantic.BaseModel):
    company: Company
    metrics: list[MetricData]
    budgets: list[Budget]
    notes: list[Note]
    custom_columns: list[CustomColumn]
    performance_period: str
    date_range: DateRange


class DateRange(pydantic.BaseModel):
    start: dt.date
    end: dt.date


class FinancialSummary(pydantic.BaseModel):
    company: Company
    period: str
    total_metrics: int
    metrics_by_category: dict[str, int]
    latest_metrics: dict[str, MetricData]
    date_range: DateRange


class PaginatedResponse[T](pydantic.BaseModel):
    results: list[T]
    count: int | None = None
    next: str | None = None
    previous: str | None = None


# These can't be type-aliases as we need to make use of runtime behavior.
PaginatedCompanies = PaginatedResponse[Company]
PaginatedFunds = PaginatedResponse[Fund]
PaginatedBudgets = PaginatedResponse[Budget]
PaginatedMetricData = PaginatedResponse[MetricData]
PaginatedMetricOptions = PaginatedResponse[MetricOption]
PaginatedCustomColumns = PaginatedResponse[CustomColumn]
PaginatedCustomColumnOptions = PaginatedResponse[CustomColumnOption]
PaginatedDocuments = PaginatedResponse[Document]
PaginatedNotes = PaginatedResponse[Note]
PaginatedUsers = PaginatedResponse[User]
PaginatedInformationRequests = PaginatedResponse[InformationRequest]
PaginatedInformationReports = PaginatedResponse[InformationReport]
