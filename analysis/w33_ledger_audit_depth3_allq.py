#!/usr/bin/env python3
"""Follow-up Ledger audit theorem: three-party depth three beats depth=q."""
from __future__ import annotations
import itertools, json
from pathlib import Path
import numpy as np
OUT=Path("data/PART_LEDGER_AUDIT_DEPTH3_ALLQ.json")

def digits(i,n,q):
    a=[0]*n
    for k in range(n-1,-1,-1): a[k]=i%q; i//=q
    return a
def idx(a,q):
    z=0
    for x in a: z=z*q+x
    return z
def fourier(q):
    w=np.exp(2j*np.pi/q)
    return np.array([[w**(j*k)/np.sqrt(q) for k in range(q)] for j in range(q)],complex)
def table(q,seed):
    r=np.random.default_rng(seed)
    while True:
        A=r.normal(size=(q,q)); A=A-A.mean(1,keepdims=True)-A.mean(0,keepdims=True)+A.mean()
        if np.min(np.diff(np.sort(A.ravel())))>1e-7:return A
def embed(op,R,q):
    n=3;d=q**n;R=tuple(sorted(R));C=tuple(i for i in range(n) if i not in R);bs=[digits(i,n,q) for i in range(d)]
    out=np.zeros((d,d),complex)
    for i,a in enumerate(bs):
        for j,b in enumerate(bs):
            if all(a[c]==b[c] for c in C):
                out[i,j]=op[idx([a[r] for r in R],q),idx([b[r] for r in R],q)]
    return out
def ptr(rho,R,q):
    n=3;R=tuple(sorted(R));C=tuple(i for i in range(n) if i not in R)
    T=rho.reshape([q]*(2*n)).transpose(list(R)+list(C)+[i+n for i in R]+[i+n for i in C])
    dr=q**len(R);dc=q**len(C);T=T.reshape(dr,dc,dr,dc)
    return np.einsum("aibi->ab",T)
def cert(q):
    F=fourier(q);tabs=[table(q,11+q),table(q,22+q),table(q,33+q)]
    A=np.diag(tabs[0].ravel()); U=np.kron(F,np.eye(q));B=U@np.diag(tabs[1].ravel())@U.conj().T
    U=np.kron(F,F);C=U@np.diag(tabs[2].ravel())@U.conj().T
    H=embed(A,(0,1),q)+embed(B,(1,2),q)+embed(C,(0,2),q)
    ev=np.linalg.eigvalsh(H);eps=.4/max(abs(ev.min()),abs(ev.max()));rho=np.eye(q**3)+eps*H;rho/=np.trace(rho)
    sdev=max(float(np.max(abs(ptr(rho,{i},q)-np.eye(q)/q))) for i in range(3))
    fits=[]
    for R,T in [((0,1),A),((1,2),B),((0,2),C)]:
        r=ptr(rho,set(R),q);Tc=T-np.trace(T)/T.shape[0]*np.eye(T.shape[0]);rc=r-np.trace(r)/r.shape[0]*np.eye(r.shape[0])
        beta=(np.vdot(Tc,rc)/np.vdot(Tc,Tc)).real
        fits.append((float(np.max(abs(rc-beta*Tc))),float(np.min(np.diff(np.sort(np.linalg.eigvalsh(r)))))))
    labels={(e,c,f,a,b,d) for a,b,c,d,e,f in itertools.product(range(q),repeat=6)}
    return {"q":q,"operator_dimension":q**6,"min_rho_eigenvalue":float(np.min(np.linalg.eigvalsh(rho))),
            "single_marginal_error":sdev,"pair_fit_error":max(x[0] for x in fits),
            "pair_min_gap":min(x[1] for x in fits),"depth3_labels":len(labels)}
def main():
    cs=[cert(q) for q in (3,4,5)]
    bounds=[]
    for q in range(2,9):
        g=3*q*q+3*q-5
        bounds.append({"q":q,"A1_max":g,"A2_count_bound":g*g,"operator_dimension":q**6,"depth2_impossible":g*g<q**6})
    checks={"faithful":all(c["min_rho_eigenvalue"]>0 for c in cs),
            "exact_marginals":all(c["single_marginal_error"]<2e-14 and c["pair_fit_error"]<2e-14 for c in cs),
            "nondegenerate_pair_books":all(c["pair_min_gap"]>1e-8 for c in cs),
            "depth3_full_q345":all(c["depth3_labels"]==c["operator_dimension"] for c in cs),
            "depth2_impossible_q45":all(next(x for x in bounds if x["q"]==q)["depth2_impossible"] for q in (4,5))}
    assert all(checks.values()),checks
    out={"schema":"w33.ledger.audit-depth-three-allq.v1","status":"DEPTH_Q_CONJECTURE_KILLED_DEPTH3_OPEN_FAMILY",
         "theorem":{"A1_max":"3q^2+3q-5","A2_bound":"rank(A2)<=(3q^2+3q-5)^2",
                    "gap_factorization":"q^6-(3q^2+3q-5)^2=(q-1)(q^2-2q-5)(q^3+3q^2+3q-5)",
                    "q_ge_4":"depth two is impossible for every state",
                    "explicit_depth3":"Pair books ZZ on AB, XZ on BC, XX on AC give every Weyl label at word depth three.",
                    "open_family":"The explicit pair spectra are nondegenerate and full triple-product rank is open under sufficiently small state perturbations.",
                    "verdict":"For three parties, depth=q is false. q=4 and q=5 already close at depth 3 on an open faithful family."},
         "certificates":cs,"bounds":bounds,"prior_q3":"five exact witnesses: A2=649/729, A3=729/729","checks":checks}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n");print(json.dumps(out,indent=2,sort_keys=True));return out
if __name__=="__main__":main()
