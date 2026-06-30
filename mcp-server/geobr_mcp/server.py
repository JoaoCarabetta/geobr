"""geobr MCP server: read-only spatial SQL over geobr's auto-resolving DuckDB."""

from __future__ import annotations

import warnings

import geobr
from mcp.server.fastmcp import FastMCP

from geobr_mcp.catalog import CATALOG
from geobr_mcp.sql import assert_read_only, render_result

mcp = FastMCP("geobr")


@mcp.resource("geobr://catalog")
def catalog_resource() -> list[dict]:
    """Static catalog of geobr datasets with available years (no network)."""
    return CATALOG


@mcp.resource("geobr://tables")
def tables_resource() -> list[dict]:
    """Snapshots resolved in this session (SHOW TABLES + column schemas)."""
    conn = geobr.duckdb_connection()
    table_rows = conn.execute("SHOW TABLES").fetchall()
    out: list[dict] = []
    for (name,) in table_rows:
        safe = name.replace('"', '""')
        schema_rows = conn.sql(f'DESCRIBE SELECT * FROM "{safe}"').fetchall()
        out.append(
            {
                "name": name,
                "columns": [
                    {"name": row[0], "type": str(row[1])} for row in schema_rows
                ],
            }
        )
    return out


@mcp.tool()
def query(
    sql: str,
    limit: int = 100,
    geometry_format: str = "wkt",
) -> dict:
    """Run a read-only spatial SQL query against geobr's auto-resolving DuckDB.

    Reference datasets as `<alias>_<year>` (e.g. `states_2020`, `biomes_2019`)
    or bare `<alias>` for the latest available year. Geometry is returned as WKT
    by default; set geometry_format to `geojson` for GeoJSON strings.
    """
    assert_read_only(sql)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        rel = geobr.query(sql)
        return render_result(
            rel,
            limit=limit,
            geometry_format=geometry_format,
            warnings_list=caught,
        )


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
