from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verify_dcclxxiv_closure_transfer_resolvent_equivalence_bridge import (  # noqa: E402
    OUT_PATH,
    build_bridge,
    write_bridge,
)


def _frac(cell: dict[str, int]) -> Fraction:
    return Fraction(cell["numerator"], cell["denominator"])


def test_summary_values() -> None:
    payload = build_bridge()
    summary = payload["summary"]

    assert summary["causal_class_count"] == 6
    assert (summary["generator_weight_num"], summary["generator_weight_den"]) == (1, 2)
    assert summary["nilpotent_index"] == 6
    assert summary["maximal_transfer_denominator"] == 32
    assert summary["all_identities_hold"] is True


def test_transfer_power_rule_matches_semigroup_entries() -> None:
    payload = build_bridge()

    assert all(
        row["canonical_matches_direct_power"] and row["direct_power_matches_transfer_rule"]
        for row in payload["transfer_power_checks"]
    )

    rows = {(row["from"], row["to"]): row for row in payload["entry_rows"]}
    assert _frac(rows[(0, 0)]["semigroup_entry"]) == Fraction(1, 1)
    assert _frac(rows[(0, 1)]["power_entry"]) == Fraction(1, 2)
    assert _frac(rows[(0, 5)]["power_entry"]) == Fraction(1, 32)
    assert _frac(rows[(0, 5)]["resolvent_entry"]) == Fraction(1, 32)


def test_all_equivalence_identities_hold() -> None:
    payload = build_bridge()
    identities = payload["identities"]

    assert identities["generator_is_half_shift"] is True
    assert identities["all_generator_powers_match_transfer_rule"] is True
    assert identities["semigroup_entries_equal_power_entries"] is True
    assert identities["semigroup_entries_equal_resolvent_entries"] is True
    assert identities["resolvent_is_sum_of_transfer_powers"] is True
    assert identities["nilpotence_terminates_at_six"] is True
    assert all(identities.values())


def test_theorem_boundary_and_public_index_exposure() -> None:
    payload = build_bridge()
    index = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    assert "Closure Transfer-Resolvent Equivalence" in payload["theorem"]
    assert "does not add a continuum Hamiltonian" in payload["honesty_boundary"]
    assert "Closure Transfer-Resolvent Equivalence" in index
    assert "K=(I-G)<sup>-1</sup>" in index


def test_write_and_reload() -> None:
    out = write_bridge()
    assert out == OUT_PATH

    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["summary"]["all_identities_hold"] is True
    assert data["identities"]["maximal_transfer_is_one_over_32"] is True
