#!/usr/bin/env python3
"""Independent archaeology-driven controls: dimensional KO, gravity closure,
strong-CP/weak-CP separation, and hardware shot-time objective.

Companion orbit-frame producer addresses equivariant spectral sparsification.
These are bounded *conditional* mathematical and engineering controls, not an
emergent physical TOE or novelty claim over historical material.
"""
from __future__ import annotations
import importlib.util
import json,math
from pathlib import Path
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261104_archaeological_fivefront_controls.json"

def imp(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m
base=imp("w33_arch_base","analysis/2026_11_03_optimal_5load_apartment_hamiltonian.py")

def dimension():
    history=(ROOT/"analysis"/"w33_spacetime_dimension_from_KO.py").read_text(encoding="utf8")
    assert "eps, epsp, epspp = +1, +1, -1" in history
    assert "ko_total = 2" in history
    admissible=[d for d in range(0,65) if (d+6)%8==2]
    assert admissible[:5]==[4,12,20,28,36]
    return dict(status="PASS_CONDITIONAL_KO_4_MOD_8_NONUNIQUENESS",
        finite_KO_dimension_assumed_from_prior=6,
        total_Pfaffian_KO_dimension_assumed=2,
        allowed_spacetime_dimensions_up_to_64=admissible,
        n_distinct_solutions_up_to_64=len(admissible),
        historic_python_sets_KO_signs_by_literal_assignment=True,
        conditional_theorem="If KO(F)=6 and KO(MxF)=2 mod 8 for a spin manifold M, then dim(M)=4 mod 8, not uniquely 4.",
        nonemergence="Selection of the minimal representative 4, spin manifold existence, metric, causality, dynamics and spectral dimension are additional premises.",
        prior_owner="analysis/W33_SPACETIME_DIMENSION_FROM_KO.md (June 2026), which currently uses stronger 'forced 4D' language.")

def gravity(D,C):
    indices,load=base.choose(C,seed=33)
    B=C[:,indices].astype(np.int64)
    assert B.shape==(160,81) and np.array_equal(D@B,np.zeros((80,81),dtype=np.int64))
    a,b=0,20
    u=B[:,a];v=B[:,b]
    assert int(u@v)==1 and int(((u!=0)&(v!=0)).sum())==1
    assert int(u@u)==8 and int(v@v)==8
    # Exact rational x=(u+v)/9, p=(u-v)/7.
    numerator_x=u+v;numerator_p=u-v
    assert int(u@numerator_x)==9 and int(v@numerator_x)==9
    assert int(u@numerator_p)==7 and int(v@numerator_p)==-7
    assert not np.any(D@numerator_p)
    # g_i=(c_i.x)^2-(c_i.p)^2 -> g_a=g_b=0, but bracket nonzero.
    g_a=sp.Rational(int(u@numerator_x),9)**2-sp.Rational(int(u@numerator_p),7)**2
    g_b=sp.Rational(int(v@numerator_x),9)**2-sp.Rational(int(v@numerator_p),7)**2
    bracket=4*sp.Integer(int(u@v))*(sp.Rational(int(u@numerator_x),9)*
                 sp.Rational(int(v@numerator_p),7)-
                 sp.Rational(int(u@numerator_p),7)*sp.Rational(int(v@numerator_x),9))
    assert (g_a,g_b,bracket)==(0,0,-8)
    # The full indefinite 81-constraint zero surface contains nontrivial x=p=u.
    # For all j, (cj.x)^2-(cj.p)^2=0; Dp=0.
    common_x=u;common_p=u
    vals=(B.T@common_x)**2-(B.T@common_p)**2
    assert not np.any(vals) and not np.any(D@common_p)
    assert np.linalg.norm(B.T@common_x)>1
    return dict(status="PASS_INDEFINITE_REPAIRS_ZERO_LOCUS_BUT_NOT_PAIRWISE_FIRST_CLASS",
        exact_two_constraint_witness_indices=[a,b],
        x_formula="(c0+c20)/9",p_formula="(c0-c20)/7",
        gauss_dp_zero_exact=True,two_indefinite_constraints_zero_exact=True,
        two_constraint_Poisson_bracket_exact=str(bracket),
        full_common_indefinite_constraint_surface_has_nonpure_gauge_cycle_point=True,
        common_zero_witness="x=p=c0, with nonzero cycle component; all 81 g_i vanish and Dp=0",
        limitation="Pairwise closure fails into the two selected constraints plus Gauss at a point where those two vanish. Other 79 g_k at that point need not vanish; no full Dirac algebra/no Einstein action claimed.")

def flavor():
    I=sp.I
    Y=sp.diag(1,2,4)
    v=sp.Matrix([1,1,1+I])
    M=Y.row_join(v).col_join(v.T.row_join(sp.Matrix([[3]])))
    det=sp.expand(M.det())
    assert det==12-4*I
    theta=sp.arg(det)
    assert sp.simplify(theta+sp.atan(sp.Rational(1,3)))==0
    Yu=Y;Yd=Y-v*v.T/3
    Hup=Yu*Yu.conjugate().T
    Hd=Yd*Yd.conjugate().T
    CP=sp.simplify(sp.im(sp.trace((Hup*Hd-Hd*Hup)**3)))
    assert CP==1600
    # Historical 11951 Nelson-Barr example (exactly real determinant).
    m=sp.Matrix([[1,1,0],[0,2,1],[1,0,3]])
    B=sp.Matrix([[1+I,2-I,1+2*I]])
    mu=sp.Integer(2)
    N=m.row_join(sp.zeros(3,1)).col_join(B.row_join(sp.Matrix([[mu]])))
    denom=sp.simplify(mu**2+(B*B.conjugate().T)[0])
    Hnb=sp.simplify(m*m.T-m*B.conjugate().T*B*m.T/denom)
    Jnb=sp.simplify(sp.im(Hnb[0,1]*Hnb[1,2]*Hnb[2,0]))
    assert N.det()==14 and Jnb==sp.Rational(119,64)
    # An aligned real diagonal bare down-sector + one heavy vector produces
    # a rank-one Hermitian correction: the rephasing-invariant triple is real.
    Md=sp.diag(1,2,4)
    Ha=sp.simplify(Md*Md.T-Md*B.conjugate().T*B*Md/denom)
    Ja=sp.simplify(sp.im(Ha[0,1]*Ha[1,2]*Ha[2,0]))
    assert Ja==0
    return dict(status="PASS_STRONG_CP_AUDIT_AND_ALIGNED_RANK_ONE_FLAVOR_NO_GO",
        previous_symmetric_4x4_toy_determinant=str(det),
        previous_symmetric_toy_arg_det_radians=float(sp.N(theta,16)),
        previous_symmetric_toy_weak_CP_cubed_trace=str(CP),
        previous_symmetric_toy_nelson_barr_structure=False,
        previous_symmetric_toy_strong_CP_safe_if_bare_theta_zero=False,
        historic_11951_parity_compatible_alternative_owner="analysis/PASS11950_11951_STRONG_CP_COMPLETION.md",
        historic_11951_triangular_determinant_exact=str(N.det()),
        historic_11951_nonzero_Jarlskog_like_triple=str(Jnb),
        aligned_diagonal_real_bare_Y_and_single_B_triplet_imaginary_invariant_exact=str(Ja),
        aligned_no_go="For real diagonal m and one heavy mixing row B, Hd_ij=-mi*mj*conj(Bi)*Bj/(mu²+|B|²) for i!=j, so Im(H12 H23 H31)=0. Real light-sector misalignment or more independent structure is needed.",
        limitation="The strong-CP phase is physical only if the toy mass matrix represents the full colored sector and bare theta is not tuned to cancel it. Nelson-Barr 11951 is established repo prior art and still requires a gauge/vacuum/radiative completion.")

def hardware():
    previous=json.loads((ROOT/"data"/"toe_20261104_fivefront_hard_falsifiers.json").read_text(encoding="utf8"))
    h=previous["hardware"]
    seq=h["noisy_sequential_compile_results"]
    assert h["noisy_sequential_compile_best_depth_in_sample"]==16
    kref=.1;z=5
    points=[]
    for row in seq:
        t=float(row["total_physical_duration"])
        delta=float(row["coherent_phase_contrast"])
        eff=delta*math.exp(-kref*t/2)
        if eff==0:
            shots=None;effort=None
        else:
            shots=math.ceil(2*z*z/(eff*eff))
            effort=2*shots*t
        points.append(dict(steps=int(row["steps"]),pulses=int(row["pulses"]),
            physical_duration_per_shot=t,ideal_reference_contrast=delta,
            reference_dephasing_rate=kref,
            reference_dephased_contrast=eff,
            approximate_5sigma_shots_per_flux_setting=shots,
            idealized_total_interrogation_time_for_both_flux_settings=effort))
    valid=[p for p in points if p["steps"]>1]
    fastest=min(valid,key=lambda p:p["idealized_total_interrogation_time_for_both_flux_settings"])
    assert fastest["steps"]==8
    assert points[4]["steps"]==16
    return dict(status="PASS_HARDWARE_RESOURCE_METRIC_CHANGES_OPTIMAL_DEPTH",
        previously_optimized_target="absolute signal approximation error against noisy simultaneous-Hamiltonian target; best 16 slices",
        new_optimized_target="idealized total interrogation time to distinguish flux settings at 5 Gaussian standard deviations; best 8 slices",
        chosen_reference_dephasing_rate=kref,
        sigma_goal=z,
        shots_per_setting_formula="N=ceil(2*z²/delta_eff²); assumes two independent +/-1 expectation estimators, asymptotic normal approximation and variance ≤1.",
        shot_and_latency_budgets=points,
        best_sampled_steps=int(fastest["steps"]),
        best_sampled_pulses=int(fastest["pulses"]),
        boundary="No readout/reset latency, no shot overhead, reference phase drift, pulse crosstalk or detector inefficiency. Not a hardware-specific prescription and shot estimate is asymptotic, not a rigorous finite-sample p-value.")

def main():
    D,C,_=base.build()
    out=dict(status="PASS_FOUR_ARCHAEOLOGICAL_HARD_CONTROLS_PLUS_C3_ORBIT_PRODUCER",
        dimension=dimension(),gravity=gravity(D,C),flavor=flavor(),hardware=hardware(),
        corpus_prior_art="data/toe_20261104_corpus_archaeology.json",
        orbit_producer="analysis/toe_20261104_c3_orbit_sparsification.py",
        boundary="Only finite mathematical counterexamples, systematic historical provenance and conditional noise benchmarks; no full TOE.")
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(out["status"],"KO",out["dimension"]["allowed_spacetime_dimensions_up_to_64"][:4],
        "bracket",out["gravity"]["two_constraint_Poisson_bracket_exact"],
        "det",out["flavor"]["previous_symmetric_4x4_toy_determinant"],
        "shot_best",out["hardware"]["best_sampled_steps"],flush=True)
    return out
if __name__=="__main__":main()
