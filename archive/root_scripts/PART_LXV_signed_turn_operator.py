#!/usr/bin/env python3
"""PART LXV — Signed non-backtracking turn operator on the 480 carrier.

Builds W(3,3) from PG(3,3), constructs the 480 directed isotropic edges,
splits non-backtracking turns into triangle turns T and open turns O, and
studies C = T - O = 2T - B.
"""
from itertools import combinations, product
from pathlib import Path
import json
import numpy as np

q=3

def norm(v):
    v=tuple(x%q for x in v)
    if not any(v): return None
    for x in v:
        if x:
            inv=1 if x==1 else 2
            return tuple((inv*y)%q for y in v)

def add(u,v): return tuple((a+b)%q for a,b in zip(u,v))
def sc(c,u): return tuple((c*a)%q for a in u)
def om(u,v): return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%q

def points(): return sorted({norm(v) for v in product(range(q), repeat=4) if any(v)})

def pline(p,r):
    L=set()
    for a,b in product(range(q), repeat=2):
        if a or b: L.add(norm(add(sc(a,p),sc(b,r))))
    L.discard(None); return frozenset(L)

def all_lines(P):
    L=set()
    for p,r in combinations(P,2):
        line=pline(p,r)
        if len(line)==q+1: L.add(line)
    return sorted(L,key=lambda x:sorted(x))

def is_iso(L):
    a,b=sorted(L)[:2]
    return om(a,b)==0

def pair(i,j): return (i,j) if i<j else (j,i)

def cluster_eigs(vals,ndigits=6):
    clusters={}
    for z in vals:
        re=round(float(np.real(z)),ndigits); im=round(float(np.imag(z)),ndigits)
        if abs(re)<10**(-ndigits): re=0.0
        if abs(im)<10**(-ndigits): im=0.0
        key=f"{re:+.{ndigits}f}{im:+.{ndigits}f}i"
        clusters[key]=clusters.get(key,0)+1
    return dict(sorted(clusters.items()))

def eval_poly_residual(M, coeffs):
    A=M.astype(np.int64); I=np.eye(A.shape[0],dtype=np.int64); P=coeffs[0]*I
    for a in coeffs[1:]: P=P@A+a*I
    return int(np.max(np.abs(P)))

def main():
    P=points(); idx={p:i for i,p in enumerate(P)}
    Li=[x for x in all_lines(P) if is_iso(x)]
    edges=set()
    for line in Li:
        ids=[idx[p] for p in line]
        for i,j in combinations(ids,2): edges.add(pair(i,j))
    D=[]
    for i,j in sorted(edges): D.append((i,j)); D.append((j,i))
    didx={e:n for n,e in enumerate(D)}
    nbr=[set() for _ in P]
    for i,j in edges: nbr[i].add(j); nbr[j].add(i)
    def is_adj(i,j): return pair(i,j) in edges
    n=len(D); B=np.zeros((n,n),dtype=np.int8); T=np.zeros((n,n),dtype=np.int8)
    for e_idx,(a,b) in enumerate(D):
        for c in nbr[b]:
            if c==a: continue
            f_idx=didx[(b,c)]; B[e_idx,f_idx]=1
            if is_adj(a,c): T[e_idx,f_idx]=1
    O=B-T; C=T-O
    poly_coeffs=[1,1,-35,57,-102,-1174,474,11266,37637,32725,-37975,-42875]
    expected={
        "-7.000000+0.000000i":1,
        "-2.189656+0.000000i":24,
        "-1.828427+0.000000i":15,
        "-1.000000-2.000000i":81,
        "-1.000000+0.000000i":80,
        "-1.000000+2.000000i":81,
        "+1.000000+0.000000i":120,
        "+1.594828-3.666166i":24,
        "+1.594828+3.666166i":24,
        "+3.828427+0.000000i":15,
        "+5.000000+0.000000i":15
    }
    clusters=cluster_eigs(np.linalg.eigvals(C.astype(float)))
    results={
        "q":q,
        "directed_edge_carrier_size":n,
        "undirected_edges":len(edges),
        "hashimoto_row_sum":sorted(set(map(int,B.sum(axis=1)))),
        "triangle_turn_row_sum":sorted(set(map(int,T.sum(axis=1)))),
        "open_turn_row_sum":sorted(set(map(int,O.sum(axis=1)))),
        "signed_turn_row_sum":sorted(set(map(int,C.sum(axis=1)))),
        "operator_definitions":{"B":"Hashimoto non-backtracking operator","T":"triangle-turn part","O":"open-turn part","C":"signed turn C=T-O=2T-B"},
        "signed_turn_spectrum_clustered":clusters,
        "expected_spectrum_clustered":expected,
        "spectrum_matches_expected":clusters==expected,
        "minimal_support_polynomial":"(x+7)(x-5)(x^2-2x-7)(x^3-x^2+9x+35)(x^2+2x+5)(x+1)(x-1)",
        "minimal_support_polynomial_coefficients":poly_coeffs,
        "polynomial_residual_max_abs":eval_poly_residual(C,poly_coeffs),
        "characteristic_factorization_with_multiplicities":"(x+7)^1 (x-5)^15 (x^2-2x-7)^15 (x^3-x^2+9x+35)^24 (x^2+2x+5)^81 (x+1)^80 (x-1)^120",
        "dimension_check":"1 + 15 + 2*15 + 3*24 + 2*81 + 80 + 120 = 480",
        "new_81_observation":"C has eigenvalues -1±2i, each with multiplicity 81. Their Gaussian norm is 5=q+lambda.",
        "interpretation":"The 81=27+27+27 generation carrier appears naturally on the 480 directed-edge Hashimoto space after signing triangle turns against open turns."
    }
    assert results["directed_edge_carrier_size"]==480
    assert results["undirected_edges"]==240
    assert results["hashimoto_row_sum"]==[11]
    assert results["triangle_turn_row_sum"]==[2]
    assert results["open_turn_row_sum"]==[9]
    assert results["signed_turn_row_sum"]==[-7]
    assert results["spectrum_matches_expected"]
    assert results["polynomial_residual_max_abs"]==0
    Path("PART_LXV_signed_turn_operator_results.json").write_text(json.dumps(results,indent=2))
    print(json.dumps(results,indent=2))

if __name__=="__main__": main()
