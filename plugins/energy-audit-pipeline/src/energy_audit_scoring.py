"""Energy-audit-specific lead scoring for portfolio/owner prospect lists.

Scores a prospect (building owner or portfolio manager) on how promising
they are for an energy audit/retrofit pitch, using four transparent,
independently documented factors that sum to 100:

- Portfolio size (0-30): more properties means more buildings to audit.
- Portfolio value (0-20): a proxy for capital capacity to fund retrofits.
- Acquisition recency (0-25): a recent acquisition often means capital
  planning/renovation budgets are already being discussed.
- Contact seniority (0-25): a decision-maker is far more likely to take
  a cold energy-audit pitch seriously than a junior/administrative title.

This intentionally does not reuse any scoring model built for a
different pitch (e.g. roofing/IT/tax-and-wealth cross-sell) — the
factors above are chosen to be relevant to selling energy audits
specifically.
"""

from __future__ import annotations

from datetime import date, datetime

SENIOR_TITLES = ["ceo", "president", "owner", "founder", "principal"]
EXECUTIVE_TITLES = ["svp", "evp", "cfo", "coo", "chief"]
VP_TITLES = ["vp", "vice president"]
DIRECTOR_TITLES = ["director"]
MANAGER_TITLES = ["manager"]
JUNIOR_TITLES = ["coordinator", "assistant", "analyst", "specialist", "designer"]

TIERS = [
    (80, "A+"),
    (65, "A"),
    (50, "B"),
    (35, "C"),
    (0, "D"),
]


def title_access_score(title: str | None) -> int:
    text = (title or "").lower()
    if any(t in text for t in SENIOR_TITLES):
        return 25
    if any(t in text for t in EXECUTIVE_TITLES):
        return 21
    if any(t in text for t in VP_TITLES):
        return 17
    if any(t in text for t in DIRECTOR_TITLES):
        return 14
    if any(t in text for t in MANAGER_TITLES):
        return 9
    if any(t in text for t in JUNIOR_TITLES):
        return 5
    return 8  # unknown/unrecognized title — neutral baseline


def portfolio_score(properties_in_portfolio: float | None) -> float:
    value = properties_in_portfolio or 0
    return min(value / 100 * 30, 30)


def value_score(portfolio_assessed_value: float | None) -> float:
    value = portfolio_assessed_value or 0
    return min(value / 1_000_000_000 * 20, 20)


def months_since(last_acquisition, as_of: date) -> float | None:
    if last_acquisition is None:
        return None
    if isinstance(last_acquisition, datetime):
        last_acquisition = last_acquisition.date()
    elif isinstance(last_acquisition, str):
        try:
            last_acquisition = datetime.fromisoformat(last_acquisition).date()
        except ValueError:
            return None
    delta_days = (as_of - last_acquisition).days
    return delta_days / 30.4375


def recency_score(last_acquisition, as_of: date) -> float:
    months = months_since(last_acquisition, as_of)
    if months is None:
        return 5
    if months <= 6:
        return 25
    if months <= 12:
        return 18
    if months <= 24:
        return 10
    return 5


def tier_for(total: float) -> str:
    for threshold, label in TIERS:
        if total >= threshold:
            return label
    return "D"


def score_prospect(
    properties_in_portfolio: float | None,
    portfolio_assessed_value: float | None,
    last_acquisition,
    contact_title: str | None,
    as_of: date | None = None,
) -> dict:
    as_of = as_of or date.today()
    p_score = portfolio_score(properties_in_portfolio)
    v_score = value_score(portfolio_assessed_value)
    r_score = recency_score(last_acquisition, as_of)
    a_score = title_access_score(contact_title)
    total = p_score + v_score + r_score + a_score
    tier = tier_for(total)
    return {
        "portfolio_score": round(p_score, 1),
        "value_score": round(v_score, 1),
        "recency_score": round(r_score, 1),
        "access_score": round(a_score, 1),
        "total_score": round(total, 1),
        "tier": tier,
    }


def recommended_opening(tier: str, properties_in_portfolio: float | None) -> str:
    properties = int(properties_in_portfolio) if properties_in_portfolio else "your"
    if tier in ("A+", "A"):
        return (
            f"Given the {properties}-property portfolio and recent acquisition activity, "
            "it's worth a 15-minute portfolio-level energy risk conversation — most owners "
            "this size are leaving meaningful utility spend on the table across their portfolio."
        )
    if tier == "B":
        return (
            f"A quick energy benchmarking pass across the largest properties in the "
            f"{properties}-property portfolio often surfaces near-term utility savings, so "
            "it's worth sending a short overview."
        )
    return (
        "Low-touch intro email: flag ENERGY STAR benchmarking / audit services and let "
        "them self-select if there's a capital planning window coming up."
    )
