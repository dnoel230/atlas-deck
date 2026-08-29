"""Simple financing math for proposed retrofit measures.

Deliberately basic (no discount-rate NPV, no tax modeling) — good enough
for a first-pass conversation with a building owner, not a substitute
for a real financial model.
"""

from __future__ import annotations


def simple_payback_years(cost: float, annual_savings: float) -> float | None:
    if annual_savings <= 0:
        return None
    return cost / annual_savings


def simple_roi_percent(cost: float, annual_savings: float, years: float) -> float | None:
    if cost <= 0:
        return None
    total_savings = annual_savings * years
    return ((total_savings - cost) / cost) * 100


def monthly_loan_payment(principal: float, annual_rate_percent: float, years: float) -> float:
    n = years * 12
    if n <= 0:
        return 0.0
    if annual_rate_percent == 0:
        return principal / n
    r = (annual_rate_percent / 100) / 12
    return principal * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
