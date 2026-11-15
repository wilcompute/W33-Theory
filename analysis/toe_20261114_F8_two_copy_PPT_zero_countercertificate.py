#!/usr/bin/env python3
"""Exact PPT countercertificate for the simple symmetric two-copy F8 relaxation.

A Bell-diagonal symmetric PPT density matrix has sum_{P covered} Tr(rho
(P tensor P))=0. Hence this relaxation cannot show a positive pure-state
certainty minimum. Does not contradict stronger PPT/higher-copy bounds.
"""
from collections import Counter
from fractions import Fraction as Fr
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "toe_20261114_F8_two_copy_PPT_zero_countercertificate.json"

def mul(a,b):
    r=0
    while b:
        if b&1:r^=a
        b>>=1
        a<<=1
        if a&8:a^=0b1011
    return r

def trace(a):
    x=a;s=0
    for _ in range(3):
        s^=x
        x=mul(x,x)
    return s

def dual(a):
    return sum(trace(mul(a,1<<k))<<k for k in range(3))

def fwht(values):
    a=values[:]
    step=1
    while step<len(a):
        jump=2*step
        for i in range(0,len(a),jump):
            for j in range(i,i+step):
                p,q=a[j],a[j+step]
                a[j],a[j+step]=p+q,p-q
        step=jump
    return a

def symparity(u,z):
    return (u&z).bit_count()&1

def run():
    groups=[]
    groups.append({(0,z) for z in range(1,64)})
    for t in range(8):
        # Six commuting generators; displacement (x,y) has phase label
        # (t*y,t*x) expressed using the trace-dual F8 coordinates.
        gs=[(8*(1<<k),dual(mul(t,1<<k))) for k in range(3)]+[
            (1<<k,8*dual(mul(t,1<<k))) for k in range(3)
        ]
        group=set()
        for mask in range(1,64):
            u=z=0
            for k,(a,b) in enumerate(gs):
                if mask>>k&1:u^=a;z^=b
            group.add((u,z))
        assert len(group)==63
        assert all(symparity(*x)==0 for x in group)
        groups.append(group)
    covered=set.union(*groups)
    assert len(covered)==567
    assert sum(len(groups[i]&groups[j]) for i in range(9) for j in range(i+1,9))==0
    # The Bell labels are (u,z) encoded as u+64z.
    qeven=[0]*4096
    iscovered=[0]*4096
    for u in range(64):
        for z in range(64):
            idx=u+64*z
            qeven[idx]=1-symparity(u,z)
            iscovered[idx]=int((u,z) in covered)
    assert sum(qeven)==2080 and sum(iscovered)==567
    WC=fwht(iscovered)
    WE=fwht(qeven)
    # Exact three-shell state diagonal in the 4096 Bell basis.
    p0=Fr(0)
    pc=Fr(1,4032)
    pn=Fr(55,96768)
    assert p0+567*pc+1512*pn==1
    pt_counts=Counter()
    spectra=Counter()
    bounds=Counter()
    for u in range(64):
        for z in range(64):
            idx=u+64*z
            widx=z+64*u # symplectic Walsh character v -> (z_v,u_v)
            q=symparity(u,z)
            cw=iscovered[idx]
            even=qeven[idx]
            shell="identity" if idx==0 else "covered" if cw else "even_uncovered" if even else "odd"
            spectra[shell]+=1
            cov=WC[widx]
            ev=WE[widx]
            assert cov == (567 if idx==0 else 55 if cw else -9)
            assert ev == (2080 if idx==0 else (32 if not q else -32))
            # PT of a Bell projector labelled w has eigenvalue
            # (-1)^q(v)*(-1)^omega(v,w)/d on the v Bell state
            # whenever the supported w is a symmetric Bell label.
            alpha=(Fr(-1) if q else Fr(1))*(p0+pc*cov+pn*(ev-1-cov))/64
            assert alpha>=0, (shell,alpha)
            pt_counts[str(alpha)]+=1
            bounds[shell]+=alpha
    assert spectra=={"identity":1,"covered":567,"even_uncovered":1512,"odd":2016}
    assert pt_counts=={"1/64":1,"0":567,"31/96768":1512,"1/4032":2016}
    assert sum(bounds.values(),Fr(0))==1
    # The original K operator's symmetric Bell eigenvalues: 567,55,-9.
    Kexp=567*p0 + 55*567*pc - 9*1512*pn
    assert Kexp==0
    result={
      "status":"EXACT_SYMMETRIC_TWO_COPY_PPT_FEASIBLE_ZERO",
      "n_bases":9,"covered_Pauli_labels":567,
      "Bell_weights":{"identity":str(p0),"covered_each":str(pc),"even_uncovered_each":str(pn),"antisymmetric_each":"0"},
      "state_positive":True,"state_swap_symmetric":True,
      "partial_transpose_spectrum":dict(pt_counts),
      "partial_transpose_trace":str(sum(bounds.values(),Fr(0))),
      "K_expectation":str(Kexp),
      "logical_conclusion":"A symmetric two-copy PPT relaxation has a feasible state with objective zero, so its global infimum is at most zero and cannot certify any positive pure-state lower bound. A negative PPT optimum is not excluded.",
      "limitation":"Does not prove existence of a physical pure state with c8=0; stronger relaxations (higher moments, multi-copy extensions, purity identities) are not excluded. Does not invalidate a previously reported stronger PPT dual bound using additional constraints."
    }
    OUTPUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    return result

if __name__=="__main__":
    d=run()
    print(d["status"],d["partial_transpose_spectrum"])
