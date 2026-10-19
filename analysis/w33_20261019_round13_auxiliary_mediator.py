"""Microscopic bounded Gaussian-adjoint mediator: derive induced sign
and determine how much of the 17-class vacuum orbital algebra
this simple local coupling resolves. Exact sign; numerical overlap.
"""
from __future__ import annotations
import json,itertools
from pathlib import Path
import numpy as np
from w33_20261019_round8_clifford_vacuum_orbit import basis
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round13_auxiliary_mediator.json"
def run():
    pairs=[(9*h+a,9*h+b) for h in range(40) for a,b in itertools.combinations(range(9),2)]
    old=json.loads((ROOT/"data/w33_20261019_round10_pair_orbit_schreier.json").read_text())
    q0=np.asarray(basis[0,0]+basis[0,1],complex)
    c0=q0-(2/9)*np.eye(9)
    rows=[]
    for group in old["stabilizer_pair_orbits"]:
        idx=group["representative"];a,b=pairs[idx]
        Q=np.asarray(basis[a//9,a%9]+basis[b//9,b%9],complex)
        c=Q-(2/9)*np.eye(9)
        ov=float(np.trace(q0@Q).real)
        quart=float(np.trace(q0@Q@q0@Q).real)
        comm=float(np.linalg.norm(q0@Q-Q@q0)**2)
        rows.append({"class_representative":idx,"class_size":group["size"],
          "tr_Q0Q":ov,"tr_Q0Q_Q0Q":quart,
          "commutator_norm_squared":comm,
          "gaussian_mediator_pair_cross_coefficient_at_g2_over_m2_eq_1":float(-np.trace(c0@c).real)})
    rounded=lambda x:round(x,8)
    overlap_classes=len(set(rounded(r["tr_Q0Q"]) for r in rows))
    quart_classes=len(set((rounded(r["tr_Q0Q"]),rounded(r["tr_Q0Q_Q0Q"])) for r in rows))
    comm_classes=len(set((rounded(r["tr_Q0Q"]),rounded(r["commutator_norm_squared"])) for r in rows))
    # Full positive definite real Hermitian traceless scalar field X:
    # V[X,w]= m²/2 Tr X² -g Tr X J(w); J=Σw(Q-2I/9).
    # Completing square gives V_eff=-g²/(2m²)Tr J².
    # All rank2 Q have Tr (Q-2I/9)² =14/9.
    single=float(np.trace(c0@c0).real)
    rng=np.random.default_rng(1313)
    ps=[]
    for _ in range(120):
        sel=rng.choice(1440,size=4,replace=False)
        w=rng.dirichlet(np.ones(4))
        J=np.zeros((9,9),complex)
        for (idx,wi) in zip(sel,w):
            a,b=pairs[idx]
            J+=wi*(basis[a//9,a%9]+basis[b//9,b%9]-(2/9)*np.eye(9))
        ps.append(float(np.trace(J@J).real))
    checks={"17_pair_classes_from_prior_exact_orbits":len(rows)==17,
      "Gaussian_mediator_induces_negative_pair_trace":all(abs(r["gaussian_mediator_pair_cross_coefficient_at_g2_over_m2_eq_1"]- (4/9-r["tr_Q0Q"]))<1e-9 for r in rows),
      "constant_single_Qcentered_norm_14_over9":abs(single-14/9)<1e-10,
      "120_sampled_mixture_quadratic_norm_bounded_by_single":max(ps)<=single+1e-9,
      "commutator_equals_twice_overlap_minus_twice_quartic":all(abs(r["commutator_norm_squared"]-2*(r["tr_Q0Q"]-r["tr_Q0Q_Q0Q"]))<1e-8 for r in rows)}
    out={"schema":"w33.round13.positive_Gaussian_adjoint_mediator_induced_vacuum_orbit_kernel.v1",
      "microscopic_toy_action":"For a positive-mass real Hermitian traceless 9x9 auxiliary bosonic matrix X and vacuum mixture J(w)=Σ_a w_a(Q_a-2I/9), set V(X,w)=m²/2 Tr(X²)-g Tr[X J(w)]. The unique stable stationary value X*=(g/m²)J induces V_eff(w)=-(g²/2m²)Tr[J(w)²]. Hence pair coefficient equals -(g²/m²)[Tr(Q_a Q_b)-4/9]. This derives a NEGATIVE overlap interaction from a specified stable auxiliary field, but NOT a negative W33 PAULI commutator coefficient or fundamental spacetime mechanism.",
      "critical_no_go":"Because all 1440 Q have equal centered norm²=14/9 and Tr||Σ wQc||²<=Σw||Qc||²=14/9, the attractive Gaussian mediator cannot energetically favor a dispersed multi-vacuum mixture over a pure vacuum at fixed weight simplex: singleton is already an absolute minimum of V_eff. Its kernel only depends on 7 distinct overlap values and cannot resolve all 17 stabilizer orbits.",
      "fixed_reference_classes":rows,"num_17_orbits":len(rows),
      "distinct_overlap_values":overlap_classes,"distinct_overlap_and_quartic_signatures":quart_classes,
      "distinct_overlap_and_commutator_signatures":comm_classes,
      "single_centered_norm_sq":single,
      "sampled_max_mixed_norm_sq":max(ps),
      "physics_limitations":"X is an explicit engineered auxiliary scalar, not experimentally identified. Correct gauge and spatial kinetic dynamics/quantization and sign of any required repulsive or commutator interaction remain open. Coincident invariants in separate stabilizer orbits prohibit full 17-class identification by trace-overlap alone.",
      "checks":checks,"all_checks_pass":all(checks.values())}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"pass":out["all_checks_pass"],"orbit_classes":len(rows),"overlap":overlap_classes,"quartic":quart_classes,"comm":comm_classes}))
    return out
if __name__=="__main__":run()
