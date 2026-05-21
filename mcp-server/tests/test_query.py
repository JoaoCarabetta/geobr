"""Integration tests for the query tool (network required)."""

from __future__ import annotations

import json

import pytest

from geobr_mcp.server import query
from geobr_mcp.sql import ReadOnlySQLError, assert_read_only


@pytest.mark.network
def test_query_count_biomes_2019():
    result = query("SELECT count(*) AS n FROM biomes_2019", limit=10)
    assert result["row_count"] == 1
    assert result["columns"] == ["n"]
    assert int(result["rows"][0][0]) >= 1


@pytest.mark.network
def test_query_spatial_area():
    result = query(
        "SELECT name_biome, ST_Area(geometry) AS area FROM biomes_2019 LIMIT 3",
        limit=10,
    )
    assert result["row_count"] <= 3
    assert "area" in result["columns"]


@pytest.mark.network
def test_query_geometry_wkt():
    result = query(
        "SELECT ST_AsText(geometry) AS geometry FROM biomes_2019 LIMIT 1",
        limit=1,
        geometry_format="wkt",
    )
    wkt = result["rows"][0][0]
    assert isinstance(wkt, str)
    assert wkt.upper().startswith(("POLYGON", "MULTIPOLYGON"))


@pytest.mark.network
def test_query_geometry_geojson():
    result = query(
        "SELECT ST_AsGeoJSON(geometry) AS geometry FROM biomes_2019 LIMIT 1",
        limit=1,
        geometry_format="geojson",
    )
    geojson_str = result["rows"][0][0]
    parsed = json.loads(geojson_str)
    assert parsed["type"] in ("Polygon", "MultiPolygon")


@pytest.mark.network
def test_query_bare_name_surfaces_warning():
    # Bare alias resolves to latest available year (may emit a warning).
    result = query("SELECT name_state FROM states LIMIT 1", limit=1)
    assert result["row_count"] >= 1
    assert isinstance(result["warnings"], list)


def test_query_rejects_write():
    with pytest.raises(ReadOnlySQLError):
        query("DROP TABLE biomes", limit=1)
