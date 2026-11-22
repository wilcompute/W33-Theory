#!/usr/bin/env python3
"""Exact dependency-free modular proof of minimal four-Witting-ray U(4) control.

Uses the canonical 40-ray enumeration in toe_20261121_hermitian45_pauli_sic_bridge.py.
Nonzero modular Lie-word determinants certify characteristic-zero rank.
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

SELECTED = (5, 26, 33, 36)
PRIMES = (7, 13, 19, 31, 37, 43)

def primitive_cube_root(p):
    return next(x for x in range(2, p) if x*x*x % p == 1 and x != 1)

def all_witting_rays(p):
    w = primitive_cube_root(p)
    out = []
    for j in range(4):
        v = [0]*4
        v[j] = 1
        out.append((tuple(v), tuple(v)))
    for mu in range(3):
        for nu in range(3):
            a, b = pow(w, mu, p), pow(w, nu, p)
            ac, bc = pow(w, -mu % 3, p), pow(w, -nu % 3, p)
            configs = [
                ((0,1,-a,b),(0,1,-ac,bc)),
                ((1,0,-a,-b),(1,0,-ac,-bc)),
                ((1,-a,0,b),(1,-ac,0,bc)),
                ((1,a,b,0),(1,ac,bc,0)),
            ]
            out.extend((tuple(t % p for t in v), tuple(t % p for t in vc))
                       for v, vc in configs)
    assert len(out)==40
    return out

def outer(v, vc, p):
    return tuple(v[i]*vc[j] % p for i in range(4) for j in range(4))

def commutator(a, b, p):
    return tuple(sum(a[4*i+k]*b[4*k+j]-b[4*i+k]*a[4*k+j]
                     for k in range(4)) % p
                 for i in range(4) for j in range(4))

def modular_rank(rows, p):
    pivots={}
    for original in rows:
        r=list(original)
        for j, pivot in sorted(pivots.items()):
            f=r[j]
            if f:
                r=[(x-f*y)%p for x,y in zip(r,pivot)]
        k=next((j for j,x in enumerate(r) if x), None)
        if k is None:continue
        inv=pow(r[k],-1,p)
        pivots[k]=tuple(x*inv%p for x in r)
    return len(pivots)

def exact_certificate(p, selected=SELECTED, words=None):
    rays=all_witting_rays(p)
    P=[outer(*rays[i],p) for i in selected]
    if words is None:
        mats=P.copy()
        word_list=[('P',i) for i in range(len(P))]
        layers=[len(P)]
        assert modular_rank(mats,p)==len(P)
        start=0
        for _ in range(30):
            end=len(mats)
            for old in range(start,end):
                for generator in range(len(P)):
                    candidate=commutator(P[generator],mats[old],p)
                    if modular_rank(mats+[candidate],p)>len(mats):
                        mats.append(candidate)
                        word_list.append(('B',generator,old))
                        if len(mats)==16:break
                if len(mats)==16:break
            layers.append(len(mats))
            if len(mats)==16 or len(mats)==end:break
            start=end
        return P,mats,word_list,layers
    mats=[]
    for word in words:
        if word[0]=='P':
            mats.append(P[word[1]])
        else:
            mats.append(commutator(P[word[1]],mats[word[2]],p))
    return P,mats,words,None

def verify():
    _, basis, words, layers=exact_certificate(PRIMES[0])
    assert len(basis)==16 and modular_rank(basis,PRIMES[0])==16
    results=[]
    for p in PRIMES:
        _,mats,_,_=exact_certificate(p,words=words)
        assert modular_rank(mats,p)==16
        selected=[all_witting_rays(p)[i] for i in SELECTED]
        assert modular_rank([v for v,_ in selected],p)==4
        edges=[]
        for i in range(4):
            for j in range(i+1,4):
                if sum(selected[i][1][k]*selected[j][0][k] for k in range(4))%p:
                    edges.append((i,j))
        seen={0}
        for _ in range(4):
            seen|={v for u,v in edges if u in seen}|{u for u,v in edges if v in seen}
        assert len(seen)==4
        results.append(dict(prime=p,omega=primitive_cube_root(p),
                            generator_span_rank=4,nonorthogonality_edges=edges,Lie_rank=16))
    return dict(status='PASS_EXACT_MODULAR_LIE_CERTIFICATE',
                date='2026-11-22',selected_zero_based=list(SELECTED),
                rank_layers=layers,Lie_basis_word_count=16,
                witness_words=[list(w) for w in words],
                witness_word_sha256=hashlib.sha256(
                    json.dumps(words,separators=(',',':')).encode()).hexdigest(),
                prime_certificates=results,
                theorem='Lie_R(iP5,iP26,iP33,iP36)=u(4)',
                minimality='Three rank-one projectors fix a common nonzero orthogonal subspace',
                scope='Only continuously tunable single-photon four-mode unitaries; no multiphoton deterministic entangling gate, fault tolerance or TOE.')

def main():
    data=verify()
    path=Path(__file__).resolve().parents[1]/'data'/'toe_20261122_witting_four_ray_lie_controllability.json'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print('PASS four Witting rays, u(4), rank layers',data['rank_layers'])

if __name__=='__main__':main()
