"""SQL safety and result rendering for the geobr MCP server."""

from __future__ import annotations

import json
import re
import warnings
from typing import Any, Optional

_MAX_LIMIT = 10_000
_DEFAULT_LIMIT = 100
_MAX_BYTES = 256 * 1024

_ALLOWED_PREFIX = re.compile(
    r"^\s*(WITH|SELECT|DESCRIBE|SHOW|PRAGMA|EXPLAIN)\b",
    re.IGNORECASE | re.DOTALL,
)
_FORBIDDEN = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|ATTACH|DETACH|COPY|"
    r"TRUNCATE|GRANT|REVOKE|LOAD|INSTALL|EXPORT|IMPORT)\b",
    re.IGNORECASE,
)


class ReadOnlySQLError(ValueError):
    """Raised when SQL is not read-only."""


def assert_read_only(sql: str) -> None:
    """Reject non-read-only SQL statements."""
    stripped = sql.strip()
    if not stripped:
        raise ReadOnlySQLError("SQL must not be empty.")
    if _FORBIDDEN.search(stripped):
        raise ReadOnlySQLError(
            "Only read-only queries are allowed (SELECT, WITH, DESCRIBE, SHOW, "
            "PRAGMA, EXPLAIN)."
        )
    if not _ALLOWED_PREFIX.match(stripped):
        raise ReadOnlySQLError(
            "Query must start with SELECT, WITH, DESCRIBE, SHOW, PRAGMA, or EXPLAIN."
        )


def _clamp_limit(limit: int) -> int:
    if limit < 1:
        return _DEFAULT_LIMIT
    return min(limit, _MAX_LIMIT)


def _serialize_value(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, (bytes, bytearray, memoryview)):
        return value.hex()
    return str(value)


def _estimate_payload_size(rows: list[list[Any]]) -> int:
    try:
        return len(json.dumps(rows, default=str))
    except Exception:
        return _MAX_BYTES + 1


def _format_warnings(caught: list[warnings.WarningMessage]) -> list[str]:
    return [str(w.message) for w in caught]


def _relation_sql(relation: Any) -> Optional[str]:
    if hasattr(relation, "sql_query"):
        return relation.sql_query()
    if hasattr(relation, "sql"):
        return relation.sql()
    return None


def _geometry_columns(relation: Any, columns: list[str]) -> list[str]:
    if hasattr(relation, "types") and hasattr(relation, "columns"):
        return [
            col
            for col, typ in zip(relation.columns, relation.types)
            if "GEOMETRY" in str(typ).upper()
        ]
    return [c for c in columns if c.lower() in ("geometry", "geom")]


def render_result(
    relation: Any,
    *,
    limit: int = _DEFAULT_LIMIT,
    geometry_format: str = "wkt",
    warnings_list: Optional[list[warnings.WarningMessage]] = None,
) -> dict[str, Any]:
    """Convert a DuckDB relation to an MCP-friendly JSON payload."""
    limit = _clamp_limit(limit)
    geom_fmt = (geometry_format or "wkt").lower()
    if geom_fmt not in ("wkt", "geojson"):
        geom_fmt = "wkt"

    limited = relation.limit(limit + 1)
    columns = list(limited.columns) if hasattr(limited, "columns") else list(limited.df().columns)
    geom_cols = _geometry_columns(limited, columns)

    inner_sql = _relation_sql(limited)
    if geom_cols and inner_sql:
        try:
            import geobr

            conn = geobr.duckdb_connection()
            exprs = []
            for col in columns:
                safe = col.replace('"', '""')
                if col in geom_cols:
                    fn = "ST_AsText" if geom_fmt == "wkt" else "ST_AsGeoJSON"
                    exprs.append(f'{fn}("{safe}") AS "{safe}"')
                else:
                    exprs.append(f'"{safe}"')
            wrapped = (
                f"SELECT {', '.join(exprs)} FROM ({inner_sql}) AS _mcp_sub "
                f"LIMIT {limit + 1}"
            )
            df = conn.sql(wrapped).df()
        except Exception:
            df = limited.df()
    else:
        df = limited.df()

    truncated = len(df) > limit
    if truncated:
        df = df.head(limit)
    columns = list(df.columns)

    rows = [
        [_serialize_value(v) for v in row]
        for row in df.itertuples(index=False, name=None)
    ]

    # Byte cap: shrink rows if payload is too large.
    while rows and _estimate_payload_size(rows) > _MAX_BYTES:
        rows = rows[: max(1, len(rows) // 2)]
        truncated = True

    return {
        "columns": columns,
        "rows": rows,
        "row_count": len(rows),
        "truncated": truncated,
        "warnings": _format_warnings(warnings_list or []),
    }
