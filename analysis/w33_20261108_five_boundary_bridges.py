#!/usr/bin/env python3
"""November 8 five-front bridge: reduced native Maxwell, E6 Pfaffian CP,
null-local speed, scalable photonic resources, frozen cosmology holdouts.

All theorems are conditional. No physical photon, E6 vacuum, or TOE inferred.
"""
from __future__ import annotations
import argparse, hashlib, itertools, json, math, sys
from pathlib import Path
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
def load(path):return json.loads(Path(path).read_text(encoding="utf-8"))

def reduced_maxwell(root=ROOT):
    """Exact small-momentum native M/27 cone; k4=0 is a SUPPLIED compactification."""
    prior=load(root/"data/w33_20261027_native_bloch_face_module.json")
    M=sp.Matrix([[sp.Rational(z) for z in row]
        for row in prior["effective_symbol"]["harmonic_link_gram_M"]])
    assert M==sp.Matrix([[10,5,-6,0],[5,10,0,-6],[-6,0,12,-6],[0,-6,-6,12]])
    assert M.det()==2916
    assert all(M[:j,:j].det()>0 for j in range(1,5))
    inv44=sp.factor(M.inv()[3,3])
    assert inv44==sp.Rational(5,27)
    # The local 3D effective description retains only k4=0 (a compact
    # zero-mode assumption); the A4 Wilson-loop coordinate is gauge invariant.
    m2=sp.Rational(1,5)                  # deliberately supplied coefficient
    E44=sp.zeros(4);E44[3,3]=1
    examples=[]
    x=sp.symbols("x")
    for coords in ((1,0,0,0),(1,2,3,0),(2,-1,1,0)):
        n=sp.Matrix(coords)
        acoustic=sp.factor((n.T*M*n)[0]/27)
        K=sp.factor((n.T*M*n)[0])*M/27-(M*n)*(M*n).T/27
        # Fully gauge-invariant 4D curvature: K n=0.
        assert K*n==sp.zeros(4,1)
        massed=K+m2*E44
        assert massed*n==sp.zeros(4,1)  # only holds because k4=0
        characteristic=sp.factor((massed-x*M).det())
        expected=sp.factor(M.det()*(-x)*(acoustic-x)**2
                 *(acoustic+m2*inv44-x))
        assert sp.simplify(characteristic-expected)==0
        # two 3D transverse photon-like modes, one scalar-like (gapped)
        examples.append({"k":coords,"two_transverse_omega2":str(acoustic),
                         "compact_scalar_omega2":str(acoustic+m2*inv44),
                         "gauge_zero_eigenvalue":True,
                         "scalar_extra_gap_omega2":str(m2*inv44)})
    n4=sp.Matrix([0,0,0,1])
    assert (n4.T*(m2*E44)*n4)[0]==m2 # explicit 4D gauge violation
    return {"status":"EXACT_NATIVE_4D_TO_3D_GAUGE_INVARIANT_ZERO_MODE_REDUCTION",
      "native_matrix_M":[[int(M[i,j]) for j in range(4)] for i in range(4)],
      "native_metric_determinant":int(M.det()),
      "native_leading_cone":"K(k)=((k.T M k) M - (M k)(M k).T)/27",
      "three_space_zero_mode_assumption":"k4=0 (compact periodic fourth spatial direction, nonzero KK modes omitted)",
      "gauge_invariant_scalar_variable":"A4 zero mode/Wilson holonomy; invariant under small periodic gauge transformations",
      "unlifted_physical_transverse_modes":3,
      "two_transverse_3D_modes_plus_one_scalar":True,
      "supplied_Wilson_mass_term":"(mu2/2)*A4^2 in zero-mode effective theory; this is locally gauge invariant under k4=0 but NOT a local gauge-invariant full 4D mass",
      "supplied_mu_squared":str(m2),
      "Schur_scalar_metric":str(1/inv44),
      "inverse_kinetic_M44":str(inv44),
      "scalar_mass_gap_squared":str(m2*inv44),
      "exact_three_momenta":examples,
      "nonzero_k4_breaks_full_4D_gauge_symmetry":True,
      "critical_limit":"The two-plus-one decomposition and mass gap are exact for the PREEXISTING ENGINEERED leading symbol and a supplied compactification/Wilson potential. They do not derive why a fourth direction compactifies, a Wilson potential arises, or how a photon couples to measured charges."}

def pfaffian_skew(A,tol=1e-10):
    """Complex Pfaffian by pivoted skew Schur complements, O(n^3)."""
    A=np.array(A,dtype=complex,copy=True)
    n=A.shape[0]
    assert n%2==0 and np.max(abs(A+A.T))<tol
    p=1.+0j
    for k in range(0,n,2):
        j=k+1+int(np.argmax(abs(A[k,k+1:])))
        if abs(A[k,j])<1e-14:return 0j
        if j!=k+1:
            A[[k+1,j],:]=A[[j,k+1],:]
            A[:,[k+1,j]]=A[:,[j,k+1]]
            p=-p
        pivot=A[k,k+1];p*=pivot
        u=A[k,k+2:].copy();v=A[k+1,k+2:].copy()
        A[k+2:,k+2:]-=(np.outer(u,v)-np.outer(v,u))/pivot
    return p

def pfaffian_mass(root=ROOT):
    """Actual E6 1620-term signed skew map, not a toy 81-state tensor."""
    sys.path.insert(0,str(root/"analysis"))
    import w33_pass11261_g26_cartan_coordinate_map as P
    old=P._load(root/"analysis/w33_pass11218_e8_cubic_cartan_kernel.py",
                "pfaffian_three_spurion")
    records=old.load_parent().build_records()
    assert len(records)==1620
    rng=np.random.default_rng(14062026)
    phi=rng.normal(size=81)+1j*rng.normal(size=81)
    M=np.zeros((81,81),complex)
    for u,x,o,c in records:M[o,x]+=c*phi[u]
    assert np.max(abs(M+M.T))<1e-11
    assert np.linalg.matrix_rank(M,tol=1e-8)==78
    U=[]
    for _ in range(3):
        z=rng.normal(size=81)+1j*rng.normal(size=81)
        z=z/np.linalg.norm(z)
        U.append(np.sqrt(.4)*z.conj())
    U=np.column_stack(U)
    aug=np.block([[M,U],[-U.T,np.zeros((3,3),complex)]])
    Pf=pfaffian_skew(aug)
    detsign,logabs=np.linalg.slogdet(M+U@U.T)
    assert abs(Pf)>1e-14
    phase_error=float(abs(np.angle(detsign/(Pf/abs(Pf))**2)))
    log_error=float(abs(logabs-2*math.log(abs(Pf))))
    assert phase_error<1e-7 and log_error<1e-7
    # A single independently rephased scalar rotates the Pfaffian linearly,
    # hence the mass determinant phase *twice*. No theta-bar is predicted.
    theta=math.pi/9
    U2=U.copy()
    U2[:,0]*=np.exp(-1j*theta)
    P2=pfaffian_skew(np.block(
        [[M,U2],[-U2.T,np.zeros((3,3),complex)]]))
    ph_shift=float(np.angle((P2/Pf)/np.exp(-1j*theta)))
    det2=np.linalg.slogdet(M+U2@U2.T)[0]
    det_phase_shift=float(np.angle(
        (det2/detsign)/np.exp(-2j*theta)))
    assert abs(ph_shift)<1e-7 and abs(det_phase_shift)<1e-7
    # Independent small-rank adversarial examples with exact algebra.
    Z=sp.zeros(3)
    B=sp.Matrix([[0,2,0],[-2,0,0],[0,0,0]])
    v=sp.Matrix([[1],[2],[3]])
    C=B+v*v.T
    W=B.row_join(v).col_join((-v.T).row_join(sp.zeros(1)))
    assert C.det()==sp.Rational(36)
    assert W.det()==C.det()
    # Critical adversarial control: a generic corank-one skew matrix with
    # three added vectors does NOT satisfy the same square identity.
    V3=sp.Matrix([[1,2,3],[2,0,1],[3,-1,2]])
    C3=B+V3*V3.T
    W3=B.row_join(V3).col_join((-V3.T).row_join(sp.zeros(3)))
    assert C3.det()==105 and W3.det()==49
    assert C3.det()!=W3.det()
    return {"status":"NATIVE_81_STATE_PFAFFIAN_SQUARE_AND_CP_REPHASING_THEOREM",
      "records":1620,"native_skew_rank":78,
      "three_spurion_full_rank":int(np.linalg.matrix_rank(M+U@U.T,tol=1e-8)),
      "augmented_skew_dimension":84,
      "identity":"For a skew 81x81 matrix M of corank AT LEAST THREE and any 81x3 U: det(M+U U^T)=Pf([[M,U],[-U^T,0_3]])^2. This is NOT true for arbitrary corank-one skew M.",
      "proof":"Since rank(M)<=78 and rank(U U^T)<=3, every determinant term using fewer than three rank-one insertions vanishes. The surviving three-insertion term equals the square of the signed Pfaffian minor expansion of the 84x84 augmented skew matrix. Equivalently use a nonsingular 78x78 skew block and a Schur complement when rank(M)=78; polynomial continuation gives the rank<=78 case.",
      "native_relative_determinant_phase_error":phase_error,
      "native_log_modulus_error":log_error,
      "corank_one_three_column_adversarial_counterexample":{"det_mass":105,"augmented_pfaffian_squared":49},
      "synthetic_mass_determinant_phase_rad":float(np.angle(detsign)),
      "one_spurion_rephasing_theta":theta,
      "augmented_pfaffian_rephasing_error":ph_shift,
      "mass_determinant_double_rephasing_error":det_phase_shift,
      "cp_boundary":"The Pfaffian-square algebra constrains a synthetic determinant but does NOT force its phase to vanish. One scalar phase rotates the determinant by twice that phase. Gauge rephasings, anomalous chiral rotations, physical quark-sector projection, vacuum selection and theta-bar require independent dynamics.",
      "prior_owner":"Native rank78 and Pfaffian-squared PRINCIPAL minors were already recorded in w33_pass11218_e8_cubic_cartan_kernel.py. The augmented low-rank update formula and actual 81x81 84-Pfaffian check are the additional result."}

def null_local_speed():
    p=5
    rng=np.random.default_rng(20261108)
    h=np.zeros((p,p,p),complex);seen=set()
    a,b,c=np.indices((p,p,p))
    null=((a*c-b*b)%p==0)
    null[0,0,0]=False
    for d in itertools.product(range(p),repeat=3):
        if not null[d] or d in seen:continue
        inv=tuple((-x)%p for x in d)
        z=(rng.normal()+1j*rng.normal())/math.sqrt(2)
        h[d]=z;h[inv]=z.conjugate()
        seen.add(d);seen.add(inv)
    assert len(seen)==p*p-1
    eigen=np.fft.fftn(h)
    assert np.max(abs(eigen.imag))<1e-10
    radius=float(np.max(abs(eigen)))
    selected=(0,1,0)
    assert not null[selected] and h[selected]==0
    rows=[]
    for tau in (0.05,0.1,0.25):
        t=tau/radius
        u=np.fft.ifftn(np.exp(-1j*t*eigen))
        actual=float(abs(u[selected]))
        ceiling=tau*tau/2
        assert actual<=ceiling+1e-12
        rows.append({"normalized_time_tH":tau,
                     "actual_nonnull_transition_amplitude":actual,
                     "rigorous_Taylor_bound":ceiling})
    t_min=math.sqrt(2*p**(-1.5))
    return {"status":"UNCONDITIONAL_STRICT_NULL_LOCAL_SECOND_ORDER_SPEED_LIMIT",
      "theorem":"Any Hermitian 5^3-mode H, even non-translation-invariant and fully anisotropic, with H_ij=0 for one nonnull pair i!=j satisfies |e^(-itH)_ij|<=t^2||H||op^2/2. Exact flat mixing forces |t| ||H||op>=sqrt(2)*5^(-3/4).",
      "proof":"For an off-support pair, entries of both I and H vanish. The scalar spectral remainder |e^(-ix)-1+ix|<=x^2/2 for real x bounds the matrix entry by the operator norm of the second-order remainder.",
      "target_flat_amplitude":p**(-1.5),
      "minimum_dimensionless_time_energy":t_min,
      "synthetic_H_null_hopping_pairs":len(seen)//2,
      "synthetic_H_operator_norm":radius,
      "tested_times":rows,
      "general_q":"sqrt(2)*q^(-3/4) if at least one desired flat-mixing output is not directly coupled, for all q and any Hermitian H.",
      "boundary":"A speed/resource lower bound, not a universal no-flat-mixing theorem; a long-running local Hamiltonian may evade it."}

def one_photon_resource():
    p=3
    v=list(itertools.product(range(p),repeat=3))
    N=len(v)
    omega=np.exp(2j*np.pi/p)
    U=np.empty((N,N),complex)
    for i,x in enumerate(v):
        for j,y in enumerate(v):
            a,b,c=((x[k]-y[k])%p for k in range(3))
            U[i,j]=omega**((a*c-b*b)%p)/math.sqrt(N)
    assert np.max(abs(U@U.conj().T-np.eye(N)))<1e-12
    psi=U[:,0]
    z9=np.exp(2j*np.pi/9)
    psi=np.array([psi[i]*[1,z9,z9.conjugate()][x[2]] for i,x in enumerate(v)])
    assert abs(np.vdot(psi,psi)-1)<1e-12
    probs=[float(sum(abs(psi[i])**2 for i,x in enumerate(v) if x[0]==a))
           for a in range(p)]
    assert all(abs(z-1/p)<1e-12 for z in probs)
    # A classical simulator draws one measurement outcome then applies an
    # outcome-dependent phase. The state remains an ordinary length-N vector.
    rng=np.random.default_rng(20261108)
    out=int(rng.choice(p,p=probs))
    post=np.array([psi[i] if x[0]==out else 0j for i,x in enumerate(v)])
    post/=np.linalg.norm(post)
    feedforward=np.array([omega**((out*x[1])%p) for x in v])
    post*=feedforward
    assert abs(np.vdot(post,post)-1)<1e-12
    return {"status":"EXACT_ONE_PHOTON_CLASSICAL_TRACKING_WITH_NONCLIFFORD_AND_FEEDFORWARD",
      "modes":N,"logical_qutrits":3,
      "unitary":"27-mode determinant Gaussian clock followed by ninth-root non-Clifford path phase",
      "measured_first_address_probabilities":probs,
      "sampled_measurement_outcome":out,
      "conditional_feedforward_state_norm":float(np.vdot(post,post).real),
      "classical_vector_storage_complex_amplitudes":N,
      "dense_gate_cost_arithmetic":"O(N^2) for a dense N-mode gate; O(N) for a diagonal phase, projector or sparse permutation; sample one adaptive trajectory in polynomial time in gate count and N.",
      "modes_needed_for_n_logical_qutrits":{str(n):3**n for n in [3,5,10,15,20]},
      "example_n20_orthogonal_modes":3**20,
      "proof":"The one-photon sector on N orthogonal modes is C^N. Passive linear optics acts by N-by-N unitaries, a local phase by a diagonal, and one-photon projective measurement/feedforward by classical matrix-vector updates and normalized Born sampling. An isometric embedding of n independent qutrits needs N>=3^n.",
      "complexity_boundary":"Non-Clifford magic is NOT sufficient for scalable single-photon BQP advantage in a polynomial-size single-particle mode register. The repository's 2026-09-24 architecture atlas already identified exponential mode cost. Stationary quantum memories, more photons, physical nonlinearities, or CV resources can change the computation model.",
      "optical_boundary":"One adaptive pure-state trajectory is classically samplable in polynomial(N,gate count) for the specified one-photon passive-optical/Kraus model; enumerating exponentially many complete outcome histories or conditioning on exponentially rare events is a different task."}

def prereg_cosmology(root=ROOT):
    uv=root/"analysis/toe_uv"
    prereg_path=uv/"prereg_tilt.json"
    data=json.loads(prereg_path.read_text(encoding="utf8"))
    raw=prereg_path.read_bytes()
    h_raw=hashlib.sha256(raw).hexdigest()
    # Git on the user's Windows machine may check out CRLF while CI on
    # Linux sees the committed LF bytes. Verify canonical tracked LF content.
    lf_bytes=raw.replace(b"\r\n",b"\n")
    h=hashlib.sha256(lf_bytes).hexdigest()
    recorded=(uv/"prereg_tilt.sha256").read_text(encoding="utf8").split()[0]
    assert h==recorded
    tilt=data["S7_tomographic_tilt"]
    b={}
    for survey in ("des_pairs","kids_pairs"):
        pairs=tilt[survey]
        low=[float(v) for k,v in pairs.items() if k.startswith("0")]
        highest=max(int(k[0]) for k in pairs)
        high=[float(v) for k,v in pairs.items() if k.startswith(str(highest))]
        assert all(x<0 for x in low)
        assert min(low)<min(high)
        lowest=pair00=float(pairs["00"])
        highest_pair=str(highest)*2
        r_hi=float(pairs[highest_pair])
        # Fixed prospective amplitude-free ratio contrast. Cancels an overall
        # common multiplicative amplitude, but not redshift calibration errors.
        contrast=math.log1p(pair00)-math.log1p(r_hi)
        assert contrast<0
        b[survey]={"count":len(pairs),"lowest_bin_pair_count":len(low),
                   "minimum_low_z_relative_tilt":min(low),
                   "highest_bin_pair_count":len(high),
                   "highest_z_relative_tilt":high,
                   "frozen_low_over_high_log_ratio_contrast":contrast,
                   "comparison":"log[(xi_low/xi_high)_CPL/(xi_low/xi_high)_fading], derived only from already frozen ratios; not a new observed release"}
    ppd={}
    for hold,filename in (("bao","class_ppd_dovekie_bao_trunc.json"),
                          ("sn","class_ppd_dovekie_sn_trunc.json")):
        obj=load(uv/filename)
        assert obj["hold"]==hold
        ppd[hold]={}
        for label,row in obj["rows"].items():
            accepted=int(row["n"]);failed=int(row["failed"])
            ppd[hold][label]={"accepted":accepted,"solver_failed":failed,
                "failure_fraction_among_accepted_plus_failed":
                   failed/(accepted+failed),
                "outside_prior_rejected":int(row["rejected_outside_prior"]),
                "elpd_snapshot":float(row["elpd"])}
    assert ppd["bao"]["klt25_infl1"]["accepted"]==18
    assert ppd["sn"]["klt25_infl1"]["accepted"]==12
    return {"status":"FROZEN_S7_HASH_VERIFIED_AND_PRELIMINARY_KLT_PPD_COMPLETENESS_AUDIT",
      "S7_frozen_hash_sha256":h,
      "S7_local_line_ending_translation_detected":h_raw!=h,
      "S7_prediction":"CPL/fading low tomographic xi+ ratios are lower; sign-only prediction not a new observed release.",
      "S7_tomographic_signed_ratios":b,
      "new_release_holdout_scored":False,
      "KLT_preliminary_PPD_rows":ppd,
      "KLT_PPD_class":"IN_PROGRESS_SNAPSHOT_WITH_DIFFERENT_SUCCESSFUL_SAMPLE_COUNTS",
      "KLT_failures_not_physical_exclusion":True,
      "statistical_boundary":"No original KiDS/DES covariance or sample-level posterior draws are committed here; solver failures and unequal successful draws can induce selection bias. These snapshots do not justify a calibrated predictive model ranking, a Bayes factor, or a cosmic detection.",
      "provenance":"Prior published frozen S7 authored in analysis/toe_uv/prereg_tilt.py; this pass only verifies its SHA256 and audits the newly committed in-progress PPD rows."}

def produce(root=ROOT):
    return {"schema":"w33.20261108.five_boundary_bridges.v1",
      "gauge_reduction":reduced_maxwell(root),
      "native_E6_augmented_pfaffian":pfaffian_mass(root),
      "null_local_quantum_speed":null_local_speed(),
      "one_photon_photonic_scaling":one_photon_resource(),
      "cosmology_prereg_and_PPD":prereg_cosmology(root),
      "status":"TWO_EXACT_NATIVE_ALGEBRAIC_BRIDGES_TWO_FALSIFIERS_ONE_EVIDENCE_AUDIT",
      "scope":"Independent follow-through, not experimentally confirmed physics or a TOE."}
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",type=Path,default=ROOT)
    p.add_argument("--out",type=Path,default=Path("data/w33_20261108_five_boundary_bridges.json"))
    x=p.parse_args()
    result=produce(x.root)
    x.out.parent.mkdir(parents=True,exist_ok=True)
    x.out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(json.dumps({"gauge_scalar_gap":result["gauge_reduction"]["scalar_mass_gap_squared"],
      "E6_pfaffian_log_error":result["native_E6_augmented_pfaffian"]["native_log_modulus_error"],
      "q5_local_tH_min":result["null_local_quantum_speed"]["minimum_dimensionless_time_energy"],
      "one_photon_20_qutrit_modes":result["one_photon_photonic_scaling"]["example_n20_orthogonal_modes"],
      "S7_prereg_hash":result["cosmology_prereg_and_PPD"]["S7_frozen_hash_sha256"]}))
if __name__=="__main__":main()
