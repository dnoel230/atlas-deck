# Energy Audit Pipeline

A local retrofit-audit pipeline for Atlas Deck: track buildings through a
sales/audit pipeline, match them against incentive programs, run basic
financing math, and pull property data from ENERGY STAR Portfolio Manager
— all stored on your own hardware, no subscription required.

This plugin exists to be the "connective layer" between several tools that
each do one piece of this well but don't talk to each other:

| Need | Where it comes from |
|---|---|
| Standardized audit reports | [DOE Audit Template](https://buildingenergyscore.energy.gov) / ASHRAE Standard 211 |
| Building scoring | [ASHRAE Building EQ](https://www.buildingeq.ashrae.org) |
| Consumption benchmarking, EUI, 1-100 score | [ENERGY STAR Portfolio Manager](https://portfoliomanager.energystar.gov) |
| Equipment/asset condition scoring | [DOE Asset Score](https://buildingenergyscore.energy.gov) |
| Field data collection | e.g. EMAT Field Auditor |
| **Incentive matching, financing, pipeline tracking** | **this plugin** |

None of the tools above are reimplemented here — this plugin assumes you
still use them for audits and scoring, and gives you a place to track leads,
attach measures and costs, match incentives, and run payback math on top of
their output.

## Setup

No credentials are required to get started:

```bash
plugins/energy-audit-pipeline/run.sh
```

Data is stored in a local SQLite database, by default at
`~/atlas-data/energy-audit/pipeline.db` (outside the git repo, so it's
never at risk of being committed). Override the location, or point at your
own incentives file, by copying `config.env.example` to `config.env` in
this folder.

## Portfolio Manager data

Portfolio Manager has a web services API, but it requires setting up a
separate web services account and OAuth-style credentials that are easy to
misconfigure without a live account to test against. Instead, this plugin
imports the CSV export every Portfolio Manager account already has built
in:

1. In Portfolio Manager: **My Portfolio -> Download to Spreadsheet -> CSV**.
2. In the plugin menu: **Import Portfolio Manager CSV**, then give it the
   file path.

Properties are matched by Property ID when present, otherwise by name +
address, so re-importing an updated export is safe — it updates existing
buildings rather than duplicating them.

DOE Asset Score results don't have an equivalent bulk export, so the asset
score is a manual field on each building for now (set it from the
building-detail view once you add an "edit" flow, or directly in the
database).

## Incentives

`data/incentives.sample.json` ships with three example entries (a federal
tax deduction, a USDA program, and a pointer to
[DSIRE](https://www.dsireusa.org)) — deliberately not a full incentive
database, since program terms and dollar amounts change often enough that
hard-coding them here would go stale. Each entry carries a `verify` note
that's always printed alongside a match as a reminder to confirm current
terms before quoting a client.

To build out real coverage: look up what's live for a state/utility on
DSIRE, add it as a new entry in your own incentives file (see
`config.env.example` for pointing the plugin at it), following the same
shape — `state`, `building_types`, `measure_keywords`, `summary`, `verify`.

## What this doesn't do

- No live API calls to Portfolio Manager, Asset Score, or ASHRAE Building
  EQ — data comes in via CSV import or manual entry.
- No discounted cash flow / tax modeling — the financing calculator is
  simple payback, simple ROI, and a loan payment estimate only.
- No multi-user sync — it's a single local SQLite file, matching Atlas
  Deck's "your hardware, your data" model. If you need shared access
  across a team, point `ATLAS_ENERGY_DB` at a file on shared storage.
