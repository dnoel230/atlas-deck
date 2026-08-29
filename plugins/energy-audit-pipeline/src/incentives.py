"""Rules-based incentive matching against a local, editable JSON file.

There is no single free, reliable API for state/utility incentives, and
program terms change often enough that hard-coding dollar amounts would
go stale immediately. This module matches against a local incentives
file the user maintains (starting from data/incentives.sample.json) and
always prints the entry's "verify" note so stale data doesn't get quoted
to a client as fact.
"""

from __future__ import annotations

import json
import os

DEFAULT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "incentives.sample.json",
)


def incentives_path() -> str:
    return os.environ.get("ATLAS_ENERGY_INCENTIVES", DEFAULT_PATH)


def load_incentives() -> list[dict]:
    path = incentives_path()
    if not os.path.isfile(path):
        return []
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def match(
    incentives: list[dict],
    state: str | None,
    building_type: str | None,
    measure_keyword: str | None,
) -> list[dict]:
    state_norm = (state or "").strip().upper()
    type_norm = (building_type or "").strip().lower()
    keyword_norm = (measure_keyword or "").strip().lower()

    results = []
    for entry in incentives:
        entry_states = {s.strip().upper() for s in entry.get("state", "ALL").split(",")}
        if "ALL" not in entry_states and state_norm and state_norm not in entry_states:
            continue

        entry_types = [t.lower() for t in entry.get("building_types", ["ALL"])]
        if "all" not in entry_types and type_norm and type_norm not in entry_types:
            continue

        entry_keywords = [k.lower() for k in entry.get("measure_keywords", ["ALL"])]
        if (
            "all" not in entry_keywords
            and keyword_norm
            and not any(keyword_norm in k or k in keyword_norm for k in entry_keywords)
        ):
            continue

        results.append(entry)
    return results
