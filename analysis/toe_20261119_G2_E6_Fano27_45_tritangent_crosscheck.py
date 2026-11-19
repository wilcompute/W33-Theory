#!/usr/bin/env python3
"""Cross-verify Grigorian's Nov 2026 G2/E6 cubic normalizations and
the classical 27-lines/45-tritangents cubic-surface incidence.

Neither the external exceptional-stabilizer theorem nor the recent
1,335,373 E6 matroid census is re-proved here. They are cited literature.
"""
from itertools import combinations
from collections import Counter
from pathlib import Path
import json
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261119_G2_E6_Fano_cubic27_45_tritangents_crosscheck.json"

def fano_g2_cubics():
    # Standard G2 three-form phi = e123+e145+e167+e246-e257-e347-e356.
    lines=[(0,1,2,1),(0,3,4,1),(0,5,6,1),(1,3,5,1),
           (1,4,6,-1),(2,3,6,-1),(2,4,5,-1)]
    phi=np.zeros((7,7,7),dtype=float)
    for a,b,c,sgn in lines:
        phi[a,b,c]=sgn;phi[b,c,a]=sgn;phi[c,a,b]=sgn
        phi[a,c,b]=-sgn;phi[c,b,a]=-sgn;phi[b,a,c]=-sgn
    assert np.count_nonzero(phi)==42
    rng=np.random.default_rng(261119)
    max_C0=0.;max_Cphi=0.
    vals=[]
    for idx in range(32):
        u=np.eye(7)[idx] if idx<7 else rng.normal(size=7)
        u=u/np.linalg.norm(u)
        h=7*np.outer(u,u)-np.eye(7)
        assert np.linalg.norm(h-h.T)<1e-13
        c0=float(np.trace(h@h@h))
        cp=float(np.einsum("abc,def,ad,be,cf->",phi,phi,h,h,h,optimize=True))
        vals.append((c0,cp))
        max_C0=max(max_C0,abs(c0-210))
        max_Cphi=max(max_Cphi,abs(cp-84))
    assert max_C0<1e-10 and max_Cphi<1e-10,(max_C0,max_Cphi)
    lam=sp.symbols("lam")
    discriminant=8*lam**2-2*lam+1
    roots=sp.solve(discriminant,lam)
    assert sorted(roots,key=lambda z:sp.im(z).evalf())==[
        (1-sp.I*sp.sqrt(7))/8,(1+sp.I*sp.sqrt(7))/8]
    normvals=[sp.simplify(210+84*r) for r in roots]
    for r,val in zip(roots,normvals):
        assert sp.simplify(val-42*(5+2*r))==0
    return {"phi_nonzero_signed_entries":42,
      "Fano_oriented_support_triples":7,
      "random_unit_line_basepoints":32,
      "max_trace_cubic_error_from_210":max_C0,
      "max_phi_cubic_error_from_84":max_Cphi,
      "critical_lambda_quadratic":"8*lambda^2-2*lambda+1",
      "critical_lambda":[str(r) for r in roots],
      "E_line_cubic_at_critical_lambdas":[str(v) for v in normvals],
      "external_theorem":"Sergey Grigorian arXiv:2611.21589 proves stabilizer jump G2(dim14) -> E6(dim78) and Albert norm equivalence at these roots.",
      "scope":"We checked only cubic contractions and critical quadratic arithmetic, NOT 78-dimensional Lie stabilizers, full Jordan identity, global bundle existence or 11D physics."}

def all_matchings(items):
    if not items:
        yield ()
        return
    first=items[0]
    for j in range(1,len(items)):
        pair=(first,items[j])
        for rest in all_matchings(items[1:j]+items[j+1:]):
            yield (pair,)+rest

def tritangent_incidence():
    ids=list(range(6))
    E=[("E",i) for i in ids]
    Q=[("Q",i) for i in ids]
    L=[("L",i,j) for i,j in combinations(ids,2)]
    vertices=E+Q+L
    assert len(vertices)==27
    trits=[]
    for i in ids:
        for j in ids:
            if i==j:continue
            trits.append(frozenset((("E",i),("Q",j),("L",min(i,j),max(i,j)))))
    matching=list(all_matchings(ids))
    assert len(matching)==15
    for m in matching:
        trits.append(frozenset(("L",i,j) for i,j in m))
    assert len(trits)==45 and len(set(trits))==45
    assert all(len(t)==3 for t in trits)
    deg=Counter(v for t in trits for v in t)
    assert len(deg)==27 and set(deg.values())=={5}
    index={v:i for i,v in enumerate(vertices)}
    A=np.zeros((27,27),dtype=int)
    pair_counts=Counter()
    for t in trits:
        for a,b in combinations(sorted(t),2):
            i,j=sorted([index[a],index[b]])
            pair_counts[(i,j)]+=1
            A[i,j]=A[j,i]=1
    assert len(pair_counts)==135 and set(pair_counts.values())=={1}
    assert set(A.sum(axis=0))=={10}
    J=np.ones((27,27),dtype=int)
    assert np.array_equal(A@A,10*np.eye(27,dtype=int)+A+5*(J-np.eye(27,dtype=int)-A))
    eigen=np.linalg.eigvalsh(A)
    assert np.max(abs(eigen-np.array([-5]*6+[1]*20+[10])))<1e-10
    return {"lines":27,"exceptional_lines":6,"conic_lines":6,
      "pair_lines":15,"tritangent_planes":45,
      "mixed_E_L_Q_tritangents":30,"three_pair_L_tritangents":15,
      "tritangents_incident_to_each_line":5,
      "intersecting_lines_per_line":10,"unique_pair_incidence":135,
      "intersection_graph_strongly_regular_parameters":[27,10,1,5],
      "intersection_graph_eigenvalues":{"-5":6,"1":20,"10":1},
      "Schlafli_skew_graph_degree":16,
      "external_new_work":"D. Corey arXiv:2611.19606 classifies E6 minuscule Coxeter matroids as 1,335,373 matroids in 230 Weyl orbits; NOT reproduced here.",
      "scope":"Classical cubic surface incidence reconstructed independently, but does not imply that physical E6 matter or a G2 compactification follows."}

def run():
    result={"research_date":"2026-11-19",
        "G2_27_cubic_pencil":fano_g2_cubics(),
        "E6_cubic_surface_lines":tritangent_incidence(),
        "literature":[
          "https://arxiv.org/html/2611.21589",
          "https://arxiv.org/abs/2611.19606"]}
    OUT.parent.mkdir(exist_ok=True,parents=True)
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    print(json.dumps(result,indent=2))
    return result

if __name__=="__main__":run()
