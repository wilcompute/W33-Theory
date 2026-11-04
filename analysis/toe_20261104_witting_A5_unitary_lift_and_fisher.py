#!/usr/bin/env python3
"""Test physical projective-unitary lift of native W33 A5s to 40 Witting rays.

Derive *explicit* 4x4 unitaries realizing native point-graph A5
automorphisms and verify the class1 E8 A4+A4 eight-observable
intertwiner is covariant by actual conjugation, not merely a
combinatorial ray-permutation. Calibrate the Witting 40-outcome POVM's
eight-parameter Fisher information with detected/lost shots.

Classical Witting projective symmetry, tight 2-design, multinomial
Fisher theory are established; integration with the packet A4^2
kernel and reciprocal W33 A5 class selection is the new computation.
"""
from __future__ import annotations
import collections,json,sys,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
for path in (ROOT,ROOT/"analysis"):
    if str(path) not in sys.path:sys.path.insert(0,str(path))
import w33_pass999_a5_double_class_census as previous
from exploration.w33_witting_srg_bridge import construct_witting_rays,witting_to_symplectic_isomorphism
OUT=ROOT/"data"/"toe_20261104_witting_A5_unitary_lift_and_fisher.json"
def perm40(g):
    U=np.zeros((40,40))
    U[np.array(g),np.arange(40)]=1
    return U
def mapped(g,w2s,s2w):
    return tuple(s2w[g[w2s[j]]] for j in range(40))
def triple_wigner_type(rays,p):
    ov=rays.conj()@rays.T
    B=ov[:,:,None]*ov[None,:,:]*ov.T[:,None,:] # check shape: last should (k,i) indexed
    # More robust via einsum broadcasting: B_ijk=ov_ij ov_jk ov_ki
    B=ov[:,:,None]*ov[None,:,:]*ov.T[:,None,:]
    q=np.array(p)
    dst=B[np.ix_(q,q,q)]
    du=float(np.max(abs(B-dst)))
    da=float(np.max(abs(B.conj()-dst)))
    return du,da
def physical_unitary(rays,p):
    T=np.column_stack([rays[p[i]] for i in range(4)])
    assert np.max(abs(T.conj().T@T-np.eye(4)))<1e-12
    phase=[None]*4
    phase[0]=1+0j
    relations=[]
    for j in range(4,40):
        v=rays[j]
        a=T.conj().T@rays[p[j]]
        supports=[i for i in range(4) if abs(v[i])>1e-9]
        assert all(abs(a[i])>1e-9 for i in supports)
        for i in supports:
            for k in supports:
                if i==k:continue
                z=(a[i]/v[i])/(a[k]/v[k])
                assert abs(abs(z)-1)<1e-10
                relations.append((i,k,z/abs(z)))
    for _ in range(8):
        for i,k,z in relations:
            if phase[k] is not None and phase[i] is None:phase[i]=z*phase[k]
            if phase[i] is not None and phase[k] is None:phase[k]=phase[i]/z
    assert all(v is not None for v in phase)
    assert max(abs(phase[i]/phase[k]-z) for i,k,z in relations)<1e-8
    U=T@np.diag(phase)
    assert np.max(abs(U.conj().T@U-np.eye(4)))<1e-10
    residual=0.
    for j in range(40):
        x=U@rays[j]
        y=rays[p[j]]
        residual=max(residual,float(np.max(abs(np.outer(x,x.conj())-np.outer(y,y.conj())))))
    assert residual<1e-10
    return U,residual
def main():
    rays=np.array(construct_witting_rays())
    assert rays.shape==(40,4)
    w2s=witting_to_symplectic_isomorphism()
    s2w={v:k for k,v in w2s.items()}
    assert len(s2w)==40
    c=previous.core_objects()
    old=json.loads((ROOT/"data/toe_20261104_witting_operator_dark_spectral_A5_duality.json").read_text())
    E=np.array(old["A5_classes"][1]["explicit_W33_40x8_observable_coefficient_map"])
    Ops=np.array(old["A5_classes"][1]["explicit_8_Hermitian_ququart_observables_real"])+1j*np.array(
      old["A5_classes"][1]["explicit_8_Hermitian_ququart_observables_imag"])
    assert E.shape==(40,8) and Ops.shape==(8,4,4)
    Fraw=json.loads((ROOT/"data/toe_20261104_actual_a5_w33_25_to40_intertwiner.json").read_text())
    F=np.array(Fraw["both_W33_class_certificates"][1]["intertwiner_matrix_40x25"])
    labels=[(i,j) for i in range(5) for j in range(5)]
    B=np.zeros((25,8))
    for i,(r,k) in enumerate(labels):
        for a in range(4):
            B[i,a]=int(r==a+1)-int(r==0)
            B[i,a+4]=int(k==a+1)-int(k==0)
    QB,_=np.linalg.qr(B)
    P=np.einsum("ia,ib->iab",rays,rays.conj())
    Psymp=P[np.argsort([w2s[i] for i in range(40)])]
    assert np.max(abs(Ops-np.einsum("ij,iab->jab",E,Psymp)))<1e-9
    records=[]
    for index,H in enumerate(c["A5_classes"]):
        types=collections.Counter()
        residuals=[]
        selected=[]
        for g in H:
            p=mapped(g,w2s,s2w)
            du,da=triple_wigner_type(rays,p)
            if du<1e-9:types["unitary"]+=1
            elif da<1e-9:types["antiunitary"]+=1
            else:types["neither"]+=1
            residuals.append([du,da])
            if previous.order_of(g) in (3,5) and len(selected)<6:
                selected.append((g,p))
        assert sum(types.values())==60
        assert types["neither"]==0
        # A5 simple => map into ± from antiunitarity must be trivial.
        assert types["antiunitary"]==0
        assert types["unitary"]==60
        # Exhibit U(4) generators that collectively generate whole A5.
        order5=[g for g in H if previous.order_of(g)==5]
        order3=[g for g in H if previous.order_of(g)==3]
        generator_pair=None
        for g5 in order5:
            for g3 in order3:
                if previous.subgroup_closure([g5,g3],cap=70)==H:
                    generator_pair=(g5,g3)
                    break
            if generator_pair:break
        assert generator_pair
        lifts=[]
        for g in generator_pair:
            p=mapped(g,w2s,s2w)
            U,res=physical_unitary(rays,p)
            lifts.append(dict(order=previous.order_of(g),
                symplectic_40point_permutation=list(g),
                Witting_ray_permutation=list(p),
                U4_real=U.real.tolist(),U4_imag=U.imag.tolist(),
                maximum_40ray_projector_conjugation_residual=res))
            if index==1:
                Ug=perm40(g)
                S=F.T@Ug@F
                V=QB.T@S@QB
                assert np.max(abs(Ug@E-E@V))<1e-8
                rhs=np.einsum("kj,kab->jab",V,Ops)
                lhs=np.einsum("ac,jcd,bd->jab",U,Ops,U.conj())
                assert np.max(abs(lhs-rhs))<1e-8
        records.append(dict(A5_class_index=index,
            unitary_vs_antiunitary_triple_Bargmann_invariant_census=dict(types),
            verified_Witting_projective_unitary_generators=lifts,
            generator_orders=[z["order"] for z in lifts],
            maximal_unitary_Bargmann_residual=max(x[0] for x in residuals),
            native_40point_W33_action_lifts_to_physical_ququart_4x4_unitaries=True,
            class1_reye_8dim_operator_embedding_physically_A5_covariant=bool(index==1)))

    # Exact Witting 40-outcome POVM p_i=Tr(P_i rho)/10.
    # Near rho=I/4+sum theta_j O_j:
    # p_i(theta)=1/40 + (E_ij theta_j)/5.
    grad=np.real(np.einsum("iab,jba->ij",Psymp,Ops))/10
    assert grad.shape==(40,8)
    assert np.max(abs(grad-E/5))<1e-10
    p0=np.ones(40)/40
    fisher=grad.T@(grad/p0[:,None])
    assert np.max(abs(fisher-np.eye(8)*1.6))<1e-10
    assert np.max(abs(np.sum(grad,axis=0)))<1e-10
    # With independent erasure eta, the 41st outcome is "no click".
    # The nuisance eta is Fisher-orthogonal to theta at maximally mixed.
    eta=.85
    p_observed=np.r_[eta*p0,1-eta]
    theta_jac=np.vstack([eta*grad,np.zeros((1,8))])
    eta_jac=np.r_[p0,-1]
    Jac=np.column_stack([theta_jac,eta_jac])
    Fishall=Jac.T@(Jac/p_observed[:,None])
    assert np.max(abs(Fishall[:8,:8]-eta*1.6*np.eye(8)))<1e-10
    assert np.max(abs(Fishall[:8,8]))<1e-10
    assert abs(Fishall[8,8]-1/(eta*(1-eta)))<1e-10
    # Linear unbiased local estimator for KNOWN eta:
    # theta_hat=(5/eta) E^T (observed 40 probabilities);
    # E^T ones=0 and Fisher CRLB is achieved at theta0.
    rng=np.random.default_rng(20261104)
    N=10000
    counts=rng.multinomial(N,p_observed,size=1000)
    theta_estimators=(5/eta)*(counts[:,:40]@E)/N
    sample_var=np.var(theta_estimators,axis=0,ddof=1)
    expected_var=5/(8*N*eta)
    assert np.max(abs(sample_var/expected_var-1))<.2
    assert np.max(abs(np.mean(theta_estimators,axis=0)))<.0015
    result=dict(status="PASS_WITTING_BOTH_A5_CLASSES_UNITARY_LIFT_AND_8D_LOSS_AWARE_FISHER",
      Witting_ray_count=40,Witting_physical_Hilbert_dimension=4,
      group_records=records,
      class1_E8_A4plusA4_8real_params_acts_by_physical_projective_unitary_A5=True,
      at_maximally_mixed_ququart_8parameter_Fisher_per_detected_photon=1.6,
      Fisher_matrix_8params=fisher.tolist(),
      theta_coordinates="rho(theta)=I4/4+sum_j theta_j O_j, with Tr(O_i O_j)=2 delta_ij.",
      Witting_40outcome_probability_model="p_i(theta)=1/40 + sum_j E_ij theta_j /5, exact within positivity region.",
      estimator_known_eta="theta_hat=(5/eta)*E^T (count_i/N), sum_i E_ij=0; asymptotically attains local CRLB.",
      independent_erasure_eta=eta,
      with_erasure_41outcome_Fisher_eight_density_params_and_eta=Fishall.tolist(),
      independent_erasure_nuisance_cross_Fisher_zero=True,
      number_of_incident_photons_in_MC=N,
      Monte_Carlo_repeats=1000,
      CRLB_variance_per_density_coordinate_at_theta0=expected_var,
      Monte_Carlo_variance_eight_coordinates=sample_var.tolist(),
      if_encoding_by_epsilon_point_one_then_variance_for_dimensionless_parameters=expected_var/(.1**2),
      caveat="Loss and efficiency are iid and rail-independent with a known no-click flag. Calibration, dark counts, coherent reference phase uncertainty and finite experimental confidence are not modeled.",
      projective_symmetry_caveat="Physical A5 action is represented by U4 only up to scalar phase; Witting40 ray-label permutations by themselves would not have sufficed, and each 4x4 generator was verified on all40 projectors.",
      provenance="Witting 40-ray design, native W33 A5 classes, and photon multinomial Fisher are known; explicit A5 physical unitary lift of the specific E8 packet 8D operator intertwiner and efficiency calculations here."
    )
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    print(result["status"],"class Wigner",[(x["A5_class_index"],x["unitary_vs_antiunitary_triple_Bargmann_invariant_census"]) for x in records],
          "maxvarratio",max(sample_var/expected_var),flush=True)
    return result
if __name__=="__main__":main()
