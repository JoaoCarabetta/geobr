"""Tests for MCP resources (no network)."""

from __future__ import annotations

from geobr_mcp.catalog import CATALOG
from geobr_mcp.server import catalog_resource, tables_resource


def test_catalog_resource_returns_catalog():
    assert catalog_resource() == CATALOG


def test_tables_resource_empty_session():
    tables = tables_resource()
    assert isinstance(tables, list)
