#!/usr/bin/env python3
"""Five independently checkable constraints on W33/TOE hypotheses.

F1: exact uniform-subdivision eigenvalue equation and 1/L correction.
F2: C3-equivariant frame-weight tuning vs dense all-apartment projector.
F3: positivity makes the proposed 81 quadratic "GR constraints" trivial.
F4: vectorlike Schur complement opens a nonzero CP spurion loophole.
F5: 5-level Lindblad Ramsey witness, plus a three-coupler Trotter compilation.

Finite mathematics and toy quantum simulation only. Not a TOE, GR action,
measured masses, physical cosmology, or a demonstrated hardware device.
"""
from __future__ import annotations
import importlib.util
import json, math
from pathlib import Path
import numpy as np
import sympy as sy
from scipy.optimize import brentq, minimize
from scipy.linalg import expm

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261104_fivefront_hard_falsifiers.json"

def import_from(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

base=import_from("base_w33","analysis/2026_11_03_optimal_5load_apartment_hamiltonian.py")
c3=import_from("c3_prev","analysis/toe_20261103_c3_symmetry_selector.py")

def continuum():
    mu=math.sqrt(6)
    a=math.acos(mu/4)
    target=a*a
    rows=[]
    for L in (1,2,4,8,16,32,64,128,256):
        def characteristic(theta):
            return (4*math.cos(L*theta)+2*math.tan(theta/2)*math.sin(L*theta)-mu)
        theta=brentq(characteristic,1e-14,math.pi/L,xtol=1e-14)
        eig=2*(1-math.cos(theta))
        scaled=L*L*eig
        rows.append(dict(segments=L,subdivision_vertices=80+160*(L-1),
            edges=160*L,cycle_rank=81,laplacian_eigenvalue=eig,
            rescaled_first_gap=scaled,
            asymptotic_coefficient_L_times_relative_error=L*(scaled/target-1),
            analytic_first_order_prediction=target*(1+1/(2*L))))
    assert abs(rows[5]["rescaled_first_gap"]-0.844388698793618)<1e-9
    assert abs(rows[-1]["asymptotic_coefficient_L_times_relative_error"]-0.5)<.001
    return dict(status="PASS_EQUIDISTANT_EDGE_SUBDIVISION_FINITE_SIZE_LAW",
        underlying_W33_Levi_adjacency_eigenvalue=mu,
        original_graph_valency=4,first_gap_metric_graph_target=target,
        exact_characteristic="sqrt(6) = 4*cos(L*theta)+2*tan(theta/2)*sin(L*theta); lambda=2-2cos(theta)",
        asymptotic_formula="L^2 lambda_1(L) = alpha^2 * (1+1/(2L)+O(1/L^2)); alpha=acos(sqrt(6)/4)",
        results=rows,
        boundary="Same fixed metric-graph topology under subdivision: one-dimensional Weyl law, not generated 3+1 dimensions.")

def signed_basis(D,C,supports):
    known={tuple(np.flatnonzero(C[:,j]).tolist()):C[:,j] for j in range(C.shape[1])}
    B=np.stack([known[tuple(s)] for s in supports],axis=1).astype(np.int64)
    assert B.shape==(160,81) and not np.any(D@B)
    return B

def symmetry(D,C):
    picked,_=base.choose(C,seed=33)
    Q,_=np.linalg.qr(C[:,picked].astype(float))
    mats=[];Hs=[];constituents=[]
    for seed in (5,9,18):
        witness=c3.certificate(seed=seed,save=False)
        assert witness["C3_H_invariant"] and witness["max_flag_load"]==6
        B=signed_basis(D,C,witness["selected_apartment_flag_supports"])
        H=B@B.T
        Hs.append(H)
        mats.append((Q.T@H@Q+Q.T@H.T@Q)/2)
        constituents.append(dict(seed=seed,cycle_rank=81,max_flag_load=6))
    fullK=C@C.T
    assert np.array_equal(fullK@fullK,160*fullK)
    assert not np.any(D@fullK)
    full_nnz=int(np.count_nonzero(np.triu(fullK,1)))
    full_degree=int(np.max(np.count_nonzero(fullK,axis=1)-1))
    full_eig=np.linalg.eigvalsh(Q.T@fullK@Q)
    assert np.allclose(full_eig,160,atol=1e-8)
    M=np.stack(mats)
    def fun(x):
        w=np.array([x[0],x[1],3-x[0]-x[1]])
        if min(w)<=0:return 10000+1000*abs(min(w))
        ev=np.linalg.eigvalsh(np.tensordot(w,M,axes=(0,0)))
        if min(ev)<=0:return 10000
        return float(ev[-1]/ev[0])
    rng=np.random.default_rng(44)
    runs=[]
    initial=[(1.,1.)]+[tuple(np.array([.4,.4])+2.2*rng.dirichlet([2,2,2])[:2]) for _ in range(4)]
    for x0 in initial:
        opt=minimize(fun,x0,method="SLSQP",bounds=[(.05,2.9)]*2,
                     constraints=[{"type":"ineq","fun":lambda x: 2.95-x[0]-x[1]}],
                     options=dict(ftol=1e-11,maxiter=160))
        runs.append((float(opt.fun),list(map(float,opt.x)),bool(opt.success)))
    result=min(runs,key=lambda z:z[0])
    w=[result[1][0],result[1][1],3-sum(result[1])]
    unweighted=fun([1.,1.])
    weighted=result[0]
    assert weighted<=unweighted+1e-8
    Hw=sum(float(a)*mat for a,mat in zip(w,Hs))
    H_unweighted=sum(Hs)
    w_nnz=int(np.count_nonzero(np.triu(abs(Hw)>1e-9,1)))
    u_nnz=int(np.count_nonzero(np.triu(H_unweighted,1)))
    w_deg=int(np.max(np.count_nonzero(abs(Hw)>1e-9,axis=1)-1))
    return dict(status="PASS_C3_WEIGHT_TUNING_AND_FULL_PROJECTOR_CONTROL",
        selected_C3_frame_seeds=[5,9,18],
        each_frame_exact_C3_invariant_and_cycle_preserving=True,
        unweighted_three_frame_condition_number=unweighted,
        optimized_weight_sum=3.,sampled_optimal_weights=w,
        sampled_optimized_condition_number=weighted,
        relative_condition_improvement=unweighted/weighted,
        unweighted_frame_hopping_pairs=u_nnz,
        weighted_frame_hopping_pairs=w_nnz,
        weighted_frame_max_offdiagonal_neighbors=w_deg,
        optimizer_start_results=[dict(condition=r[0],weights_first_two=r[1],success=r[2]) for r in runs],
        all_apartments=1620,all_apartments_exact_cycle_operator="C C^T = 160 P_cycle",
        all_apartment_frame_condition_number=float(full_eig[-1]/full_eig[0]),
        all_apartment_undirected_hopping_pairs=full_nnz,
        all_apartment_max_offdiagonal_neighbors=full_degree,
        boundary="Weights and C3 chosen by optimizer, not by a derived physical variational action; finite carrier only.")

def gravity(D,C):
    chosen,load=base.choose(C,seed=33)
    B=C[:,chosen].astype(np.int64)
    assert B.shape==(160,81) and not np.any(D@B)
    assert min(load)>0 and len(load)==160
    assert np.linalg.matrix_rank(D.astype(float))==79
    assert np.linalg.matrix_rank(B.astype(float))==81
    assert not np.any(B.T@D.T)
    rng=np.random.default_rng(28)
    alpha=rng.integers(-2,3,size=80)
    x=D.T@alpha
    p=np.zeros(160,dtype=np.int64)
    gradX=B.T@x
    active=(np.abs(B).T@(p*p))
    h=(gradX*gradX+active)/2
    assert np.array_equal(h,np.zeros(81))
    for i in range(160):
        assert np.any(B[i])  # union of supports covers all momentum coordinates
    # If each h_i=0, its two nonnegative components vanish separately.
    # All momentum entries occur in some cycle => p=0.
    # B is a basis of ker D, so B^T x=0 => x in im D^T.
    return dict(status="PASS_QUADRATIC_CONSTRAINT_TRIVIAL_ZERO_LOCUS",
        cycle_rank=81,incidence_rank=79,positive_local_constraints=81,
        supported_edges=160,minimum_edge_participation=int(min(load)),
        explicit_pure_gauge_zero_witness=True,
        theorem="For h_i=(c_i.x)^2/2+sum_{e in supp(ci)}p_e^2/2, h_i=0 for all 81 iff p=0 and x=D^T phi; reduced zero surface modulo x gauge shifts is a single point.",
        proof="Every h_i is sum of nonnegative real squares; all supports cover all 160 edges; B spans ker D and im D^T=(ker D)^perp.",
        boundary="No-go ONLY for these positive cycle quadratic densities treated simultaneously as zero constraints. Does not preclude Einstein/Regge/ADM gravity.")

def flavor():
    I=sy.I
    Yu=sy.diag(1,2,4)
    v=sy.Matrix([1,1,1+I])
    heavy=sy.Integer(3)
    M=Yu.row_join(v).col_join(v.T.row_join(sy.Matrix([[heavy]])))
    effective=Yu-v*v.T/heavy
    assert effective==effective.T
    assert sy.simplify(M.det()/heavy-effective.det())==0
    up=Yu*Yu.conjugate().T
    down=effective*effective.conjugate().T
    comm=up*down-down*up
    cp=sy.simplify(sy.im(sy.trace(comm**3)))
    assert cp==1600
    real_v=sy.Matrix([1,1,2])
    real_down=Yu-real_v*real_v.T/3
    real_h=real_down*real_down.conjugate().T
    assert sy.im(sy.trace((up*real_h-real_h*up)**3))==0
    vc=v.conjugate()
    conj_down=Yu-vc*vc.T/heavy
    conj_h=conj_down*conj_down.conjugate().T
    opposite=sy.im(sy.trace((up*conj_h-conj_h*up)**3))
    assert opposite==-cp
    return dict(status="PASS_VECTORLIKE_SCHUR_CP_COUNTEREXAMPLE",
        bare_one_spurion_matrix=[["1","0","0"],["0","2","0"],["0","0","4"]],
        new_flavor_mix_vector=[str(a) for a in v],
        heavy_mass=str(heavy),effective_Yd=[[str(z) for z in row] for row in effective.tolist()],
        effective_rank_one_update=True,exact_block_determinant_identity=True,
        CP_odd_commutator_imag_cubed_trace=str(cp),
        real_flavor_vector_CP_invariant=0,
        conjugated_vector_CP_invariant=str(opposite),
        boundary="The vectorlike mixing vector v is a second independent flavor-sensitive spurion. This does not derive v, explain observed flavor, or refute the strict one-spurion no-go.")

def h_triangle(flux):
    H=np.zeros((5,5),dtype=float)
    H[1,2]=H[2,1]=flux
    H[1,3]=H[3,1]=1.
    H[2,3]=H[3,2]=1.
    return H

def liouvillian(H, gamma, kappa):
    n=len(H);I=np.eye(n,dtype=complex)
    Li=-1j*(np.kron(I,H)-np.kron(H.T,I))
    for site in (1,2,3):
        loss=np.zeros((n,n),dtype=complex);loss[4,site]=math.sqrt(gamma)
        dephase=np.zeros((n,n),dtype=complex);dephase[site,site]=math.sqrt(kappa)
        for L in (loss,dephase):
            N=L.conj().T@L
            Li+=np.kron(L.conj(),L)-.5*(np.kron(I,N)+np.kron(N.T,I))
    return Li

def density(H,gamma,kappa,time):
    psi=np.zeros(5);psi[0]=psi[1]=1/math.sqrt(2)
    rho=np.outer(psi,psi)
    evolved=expm(time*liouvillian(H,gamma,kappa))@rho.reshape(-1,order="F")
    return evolved.reshape((5,5),order="F")

def trotter(flux,t,n):
    h=np.zeros((3,3),dtype=float)
    h[0,1]=h[1,0]=flux
    h[0,2]=h[2,0]=1
    h[1,2]=h[2,1]=1
    edgeM=[]
    for a,b in ((0,1),(0,2),(1,2)):
        edge=np.zeros((3,3),dtype=float)
        edge[a,b]=edge[b,a]=h[a,b]
        edgeM.append(expm(-1j*t*edge/n))
    step=edgeM[0]@edgeM[1]@edgeM[2]
    U=np.linalg.matrix_power(step,n)
    Uexact=expm(-1j*t*h)
    return U,Uexact

def compiled_lindblad(flux,n,deadtime=.003,gamma=.1,kappa=.1,time=.4):
    """Three signed-edge Lindblad pulses per slice, with idle noise overhead."""
    H=h_triangle(flux)
    idle=expm(deadtime*liouvillian(np.zeros((5,5)),gamma,kappa))
    full_slice=np.eye(25,dtype=complex)
    for a,b in ((1,2),(1,3),(2,3)):
        edge=np.zeros((5,5),dtype=float)
        edge[a,b]=edge[b,a]=H[a,b]
        link=expm(time/n*liouvillian(edge,gamma,kappa))
        full_slice=idle@link@full_slice
    psi=np.zeros(5);psi[0]=psi[1]=1/math.sqrt(2)
    initial=np.outer(psi,psi).reshape(-1,order="F")
    evolved=np.linalg.matrix_power(full_slice,n)@initial
    density=evolved.reshape((5,5),order="F")
    assert abs(np.trace(density)-1)<1e-11
    assert np.linalg.eigvalsh(density).min()>-1e-12
    return density

def hardware():
    t=.4
    scenarios=[]
    refcontrast=None
    for loss,phase in ((0,0),(.1,0),(0,.1),(.1,.1),(.5,.2)):
        a=density(h_triangle(1),loss,phase,t)
        b=density(h_triangle(-1),loss,phase,t)
        contrast=abs(float(2*(a[0,1]-b[0,1]).imag))
        probgap=float(np.max(np.abs(np.diag(a)[1:4]-np.diag(b)[1:4])))
        assert probgap<1e-12 and contrast>0.03
        if loss==phase==0:refcontrast=contrast
        assert abs(np.trace(a)-1)<1e-10 and abs(np.trace(b)-1)<1e-10
        scenarios.append(dict(loss_rate=loss,dephasing_rate=phase,
            absolute_Ramsey_imaginary_coherence_difference=contrast,
            max_observed_triangle_population_difference=probgap,
            loss_to_vacuum_probability=float(a[4,4].real)))
    assert abs(refcontrast-0.04098706247851882)<1e-12
    compiled=[]
    for n in (1,2,4,8,16,32,64):
        p,pe=trotter(1,t,n)
        m,me=trotter(-1,t,n)
        signal=float((p[0,0]-m[0,0]).imag)
        target=float((pe[0,0]-me[0,0]).imag)
        compiled.append(dict(steps=n,elementary_signed_edge_pulses=3*n,
            approximate_Ramsey_contrast=signal,
            exact_Ramsey_contrast=target,
            contrast_absolute_error=abs(signal-target),
            max_unitary_entry_error=float(max(np.max(abs(p-pe)),np.max(abs(m-me))))))
    assert compiled[-1]["contrast_absolute_error"]<.0005
    noisy=[]
    analog_target=scenarios[3]["absolute_Ramsey_imaginary_coherence_difference"]
    for n in (1,2,4,8,16,32,64):
        a=compiled_lindblad(1,n,deadtime=.003,gamma=.1,kappa=.1,time=t)
        b=compiled_lindblad(-1,n,deadtime=.003,gamma=.1,kappa=.1,time=t)
        observed=abs(float(2*(a[0,1]-b[0,1]).imag))
        noisy.append(dict(steps=n,pulses=3*n,total_physical_duration=3*t+3*n*.003,
            coherent_phase_contrast=observed,
            error_relative_to_simultaneous_noisy_analog=abs(observed-analog_target),
            loss_vacuum_population=float(a[4,4].real)))
    best=min(noisy,key=lambda row:row["error_relative_to_simultaneous_noisy_analog"])
    assert best["steps"]==16
    assert noisy[-1]["error_relative_to_simultaneous_noisy_analog"]>best["error_relative_to_simultaneous_noisy_analog"]
    return dict(status="PASS_LINDBLAD_RAMSEY_PHASE_WITNESS",
        Hilbert_states=["idle_reference","site0","site1","site2","vacuum_loss"],
        interferometric_initial_state="(|reference>+|site0>)/sqrt(2)",
        contrast_definition="abs[2 Im (rho_ref,site0_zeroFlux-rho_ref,site0_piFlux)]",
        t=t,scenarios=scenarios,
        trotter_compilation_order="(edge01 pulse)*(edge02 pulse)*(edge12 pulse) repeated n times",
        trotter_results=compiled,
        noisy_sequential_compile_deadtime_per_pulse=.003,
        noisy_sequential_compile_reference_gamma=.1,
        noisy_sequential_compile_reference_kappa=.1,
        noisy_sequential_compile_analog_contrast=analog_target,
        noisy_sequential_compile_best_depth_in_sample=best["steps"],
        noisy_sequential_compile_results=noisy,
        boundary="Independent Markovian loss/dephasing on 3 sites plus ideal phase-stable idle arm. No detector inefficiency, cross-talk, pulse calibration, spatial embedding or demonstrated circuit.")

def main():
    D,C,_=base.build()
    result=dict(status="PASS_FIVE_TOE_FALSIFICATION_GATES",
        continuum=continuum(),symmetry=symmetry(D,C),gravity=gravity(D,C),
        flavor=flavor(),hardware=hardware(),
        claim_boundary="All derived claims are finite mathematics, conditioned models, or idealized open-system simulation. Not a theory of everything.")
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(result["status"],"condition",result["symmetry"]["sampled_optimized_condition_number"],
          "vectorlike_cp",result["flavor"]["CP_odd_commutator_imag_cubed_trace"],
          "lindblad",result["hardware"]["scenarios"][3]["absolute_Ramsey_imaginary_coherence_difference"],flush=True)
    return result

if __name__=="__main__":main()
