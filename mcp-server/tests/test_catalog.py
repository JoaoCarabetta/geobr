"""Tests for the static catalog resource."""

from __future__ import annotations

from geobr_mcp.catalog import CATALOG, _ROWS, _YEARS


def test_catalog_has_all_datasets():
    assert len(CATALOG) == len(_ROWS)


def test_catalog_entry_shape():
    entry = CATALOG[0]
    assert set(entry.keys()) == {
        "dataset_id",
        "function",
        "geography",
        "source",
        "years_available",
        "table_name_pattern",
    }


def test_catalog_dataset_ids_match_years_map():
    for row in CATALOG:
        assert row["dataset_id"] in _YEARS
        assert row["years_available"] == _YEARS[row["dataset_id"]]


def test_biomes_in_catalog():
    biomes = next(r for r in CATALOG if r["dataset_id"] == "biomes")
    assert biomes["function"] == "read_biomes"
    assert 2019 in biomes["years_available"]
