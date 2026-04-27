#!/usr/bin/env python3
"""PART LXIV — Pascal line-split theorem verifier.

Verifies that the Gaussian Pascal row Gr(2,4)(F_3) = 130 projective lines
splits under the standard symplectic form into 40 isotropic lines and 90
non-isotropic lines. These tile K_40 into 240 W(3,3) edges and 540 complement
edges. Also verifies the signed Seidel-sector operator S = A_iso - A_non.
"""
from itertools import combinations, product
from pathlib import Path
import json
import numpy as np

q = 3

def norm(v):
    v = tuple(x % q for x in v)
    if not any(v):
        return None
    for x in v:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv*y) % q for y in v)

def add(u,v): return tuple((a+b) % q for a,b in zip(u,v))
def sc(c,u): return tuple((c*a) % q for a in u)
def om(u,v): return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1]) % q

def points():
    return sorted({norm(v) for v in product(range(q), repeat=4) if any(v)})

def pline(p,r):
    L=set()
    for a,b in product(range(q), repeat=2):
        if a or b:
            L.add(norm(add(sc(a,p), sc(b,r))))
    L.discard(None)
    return frozenset(L)

def all_lines(P):
    L=set()
    for p,r in combinations(P,2):
        line=pline(p,r)
        if len(line)==q+1:
            L.add(line)
    return sorted(L, key=lambda x: sorted(x))

def is_iso(L):
    a,b = sorted(L)[:2]
    return om(a,b)==0

def pair(i,j): return (i,j) if i<j else (j,i)

def line_pairs(lines, idx):
    out=set()
    for L in lines:
        ids=[idx[p] for p in L]
        for i,j in combinations(ids,2):
            out.add(pair(i,j))
    return out

def adj(n,pairs):
    A=np.zeros((n,n), dtype=int)
    for i,j in pairs:
        A[i,j]=A[j,i]=1
    return A

def spec(M):
    vals=[int(round(x)) for x in np.linalg.eigvalsh(M.astype(float))]
    d={}
    for x in vals: d[str(x)] = d.get(str(x),0)+1
    return dict(sorted(d.items(), key=lambda kv:int(kv[0])))

def poly_resid(M, roots):
    A=M.astype(object); I=np.eye(M.shape[0], dtype=object); P=I.copy()
    for r in roots:
        P = P @ (A-r*I)
    return max(abs(int(x)) for x in P.reshape(-1))


def build_summary():
    P=points(); idx={p:i for i,p in enumerate(P)}
    L=all_lines(P); Li=[x for x in L if is_iso(x)]; Ln=[x for x in L if not is_iso(x)]
    Ei=line_pairs(Li,idx); En=line_pairs(Ln,idx)
    K={pair(i,j) for i,j in combinations(range(len(P)),2)}
    A=adj(len(P), Ei); N=adj(len(P), En)
    S=A-N
    through=[0]*len(P); ithrough=[0]*len(P); nthrough=[0]*len(P)
    for line in L:
        for p in line: through[idx[p]]+=1
    for line in Li:
        for p in line: ithrough[idx[p]]+=1
    for line in Ln:
        for p in line: nthrough[idx[p]]+=1
    results={
        "q":q,
        "projective_points":len(P),
        "projective_lines_total":len(L),
        "isotropic_lines":len(Li),
        "nonisotropic_lines":len(Ln),
        "total_pairs_K40":len(K),
        "isotropic_pairs_edges":len(Ei),
        "nonisotropic_pairs_complement":len(En),
        "edge_partition_exact":len(Ei)==240,
        "complement_partition_exact":len(En)==540,
        "all_projective_pairs_partition_exact":(Ei|En)==K and not (Ei&En),
        "degree_profile_unique":sorted(set(map(int,A.sum(axis=1)))),
        "opposite_degree_profile_unique":sorted(set(map(int,N.sum(axis=1)))),
        "lines_through_point_unique":sorted(set(through)),
        "isotropic_lines_through_point_unique":sorted(set(ithrough)),
        "nonisotropic_lines_through_point_unique":sorted(set(nthrough)),
        "adjacency_spectrum":spec(A),
        "complement_spectrum":spec(N),
        "seidel_spectrum":spec(S),
        "seidel_formula":"S = A_iso - A_non = 2A + I - J",
        "seidel_minimal_polynomial":"(x + 15)(x - 5)(x + 7)",
        "seidel_polynomial_residual":poly_resid(S,[-15,5,-7]),
        "pascal_grassmann_row":[1,40,130,40,1],
        "line_split_identity":"[4 choose 2]_3 = 130 = 40 isotropic + 90 non-isotropic",
        "pair_split_identity":"C(40,2)=780 = 40*C(4,2) + 90*C(4,2) = 240 + 540",
        "signed_trace_identity":"-15 + 24*5 - 15*7 = 0",
        "new_interpretation":"The Gaussian Pascal Grassmannian line count is polarized by the symplectic form into the W(3,3) graph and its complement."
    }
    assert results["projective_points"]==40
    assert results["projective_lines_total"]==130
    assert results["isotropic_lines"]==40 and results["nonisotropic_lines"]==90
    assert results["isotropic_pairs_edges"]==240 and results["nonisotropic_pairs_complement"]==540
    assert results["all_projective_pairs_partition_exact"]
    assert results["degree_profile_unique"]==[12]
    assert results["opposite_degree_profile_unique"]==[27]
    assert results["lines_through_point_unique"]==[13]
    assert results["isotropic_lines_through_point_unique"]==[4]
    assert results["nonisotropic_lines_through_point_unique"]==[9]
    assert results["adjacency_spectrum"]=={"-4":15,"2":24,"12":1}
    assert results["complement_spectrum"]=={"-3":24,"3":15,"27":1}
    assert results["seidel_spectrum"]=={"-15":1,"-7":15,"5":24}
    assert results["seidel_polynomial_residual"]==0
    return results

def main():
    results = build_summary()
    Path("PART_LXIV_pascal_line_split_results.json").write_text(json.dumps(results, indent=2))
    print("="*78)
    print("PART LXIV — PASCAL LINE-SPLIT THEOREM VERIFIED")
    print("="*78)
    for key in ["projective_points","projective_lines_total","isotropic_lines","nonisotropic_lines","isotropic_pairs_edges","nonisotropic_pairs_complement"]:
        print(f"{key}: {results[key]}")
    print("Adjacency spectrum:", results["adjacency_spectrum"])
    print("Complement spectrum:", results["complement_spectrum"])
    print("Seidel spectrum:", results["seidel_spectrum"])
    print(results["line_split_identity"])
    print(results["pair_split_identity"])
    print(results["signed_trace_identity"])

if __name__ == "__main__":
    main()
