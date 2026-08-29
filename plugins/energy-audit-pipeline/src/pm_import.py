"""Import properties from an ENERGY STAR Portfolio Manager CSV export.

Portfolio Manager has a real web services API, but it requires a web
services account and OAuth-style setup that's easy to get wrong without
a live account to test against. Every Portfolio Manager account can
already export its property list to CSV/XLSX from the web UI (My
Portfolio -> Download to Spreadsheet), so that export is the supported
path here: no credentials, no API contract to keep in sync, works
offline once exported.

Column headers in Portfolio Manager exports vary by report
configuration, so columns are detected by matching header text rather
than requiring an exact schema.
"""

from __future__ import annotations

import csv
import sqlite3

from db import now

HEADER_ALIASES: dict[str, list[str]] = {
    "pm_property_id": ["property id", "portfolio manager property id"],
    "name": ["property name"],
    "address": ["property address", "address 1", "address"],
    "city": ["city"],
    "state": ["state", "province"],
    "sqft": ["gross floor area", "property gfa"],
    "building_type": ["primary property type", "property type"],
    "energy_star_score": ["energy star score"],
    "site_eui": ["site eui"],
}


def detect_columns(fieldnames: list[str]) -> dict[str, str]:
    detected: dict[str, str] = {}
    for logical, aliases in HEADER_ALIASES.items():
        for field in fieldnames:
            field_lower = field.strip().lower()
            if any(alias in field_lower for alias in aliases):
                detected[logical] = field
                break
    return detected


def _to_float(value: str) -> float | None:
    try:
        return float(str(value).replace(",", "").strip())
    except (TypeError, ValueError):
        return None


def _to_int(value: str) -> int | None:
    as_float = _to_float(value)
    return int(as_float) if as_float is not None else None


def import_csv(path: str, conn: sqlite3.Connection) -> tuple[int, int, int]:
    """Import a Portfolio Manager CSV export. Returns (created, updated, skipped)."""
    created = updated = skipped = 0

    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames:
            return (0, 0, 0)
        columns = detect_columns(reader.fieldnames)

        if "name" not in columns:
            raise ValueError(
                "Could not find a 'Property Name' column in this CSV. "
                "Export from Portfolio Manager's My Portfolio -> Download to Spreadsheet."
            )

        for row in reader:
            name = (row.get(columns["name"]) or "").strip()
            if not name:
                skipped += 1
                continue

            pm_property_id = row.get(columns.get("pm_property_id", ""), "").strip() or None
            address = row.get(columns.get("address", ""), "").strip() or None
            city = row.get(columns.get("city", ""), "").strip() or None
            state = row.get(columns.get("state", ""), "").strip() or None
            building_type = row.get(columns.get("building_type", ""), "").strip() or None
            sqft = _to_float(row.get(columns.get("sqft", ""), ""))
            energy_star_score = _to_int(row.get(columns.get("energy_star_score", ""), ""))
            site_eui = _to_float(row.get(columns.get("site_eui", ""), ""))

            existing = None
            if pm_property_id:
                existing = conn.execute(
                    "SELECT id FROM buildings WHERE pm_property_id = ?", (pm_property_id,)
                ).fetchone()
            if existing is None:
                existing = conn.execute(
                    "SELECT id FROM buildings WHERE name = ? AND (address IS ? OR address = ?)",
                    (name, address, address),
                ).fetchone()

            timestamp = now()
            if existing is None:
                conn.execute(
                    """
                    INSERT INTO buildings (
                        name, address, city, state, building_type, sqft,
                        stage, pm_property_id, site_eui, energy_star_score,
                        created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, 'LEAD', ?, ?, ?, ?, ?)
                    """,
                    (
                        name, address, city, state, building_type, sqft,
                        pm_property_id, site_eui, energy_star_score,
                        timestamp, timestamp,
                    ),
                )
                created += 1
            else:
                conn.execute(
                    """
                    UPDATE buildings SET
                        address = COALESCE(?, address),
                        city = COALESCE(?, city),
                        state = COALESCE(?, state),
                        building_type = COALESCE(?, building_type),
                        sqft = COALESCE(?, sqft),
                        pm_property_id = COALESCE(?, pm_property_id),
                        site_eui = COALESCE(?, site_eui),
                        energy_star_score = COALESCE(?, energy_star_score),
                        updated_at = ?
                    WHERE id = ?
                    """,
                    (
                        address, city, state, building_type, sqft,
                        pm_property_id, site_eui, energy_star_score,
                        timestamp, existing["id"],
                    ),
                )
                updated += 1

    conn.commit()
    return (created, updated, skipped)
