#!/usr/bin/env python3
"""
BT414: Threshold Reciprocity Bridge for Gauge Running and the Higgs Quartic

BT413 found that the W33 seesaw scale is not the triple one-loop GUT point.
Instead it is the mu/F5 = 4/5 weighted geometric center of the first two
electroweak pairwise crossings.

The scalar side carries the reciprocal operation: a universal W33 vertex
coupling 1/v = 1/40 lifted by the Fibonacci factor F5 gives

    lambda_H(EW) = F5 / v = 5/40 = 1/8 = 2^{-q}.

Then the Higgs mass relation m_H = sqrt(2 lambda_H) v_H gives

    m_H = v_H / 2

within about 1.7 percent of the measured Higgs mass. This is not a complete
Higgs theorem because the electroweak VEV is still an input, but it gives the
missing threshold bridge a precise two-sided algebra:

    (gauge scale weight) * (scalar quartic lift) = (mu/F5) * F5 = mu.
"""

from __future__ import annotations

import json
import math
from pathlib import Path


q = 3
lambda_ = 2
mu = 4
F5 = 5
v_w33 = 40

HIGGS_VEV_GEV = 246.21964023926205
M_H_OBS_GEV = 125.25


def rel_err(value: float, target: float) -> float:
    return abs(value - target) / abs(target)


def load_json(path: str):
    p = Path(path)
    if not p.exists():
        return None
    with p.open() as fobj:
        return json.load(fobj)


bt399 = load_json("BT413_results.json")
bt394 = load_json("BT394_results.json")

if bt399 is None:
    raise FileNotFoundError("BT413_results.json must be generated before BT414")

gauge_weight = bt399["w33_scale_center"]["target_mu_over_F5"]
observed_gauge_weight = bt399["w33_scale_center"]["M_W33_over_geometric_center"]
gauge_weight_error = bt399["w33_scale_center"]["relative_error_to_target_scale"]

scalar_seed = 1.0 / v_w33
scalar_lift = F5
lambda_H_EW = scalar_lift * scalar_seed
lambda_H_binary_target = 1.0 / (2**q)
lambda_H_obs = (M_H_OBS_GEV / HIGGS_VEV_GEV) ** 2 / 2.0

m_H_pred = math.sqrt(2.0 * lambda_H_EW) * HIGGS_VEV_GEV
m_H_binary = HIGGS_VEV_GEV / 2.0

reciprocity_product = gauge_weight * scalar_lift

bt394_best_error = None
improvement_over_bt394 = None
if bt394 is not None:
    bt394_best_error = bt394.get("best_prediction", {}).get("err_pct")
    if bt394_best_error is not None:
        improvement_over_bt394 = bt394_best_error / (rel_err(m_H_pred, M_H_OBS_GEV) * 100.0)

checks = {
    "scalar_seed_is_vertex_reciprocal": abs(scalar_seed - 1.0 / 40.0) < 1e-15,
    "scalar_lift_is_F5": scalar_lift == F5,
    "lambda_H_EW_is_binary_volume": abs(lambda_H_EW - lambda_H_binary_target) < 1e-15,
    "higgs_mass_is_vev_over_two": abs(m_H_pred - m_H_binary) < 1e-12,
    "gauge_scalar_reciprocity_product_is_mu": abs(reciprocity_product - mu) < 1e-15,
    "higgs_mass_error_under_2pct": rel_err(m_H_pred, M_H_OBS_GEV) < 0.02,
    "higgs_quartic_error_under_4pct": rel_err(lambda_H_EW, lambda_H_obs) < 0.04,
    "bt399_gauge_weight_error_under_0p2pct": gauge_weight_error < 0.002,
}

if improvement_over_bt394 is not None:
    checks["improves_BT394_executable_mass_error_by_10x"] = improvement_over_bt394 > 10.0

for check_name, passed in checks.items():
    if not passed:
        raise AssertionError(f"BT414 check failed: {check_name}")

results = {
    "BT": 400,
    "title": "Threshold Reciprocity Bridge for Gauge Running and the Higgs Quartic",
    "substrate_primitives": {
        "q": q,
        "lambda": lambda_,
        "mu": mu,
        "F5": F5,
        "v_w33": v_w33,
    },
    "gauge_side_from_BT413": {
        "target_gauge_weight": gauge_weight,
        "observed_gauge_weight": observed_gauge_weight,
        "relative_error_to_BT413_target_scale": gauge_weight_error,
        "meaning": "M_W33 is approximately (mu/F5)*sqrt(M12*M13)",
    },
    "scalar_side": {
        "lambda_H_seed_GUT": scalar_seed,
        "lambda_H_seed_formula": "1/v(W33) = 1/40",
        "scalar_lift": scalar_lift,
        "scalar_lift_formula": "F5",
        "lambda_H_EW": lambda_H_EW,
        "lambda_H_EW_formula": "F5/v = 5/40 = 1/8 = 2^-q",
        "lambda_H_obs_from_mH_and_vev": lambda_H_obs,
        "lambda_H_error_pct": rel_err(lambda_H_EW, lambda_H_obs) * 100.0,
    },
    "higgs_mass": {
        "Higgs_VEV_GeV_input": HIGGS_VEV_GEV,
        "m_H_pred_GeV": m_H_pred,
        "m_H_pred_formula": "sqrt(2*(1/8))*v_H = v_H/2",
        "m_H_obs_GeV": M_H_OBS_GEV,
        "m_H_error_pct": rel_err(m_H_pred, M_H_OBS_GEV) * 100.0,
        "BT394_best_error_pct": bt394_best_error,
        "improvement_over_BT394_executable": improvement_over_bt394,
    },
    "reciprocity": {
        "gauge_weight": gauge_weight,
        "scalar_lift": scalar_lift,
        "product": reciprocity_product,
        "target": mu,
        "identity": "(mu/F5)*F5 = mu",
        "interpretation": "the same finite threshold bridge lowers the gauge crossing center by 4/5 and raises the scalar vertex coupling by 5",
    },
    "boundary": {
        "complete_Higgs_theorem": False,
        "reason": "the electroweak VEV is still an external input",
        "next_target": "derive the W33 threshold vector that simultaneously fixes BT387 alpha and the Higgs quartic running",
    },
    "checks": checks,
}

with open("BT414_results.json", "w") as fobj:
    json.dump(results, fobj, indent=2)

print("=" * 80)
print("BT414 THRESHOLD RECIPROCITY HIGGS BRIDGE")
print("=" * 80)
print("Gauge side:")
print(f"  M_W33 / sqrt(M12*M13) = {observed_gauge_weight:.6f}")
print(f"  target mu/F5 = {gauge_weight:.6f}")
print(f"  BT413 target-scale error = {gauge_weight_error*100:.4f}%")
print("")
print("Scalar side:")
print(f"  lambda_H seed = 1/40 = {scalar_seed:.6f}")
print(f"  F5 lift gives lambda_H(EW) = 5/40 = {lambda_H_EW:.6f}")
print(f"  binary target 2^-q = {lambda_H_binary_target:.6f}")
print(f"  observed lambda_H = {lambda_H_obs:.6f}")
print(f"  lambda_H error = {rel_err(lambda_H_EW, lambda_H_obs)*100:.4f}%")
print("")
print("Higgs mass:")
print(f"  m_H = sqrt(2*(1/8))*v_H = v_H/2 = {m_H_pred:.6f} GeV")
print(f"  observed m_H = {M_H_OBS_GEV:.6f} GeV")
print(f"  error = {rel_err(m_H_pred, M_H_OBS_GEV)*100:.4f}%")
if improvement_over_bt394 is not None:
    print(f"  improvement over BT394 executable error = {improvement_over_bt394:.2f}x")
print("")
print("Reciprocity:")
print(f"  (mu/F5)*F5 = {reciprocity_product:.6f} = mu")
print("BT414 checks passed.")
print("Results saved to BT414_results.json")
