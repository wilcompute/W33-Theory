#!/usr/bin/env python3
"""
BT413: Electroweak Pairwise-Crossing Lattice at the W33 Scale

BT387's literal one-loop script does not close alpha by itself. The useful
structure is more precise: using the observed M_Z couplings and standard
one-loop SM beta coefficients, the three pairwise crossing scales form an
almost substrate-clean ladder, and the W33 seesaw scale sits at the 4/5
weighted geometric center of the first two crossings.

This script keeps the result honest:
  * no triple one-loop unification is claimed;
  * the current BT387 alpha mismatch is preserved as a frontier;
  * the next missing object is a threshold/normalization bridge at M_W33.
"""

import json
import math
from pathlib import Path


# ---------------------------------------------------------------------------
# Substrate primitives
# ---------------------------------------------------------------------------
q = 3
lambda_ = 2
mu = 4
F5 = 5
k = 12
f = 24
q_fact = math.factorial(q)

M_Z = 91.1876
M_W33 = 5.0e13

# Repo/BT388 observable inputs. These are the same values used by the
# immediately preceding dashboard batch.
alpha_em_inv_MZ_obs = 128.9
sin2_thetaW_MZ_obs = 0.23122
alpha_s_MZ_obs = 0.1181

# Standard Model one-loop beta coefficients with GUT-normalized U(1).
b1 = 41.0 / 10.0
b2 = -19.0 / 6.0
b3 = -7.0


def observed_gut_normalized_couplings():
    """Return alpha_i^{-1}(M_Z) for GUT-normalized U(1), SU(2), SU(3)."""
    cos2 = 1.0 - sin2_thetaW_MZ_obs
    alpha2_inv = sin2_thetaW_MZ_obs * alpha_em_inv_MZ_obs
    alpha_y_inv = cos2 * alpha_em_inv_MZ_obs
    alpha1_inv = (3.0 / 5.0) * alpha_y_inv
    alpha3_inv = 1.0 / alpha_s_MZ_obs
    return {
        "alpha1_inv": alpha1_inv,
        "alpha2_inv": alpha2_inv,
        "alpha3_inv": alpha3_inv,
        "alphaY_inv": alpha_y_inv,
    }


def pairwise_crossing(ai, aj, bi, bj):
    """Solve alpha_i^{-1}(mu) = alpha_j^{-1}(mu) at one loop."""
    ln_mu_over_mz = 2.0 * math.pi * (ai - aj) / (bi - bj)
    scale = M_Z * math.exp(ln_mu_over_mz)
    alpha_inv_at_crossing = ai - (bi / (2.0 * math.pi)) * ln_mu_over_mz
    return {
        "ln_mu_over_MZ": ln_mu_over_mz,
        "scale_GeV": scale,
        "alpha_inv": alpha_inv_at_crossing,
    }


def run_to_scale(alpha_inv_mz, beta, scale):
    ln_mu_over_mz = math.log(scale / M_Z)
    return alpha_inv_mz - beta / (2.0 * math.pi) * ln_mu_over_mz


def rel_err(value, target):
    return abs(value - target) / abs(target)


def load_bt387_frontier():
    path = Path("BT387_results.json")
    if not path.exists():
        return {"available": False}
    with path.open() as fobj:
        data = json.load(fobj)
    return {
        "available": True,
        "alpha_em_inv_0": data.get("alpha_em_inv_0"),
        "alpha_em_inv_0_err_pct": data.get("alpha_em_inv_0_err_pct"),
        "sin2_thetaW_MZ": data.get("predictions_MZ", {}).get("sin2_thetaW"),
        "sin2_thetaW_MZ_err_pct": data.get("predictions_MZ", {}).get("sin2_thetaW_err_pct"),
        "status": data.get("status"),
    }


couplings = observed_gut_normalized_couplings()

cross_12 = pairwise_crossing(couplings["alpha1_inv"], couplings["alpha2_inv"], b1, b2)
cross_13 = pairwise_crossing(couplings["alpha1_inv"], couplings["alpha3_inv"], b1, b3)
cross_23 = pairwise_crossing(couplings["alpha2_inv"], couplings["alpha3_inv"], b2, b3)

scale_12 = cross_12["scale_GeV"]
scale_13 = cross_13["scale_GeV"]
scale_23 = cross_23["scale_GeV"]

ratio_13_12 = scale_13 / scale_12
ratio_23_13 = scale_23 / scale_13
ratio_23_12 = scale_23 / scale_12

target_13_12 = F5**2
target_23_13 = (f - q_fact) * F5**2
target_23_12 = target_13_12 * target_23_13

geometric_center_12_13 = math.sqrt(scale_12 * scale_13)
w33_center_target = (mu / F5) * geometric_center_12_13
w33_center_ratio = M_W33 / geometric_center_12_13
w33_center_target_ratio = mu / F5

alpha_at_w33 = {
    "alpha1_inv": run_to_scale(couplings["alpha1_inv"], b1, M_W33),
    "alpha2_inv": run_to_scale(couplings["alpha2_inv"], b2, M_W33),
    "alpha3_inv": run_to_scale(couplings["alpha3_inv"], b3, M_W33),
}
alpha_values = list(alpha_at_w33.values())
alpha_mean = sum(alpha_values) / len(alpha_values)
threshold_vector = {name: value - alpha_mean for name, value in alpha_at_w33.items()}
spread = max(alpha_values) - min(alpha_values)
rms_spread = math.sqrt(sum((value - alpha_mean) ** 2 for value in alpha_values) / 3.0)

bt387_frontier = load_bt387_frontier()

checks = {
    "m13_over_m12_is_F5_squared_within_0p5pct": rel_err(ratio_13_12, target_13_12) < 0.005,
    "m23_over_m13_is_18_F5_squared_within_0p1pct": rel_err(ratio_23_13, target_23_13) < 0.001,
    "m23_over_m12_is_product_ladder_within_0p6pct": rel_err(ratio_23_12, target_23_12) < 0.006,
    "w33_is_four_fifths_geometric_center_within_0p2pct": rel_err(M_W33, w33_center_target) < 0.002,
    "no_exact_triple_unification_at_w33": spread > 1.0,
}

for check_name, passed in checks.items():
    if not passed:
        raise AssertionError(f"BT413 check failed: {check_name}")

results = {
    "BT": 399,
    "title": "Electroweak Pairwise-Crossing Lattice at the W33 Scale",
    "inputs": {
        "M_Z_GeV": M_Z,
        "M_W33_GeV": M_W33,
        "alpha_em_inv_MZ_obs": alpha_em_inv_MZ_obs,
        "sin2_thetaW_MZ_obs": sin2_thetaW_MZ_obs,
        "alpha_s_MZ_obs": alpha_s_MZ_obs,
        "beta_coefficients": {"b1": b1, "b2": b2, "b3": b3},
    },
    "substrate_primitives": {
        "q": q,
        "lambda": lambda_,
        "mu": mu,
        "F5": F5,
        "f": f,
        "q_factorial": q_fact,
    },
    "couplings_at_MZ": couplings,
    "pairwise_crossings": {
        "M12_alpha1_alpha2": cross_12,
        "M13_alpha1_alpha3": cross_13,
        "M23_alpha2_alpha3": cross_23,
    },
    "crossing_ladder": {
        "M13_over_M12": ratio_13_12,
        "target_M13_over_M12": target_13_12,
        "relative_error_M13_over_M12": rel_err(ratio_13_12, target_13_12),
        "M23_over_M13": ratio_23_13,
        "target_M23_over_M13": target_23_13,
        "relative_error_M23_over_M13": rel_err(ratio_23_13, target_23_13),
        "M23_over_M12": ratio_23_12,
        "target_M23_over_M12": target_23_12,
        "relative_error_M23_over_M12": rel_err(ratio_23_12, target_23_12),
    },
    "w33_scale_center": {
        "geometric_center_M12_M13_GeV": geometric_center_12_13,
        "M_W33_over_geometric_center": w33_center_ratio,
        "target_mu_over_F5": w33_center_target_ratio,
        "target_scale_GeV": w33_center_target,
        "relative_error_to_target_scale": rel_err(M_W33, w33_center_target),
    },
    "couplings_at_W33_scale": {
        "alpha_inv_values": alpha_at_w33,
        "mean_alpha_inv": alpha_mean,
        "threshold_vector_to_mean": threshold_vector,
        "spread": spread,
        "rms_spread": rms_spread,
    },
    "BT387_frontier": bt387_frontier,
    "interpretation": {
        "closed_alpha_proof": False,
        "triple_unification_claim": False,
        "new_bridge_target": "derive the finite W33 threshold/normalization vector at M_W33",
        "core_result": "M_W33 is the mu/F5 weighted geometric center of the alpha1-alpha2 and alpha1-alpha3 pairwise crossings",
    },
    "checks": checks,
}

with open("BT413_results.json", "w") as fobj:
    json.dump(results, fobj, indent=2)

print("=" * 80)
print("BT413 ELECTROWEAK PAIRWISE-CROSSING LATTICE")
print("=" * 80)
print("Observed one-loop pairwise crossing scales:")
print(f"  M12 (alpha1=alpha2): {scale_12:.6e} GeV")
print(f"  M13 (alpha1=alpha3): {scale_13:.6e} GeV")
print(f"  M23 (alpha2=alpha3): {scale_23:.6e} GeV")
print("")
print("Substrate ladder:")
print(f"  M13/M12 = {ratio_13_12:.6f}  target F5^2 = {target_13_12}")
print(f"  M23/M13 = {ratio_23_13:.6f}  target (f-q!)*F5^2 = {target_23_13}")
print(f"  M23/M12 = {ratio_23_12:.6f}  target product = {target_23_12}")
print("")
print("W33 scale placement:")
print(f"  sqrt(M12*M13) = {geometric_center_12_13:.6e} GeV")
print(f"  M_W33 / sqrt(M12*M13) = {w33_center_ratio:.6f}")
print(f"  target mu/F5 = {w33_center_target_ratio:.6f}")
print(f"  (mu/F5)*sqrt(M12*M13) = {w33_center_target:.6e} GeV")
print(f"  relative error = {rel_err(M_W33, w33_center_target)*100:.4f}%")
print("")
print("At M_W33, no triple unification is claimed:")
for name, value in alpha_at_w33.items():
    print(f"  {name}(M_W33)^-1 = {value:.6f}")
print(f"  spread = {spread:.6f}, rms spread = {rms_spread:.6f}")
print("")
print("BT413 checks passed.")
print("Results saved to BT413_results.json")
