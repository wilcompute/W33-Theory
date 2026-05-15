from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.PART_CCCCCXC_tomotope_cover_convergence_ledger import build


def test_claim_status_partition_is_explicit() -> None:
    ledger = build()
    statuses = {claim.status for claim in ledger.claims}
    assert statuses == {"exact_verified", "conditional_verified", "open_frontier"}


def test_cover_tower_continuity_claim_is_conditional() -> None:
    ledger = build()
    claim = next(c for c in ledger.claims if c.id == "cover_tower_continuity_requires_external_or_convergence_lift")
    assert claim.status == "conditional_verified"
    assert len(claim.assumptions) >= 1


def test_intrinsic_4d_from_cover_only_is_open_frontier() -> None:
    ledger = build()
    claim = next(c for c in ledger.claims if c.id == "intrinsic_4d_from_discrete_covers_only")
    assert claim.status == "open_frontier"


def test_ledger_checks_pass() -> None:
    ledger = build()
    assert all(ledger.checks.values())
