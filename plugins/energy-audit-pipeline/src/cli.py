#!/usr/bin/env python3
"""Terminal CRM for the energy audit / retrofit pipeline plugin.

Everything here runs locally against a SQLite file under
~/atlas-data/energy-audit/ (override with ATLAS_ENERGY_DB) — no cloud
account, no subscription, consistent with Atlas Deck's "your hardware,
your data" approach.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import db  # noqa: E402
import financing  # noqa: E402
import incentives  # noqa: E402
import pm_import  # noqa: E402
import prospect_import  # noqa: E402

BUSINESS_NAME = os.environ.get("BUSINESS_NAME", "").strip() or "[YOUR BUSINESS NAME]"
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "").strip() or "[YOUR EMAIL]"
CONTACT_PHONE = os.environ.get("CONTACT_PHONE", "").strip() or "[YOUR PHONE]"

COMPANY_HINTS = ["inc", "corp", "llc", "trust", "group", "partners", "company",
                  "co.", "health", "realty", "lp", "ltd", "associates"]


def guess_first_name(owner: str, contact_name: str | None) -> str:
    """Best-effort first name for a salutation, from owner/contact text.

    Prospect rows store either a person as the owner (contact_name holds
    their title, e.g. "CEO at Example Corp") or a company as the owner
    (contact_name holds "Name (Title)"). Falls back to "there" when
    neither pattern is recognizable.
    """
    owner_lower = owner.lower()
    is_company = ("," in owner) or any(
        f" {hint}" in f" {owner_lower} " or owner_lower.endswith(hint) for hint in COMPANY_HINTS
    )
    if not is_company and owner.split():
        return owner.split()[0]
    if contact_name and "(" in contact_name:
        before = contact_name.split("(")[0].strip()
        if before:
            return before.split()[0]
    return "there"


def prompt(message: str, default: str | None = None) -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{message}{suffix}: ").strip()
    return value if value else (default or "")


def prompt_float(message: str) -> float | None:
    raw = input(f"{message}: ").strip()
    if not raw:
        return None
    try:
        return float(raw)
    except ValueError:
        print(f"'{raw}' is not a number — leaving blank.")
        return None


def prompt_int(message: str) -> int | None:
    value = prompt_float(message)
    return int(value) if value is not None else None


def pause() -> None:
    input("\nPress Enter to continue...")


def choose_building(conn) -> "db.sqlite3.Row | None":
    rows = conn.execute("SELECT id, name, stage FROM buildings ORDER BY updated_at DESC").fetchall()
    if not rows:
        print("No buildings in the pipeline yet. Add one first.")
        return None
    for row in rows:
        print(f"  {row['id']}. {row['name']} [{row['stage']}]")
    raw = input("Building ID: ").strip()
    if not raw.isdigit():
        print("Not a valid ID.")
        return None
    match = conn.execute("SELECT * FROM buildings WHERE id = ?", (int(raw),)).fetchone()
    if match is None:
        print("No building with that ID.")
    return match


def add_building(conn) -> None:
    print("\nAdd building / lead")
    name = prompt("Name")
    if not name:
        print("Name is required — cancelled.")
        return
    address = prompt("Address")
    city = prompt("City")
    state = prompt("State (2-letter)").upper()
    building_type = prompt("Building type (office, retail, multifamily, industrial, ...)")
    sqft = prompt_float("Square footage")
    contact_name = prompt("Contact name")
    contact_email = prompt("Contact email")
    contact_phone = prompt("Contact phone")

    timestamp = db.now()
    conn.execute(
        """
        INSERT INTO buildings (
            name, address, city, state, building_type, sqft,
            contact_name, contact_email, contact_phone,
            stage, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'LEAD', ?, ?)
        """,
        (name, address, city, state, building_type, sqft,
         contact_name, contact_email, contact_phone, timestamp, timestamp),
    )
    conn.commit()
    print(f"Added '{name}' to the pipeline as a LEAD.")


def list_pipeline(conn) -> None:
    print("\nPIPELINE")
    print("-" * 70)
    for stage in db.STAGES:
        rows = conn.execute(
            "SELECT id, name, city, state FROM buildings WHERE stage = ? ORDER BY updated_at DESC",
            (stage,),
        ).fetchall()
        print(f"\n{stage} ({len(rows)})")
        for row in rows:
            location = ", ".join(part for part in [row["city"], row["state"]] if part)
            print(f"  #{row['id']} {row['name']}" + (f" — {location}" if location else ""))


def update_stage(conn) -> None:
    print("\nUpdate stage")
    building = choose_building(conn)
    if building is None:
        return
    print("Stages: " + ", ".join(db.STAGES))
    new_stage = prompt("New stage", building["stage"]).upper()
    if new_stage not in db.STAGES:
        print(f"'{new_stage}' is not a valid stage.")
        return
    conn.execute(
        "UPDATE buildings SET stage = ?, updated_at = ? WHERE id = ?",
        (new_stage, db.now(), building["id"]),
    )
    conn.commit()
    print(f"'{building['name']}' moved to {new_stage}.")


def add_measure(conn) -> None:
    print("\nAdd measure")
    building = choose_building(conn)
    if building is None:
        return
    name = prompt("Measure name (e.g. LED lighting retrofit)")
    if not name:
        print("Name is required — cancelled.")
        return
    category = prompt("Category (lighting, hvac, envelope, controls, ...)")
    cost = prompt_float("Installed cost ($)")
    annual_savings = prompt_float("Estimated annual savings ($)")
    if cost is None or annual_savings is None:
        print("Cost and annual savings are required — cancelled.")
        return
    conn.execute(
        """
        INSERT INTO measures (building_id, name, category, cost, annual_savings, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (building["id"], name, category, cost, annual_savings, db.now()),
    )
    conn.commit()

    payback = financing.simple_payback_years(cost, annual_savings)
    payback_text = f"{payback:.1f} years" if payback is not None else "n/a (no positive savings)"
    print(f"Added '{name}' — simple payback {payback_text}.")


def view_building(conn) -> None:
    print("\nBuilding detail")
    building = choose_building(conn)
    if building is None:
        return

    print(f"\n{building['name']} [{building['stage']}]")
    print(f"  {building['address'] or ''} {building['city'] or ''} {building['state'] or ''}".strip())
    print(f"  Type: {building['building_type'] or 'n/a'}  Sqft: {building['sqft'] or 'n/a'}")
    print(f"  Contact: {building['contact_name'] or 'n/a'} "
          f"{building['contact_email'] or ''} {building['contact_phone'] or ''}".rstrip())
    print(f"  Site EUI: {building['site_eui'] or 'n/a'}  "
          f"ENERGY STAR score: {building['energy_star_score'] or 'n/a'}  "
          f"Asset score: {building['asset_score'] or 'n/a'}")

    measures = conn.execute(
        "SELECT * FROM measures WHERE building_id = ? ORDER BY created_at", (building["id"],)
    ).fetchall()
    if measures:
        print("\n  Measures:")
        total_cost = total_savings = 0.0
        for measure in measures:
            payback = financing.simple_payback_years(measure["cost"], measure["annual_savings"])
            payback_text = f"{payback:.1f}y" if payback is not None else "n/a"
            print(f"    - {measure['name']} ({measure['category'] or 'uncategorized'}): "
                  f"${measure['cost']:,.0f} cost, ${measure['annual_savings']:,.0f}/yr savings, "
                  f"payback {payback_text}")
            total_cost += measure["cost"]
            total_savings += measure["annual_savings"]
        combined_payback = financing.simple_payback_years(total_cost, total_savings)
        combined_text = f"{combined_payback:.1f} years" if combined_payback is not None else "n/a"
        print(f"    Package total: ${total_cost:,.0f} cost, ${total_savings:,.0f}/yr savings, "
              f"blended payback {combined_text}")
    else:
        print("\n  No measures added yet.")

    if building["notes"]:
        print("\n  Notes:")
        for line in building["notes"].splitlines():
            print(f"    {line}")


def match_incentives_for_building(conn) -> None:
    print("\nMatch incentives")
    building = choose_building(conn)
    if building is None:
        return
    keyword = prompt("Measure keyword to filter on (blank for any)")

    all_incentives = incentives.load_incentives()
    if not all_incentives:
        print(f"No incentives file found at {incentives.incentives_path()}.")
        return

    matches = incentives.match(all_incentives, building["state"], building["building_type"], keyword)
    if not matches:
        print("No matches in the local incentives file for this building/keyword.")
        print("Check dsireusa.org for current state/utility programs and add them to "
              f"{incentives.incentives_path()}.")
        return

    print(f"\n{len(matches)} match(es):")
    for entry in matches:
        print(f"\n  {entry['name']} ({entry.get('level', 'n/a')})")
        print(f"    {entry.get('summary', '')}")
        if entry.get("verify"):
            print(f"    VERIFY BEFORE QUOTING: {entry['verify']}")


def financing_calculator() -> None:
    print("\nFinancing calculator")
    cost = prompt_float("Project cost ($)")
    annual_savings = prompt_float("Estimated annual savings ($)")
    if cost is None or annual_savings is None:
        print("Cost and annual savings are required.")
        return

    payback = financing.simple_payback_years(cost, annual_savings)
    print(f"Simple payback: {payback:.1f} years" if payback is not None else "Simple payback: n/a")

    years = prompt_float("Evaluation period for ROI (years)") or 10
    roi = financing.simple_roi_percent(cost, annual_savings, years)
    print(f"Simple ROI over {years:.0f} years: {roi:.0f}%" if roi is not None else "ROI: n/a")

    finance = prompt("Model a loan for this project? (y/N)").lower()
    if finance == "y":
        rate = prompt_float("Annual interest rate (%)") or 0.0
        term = prompt_float("Loan term (years)") or 10.0
        payment = financing.monthly_loan_payment(cost, rate, term)
        print(f"Estimated monthly payment: ${payment:,.2f}")
        monthly_savings = annual_savings / 12
        cash_flow = monthly_savings - payment
        sign = "positive" if cash_flow >= 0 else "negative"
        print(f"Monthly savings ${monthly_savings:,.2f} vs. payment ${payment:,.2f}: "
              f"{sign} cash flow of ${abs(cash_flow):,.2f}/month")


def import_pm_csv(conn) -> None:
    print("\nImport ENERGY STAR Portfolio Manager export")
    print("In Portfolio Manager: My Portfolio -> Download to Spreadsheet -> CSV.")
    path = prompt("Path to CSV file")
    if not path:
        return
    path = os.path.expanduser(path)
    if not os.path.isfile(path):
        print(f"File not found: {path}")
        return
    try:
        created, updated, skipped = pm_import.import_csv(path, conn)
    except ValueError as exc:
        print(f"Import failed: {exc}")
        return
    print(f"Import complete: {created} created, {updated} updated, {skipped} skipped (no name).")


def import_prospect_csv(conn) -> None:
    print("\nImport prospect list (Owner / Portfolio / Contact)")
    print("Expected columns: Owner, Contact / Title, Properties In Portfolio, "
          "Portfolio Assessed Value, Last Acquisition Date.")
    path = prompt("Path to CSV file")
    if not path:
        return
    path = os.path.expanduser(path)
    if not os.path.isfile(path):
        print(f"File not found: {path}")
        return
    try:
        created, skipped = prospect_import.import_csv(path, conn)
    except ValueError as exc:
        print(f"Import failed: {exc}")
        return
    print(f"Import complete: {created} leads created, {skipped} skipped (no owner name).")
    print("Each lead's score, tier, and recommended opening are in its notes — see 'View building detail'.")


def top_priority_leads(conn) -> None:
    print("\nTOP PRIORITY LEADS (A+/A tier prospects)")
    print("-" * 42)
    rows = conn.execute(
        "SELECT * FROM buildings WHERE notes LIKE 'Prospect import%' "
        "AND stage = 'LEAD' ORDER BY updated_at DESC"
    ).fetchall()

    ranked = []
    for row in rows:
        first_line = (row["notes"] or "").splitlines()[0] if row["notes"] else ""
        if "Tier A+" in first_line or "Tier A " in first_line or first_line.endswith("Tier A"):
            ranked.append(row)

    if not ranked:
        print("No A/A+ tier prospects yet — import a prospect list first.")
        return

    for row in ranked:
        print(f"\n#{row['id']} {row['name']}" + (f" — {row['contact_name']}" if row["contact_name"] else ""))
        for line in (row["notes"] or "").splitlines():
            print(f"    {line}")


def draft_email(conn) -> None:
    print("\nDraft outreach email")
    building = choose_building(conn)
    if building is None:
        return

    opening = None
    for line in (building["notes"] or "").splitlines():
        if line.strip().startswith("Recommended opening:"):
            opening = line.split(":", 1)[1].strip()
            break
    if opening is None:
        opening = prompt("No stored recommended opening — type one line to use")
        if not opening:
            print("Cancelled — nothing to draft without an opening line.")
            return

    first_name = guess_first_name(building["name"], building["contact_name"])
    properties_hint = ""
    for line in (building["notes"] or "").splitlines():
        if line.strip().startswith("Properties in portfolio:"):
            properties_hint = line.split(":", 1)[1].strip()
            break
    subject_suffix = f"the {properties_hint}-property portfolio" if properties_hint else "your portfolio"

    print(f"\nSubject: Quick question about {subject_suffix}")
    print()
    print(f"Hi {first_name},")
    print()
    print(opening)
    print()
    print("If it's useful, I can send a short one-page overview, or we could grab "
          "15 minutes this week — whichever's easier.")
    print()
    print("Best,")
    print("[YOUR NAME]")
    print(BUSINESS_NAME)
    print(f"{CONTACT_EMAIL} | {CONTACT_PHONE}")


MENU = [
    ("List pipeline", list_pipeline),
    ("Top priority leads (A/A+ tier)", top_priority_leads),
    ("Draft outreach email for a lead", draft_email),
    ("Add building / lead", add_building),
    ("View building detail", view_building),
    ("Update stage", update_stage),
    ("Add measure to a building", add_measure),
    ("Match incentives for a building", match_incentives_for_building),
    ("Financing calculator (standalone)", lambda _conn: financing_calculator()),
    ("Import Portfolio Manager CSV", import_pm_csv),
    ("Import prospect list (Owner / Portfolio)", import_prospect_csv),
]


def main() -> None:
    conn = db.connect()
    while True:
        print("\nATLAS ENERGY AUDIT PIPELINE")
        print("-" * 27)
        for idx, (label, _fn) in enumerate(MENU, start=1):
            print(f"{idx}. {label}")
        print("0. Exit")

        choice = input("\nChoose: ").strip()
        if choice == "0":
            break
        if not choice.isdigit() or not (1 <= int(choice) <= len(MENU)):
            print("Invalid option.")
            continue

        _label, action = MENU[int(choice) - 1]
        try:
            action(conn)
        except KeyboardInterrupt:
            print("\nCancelled.")
        except Exception as exc:  # noqa: BLE001 - keep the CLI alive on any single-action failure
            print(f"Error: {exc}")
        pause()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print()
