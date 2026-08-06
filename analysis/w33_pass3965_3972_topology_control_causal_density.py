#!/usr/bin/env python3
"""Exact/declared-model verifier for Passes 3965--3972.

Quick mode reconstructs W(3,3), the SRG residual primitives, all weight-two
fingerprints, the four-generator automorphism group, the 24-port commutant
certificate, the causal-density formulas, and semantic equality with the
frozen certificate.

`--heavy` additionally regenerates the 78,788,060 weight-three fingerprint
ledger and the alternating weight-four / simple weight-six zero-residual
firewalls.  The heavy replay uses a temporary uint64 memmap and is intended
for a large CI runner or manual evidence job, not an interactive notebook.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import itertools
import json
import math
import tempfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "data" / "PART_3965_3972_TOPOLOGY_CONTROL_CAUSAL_DENSITY_results.json"
MASK64 = (1 << 64) - 1
PORTS = [0,1,2,4,5,6,7,8,9,13,14,16,17,22,23,3,10,11,15,18,25,26,31,32]
GEN_VECTORS = [(0,0,0,1),(0,1,0,0),(0,0,1,1),(1,0,0,0)]
SEMANTIC = "90911496d42850652801e77da5bf6523027f5e3a52e8d906a9e817526fa68d57"


def canonical_json_sha(obj: dict) -> str:
    work = json.loads(json.dumps(obj))
    work.pop("semantic_sha256", None)
    raw = json.dumps(work, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def norm_projective(v: tuple[int, ...]) -> tuple[int, ...]:
    v = tuple(x % 3 for x in v)
    for x in v:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv*y) % 3 for y in v)
    raise ValueError("zero vector")


def points40() -> list[tuple[int, int, int, int]]:
    return sorted({norm_projective(v) for v in itertools.product(range(3), repeat=4) if any(v)})


def symp(x, y) -> int:
    # Standard alternating form with coordinate pairs (0,2), (1,3).
    return (x[0]*y[2] + x[1]*y[3] - x[2]*y[0] - x[3]*y[1]) % 3


def build_w33():
    pts = points40()
    assert len(pts) == 40
    A = np.zeros((40,40), dtype=np.int64)
    for i,x in enumerate(pts):
        for j in range(i+1,40):
            if symp(x, pts[j]) == 0:
                A[i,j] = A[j,i] = 1
    return pts, A


def verify_srg(A):
    I = np.eye(40, dtype=np.int64)
    J = np.ones((40,40), dtype=np.int64)
    assert np.all(A == A.T)
    assert not np.any(np.diag(A))
    assert np.all(A.sum(axis=1) == 12)
    assert np.array_equal(A @ A, 8*I - 2*A + 4*J)
    eig = np.linalg.eigvalsh(A.astype(float))
    got = collections.Counter(int(round(x)) for x in eig)
    assert got == collections.Counter({-4:15, 2:24, 12:1})


def candidates(A):
    out = []
    for u in range(40):
        for v in range(u+1,40):
            out.append((u,v,-1 if A[u,v] else 1))
    assert len(out) == 780
    assert sum(s < 0 for _,_,s in out) == 240
    assert sum(s > 0 for _,_,s in out) == 540
    return out


def residual(A, toggles):
    D = np.zeros_like(A)
    for u,v,s in toggles:
        D[u,v] += s
        D[v,u] += s
    return A@D + D@A + D@D + 2*D


def fp_u64(C, M) -> np.uint64:
    words = np.asarray(M, dtype=np.int64).view(np.uint64)
    return np.sum(C * words, dtype=np.uint64)


def fingerprint_primitives(A, cand):
    rng = np.random.default_rng(20260805)
    C = rng.integers(0, np.iinfo(np.uint64).max, size=(40,40),
                     dtype=np.uint64, endpoint=True)
    assert hashlib.sha256(C.tobytes()).hexdigest() == \
        "1b4e7c98a197dbc9878c46b808ba074f6ff9785b765aeba3d45f63d611967945"
    n = len(cand)
    singles = np.zeros(n, dtype=np.uint64)
    Es = []
    for q,(u,v,s) in enumerate(cand):
        E = np.zeros_like(A)
        E[u,v] = E[v,u] = 1
        Es.append(E)
        singles[q] = fp_u64(C, s*(A@E + E@A + 2*E) + E@E)
    pair = np.zeros((n,n), dtype=np.uint64)
    by_vertex = [[] for _ in range(40)]
    for q,(u,v,_) in enumerate(cand):
        by_vertex[u].append(q); by_vertex[v].append(q)
    seen = set()
    for bucket in by_vertex:
        for i,j in itertools.combinations(bucket,2):
            if (i,j) in seen:
                continue
            seen.add((i,j))
            si, sj = cand[i][2], cand[j][2]
            cross = si*sj*(Es[i]@Es[j] + Es[j]@Es[i])
            pair[i,j] = pair[j,i] = fp_u64(C, cross)
    return C, singles, pair


def weight2_ledger(singles, pair):
    n = len(singles)
    vals = np.empty(n*(n-1)//2, dtype=np.uint64)
    k = 0
    for i in range(n-1):
        m = n-i-1
        vals[k:k+m] = singles[i] + singles[i+1:] + pair[i,i+1:]
        k += m
    assert k == len(vals)
    vals.sort()
    assert not np.any(vals[1:] == vals[:-1])
    digest = hashlib.sha256(vals.tobytes()).hexdigest()
    assert digest == "6361a09388cfa3f369f0fae116477c05c376c92e45a46ad918d1242d4589f377"
    return vals


def transvection_perm(pts, v):
    index = {x:i for i,x in enumerate(pts)}
    p=[]
    for x in pts:
        a = symp(x,v)
        y = tuple((x[i] + a*v[i]) % 3 for i in range(4))
        p.append(index[norm_projective(y)])
    return tuple(p)


def compose(p,q):
    return tuple(p[q[i]] for i in range(len(p)))


def generate_group(gens):
    ident=tuple(range(len(gens[0])))
    seen={ident}
    queue=[ident]
    while queue:
        x=queue.pop()
        for g in gens:
            y=compose(g,x)
            if y not in seen:
                seen.add(y); queue.append(y)
    return sorted(seen)


def pair_orbits(group):
    unseen={(i,j) for i in range(40) for j in range(40)}
    sizes=[]
    while unseen:
        seed=next(iter(unseen))
        orb={(g[seed[0]],g[seed[1]]) for g in group}
        sizes.append(len(orb))
        unseen.difference_update(orb)
    return sorted(sizes)


def mod_rank(M, p):
    X=np.asarray(M, dtype=np.int64) % p
    m,n=X.shape
    r=0
    for c in range(n):
        piv=next((i for i in range(r,m) if X[i,c] % p), None)
        if piv is None:
            continue
        if piv != r:
            X[[r,piv]]=X[[piv,r]]
        X[r]=(X[r]*pow(int(X[r,c]),-1,p))%p
        rows=np.where(X[:,c] != 0)[0]
        for i in rows:
            if i != r:
                X[i]=(X[i]-X[i,c]*X[r])%p
        r += 1
        if r == m:
            break
    return r


def commutant_matrix(A):
    controlled=set(PORTS)
    free=[i for i in range(40) if i not in controlled]
    basis=[]
    for i in PORTS:
        X=np.zeros((40,40),dtype=np.int64); X[i,i]=1; basis.append(X)
    for i in free:
        for j in free:
            X=np.zeros((40,40),dtype=np.int64); X[i,j]=1; basis.append(X)
    assert len(basis)==280
    cols=np.stack([(X@A-A@X).reshape(-1) for X in basis],axis=1)
    cols=cols[np.any(cols,axis=1)]
    assert cols.shape[0] == 1196
    return cols


def quick_verify(frozen):
    assert canonical_json_sha(frozen) == SEMANTIC == frozen["semantic_sha256"]
    pts,A=build_w33()
    verify_srg(A)
    cand=candidates(A)
    _,single,pair=fingerprint_primitives(A,cand)
    w2=weight2_ledger(single,pair)
    assert len(w2)==303810
    gens=[transvection_perm(pts,v) for v in GEN_VECTORS]
    G=generate_group(gens)
    assert len(G)==25920
    assert pair_orbits(G)==[40,480,1080]
    C=commutant_matrix(A)
    assert {p:mod_rank(C,p) for p in (5,7,101)} == {5:279,7:279,101:279}
    B=np.ones((40,40),dtype=np.int64)-np.eye(40,dtype=np.int64)-A
    assert np.array_equal(4*B, A@A-2*A-12*np.eye(40,dtype=np.int64))
    p4=math.sqrt(1-(1-0.999)**0.25)
    p2=math.sqrt(1-math.sqrt(1-0.999))
    assert abs(p4-0.906737039607464)<1e-14
    assert abs(p2-0.9840615953274044)<1e-14
    assert abs(4*math.pi**2/math.log(2)-56.95531729995002)<1e-12
    return {"group_order":len(G),"pair_orbits":[40,480,1080],
            "weight2":len(w2),"port_ranks":{str(p):mod_rank(C,p) for p in (5,7,101)}}


def fill_weight3_memmap(singles, pair, path):
    n=len(singles)
    count=n*(n-1)*(n-2)//6
    vals=np.memmap(path, mode="w+", dtype=np.uint64, shape=(count,))
    off=0
    for i in range(n-2):
        for j in range(i+1,n-1):
            ks=slice(j+1,n)
            block=singles[i]+singles[j]+singles[ks]+pair[i,j]+pair[i,ks]+pair[j,ks]
            vals[off:off+len(block)]=block
            off += len(block)
    assert off==count
    vals.flush()
    return vals


def sha_array_stream(a, chunk=4_000_000):
    h=hashlib.sha256()
    for i in range(0,len(a),chunk):
        h.update(np.asarray(a[i:i+chunk]).tobytes())
    return h.hexdigest()


def alternating_weight4(A,cand):
    lookup={(u,v):(u,v,s) for u,v,s in cand}
    count=zeros=0
    for quad in itertools.combinations(range(40),4):
        a,b,c,d=quad
        cycles=((a,b,c,d),(a,b,d,c),(a,c,b,d))
        for cyc in cycles:
            edges=[]
            signs=[]
            for i in range(4):
                u,v=sorted((cyc[i],cyc[(i+1)%4]))
                t=lookup[(u,v)]
                edges.append(t); signs.append(t[2])
            if all(signs[i] == -signs[(i+1)%4] for i in range(4)):
                count += 1
                if not np.any(residual(A,edges)):
                    zeros += 1
    return count,zeros


def alternating_simple_weight6(A):
    dels=[(u,v,-1) for u in range(40) for v in range(u+1,40) if A[u,v]]
    count=zeros=0
    for e1,e2,e3 in itertools.combinations(dels,3):
        verts={e1[0],e1[1],e2[0],e2[1],e3[0],e3[1]}
        if len(verts)!=6:
            continue
        base=[e1,e2,e3]
        for bits in ((0,0,0),(0,0,1),(0,1,0),(0,1,1)):
            oriented=[]
            for e,b in zip(base,bits):
                oriented.append((e[b],e[1-b]))
            ins=[]
            ok=True
            for q in range(3):
                u=oriented[q][1]; v=oriented[(q+1)%3][0]
                if A[u,v]:
                    ok=False; break
                u,v=sorted((u,v)); ins.append((u,v,1))
            if not ok or len({(u,v) for u,v,_ in ins})<3:
                continue
            count += 1
            toggles=base+ins
            if not np.any(residual(A,toggles)):
                zeros += 1
    return count,zeros


def heavy_verify(frozen, workdir=None):
    pts,A=build_w33(); cand=candidates(A)
    _,single,pair=fingerprint_primitives(A,cand)
    w2=weight2_ledger(single,pair)
    with tempfile.TemporaryDirectory(dir=workdir) as td:
        p=Path(td)/"weight3.u64"
        w3=fill_weight3_memmap(single,pair,p)
        w3.sort(); w3.flush()
        assert not np.any(w3[1:]==w3[:-1])
        assert sha_array_stream(w3) == \
            "5c642f198f4d4a79f3789af8a2cc8d614d162342623f5d822dad65ba762deed5"
        small=np.concatenate([np.array([0],dtype=np.uint64),single,w2])
        small=np.unique(small)
        positions=np.searchsorted(w3,small)
        for value,pos in zip(small,positions):
            if pos < len(w3):
                assert w3[pos] != value
        del w3
    c4,z4=alternating_weight4(A,cand)
    c6,z6=alternating_simple_weight6(A)
    assert (c4,z4)==(27000,0)
    assert (c6,z6)==(2769952,0)
    P=np.eye(40,dtype=np.int64)
    P[[0,4]]=P[[4,0]]
    B=P@A@P.T
    toggled=np.argwhere(np.triu(A!=B,1))
    assert len(toggled)==32
    I=np.eye(40,dtype=np.int64); J=np.ones((40,40),dtype=np.int64)
    assert np.array_equal(B@B+2*B-8*I-4*J,np.zeros((40,40),dtype=np.int64))
    return {"weight3":78788060,"weight4":c4,"weight6":c6,"upper_witness":32}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--json", type=Path)
    ap.add_argument("--heavy", action="store_true")
    ap.add_argument("--workdir", type=Path)
    args=ap.parse_args()
    frozen=json.loads(FROZEN.read_text())
    quick=quick_verify(frozen)
    if args.heavy:
        quick["heavy"]=heavy_verify(frozen,args.workdir)
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps(frozen,sort_keys=True,separators=(",",":"))+"\n")
    print("PASS_8_FRONTS", frozen["semantic_sha256"])
    print(json.dumps(quick,sort_keys=True))


if __name__=="__main__":
    main()
