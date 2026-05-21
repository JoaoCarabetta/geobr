"""Static geobr dataset catalog for MCP discovery (no network calls)."""

from __future__ import annotations

# Years copied from README.md "Years available" column (updated manually).
_YEARS: dict[str, list[int | str]] = {
    "amazonialegal": [2019, 2020, 2021, 2022, 2024],
    "biomes": [2006, 2019, 2025],
    "censustracts": [2000, 2010, 2022],
    "conservationunits": [202402, 202503],
    "country": [
        1872, 1900, 1911, 1920, 1933, 1940, 1950, 1960, 1970, 1980, 1991, 2000,
        2001, 2010, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022,
        2023, 2024, 2025,
    ],
    "disasterriskareas": [2010],
    "favelas": [2022],
    "healthfacilities": [
        201704, 201707, 201710, 201801, 201804, 201807, 201810, 201901, 201904,
        201907, 201910, 202001, 202004, 202007, 202010, 202101, 202104, 202107,
        202110, 202201, 202204, 202207, 202210, 202301, 202304, 202307, 202310,
        202401, 202404, 202407, 202410, 202501, 202504, 202507, 202510, 202601,
    ],
    "healthregions": [1991, 1994, 1997, 2001, 2005, 2013, 2023, 2024, 2025],
    "immediateregions": [2019, 2020, 2021, 2022, 2023, 2024, 2025],
    "indigenousland": [2016, 2017, 2018, 2019, 2022, 2024, 2025],
    "intermediateregions": [2019, 2020, 2021, 2022, 2023, 2024, 2025],
    "mesoregions": [
        2000, 2001, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022,
    ],
    "metropolitanarea": [
        1970, 2001, 2002, 2003, 2005, 2008, 2009, 2010, 2013, 2014, 2015, 2016,
        2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024,
    ],
    "microregions": [
        2000, 2001, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022,
    ],
    "municipalities": [
        1872, 1900, 1911, 1920, 1933, 1940, 1950, 1960, 1970, 1980, 1991, 2000,
        2001, 2005, 2007, 2010, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020,
        2021, 2022, 2023, 2024, 2025,
    ],
    "municipalseats": [
        1872, 1900, 1911, 1920, 1933, 1940, 1950, 1960, 1970, 1980, 1991, 2010,
        2022,
    ],
    "neighborhoods": [2010, 2022],
    "pollingplaces": [2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024],
    "urbanconcentrations": [2010],
    "poparrengements": [2010],
    "quilombolalands": [202605],
    "amc": ["temporarily suspended"],
    "regions": [
        1872, 1900, 1911, 1920, 1933, 1940, 1950, 1960, 1970, 1980, 1991, 2000,
        2001, 2010, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022,
        2023, 2024, 2025,
    ],
    "schools": list(range(2007, 2026)),
    "semiarid": [2005, 2017, 2021, 2022],
    "states": [
        1872, 1900, 1911, 1920, 1933, 1940, 1950, 1960, 1970, 1980, 1991, 2000,
        2001, 2010, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022,
        2023, 2024, 2025,
    ],
    "statsgrid": [2010],
    "urbanareas": [2005, 2015, 2019],
    "weightingareas": [2010],
}

_ROWS: list[dict[str, str]] = [
    {"function": "read_amazon", "geography": "Brazil's Legal Amazon", "source": "MMA", "dataset_id": "amazonialegal"},
    {"function": "read_biomes", "geography": "Biomes", "source": "IBGE", "dataset_id": "biomes"},
    {"function": "read_census_tract", "geography": "Census tract (setor censitário)", "source": "IBGE", "dataset_id": "censustracts"},
    {"function": "read_conservation_units", "geography": "Environmental Conservation Units", "source": "MMA", "dataset_id": "conservationunits"},
    {"function": "read_country", "geography": "Country", "source": "IBGE", "dataset_id": "country"},
    {"function": "read_disaster_risk_area", "geography": "Disaster risk areas", "source": "CEMADEN and IBGE", "dataset_id": "disasterriskareas"},
    {"function": "read_favelas", "geography": "Favelas and urban communities", "source": "IBGE", "dataset_id": "favelas"},
    {"function": "read_health_facilities", "geography": "Health facilities", "source": "CNES, DataSUS", "dataset_id": "healthfacilities"},
    {"function": "read_health_region", "geography": "Health regions and macro regions", "source": "DataSUS", "dataset_id": "healthregions"},
    {"function": "read_immediate_region", "geography": "Immediate region", "source": "IBGE", "dataset_id": "immediateregions"},
    {"function": "read_indigenous_land", "geography": "Indigenous lands", "source": "FUNAI", "dataset_id": "indigenousland"},
    {"function": "read_intermediate_region", "geography": "Intermediate region", "source": "IBGE", "dataset_id": "intermediateregions"},
    {"function": "read_meso_region", "geography": "Meso region", "source": "IBGE", "dataset_id": "mesoregions"},
    {"function": "read_metro_area", "geography": "Metropolitan areas", "source": "IBGE", "dataset_id": "metropolitanarea"},
    {"function": "read_micro_region", "geography": "Micro region", "source": "IBGE", "dataset_id": "microregions"},
    {"function": "read_municipality", "geography": "Municipality", "source": "IBGE", "dataset_id": "municipalities"},
    {"function": "read_municipal_seat", "geography": "Municipality seats (sedes municipais)", "source": "IBGE", "dataset_id": "municipalseats"},
    {"function": "read_neighborhood", "geography": "Neighborhood limits", "source": "IBGE", "dataset_id": "neighborhoods"},
    {"function": "read_polling_places", "geography": "Voting places", "source": "TSE", "dataset_id": "pollingplaces"},
    {"function": "read_urban_concentrations", "geography": "Urban concentration areas", "source": "IBGE", "dataset_id": "urbanconcentrations"},
    {"function": "read_pop_arrangements", "geography": "Population arrangements", "source": "IBGE", "dataset_id": "poparrengements"},
    {"function": "read_quilombola_lands", "geography": "Quilombola lands", "source": "INCRA", "dataset_id": "quilombolalands"},
    {"function": "read_comparable_areas", "geography": "Comparable municipalities (AMCs)", "source": "IBGE", "dataset_id": "amc"},
    {"function": "read_region", "geography": "Region", "source": "IBGE", "dataset_id": "regions"},
    {"function": "read_schools", "geography": "Schools", "source": "INEP", "dataset_id": "schools"},
    {"function": "read_semiarid", "geography": "Semi Arid region", "source": "IBGE", "dataset_id": "semiarid"},
    {"function": "read_state", "geography": "States", "source": "IBGE", "dataset_id": "states"},
    {"function": "read_statistical_grid", "geography": "Statistical Grid", "source": "IBGE", "dataset_id": "statsgrid"},
    {"function": "read_urban_area", "geography": "Urban footprints", "source": "IBGE", "dataset_id": "urbanareas"},
    {"function": "read_weighting_area", "geography": "Census weighting area", "source": "IBGE", "dataset_id": "weightingareas"},
]


def _build_catalog() -> list[dict]:
    out: list[dict] = []
    for row in _ROWS:
        dataset_id = row["dataset_id"]
        out.append(
            {
                "dataset_id": dataset_id,
                "function": row["function"],
                "geography": row["geography"],
                "source": row["source"],
                "years_available": _YEARS.get(dataset_id, []),
                "table_name_pattern": (
                    f"Use FROM {dataset_id}_<year> in SQL (e.g. {dataset_id}_2022). "
                    f"Bare FROM {dataset_id} resolves to the latest available year."
                ),
            }
        )
    return out


CATALOG: list[dict] = _build_catalog()
