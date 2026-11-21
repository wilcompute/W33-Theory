#!/usr/bin/env python3
"""Five operational/continuum falsifiers following Witting–G2 finite geometry.

Imports the PREVIOUS tested 40-ray/364-point construction, not a free-standing
invention of the projective Pauli–Witting–E8 dictionary.
Uses numpy only. Every physical coupling and optical reference is conditional.
"""
from __future__ import annotations
from collections import Counter
from itertools import combinations,product
from math import comb,sqrt,exp,log,ceil
from pathlib import Path
import json
import numpy as np
import toe_20261120_octonion_mereology_radon as B

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261120_nextfive_falsifiers.json"

def chart_action():
    planes=set()
    for u,v in combinations(B.V,2):
        if not B.sp(u,v):continue
        pl=frozenset(B.cn([(a*u[k]+b*v[k])%3 for k in range(4)])
                     for a,b in product(range(3),repeat=2) if a or b)
        assert len(pl)==4
        planes.add(pl)
    assert len(planes)==90
    charts=set()
    for pl in planes:
        perp=frozenset(v for v in B.V if all(B.sp(v,u)==0 for u in pl))
        assert perp in planes and len(perp)==4 and perp.isdisjoint(pl)
        charts.add(frozenset((pl,perp)))
    blocks=sorted((frozenset().union(*c) for c in charts),
                  key=lambda b:tuple(sorted(b)))
    assert len(blocks)==45 and len(set(blocks))==45
    M=np.array([[int(v in c) for v in B.V] for c in blocks],dtype=int)
    K=M@M.T
    assert set(M.sum(1))=={8} and set(M.sum(0))=={9}
    assert Counter(K[np.triu_indices(45,1)])=={0:270,2:720}
    eigs=Counter(int(round(x)) for x in np.linalg.eigvalsh(K))
    assert eigs=={72:1,12:24,0:20}
    A=(K==0).astype(int);np.fill_diagonal(A,0)
    assert np.array_equal(A@A,9*np.eye(45,dtype=int)+3*np.ones((45,45),dtype=int))
    source_counts=Counter()
    chosen=Counter()
    for i,j in combinations(range(40),2):
        energy=1-(M[:,i]+M[:,j])/2
        values=Counter(float(x) for x in energy)
        if B.sp(B.V[i],B.V[j]):
            assert values=={0.:1,.5:16,1.:28}
            chosen[int(np.argmin(energy))]+=1
            source_counts["noncommuting"]+=1
        else:
            assert values=={0.:3,.5:12,1.:30}
            source_counts["commuting"]+=1
    assert source_counts=={"noncommuting":540,"commuting":240}
    assert len(chosen)==45 and set(chosen.values())=={12}
    prob=1/(1+16*exp(-5)+28*exp(-10))
    assert .90<prob<.91
    # p>=0, sum p=1: pT K p <=2+6 sum p_i^2<=8.
    # Equality iff p is one of 45 unit vectors. With p=|psi|^2 this
    # defines an invariant *quartic toy* action with 45 degenerate vacua.
    rng=np.random.default_rng(20261120)
    for _ in range(200):
        p=rng.dirichlet(np.ones(45))
        assert p@K@p<8
    return dict(charts=45,points=40,K_spectrum=dict(eigs),
        K_offdiagonal_counts={"disjoint":270,"intersection_two":720},
        M_rank=int(np.linalg.matrix_rank(M)),
        disjoint_graph_srg=[45,12,3,3],
        all_noncmt_pairs=540,unique_pairs_per_chart=12,
        source_spectra={"noncommuting":[1,16,28],"commuting":[3,12,30]},
        source_ground_probability_beta10=prob,
        conditional_source_gap=.5,
        sufficient_adversarial_operator_perturbation_norm_bound=.25,
        invariant_action="V(psi)=-J/2 sum_FG K_FG abs(psi_F)^2 abs(psi_G)^2",
        invariant_action_global_vacua=45,identical_vacuum_energy_minus_J_units=-4,
        vacuum_amplitude_quadratic_fluctuation_coefficients={"6J":32,"8J":12},
        requirement="J>0 and sum_F abs(psi_F)^2=1; physically motivated J and an actual chart field are not derived")

def exceptional_projection():
    points=sorted({B.cn(v) for v in product(range(3),repeat=7) if any(v)})
    def q(v):return (-v[0]*v[0]-sum(v[1+k]*v[4+k] for k in range(3)))%3
    quadric=[v for v in points if q(v)==0]
    assert len(points)==1093 and len(quadric)==364
    results=Counter();fibers={}
    for w in points:
        kind=q(w)
        if kind==0:
            results["quadric_center_undefined"]+=1
            continue
        j=next(i for i,x in enumerate(w) if x)
        images=Counter(B.cn(tuple((v[k]-v[j]*w[k])%3 for k in range(7)))
                       for v in quadric)
        typ=(kind,len(images))
        results[typ]+=1
        if kind not in fibers:fibers[kind]=Counter(images.values())
        assert max(images.values())==2
    assert results=={"quadric_center_undefined":364,(1,238):351,(2,247):378}
    assert fibers[1]=={1:112,2:126} and fibers[2]=={1:130,2:117}
    return dict(centers_tested=1093,isotropic_centers_undefined=364,
        norm1_centers=351,norm1_distinct_images=238,
        norm2_centers=378,norm2_distinct_images=247,
        norm1_fibers={"single":112,"double":126},
        norm2_fibers={"single":130,"double":117},
        result="no surjective LINEAR 7-to-6 quotient of natural Q(6,3) injective on all 364 points",
        caveat="Does not rule out arbitrary non-linear bijections, different realizations or weaker operator correspondences")

def tomography():
    S=sum(B.Pi.values())
    err=float(np.linalg.norm(S-(13*B.I+3*B.P)))
    assert err<1e-10
    pe=(B.I+B.P)/2;po=(B.I-B.P)/2
    assert np.linalg.norm(S/40-(.4*pe+.25*po))<1e-10
    eye3=np.eye(3)
    p3=np.zeros((3,3))
    for i in range(3):p3[-i%3,i]=1
    assert np.array_equal(B.P,np.kron(p3,p3))
    mu=1/9; p=(13+3*mu)/40
    randomized_var_mu=(40/3)**2*p*(1-p)
    direct_var_mu=1-mu*mu
    ratio=randomized_var_mu/direct_var_mu
    assert abs(ratio-40)<1e-10
    n_hoeff=ceil(log(100)/(2*(13/40-1/4)**2))
    n_parity=ceil(log(.01)/log(.5))
    assert n_hoeff==410 and n_parity==7
    return dict(projector_sum_error=err,
        randomized_binary_effect="0.4 P_even + 0.25 P_odd",
        classical_parity_garbling_rates={"even":.4,"odd":.25},
        physical_parity_is_local_tensor_product=True,
        maxmixed_variance_ratio_randomized_to_direct=ratio,
        target_ideal_odd_cell_1pct_Hoeffding_randomized=410,
        target_ideal_odd_cell_1pct_all_odd_direct=7,
        limitation="Requires comparable detector costs and discarding direction and nonbinary information; not a security or universal tomography theorem")

def phase_reference():
    z=np.exp(2j*np.pi/6)
    psi=np.array([1,0],complex)
    error=max(float(np.linalg.norm(np.outer(z**k*psi,np.conjugate(z**k*psi))-
                                    np.outer(psi,psi.conj()))) for k in range(6))
    assert error<1e-12
    def pgm(n):
        spectrum=[6*sum(comb(n,k) for k in range(r,n+1,6))/2**n
                  for r in range(6)]
        return sum(sqrt(x) for x in spectrum)**2/36,spectrum
    vals={str(n):pgm(n)[0] for n in (1,2,3,4,5,8,12,14,16,20)}
    for n in range(1,6):
        gram=np.array([[((1+z**(j-i))/2)**n for j in range(6)]
                       for i in range(6)])
        assert np.allclose(sorted(np.linalg.eigvalsh(gram)),sorted(pgm(n)[1]),atol=1e-12)
    assert abs(vals["1"]-1/3)<1e-12
    first=next(n for n in range(1,50) if pgm(n)[0]>.99)
    assert first==14
    return dict(global_phase_projector_error=error,
        no_reference_best_guess=1/6,
        hypothetical_coherently_referenced_one_copy_PGM_success=vals["1"],
        hypothetical_coherently_referenced_two_copy_PGM_success=vals["2"],
        hypothetical_coherently_referenced_fourteen_copy_PGM_success=vals["14"],
        hypothetical_PGM_success_by_copy_count=vals,
        first_hypothetical_copy_count_above_99pct=first,
        assumption="An external *physical* phase reference encodes six DIFFERENT equatorial qubit states",
        no_go="Six global scalar root phases of the SAME Witting ray remain one identical quantum density matrix, with no observable label to recover")

def continuum():
    spectra={"W33":([0,10,16],[1,24,15]),"H3":([0,7,13,16],[1,104,168,91])}
    times=np.logspace(-4,2,1500)
    def dim(t,L,m):
        weights=[n*exp(-t*l) for l,n in zip(L,m)]
        return 2*t*sum(l*v for l,v in zip(L,weights))/sum(weights)
    peaks={}
    for name,(L,m) in spectra.items():
        d=np.array([dim(t,L,m) for t in times])
        k=int(np.argmax(d))
        peaks[name]={"peak":float(d[k]),"time":float(times[k])}
    assert peaks["W33"]["peak"]<4<peaks["H3"]["peak"]
    examples={str(q):{"W_diam_edge1overq":2/q,"H_diam_edge1overq":3/q,
            "W_GromovHausdorff_lower_bound_to_unit_diameter":abs(1-2/q)/2,
            "H_GromovHausdorff_lower_bound_to_unit_diameter":abs(1-3/q)/2}
            for q in (3,5,7,11,31,101)}
    return dict(point_graph_diameters={"W(3,q)":2,"H(q)":3},
        metric_edge_length="1/q",metric_diameter_as_q_grows=0,
        GH_distance_lower_bound_to_any_unit_diameter_compact_space_limit=.5,
        computed_heat_spectral_dimension_peaks=peaks,
        samples=examples,
        prior_repo="w33_20261009_toe21_qfamily_heat_nogo.py and 2026-11-18_sixfront_character_winding_continuum_falsifiers.md",
        caveat="Ordinary graph-shortest-path/Gromov-Hausdorff metric only, not a no-go for causal/Lorentzian or nonlocal multiscale limits")

def run(write=True):
    data=dict(status="PASS_FIVE_FOLLOWTHROUGH_GATES",
        selection=chart_action(),exceptional=exceptional_projection(),
        tomography=tomography(),reference=phase_reference(),continuum=continuum(),
        scientific_status="Reproducible finite geometry and conditional operational falsifiers, not a Theory of Everything or hardware experiment")
    if write:
        OUT.parent.mkdir(parents=True,exist_ok=True)
        OUT.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n",encoding="utf8")
    return data

if __name__=="__main__":
    r=run()
    print("PASS",r["selection"]["invariant_action_global_vacua"],
          r["exceptional"]["centers_tested"],
          r["tomography"]["maxmixed_variance_ratio_randomized_to_direct"])
