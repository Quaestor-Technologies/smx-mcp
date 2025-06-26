from __future__ import annotations

from typing import Any
import time

import pytest
from aioresponses import aioresponses

import pytest_mock
from src._auth import TokenManager


@pytest.fixture
def token_manager() -> TokenManager:
    return TokenManager()


@pytest.mark.parametrize(
    "expires_in,should_be_valid",
    [
        (3600, True),  # 1 hour token, should be valid
        (120, True),  # 2 minutes token, should be valid
        (30, False),  # 30 seconds token, should be invalid (within buffer)
        (0, False),  # Expired token, should be invalid
    ],
)
def test_token_validity_check(
    token_manager: TokenManager,
    expires_in: int,
    should_be_valid: bool,
):
    """Test token validity with different expiration times."""
    token_manager._access_token = "test_token"  # type: ignore
    token_manager._expires_at = time.time() + expires_in  # type: ignore
    assert token_manager.is_token_valid == should_be_valid


@pytest.mark.asyncio
async def test_get_access_token(
    token_manager: TokenManager,
    mock_token_response: dict[str, Any],
    mocker: pytest_mock.MockerFixture,
):
    """Test getting access token for the first time."""
    time_of_request = 1719321600
    mocker.patch("time.time", return_value=time_of_request)
    with aioresponses() as mock_api:
        mock_api.post(  # type: ignore
            "https://api.standardmetrics.io/o/token/",
            payload=mock_token_response,
        )

        token = await token_manager.get_access_token()
        assert token == "test_access_token_12345"
        assert token_manager._access_token == "test_access_token_12345"  # type: ignore
        assert (
            token_manager._expires_at  # type: ignore
            >= time_of_request + mock_token_response["expires_in"]
        )


@pytest.mark.asyncio
async def test_get_access_token_cached(
    token_manager: TokenManager,
):
    """Test that cached valid token is returned without API call."""
    token_manager._access_token = "cached_token"  # type: ignore
    token_manager._expires_at = time.time() + 3600  # 1 hour from now  # type: ignore

    with aioresponses() as mock_api:
        token = await token_manager.get_access_token()
        assert token == "cached_token"
        assert len(mock_api.requests) == 0  # type: ignore
