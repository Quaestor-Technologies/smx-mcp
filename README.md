# Standard Metrics MCP Server

A Model Context Protocol (MCP) server that connects Claude Desktop to the Standard Metrics API, enabling AI-powered analysis of your venture capital portfolio data.

![Standard Metrics MCP Demo](docs/images/demo.gif)

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
2. Navigate to **API/Developer** section  
3. Create a new **OAuth2 application**
4. Copy your **Client ID** and **Client Secret** (save these - you won't see the secret again!)

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

| Data Type               | Description                                |
| ----------------------- | ------------------------------------------ |
| **Companies**           | Portfolio company information and details  |
| **Financial Metrics**   | Revenue, expenses, growth rates, burn rate |
| **Budgets & Forecasts** | Budget data and financial projections      |
| **Custom Fields**       | Your firm's custom data columns            |
| **Documents**           | Uploaded reports and financial documents   |
| **Notes**               | Internal notes and commentary              |
| **Fund Data**           | Fund-level information and allocations     |

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
        "standardmetrics/mcp-server:latest"
      ]
    }
  }
}
```


### Local Development

```bash
git clone https://github.com/standardmetrics/mcp-server
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

## Privacy & Security

- **OAuth2 Security**: Uses industry-standard OAuth2 client credentials flow
- **No Data Storage**: Your data is never stored by the MCP server
- **Direct API Access**: Connects directly to Standard Metrics API
- **Local Processing**: All analysis happens locally in Claude Desktop

## Support

- **Standard Metrics API Issues**: Contact Standard Metrics support
- **MCP Server Issues**: [Open an issue on GitHub](https://github.com/standardmetrics/mcp-server/issues)
- **Claude Desktop Issues**: Check [Claude Desktop documentation](https://claude.ai/desktop)
