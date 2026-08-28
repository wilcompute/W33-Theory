#!/usr/bin/env python3
"""P^1(F9) pair-orbital no-go for the W33 45-state GQ(4,2) carrier.

The current HJ10/P^1(F9) frontier naturally supplies ten states.  Their 45
unordered pairs have the same cardinality as the W33 GQ(4,2) carrier, so this
script tests the strongest cheap equivariance hypothesis: can the GQ(4,2)
point graph arise as a PGL(2,9)- or PSL(2,9)-invariant orbital fusion on those
45 pairs?

Answer: no.

PGL(2,9) has pair-stabilizer subdegrees 1,16,8,8,8,4.  Exhausting all 31
nonempty undirected orbital fusions produces only the connected nontrivial
SRGs T(10)=SRG(45,16,8,4) and its complement SRG(45,28,15,21).

PSL(2,9) refines the pair action.  After transpose-pairing nonsymmetric
orbitals there are seven undirected atoms; all 127 fusions again contain no
SRG(45,12,3,3) and no SRG(45,32,22,24).  Hence no PGL, PSL, or PGammaL
invariant pair-relation realizes the W33 GQ(4,2) carrier.  (The PGammaL claim
follows because invariance under PGammaL implies invariance under its PGL
subgroup.)
"""
from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_W33_20260828_P1F9_PAIR_ORBITAL_GQ42_NOGO.json"

F3 = range(3)
ELS = [(a,b) for a in F3 for b in F3]
ZERO=(0,0); ONE=(1,0); INF=None


def add(x,y): return ((x[0]+y[0])%3,(x[1]+y[1])%3)
def neg(x): return ((-x[0])%3,(-x[1])%3)
def sub(x,y): return add(x,neg(y))
def mul(x,y):
    # F9=F3[i]/(i^2+1), so i^2=-1=2.
    return ((x[0]*y[0]+2*x[1]*y[1])%3,
            (x[0]*y[1]+x[1]*y[0])%3)
def inv(x):
    assert x != ZERO
    for y in ELS:
        if mul(x,y)==ONE: return y
    raise AssertionError
def div(x,y): return mul(x,inv(y))


def mobius(M,x):
    a,b,c,d=M
    if x is INF:
        return INF if c==ZERO else div(a,c)
    den=add(mul(c,x),d)
    num=add(mul(a,x),b)
    return INF if den==ZERO else div(num,den)


def pgl_perms():
    P=ELS+[INF]; idx={x:i for i,x in enumerate(P)}
    perms={}
    for a,b,c,d in itertools.product(ELS, repeat=4):
        det=sub(mul(a,d),mul(b,c))
        if det==ZERO: continue
        M=(a,b,c,d)
        p=tuple(idx[mobius(M,x)] for x in P)
        perms[p]=M
    assert len(perms)==720
    return P, perms


def pair_action(point_perm,pairs,pidx):
    return tuple(pidx[tuple(sorted((point_perm[a],point_perm[b])))] for a,b in pairs)


def suborbits(group,base=0,n=45):
    stab=[g for g in group if g[base]==base]
    unseen=set(range(n)); out=[]
    while unseen:
        s=min(unseen); O={g[s] for g in stab}
        out.append(tuple(sorted(O))); unseen-=O
    return out,stab


def relation_from_suborbit(O,group,base=0,n=45):
    R=[[0]*n for _ in range(n)]
    for g in group:
        a=g[base]
        for y in O: R[a][g[y]]=1
    return R


def transpose(R): return [list(x) for x in zip(*R)]
def symmetric(R): return R==transpose(R)

def union_relations(rels,mask,n=45):
    R=[[0]*n for _ in range(n)]
    for j,A in enumerate(rels):
        if (mask>>j)&1:
            for a in range(n):
                for b in range(n):
                    R[a][b] |= A[a][b]
    return R


def srg_params(R):
    n=len(R); deg=[sum(r) for r in R]
    if len(set(deg))!=1: return None
    k=deg[0]; la=set(); mu=set()
    for a,b in itertools.combinations(range(n),2):
        c=sum(R[a][z]*R[b][z] for z in range(n))
        (la if R[a][b] else mu).add(c)
    if len(la)==len(mu)==1:
        return (n,k,next(iter(la)),next(iter(mu)))
    return None


def connected(R):
    seen={0}; front=[0]
    while front:
        a=front.pop()
        for b,x in enumerate(R[a]):
            if x and b not in seen: seen.add(b); front.append(b)
    return len(seen)==len(R)


def identify_t10(R,pairs):
    return all(R[i][j] == int(bool(set(pairs[i]) & set(pairs[j])))
               for i in range(45) for j in range(45) if i!=j)


def main():
    P, raw=pgl_perms()
    pairs=list(itertools.combinations(range(10),2)); pidx={p:i for i,p in enumerate(pairs)}
    PGL=[pair_action(g,pairs,pidx) for g in raw]
    assert len(set(PGL))==720

    # PGL(2,9) pair orbitals.
    orbs,stab=suborbits(PGL)
    assert [len(x) for x in orbs]==[1,16,8,8,8,4]
    atoms=[relation_from_suborbit(O,PGL) for O in orbs[1:]]
    assert all(symmetric(A) for A in atoms)
    pgl_srgs=[]
    for mask in range(1,1<<len(atoms)):
        R=union_relations(atoms,mask)
        p=srg_params(R)
        if p: pgl_srgs.append((mask,p,connected(R)))
    assert [(m,p) for m,p,c in pgl_srgs if c] == [
        (1,(45,16,8,4)), (30,(45,28,15,21))]
    assert identify_t10(union_relations(atoms,1),pairs)
    assert not any(p in ((45,12,3,3),(45,32,22,24)) for _,p,_ in pgl_srgs)

    # PSL(2,9) is the square-determinant half of PGL(2,9).
    squares={mul(x,x) for x in ELS if x!=ZERO}
    PSL=[]
    for p,M in raw.items():
        a,b,c,d=M; det=sub(mul(a,d),mul(b,c))
        if det in squares:
            PSL.append(pair_action(p,pairs,pidx))
    assert len(set(PSL))==360
    orbs2,stab2=suborbits(PSL)
    assert [len(x) for x in orbs2]==[1,8,8,8,8,4,2,2,4]
    directed=[relation_from_suborbit(O,PSL) for O in orbs2[1:]]
    partner=[]
    for R in directed:
        T=transpose(R)
        partner.append(next(j for j,S in enumerate(directed) if S==T))
    assert partner==[0,1,2,3,7,5,6,4]
    atoms2=[directed[0],directed[1],directed[2],directed[3],
            [[directed[4][i][j] or directed[7][i][j] for j in range(45)] for i in range(45)],
            directed[5],directed[6]]
    assert all(symmetric(A) for A in atoms2)
    psl_srgs=[]
    for mask in range(1,1<<len(atoms2)):
        R=union_relations(atoms2,mask)
        p=srg_params(R)
        if p: psl_srgs.append((mask,p,connected(R)))
    counts=Counter(p for _,p,_ in psl_srgs)
    assert counts==Counter({(45,2,1,0):2,(45,42,39,42):2,
                           (45,16,8,4):1,(45,28,15,21):1})
    assert not any(p in ((45,12,3,3),(45,32,22,24)) for _,p,_ in psl_srgs)

    out={
      "schema":"w33.20260828.p1f9-pair-orbital-gq42-nogo.v1",
      "status":"PASS",
      "ten_state_model":{"set":"P1(F9)","points":10,"unordered_pairs":45},
      "PGL2_9":{"order":720,"pair_stabilizer_order":16,
        "pair_subdegrees":[1,16,8,8,8,4],"undirected_atoms":5,
        "orbital_fusions_tested":31,
        "connected_nontrivial_srgs":[[45,16,8,4],[45,28,15,21]],
        "degree16_identification":"T(10), pair adjacency iff nonempty intersection"},
      "PSL2_9":{"order":360,"pair_stabilizer_order":8,
        "pair_subdegrees":[1,8,8,8,8,4,2,2,4],"undirected_atoms_after_transpose_closure":7,
        "orbital_fusions_tested":127,
        "srg_census":{"SRG(45,2,1,0)":2,"SRG(45,42,39,42)":2,
                      "SRG(45,16,8,4)":1,"SRG(45,28,15,21)":1}},
      "target":{"W33_45_state_graph":"GQ(4,2) point graph",
        "parameters":[45,12,3,3],"complement_parameters":[45,32,22,24]},
      "theorem":"No PGL(2,9)- or PSL(2,9)-invariant orbital fusion on the 45 unordered pairs of P1(F9) realizes GQ(4,2) or its complement. Consequently no PGammaL(2,9)-invariant pair relation does either.",
      "boundary":"This rules out the natural pair-orbital bridge only. It does not rule out a non-orbital, symmetry-breaking, or differently indexed map between a ten-state carrier and a W33 45-state object."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"PASS","PGL_subdegrees":[1,16,8,8,8,4],
                      "PGL_connected_srgs":[[45,16,8,4],[45,28,15,21]],
                      "GQ42_orbital_bridge":False},sort_keys=True))

if __name__=="__main__": main()
