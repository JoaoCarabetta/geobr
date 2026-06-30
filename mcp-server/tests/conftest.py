"""Pytest fixtures for geobr-mcp."""

from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def reset_geobr_duckdb():
    """Isolate DuckDB state between tests."""
    from geobr._duckdb_backend import _reset_shared_connection

    _reset_shared_connection()
    yield
    _reset_shared_connection()
