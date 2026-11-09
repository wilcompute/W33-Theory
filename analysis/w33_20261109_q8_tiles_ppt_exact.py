#!/usr/bin/env python3
"""Exact PPT bound-entangled Tiles witness using one W33/Q8 Clifford 8-MUB frame.

The 3x3 Tiles UPB state is known since Bennett et al., PRL 82, 5385 (1999).
Prove rho^Gamma=rho, rho>=0 and a rational dual trace-norm witness >2/3
using only Q(sqrt(3)) and exact integer arithmetic. A finite shot budget
study is deliberately an expected-count scenario, not a measured experiment.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp

from w33_20261109_q8_correlation_five import (
    frames, hermitian_basis, frame_map, probabilities, tensor_recovered,
    trace_norm, min_dual_lp
)

N_DUAL = [
    [-316478,0,-108319,0,-316478,0,111165,-880678],
    [0,86137,0,996283,0,0,0,0],
    [-108319,0,-936068,0,-108319,0,-274287,158360],
    [0,-996283,0,86137,0,0,0,0],
    [-316478,0,-108319,0,-316478,0,818272,344067],
    [0,0,0,0,0,1000000,0,0],
    [818272,0,-274287,0,111165,0,426767,-246394],
    [344067,0,158360,0,-880678,0,-246394,142256],
]


def exact_tiles():
    e=[sp.eye(3)[:,i] for i in range(3)]
    d=lambda i,j: e[i]-e[j]
    tiles=[sp.kronecker_product(e[0],d(0,1)),
           sp.kronecker_product(d(0,1),e[2]),
           sp.kronecker_product(e[2],d(1,2)),
           sp.kronecker_product(d(1,2),e[0])]
    projectors=[u*u.T/2 for u in tiles]
    stopper=sp.ones(9,1)
    projectors.append(stopper*stopper.T/9)
    assert all(sp.trace(P*Q)==(i==j)
               for i,P in enumerate(projectors) for j,Q in enumerate(projectors))
    rho=(sp.eye(9)-sum(projectors,sp.zeros(9)))/4
    assert sp.trace(rho)==1 and rho*rho==rho/4
    rho_PT=sp.Matrix(9,9,lambda i,j:
        rho[3*(i//3)+(j%3),3*(j//3)+(i%3)])
    assert rho_PT==rho  # All Tiles UPB projectors are real products.

    H=[]
    s=sp.sqrt
    for i in range(3):
        for j in range(i+1,3):
            X=sp.zeros(3);X[i,j]=X[j,i]=1/s(2);H.append(X)
            Y=sp.zeros(3);Y[i,j]=-sp.I/s(2);Y[j,i]=sp.I/s(2);H.append(Y)
    H += [sp.diag(1,-1,0)/s(2),sp.diag(1,1,-2)/s(6)]
    T=sp.simplify(sp.Matrix(8,8,lambda i,j:
        sp.trace(rho*sp.kronecker_product(H[i],H[j]))))
    assert sp.simplify(sp.trace(T.T*T)-sp.Rational(17,144))==0

    D=sp.Integer(10**6)
    W=sp.Matrix(N_DUAL)/D
    G=W.T*W
    row_upper=max(sum(abs(G[i,j]) for j in range(8)) for i in range(8))
    C=sp.Rational(1001,1000)
    assert row_upper<C*C
    # Symmetric Gram and infinity norm bound guarantee ||W||_op < C.
    # Therefore ||T||_* >= tr(W.T*T)/C.
    lower=sp.simplify(sp.trace(W.T*T)/C)
    exact_want=sp.Rational(111431,600600)*sp.sqrt(3)+sp.Rational(4982501,13104000)
    assert sp.simplify(lower-exact_want)==0
    # Rational certificate: sqrt(3)>433/250, by comparing positive squares.
    assert sp.Rational(433,250)**2<3
    lower_rational=sp.Rational(111431,600600)*sp.Rational(433,250)+sp.Rational(4982501,13104000)
    assert lower_rational>sp.Rational(2,3)
    return rho,T,dict(
        proof_status="PASS_EXACT_Q_SQRT3_BOUND_ENTANGLED_TILES",
        density_rank=4,
        purity="1/4",
        partial_transpose_equals_density_exact=True,
        five_projectors_orthonormal_exact=True,
        centered_eight_MUB_F8_exact="17/144",
        separable_trace_norm_threshold_exact="2/3",
        rational_dual_matrix_denominator=1000000,
        rational_dual_matrix_rows=N_DUAL,
        dual_operator_norm_upper_bound="1001/1000",
        gram_infinity_upper_bound_exact=str(row_upper),
        exact_dual_lower=str(lower),
        exact_dual_lower_decimal=float(lower),
        rational_lower_using_sqrt3_gt_433_over_250=str(lower_rational),
        rational_excess_over_separable=str(lower_rational-sp.Rational(2,3)),
        valid_ppt_entanglement_witness=True,
        prior_art="Bennett et al. (1999) Tiles UPB bound entanglement; CCNR/correlation witness paradigm known; new here is explicit W33/Q8 eight-setting dual certificate."
    )


def measurement_and_shot_controls(rho,T):
    _,family=frames()
    rho_n=np.array(rho).astype(float)
    operators=np.array(hermitian_basis())
    err=[];values=[]
    for E in family:
        A=frame_map(E,operators)
        p=probabilities(E,rho_n)
        rec=tensor_recovered(A,p)
        err.append(float(np.max(np.abs(rec-np.array(T).astype(float)))))
        values.append(trace_norm(rec))
    assert max(err)<3e-12
    eff=np.array([.63+.045*j for j in range(9)])
    E=family[0]
    A=frame_map(E,operators)
    p=np.array([probabilities(E[:,9*b:9*(b+1)],rho_n) for b in range(8)])
    q=p*eff[None,:];q=q/q.sum(axis=1,keepdims=True)
    rows=[]
    for rel in (.0001,.001,.01):
        low=eff*(1-rel);high=eff*(1+rel)
        for N in (100000,1000000,10000000,100000000):
            eps=math.sqrt(math.log(2*72/.05)/(2*N))
            cert=min_dual_lp(A,q,low,high,eps)
            rows.append({"efficiency_relative_uncertainty":rel,
                         "accepted_shots_per_setting":N,
                         "nominal_ideal_expected_q_used":True,
                         "simultaneous_confidence_radius":eps,
                         "conservative_lower_bound":cert["lower_bound"],
                         "detects_bound_entanglement":cert["lower_bound"]>2/3})
    return {"exact_Q8_frame_reconstruction_errors":err,
            "trace_norm_measured_by_each_coset":values,
            "realized_T_trace_norm":trace_norm(np.array(T).astype(float)),
            "expected_counts_only_design_table":rows,
            "confidence_warning":"qhat was set to expected conditional probabilities, not an observed multinomial sample; these thresholds are analytic design diagnostics, not statistical power or experimental data"}


def main(path=None):
    rho,T,exact=exact_tiles()
    measurements=measurement_and_shot_controls(rho,T)
    data={"status":"PASS_EXACT_PPT_BOUND_ENTANGLEMENT_FROM_ONE_W33_Q8_FRAME",
          "exact_certificate":exact,
          "measurement_and_shots":measurements,
          "scope":"Known Tiles UPB/PPT bound entangled state; computational test of W33 Q8 correlation analyzer, not discovery of bound entanglement or physical experiment."}
    if path:Path(path).write_text(json.dumps(data,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS PPT Tiles Q8",json.dumps({
        "rational_certified_min":float(exact["exact_dual_lower_decimal"]),
        "true_trace_norm":measurements["realized_T_trace_norm"],
        "PPT_exact":exact["partial_transpose_equals_density_exact"],
        "Q8_error":max(measurements["exact_Q8_frame_reconstruction_errors"]),
        "shot_rows":len(measurements["expected_counts_only_design_table"])
    }))
    return data


if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else None)
