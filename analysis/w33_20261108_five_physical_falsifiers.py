#!/usr/bin/env python3
"""Five post-PASS12632 physics falsifiers on native W33 data. No TOE proof.

1. Local square faces: exact Maxwell H1 completion and physical gap.
2. E6 three-spurion invariant scalar potential: vacuum manifold obstruction.
3. q=5 complex Hermitian null-local hopping: FFT/gradient numerical search.
4. Qutrit ninth-root magic injection + 27-mode 729-intensity diagnostic.
5. Fail-closed CLASS/Halofit scalar-field controls and withdrawn shear claims.
"""
from __future__ import annotations
import argparse
import itertools
import json
import math
import sys
from pathlib import Path
import numpy as np
from scipy.optimize import minimize

ROOT=Path(__file__).resolve().parents[1]
def rjson(path,root=ROOT):
    return json.loads((root/path).read_text(encoding="utf-8"))

def rank_mod_prime(matrix,prime=101):
    """Exact finite-field row elimination; rank mod p bounds rational rank below."""
    a=np.asarray(matrix,dtype=np.int64)%prime
    piv=0
    for col in range(a.shape[1]):
        if piv>=a.shape[0]:break
        candidates=np.flatnonzero(a[piv:,col])
        if not len(candidates):continue
        i=piv+int(candidates[0])
        if i!=piv:a[[i,piv]]=a[[piv,i]]
        a[piv]=(a[piv]*pow(int(a[piv,col]),-1,prime))%prime
        rows=np.flatnonzero(a[:,col]);rows=rows[rows!=piv]
        if len(rows):a[rows]=(a[rows]-a[rows,col,None]*a[piv][None,:])%prime
        piv+=1
    return piv

def square_curvature(root=ROOT):
    sys.path.insert(0,str(root/"analysis"))
    import w33_20261108_s4_harmonic_qdual as s
    edges,faces,ei,b1,b2=s.complex27()
    directions=[(1,0,0),(0,0,1),(1,1,1),(1,2,1)]
    ix={v:i for i,v in enumerate(s.V)}
    squares=[]
    for x in s.V:
        for i in range(4):
            for j in range(i+1,4):
                def translated(*ds):
                    return ix[tuple((x[k]+sum(d[k] for d in ds))%3 for k in range(3))]
                squares.append((translated(),translated(directions[i]),
                                translated(directions[i],directions[j]),translated(directions[j])))
    bs=np.zeros((108,162),dtype=int)
    for col,sq in enumerate(squares):
        for a,b in zip(sq,sq[1:]+sq[:1]):
            key=tuple(sorted((a,b)))
            bs[ei[key],col]+=1 if a<b else -1
    assert len(squares)==len({tuple(sorted(sq)) for sq in squares})==162
    assert not np.any(b1@bs)
    assert np.linalg.matrix_rank(b1)==26
    assert np.linalg.matrix_rank(b2)==36
    # Exact finite-field witness: rational rank is at least 82 mod 101,
    # while B1*[B2 Bs]=0 and rank(B1)=26 cap rank at 108-26=82.
    rank_fp=rank_mod_prime(np.hstack((b2,bs)))
    assert rank_fp==82
    assert np.linalg.matrix_rank(np.hstack((b2,bs)))==82
    k=np.asarray(b2@b2.T+bs@bs.T,dtype=np.int64)
    I=np.eye(108,dtype=np.int64)
    polynomial=I.copy()
    for lam in (0,3,6,9,12):polynomial=polynomial@(k-lam*I)
    assert not np.any(polynomial) # exact integer annihilating polynomial
    spec=np.rint(np.linalg.eigvalsh(k)).astype(int)
    count={int(l):int(np.sum(spec==l)) for l in np.unique(spec)}
    assert count=={0:26,3:4,6:12,9:40,12:26},count
    # Integer trace moments and exact polynomial pin the multiplicities.
    for power in (1,2,3,4):
        moment=int(np.trace(np.linalg.matrix_power(k,power)))
        assert moment==sum(mult*(lam**power) for lam,mult in count.items())
    assert not np.any((k@b1.T).astype(int))
    return dict(status="EXACT_NATIVE_LOCAL_SQUARE_CURVATURE_COMPLETION",
                vertices=27,edges=108,original_triangles=36,additional_translation_squares=162,
                square_unique_count=len(squares),gradient_rank=26,triangle_boundary_rank=36,
                completed_boundary_rank=82,original_harmonic_dimension=46,
                completed_harmonic_dimension=0,magnetic_spectrum=count,
                modular_rank_prime=101,modular_rank_witness=rank_fp,
                exact_integer_annihilator="K(K-3I)(K-6I)(K-9I)(K-12I)=0",
                moment_checks=[1,2,3,4],physical_gap_in_equal_stiffness_units=3,
                warning="Local squares cure flat H1 but gap all 82 gauge-invariant real modes. No two gapless transverse photons, charged matter, or continuum limit is established.")

def scalar_potential(root=ROOT):
    sys.path.insert(0,str(root/"analysis"))
    import w33_pass11261_g26_cartan_coordinate_map as p
    old=p._load(root/"analysis/w33_pass11218_e8_cubic_cartan_kernel.py","fivefront_vacuum")
    records=old.load_parent().build_records()
    assert len(records)==1620
    rng=np.random.default_rng(202611082)
    phi=rng.normal(size=81)+1j*rng.normal(size=81)
    m=np.zeros((81,81),complex)
    for u,x,o,c in records:m[o,x]+=c*phi[u]
    assert np.linalg.matrix_rank(m,tol=1e-8)==78
    assert np.max(np.abs(m+m.T))<1e-11
    raw=rng.normal(size=(81,3))+1j*rng.normal(size=(81,3))
    xi=np.linalg.qr(raw)[0] # xi^dagger xi=I_3, zero-potential vacuum
    gram=xi.conj().T@xi
    assert np.max(np.abs(gram-np.eye(3)))<1e-13
    def V(z):
        g=z.conj().T@z-np.eye(3)
        return float(np.vdot(g,g).real)
    assert V(xi)<1e-26
    # Real scalar space: 2*81*3=486. Nine orthogonal Gram constraints,
    # hence a 477D Stiefel manifold of exactly degenerate vacua.
    manifold_dim=2*81*3-3*3
    h=np.diag([1.,-0.5,0.25])
    anti=1j*np.diag([1.,-0.5,0.25])
    eps=1e-4
    normal_ratio=V(xi@(np.eye(3)+eps*h))/(eps*eps)
    tangent_ratio=V(xi@(np.eye(3)+eps*anti))/(eps*eps)
    expected_normal=4*np.trace(h@h).real
    assert abs(normal_ratio-expected_normal)<0.005,(normal_ratio,expected_normal)
    assert tangent_ratio<1e-6,(tangent_ratio,normal_ratio)
    t=np.diag([.4,.6,.8])
    u=xi.conj()
    mass=m+u@t@u.T
    assert np.linalg.matrix_rank(mass,tol=1e-8)==81
    aug=np.block([[m,u],[-u.T,np.zeros((3,3),complex)]])
    lhs=np.linalg.slogdet(mass)
    rhs=np.linalg.slogdet(aug)
    err=abs(lhs[1]-(rhs[1]+np.log(np.linalg.det(t))))
    assert err<1e-6,err
    phase=float(np.angle(lhs[0]))
    assert abs(phase)>0.01
    return dict(status="EXACT_INVARIANT_SCALAR_POTENTIAL_VACUUM_DEGENERACY_AND_MASS_RANK",
        potential="V=lambda*Tr[(Xi^dagger Xi-v^2 I_3)^2], lambda>0, Xi in C^(81x3)",
        symmetries="Invariant under any unitary 81-dimensional representation acting on Xi at left and U(3) flavor acting at right; spurion couplings need not preserve full U(3).",
        real_scalar_components=486,normal_Gram_constraints=9,
        zero_potential_vacuum_manifold="V_3(C^81), complex Stiefel manifold",
        vacuum_flat_real_dimension=manifold_dim,
        stable_radial_hessian_eigenvalue_for_lambda_v2_one=8,
        normal_quadratic_numerical_coefficient=normal_ratio,
        expected_normal_coefficient=expected_normal,
        tangent_quadratic_numerical_coefficient=tangent_ratio,
        native_mass_rank_before=78,native_mass_rank_after=81,
        mass_det_factorization_log_error=err,mass_det_phase_radians=phase,
        missing_physics="The potential alone leaves 477 flat real directions; it does not select an isolated E6-breaking SM vacuum, enforce anomaly-free chiral reps, or protect strong CP at loop order.")

def magnetic_q5(root=ROOT):
    old=rjson("data/w33_20261108_five_physics_gates.json",root)["local_hamiltonian"]
    prior=float(old["q5_local_anisotropic_best_mean_squared_probability_error"])
    oldw=np.array(old["q5_local_anisotropic_best_couplings"])
    p=5
    dirs=[(1,x,x*x%p) for x in range(p)]+[(0,0,1)]
    antipodal_pairs=[]
    memberships=[]
    for i,d in enumerate(dirs):
        found=set()
        for scale in range(1,p):
            v=tuple(scale*x%p for x in d)
            vn=tuple((-y)%p for y in v)
            key=min(v,vn)
            if key not in found:
                found.add(key);antipodal_pairs.append(key);memberships.append(i)
        assert len(found)==2
    assert len(antipodal_pairs)==12
    a,b,c=np.indices((p,p,p))
    theta=np.array([2*np.pi*(a*v[0]+b*v[1]+c*v[2])/p
                    for v in antipodal_pairs])
    # c_v=a_v+i b_v, c_-v=conj(c_v) => real band E(k)
    features=np.concatenate([2*np.cos(theta),2*np.sin(theta)],axis=0)
    target=1/p**3
    def evaluate(w,gradient=False):
        spectrum=np.tensordot(w,features,axes=(0,0))
        phase=np.exp(-1j*spectrum)
        amplitude=np.fft.ifftn(phase)
        error=np.abs(amplitude)**2-target
        obj=float(np.mean(error**2))
        if not gradient:return obj,error
        der=np.fft.ifftn(-1j*features*phase[None,:,:,:],axes=(1,2,3))
        g=4*np.mean(error[None,:,:,:]*np.real(amplitude.conj()[None,:,:,:]*der),
                    axis=(1,2,3))
        return obj,g
    x0=np.zeros(24)
    x0[:12]=[oldw[i] for i in memberships]
    obj0,_=evaluate(x0)
    assert abs(obj0-prior)<2e-10,(obj0,prior)
    # Analytic-gradient crosscheck versus independent central differences.
    val,grad=evaluate(x0,True)
    for j in (0,7,12,19):
        delta=np.zeros(24);delta[j]=1e-5
        numeric=(evaluate(x0+delta)[0]-evaluate(x0-delta)[0])/(2e-5)
        assert abs(numeric-grad[j])<1e-8,(j,numeric,grad[j])
    starts=[x0]
    rng=np.random.default_rng(20261108)
    for _ in range(3):starts.append(x0+rng.normal(scale=.5,size=24))
    trials=[]
    for start in starts:
        opt=minimize(lambda w:evaluate(w,True),start,jac=True,method="L-BFGS-B",
                     options={"maxiter":300,"ftol":1e-13,"gtol":1e-9,"maxls":30})
        v,err=evaluate(opt.x)
        trials.append((v,float(np.max(np.abs(err))),opt.x,int(opt.nit)))
    best=min(trials,key=lambda t:t[0])
    assert best[0]<=prior+1e-10,(best[0],prior)
    assert best[0]>0
    return dict(status="NUMERICAL_HEURISTIC_COMPLEX_NULL_LOCALITY_SEARCH",
        p=5,hilbert_dimension=125,projective_null_directions=6,
        conjugate_hopping_pairs=12,independent_real_hopping_parameters=24,
        optimizer="Four deterministic L-BFGS-B starts, exact FFT objective + checked analytic gradient",
        initial_six_real_parameter_MSE=prior,initial_recomputed_MSE=obj0,
        best_24_parameter_MSE=best[0],best_max_probability_residual=best[1],
        best_coefficients=list(map(float,best[2])),best_iteration_count=best[3],
        improvement_factor=float(prior/best[0]),
        proof_boundary="Local optimization is not a proof of global impossibility or a physical qutrit photonic clock. Hamiltonian is translation invariant, complex Hermitian and null supported; no translation-breaking/time-dependent search.")

def qutrit_magic_injection():
    root=np.exp(2j*np.pi/3)
    z=np.exp(2j*np.pi/9)
    t=np.array([1,z,z**-1])
    x=np.roll(np.eye(3),1,axis=0)
    zz=np.diag([root**j for j in range(3)])
    corrections=[]
    for m in range(3):
        corr=np.diag(t/np.roll(t,-m))
        image=corr@x@corr.conj().T
        overlap=max(abs(np.trace((np.linalg.matrix_power(x,a)@
                 np.linalg.matrix_power(zz,b)).conj().T@image)/3)
                 for a in range(3) for b in range(3))
        assert abs(overlap-1)<1e-12
        corrections.append(dict(outcome=m,probability=1/3,
                                correction_is_qutrit_diagonal_Clifford=True,
                                phase_exponents_mod_nine=[int(round((np.angle(zval)%(2*np.pi))*9/(2*np.pi)))%9
                                                          for zval in np.diag(corr)]))
    rng=np.random.default_rng(9931)
    psi=rng.normal(size=3)+1j*rng.normal(size=3);psi/=np.linalg.norm(psi)
    out=t*psi
    for m in range(3):
        raw=psi*np.roll(t,-m)/np.sqrt(3)  # ancilla Z measurement after SUM^-1
        corr=np.diag(t/np.roll(t,-m))
        actual=np.sqrt(3)*corr@raw
        assert np.max(np.abs(actual-out))<1e-13
    # 27-rail logical F3 tensor-circuit = 3 layers * 9 tritters each.
    f=np.array([[root**(i*j)/np.sqrt(3) for j in range(3)] for i in range(3)])
    f27=np.kron(np.kron(f,f),f)
    assert np.max(np.abs(f27.conj().T@f27-np.eye(27)))<1e-13
    assert np.max(np.abs(np.abs(f27)**2-1/27))<1e-13
    # A ninth-root phase placed on input rails: 729 intensities unchanged.
    diagonal=np.ones(27,dtype=complex)
    diagonal[0]=z;diagonal[1]=z**-1
    magic_f27=f27*diagonal[None,:]
    max_difference=float(np.max(np.abs(np.abs(magic_f27)**2-np.abs(f27)**2)))
    assert max_difference<1e-13
    return dict(status="EXACT_ALGEBRAIC_QUTRIT_MAGIC_INJECTION_CLIFFORD_FEEDFORWARD",
        target_gate="T9=diag(1,zeta9,zeta9^-1)",
        resource_state="T9|+> in a separate ancilla qutrit",
        circuit="Use SUM^-1 (data control, ancilla target), measure ancilla in Z, feedforward C_m=diag(t_x/t_(x+m)), m=0,1,2",
        correction_outcomes=corrections,deterministic_conditional_on_ideal_gate_and_detection=True,
        ideal_27_mode_tritters=27,stage_count=3,mode_dimension=27,
        single_port_intensity=1/27,ideal_channel_intensity_values=729,
        input_magic_phase_729_intensity_max_change=max_difference,
        necessary_validation="Intensities alone cannot certify the magic phase; basis-referenced interferometry/process tomography is needed.",
        hardware_boundary="SUM^-1 is a TWO-qutrit entangling gate, not supplied by passive single-photon path rephasing. Logical circuit success says nothing about a physical one-photon deterministic gate, state source, detectors, or fault-tolerant overhead.",
        illustrative_end_to_end_success_formula="eta_source * eta_SUM * eta_meas * eta_tritter**27 * eta_feedforward",
        parameters_not_measured=True)

def cosmology_halofit_firewall(root=ROOT):
    before=rjson("analysis/toe_uv/halofit_check_orig.json",root)
    after=rjson("analysis/toe_uv/halofit_check_hf.json",root)
    cases=[]
    for redshift in ("0.01","1.0"):
        for k in ("0.1","1.0","3.0"):
            reference=after["rows"]["lcdm_lambda"][redshift][k]
            original=before["rows"]["lcdm_scf"][redshift][k]
            fixed=after["rows"]["lcdm_scf"][redshift][k]
            fluid=after["rows"]["lcdm_fluid"][redshift][k]
            error=abs(fixed/reference-1)
            assert error<3e-6,(redshift,k,error)
            assert abs(fluid/reference-1)<1e-13
            cases.append(dict(redshift=redshift,k_h_per_Mpc=k,
                 original_scalar_to_lambda_ratio=original/reference,
                 patched_scalar_to_lambda_ratio=fixed/reference,
                 patched_relative_error=error))
    assert min(c["original_scalar_to_lambda_ratio"] for c in cases)<.43
    impact=rjson("analysis/toe_uv/hf_impact.json",root)
    assert max(abs(v["delta_hf_minus_orig"]["total"])
               for v in impact.values())<1.1
    return dict(status="WITHDRAWN_SHEAR_CLAIMS_AND_REPRODUCED_NONLINEAR_CONTROL",
        original_and_patched_controls=cases,
        patch_change_training_chi2_max_less_than_1p1=True,
        failed_previous_model_assessment=[
         "data/w33_20261108_S8_hybrid_shapley_audit.json",
         "data/w33_pass12631_kids_heldout.json",
         "analysis/PASS20261108_FIVE_GATE_EXTENSIONS.md section 5",
         "analysis/NOTE_DARK_ENERGY_EVIDENCE_20261108.md shear comparison",
         "analysis/PASS20261108_FIVE_PHYSICS_GATES.md section 5"],
        source_notice="analysis/PASS12632_HALOFIT_SCF_BUG.md",
        fail_closed=True,
        correctness_statement="The patched CLASS control numerically matches ordinary LCDM/nonlinear halofit at six measured k,z cells; it DOES NOT independently rerun DES or KiDS likelihoods. All pre-patch S8/shear rankings remain withdrawn.",
        external_data="KiDS-Legacy extended cosmology A&A 709 A82 (2026), DOI 10.1051/0004-6361/202558581")

def produce(root=ROOT):
    return dict(schema="w33.20261108.five_physical_falsifiers.v1",
                maxwell=square_curvature(root),
                e6=scalar_potential(root),
                clock=magnetic_q5(root),
                photonic=qutrit_magic_injection(),
                cosmology=cosmology_halofit_firewall(root),
                scientific_boundary="Three exact finite mathematical/algebraic conclusions, one bounded numerical heuristic, one source-controlled retraction; no physical TOE or new observational model ranking.")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",default="data/w33_20261108_five_physical_falsifiers.json")
    a=ap.parse_args()
    out=produce()
    path=ROOT/a.output
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"output":str(path),"square_spectrum":out["maxwell"]["magnetic_spectrum"],
        "e6_flat_modes":out["e6"]["vacuum_flat_real_dimension"],
        "clock_MSE":out["clock"]["best_24_parameter_MSE"],
        "magic_outcomes":len(out["photonic"]["correction_outcomes"]),
        "withdrawn_shear":out["cosmology"]["fail_closed"]},indent=2))
if __name__=="__main__":main()
