"""TOE59 rigorous infinite-flux ground-energy interval for native 3-loop block.

Use positive Wilson magnetic operator and exact boundary coupling norm.
Conditional for 3 selected loops ONLY, not full W33 1385-plaquette QED.
"""
from pathlib import Path
import json,sys,numpy as np
R=Path(__file__).resolve().parents[1]
cert=json.loads((R/"data/w33_20261013_toe58_three_octagons.json").read_text())
G=np.asarray(cert["signed_Gram"],float)
lam=float(np.linalg.eigvalsh(G)[0]);assert abs(lam-4)<1e-12
rows=[]
for g in (.7,1.1):
 v=cert["samples"][f"{g}_neutral"]
 bounds=[]
 for item in v:
  N=item["N"];e=float(item["ground"])
  # Full infinite Hilbert H= g²/2 m.T G m + sum_i(1-cos theta_i)/g².
  # If m outside cube [-N,N]^3, ||m|| >= N+1, so KE>=g² λmin(G)(N+1)²/2.
  # Wilson magnetic part is PSD, including on the complement.
  exterior_min=g*g*lam*(N+1)**2/2
  # Offdiag from inside to outside is -1/(2g²). Each exterior
  # neighbor adjacent to cube has exactly one interior neighbor.
  # BB.T is diagonal inside with max corner 3/(4g^4).
  Bnorm_sq=3/(4*g**4)
  if exterior_min>e:
   lower=e-Bnorm_sq/(exterior_min-e)
   assert lower<=e
  else:lower=0.
  lower=max(lower,0)
  bounds.append({"N":N,"restricted_upper_E0":e,"rigorous_lower_E0":lower,
  "error_width_upper":e-lower,"exterior_kinetic_min":exterior_min,
  "exact_boundary_operator_norm_squared":Bnorm_sq})
 assert bounds[-1]["error_width_upper"]<bounds[-2]["error_width_upper"]
 rows.append({"g":g,"bound_rows":bounds,
   "combined_best_lower_bound":max(x["rigorous_lower_E0"] for x in bounds),
   "best_upper_bound":min(x["restricted_upper_E0"] for x in bounds)})
out={"status":"PASS_TOE59_CERTIFIED_THREE_LOOP_INFINITE_FLUX_BRACKETS",
"selected_octagon_Gram":G.astype(int).tolist(),"minimum_flux_quadratic_eigenvalue":lam,
"bound_derivation":"Block decompose full infinite Z³ electric rotor Hilbert into finite cube A, exterior C and boundary B. Wilson potential 3/g²-Σ(S_i+S_i†)/(2g²) is PSD. Exterior C>=c_N=g² λmin(G)(N+1)²/2. Each one-step exterior site attaches to at most one interior site, so BB† is diagonal with max boundary occupancy 3/(4g^4)=b². For full ground E<=E_A and C>=c_N>E_A, Schur/minimax yields E>=E_A-b²/(c_N-E_A), while variational E<=E_A. Also H>=0. Hence interval [max(0,E_A-b²/(c_N-E_A)),E_A] is unconditional within the selected three-loop infinite rotor.",
"rigorous_intervals":rows,
"limits":"This is a mathematical worst-case operator-norm error bound, usually much looser than observed N→N+1 differences. It excludes 1382 other native plaquettes and all dynamic fermions, so is not a full W33, thermodynamic or interacting-QED certificate.",
"prior_art":"Schur complements and variational Ritz energy enclosures are standard. Native W33 loop coupling data were first computed TOE58. Quantum electric truncation bounds are active lattice gauge prior art (e.g. Efficient truncations of lattice gauge theory for quantum simulation, Phys Rev D 2025)."}
(R/"data/w33_20261013_toe59_flux_error_bound.json").write_text(json.dumps(out,indent=2)+"\n")
print("TOE59 certified",[(r["g"],r["combined_best_lower_bound"],r["best_upper_bound"]) for r in rows])
