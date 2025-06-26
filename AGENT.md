# Standard Metrics MCP Server - Agent Guide

## Commands
- **Lint**: `uv run ruff check src/` (fix with `--fix`)
  - Make sure you run this after any changes.
- **Format**: `uv run ruff format src/`
  - Make sure you run this after any changes.
- **Type check**: `uv run pyright`
- **Test**: `uv run pytest` (single test: `uv run pytest path/to/test.py::test_name`)
  - Ensure you're writing tests in a functional style, making use of parameterization and fixtures when needed.
  - Tests must be passing before finishing your change.
- **Install deps**: `uv sync` (dev deps included)
- **Run server**: `uv run python src/server.py`

## Architecture
- **Type**: Model Context Protocol (MCP) server for Standard Metrics API
- **Main entry**: `src/server.py` - FastMCP server with async main
- **Core modules**: `_client.py` (API client), `_auth.py` (OAuth2), `_types.py` (Pydantic models), `_settings.py` (config)
- **Tools**: `tools.py` - MCP tool definitions for company search and financial summaries
- **Dependencies**: FastMCP, aiohttp, Pydantic for async API client with type safety

## Code Style
- **Imports**: Required `from __future__ import annotations` header (enforced by Ruff)
- **Types**: Strict type checking (Pyright), Pydantic models for data validation
- **Naming**: snake_case for variables/functions, PascalCase for classes/enums
- **Line length**: 100 chars max, Ruff formatter handles formatting
- **Async**: Use async/await patterns, aiohttp for HTTP clients
- **Error handling**: Raise appropriate exceptions, use Pydantic validation
