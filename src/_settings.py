from __future__ import annotations

import pydantic
import pydantic_settings


class Settings(pydantic_settings.BaseSettings):
    """Settings for the Standard Metrics MCP server."""

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore",
    }

    standard_metrics_api_key: str | None = pydantic.Field(
        default=None, description="Standard Metrics API key for authentication"
    )
    standard_metrics_base_url: str = pydantic.Field(
        default="https://api.standardmetrics.com",
        description="Base URL for the Standard Metrics API",
    )
    request_timeout: float = pydantic.Field(
        default=30.0, description="Timeout for API requests in seconds"
    )
    server_host: str = pydantic.Field(default="localhost", description="Host for the MCP server")
    server_port: int = pydantic.Field(default=8000, description="Port for the MCP server")


settings = Settings()


def get_api_key() -> str:
    """Get the API key with proper error handling."""
    if settings.standard_metrics_api_key is None:
        raise ValueError(
            "Standard Metrics API key not configured. "
            "Set STANDARD_METRICS_API_KEY environment variable or "
            "provide API key via connection parameters."
        )
    return settings.standard_metrics_api_key
