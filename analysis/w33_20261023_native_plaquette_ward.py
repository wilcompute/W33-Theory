#!/usr/bin/env python3
"""W33 round 10: native voltage-cover contractible plaquettes & Ward identity.

Enumerate real triangles in the 27-site 135-edge voltage graph. Only cycles
with zero total integer voltage close in the infinite Z^4 lift and support
a strictly local, gauge-invariant magnetic loop at arbitrary Bloch momentum.
"""
import itertools,json,sys
from pathlib import Path
import numpy as np
try:
 from analysis.w33_pass12189_12193_five_bridges import graph_inputs
except ImportError:
 from w33_pass12189_12193_five_bridges import graph_inputs


def build():
    data,B,V,G,aa,bb=graph_inputs()
    V=np.rint(V).astype(np.int64)
    assert np.max(abs(V-data["primitive_integer_edge_voltages"]))==0
    n=27;m=len(aa);edges={}
    neighbors=[set() for _ in range(n)]
    for e,(a,b) in enumerate(zip(aa,bb)):
        a=int(a);b=int(b);edges[(a,b)]=e
        neighbors[a].add(b);neighbors[b].add(a)
    def walk(a,b):
        if a<b:return int(edges[(a,b)]),1
        return int(edges[(b,a)]),-1
    triangles=[];closed=[]
    for a,b,c in itertools.combinations(range(n),3):
        if b not in neighbors[a] or c not in neighbors[b] or a not in neighbors[c]:continue
        e1,s1=walk(a,b);e2,s2=walk(b,c);e3,s3=walk(c,a)
        flux=s1*V[e1]+s2*V[e2]+s3*V[e3]
        record=(a,b,c,(e1,e2,e3),(s1,s2,s3),tuple(map(int,flux)))
        triangles.append(record)
        if not np.any(flux):closed.append(record)
    # The 45 native triangles partition all 135 edges exactly once.
    counts=np.bincount([e for _,_,_,E,S,F in closed for e in E],minlength=m)
    assert len(closed)==45 and np.all(counts==1)
    vertex_counts=np.bincount([v for a,b,c,*_ in closed for v in (a,b,c)],minlength=n)
    assert np.all(vertex_counts==5)
    # Check the defining GQ(2,4) incidence axiom, not just the counts.
    graphA=np.zeros((n,n),dtype=np.int8)
    for a,b in zip(aa,bb):graphA[a,b]=graphA[b,a]=1
    assert np.all(graphA.sum(axis=1)==10)
    common=graphA.astype(np.int64)@graphA.astype(np.int64)
    assert np.array_equal(common,10*np.eye(n,dtype=np.int64)+graphA+5*(1-np.eye(n,dtype=np.int64)-graphA))
    for a,b,c,*_ in closed:
        for p in range(n):
            if p not in (a,b,c):assert graphA[p,a]+graphA[p,b]+graphA[p,c]==1
    # Hence the 45 triples satisfy the exact GQ(2,4) axiom.
    # Their cellular boundary rows are independent and rank 45.
    # For the 27-vertex/135-edge/45-face finite 2-complex:
    # b0=1, b2=0, b1=135-27+1-45=64, chi=-63.
    rng=np.random.default_rng(10232026)
    checks=[]
    for k in ([0,0,0,0],[.1,.2,-.3,.05],[.3,-.4,.15,.35]):
        k=np.array(k)
        z=np.exp(1j*V@k)
        D=np.zeros((m,n),complex)
        D[np.arange(m),aa]=-1
        D[np.arange(m),bb]=z
        singular=np.linalg.svd(D,compute_uv=False)
        rank=int(np.sum(singular>1e-8))
        # Each contractible plaquette contributes a Bloch curl row.
        curl=np.zeros((len(closed),m),complex)
        for r,(a,b,c,E,S,F) in enumerate(closed):
            prefix=1+0j
            for eid,sgn in zip(E,S):
                if sgn==1:
                    curl[r,eid]+=prefix
                    prefix*=z[eid]
                else:
                    curl[r,eid]+=-prefix/z[eid]
                    prefix/=z[eid]
            assert np.isclose(prefix,1,atol=1e-10)
        ward=float(np.max(np.abs(curl@D))) if len(closed) else 0.
        assert ward<1e-10
        curlrank=int(np.linalg.matrix_rank(curl,tol=1e-8)) if len(closed) else 0
        # curl^* curl acts on 135 *native links*, annihilating all gradients.
        tests=rng.normal(size=n)+1j*rng.normal(size=n)
        A=rng.normal(size=m)+1j*rng.normal(size=m)
        assert np.allclose(curl@(A+D@tests),curl@A,atol=1e-10)
        checks.append({"k":k.tolist(),"rank_grad":rank,
                       "rank_contractible_triangle_curl":curlrank,
                       "gauge_ward_max":ward,
                       "gradient_nullity_in_linkspace":m-rank})
    assert checks[0]["rank_grad"]==26
    assert all(x["rank_grad"]==27 for x in checks[1:])
    return {"status":"NATIVE_ZERO_VOLTAGE_PLAQUETTE_WARD_CENSUS",
            "vertices":n,"edges":m,"rank_periods":4,
            "total_base_triangles":len(triangles),
            "contractible_zero_voltage_triangles":len(closed),
            "nontrivial_voltage_triangles":len(triangles)-len(closed),
            "all_edges_in_exactly_one_triangle":True,
            "incidence_structure":"GQ(2,4), verified by point-outside-line axiom",
            "collinearity_srg_parameters":[27,10,1,5],
            "graph_spectrum_expected":"10 multiplicity1, 1 multiplicity20, -5 multiplicity6",
            "triangles_per_vertex":5,
            "finite_2_complex_betti":[1,64,0],
            "finite_2_complex_Euler_characteristic":-63,
            "generic_Bloch_first_homology_rank":63,
            "finite_cell_first_homology_rank":64,
            "four_voltage_periods_not_four_gauge_polarizations":True,
            "closed_cycles":[{"vertices":[int(a),int(b),int(c)],
                "edge_ids":list(E),"orientation_signs":list(S)}
                for a,b,c,E,S,F in closed],
            "controls":checks,
            "key_boundary":"Native 3-edge loops with nonzero period are NOT plaquettes of the infinite voltage lift. Zero-holonomy loops support exact gauge-invariant curl rows, but their span may be smaller than the full physical link-space complement and no Lorentzian dynamics are inferred."}

if __name__=="__main__":
 raw=json.dumps(build(),indent=2)+"\n"
 if len(sys.argv)>1:Path(sys.argv[1]).write_text(raw,encoding="utf-8")
 else:print(raw)
