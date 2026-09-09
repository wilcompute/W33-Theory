"""Regression gates for the 2026-09-09 crypto/network/Marcelis execution pass."""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(relpath: str, name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relpath)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_contextual_decryption_global_section_boundary():
    m = load("analysis/w33_contextual_decryption_obstruction.py", "w33_contextual_decryption")
    row = m.verify()
    assert row["status"] == "PASS"
    assert row["control_W2"]["global_keys"] == 6
    assert row["W33"]["global_keys"] == 0
    assert row["contextuality_quantities"]["abramsky_barbosa_contextual_fraction"] == 1
    assert row["contextuality_quantities"]["ks_satisfiability_defect"] == "1/10"
    # Negative result is part of the theorem firewall: this weak linearization
    # is soluble and therefore must not be sold as the contextuality witness.
    assert row["linearized_cohomology_probe"]["F2"]["solvable"] is True
    assert row["linearized_cohomology_probe"]["F3"]["solvable"] is True


def test_support_min_entropy_q3():
    m = load("analysis/w33_support_min_entropy.py", "w33_support_min_entropy")
    row = m.exact_row(3)
    assert row["optimal_classical_guessing_probability"] == "16/81"
    assert math.isclose(row["conditional_min_entropy_bits"], math.log2(81 / 16), rel_tol=0, abs_tol=1e-12)
    assert math.isclose(row["conditional_shannon_entropy_bits"], 8 / 3, rel_tol=0, abs_tol=1e-12)
    assert m.exact_row(2)["conditional_min_entropy_bits"] == 0


def test_witting_card_inverse_analyzer_compiler():
    m = load("analysis/w33_witting_card_single_photon_protocol.py", "w33_witting_card")
    rays = m.rays40()
    bases, _ = m.tetrads(rays)
    assert len(rays) == 40
    assert len(bases) == 40
    memberships = [0] * 40
    families = {}
    for T in bases:
        U = m.analyzer(rays, T)
        profile = [m.support_weight(rays[r]) for r in T]
        f = m.family(profile)
        families[f] = families.get(f, 0) + 1
        for slot, ray in enumerate(T):
            memberships[ray] += 1
            prepared = U.conj().T[:, slot]
            assert abs(abs(prepared.conj() @ rays[ray]) - 1) < 1e-10
    assert set(memberships) == {4}
    assert families == {
        "COMPUTATIONAL_DIRECT_RAILS": 1,
        "ONE_DIRECT_RAIL_PLUS_COMPLEMENT_TRITTER": 12,
        "FOUR_THREE_RAIL_WITTING_ROWS": 27,
    }


def test_marcelis_multichart_firewalls():
    m = load("analysis/w33_marcelis_multichart_atlas.py", "w33_marcelis_atlas")
    _, lines = m.w33()
    charts, web, trans = m.chart_web(lines)
    assert len(charts) == 540
    assert trans == {4: 540}
    assert {len(x) for x in web} == {6}
    assert m.edge_count(web) == 1620
    assert m.triangle_count(web) == 0
    d2 = m.distance_two_graph(web)
    assert {len(x) for x in d2} == {30}
    assert len(m.max_clique_exact(d2)) == 6
    assert m.find_trace_projective_counterexample() is not None
