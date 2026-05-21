"""Tests for SQL guard and result rendering."""

from __future__ import annotations

import pytest

from geobr_mcp.sql import ReadOnlySQLError, assert_read_only, render_result


def test_assert_read_only_accepts_select():
    assert_read_only("SELECT 1")


def test_assert_read_only_accepts_with():
    assert_read_only("WITH cte AS (SELECT 1) SELECT * FROM cte")


def test_assert_read_only_rejects_insert():
    with pytest.raises(ReadOnlySQLError):
        assert_read_only("INSERT INTO t VALUES (1)")


def test_assert_read_only_rejects_drop():
    with pytest.raises(ReadOnlySQLError):
        assert_read_only("DROP TABLE biomes")


def test_assert_read_only_rejects_attach():
    with pytest.raises(ReadOnlySQLError):
        assert_read_only("ATTACH 'x.db' AS x")


def test_render_result_from_relation():
    import geobr

    rel = geobr.query("SELECT 1 AS n, 'a' AS s")
    out = render_result(rel, limit=10)
    assert out["columns"] == ["n", "s"]
    assert out["rows"] == [[1, "a"]]
    assert out["row_count"] == 1
    assert out["truncated"] is False


def test_render_result_converts_geometry_column():
    import geobr

    conn = geobr.duckdb_connection()
    conn.execute("CREATE OR REPLACE VIEW _mcp_geom_test AS SELECT ST_GeomFromText('POINT(1 2)') AS geometry")
    rel = conn.sql("SELECT geometry FROM _mcp_geom_test")
    out = render_result(rel, limit=1, geometry_format="wkt")
    assert out["columns"] == ["geometry"]
    assert out["rows"][0][0].upper().startswith("POINT")
