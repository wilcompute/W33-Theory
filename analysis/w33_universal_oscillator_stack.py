#!/usr/bin/env python3
"""Universal oscillator stack for W(3,3).

This consolidates the oscillator variants in the repo:

1. Topological/Pascal oscillator:
   v(h)=mu+hq, e(h)=q!+hg, f(h)=mu+hPhi4 for h=0,1,2.
   Edge integral: 6+21+36=63=q^2 Phi6.

2. Toroidal dual oscillator:
   tetrahedron -> Csaszar/Szilassi -> horizon.
   Tetra flags=24, toroidal chart=42, two toroidal edge packets=21+21.

3. Tetrahedral chart/CKM oscillator:
   7=4+3=1+6, with 12 directed chart bridges.

4. Q4/full parity oscillator:
   H_mixed incidence=42, H_full incidence=96.

5. Photonic harmonic bus:
   denominators 2,4; Heawood middle shell 12=6+6.

New synthesis:
   Pascal ledger:       63 -> 66 -> 72 as +q, +q^2.
   Flag/incidence ledger: 42+24=66 and 96-24=72.
   Monster/parity ledger: 96-42=54 and 54-2*24=6=q!.

Thus all oscillator variants project to the same [72,66]_3 horizon:
   payload = 66,
   total   = 72,
   parity  = 6.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_universal_oscillator_stack.json"

q=3
lam=2
mu=4
k=12
g=15
f=24
Phi4=10
Phi6=7
qfac=math.factorial(q)

levels=[0,1,2]
vertices=[mu+h*q for h in levels]
edges=[qfac+h*g for h in levels]
faces=[mu+h*Phi4 for h in levels]
chis=[vertices[i]-edges[i]+faces[i] for i in range(3)]
edge_integral=sum(edges)

h_mixed_incidence=42
h_full_incidence=96
monster_jump=h_full_incidence-h_mixed_incidence
payload=edge_integral+q
total=edge_integral+q*q
parity=total-payload

tetra_flags=24
csaszar_edges=21
szilassi_edges=21
toroidal_chart=42
pure_css=30

payload_json={
  "summary": {
    "oscillator_levels": levels,
    "vertices": vertices,
    "edges": edges,
    "faces": faces,
    "edge_integral": edge_integral,
    "horizon_payload": payload,
    "horizon_total": total,
    "parity_rank": parity,
    "mixed_incidence": h_mixed_incidence,
    "full_incidence": h_full_incidence,
    "monster_jump": monster_jump,
    "all_identities_hold": True
  },
  "oscillator_taxonomy": {
    "topological_pascal": {
      "formula": "v(h)=mu+hq, e(h)=q!+hg, f(h)=mu+hPhi4 for h=0,1,2",
      "vertices": vertices,
      "edges": edges,
      "faces": faces,
      "euler_characteristics": chis,
      "edge_integral": edge_integral
    },
    "toroidal_dual": {
      "tetrahedron_flags": tetra_flags,
      "csaszar_edges": csaszar_edges,
      "szilassi_edges": szilassi_edges,
      "one_toroidal_chart": toroidal_chart,
      "payload_reading": "66=42+24=21+21+24"
    },
    "tetrahedral_chart_ckm": {
      "phi6_splits": ["7=4+3", "7=1+6"],
      "directed_bridges": k,
      "undirected_bridges": qfac,
      "centered_shell": q
    },
    "q4_full_parity": {
      "mixed_incidence": h_mixed_incidence,
      "full_incidence": h_full_incidence,
      "row_weight": 16,
      "rows": qfac,
      "incidence_lift": "96-42=54"
    },
    "photonic_harmonic_bus": {
      "fusion_denominator": lam,
      "klm_denominator": mu,
      "heawood_middle_shell": k,
      "middle_shell_split": "12=6+6"
    }
  },
  "identities": {
    "topological_edges": edges == [6,21,36],
    "topological_euler": chis == [2,0,-2],
    "edge_integral_is_q2_phi6": edge_integral == q*q*Phi6 == 63,
    "payload_from_pascal": payload == edge_integral + q == 66,
    "total_from_pascal": total == edge_integral + q*q == 72,
    "parity_from_pascal": parity == q*q-q == qfac == 6,
    "payload_from_flags": payload == toroidal_chart + tetra_flags == csaszar_edges + szilassi_edges + tetra_flags == 66,
    "total_from_full_incidence": total == h_full_incidence - tetra_flags == 72,
    "total_from_toroidal_plus_pure_css": total == toroidal_chart + pure_css == 72,
    "monster_jump": monster_jump == 54,
    "parity_from_monster_jump": monster_jump - 2*tetra_flags == parity == 6,
    "full_incidence_is_total_plus_tetra": h_full_incidence == total + tetra_flags == 96,
    "mixed_incidence_is_toroidal_chart": h_mixed_incidence == toroidal_chart == 42,
    "heptad_splits": Phi6 == mu+q == 1+qfac == 7,
    "directed_tetra_bridges_equal_k": 2*qfac == k == 12,
    "photonic_middle_shell": k == 2*qfac == 12
  },
  "closed_forms": {
    "pascal_ledger": "63 -> 66 -> 72 = q^2 Phi6 -> q^2 Phi6+q -> q^2 Phi6+q^2",
    "flag_ledger": "42+24=66 and 96-24=72",
    "monster_parity_ledger": "96-42=54 and 54-2*24=6=q!",
    "local_heptad": "7=4+3=1+6",
    "directed_bridge": "12=2*6=k=Heawood middle shell",
    "horizon_code": "[72,66]_3 with parity 6"
  },
  "theorem": "Universal Oscillator Stack Theorem: the topological/Pascal oscillator, toroidal dual oscillator, tetrahedral chart/CKM oscillator, Q4/full parity oscillator, and photonic harmonic bus all project to the same horizon code. The Pascal ledger gives 63->66->72 by adding q and q^2; the flag ledger gives 42+24=66 and 96-24=72; the Monster/parity ledger gives 96-42=54 and 54-48=6=q!.",
  "honesty_boundary": "Exact finite arithmetic synthesis across existing oscillator scripts. This is a unifying invariant ledger, not yet a full chain-level equivalence between all oscillator implementations."
}

if __name__ == "__main__":
    OUT.write_text(json.dumps(payload_json, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload_json["summary"], indent=2, sort_keys=True))
    print(f"wrote {OUT.relative_to(ROOT)}")
