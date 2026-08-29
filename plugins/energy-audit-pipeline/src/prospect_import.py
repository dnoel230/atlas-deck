"""Import a raw prospect list (owner/portfolio data) as scored leads.

Unlike pm_import.py (which imports individual buildings from Portfolio
Manager), this is for portfolio-owner prospecting exports — e.g. a
commercial real estate contact list with columns like:

    Owner, Contact / Title, Properties In Portfolio,
    Portfolio Assessed Value, Last Acquisition Date

Each row is scored for energy-audit fit with energy_audit_scoring.py and
inserted as a LEAD. The score/tier/recommended opening are stored in the
notes field (kept out of dedicated columns since this scoring model is
specific to portfolio-prospecting, not every building record).
"""

from __future__ import annotations

import csv
import sqlite3
from datetime import date

from db import now
from energy_audit_scoring import recommended_opening, score_prospect

HEADER_ALIASES: dict[str, list[str]] = {
    "owner": ["owner"],
    "contact_title": ["contact / title", "contact/title", "contact"],
    "properties": ["properties in portfolio"],
    "assessed_value": ["portfolio assessed value", "assessed value"],
    "last_acquisition": ["last acquisition date", "last acquisition"],
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
        return float(str(value).replace(",", "").replace("$", "").strip())
    except (TypeError, ValueError):
        return None


def import_csv(path: str, conn: sqlite3.Connection, as_of: date | None = None) -> tuple[int, int]:
    """Import a raw prospect CSV, scoring each row. Returns (created, skipped)."""
    created = skipped = 0

    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames:
            return (0, 0)
        columns = detect_columns(reader.fieldnames)

        if "owner" not in columns:
            raise ValueError(
                "Could not find an 'Owner' column in this CSV. "
                "Expected headers like Owner, Contact / Title, Properties In Portfolio, "
                "Portfolio Assessed Value, Last Acquisition Date."
            )

        for row in reader:
            owner = (row.get(columns["owner"]) or "").strip()
            if not owner:
                skipped += 1
                continue

            contact_title = row.get(columns.get("contact_title", ""), "").strip() or None
            properties = _to_float(row.get(columns.get("properties", ""), ""))
            assessed_value = _to_float(row.get(columns.get("assessed_value", ""), ""))
            last_acquisition = row.get(columns.get("last_acquisition", ""), "").strip() or None

            result = score_prospect(properties, assessed_value, last_acquisition, contact_title, as_of)
            opening = recommended_opening(result["tier"], properties)

            notes_lines = [
                f"Prospect import — Tier {result['tier']} (score {result['total_score']}/100)",
                f"  Portfolio {result['portfolio_score']}/30, Value {result['value_score']}/20, "
                f"Recency {result['recency_score']}/25, Access {result['access_score']}/25",
                f"Recommended opening: {opening}",
            ]
            if properties is not None:
                notes_lines.append(f"Properties in portfolio: {int(properties)}")
            if assessed_value is not None:
                notes_lines.append(f"Portfolio assessed value: ${assessed_value:,.0f}")
            if last_acquisition:
                notes_lines.append(f"Last acquisition: {last_acquisition}")

            timestamp = now()
            conn.execute(
                """
                INSERT INTO buildings (
                    name, building_type, contact_name, stage, notes,
                    created_at, updated_at
                ) VALUES (?, 'portfolio owner', ?, 'LEAD', ?, ?, ?)
                """,
                (owner, contact_title, "\n".join(notes_lines), timestamp, timestamp),
            )
            created += 1

    conn.commit()
    return (created, skipped)
