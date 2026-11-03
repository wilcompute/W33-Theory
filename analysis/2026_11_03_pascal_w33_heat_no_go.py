#!/usr/bin/env python3
"""Exact W33 heat-spectrum scale obstruction and a Lucas/Pascal refinement control.

An exact graph theorem, not a physical TOE or a 4D continuum construction.
Uses standard-library arithmetic and independent finite-geometry enumeration.
"""
from __future__ import annotations
from collections import deque
from itertools import product
from math import comb, exp, log
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "2026_11_03_pascal_w33_heat_no_go.json"

def canonical(v, p):
    a = next(x for x in v if x)
    inv = pow(a, -1, p)
    return tuple((x * inv) % p for x in v)

def pairing(a, b, p):
    return (a[0]*b[2]-a[2]*b[0]+a[1]*b[3]-a[3]*b[1]) % p

def w33_certificate():
    p=3
    points=sorted({canonical(v,p) for v in product(range(p),repeat=4) if any(v)})
    assert len(points)==40
    A=[[int(i!=j and pairing(u,v,p)==0) for j,v in enumerate(points)]
       for i,u in enumerate(points)]
    k=12
    assert all(sum(row)==k for row in A)
    # Strong regularity is checked directly, not assumed from the spectrum.
    count_types={"diagonal":0,"adjacent":0,"nonadjacent":0}
    for i in range(40):
        for j in range(40):
            mutual=sum(A[i][h]*A[h][j] for h in range(40))
            kind="diagonal" if i==j else "adjacent" if A[i][j] else "nonadjacent"
            expected={"diagonal":12,"adjacent":2,"nonadjacent":4}[kind]
            assert mutual==expected, (i,j,mutual,kind)
            count_types[kind]+=1
    # From A^2=8I-2A+4J follows (A-2I)(A+4I)=0
    # on the constants-orthogonal subspace.  Trace A=0 fixes multiplicities.
    assert 12+24*2+15*(-4)==0
    assert 1+24+15==40
    return dict(vertices=40,edges=240,degree=12,
                srg=[40,12,2,4],adjacency_eigenvalues={"12":1,"2":24,"-4":15},
                laplacian_eigenvalues={"0":1,"10":24,"16":15},
                checked_pair_types=count_types)

def spectral_dimension(t):
    x=exp(-10*t);y=exp(-16*t)
    return 480*t*(x+y)/(1+24*x+15*y)

def maximum_dimension():
    # Derivative of ds; scalar root finding, not a global certificate.
    def dprime(t):
        x=exp(-10*t);y=exp(-16*t)
        k=1+24*x+15*y
        s=240*(x+y)
        sp=-2400*x-3840*y
        kp=-240*x-240*y
        return 2*((s+t*sp)*k-t*s*kp)/(k*k)
    lo,hi=.2,.35
    assert dprime(lo)>0 and dprime(hi)<0
    for _ in range(90):
        mid=(lo+hi)/2
        if dprime(mid)>0:lo=mid
        else:hi=mid
    t=(lo+hi)/2
    return {"t_peak_numeric":t, "dimension_peak_numeric":spectral_dimension(t),
            "numeric_only":True}

def pascal_support(level):
    """Lucas-supported Pascal positions in first 3**level rows."""
    width=3**level
    cells={(n,k) for n in range(width) for k in range(n+1)
           if comb(n,k)%3}
    # Three directions of the triangular lattice, no free edge weights.
    adj={z:set() for z in cells}
    for n,k in cells:
        for nbr in ((n,k+1),(n+1,k),(n+1,k+1)):
            if nbr in cells:
                adj[(n,k)].add(nbr);adj[nbr].add((n,k))
    E=sum(map(len,adj.values()))//2
    def distances(src):
        dst={src:0};q=deque([src])
        while q:
            x=q.popleft()
            for z in adj[x]:
                if z not in dst:
                    dst[z]=dst[x]+1;q.append(z)
        return dst
    from_top=distances((0,0))
    assert len(from_top)==len(cells)
    maxdist=max(from_top.values())
    assert len(cells)==6**level
    assert maxdist==width-1 # farthest point from root in these tested levels
    # Exact all-source diameter for levels up to 3 only; otherwise a lower bound.
    diameter=max(max(distances(z).values()) for z in cells) if level<=3 else None
    if diameter is not None:assert diameter==width-1
    return {"level":level,"row_count":width,"nonzero_pascal_entries":len(cells),
            "undirected_edges":E,"connected":True,
            "distance_from_top_to_farthest":maxdist,
            "all_pairs_diameter_exact":diameter,
            "dimension_ratio":log(len(cells))/log(width)}

def run():
    graph=w33_certificate()
    sampled=[{"time":t,"dimension":spectral_dimension(t)}
             for t in (.05,.1,.15,.2,.25,.3,.4,.5,.7,1.)]
    peak=maximum_dimension()
    assert 3.7<peak["dimension_peak_numeric"]<3.8
    # Exact global bound: ds(t)<4 iff
    # 24(5t-1)e^-10t + 15(8t-1)e^-16t < 1.
    # Independent maxima are at t=3/10 and t=3/16:
    # 12/e^3+15/(2e^3)=39/(2e^3)<1.
    # e^3>39/2 follows from sum_{j=0}^7 3^j/j! > 39/2.
    e3_lower=sum(3**j / __import__("math").factorial(j) for j in range(8))
    assert e3_lower>39/2
    assert 39/(2*exp(3))<1
    pascal=[pascal_support(level) for level in (1,2,3,4)]
    result={
      "status":"PASS_EXACT_COMBINATORICS_AND_ANALYTIC_BOUND",
      "w33":graph,"heat_trace":"1+24 exp(-10t)+15 exp(-16t)",
      "spectral_dimension":"480t(exp(-10t)+exp(-16t))/(1+24exp(-10t)+15exp(-16t))",
      "four_dimensional_global_no_go":{
        "claim":"For the unweighted W33 collinearity graph, d_s(t)<4 for all t>0.",
        "proof":"Each of 24(5t-1)exp(-10t) and 15(8t-1)exp(-16t) is bounded above by 12/e^3 and 15/(2e^3). Their sum is 39/(2e^3)<1; this is equivalent to d_s(t)<4.",
        "all_positive_time":True,
        "exponential_inequality_certified_by_rational_series":True
      },
      "peak":peak,"samples":sampled,
      "family_obstruction":"Every W(3,q) point-collinearity graph has diameter 2 and at most three distinct graph-Laplacian eigenvalues; rescaling alone cannot manufacture the unbounded Laplace spectrum of a smooth compact 4-manifold.",
      "pascal_mod3":{
        "Lucas_theorem":"binomial(n,k) nonzero modulo 3 iff every base-3 digit k_i <= n_i",
        "exact_nonzero_count":"6^m for 0<=n<3^m",
        "box_dimension":"log(6)/log(3)",
        "box_dimension_numeric":log(6)/log(3),
        "triangular_nearest_neighbor_graph_tests":pascal,
        "continuum_warning":"Unbounded graph diameter and nonintegral box dimension are promising properties of a refinement family but neither produces a 4D Lorentzian continuum nor a physical meter."
      },
      "scale_identifiability":"Laplacian heat time t and Pascal dilation factor 3 are dimensionless. Absolute lengths require a physical reference/coupling and a measured mapping; assigning physical size is not a deduction from graph topology.",
      "prior_art_scope":"Lucas congruences, Pascal fractal dimension, W(3,q) SRG spectra, graph heat-trace and dimensional transmutation are established mathematics/physics. The concise global ds<4 inequality is a project-specific derived bound; novelty in literature is not claimed."
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("PASS W33 heat dimension <4; numeric peak",peak)
    print("PASS Lucas 3-adic support",[(x["level"],x["nonzero_pascal_entries"],x["distance_from_top_to_farthest"]) for x in pascal])
    return result

if __name__=="__main__":run()
