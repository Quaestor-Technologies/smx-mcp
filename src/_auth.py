from __future__ import annotations

import asyncio
import base64
import time
from typing import final

import aiohttp

from ._settings import settings

# Buffer in seconds in which we consider the token valid
# so that we refresh if it's about to expire.
_EXPIRY_BUFFER = 60


@final
class TokenManager:
    """Manages OAuth2 access tokens with automatic refresh."""

    def __init__(self) -> None:
        self._access_token: str | None = None
        self._expires_at: float | None = None
        self._refresh_lock = asyncio.Lock()

    @property
    def is_token_valid(self) -> bool:
        """Check if the current token is valid and not expired."""
        if not self._access_token or not self._expires_at:
            return False
        return time.time() < (self._expires_at - _EXPIRY_BUFFER)

    async def get_access_token(self) -> str:
        """Get a valid access token, refreshing if necessary."""
        if self.is_token_valid and self._access_token:
            return self._access_token

        async with self._refresh_lock:
            if self.is_token_valid and self._access_token:
                return self._access_token

            return await self._refresh_token()

    async def _refresh_token(self) -> str:
        """Refresh the OAuth2 access token using client credentials."""
        if not settings.smx_client_id or not settings.smx_client_secret:
            raise ValueError(
                "SMX_CLIENT_ID and SMX_CLIENT_SECRET environment variables must be set"
            )

        credential = f"{settings.smx_client_id}:{settings.smx_client_secret}"
        encoded_credential = base64.b64encode(credential.encode("utf-8")).decode()

        headers = {
            "Authorization": f"Basic {encoded_credential}",
            "Cache-Control": "no-cache",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        payload = {"grant_type": "client_credentials"}

        async with (
            aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=settings.request_timeout)
            ) as session,
            session.post(
                f"{settings.smx_base_url}/o/token/",
                headers=headers,
                data=payload,
            ) as response,
        ):
            response.raise_for_status()
            token_data = await response.json()

        access_token = token_data["access_token"]
        expires_in = token_data["expires_in"]

        self._access_token = access_token
        self._expires_at = time.time() + expires_in

        return access_token

    def clear_token(self) -> None:
        """Clear the stored token (useful for testing or manual refresh)."""
        self._access_token = None
        self._expires_at = None

    async def get_auth_headers(self) -> dict[str, str]:
        """Get authorization headers for API requests."""
        access_token = await self.get_access_token()
        return {"Authorization": f"Bearer {access_token}"}


_TOKEN_MANAGER = TokenManager()


async def get_access_token() -> str:
    """Get a valid OAuth2 access token."""
    return await _TOKEN_MANAGER.get_access_token()


async def get_auth_headers() -> dict[str, str]:
    """Get authorization headers for API requests."""
    return await _TOKEN_MANAGER.get_auth_headers()
