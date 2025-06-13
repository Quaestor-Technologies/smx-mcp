# Standard Metrics Authentication Guide

This guide explains how to set up OAuth2 authentication for the Standard Metrics MCP server.

## OAuth2 Client Credentials Authentication

The Standard Metrics MCP server uses OAuth2 client credentials authentication for secure API access with automatic token management.

### Setting Up OAuth2

1. **Get Your OAuth2 Credentials**
   - Log into your Standard Metrics account
   - Navigate to the API/Developer section
   - Create a new OAuth2 application
   - Copy your Client ID and Client Secret (shown in the dialog)

2. **Configure Environment Variables**
   Create a `.env` file in your project root with:
   ```bash
   # OAuth2 Credentials (Required)
   SMX_CLIENT_ID=your_client_id_here
   SMX_CLIENT_SECRET=your_client_secret_here
   
   # API Configuration (Optional)
   STANDARD_METRICS_BASE_URL=https://api.standardmetrics.com
   SMX_TOKEN_BASE_URL=https://api.standardmetrics.com
   REQUEST_TIMEOUT=30.0
   ```

3. **How It Works**
   - The client automatically obtains access tokens using your credentials
   - Tokens are cached and automatically refreshed before expiration
   - All API requests use `Bearer {access_token}` authentication
   - No manual token management required

### Token Management Features

- **Automatic Refresh**: Tokens are refreshed automatically 60 seconds before expiration
- **Thread-Safe**: Multiple concurrent requests share the same token safely
- **Error Handling**: Automatic retry on authentication failures
- **Memory Caching**: Tokens are cached in memory to avoid unnecessary requests

## Usage Examples

### Basic Usage
```python
from src._client import StandardMetrics

# Automatically uses OAuth2 credentials from environment
async with StandardMetrics() as client:
    companies = await client.list_companies()
    company = await client.get_company("company_id")
```

### Custom Configuration
```python
from src._client import StandardMetrics

# Override default settings
async with StandardMetrics(
    base_url="https://api.standardmetrics.com",
    timeout=60.0
) as client:
    companies = await client.list_companies()
```

### Using MCP Tools
```python
from src.tools import list_companies, get_company

# MCP tools automatically handle authentication
companies = await list_companies(page=1, page_size=50)
company = await get_company("company_id")
```

## Troubleshooting

### Common Issues

1. **"OAuth2 credentials required" Error**
   - Ensure `SMX_CLIENT_ID` and `SMX_CLIENT_SECRET` are set in your environment
   - Check that your `.env` file is in the correct location
   - Verify environment variables are loaded correctly

2. **"Invalid client credentials" Error**
   - Verify your Client ID and Client Secret are correct
   - Ensure your OAuth2 application has the necessary scopes
   - Check that credentials haven't expired or been revoked

3. **Token Refresh Failures**
   - Check network connectivity to the token endpoint
   - Verify the token base URL is correct
   - Ensure your OAuth2 application is still active

### Debug Mode

To debug authentication issues, you can clear the token cache:

```python
from src._auth import clear_token_cache

# Clear cached tokens to force refresh
clear_token_cache()
```

### Checking Token Status

```python
from src._auth import get_access_token

# Get current access token (will refresh if needed)
token = await get_access_token()
print(f"Current token: {token[:20]}...")
```

## Security Best Practices

1. **Environment Variables**: Never commit credentials to version control
2. **Scope Limitation**: Request only the minimum required OAuth2 scopes
3. **Token Storage**: Tokens are stored in memory only, not persisted to disk
4. **Credential Rotation**: Regularly rotate your OAuth2 credentials
5. **Access Control**: Limit who has access to your OAuth2 credentials

## Environment File Example

Create a `.env` file in your project root:

```bash
# Required OAuth2 Credentials
SMX_CLIENT_ID=olexpA6KNUvggCPMHn0i6d5f9u8FTSLa9iK
SMX_CLIENT_SECRET=sW0BL4bgh0ts7GH79IESFmzmyPfTfTNbCg

# Optional Configuration
STANDARD_METRICS_BASE_URL=https://api.standardmetrics.com
SMX_TOKEN_BASE_URL=https://api.standardmetrics.com
REQUEST_TIMEOUT=30.0

# MCP Server Settings (for local development)
SERVER_HOST=localhost
SERVER_PORT=8000
```

**Important**: Replace the example credentials with your actual OAuth2 credentials from Standard Metrics. 