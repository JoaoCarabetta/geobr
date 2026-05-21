# geobr-mcp

MCP server for querying official Brazilian spatial datasets via [geobr](https://github.com/ipeaGIT/geobr) and DuckDB.

Designed for AI assistants (Cursor, Claude Desktop, etc.): a **single `query` tool** runs read-only spatial SQL. Datasets are referenced as `<alias>_<year>` (e.g. `states_2020`, `biomes_2019`) and auto-download on first use.

## Install

```bash
pip install geobr-mcp
# or one-shot (no install)
uvx geobr-mcp
```

Requires Python 3.10+ and `geobr[duckdb]>=0.3.0`.

## Cursor configuration

Add to `.cursor/mcp.json` (or global MCP settings):

```json
{
  "mcpServers": {
    "geobr": {
      "command": "uvx",
      "args": ["geobr-mcp"]
    }
  }
}
```

For local development in this monorepo:

```json
{
  "mcpServers": {
    "geobr": {
      "command": "uv",
      "args": ["run", "--directory", "mcp-server", "geobr-mcp"]
    }
  }
}
```

## Claude Desktop configuration

```json
{
  "mcpServers": {
    "geobr": {
      "command": "uvx",
      "args": ["geobr-mcp"]
    }
  }
}
```

## MCP surface

### Resources

| URI | Description |
|-----|-------------|
| `geobr://catalog` | All datasets: `dataset_id`, geography, source, years, SQL naming hint |
| `geobr://tables` | Snapshots already loaded in this session (`SHOW TABLES` + schemas) |

### Tools

| Tool | Description |
|------|-------------|
| `query(sql, limit=100, geometry_format="wkt")` | Read-only DuckDB SQL. Auto-downloads missing datasets. Returns JSON rows. |

### Example workflow for an LLM

1. Read `geobr://catalog` to pick `dataset_id` and year.
2. Call `query` with SQL such as:

```sql
SELECT name_state, abbrev_state
FROM states_2020
WHERE abbrev_state = 'RJ'
```

3. For geometry, use `ST_AsText(geometry)` or set `geometry_format="geojson"`.

```sql
SELECT name_biome, ST_Area(geometry) / 1e6 AS area_km2
FROM biomes_2019
ORDER BY area_km2 DESC
```

Bare table names (e.g. `FROM biomes`) resolve to the latest available year and may include a warning in the response.

## Development

```bash
cd mcp-server
uv sync
uv run pytest -m "not network"   # unit tests
uv run pytest -m network         # integration (downloads data)
```

## License

MIT (same as geobr).
