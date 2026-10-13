"""Exact topology gate for a native dual-tetrahedron nonlinear Regge attempt.

Not a no-go for all native gravity. A four-edge-coloured Levi graph glued as
80 tetrahedra cannot be a closed3-manifold, regardless of its colouring.
"""
from pathlib import Path
import json
import sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass11969_full_native_gauss_compiler import NativeGaussCompiler


def components(edges,vertices):
    adj={v:[] for v in vertices}
    for a,b in edges:adj[a].append(b);adj[b].append(a)
    remaining=set(vertices);out=[]
    while remaining:
        start=min(remaining);part={start};queue=[start]
        for u in queue:
            for v in adj[u]:
                if v not in part:part.add(v);queue.append(v)
        remaining-=part;out.append(sorted(part))
    return out


def colouring(seed):
    c=NativeGaussCompiler();edges=c.edges;remaining=set(range(160));cols={};rng=np.random.default_rng(seed)
    left=[v for v in range(80) if c.color[v]==0]
    for color in range(4):
        adj={v:[] for v in left}
        for e in sorted(remaining):
            a,b=edges[e];a,b=(a,b) if a in adj else (b,a);adj[a].append((b,e))
        for v in left:rng.shuffle(adj[v])
        mate={}
        def augment(u,seen):
            for v,e in adj[u]:
                if v in seen:continue
                seen.add(v)
                if v not in mate or augment(mate[v][0],seen):mate[v]=(u,e);return True
            return False
        order=list(left);rng.shuffle(order)
        assert all(augment(u,set()) for u in order)
        for u,e in mate.values():cols[e]=color;remaining.remove(e)
    assert not remaining
    return edges,cols


def census(seed):
    edges,cols=colouring(seed)
    pairs={}
    for i in range(4):
        for j in range(i+1,4):
            parts=components([e for k,e in enumerate(edges) if cols[k] in (i,j)],range(80))
            assert all(len(p)>=8 for p in parts)
            pairs[(i,j)]=parts
    links=[]
    for omit in range(4):
        colors=[i for i in range(4) if i!=omit]
        bubbles=components([e for k,e in enumerate(edges) if cols[k]!=omit],range(80))
        for part in bubbles:
            ps=set(part);f=len(part);e=3*f//2
            v=sum(sum(set(p)<=ps for p in pairs[(i,j)]) for i in colors for j in colors if i<j)
            chi=v-e+f;assert chi%2==0 and chi<=2
            links.append(dict(omitted_color=omit,tetrahedra=f,link_f_vector=[v,e,f],Euler=chi,genus=1-chi//2))
    V=len(links);E=sum(len(p) for p in pairs.values());chi=V-E+80
    assert chi==sum(x['genus'] for x in links)>=24
    return dict(seed=seed,edge_colours=[cols[i] for i in range(160)],
                primal_f_vector=[V,E,160,80],Euler=chi,total_vertex_link_genus=sum(x['genus'] for x in links),links=links,
                bicolour_cycle_counts={str(p):len(z) for p,z in pairs.items()})


def payload():
    rows=[census(seed) for seed in (11972,71921)]
    return dict(status='PASS',attempt='Use proper4-edge-colouring of native4-regular bipartite80-vertex Levi graph as face-pairing dual of80 labelled tetrahedra; assign edge lengths and a nonlinear Regge action.',
        exact_colour_independent_obstruction='Each two-colour component is a cycle of length>=8 by native girth. At most10 components per colour pair, so primalE<=60. There are at least4 three-colour bubbles, hence primalV>=4. WithF=160,T=80, chi=V-E+80>=24, whereas every closed3-manifold has chi=0.',
        stronger_link_identity='The link of each primal vertex is an orientable surface encoded by its connected3-colour bubble. Bipartiteness gives orientability. Sum_link chi_link=2E-160, so sum_link genus=V-E+80=chi>=24. Some links must have positive genus for EVERY proper colouring.',
        witnesses=rows,
        consequence='The attempted native Regge spatial slice has conical singularities with nonspherical vertex links. An ordinary smooth3+1D ADM/Regge interpretation fails before constraint closure. Resolving links by handlebodies introduces topology and boundary data that the graph alone has not selected.',
        scope='Only this specified coloured dual-tetrahedron construction. Does not exclude other cell complexes, graph-cover continuum routes, singular gravity, refined resolutions, or nonlinearGR. No dynamical metric or constraint algebra constructed.',
        prior=['11968 native linear spin2 derivative and projection','11323 native nonlinear rotational/lapse constraints','K12 singular-link audits: a different2D object, not this80-tetrahedron construction'],
        primary='https://www.combinatorics.org/ojs/index.php/eljc/article/download/v21i1p61/pdf/')


if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11972_native_tetrahedron_link_audit.json').write_text(json.dumps(d,indent=2)+'\n')
    print('PASS',[(r['primal_f_vector'],r['total_vertex_link_genus']) for r in d['witnesses']])
