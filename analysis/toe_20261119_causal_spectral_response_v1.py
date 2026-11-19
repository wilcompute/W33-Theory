#!/usr/bin/env python3
"""Causal spectral-response gate: blind block determinant, visible Wilson response.

Finite DAGs with q-dimensional unitary parallel transport. This is an
exact finite linear-algebra theorem plus numerical controls, NOT a derived
fermionic quantum field theory, gravity measure or physical chiral Dirac operator.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "toe_20261119_causal_spectral_response_v1.json"

def dagger(a):
    return np.asarray(a).conj().T

def random_unitary(q, rng):
    z = rng.normal(size=(q,q)) + 1j*rng.normal(size=(q,q))
    x,r = np.linalg.qr(z)
    return x @ np.diag(np.diag(r)/np.abs(np.diag(r)))

def dag_operator(n,q,edges,masses,alpha):
    """A directed acyclic graph given in topological order u<v.
    Edges have unitary q x q gauge transports; arbitrary site blocks
    are allowed, but ordinary triangular determinant blindness remains.
    """
    D=np.zeros((n*q,n*q),complex)
    for i,M in enumerate(masses):
        D[i*q:(i+1)*q,i*q:(i+1)*q]=M
    for u,v,U in edges:
        assert 0 <= u < v < n and U.shape==(q,q)
        assert np.linalg.norm(dagger(U)@U-np.eye(q))<1e-10
        D[u*q:(u+1)*q,v*q:(v+1)*q]-=alpha*U
    return D

def extract(A,u,v,q):
    return A[u*q:(u+1)*q,v*q:(v+1)*q]

def diamond(W,m=1.3,alpha=0.6):
    q=W.shape[0]
    I=np.eye(q, dtype=complex)
    edges=[(0,1,I),(0,2,I),(1,3,I),(2,3,W)]
    D=dag_operator(4,q,edges,[m*I for _ in range(4)],alpha)
    G=np.linalg.inv(D)
    X=extract(G,0,3,q)
    c=alpha**4/m**6
    # W here is the second path, so relative holonomy is W^dagger.
    expectation=(alpha**2/m**3)*(I+W)
    assert np.linalg.norm(X-expectation)<1e-11
    K=dagger(D)@D
    return D,G,X,K,edges

def trace_slope_prediction(W,m=1.3,alpha=0.6):
    q=W.shape[0]
    return 4*q/m**2+4*q*alpha**2/m**4 + alpha**4/m**6*(2*q+2*np.trace(W).real)

def observables(W,m=1.3,alpha=0.6,mu=0.1,coupling=2.0):
    D,G,X,K,edges=diamond(W,m,alpha)
    q=W.shape[0]
    Kinv=np.linalg.inv(K)
    sign,logdet=np.linalg.slogdet(K+mu*np.eye(K.shape[0]))
    sign0,logdet0=np.linalg.slogdet(K)
    assert sign.real>0 and sign0.real>0
    response=float(np.exp(logdet-logdet0))
    zprobe=float(np.linalg.det(np.eye(q)+coupling*X@dagger(X)).real)
    first=float(np.trace(Kinv).real)
    second=float(np.trace(Kinv@Kinv).real)
    return {
        "q":q,"bare_det_real":float(np.linalg.det(D).real),
        "spectral_gap_inverse_trace":first,
        "closed_form_slope":trace_slope_prediction(W,m,alpha),
        "second_logdet_derivative_at_zero":-second,
        "spectrally_regularized_det_ratio_mu_0p1":response,
        "endpoint_probe_det_lambda_2":zprobe,
        "positive_regulator_min_eig":float(np.linalg.eigvalsh(K+mu*np.eye(K.shape[0]))[0]),
        "wilson_trace_real":float(np.trace(W).real),
        "wilson_trace_imag":float(np.trace(W).imag),
        "propagator_source_endpoint_normsq":float(np.trace(X@dagger(X)).real),
        "non_normal_commutator_norm":float(np.linalg.norm(K-D@dagger(D))),
    }

def run():
    m=1.3;alpha=.6
    rng=np.random.default_rng(20261119)
    # I: full-block generalization, even with nonidentical, noncommuting M_v.
    block_checks=0
    samples=[]
    for n,q in [(4,2),(7,2),(9,3),(12,3)]:
        for trial in range(8):
            masses=[]
            for i in range(n):
                Z=rng.normal(size=(q,q))+1j*rng.normal(size=(q,q))
                masses.append((m+0.1*i)*np.eye(q)+.04*(Z+dagger(Z)))
            edges=[(u,v,random_unitary(q,rng)) for u in range(n)
                for v in range(u+1,n) if rng.uniform()<.4]
            D=dag_operator(n,q,edges,masses,alpha)
            local=np.prod([np.linalg.det(M) for M in masses])
            assert np.isclose(np.linalg.det(D),local,rtol=2e-8,atol=1e-7)
            local_spect=np.concatenate([np.linalg.eigvals(M) for M in masses])
            full=np.linalg.eigvals(D)
            # Compare characteristic polynomials rather than unstable eigenvector ordering.
            assert np.allclose(np.sort_complex(full),np.sort_complex(local_spect),atol=1e-7,rtol=1e-7)
            assert np.isclose(np.linalg.det(dagger(D)@D),abs(local)**2,rtol=3e-8,atol=1e-7)
            block_checks+=1
            samples.append((n,q,len(edges)))
    # II: U(1), SU(2) and SU(3) causal-diamond Wilson sensitivity.
    su2=[]
    for theta in [0,np.pi/3,np.pi/2,np.pi]:
        W=np.diag([np.exp(1j*theta),np.exp(-1j*theta)])
        o=observables(W)
        assert abs(o["spectral_gap_inverse_trace"]-o["closed_form_slope"])<1e-10
        expected=(1+2*2*(alpha**4/m**6)*(1+np.cos(theta)))**2
        assert abs(o["endpoint_probe_det_lambda_2"]-expected)<1e-10
        assert abs(o["bare_det_real"]-m**8)<1e-9
        su2.append({"angle":float(theta), **o})
    assert su2[0]["spectrally_regularized_det_ratio_mu_0p1"] > su2[-1]["spectrally_regularized_det_ratio_mu_0p1"]
    # III: gauge-frame covariance across all 4 vertices in U(3).
    phi=0.83
    W=np.diag([np.exp(1j*phi),np.exp(.31j),np.exp(-1j*(phi+.31))])
    D,G,X,K,edges=diamond(W)
    z=observables(W)
    max_errors=[0.0,0.0,0.0]
    for _ in range(24):
        frames=[random_unitary(3,rng) for _ in range(4)]
        H=np.zeros((12,12),complex)
        for i,U in enumerate(frames):H[i*3:(i+1)*3,i*3:(i+1)*3]=U
        D2=H@D@dagger(H)
        G2=np.linalg.inv(D2);X2=extract(G2,0,3,3)
        e0=float(np.linalg.norm(X2-frames[0]@X@dagger(frames[3])))
        e1=abs(np.trace(X2@dagger(X2))-np.trace(X@dagger(X)))
        K2=dagger(D2)@D2
        e2=abs(np.linalg.det(K2+.1*np.eye(12))/np.linalg.det(K2) -
               np.linalg.det(K+.1*np.eye(12))/np.linalg.det(K))
        max_errors=[max(max_errors[i],v) for i,v in enumerate([e0,e1,e2])]
        assert max([e0,e1,e2])<1e-8
    # IV: SU(3) non-Abelian shape that defeats a mere Re Tr(W) diagnostic.
    p=1.0
    target=2*np.cos(p)+np.cos(2*p)
    theta=float(np.arccos((target-1)/2))
    W_real=np.diag([np.exp(1j*theta),np.exp(-1j*theta),1.])
    W_complex=np.diag([np.exp(1j*p),np.exp(1j*p),np.exp(-2j*p)])
    assert abs(np.linalg.det(W_real)-1)<1e-12
    assert abs(np.linalg.det(W_complex)-1)<1e-12
    a=observables(W_real);b=observables(W_complex)
    assert abs(a["wilson_trace_real"]-b["wilson_trace_real"])<1e-12
    assert abs(a["spectral_gap_inverse_trace"]-b["spectral_gap_inverse_trace"])<1e-10
    assert abs(a["second_logdet_derivative_at_zero"]-b["second_logdet_derivative_at_zero"])>1e-4
    assert abs(a["spectrally_regularized_det_ratio_mu_0p1"]-b["spectrally_regularized_det_ratio_mu_0p1"])>1e-6
    # V: actual topology selection DOES NOT follow from response sensitivity.
    # Positive probe factors favor constructive path degeneracy if inserted with plus sign,
    # but an undetermined sign/measure/reference alters that choice.
    q=2;I=np.eye(q);Dempty=dag_operator(4,q,[],[m*I for _ in range(4)],alpha)
    baseline=float(np.trace(np.linalg.inv(dagger(Dempty)@Dempty)).real)
    assert su2[0]["spectral_gap_inverse_trace"]>baseline
    certificate={
        "date":"2026-11-19",
        "status":"FINITE_LINEAR_ALGEBRA_PASS_NOT_A_TOE",
        "head_at_start":"f73c83e853157a305507ed52f9631e7b80a03413",
        "theorem":"A block-forward causal DAG operator has graph-independent characteristic polynomial, determinant and bare Hermitianized determinant. Its inverse singular-value response and endpoint-conditioned positive determinant detect gauge-covariant path interference.",
        "block_dag_cases":block_checks,"block_dag_sample_summary":samples[:8],
        "su2_diamond":su2,
        "gauge_frame_checks":24,"gauge_max_residuals":max_errors,
        "su3_same_first_wilson_moment":{
          "theta_real_family":theta,"phi_complex_family":p,
          "case_A":a,"case_B":b,
          "positive_det_ratio_difference":b["spectrally_regularized_det_ratio_mu_0p1"]-a["spectrally_regularized_det_ratio_mu_0p1"]},
        "empty_graph_trace_response":baseline,
        "caveats":["Site masses and links supplied, not derived",
          "D is not a physical Lorentzian spin Dirac operator",
          "Positive regulator mu introduces a new operator not equal to D^dagger D",
          "Detector/probe factor is an observable, not a derived quantum gravity measure",
          "No reflection positivity, anomaly cancellation, or continuum limit proved"] }
    return certificate

if __name__=="__main__":
    result=run()
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:v for k,v in result.items() if k not in ("su2_diamond","su3_same_first_wilson_moment","block_dag_sample_summary")},indent=2))
    print("CERTIFICATE",OUT)
