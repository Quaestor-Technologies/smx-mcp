# Standard Metrics MCP Server

A Model Context Protocol (MCP) server that connects Claude Desktop and other MCP-compatible clients to the Standard Metrics API, enabling AI-powered analysis of your venture capital portfolio data.

## What This Does

This MCP server allows Claude to directly access your Standard Metrics data to:

- **Analyze Portfolio Performance**: Get comprehensive overviews of all your portfolio companies
- **Query Financial Metrics**: Access revenue, growth, burn rate, and other key metrics
- **Search and Filter**: Find companies by sector, performance, or custom criteria  
- **Generate Reports**: Create detailed financial summaries and performance analyses
- **Track Trends**: Monitor metrics over time with historical data analysis
## Installation

### 1. Get Your Standard Metrics OAuth2 Credentials

1. Log into your Standard Metrics account
2. On the left hand menu, click on Settings
3. Click on Developer Settings
4. Click "Add Application" in the top right
5. Fill in the application name and description
6. Click "Create Application"
7. Copy your **Client ID** and **Client Secret** and store them securely (you won't be able to see the secret again!)

### 2. Install via Claude Desktop

Add the following to your Claude Desktop MCP configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "standard-metrics": {
      "command": "uvx",
      "args": ["smx-mcp"],
      "env": {
        "SMX_CLIENT_ID": "your_client_id_here",
        "SMX_CLIENT_SECRET": "your_client_secret_here"
      }
    }
  }
}
```

Replace `your_client_id_here` and `your_client_secret_here` with your actual OAuth2 credentials.

### 3. Restart Claude Desktop

Close and reopen Claude Desktop. You should see "Standard Metrics" appear in your MCP connections.

## Usage Examples

Once installed, you can ask Claude to analyze your portfolio data:

### Portfolio Overview
```
Show me a summary of my entire portfolio performance
```

### Company Analysis  
```
What are the key metrics for Acme Corp over the last 12 months?
```

### Sector Comparison
```
Compare the revenue growth of all my SaaS companies
```

### Financial Deep Dive
```
Create a financial summary for company ID abc123 including burn rate and runway
```

### Custom Queries
```
Find all companies with revenue growth above 50% and show their latest metrics
```

## Available Data

The MCP server provides access to:

| Data Type                | Description                                |
| ------------------------ | ------------------------------------------ |
| **Companies**            | Portfolio company information and details  |
| **Financial Metrics**    | Revenue, expenses, growth rates, burn rate |
| **Budgets & Forecasts**  | Budget data and financial projections      |
| **Custom Columns**       | Your firm's custom data columns            |
| **Documents**            | Uploaded reports and financial documents   |
| **Notes**                | Internal notes and commentary              |
| **Fund Data**            | Fund-level information                     |
| **Information Requests** | Data collection requests sent to companies |
| **Information Reports**  | Responses to information requests          |
| **Users**                | Team members in your firm                  |


## Alternative Installation Methods

### Using Docker

```json
{
  "mcpServers": {
    "standard-metrics": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-e", "SMX_CLIENT_ID=your_client_id_here",
        "-e", "SMX_CLIENT_SECRET=your_client_secret_here",
        "-p", "8000:8000",
        "quaestorapp/mcp-server:latest"
      ]
    }
  }
}
```


### Local Development

```bash
git clone https://github.com/Quaestor-Technologies/smx-mcp
cd mcp-server
uv sync
```

Then use the local path in your Claude Desktop config:

```json
{
  "mcpServers": {
    "standard-metrics": {
      "command": "uv",
      "args": ["run", "python", "-m", "src.server"],
      "env": {
        "SMX_CLIENT_ID": "your_client_id_here",
        "SMX_CLIENT_SECRET": "your_client_secret_here"
      }
    }
  }
}
```

## Running with Docker

### 1. Run with the Hosted Image (Recommended)

You can use the prebuilt image from Docker Hub for the fastest setup:

```bash
docker run --rm -it \
  -e SMX_CLIENT_ID=your_client_id_here \
  -e SMX_CLIENT_SECRET=your_client_secret_here \
  -p 8000:8000 \
  standardmetrics/mcp-server:latest
```

- Replace `your_client_id_here` and `your_client_secret_here` with your actual Standard Metrics OAuth2 credentials.
- The server will be available at `http://localhost:8000`.

### 2. Build and Run Locally

If you want to build the image yourself (for development or customization):

```bash
# Build the Docker image
docker build -t smx-mcp .

# Run the container
docker run --rm -it \
  -e SMX_CLIENT_ID=your_client_id_here \
  -e SMX_CLIENT_SECRET=your_client_secret_here \
  -p 8000:8000 \
  smx-mcp
```

- Again, replace the environment variables with your credentials.

### 3. Using Docker in Claude Desktop

Add this to your Claude Desktop MCP config to use the Docker image:

```json
{
  "mcpServers": {
    "standard-metrics": {
      "command": "docker",
      "args": [
        "run", "--rm", "-i",
        "-e", "SMX_CLIENT_ID=your_client_id_here",
        "-e", "SMX_CLIENT_SECRET=your_client_secret_here",
        "-p", "8000:8000",
        "standardmetrics/mcp-server:latest"
      ]
    }
  }
}
```

**Tip:**
- The hosted image is updated automatically with every release.
- For local development, you can mount your code into the container with `-v $(pwd)/src:/app/src` if you want live code reloads.

## Troubleshooting

### "Connection Failed" Error
- Verify your Client ID and Client Secret are correct
- Ensure your OAuth2 application is active in Standard Metrics
- Check that Claude Desktop has been restarted after configuration

### "No Data Found" Error  
- Confirm your Standard Metrics account has portfolio data
- Verify your OAuth2 application has the necessary permissions
- Try a simpler query first: "List my companies"

### Authentication Issues
- Double-check your credentials haven't expired
- Ensure there are no extra spaces in your configuration
- Try regenerating your OAuth2 credentials if needed


## Available Tools

### Companies
**list_companies** - List all companies associated with your firm
- `page`: Page number for pagination (number, optional, default: 1)
- `per_page`: Results per page (number, optional, default: 100, max: 100)

**get_company** - Get a specific company by ID
- `company_id`: The unique identifier for the company (string, required)

**search_companies** - Search companies by various criteria
- `name_contains`: Filter companies containing this text in their name (string, optional)
- `sector`: Filter companies by sector (string, optional)
- `city`: Filter companies by city (string, optional)
- `page`: Page number for pagination (number, optional, default: 1)
- `per_page`: Results per page (number, optional, default: 100, max: 100)

### Financial Metrics
**get_company_metrics** - Get metrics for a specific company
- `company_id`: The unique identifier for the company (string, required)
- `from_date`: Start date for metrics (YYYY-MM-DD format) (date, optional)
- `to_date`: End date for metrics (YYYY-MM-DD format) (date, optional)
- `category`: Filter by metric category (string, optional)
- `cadence`: Filter by metric cadence (daily, monthly, etc.) (string, optional)
- `include_budgets`: Include budget metrics in results (boolean, optional, default: false)
- `page`: Page number for pagination (number, optional, default: 1)
- `per_page`: Results per page (number, optional, default: 100, max: 100)

**get_metrics_options** - Get available metric categories and options
- `category_name`: Filter by specific category name (string, optional)
- `is_standard`: Filter by standard vs custom metrics (boolean, optional)
- `page`: Page number for pagination (number, optional, default: 1)
- `per_page`: Results per page (number, optional, default: 100, max: 100)

**get_company_recent_metrics** - Get the most recent metrics for a company
- `company_id`: The unique identifier for the company (string, required)
- `category`: Filter by specific metric category (string, optional)
- `limit`: Maximum number of recent metrics to return (number, optional, default: 10)

### Portfolio Analysis
**get_portfolio_summary** - Get a comprehensive portfolio summary including companies, funds, and key metrics
- `company_ids`: Specific company IDs to include (array of strings, optional, if None includes all companies)
- `max_companies`: Maximum number of companies to include metrics for (number, optional, if None includes all)
- `include_metrics`: Whether to fetch metrics for each company (boolean, optional, default: true)
- `metrics_per_company`: Number of recent metrics to fetch per company (number, optional, default: 50)

**get_company_performance** - Get comprehensive performance data for a specific company
- `company_id`: The unique identifier for the company (string, required)
- `months`: Number of months of historical data to include (number, optional, default: 12)

**get_company_financial_summary** - Get a financial summary for a company including key metrics over time
- `company_id`: The unique identifier for the company (string, required)
- `months`: Number of months of historical data to include (number, optional, default: 12)

### Budgets & Forecasts
**list_budgets** - List all budgets associated with your firm
- `company_slug`: Filter by company slug (string, optional)
- `company_id`: Filter by company ID (string, optional)
- `page`: Page number for pagination (number, optional, default: 1)
- `per_page`: Results per page (number, optional, default: 100, max: 100)

### Custom Data
**get_custom_columns** - Get custom column data for companies
- `company_slug`: Filter by company slug (string, optional)
- `company_id`: Filter by company ID (string, optional)
- `page`: Page number for pagination (number, optional, default: 1)
- `per_page`: Results per page (number, optional, default: 100, max: 100)

**get_custom_column_options** - Get all custom columns and their available options
- `page`: Page number for pagination (number, optional, default: 1)
- `per_page`: Results per page (number, optional, default: 100, max: 100)

### Documents
**list_documents** - List all documents associated with your firm
- `company_id`: Filter by company ID (string, optional)
- `parse_state`: Filter by document parse state (string, optional)
- `from_date`: Filter documents from this date (YYYY-MM-DD format) (date, optional)
- `to_date`: Filter documents to this date (YYYY-MM-DD format) (date, optional)
- `source`: Filter by document source (string, optional)
- `page`: Page number for pagination (number, optional, default: 1)
- `per_page`: Results per page (number, optional, default: 100, max: 100)

### Funds
**list_funds** - List all funds associated with the firm
- `page`: Page number for pagination (number, optional, default: 1)
- `per_page`: Results per page (number, optional, default: 100, max: 100)

### Information Requests & Reports
**list_information_requests** - List all information requests associated with the firm
- `name`: Filter by request name (string, optional)
- `page`: Page number for pagination (number, optional, default: 1)
- `per_page`: Results per page (number, optional, default: 100, max: 100)

**list_information_reports** - List all information reports associated with the firm
- `company_id`: Filter by company ID (string, optional)
- `information_request_id`: Filter by information request ID (string, optional)
- `page`: Page number for pagination (number, optional, default: 1)
- `per_page`: Results per page (number, optional, default: 100, max: 100)

### Notes
**list_notes** - List all notes associated with a specific company
- `company_slug`: Filter by company slug (string, optional)
- `company_id`: Filter by company ID (string, optional)
- `sort_by`: Sort notes by specific field (string, optional)
- `page`: Page number for pagination (number, optional, default: 1)
- `per_page`: Results per page (number, optional, default: 100, max: 100)

**get_company_notes_summary** - Get a summary of notes for a company
- `company_id`: The unique identifier for the company (string, required)
- `recent_notes_limit`: The number of recent notes to return (number, optional, default: 5, max: 100)

### Users
**list_users** - List all users associated with your firm
- `email`: Filter by user email (string, optional)
- `page`: Page number for pagination (number, optional, default: 1)
- `per_page`: Results per page (number, optional, default: 100, max: 100)


## Support

- **Standard Metrics API Issues**: Contact Standard Metrics support
- **MCP Server Issues**: [Open an issue on GitHub](https://github.com/Quaestor-Technologies/smx-mcp/issues)
- **Claude Desktop Issues**: Check [Claude Desktop documentation](https://support.anthropic.com/en/articles/10065433-installing-claude-for-desktop)

