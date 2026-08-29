"""SQLite storage for the energy audit pipeline plugin.

Data lives outside the git repo by default (see db_path()) so that
building names, contacts, and pricing never end up committed to a
public repository.
"""

from __future__ import annotations

import os
import sqlite3
from datetime import datetime, timezone

STAGES = [
    "LEAD",
    "AUDIT_SCHEDULED",
    "AUDIT_COMPLETE",
    "PROPOSAL_SENT",
    "WON",
    "LOST",
]

SCHEMA = """
CREATE TABLE IF NOT EXISTS buildings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT,
    city TEXT,
    state TEXT,
    building_type TEXT,
    sqft REAL,
    contact_name TEXT,
    contact_email TEXT,
    contact_phone TEXT,
    stage TEXT NOT NULL DEFAULT 'LEAD',
    pm_property_id TEXT,
    site_eui REAL,
    energy_star_score INTEGER,
    asset_score INTEGER,
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS measures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    building_id INTEGER NOT NULL REFERENCES buildings(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    category TEXT,
    cost REAL NOT NULL,
    annual_savings REAL NOT NULL,
    created_at TEXT NOT NULL
);
"""


def db_path() -> str:
    override = os.environ.get("ATLAS_ENERGY_DB")
    if override:
        return override
    return os.path.expanduser("~/atlas-data/energy-audit/pipeline.db")


def connect() -> sqlite3.Connection:
    path = db_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    return conn


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
