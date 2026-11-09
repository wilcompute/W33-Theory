#!/usr/bin/env python3
"""2026-11-08 five physics falsifiers plus four-frame coherence witness.

All math is scoped: order-parameter and frame averaging; selected-frame
lattice U(1) matter/Ward; ideal-clock perturbations; partial E6 torus/SL3
covariance (NOT all 78 E6 generators); corrected CLASS evidence audit.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
from itertools import combinations,product
import json,math,sys
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.linalg import expm

ROOT=Path(__file__).resolve().parents[1]
SELECTED=((1,0,0),(1,1,1),(0,0,1),(1,2,1))
def jread(p,root=ROOT):
    return json.loads((root/p).read_text(encoding="utf-8"))
def q(x,p=3):
    return (x[0]*x[2]-x[1]*x[1])%p

def frame_order_parameter():
    """Permutation invariant quartic with exactly C(p+1,3) minima."""
    out=[]
    for p in (3,5,7,11):
        n=p+1;kappa=.7
        nmin=math.comb(n,3)
        minima=[]
        if p<=7:
            for bits in product((0,1),repeat=n):
                v=sum((x*x*(1-x)*(1-x)) for x in bits)+kappa*(sum(bits)-3)**2
                if abs(v)<1e-14:minima.append(bits)
            assert len(minima)==nmin
        # At each binary minimum f''(0)=f''(1)=2. Rank-one positive
        # Hessian correction from kappa(sum w -3)^2.
        hess=2*np.eye(n)+2*kappa*np.ones((n,n))
        evals=np.linalg.eigvalsh(hess)
        assert abs(evals[0]-2)<1e-12
        assert abs(evals[-1]-(2+2*kappa*n))<1e-11
        out.append(dict(p=p,frame_directions=n,degenerate_minima=nmin,
            GL2_orbit_size=nmin,quartic_local_radial_mass_squared=2,
            collective_radial_mass_squared=2+2*kappa*n,
            zero_temperature_minima_entropy_log=math.log(nmin)))
    assert [x["degenerate_minima"] for x in out]==[4,20,56,220]
    return dict(status="EXPLICIT_DISCRETE_GLOBAL_ORDER_PARAMETER_HAS_GAPPED_MINIMA_BUT_NO_CANONICAL_FRAME",
        example_potential="V(w)=sum_j w_j^2(1-w_j)^2 + 0.7(sum_j w_j-3)^2",
        local_minima_exactly_binary_occupancy_three=True,
        selected_frames_are_PGL2_equivalent=True,
        cases=out,frame_hessian_has_positive_gap=True,
        no_unique_symmetry_invariant_minimum_theorem="If an invariant V has one frame f as a global minimum, every G-translated frame is also a minimum; PGL2(Fp) acts transitively on the unordered null triples.",
        caveat="Order parameter is a global finite-symmetry toy. Exact local gauge symmetry cannot be interpreted as spontaneously broken by a gauge-variant VEV (Elitzur). Spatial/domain-wall dynamics, metric, physical frame masses and experimental Lorentz constraints uncomputed.")

def modinv(B,p):
    return np.asarray(sp.Matrix(B).inv_mod(p)).astype(np.int64)

def four_frame_coherence():
    p=3
    X=list(product(range(p),repeat=3))
    frames=list(combinations(SELECTED,3))
    assert len(frames)==4
    G=[]
    for fr in frames:
        B=np.array(fr,dtype=np.int64).T
        BI=modinv(B,3)
        assert np.all((B@BI)%3==np.eye(3,dtype=int))
        G.append((BI.T@BI)%3)
    records=[]
    classes=defaultdict(Counter)
    for x in X:
        kvals=[tuple((A@np.array(x,dtype=int))%3) for A in G]
        mult=Counter(kvals)
        purity=sum(n*n for n in mult.values())/16
        eigs=sorted([n/4 for n in mult.values()],reverse=True)
        assert len(eigs)<=4
        classes[str(q(x))][str(purity)]+=1
        # Exact Fourier character orthogonality: <chi_k,chi_l>=delta_kl.
        if x==(0,0,0): assert purity==1
        elif q(x)==2:assert purity==3/8
        else:assert purity==1/4
        records.append(dict(point=list(x),q=q(x),purity=purity,
                            frame_character_multiplicity=sorted(mult.values(),reverse=True),
                            rho_nonzero_eigenvalues=eigs))
    assert dict(classes)=={"0":Counter({"0.25":8,"1.0":1}),
                           "1":Counter({"0.25":6}),
                           "2":Counter({"0.375":12})}
    # Independent full complex-density-matrix replay for two classes.
    z=np.exp(2j*np.pi/3)
    sampled={}
    for x in ((0,0,1),(0,1,0),(0,0,0)):
        psi=[np.array([z**(np.dot(y,(A@np.array(x))%3)%3)/math.sqrt(27)
              for y in X]) for A in G]
        rho=sum(np.outer(v,v.conj()) for v in psi)/4
        purity=float(np.trace(rho@rho).real)
        diagmax=float(np.max(abs(np.diag(rho)-1/27)))
        assert abs(purity-records[X.index(x)]["purity"])<1e-12
        assert diagmax<1e-12
        sampled[str(x)]=dict(Tr_rho_squared=purity,intensity_deviation=diagmax)
    def echo_probability(x,reference_frame):
        K=[tuple((A@np.array(x,dtype=int))%3) for A in G]
        return K.count(K[reference_frame])/4
    # A coherent, known-frame device inverts to probability ONE;
    # a hidden equal-mixture frame, followed by an ideal frame-matched
    # inverse, returns to that input with probability 1/4 or 1/2.
    echo=dict(origin=echo_probability((0,0,0),0),
              q0_nonzero=echo_probability((0,0,1),0),
              q2_singleton_reference=echo_probability((0,1,0),0),
              q2_duplicated_reference=echo_probability((0,1,0),1))
    assert echo=={"origin":1,"q0_nonzero":.25,
                  "q2_singleton_reference":.25,"q2_duplicated_reference":.5}
    return dict(status="EXACT_Q3_FOUR_FRAME_COHERENCE_WITNESS",
        frames=4,point_count=27,all_channel_intensities=1/27,
        frame_matched_inverse_echo_probabilities=echo,
        exact_purity_class_census={k:dict(v) for k,v in sorted(classes.items())},
        representative_density_checks=sampled,points=records,
        proof="For frame basis B, U_B=F3^tensor3 conjugated by the physical coordinate permutation. Its column at input x is the normalized character y -> omega^(y^T B^(-T)B^(-1) x). Distinct character labels are exactly orthogonal; equal labels are identical. Uniform classical frame mixing gives purity sum multiplicity^2/4^2, while every output diagonal is 1/27.",
        observation="Frame randomness is invisible to the entire 27x27 transition-intensity matrix, but detectable by basis-referenced coherence or purity measurements; this is ordinary quantum theory, not evidence for a new physical force.")

def gauge_matter_ward():
    p=3
    X=list(product(range(p),repeat=3));ix={x:i for i,x in enumerate(X)}
    E=[]
    for x in X:
        for direction in range(3):
            y=list(x);y[direction]=(y[direction]+1)%p
            E.append((ix[x],ix[tuple(y)],direction))
    assert len(E)==81
    # Explicit source-native check: selected cubic links are precisely
    # a subset of the original 27-point, 108-edge det-null graph.
    sys.path.insert(0,str(ROOT/"analysis"))
    import w33_20261108_s4_harmonic_qdual as native
    native_edges,_,native_edge_index,_,_=native.complex27()
    pxy=[native.IX[((x[0]+x[1])%3,x[1],(x[1]+x[2])%3)] for x in X]
    selected_native={tuple(sorted((pxy[a],pxy[b]))) for a,b,_ in E}
    assert len(native_edges)==108 and len(selected_native)==81
    assert selected_native.issubset(native_edge_index.keys())
    B1=np.zeros((27,81),int)
    for i,(u,v,_) in enumerate(E):B1[u,i]=-1;B1[v,i]=1
    edge_index={(u,j):i for i,(u,v,j) in enumerate(E)}
    B2=np.zeros((81,81),int)
    t=0
    for x in X:
        u=ix[x]
        for j,k in combinations(range(3),2):
            y=list(x);y[j]=(y[j]+1)%p;y=tuple(y)
            z=list(x);z[k]=(z[k]+1)%p;z=tuple(z)
            B2[edge_index[u,j],t]+=1
            B2[edge_index[ix[y],k],t]+=1
            B2[edge_index[ix[z],j],t]-=1
            B2[edge_index[u,k],t]-=1
            t+=1
    assert t==81 and not np.any(B1@B2)
    assert np.linalg.matrix_rank(B1)==26
    rng=np.random.default_rng(2026110801)
    psi=rng.normal(size=27)+1j*rng.normal(size=27)
    A=rng.normal(scale=.4,size=81)
    chi=rng.normal(scale=.7,size=27)
    u=np.array([x for x,y,d in E])
    v=np.array([y for x,y,d in E])
    def energy(P,A):
        D=P[v]-np.exp(1j*A)*P[u]
        F=B2.T@A
        return float(np.vdot(D,D).real+.8*np.sum(1-np.cos(F))+.6*np.vdot(P,P).real)
    base=energy(psi,A)
    transform=energy(np.exp(1j*chi)*psi,A+B1.T@chi)
    invariant=abs(base-transform)
    assert invariant<1e-10
    # Purely covariant complex matter gradient D has a Hermitian H=D^dag D.
    U=np.exp(1j*A)
    H=np.zeros((27,27),complex)
    for e,(a,b,_) in enumerate(E):
        H[a,a]+=1;H[b,b]+=1;H[a,b]-=np.conj(U[e]);H[b,a]-=U[e]
    assert np.max(abs(H-H.conj().T))<1e-13
    j=2*np.imag(np.conj(psi[v])*U*psi[u])
    drho=2*np.imag(np.conj(psi)*(H@psi))
    cont=float(np.max(abs(drho+B1@j)))
    assert cont<1e-11,(cont,np.max(abs(drho)))
    assert abs(np.sum(drho))<1e-11
    # Infinitesimal Ward identity: nonlinear gauge variation has zero derivative.
    eps=1e-6
    derivative=(energy(np.exp(1j*eps*chi)*psi,A+eps*B1.T@chi)-
                energy(np.exp(-1j*eps*chi)*psi,A-eps*B1.T@chi))/(2*eps)
    assert abs(derivative)<1e-7
    # On a neutral 27-site charge source, B1 E = rho has a solution.
    charges=np.zeros(27);charges[0]=1;charges[1]=-1
    L=B1@B1.T
    pot=np.linalg.lstsq(L,charges,rcond=None)[0]
    field=B1.T@pot
    gauss=float(np.max(abs(B1@field-charges)))
    assert gauss<1e-10
    return dict(status="EXPLICIT_SELECTED_FRAME_LATTICE_U1_CHARGED_MATTER_GAUSS_AND_WARD",
       vertices=27,edges=81,oriented_square_plaquettes=81,
       original_native_graph_edges=108,selected_81_edges_native_subset_verified=True,
       vertex_gradient_rank=26,
       nonlinear_gauge_action_difference=invariant,
       discrete_charge_continuity_residual=cont,
       finite_difference_gauge_Ward_residual=abs(derivative),
       neutral_Gauss_constraint_residual=gauss,
       energy="S=sum_{x,i}|psi_(x+e_i)-exp(iA_xi)psi_x|² +0.8 sum_plaquette(1-cos(curlA))+0.6sum_x|psi_x|²",
       gauge_map="psi_x -> exp(i chi_x) psi_x; A_xi -> A_xi+chi_(x+e_i)-chi_x",
       proof_boundary="This is exactly the standard U(1) scalar lattice coupling on a deliberately selected cubic frame with externally assigned continuous time for the Schroedinger current. Not a derivation of charge, qED fermions, 3+1 Minkowski spacetime, physical photon masses or fine structure constant.")

def clock_noise():
    sys.path.insert(0,str(ROOT/"analysis"))
    import w33_20261108_null_frame_selection_five_fronts as prior
    F,h=prior.dft_and_log(3)
    I=np.eye(3)
    H=np.kron(np.kron(h,I),I)+np.kron(np.kron(I,h),I)+np.kron(np.kron(I,I),h)
    Uideal=np.kron(np.kron(F,F),F)
    assert np.max(abs(expm(-1j*H)-Uideal))<3e-12
    from scipy.linalg import eigvalsh
    rng=np.random.default_rng(2026110802)
    edges=[]
    for a in range(27):
        for b in range(a+1,27):
            if abs(H[a,b])>1e-10:edges.append((a,b))
    assert len(edges)==81
    points=[]
    for typ in ("onsite_detuning","null_edge_coupling"):
        for sigma in (.005,.02,.06):
            stats=[]
            for rep in range(8):
                D=np.zeros((27,27),complex)
                if typ=="onsite_detuning":
                    D[np.diag_indices(27)]=sigma*rng.normal(size=27)
                else:
                    for a,b in edges:
                        w=sigma*rng.normal()/3
                        D[a,b]=w;D[b,a]=w
                noisy=expm(-1j*(H+D))
                dn=float(max(abs(eigvalsh(D)[0]),abs(eigvalsh(D)[-1])))
                amp=float(np.max(abs(noisy-Uideal)))
                prob=float(np.max(abs(abs(noisy)**2-1/27)))
                tv=float(max(.5*np.sum(abs(abs(noisy[:,j])**2-1/27))
                             for j in range(27)))
                assert amp<=dn+1e-10,(amp,dn)
                assert prob<=2*dn+1e-10
                stats.append(dict(op_norm_deltaH=dn,max_amplitude_error=amp,
                       max_probability_error=prob,max_column_total_variation=tv))
            points.append(dict(type=typ,sigma=sigma,trials=len(stats),
                worst_operator_norm=max(x["op_norm_deltaH"] for x in stats),
                worst_probability_error=max(x["max_probability_error"] for x in stats),
                mean_probability_error=sum(x["max_probability_error"] for x in stats)/len(stats),
                worst_TV=max(x["max_column_total_variation"] for x in stats)))
    shift=expm(-1j*(H+.12*np.eye(27)))
    assert np.max(abs(abs(shift)**2-1/27))<1e-12
    return dict(status="NULL_CLOCK_DUHAMEL_BOUND_PLUS_REPRODUCIBLE_PERTURBATION_SWEEP",
       tested_matrix_dimension=27,ideal_supported_edges=81,
       perturbations=points,total_trials=sum(x["trials"] for x in points),
       exact_bound="For Hermitian H and H+D at time t=1: ||exp(-i(H+D))-exp(-iH)||_op <= ||D||_op. Therefore every entry intensity changes by at most 2||D||_op (a conservative bound).",
       uniform_common_onsite_shift_probability_error_less_than_1e_minus_12=True,
       scope="Reproducible synthetic Gaussian detuning/coupling noise, not a measured error budget or hardware-achievable fabrication precision.")

def e6_partial_covariance(root=ROOT):
    sys.path.insert(0,str(root/"analysis"))
    import w33_e6_cubic_jacobian_rank_stratification as native
    records=native.build_records()
    assert len(records)==1620
    triads=sorted({tuple(sorted((a//3,b//3,c//3))) for a,b,c,s in records})
    assert len(triads)==45
    T=sp.zeros(45,27)
    for j,ids in enumerate(triads):
        for i in ids:T[j,i]=1
    rank=T.rank()
    # Six diagonal commuting E6-Cartan directions are expected; derive them,
    # do NOT blindly assume it or claim the other 72 are verified.
    assert rank==21,(rank,27-rank)
    basis=T.nullspace()
    assert len(basis)==6
    vec=np.array([float(x) for x in basis[0]])
    assert np.max(abs(np.asarray(T.tolist(),int)@vec))<1e-10
    rng=np.random.default_rng(2026110803)
    Xi=rng.normal(size=(81,3))+1j*rng.normal(size=(81,3))
    def cubic(W):
        return sum(int(s)*W[a,0]*W[b,1]*W[c,2] for a,b,c,s in records)
    original=cubic(Xi)
    assert abs(original)>1e-4
    # Torus acts on e6id with same weight on all external SU3 phases.
    W=Xi*np.exp(.41*vec.repeat(3))[:,None]
    torus_err=abs(cubic(W)/original-1)
    assert torus_err<1e-10
    T3=np.array([[.1,.3,-.2],[-.2,.2,.1],[.05,-.1,-.3]],complex)
    T3-=np.trace(T3)/3*np.eye(3)
    S=expm(.37*T3)
    assert abs(np.linalg.det(S)-1)<1e-12
    Y=np.einsum("ab,ibj->iaj",S,Xi.reshape(27,3,3)).reshape(81,3)
    ext_err=abs(cubic(Y)/original-1)
    assert ext_err<1e-10
    return dict(status="NATIVE_E6_CUBIC_VERIFIED_ON_CARTAN6_AND_EXTERNAL_SL3_NOT_ALL_E6_78",
       ordered_signed_records=1620,unordered_signed_E6_triples=45,
       e6_triad_incidence_rank=rank,e6_torus_nullspace_dimension=len(basis),
       Cartan_torus_finite_rescaling_invariance_relative_error=torus_err,
       external_SL3_complex_finite_invariance_relative_error=ext_err,
       full_78_generators_present=(root/"artifacts/e6_27rep_basis_export/E6_basis_78.npy").is_file(),
       full_E6_covariance_certified=False,
       candidate_VEV_cubic_interaction_physically_allowed_certified=False,
       actual_conclusion="Proved invariance under six explicitly solved diagonal E6-torus weights and the external SL3 on qutrit fiber. This is a 14-dimensional Lie subalgebra; the other 72 E6 generators and supersymmetric F/D-term potential remain unchecked.",
       known_source="analysis/w33_e6_cubic_jacobian_rank_stratification.py; 45 signed E6 triples with epsilon_abc")

def corrected_cosmology(root=ROOT):
    old=jread("analysis/toe_uv/halofit_check_orig.json",root)["rows"]
    hf=jread("analysis/toe_uv/halofit_check_hf.json",root)["rows"]
    hm=jread("analysis/toe_uv/hmcode_check.json",root)["hm"]
    rows=[]
    for z,k in product(("0.01","1.0"),("0.1","1.0","3.0")):
        ref=hf["lcdm_lambda"][z][k]
        assert abs(hf["lcdm_scf"][z][k]/ref-1)<3e-6
        rows.append(dict(z=z,k=k,uncorrected_scf_over_Lambda=old["lcdm_scf"][z][k]/ref,
            corrected_scf_over_Lambda=hf["lcdm_scf"][z][k]/ref,
            Halofit_fading_over_CPL_boost=hf["fading_fit"][z][k]/hf["cpl_fit"][z][k],
            HMcode_fading_over_CPL_boost=hm["fading_fit"][z][k]/hm["cpl_fit"][z][k]))
    prereg=jread("analysis/toe_uv/prereg_noshear.json",root)
    p12633=jread("data/w33_pass12633_flavour_clock.json",root)
    assert p12633["all_checks_pass"] is True
    min_ratio=p12633["min_violation_factor"]
    assert min_ratio>1e6
    before=jread("analysis/toe_uv/sign_des_orig.json",root)
    after=jread("analysis/toe_uv/sign_des.json",root)
    prev=before["CPL"]["des"]-before["free_neg"]["des"]
    now=after["CPL"]["des"]-after["free_neg"]["des"]
    assert prev>3 and -1<now<0
    return dict(status="COSMO_RETRACTION_LEDGER_SOURCE_REPLAY_NO_NEW_LIKELIHOOD",
        corrected_control_rows=rows,
        DES_fixed_background_CPL_minus_fading_old_chi2=prev,
        DES_fixed_background_CPL_minus_fading_patched_chi2=now,
        S9_preregistration_exists=True,
        S9_preregistration_path="analysis/toe_uv/prereg_noshear.json",
        S9_preregistration_not_future_data=True,
        future_independent_shear_likelihood_executed=False,
        KiDS_corrected_heldout_reanalysis_executed_here=False,
        A4_flavour_modulus_clock_violation_factor_min=min_ratio,
        source_crosscheck="PASS12632 stock CLASS bug reproduction (issue 682); later S9 is a preregistered forecast, not observational validation; external 2026 single-scalar PRD status paper cautions sensitivity to priors and data selection.",
        safety="Old S7/S8 shear rankings remain withdrawn. No claim of true evidence from a frozen forecast or numeric source replay.")

def produce(root=ROOT):
    return dict(schema="w33.20261108.five_physical_followthrough_plus_coherence.v1",
       frame=frame_order_parameter(),Maxwell=gauge_matter_ward(),
       clock=clock_noise(),E6=e6_partial_covariance(root),
       cosmology=corrected_cosmology(root),sixth=four_frame_coherence(),
       scientific_boundary="A mathematically consistent global toy frame, standard chosen-lattice U1 charged matter, bounded synthetic clock noise, 14/86 E6xSL3 generator-sector coverage, historical cosmology audit, and a frame-mixture coherence signature. No TOE, emergent metric, all-78 E6 covariance, measured quantum hardware or new likelihood.")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",default="data/w33_20261108_five_followthrough_plus_coherence.json")
    a=p.parse_args()
    z=produce();out=ROOT/a.out
    out.parent.mkdir(exist_ok=True,parents=True)
    out.write_text(json.dumps(z,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps(dict(path=str(out),frame_minima=z["frame"]["cases"][0]["degenerate_minima"],
      gauge_Ward=z["Maxwell"]["finite_difference_gauge_Ward_residual"],
      noise_trials=z["clock"]["total_trials"],
      E6_cartan_rank=z["E6"]["e6_torus_nullspace_dimension"],
      S9_future_only=z["cosmology"]["S9_preregistration_not_future_data"],
      coherence_classes=z["sixth"]["exact_purity_class_census"]),indent=2))
if __name__=="__main__": main()
