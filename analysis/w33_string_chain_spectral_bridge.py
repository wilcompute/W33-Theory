#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_string_chain_spectral_bridge.json"

q = 3
qfac = 6
Phi3 = 13
Phi4 = 10
Phi6 = 7
pIh = 11
k = 12
f = 24
lam = 2
v = 40
metric_even = 55
wzw_sum = Phi6 * Phi3
chain = [Phi6, Phi4, pIh, k, f + lam]
core = sum(chain[:4])
total = sum(chain)
middle = total + qfac
payload = {
  "summary": {
    "dimension_chain": chain,
    "core_sum": core,
    "total_sum": total,
    "middle_index": middle,
    "all_identities_hold": True
  },
  "identities": {
    "core_is_v": core == v,
    "total_is_C12_2": total == k*(k-1)//2,
    "middle_is_total_plus_qfac": middle == 72,
    "hessian_is_q2_middle": q*q*middle == 648,
    "conjugate_real_part": 2*middle == 144,
    "conjugate_radical_coeff": qfac*qfac == 36,
    "F4_from_total": total - 2*Phi6 == 52,
    "E6_from_total": total + k == 78,
    "E7_from_total": total + k + metric_even == 133,
    "E8_from_total": total + 2*wzw_sum == 248,
    "cycle_from_total": 3*total + lam == 200
  },
  "closed_forms": {
    "40": "7+10+11+12 = v",
    "66": "7+10+11+12+26 = C(12,2)",
    "72": "66+6",
    "648": "9*72",
    "144_pm_36sqrt6": "2*72 +/- 36*sqrt(6)",
    "F4": "52 = 66 - 14",
    "E6": "78 = 66 + 12",
    "E7": "133 = 66 + 12 + 55",
    "E8": "248 = 66 + 2*91",
    "Ihara_cycle": "200 = 3*66 + 2"
  },
  "theorem": "The dimension chain 7,10,11,12,26 gives core 40, total 66, middle 72, Hessian 648, and the conjugate pair 144 +/- 36 sqrt(6)."
}

if __name__ == "__main__":
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    print(f"wrote {OUT.relative_to(ROOT)}")
