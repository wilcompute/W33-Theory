#!/usr/bin/env python3
"""Explicit PG(3,4) / hyperbolic quadric from 600-cell icosian coordinates.

Recover all 85 projective points from EXACT binary-icosian 60 antipodal
axes and 25 inscribed 24-cells. The cells are the Q+(3,4) rank-one
matrix points; axes are the invertible PGL2(4)=A5 matrix points. Their
geometric membership exactly matches polar-quadric orthogonality.
Full 357 projective lines and 85 planes verified with GF4 arithmetic.

PG(3,4) relationship and 25 cells preexist Denney et al 2020. The
particular icosian-coset/matrix coordinatization is an independently
reproducible explicit bridge and should not be claimed new without
historical isomorphism check.
"""
from __future__ import annotations
import collections,itertools,json
from pathlib import Path
import networkx as nx
import toe_20261104_icosian_24cell_tomotope_obstruction as ico

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261104_pg34_icosian_quadric.json"
F=range(4)
def add(a,b):return a^b
def mul(a,b):
    a0,a1=a&1,(a>>1)&1
    b0,b1=b&1,(b>>1)&1
    return (a0*b0^a1*b1)|((a0*b1^a1*b0^a1*b1)<<1)
def inv(a):
    assert a!=0
    return next(b for b in (1,2,3) if mul(a,b)==1)
def norm(v):
    a=next(x for x in v if x!=0)
    return tuple(mul(x,inv(a)) for x in v)
def vadd(v,w):return tuple(add(x,y) for x,y in zip(v,w))
def vscale(a,v):return tuple(mul(a,x) for x in v)
def rankone(u,v):
    return norm(tuple(mul(x,y) for x in u for y in v))
def det(m):return mul(m[0],m[3])^mul(m[1],m[2])
def polar(x,y):return det(vadd(x,y))^det(x)^det(y)
def sign(per):
    return sum(per[i]>per[j] for i in range(5) for j in range(i+1,5))%2

def spatial_rank_at_most_two(a,b,c):
    """Exact rank over Q(phi) of three R4 icosian vectors, with /2 scaled away."""
    def sub(x,y):return ico.add(x,ico.neg(y))
    for i,j,k in itertools.combinations(range(4),3):
        term1=ico.m(a[i],sub(ico.m(b[j],c[k]),ico.m(b[k],c[j])))
        term2=ico.m(a[j],sub(ico.m(b[i],c[k]),ico.m(b[k],c[i])))
        term3=ico.m(a[k],sub(ico.m(b[i],c[j]),ico.m(b[j],c[i])))
        val=ico.add(sub(term1,term2),term3)
        if val!=(0,0):return False
    return True
def lines_of_pg(points):
    """357 lines, all points of each are spanned by GF4 vector pairs."""
    idx={p:i for i,p in enumerate(points)}
    d={}
    for i,p in enumerate(points):
        for j in range(i+1,len(points)):
            q=points[j]
            line=frozenset(idx[norm(vadd(p,vscale(a,q)))] for a in F) | {j}
            assert len(line)==5
            d[line]=None
    assert len(d)==357
    lines=sorted((tuple(sorted(x)) for x in d),key=lambda x:x)
    assert all(len(x)==5 for x in lines)
    through=collections.Counter(i for ln in lines for i in ln)
    assert set(through.values())=={21}
    return lines

def geometry():
    G,H=ico.build()
    cells,_=ico.twentyfive(G,H)
    all_axes=sorted({frozenset((x,ico.scaled(x,-1))) for x in G},
                    key=lambda a:sorted(a)[0])
    assert len(all_axes)==60
    disjoint=nx.Graph()
    disjoint.add_nodes_from(range(25))
    disjoint.add_edges_from((i,j) for i in range(25) for j in range(i+1,25) if not cells[i]&cells[j])
    assert nx.is_isomorphic(disjoint,nx.line_graph(nx.complete_bipartite_graph(5,5)))
    cliques=sorted((frozenset(z) for z in nx.find_cliques(disjoint)),key=lambda z:tuple(sorted(z)))
    assert len(cliques)==10
    rows=[cliques[0]]+[c for c in cliques[1:] if not c&cliques[0]]
    cols=[c for c in cliques if c not in rows]
    assert len(rows)==len(cols)==5 and all(len(x)==5 for x in rows+cols)
    pos={next(iter(r&c)):(i,j) for i,r in enumerate(rows) for j,c in enumerate(cols)}
    assert len(pos)==25
    row_col_to_cell={(i,j):k for k,(i,j) in pos.items()}
    assert len(row_col_to_cell)==25
    permutations={}
    for ix,axis in enumerate(all_axes):
        own=[c for c in range(25) if axis<=cells[c]]
        assert len(own)==5
        p=tuple(next(pos[c][1] for c in own if pos[c][0]==i) for i in range(5))
        assert len(set(p))==5
        assert p not in permutations
        permutations[p]=ix
    assert len(permutations)==60
    initial_parities=collections.Counter(sign(p) for p in permutations)
    assert len(initial_parities)==1
    if 1 in initial_parities:
        # Column relabelling flips all odd permutations to A5.
        pos={k:(r,c^1 if c in (0,1) else c) for k,(r,c) in pos.items()}
        row_col_to_cell={(i,j):k for k,(i,j) in pos.items()}
        permutations={}
        for ix,axis in enumerate(all_axes):
            own=[c for c in range(25) if axis<=cells[c]]
            p=tuple(next(pos[c][1] for c in own if pos[c][0]==i) for i in range(5))
            assert p not in permutations
            permutations[p]=ix
    assert set(sign(p) for p in permutations)=={0}

    proj=[norm(v) for v in itertools.product(F,repeat=2) if v!=(0,0)]
    proj=sorted(set(proj))
    assert len(proj)==5
    quadric=[rankone(u,v) for u in proj for v in proj]
    assert len(set(quadric))==25
    full=set(norm(m) for m in itertools.product(F,repeat=4) if any(m))
    assert len(full)==85
    nonsingular={m for m in full if det(m)}
    assert len(nonsingular)==60
    gper={}
    for m in nonsingular:
        p=[]
        for u in proj:
            matches=[j for j,v in enumerate(proj) if polar(m,rankone(u,v))==0]
            assert len(matches)==1
            p.append(matches[0])
        pp=tuple(p)
        assert pp not in gper and sign(pp)==0
        gper[pp]=m
    assert set(gper)==set(permutations)=={p for p in itertools.permutations(range(5)) if sign(p)==0}
    objects=[None]*85
    for c in range(25):
        r,k=pos[c]
        objects[c]=rankone(proj[r],proj[k])
    for perm,ix in permutations.items():
        objects[25+ix]=gper[perm]
    assert len(set(objects))==85 and set(objects)==full
    # Membership of an axis in a cell equals hyperbolic polarity in PG3(F4)
    incidence=[(c,ix) for c in range(25) for ix,ax in enumerate(all_axes) if ax<=cells[c]]
    assert len(incidence)==300
    for c in range(25):
        for ix in range(60):
            assert ((c,ix) in incidence)==(polar(objects[c],objects[25+ix])==0)
    assert all(sum(c==c0 for c,_ in incidence)==12 for c0 in range(25))
    assert all(sum(ix==ix0 for _,ix in incidence)==5 for ix0 in range(60))
    lines=lines_of_pg(objects)
    typ=collections.Counter(sum(det(objects[p])==0 for p in line) for line in lines)
    assert typ=={0:72,1:75,2:200,5:10}
    # Every rank-one point lies on 2 generators, 3 tangent lines,
    # 16 secants and on 12 external polar points.
    assert all(sum(c in ln and sum(det(objects[p])==0 for p in ln)==5 for ln in lines)==2 for c in range(25))
    assert all(sum(c in ln and sum(det(objects[p])==0 for p in ln)==1 for ln in lines)==3 for c in range(25))
    rows_all=set()
    for c in range(25):
        rows_all.add(tuple(sorted([j for j in range(85) if polar(objects[c],objects[j])==0])))
    assert len(rows_all)==25 and all(len(x)==21 for x in rows_all)
    # All 85 polar planes non-degenerate: 21 points in a plane; direct
    # projective-polars since matrix determinant is a nondegenerate quadratic.
    polar_planes=[tuple(j for j in range(85) if polar(objects[i],objects[j])==0) for i in range(85)]
    assert len(set(polar_planes))==85 and set(map(len,polar_planes))=={21}

    reye_tangent_plane_records=[]
    for c in range(25):
        tangent=set(polar_planes[c])
        tangent_lines=[ln for ln in lines if set(ln)<=tangent]
        assert len(tangent_lines)==21
        through_c=[ln for ln in tangent_lines if c in ln]
        avoid_c=[ln for ln in tangent_lines if c not in ln]
        assert len(through_c)==5 and len(avoid_c)==16
        axes_within={ix for ix,axis in enumerate(all_axes) if axis<=cells[c]}
        assert len(axes_within)==12
        assert {i-25 for i in tangent if i>=25}==axes_within
        projective_reye_planes={frozenset(i-25 for i in ln if i>=25) for ln in avoid_c}
        assert len(projective_reye_planes)==16 and all(len(t)==3 for t in projective_reye_planes)
        # Compare against the *geometric* 16 central hexagonal planes
        # of this 24-cell, using exact Q(phi) 3x3 minors.
        spatial_planes=set()
        for i,j in itertools.combinations(sorted(axes_within),2):
            va=sorted(all_axes[i])[0]
            vb=sorted(all_axes[j])[0]
            pp=frozenset(k for k in axes_within if
                spatial_rank_at_most_two(va,vb,sorted(all_axes[k])[0]))
            if len(pp)==3:spatial_planes.add(pp)
        assert len(spatial_planes)==16
        assert projective_reye_planes==spatial_planes
        assert all(sum(ix in pp for pp in spatial_planes)==4 for ix in axes_within)
        counts=collections.Counter(sum(det(objects[p])==0 for p in ln) for ln in tangent_lines)
        assert counts=={1:3,2:16,5:2}
        reye_tangent_plane_records.append(dict(cell_id=c,
            incidence_axes=sorted(axes_within),
            central_hexagon_axes=[sorted(t) for t in sorted(spatial_planes,key=lambda s:tuple(sorted(s)))],
            tangent_plane_projective_lines=21,
            lines_not_through_quadric_center=16,
            icosian_hexagon_planes_identical_to_projective_secants=True))

    # Pairwise 24cell intersection is precisely the PG3(4) generator/secant
    # line dichotomy. The 200 non-disjoint pairs share one full hexagon
    # (3 axes), and those 200 triples are all DIFFERENT. Every one of
    # the 25 Reye packets contributes its 16 central-plane triples
    # twice to the 200 shared hexagons.
    common_hexagon_counts=collections.Counter()
    shared_hexagons={}
    bypair={}
    for ln in lines:
        qq=[v for v in ln if v<25]
        if len(qq)==2:bypair[tuple(sorted(qq))]=set(ln)
        if len(qq)==5:
            for a,b in itertools.combinations(qq,2):
                bypair[tuple(sorted((a,b)))]=set(ln)
    assert len(bypair)==300
    shared_count=collections.Counter()
    for c1,c2 in itertools.combinations(range(25),2):
        x1=set(reye_tangent_plane_records[c1]["incidence_axes"])
        x2=set(reye_tangent_plane_records[c2]["incidence_axes"])
        joint=frozenset(x1&x2)
        assert len(joint) in (0,3)
        shared_count[len(joint)]+=1
        qline=bypair[(c1,c2)]
        polar_line={k for k in range(85) if
            polar(objects[c1],objects[k])==0 and
            polar(objects[c2],objects[k])==0}
        assert len(polar_line)==5
        assert tuple(sorted(polar_line)) in {tuple(ln) for ln in lines}
        if joint:
            assert len(qline)==5 and sum(x<25 for x in qline)==2
            assert {k-25 for k in polar_line if k>=25}==set(joint)
            assert sum(k<25 for k in polar_line)==2
            assert c1 not in polar_line and c2 not in polar_line
            h1={frozenset(ln) for ln in reye_tangent_plane_records[c1]["central_hexagon_axes"]}
            h2={frozenset(ln) for ln in reye_tangent_plane_records[c2]["central_hexagon_axes"]}
            assert joint in h1 and joint in h2
            common_hexagon_counts[joint]+=1
            shared_hexagons[f"{c1}-{c2}"]=sorted(joint)
        else:
            assert all(x<25 for x in qline)
            assert polar_line==qline
    assert shared_count=={0:100,3:200}
    assert len(common_hexagon_counts)==200
    assert set(common_hexagon_counts.values())=={1}

    return {
        "status":"PASS_FULL_EXPLICIT_PG34_600CELL_85_POINTS_357_LINES_POLARITY",
        "icosian_vertices":120,
        "inscribed_24cells":25,"antipodal_axes":60,
        "all_axes_are_even_5_permutations":True,
        "axis_permutations_equal_A5_equal_PGL2_F4":True,
        "axes_as_projective_invertible_2x2_F4_matrices":60,
        "cells_as_projective_rank1_2x2_F4_matrices":25,
        "axis_cell_polar_incidence_exact_matches_300_memberships":True,
        "PG3F4_points":85,"PG3F4_lines":len(lines),"PG3F4_planes":len(polar_planes),
        "lines_through_each_point":21,"points_on_each_line":5,
        "line_types_number_quadric_points":dict(sorted(typ.items())),
        "quadric_generators_two_reguli":10,
        "cell_axis_incidence_rows_each":12,
        "cell_axis_incidence_cols_each":5,
        "quadric_polar_plane_contains_21_points":True,
        "all_25_24cells_reye_graphs_are_16_tangent_plane_secants":True,
        "all_25_spatial_hexagon_planes_equal_projective_secant_triples":True,
        "24cell_pair_shared_icosian_axes_histogram":dict(shared_count),
        "200_distinct_shared_3axis_hexagons":len(common_hexagon_counts),
        "all_200_shared_hexagons_match_polar_duals_of_2quadric_secants":True,
        "shared_hexagon_between_cell_pairs":shared_hexagons,
        "reye_tangent_plane_records_25":reye_tangent_plane_records,
        "projective_point_coordinates_85":[list(v) for v in objects],
        "icosian_axis_permutations_60":[{"axis_id":ix,"permutation":list(perm)}
            for perm,ix in sorted(permutations.items(),key=lambda kv:kv[1])],
        "cell_grid_locations_25":[[pos[i][0],pos[i][1]] for i in range(25)],
        "known_prior_art":"Denney et al (2020) establish 600-cell to PG(3,4) using E8/2E8; A5=PGL2(4) and hyperbolic quadric coordinatization are classical. This concrete icosian incidence realization is independently recomputed; no discovery priority claim.",
        "physics_boundary":"Finite exact F4 incidence only. Does not derive E8/2E8 lattice isomorphism, a canonical quantum state-map, physical 4D spacetime, or an experimentally selected 24-cell."
    }
def main():
    out=geometry()
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(out["status"],out["line_types_number_quadric_points"],flush=True)
    return out
if __name__=="__main__":main()
