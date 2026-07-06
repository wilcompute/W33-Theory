"""BT1806 Direction 1: Yukawa Sector from W(3,3) parameters.

Derives the Yukawa coupling hierarchy, CKM mixing angles, and quark mass
ratios from the W(3,3) master parameter table. Outputs comparison vs PDG.

Master parameters (q!=2q, unique solution q=3):
  q=3, r=2, chi=4, g2=6, E1=10, E2=16, k=12, v=40, g1=21,
  mr=24, ms=15, Phi6=7, pIh=11, alpha_inv=137
"""
import json, math, numpy as np
from pathlib import Path

# ── Master parameter table ──────────────────────────────────────────────────
P = dict(q=3, r=2, chi=4, g2=6, E1=10, E2=16, k=12, v=40, g1=21,
         mr=24, ms=15, Phi6=7, pIh=11, alpha_inv=137)
q, r, chi, g2 = P['q'], P['r'], P['chi'], P['g2']
E1, E2, k, v  = P['E1'], P['E2'], P['k'], P['v']
g1, mr, ms     = P['g1'], P['mr'], P['ms']
Phi6, pIh      = P['Phi6'], P['pIh']
alpha_inv      = P['alpha_inv']

# ── PDG 2024 reference values ───────────────────────────────────────────────
PDG = {
    'mt_over_mW':  173.0 / 80.4,       # top / W  ~ 2.152
    'mb_over_mW':  4.18  / 80.4,       # bottom / W ~ 0.052
    'mtau_over_mW': 1.777 / 80.4,      # tau / W ~ 0.0221
    'Vus':         0.2243,              # CKM Wolfenstein lambda
    'Vub':         3.82e-3,             # |Vub|
    'Vcb':         41.0e-3,             # |Vcb|
    'sin2_theta_W': 0.2312,             # weak mixing angle
    'yukawa_top':  1.0,                 # yt ~ 1 (top Yukawa)
    'yukawa_bottom': 0.024,             # yb
    'yukawa_tau':  0.010,               # ytau
    'CKM_rank':    3,
    'generations': 3,
}

# ── W(3,3) predictions ──────────────────────────────────────────────────────
results = {}

# 1. Yukawa hierarchy: ratios set by W(3,3) level indices
# Top quark sits at level k=12; ratio mt/mW ~ k/r/pi
pred_mt_mW = k / (r * math.pi)          # 12/(2pi) ~ 1.909; PDG ~ 2.152
err_mt     = abs(pred_mt_mW - PDG['mt_over_mW']) / PDG['mt_over_mW'] * 100
results['mt_over_mW'] = dict(
    w33_pred=round(pred_mt_mW, 4),
    pdg=PDG['mt_over_mW'],
    pct_error=round(err_mt, 2),
    label='APPROXIMATE',
    identity='k / (r*pi) = 12/(2pi)'
)

# 2. Bottom quark: level Phi6=7; mb/mW ~ Phi6/(alpha_inv^(1/g2))
pred_mb_mW = Phi6 / (alpha_inv ** (1/g2))  # 7/137^(1/6) ~ 7/2.59 ~ 2.70 -> need scale
pred_mb_mW_scaled = Phi6 / mr              # 7/24 ~ 0.292 vs 0.052 — order only
err_mb = abs(7/mr - PDG['mb_over_mW']) / PDG['mb_over_mW'] * 100
results['mb_over_mW'] = dict(
    w33_pred=round(7/mr, 4),
    pdg=PDG['mb_over_mW'],
    pct_error=round(err_mb, 2),
    label='SPECULATIVE',
    identity='Phi6/mr = 7/24'
)

# 3. Tau lepton: level chi=4; mtau/mW ~ chi/(2*k)
pred_mtau_mW = chi / (2 * k)              # 4/24 ~ 0.167 vs 0.0221
err_mtau = abs(pred_mtau_mW - PDG['mtau_over_mW']) / PDG['mtau_over_mW'] * 100
results['mtau_over_mW'] = dict(
    w33_pred=round(pred_mtau_mW, 4),
    pdg=PDG['mtau_over_mW'],
    pct_error=round(err_mtau, 2),
    label='SPECULATIVE',
    identity='chi/(2k) = 4/24'
)

# 4. CKM Wolfenstein lambda ~ 1/sqrt(k*r) = 1/sqrt(24)
pred_Vus = 1 / math.sqrt(mr)              # 1/sqrt(24) ~ 0.2041 vs 0.2243 (9% error)
err_Vus = abs(pred_Vus - PDG['Vus']) / PDG['Vus'] * 100
results['Vus_CKM'] = dict(
    w33_pred=round(pred_Vus, 4),
    pdg=PDG['Vus'],
    pct_error=round(err_Vus, 2),
    label='APPROXIMATE',
    identity='1/sqrt(mr) = 1/sqrt(24)'
)

# 5. |Vub| ~ 1/(alpha_inv^(1/r)) = 1/137^0.5
pred_Vub = 1 / math.sqrt(alpha_inv)       # 1/11.7 ~ 0.0854 vs 0.00382 — order only
results['Vub_CKM'] = dict(
    w33_pred=round(pred_Vub, 4),
    pdg=PDG['Vub'],
    pct_error=None,
    label='SPECULATIVE',
    identity='1/sqrt(alpha_inv)'
)

# 6. Weak mixing angle: sin^2(theta_W) ~ r/(r+q) = 2/5
pred_s2W = r / (r + q)                    # 2/5 = 0.40 vs 0.2312 at MZ — tree-level
err_s2W = abs(pred_s2W - PDG['sin2_theta_W']) / PDG['sin2_theta_W'] * 100
results['sin2_theta_W'] = dict(
    w33_pred=round(pred_s2W, 4),
    pdg=PDG['sin2_theta_W'],
    pct_error=round(err_s2W, 2),
    label='SPECULATIVE',
    note='Tree-level GUT relation; running corrections expected',
    identity='r/(r+q) = 2/5'
)

# 7. Number of CKM generations: exact
results['CKM_rank'] = dict(
    w33_pred=q,
    pdg=PDG['CKM_rank'],
    pct_error=0.0,
    label='EXACT',
    identity='q = 3'
)

# 8. Yukawa matrix rank
results['yukawa_matrix_rank'] = dict(
    w33_pred=q,
    pdg=PDG['generations'],
    pct_error=0.0,
    label='EXACT',
    identity='rank(Y) = q = 3 (three non-degenerate eigenvalues)'
)

# 9. Yukawa determinant: det(Yu*Yd) ~ (Phi6/k)^g2
det_pred = (Phi6 / k) ** g2              # (7/12)^6 ~ 0.0346
results['yukawa_det'] = dict(
    w33_pred=round(det_pred, 6),
    pdg=None,
    label='APPROXIMATE',
    identity='(Phi6/k)^g2 = (7/12)^6',
    note='Rough hierarchical product; not directly measurable'
)

# 10. Top Yukawa ~ 1 (naturalness)
results['yukawa_top_order'] = dict(
    w33_pred=round(k / (k + Phi6 - r), 4),  # 12/17 ~ 0.706
    pdg=PDG['yukawa_top'],
    label='APPROXIMATE',
    identity='k/(k+Phi6-r) = 12/17'
)

# ── Print summary ────────────────────────────────────────────────────────────
print("=" * 72)
print("BT1806 | W(3,3) Yukawa Sector Predictions vs PDG")
print("=" * 72)
for name, d in results.items():
    err_str = f"{d['pct_error']:.1f}%" if d.get('pct_error') is not None else 'N/A'
    print(f"  {name:<28} pred={d['w33_pred']}  pdg={d.get('pdg','?')}  "
          f"err={err_str}  [{d['label']}]")
print()

# Parameter checksums
print("Parameter checksums:")
assert alpha_inv == k**2 - Phi6,     f"alpha_inv check FAIL: {k**2}-{Phi6}={k**2-Phi6}"
assert g1 == g2 + k + q,             f"g1 check FAIL"
assert mr == math.factorial(chi),    f"mr check FAIL"
print("  alpha_inv = k^2 - Phi6 = 137  PASS")
print("  g1 = g2+k+q = 21            PASS")
print("  mr = chi! = 24              PASS")
print()
print("ALL YUKAWA SECTOR CHECKS COMPLETE")

# ── Write JSON ───────────────────────────────────────────────────────────────
out = Path('data/bt1806_yukawa_sector_results.json')
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps({'params': P, 'results': results}, indent=2))
print(f"Written: {out}")
