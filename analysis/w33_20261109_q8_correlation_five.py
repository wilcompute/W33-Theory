#!/usr/bin/env python3
"""W33 Q8 correlation tomography and five falsification-oriented physics fronts.

Tracks: exact/tight mixed Schmidt-number witness; calibration- and
finite-shot-robust dual LP; nine-mode optical factorization; supplied-dimension
continuum heat-kernel check; fail-closed DES Y6 preregistration audit.

Uses the independently published Q8 producer for the Clifford matrices.
No claim of hardware results, a continuum field theory, or cosmology likelihood.
"""
import itertools
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import linprog
from w33_20261109_q8_design_purity import I, mul, order, generators_as_unitaries

ROOT = Path(__file__).resolve().parents[1]


def frames():
    G = sorted(g for g in itertools.product(range(3), repeat=4)
               if (g[0]*g[3]-g[1]*g[2]) % 3 == 1)
    Q = frozenset(g for g in G if order(g) in (1, 2, 4))
    cosets = sorted({frozenset(mul(g, q) for q in Q) for g in G},
                    key=lambda v: sorted(v))
    gates = generators_as_unitaries(G)
    assert len(G) == 24 and len(Q) == 8 and len(cosets) == 3
    return gates, [np.concatenate([gates[g] for g in sorted(c)], axis=1)
                   for c in cosets]


def hermitian_basis():
    H = []
    for i in range(3):
        for j in range(i+1, 3):
            X = np.zeros((3, 3), complex)
            X[i, j] = X[j, i] = 1/np.sqrt(2)
            H.append(X)
            Y = np.zeros((3, 3), complex)
            Y[i, j], Y[j, i] = -1j/np.sqrt(2), 1j/np.sqrt(2)
            H.append(Y)
    H += [np.diag([1, -1, 0])/np.sqrt(2),
          np.diag([1, 1, -2])/np.sqrt(6)]
    assert len(H) == 8
    return [np.kron(x, y) for x in H for y in H]


def frame_map(E, operators):
    A = np.array([np.einsum("i,kij,j->k", e.conj(), operators, e).real
                  for e in E.T])
    assert A.shape == (72, 64)
    return A


def rho_schmidt(xs):
    v = np.zeros(9, complex)
    for i, x in enumerate(xs):
        v[4*i] = np.sqrt(x)
    return np.outer(v, v.conj())


def probabilities(E, rho):
    return np.einsum("ij,ik,kj->j", E.conj(), rho, E).real


def tensor_direct(rho, operators):
    return np.array([np.trace(rho @ h).real for h in operators]).reshape(8,8)


def tensor_recovered(A, p):
    return (A.T @ (p - 1/9)).reshape(8, 8)


def trace_norm(T):
    return float(np.linalg.svd(T, compute_uv=False).sum())


def correlation_checks():
    gates, bases = frames()
    operators = np.array(hermitian_basis())
    maps = [frame_map(E, operators) for E in bases]
    tight = max(float(np.max(abs(A.T @ A - np.eye(64)))) for A in maps)
    assert tight < 4e-12
    rng = np.random.default_rng(202611091)
    reconstruction, pure = [], []
    for rank in (1, 2, 3, 6, 9):
        for _ in range(8):
            x = rng.normal(size=(9, rank))+1j*rng.normal(size=(9, rank))
            rho = x @ x.conj().T
            rho /= np.trace(rho)
            T = tensor_direct(rho, operators)
            for E, A in zip(bases, maps):
                p = probabilities(E, rho)
                reconstructed = tensor_recovered(A, p)
                reconstruction.append(float(np.max(abs(T-reconstructed))))
                assert abs(float(np.sum((p-1/9)**2))-float(np.sum(T*T)))<3e-12
    for k in (1, 2, 3):
        for _ in range(18):
            lam = rng.dirichlet(np.ones(k))
            T = tensor_direct(rho_schmidt(lam), operators)
            pure.append(abs(trace_norm(T) - (sum(np.sqrt(lam))**2-1/3)))
            assert trace_norm(T) <= k-1/3+1e-12
    assert max(reconstruction+pure)<5e-12
    iso={}
    for eta in (.2, .3, .5, .65, .8, 1.):
        rho = eta*rho_schmidt([1/3]*3)+(1-eta)*np.eye(9)/9
        T = tensor_recovered(maps[0], probabilities(bases[0],rho))
        assert abs(trace_norm(T)-8*eta/3)<3e-12
        iso[str(eta)] = {"correlation_trace_norm":trace_norm(T),
                         "Schmidt_number_at_least_2":trace_norm(T)>2/3+1e-12,
                         "Schmidt_number_3":trace_norm(T)>5/3+1e-12}
    return {
        "max_orthonormal_frame_error":tight,
        "max_mixed_correlation_reconstruction_error":max(reconstruction),
        "max_pure_Schmidt_trace_norm_identity_error":max(pure),
        "random_mixed_density_matrices":40,
        "random_pure_schmidt_vectors":54,
        "rows":72, "columns":64, "frame_rank":64,
        "unmeasured_local_bloch_components":16,
        "exact_Gram":"A.T @ A = I_64",
        "pure_formula":"||T||_*=(sum_i sqrt(lambda_i))^2-1/3",
        "tight_mixed_bounds":{
            "Schmidt_number_le_1":2/3,
            "Schmidt_number_le_2":5/3,
            "Schmidt_number_le_3":8/3},
        "visibility_2":1/4, "visibility_3":5/8,
        "isotropic_checks":iso,
    },gates,bases,maps,operators


def min_dual_lp(A,q,low,high,rad):
    """Valid one-sided nuclear-norm lower confidence bound.

    Unknown ideal p and detected v=eta*p; s=sum(v), observed q=v/s.
    Introduce p_j,v_j,s and impose linear inequalities:
      low_eta*p<=v<=high_eta*p, (qhat-rad)*s<=v<=(qhat+rad)*s.
    If q is within the simultaneous confidence intervals, true p is feasible.
    A data-dependent dual W=U V.T with spectral norm one always obeys
      ||T_true||_* >= <W,T_true>; minimize latter over physical intervals.
    """
    A3=A.reshape(8,9,64)
    q=q.reshape(8,9)
    mid=(low+high)/2
    phat=[]
    for qb in q:
        x=qb/mid
        phat.extend(x/sum(x))
    T=tensor_recovered(A,np.array(phat))
    u,_,vh=np.linalg.svd(T)
    W=u@vh
    assert np.linalg.norm(W,ord=2)<1+1e-11
    obj=A@W.reshape(64)
    total=0.
    for b in range(8):
        c=np.zeros(19);c[:9]=obj[9*b:9*b+9]
        ae=np.zeros((2,19))
        ae[0,:9]=1.
        ae[1,9:18]=1.
        ae[1,18]=-1.
        ub=[]
        for j in range(9):
            qlo=max(0,q[b,j]-rad)
            qhi=min(1,q[b,j]+rad)
            row=np.zeros(19);row[j]=-high[j];row[9+j]=1.;ub.append(row)
            row=np.zeros(19);row[j]=low[j];row[9+j]=-1.;ub.append(row)
            row=np.zeros(19);row[9+j]=1.;row[18]=-qhi;ub.append(row)
            row=np.zeros(19);row[9+j]=-1.;row[18]=qlo;ub.append(row)
        bounds=[(0,1)]*9+[(0,float(max(high)))]*9+[(float(min(low)),float(max(high)))]
        sol=linprog(c,A_ub=np.array(ub),b_ub=np.zeros(36),
                    A_eq=ae,b_eq=np.array([1.,0.]),bounds=bounds,method="highs")
        assert sol.success,sol.message
        total+=sol.fun
    return {"lower_bound":float(total),
            "nominal":trace_norm(T),
            "SN2_certified":total>2/3,
            "SN3_certified":total>5/3,
            "radius_per_outcome":rad}


def detector_checks(E,A):
    rng=np.random.default_rng(202611092)
    eff=np.array([.63+.045*j for j in range(9)])
    low,high=eff*.99,eff*1.01
    outputs={}
    for label, vis in (("product",None),("isotropic_0p5",.5),
                       ("isotropic_0p8",.8),("max_entangled",1.)):
        rho=rho_schmidt([1]) if vis is None else vis*rho_schmidt([1/3]*3)+(1-vis)*np.eye(9)/9
        p=np.array([probabilities(E[:,9*b:9*(b+1)],rho) for b in range(8)])
        q=(p*eff[None,:])
        q=q/q.sum(axis=1,keepdims=True)
        exact=min_dual_lp(A,q,low,high,0)
        wide=min_dual_lp(A,q,np.full(9,min(eff)),np.full(9,max(eff)),0)
        finite=None
        if label=="isotropic_0p8":
            N=150000
            qobs=np.array([rng.multinomial(N,v)/N for v in q])
            rad=math.sqrt(math.log(2*72/.05)/(2*N))
            finite=min_dual_lp(A,qobs,low,high,rad)
            assert finite["SN3_certified"]
        true_T=tensor_direct(rho,np.array(hermitian_basis()))
        assert exact["lower_bound"] < trace_norm(true_T)+1e-9
        outputs[label]={"true_trace_norm":trace_norm(true_T),
                        "nominal_calibrated_interval":exact,
                        "wide_efficiency_interval":wide,
                        "finite_sample_control":finite}
    assert not outputs["product"]["wide_efficiency_interval"]["SN2_certified"]
    return {"status":"ROBUST_LINEAR_PROGRAM_VALID_CONSERVATIVE_CERTIFICATE",
            "per_setting_efficiency":list(map(float,eff)),
            "efficiency_intervals":"nominal +/-1% relative, or universal broad [0.63,0.99]",
            "finite_count_alpha":.05,
            "finite_count_accepted_per_setting":150000,
            "confidence_radius_method":"union bound over 72 binomial outcomes, Hoeffding",
            "experiments":outputs,
            "caveat":"synthetic IID accepted samples, trusted efficiency intervals, no actual detector or hardware; independent source drift invalidates confidence"}


def optical_check(gates):
    w=np.exp(2j*np.pi/3)
    Wbell=np.zeros((9,9),complex)
    for a in range(3):
        for b in range(3):
            for r in range(3):
                Wbell[3*a+b,3*r+(r+a)%3]=w**(-b*r)/np.sqrt(3)
    errors=[]; gate_counts=[]
    Eall=generators_as_unitaries(sorted(gates))
    assert np.max(abs(Wbell-Eall[I].conj().T))<3e-12
    for s,U in gates.items():
        W=Wbell@np.kron(U.conj(),np.eye(3))
        errors.append(float(np.max(abs(W-Eall[s].conj().T))))
        R=U.conj().copy()
        n=0
        for col in (0,1):
            for row in range(2,col,-1):
                a,b=R[row-1,col],R[row,col]
                norm=np.hypot(abs(a),abs(b))
                g=np.eye(3,dtype=complex)
                if norm>1e-14:
                    g[row-1,row-1]=a.conj()/norm
                    g[row-1,row]=b.conj()/norm
                    g[row,row-1]=-b/norm
                    g[row,row]=a/norm
                R=g@R
                n+=1
        assert np.max(abs(R-np.diag(np.diag(R))))<3e-12
        gate_counts.append(3*n+9)
    assert max(errors)<3e-12
    assert max(gate_counts)<=18
    return {"number_of_contexts":len(gates),"verified_matrix_error":max(errors),
            "max_two_mode_couplers_per_9mode_context":max(gate_counts),
            "bell_transform":"3 qutrit Fourier tritters plus 9-mode modular-difference permutation",
            "local_context":"conjugate(U_S) tensor identity_3; 3 copies of U3 with <=3 Givens each",
            "formula":"W_S=W_Bell @ (conjugate(U_S) tensor I3)",
            "scope":"nine resolved single-photon optical modes; phase, crossing, switching, encoding, loss and feedforward not budgeted"}


def continuum_null():
    spec=[(0,1),(4-math.sqrt(6),24),(4,30),(4+math.sqrt(6),24),(8,1)]
    tvals=(8,16,32,64)
    L=256
    data={}
    for d in (3,4):
        rows={}
        for t in tvals:
            kt=4*np.sin(np.pi*np.arange(L)/L)**2
            weights=np.exp(-t*kt)
            sw=sum(m*np.exp(-t*v) for v,m in spec)
            dsw=sum(m*v*np.exp(-t*v) for v,m in spec)
            dim=2*t*(dsw/sw+d*np.dot(kt,weights)/sum(weights))
            rows[str(t)]=float(dim)
        assert abs(rows["64"]-d)<.04
        data[str(d)]=rows
    return {"model":"Levi(W33) Cartesian Z_256^d, d supplied as 3 or 4",
            "exact_spectral_gap":"4-sqrt(6)",
            "dispersion":"lambda_W+4*sum_i sin(pi*k_i/256)^2",
            "running_dimensions":data,
            "conclusion":"Neither dimension is selected by W33: it is an input from the added lattice; not a native continuum TOE or Lorentz proof"}


def cosmology_prereg_audit():
    prereg=json.loads((ROOT/"analysis/toe_uv/prereg_noshear.json").read_text())["S9_shear_no_split"]
    fixed=json.loads((ROOT/"analysis/toe_uv/class_fit_dovekie.json").read_text())
    assert prereg["frozen"]=="2026-11-08"
    selected={}
    for model in ("LCDM_native","CPL","free_neg","free_pos"):
        selected[model]=float(fixed[model]["info"]["S8"])
    y6=.789
    return {
        "DES_Y6_public_LambdaCDM_S8":y6,
        "DES_Y6_public_LambdaCDM_S8_sigma":.012,
        "DES_Y6_published_source":"https://www.darkenergysurvey.org/des-y6-cosmology-results-papers/ (published 2026 paper arXiv:2601.14559)",
        "frozen_Dovekie_pre_Halofit_refit_S8":selected,
        "raw_one_dimensional_differences_from_DES_Y6_over_reported_sigma":
            {k:(v-y6)/.012 for k,v in selected.items()},
        "S9_scored":False,
        "why_not_scored":"DES Y6 published LambdaCDM S8 is NOT a model-specific cosmic shear data-vector likelihood; S9 requires DES Y6 xi+/- covariance, matching scale cuts, patched CLASS/Halofit predictions, nuisance refits, and a blinded held-out protocol.",
        "Euclid_DR1_foundation_scheduled":"2026-11-12; not available as of 2026-11-09 and DR1 higher-level shear products expected later",
        "warning":"S8 summary pull is illustrative and NOT chi2 evidence against CPL or fading or a test of the pre-registered S9 threshold"
    }


def calculate():
    w,gates,bases,maps,_=correlation_checks()
    return {"status":"PASS_FIVE_FRONTS_EXACT_FINITE_QM_TOY_SCALING_WITH_COSMO_GATE",
            "track_1_exact_tight_schmidt":w,
            "track_2_detector_confidence_LP":detector_checks(bases[0],maps[0]),
            "track_3_optical_compilation":None,  # populated in main() after reconstructing Clifford U_s
            "track_4_scaling_null":continuum_null(),
            "track_5_cosmology_prereg":cosmology_prereg_audit(),
            "not_a_TOE":True}


def main(path=None):
    out=calculate()
    # Use the same symplectic generators U_s as the published producer.
    G=sorted(g for g in itertools.product(range(3),repeat=4)
             if (g[0]*g[3]-g[1]*g[2])%3==1)
    w=np.exp(2j*np.pi/3)
    F=np.array([[w**(i*j) for j in range(3)] for i in range(3)])/np.sqrt(3)
    P=np.diag([1,1,w])
    U={I:np.eye(3,dtype=complex)}
    q=[I]
    for s in q:
        for t,op in (((0,2,1,0),F),((1,0,1,1),P)):
            st=mul(s,t)
            if st not in U:
                U[st]=U[s]@op
                q.append(st)
    assert len(U)==24
    out["track_3_optical_compilation"]=optical_check(U)
    if path:
        Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS Five fronts Q8",json.dumps({
        "rank":out["track_1_exact_tight_schmidt"]["frame_rank"],
        "frame_error":out["track_1_exact_tight_schmidt"]["max_orthonormal_frame_error"],
        "max_optical_error":out["track_3_optical_compilation"]["verified_matrix_error"],
        "finite_SN3_certified":out["track_2_detector_confidence_LP"]["experiments"]["isotropic_0p8"]["finite_sample_control"]["SN3_certified"],
        "S9_scored":out["track_5_cosmology_prereg"]["S9_scored"]
    }))
    return out


if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else None)
