# BT1905–BT1907 Execution Summary

This packet executes the three prioritized architecture moves:

1. **Holonet Demonstrator Protocol v1** — `holonet_demonstrator_protocol_v1.tex`
2. **Public Theorem/Audit Ledger** — `docs/holonet_theorem_ledger.md`
3. **Photonic Holonet Claim-Tier Refactor** — `analysis/BT1907_photonic_holonet_claim_tier_refactor.md`

`HOLONET.md` now links all three as first-class public reader paths: run it, audit it, falsify it, grade it.

## BT1905 — Demonstrator protocol

Added `holonet_demonstrator_protocol_v1.tex`.

Purpose: isolate the first physical falsifier for the Holonet substrate: the Witting/Kochen–Specker contextuality test on the forty contexts of `W(3,3)`.

Core prediction:

```text
noncontextual: S <= 36
quantum target: S = 40
contextual fraction: (40 - 36) / 40 = 1/10
```

The protocol records:

- claim under test;
- minimal optical apparatus;
- experimental schedule;
- raw-shot JSONL schema;
- validator/estimator command path;
- decision rule;
- controls and failure modes;
- certification deliverables.

Boundary: this tests the substrate's contextual magic fuel, not the full physics program or a full fault-tolerant photonic computer.

## BT1906 — Public theorem ledger

Added `docs/holonet_theorem_ledger.md`.

Purpose: make the architecture reviewable as a claim-to-witness table.  Each row gives:

- claim;
- tier: exact, simulation, physical, corpus identification, or frontier;
- witness / command;
- output artifact;
- pass condition;
- boundary.

This makes `holonet audit` the public theorem scoreboard rather than an internal developer command.

## BT1907 — Claim-tier refactor

Added `analysis/BT1907_photonic_holonet_claim_tier_refactor.md`.

Purpose: split the full Photonic Holonet manuscript into claim classes so exact architecture is not blurred with ambitious physics identifications.

The five tiers are:

- **E** exact / theorem / exhaustive computation;
- **S** simulation / Monte Carlo / finite model;
- **P** physical demonstrator pending or completed;
- **C** corpus identification / postdiction / arithmetic match;
- **F** frontier conjecture or application.

The refactor maps the grand manuscript regions into tiers and gives rewrite rules for `photonic_holonet.tex`.

## Landing-doc integration

Updated `HOLONET.md` with public reader paths:

- **Run it:** `holonet verify`, `holonet audit`, `holonet bench`.
- **Audit it:** `docs/holonet_theorem_ledger.md`.
- **Falsify it:** `holonet_demonstrator_protocol_v1.tex`.
- **Grade it:** `analysis/BT1907_photonic_holonet_claim_tier_refactor.md`.

## Honest note

A direct `holonet_claim_tiers.tex` write was attempted but blocked by the connector safety layer.  The refactor landed as a Markdown analysis artifact instead, and the landing document links it as the claim-tier spine.
