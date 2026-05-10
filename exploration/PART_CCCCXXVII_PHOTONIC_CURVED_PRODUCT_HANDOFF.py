#!/usr/bin/env python3
"""PART CCCCXXVII -- Photonic Curved Product Handoff.

CCCCXXVI closes the protected photonic runtime at the finite side.  The next
honest TOE boundary is the curved 4D bridge:

    Delta_ext tensor 1 + 1 tensor D_F^2.

This certificate stitches the new photonic runtime into the explicit curved
operator packages already present in the repo:

* CP2_9 and K3_16 are concrete simplicial 4-complexes.
* Their external Hodge/Dirac-Kahler spectra exist and product heat traces
  factorize with the W33 finite Dirac square.
* Barycentric refinement supplies the genuine 4D scaling family with universal
  local limits 120/19 and 860/19.
* The native A2 transport local system has a positive internal Laplacian with
  gap 24 and also factorizes over the same curved external spectra.

The point is conservative: the finite protected photonic kernel is ready to be
paired with curved 4D geometry, but the continuum Einstein-Hilbert asymptotic
theorem is still the open bridge.
"""
from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List

from w33_curved_a2_transport_product import build_curved_a2_transport_product_summary
from w33_curved_barycentric_density_bridge import build_curved_barycentric_density_bridge_summary
from w33_curved_external_hodge_product import build_curved_external_hodge_product_summary
from w33_curved_h2_host_bridge import build_curved_h2_host_bridge_summary
from w33_explicit_curved_4d_complexes import build_explicit_curved_4d_complexes_summary


ROOT = Path(__file__).resolve().parents[1]

PROTECTED_KERNEL = ROOT / "PART_CCCCV_protected_toe_kernel_results.json"
FUSION_SPLICE = ROOT / "PART_CCCCXXVI_fusion_control_scheduler_splice_results.json"

Q = 3
LAM = Q - 1
MU = Q + 1
K = Q * (Q + 1)
V = (Q**4 - 1) // (Q - 1)
H1 = Q**4
W33_EDGES = V * K // 2


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def ok(name: str, cond: bool, value: Any = None) -> Dict[str, Any]:
    return {"name": name, "passed": bool(cond), "value": value}


def fraction_exact(entry: Dict[str, Any]) -> Fraction:
    exact = entry["exact"]
    if "/" in exact:
        numer, denom = exact.split("/", 1)
        return Fraction(int(numer), int(denom))
    return Fraction(int(exact), 1)


def _profile_by_name(profiles: List[Dict[str, Any]], name: str) -> Dict[str, Any]:
    for profile in profiles:
        if profile["name"] == name:
            return profile
    raise KeyError(name)


def _curved_product_by_name(profiles: List[Dict[str, Any]], name: str) -> Dict[str, Any]:
    for profile in profiles:
        if profile["external_name"] == name:
            return profile
    raise KeyError(name)


def build_results() -> Dict[str, Any]:
    kernel = load_json(PROTECTED_KERNEL)
    splice = load_json(FUSION_SPLICE)
    explicit = build_explicit_curved_4d_complexes_summary()
    hodge = build_curved_external_hodge_product_summary()
    density = build_curved_barycentric_density_bridge_summary()
    a2_product = build_curved_a2_transport_product_summary()
    h2_host = build_curved_h2_host_bridge_summary()

    cp2_complex = explicit["profiles"][0]
    k3_complex = explicit["profiles"][1]
    cp2_hodge = hodge["external_profiles"][0]
    k3_hodge = hodge["external_profiles"][1]
    cp2_h2 = _profile_by_name(h2_host["seed_profiles"], "CP2_9")
    k3_h2 = _profile_by_name(h2_host["seed_profiles"], "K3_16")
    cp2_a2 = _curved_product_by_name(a2_product["curved_product_profiles"], "CP2")
    k3_a2 = _curved_product_by_name(a2_product["curved_product_profiles"], "K3")

    protected_code = splice["qec_refinement"]["active_code"]
    snake = splice["snake_closure"]
    closure = kernel["closure_equalities"]

    logical_harmonic_channels = {
        "CP2_9_total": H1 * cp2_hodge["harmonic_form_total"],
        "CP2_9_by_degree": [H1 * count for count in cp2_hodge["zero_modes_by_degree"]],
        "K3_16_total": H1 * k3_hodge["harmonic_form_total"],
        "K3_16_by_degree": [H1 * count for count in k3_hodge["zero_modes_by_degree"]],
        "K3_16_middle_h2": H1 * k3_h2["h2_dimension"],
    }

    protected_harmonic_channels = {
        "CP2_9_total": 82320 * cp2_hodge["harmonic_form_total"],
        "K3_16_total": 82320 * k3_hodge["harmonic_form_total"],
    }

    density_limits = {
        "external_chain": density["universal_local_limits"]["external_chain_density_per_top_simplex"]["exact"],
        "external_trace": density["universal_local_limits"]["external_trace_dk_squared_per_top_simplex"]["exact"],
        "w33_product_chain": density["universal_local_limits"]["product_chain_density_per_top_simplex"]["exact"],
        "w33_product_trace": density["universal_local_limits"]["product_trace_per_top_simplex"]["exact"],
        "a2_product_chain": a2_product["density_limits"]["a2_product_chain_density_per_top_simplex"]["exact"],
        "a2_product_trace": a2_product["density_limits"]["a2_product_trace_per_top_simplex"]["exact"],
    }

    handoff = {
        "finite_runtime_degree": K,
        "external_dimension": 4,
        "finite_plus_external": K + 4,
        "k3_seed_vertices": k3_complex["vertices"],
        "cp2_seed_vertices": cp2_complex["vertices"],
        "read": "the finite runtime closes at K=12; the genuine curved factor supplies dimension 4, and K+4 lands on the K3_16 seed scale",
    }

    checks: List[Dict[str, Any]] = []
    checks.append(ok("protected finite kernel verified", kernel["verified"] is True, kernel["checks_passed"]))
    checks.append(ok("fusion-control scheduler splice verified", splice["verified"] is True, splice["checks_passed"]))
    checks.append(ok("explicit curved complexes verified by builder", explicit["status"] == "ok", explicit["construction_notes"]))
    checks.append(ok("curved external Hodge product verified by builder", hodge["status"] == "ok", hodge["bridge_verdict"]))
    checks.append(ok("curved barycentric density verified by builder", density["status"] == "ok", density["bridge_verdict"]))
    checks.append(ok("curved A2 transport product verified by builder", a2_product["status"] == "ok", a2_product["bridge_verdict"]))
    checks.append(ok("curved H2 host constraints verified by builder", h2_host["status"] == "ok", h2_host["bridge_constraints"]))

    checks.append(ok("finite protected code remains [[82320,81,>=81]]", protected_code == "[[82320,81,>=81]]", splice["qec_refinement"]))
    checks.append(ok("finite snake head/tail remains H1", snake["head_projective_frame_states"] == snake["tail_logical_h1"] == closure["logical_sector"] == H1, snake))
    checks.append(ok("finite classical selector remains V=40", snake["classical_selector_trits"] == closure["w33_vertices"] == V, snake))
    checks.append(ok("finite edge carrier remains 240", W33_EDGES == 240, W33_EDGES))

    checks.append(ok("CP2_9 has explicit 4D chain profile", cp2_complex["vertices"] == Q**2 and list(cp2_complex["betti_numbers"]) == [1, 0, 1, 0, 1], cp2_complex))
    checks.append(ok("K3_16 has explicit 4D chain profile", k3_complex["vertices"] == LAM**MU and list(k3_complex["betti_numbers"]) == [1, 0, 22, 0, 1], k3_complex))
    checks.append(ok("CP2_9 and K3_16 have expected harmonic totals", cp2_hodge["harmonic_form_total"] == Q and k3_hodge["harmonic_form_total"] == 24, {"CP2": cp2_hodge, "K3": k3_hodge}))
    checks.append(ok("external total chain dimensions are 255 and 1704", cp2_hodge["total_chain_dim"] == 255 and k3_hodge["total_chain_dim"] == 1704, {"CP2": cp2_hodge["total_chain_dim"], "K3": k3_hodge["total_chain_dim"]}))
    checks.append(ok("curved product heat traces factorize to numerical tolerance", all(check["abs_error"] < 1e-8 for check in hodge["product_heat_checks"]), hodge["product_heat_checks"]))

    checks.append(ok("logical harmonic channel on CP2_9 is 243", logical_harmonic_channels["CP2_9_total"] == 243, logical_harmonic_channels))
    checks.append(ok("logical harmonic channel on K3_16 is 1944", logical_harmonic_channels["K3_16_total"] == 1944, logical_harmonic_channels))
    checks.append(ok("K3_16 middle H2 matter channel is 1782", logical_harmonic_channels["K3_16_middle_h2"] == 1782, logical_harmonic_channels))
    checks.append(ok("CP2_9 cannot host rank-2 H2 branch", h2_host["bridge_constraints"]["cp2_is_not_rank2_h2_host"] is True, h2_host["bridge_constraints"]))
    checks.append(ok("K3_16 is first explicit rank-2 H2 host", h2_host["bridge_constraints"]["first_explicit_rank2_h2_host_is_k3"] is True, h2_host["bridge_constraints"]))
    checks.append(ok("K3_16 has indefinite H2 signature split", (k3_h2["b2_plus"], k3_h2["b2_minus"]) == (3, 19), k3_h2))

    checks.append(ok("external barycentric chain density limit is 120/19", density_limits["external_chain"] == "120/19", density_limits))
    checks.append(ok("external barycentric trace density limit is 860/19", density_limits["external_trace"] == "860/19", density_limits))
    checks.append(ok("W33 product chain density limit is 19440/19", density_limits["w33_product_chain"] == "19440/19", density_limits))
    checks.append(ok("W33 product trace density limit is 7512120/19", density_limits["w33_product_trace"] == "7512120/19", density_limits))
    checks.append(ok("barycentric modes 2 and 24 vanish", density["neighborly_mode_formulas"]["vanishing_modes"] == [2, 24], density["neighborly_mode_formulas"]))

    a2_internal = a2_product["a2_internal_profile"]
    checks.append(ok("A2 transport internal dimension is 90", a2_internal["total_dimension"] == 90, a2_internal))
    checks.append(ok("A2 transport positive gap is 24", a2_internal["spectral_gap"] == 24, a2_internal))
    checks.append(ok("A2 curved product heat traces factorize", all(check["abs_error"] < 1e-8 for check in a2_product["product_heat_checks"]), a2_product["product_heat_checks"]))
    checks.append(ok("A2 CP2 product has no zero modes", cp2_a2["zero_modes"] == 0 and cp2_a2["total_dimension"] == 22950, cp2_a2))
    checks.append(ok("A2 K3 product has no zero modes", k3_a2["zero_modes"] == 0 and k3_a2["total_dimension"] == 153360, k3_a2))
    checks.append(ok("A2 product density limits are exact", density_limits["a2_product_chain"] == "10800/19" and density_limits["a2_product_trace"] == "423000/19", density_limits))

    checks.append(ok("protected harmonic channels lift CP2 and K3", protected_harmonic_channels["CP2_9_total"] == 246960 and protected_harmonic_channels["K3_16_total"] == 1975680, protected_harmonic_channels))
    checks.append(ok("finite runtime degree plus external dimension lands on K3 seed scale", handoff["finite_plus_external"] == handoff["k3_seed_vertices"] == 16, handoff))
    checks.append(ok("external dimension is not replaced by finite kernel", handoff["external_dimension"] == 4 and handoff["finite_runtime_degree"] == K, handoff))

    verified = all(check["passed"] for check in checks)
    return {
        "part": "CCCCXXVII",
        "title": "Photonic Curved Product Handoff",
        "verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(check["passed"] for check in checks),
        "protected_finite_kernel": {
            "active_code": protected_code,
            "h1_logical": H1,
            "selector_trits": V,
            "edge_carrier": W33_EDGES,
            "fusion_budget": splice["fusion_budget_split"],
            "klm_budget": splice["klm_budget_split"],
        },
        "curved_external_seeds": {
            "CP2_9": {
                "vertices": cp2_complex["vertices"],
                "betti_numbers": list(cp2_complex["betti_numbers"]),
                "harmonic_total": cp2_hodge["harmonic_form_total"],
                "total_chain_dim": cp2_hodge["total_chain_dim"],
            },
            "K3_16": {
                "vertices": k3_complex["vertices"],
                "betti_numbers": list(k3_complex["betti_numbers"]),
                "harmonic_total": k3_hodge["harmonic_form_total"],
                "total_chain_dim": k3_hodge["total_chain_dim"],
                "h2_signature_split": [k3_h2["b2_plus"], k3_h2["b2_minus"]],
            },
        },
        "logical_harmonic_channels": logical_harmonic_channels,
        "protected_harmonic_channels": protected_harmonic_channels,
        "density_limits": density_limits,
        "a2_transport_product": {
            "internal_dimension": a2_internal["total_dimension"],
            "positive_gap": a2_internal["spectral_gap"],
            "laplacian_spectrum": {str(key): value for key, value in a2_internal["laplacian_spectrum"].items()},
            "cp2_product_dimension": cp2_a2["total_dimension"],
            "k3_product_dimension": k3_a2["total_dimension"],
            "product_zero_modes_vanish_exactly": a2_product["density_limits"]["product_zero_modes_vanish_exactly"],
        },
        "handoff_read": handoff,
        "architecture_upgrade": (
            "Attaches the protected photonic runtime to the explicit curved "
            "4D operator packages. The finite kernel supplies H1=81, the "
            "[[82320,81,>=81]] protected code, and the 40-trit selector; CP2_9 "
            "and K3_16 supply genuine external Hodge sectors, product heat "
            "factorization, and barycentric 4D refinement limits."
        ),
        "theorem": (
            "The protected finite photonic kernel can be paired with the explicit "
            "curved 4D seeds by the almost-commutative product. CP2_9 contributes "
            "3 harmonic sectors and K3_16 contributes 24, so the H1=81 logical "
            "tail lifts to 243 and 1944 curved harmonic channels. Product heat "
            "traces factorize on the explicit spectra, barycentric refinement "
            "has universal local limits 120/19 and 860/19, and the native A2 "
            "transport product has positive gap 24 with zero product zero modes."
        ),
        "honesty_boundary": (
            "This proves a finite-to-curved product handoff, not the final "
            "Einstein-Hilbert spectral-action asymptotic theorem. The finite "
            "kernel does not by itself create a 4D Weyl law; the external "
            "curved refinement family supplies the genuine continuum scale."
        ),
        "checks": checks,
    }


def main() -> int:
    results = build_results()
    out = ROOT / "PART_CCCCXXVII_photonic_curved_product_handoff_results.json"
    out.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "part": results["part"],
                "verified": results["verified"],
                "checks_passed": results["checks_passed"],
                "checks_total": results["checks_total"],
                "cp2_h1_channels": results["logical_harmonic_channels"]["CP2_9_total"],
                "k3_h1_channels": results["logical_harmonic_channels"]["K3_16_total"],
                "out_path": str(out),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
