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

    # OAuth2 client credentials
    smx_client_id: str | None = pydantic.Field(
        default=None, description="Standard Metrics OAuth2 client ID"
    )
    smx_client_secret: str | None = pydantic.Field(
        default=None, description="Standard Metrics OAuth2 client secret"
    )

    # API endpoints
    smx_base_url: str = pydantic.Field(
        default="https://api.standardmetrics.io",
        description="Base URL for the Standard Metrics API",
    )

    # Request settings
    request_timeout: float = pydantic.Field(
        default=30.0, description="Timeout for API requests in seconds"
    )


settings = Settings()
