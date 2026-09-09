#!/usr/bin/env python3
"""Deep Marcelis multichart atlas and two exact bridge firewalls.

Frans Marcelis' site repeatedly relates finite-geometric objects by projections,
quotients and changes of coordinates.  This certificate keeps those coordinate
languages separate while testing two tempting literal identifications:

1. W33 chart web versus the Heawood graph.
   W(3,3) has 540 Q3 charts, one for each skew pair of lines.  Two charts are
   adjacent when their four defining lines form an apartment.  The web is
   6-regular with 1620 edges.  A literal Heawood subgraph would force seven
   vertices in one bipartition class to form a K7 in the chart web's distance-2
   common-neighbour graph.  Exact maximum-clique search gives omega=6, so no
   literal Heawood subgraph exists.  Any Heawood bridge must therefore be a
   projection/quotient/incidence/scheduler construction, not direct inclusion.

2. GF(4) trace versus a projective coordinate map.
   Marcelis uses GF(4)->GF(2) trace in structured coordinate constructions.
   Coordinatewise trace is F2-linear on vectors, but it is NOT a globally
   well-defined map PG(3,4)->PG(3,2): scaling a GF(4) representative by omega
   can change the resulting binary projective point.  The script freezes an
   explicit counterexample.  Trace bridges need a chosen representative or
   extra geometric structure.

The file also reconstructs the small incidence objects that recur across the
site: PG(3,2), the Fano plane/Heawood incidence graph, AG(2,3) (Hesse), and the
W33 540-chart web.
"""

from __future__ import annotations

from itertools import combinations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_marcelis_multichart_atlas.json"


# ---------------------------------------------------------------------------
# Generic prime-field projective geometry helpers

def canon_prime(v, q):
    row = tuple(int(x) % q for x in v)
    for x in row:
        if x:
            inv = pow(x, -1, q)
            return tuple((inv*y) % q for y in row)
    raise ValueError("zero vector")


def rank_mod_p(rows, p):
    a = [[x % p for x in row] for row in rows]
    r = 0
    if not a:
        return 0
    for c in range(len(a[0])):
        pivot = next((i for i in range(r, len(a)) if a[i][c] % p), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = pow(a[r][c] % p, -1, p)
        a[r] = [(x*inv) % p for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c] % p:
                f = a[i][c] % p
                a[i] = [(x-f*y) % p for x,y in zip(a[i],a[r])]
        r += 1
    return r


def projective_points_prime(dim, q):
    return tuple(sorted({
        canon_prime(v,q)
        for v in product(range(q), repeat=dim)
        if any(v)
    }))


def pg32():
    pts = projective_points_prime(4,2)
    idx = {p:i for i,p in enumerate(pts)}
    lines = set()
    for i,j in combinations(range(len(pts)),2):
        span = {
            canon_prime(tuple((a*pts[i][k]+b*pts[j][k])%2 for k in range(4)),2)
            for a,b in product(range(2), repeat=2) if (a,b)!=(0,0)
        }
        if len(span)==3:
            lines.add(tuple(sorted(idx[x] for x in span)))
    return pts, tuple(sorted(lines))


def fano_plane():
    pts = projective_points_prime(3,2)
    idx = {p:i for i,p in enumerate(pts)}
    lines = set()
    for i,j in combinations(range(7),2):
        third = tuple((pts[i][k]+pts[j][k])%2 for k in range(3))
        lines.add(tuple(sorted((i,j,idx[third]))))
    return pts, tuple(sorted(lines))


def heawood_graph():
    _, lines = fano_plane()
    adj = [set() for _ in range(14)]
    for li,line in enumerate(lines):
        L = 7+li
        for p in line:
            adj[p].add(L); adj[L].add(p)
    return tuple(frozenset(x) for x in adj)


def hesse_ag23():
    pts = tuple(product(range(3), repeat=2))
    idx = {p:i for i,p in enumerate(pts)}
    lines = set()
    # affine directions: vertical plus slopes 0,1,2
    for c in range(3):
        lines.add(tuple(sorted(idx[(c,y)] for y in range(3))))
    for m in range(3):
        for b in range(3):
            lines.add(tuple(sorted(idx[(x,(m*x+b)%3)] for x in range(3))))
    return pts, tuple(sorted(lines))


# ---------------------------------------------------------------------------
# W(3,3) and its 540 hypercube chart web

def w33():
    q=3
    pts = projective_points_prime(4,q)
    idx={p:i for i,p in enumerate(pts)}
    def form(x,y):
        return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%3
    lines=set()
    for i,j in combinations(range(40),2):
        if form(pts[i],pts[j])!=0:
            continue
        span={
            canon_prime(tuple((a*pts[i][k]+b*pts[j][k])%3 for k in range(4)),3)
            for a,b in product(range(3),repeat=2) if (a,b)!=(0,0)
        }
        if len(span)==4:
            lines.add(tuple(sorted(idx[x] for x in span)))
    return pts, tuple(sorted(lines))


def chart_web(lines):
    line_sets=[set(L) for L in lines]
    skew=[]
    for i,j in combinations(range(len(lines)),2):
        if line_sets[i].isdisjoint(line_sets[j]):
            skew.append((i,j))
    chart_index={c:i for i,c in enumerate(skew)}
    web=[set() for _ in skew]
    transversal_hist={}

    # For each skew pair, the GQ axiom yields exactly four common transversals.
    for ci,(a,b) in enumerate(skew):
        trans=[
            t for t in range(len(lines))
            if t not in (a,b)
            and not line_sets[t].isdisjoint(line_sets[a])
            and not line_sets[t].isdisjoint(line_sets[b])
        ]
        transversal_hist[len(trans)]=transversal_hist.get(len(trans),0)+1
        # Each unordered pair of the four transversals gives a neighbor chart.
        for u,v in combinations(sorted(trans),2):
            cj=chart_index[tuple(sorted((u,v)))]
            web[ci].add(cj)
            web[cj].add(ci)
    return tuple(skew), tuple(frozenset(x) for x in web), transversal_hist


def edge_count(adj):
    return sum(len(x) for x in adj)//2


def triangle_count(adj):
    n=0
    for i in range(len(adj)):
        for j in adj[i]:
            if j<=i: continue
            n += sum(1 for k in adj[i].intersection(adj[j]) if k>j)
    return n


def distance_two_graph(adj):
    out=[set() for _ in adj]
    for i in range(len(adj)):
        for j in range(i+1,len(adj)):
            if j in adj[i]:
                continue
            if adj[i].intersection(adj[j]):
                out[i].add(j); out[j].add(i)
    return tuple(frozenset(x) for x in out)


def max_clique_exact(adj):
    """Bron-Kerbosch with pivot, returning one exact maximum clique."""
    best=[]
    N=[set(x) for x in adj]

    def expand(R,P,X):
        nonlocal best
        if len(R)+len(P)<=len(best):
            return
        if not P and not X:
            if len(R)>len(best):
                best=sorted(R)
            return
        union=P|X
        pivot=max(union,key=lambda u:len(P & N[u])) if union else None
        candidates=list(P - (N[pivot] if pivot is not None else set()))
        candidates.sort(key=lambda v:len(P & N[v]), reverse=True)
        for v in candidates:
            expand(R|{v}, P & N[v], X & N[v])
            P.remove(v); X.add(v)
            if len(R)+len(P)<=len(best):
                return

    expand(set(),set(range(len(adj))),set())
    return best


# ---------------------------------------------------------------------------
# GF(4) trace firewall, polynomial w^2+w+1=0.
# Encoding: 0=0, 1=1, 2=w, 3=w+1=w^2.
GF4_ADD=[[a^b for b in range(4)] for a in range(4)]
GF4_MUL=[
    [0,0,0,0],
    [0,1,2,3],
    [0,2,3,1],
    [0,3,1,2],
]


def gf4_add(a,b): return GF4_ADD[a][b]
def gf4_mul(a,b): return GF4_MUL[a][b]
def gf4_square(a): return gf4_mul(a,a)
def gf4_trace(a): return gf4_add(a,gf4_square(a))  # in {0,1}


def scale4(v,a): return tuple(gf4_mul(a,x) for x in v)
def trace4(v): return tuple(gf4_trace(x) for x in v)


def find_trace_projective_counterexample():
    for v in product(range(4), repeat=4):
        if not any(v): continue
        for scalar in (2,3):
            w=scale4(v,scalar)
            tv,tw=trace4(v),trace4(w)
            if not any(tv) or not any(tw):
                continue
            # Over F2, nonzero projective equality is literal equality.
            if tv!=tw:
                return {
                    "representative": list(v),
                    "scaled_same_GF4_projective_point": list(w),
                    "scalar": scalar,
                    "trace_representative": list(tv),
                    "trace_scaled": list(tw),
                }
    return None


def main():
    pgpts,pglines=pg32()
    fanopts,fanolines=fano_plane()
    H=heawood_graph()
    hpts,hlines=hesse_ag23()
    wpts,wlines=w33()
    charts,web,trans_hist=chart_web(wlines)
    d2=distance_two_graph(web)
    clique=max_clique_exact(d2)
    counter=find_trace_projective_counterexample()

    checks={
        "PG32_is_15_points_35_lines": len(pgpts)==15 and len(pglines)==35,
        "Fano_is_7_points_7_lines": len(fanopts)==7 and len(fanolines)==7,
        "Heawood_is_14_vertices_21_edges_cubic":
            len(H)==14 and edge_count(H)==21 and {len(x) for x in H}=={3},
        "Hesse_is_9_points_12_lines": len(hpts)==9 and len(hlines)==12,
        "W33_is_40_points_40_lines": len(wpts)==40 and len(wlines)==40,
        "W33_has_540_skew_line_pairs": len(charts)==540,
        "every_chart_has_four_common_transversals": trans_hist=={4:540},
        "chart_web_is_540_6_regular_1620":
            len(web)==540 and {len(x) for x in web}=={6} and edge_count(web)==1620,
        "chart_web_is_triangle_free": triangle_count(web)==0,
        "distance2_graph_is_30_regular": {len(x) for x in d2}=={30},
        "distance2_clique_number_is_six": len(clique)==6,
        "therefore_no_literal_Heawood_subgraph": len(clique)<7,
        "GF4_trace_table_is_0_0_1_1": [gf4_trace(x) for x in range(4)]==[0,0,1,1],
        "coordinatewise_trace_is_not_projectively_well_defined": counter is not None,
    }

    out={
        "schema":"w33.marcelis-multichart-atlas.v1",
        "status":"PASS" if all(checks.values()) else "PARTIAL",
        "small_incidence_atlas":{
            "PG(3,2)":{"points":len(pgpts),"lines":len(pglines)},
            "Fano_PG(2,2)":{"points":7,"lines":7},
            "Heawood_incidence_graph":{"vertices":14,"edges":21,"degree":3},
            "Hesse_AG(2,3)":{"points":9,"lines":12,"point_degree":4},
            "W(3,3)":{"points":40,"lines":40},
        },
        "w33_chart_web":{
            "charts_skew_line_pairs":len(charts),
            "common_transversals_per_chart":4,
            "web_degree":6,
            "web_edges":edge_count(web),
            "web_triangles":triangle_count(web),
            "distance2_graph_degree":next(iter({len(x) for x in d2})),
            "distance2_graph_clique_number":len(clique),
            "maximum_clique_witness":clique,
            "heawood_literal_lift_falsifier":(
                "A Heawood graph has a seven-vertex bipartition class. Any two "
                "vertices in that class share a neighbor in the other class. In a "
                "triangle-free host these pairs are nonadjacent but share a common "
                "neighbor, so their images would form K7 in the host distance-2 "
                "common-neighbor graph. The exact chart-web distance-2 clique number "
                "is only 6. Hence the 14-vertex Heawood graph is not a literal "
                "subgraph of the 540-chart web."
            ),
        },
        "gf4_trace_firewall":{
            "encoding":{"0":0,"1":1,"omega":2,"omega2=omega+1":3},
            "trace_table":[gf4_trace(x) for x in range(4)],
            "counterexample":counter,
            "verdict":(
                "Coordinatewise Tr_GF4/GF2 is additive on vectors but not a canonical "
                "projective map PG(3,4)->PG(3,2). Marcelis-style trace constructions "
                "must include a representative convention or additional geometry."
            ),
        },
        "site_cross_index":{
            "PG(3,2)_and_hypercubes":(
                "binary local chart language; Fano planes/pencils and the Heawood "
                "incidence graph belong here, not in the global F3^4 coordinate field"
            ),
            "Hessian_configuration":(
                "the 9_4,12_3 Hesse incidence is AG(2,3), matching the qutrit/Hesse "
                "phase-space layer"
            ),
            "Penrose_dodecahedron_and_Witting":(
                "40 Penrose/Witting projective states and 40 orthogonal tetrads give "
                "the state-side realization of the W33 context geometry"
            ),
            "GQ(4,2)_elliptic_and_27_lines":(
                "the 15+12 decomposition, double-six/cubic-surface language and "
                "600-cell model sit on the E6/GQ(4,2) flank of the 27-40-45 ladder"
            ),
            "MOG_and_Steiner_systems":(
                "PG(3,2) lines, Fano pencils/spreads and Witt-design coordinates "
                "connect the code/combinatorics threads to the same binary atlas"
            ),
            "Mermin_Cayley_Salmon_Desargues":(
                "commuting Pauli/Fano contextuality and cubic-surface incidence "
                "provide an operator/incidence bridge rather than an equality of fields"
            ),
            "Icosians_and_E8":(
                "quaternionic 600-cell/E8 route is a separate realization path to the "
                "complex Witting/Eisenstein material"
            ),
            "Heawood_harmonic_cubes":(
                "use as an incidence/scheduler quotient; the direct 14-vertex lift "
                "into the 540 W33 chart web is ruled out by this certificate"
            ),
        },
        "methodological_boundary":(
            "The atlas records compatible projections/quotients and exact finite "
            "incidence identities. Binary PG(3,2), GF(4) projective coordinates, "
            "ternary W33 symplectic coordinates and complex Witting amplitudes are "
            "different coordinate languages and are never identified by bare count."
        ),
        "checks":checks,
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":out["status"],
        "charts":len(charts),
        "web_edges":edge_count(web),
        "distance2_clique_number":len(clique),
        "literal_heawood_subgraph":False,
        "trace_projective_counterexample":counter,
    },indent=2,sort_keys=True))
    return 0 if all(checks.values()) else 1


if __name__=="__main__":
    raise SystemExit(main())
