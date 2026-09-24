#!/usr/bin/env python3
"""Complex temporal connection: coherent phase versus thermodynamic affinity.

Uses the already-established W33 chain ranks (201 cycle space, rank-120
triangle boundaries, H1 dimension 81) but adds a new operational split:
  Re C_e = 1/2 log(k_xy pi_x / k_yx pi_y)
  Im C_e = theta_e.
It also constructs an exact F3-valued locally-flat but globally nontrivial
phase cocycle, exhibiting the H^1 sector directly.
"""
from __future__ import annotations

import json
import math
from itertools import combinations, product
from pathlib import Path

from bt865_dual_torsor_steinberg_compiler import GF3Span, nullspace_mod3

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_20260924_complex_temporal_holonomy.json"
P = 3


def canon(v):
    for x in v:
        if x % P:
            s = 1 if x % P == 1 else 2
            return tuple((s*y) % P for y in v)
    raise ValueError
def build_complex():
    pts = sorted({canon(v) for v in product(range(P), repeat=4) if any(v)})
    def symp(x,y):
        return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1]) % P

    adj = [[False]*40 for _ in range(40)]
    for i,j in combinations(range(40),2):
        adj[i][j] = adj[j][i] = (symp(pts[i],pts[j]) == 0)

    lines = [frozenset(q) for q in combinations(range(40),4)
             if all(adj[i][j] for i,j in combinations(q,2))]
    edges = sorted((i,j) for i,j in combinations(range(40),2) if adj[i][j])
    ei = {e:i for i,e in enumerate(edges)}
    triangles = sorted({tuple(sorted(t)) for L in lines
                        for t in combinations(sorted(L),3)})
    assert (len(pts),len(edges),len(triangles)) == (40,240,160)

    d0 = [[0]*240 for _ in range(40)]
    for k,(a,b) in enumerate(edges):
        d0[a][k] = 2
        d0[b][k] = 1

    tri = []
    for x,y,z in triangles:
        c = [0]*240
        c[ei[(x,y)]] = 1
        c[ei[(y,z)]] = 1
        c[ei[(x,z)]] = 2
        tri.append(c)
    return pts,lines,edges,ei,tri,d0
def dot3(a,b):
    return sum(int(x)*int(y) for x,y in zip(a,b)) % P


def add3(a,b):
    return [(int(x)+int(y)) % P for x,y in zip(a,b)]


def scale_signed_cycle(edges, ei, directed_steps, value):
    out = [0.0]*len(edges)
    for u,v in directed_steps:
        e = (u,v) if u<v else (v,u)
        sign = 1.0 if u<v else -1.0
        out[ei[e]] += sign*value
    return out


def real_period(c,v):
    # c is oriented F3 cycle: 2 means -1.
    total = 0.0
    for x,y in zip(c,v):
        s = 0 if x == 0 else (1 if x == 1 else -1)
        total += s*y
    return total


def main():
    _,lines,edges,ei,tri,d0 = build_complex()
    cycles,_ = nullspace_mod3(d0)
    boundaries = GF3Span(tri)
    assert len(cycles) == 201 and boundaries.rank == 120
    # Cohomology: triangle-flat edge cochains modulo vertex gradients.
    cocycles,_ = nullspace_mod3(tri)
    assert len(cocycles) == 120
    gradient_span = GF3Span(d0)
    assert gradient_span.rank == 39

    topological = None
    for z in cocycles:
        if any(gradient_span.reduce(z)):
            topological = z
            break
    assert topological is not None
    assert all(dot3(t,topological) == 0 for t in tri)

    periods = [dot3(c,topological) for c in cycles]
    nonzero_periods = sum(p != 0 for p in periods)
    assert nonzero_periods > 0

    # Gauge shift by an exact vertex potential leaves all cycle periods unchanged.
    phi = [i % 3 for i in range(40)]
    grad = [0]*240
    for k,(a,b) in enumerate(edges):
        grad[k] = (phi[b]-phi[a]) % 3
    shifted = add3(topological,grad)
    assert [dot3(c,shifted) for c in cycles] == periods
    assert all(dot3(t,shifted) == 0 for t in tri)
    # A single local triangle benchmark for real affinity and coherent phase.
    x,y,z = sorted(next(iter(lines)))[:3]
    steps = [(x,y),(y,z),(z,x)]
    a_edge = scale_signed_cycle(edges,ei,steps,0.5*math.log(2.0))
    th_edge = scale_signed_cycle(edges,ei,steps,math.pi/6)

    tvec = [0]*240
    tvec[ei[(x,y)]] = 1
    tvec[ei[(y,z)]] = 1
    tvec[ei[(x,z)]] = 2
    real_hol = real_period(tvec,a_edge)
    phase_hol = real_period(tvec,th_edge)
    assert abs(real_hol - 1.5*math.log(2.0)) < 1e-12
    assert abs(phase_hol - math.pi/2) < 1e-12

    benchmarks = {
        "flat":{"real_cycle_holonomy":0.0,"phase_cycle_holonomy":0.0},
        "coherent_only":{"real_cycle_holonomy":0.0,"phase_cycle_holonomy":phase_hol},
        "affinity_only":{"real_cycle_holonomy":real_hol,"phase_cycle_holonomy":0.0},
        "mixed":{"real_cycle_holonomy":real_hol,"phase_cycle_holonomy":phase_hol},
    }

    out = {
        "schema":"w33.20260924.complex_temporal_holonomy.v1",
        "status":"PASS_COMPLEX_TEMPORAL_HOLONOMY_SEPARATION",
        "known_chain_complex_crosscheck":{
            "vertices":40,"edges":240,"triangles":160,
            "graph_cycle_dimension":len(cycles),
            "triangle_boundary_rank":boundaries.rank,
            "H1_dimension":len(cycles)-boundaries.rank,
            "cocycle_dimension":len(cocycles),
            "gradient_dimension":gradient_span.rank,
            "H1_dual_dimension":len(cocycles)-gradient_span.rank,
        },
        "complex_connection":{
            "definition":"C_xy = 1/2 log(k_xy*pi_x/(k_yx*pi_y)) + i theta_xy",
            "real_part":"thermodynamic/stochastic affinity coordinate",
            "imaginary_part":"coherent quantum phase coordinate",
            "cycle":"oint C = Sigma_C/2 + i Phi_C",
            "benchmark_triangle":[x,y,z],
            "benchmarks":benchmarks,
            "entropy_production_for_two_to_one_cycle":"Sigma_C = 3 log 2",
        },
        "topological_phase_sector":{
            "field":"F3 phase labels, lifted physically as 2*pi/3 multiples",
            "triangle_flat":True,
            "not_a_vertex_gradient":True,
            "nonzero_periods_on_deterministic_201_cycle_basis":nonzero_periods,
            "period_count_is_basis_dependent":True,
            "gauge_shift_preserves_all_cycle_periods":True,
            "interpretation":(
                "There are coherent phase memories with zero curvature on every "
                "filled W33 triangle but nonzero global holonomy. Local temporal "
                "flatness therefore does not imply globally trivial relational phase."
            ),
        },
        "temporal_classification":{
            "flat":"no phase holonomy and no entropy-producing affinity on the tested cycle",
            "reversible_coherent":"phase holonomy nonzero, real affinity zero",
            "irreversible":"real cycle affinity nonzero; preferred thermodynamic orientation",
            "driven_quantum":"both real affinity and coherent phase nonzero",
        },
        "boundary":(
            "The 201/120/81 chain ranks are prior repo results. The new theorem is "
            "the complex connection separation and explicit non-exact triangle-flat "
            "F3 phase cocycle. A thermodynamic affinity becomes physical only after "
            "rates and a stationary state are specified; no cosmological arrow is inferred."
        ),
    }
    OUT.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":out["status"],
                      "nonzero_topological_periods":nonzero_periods,
                      "real_triangle_holonomy":real_hol,
                      "phase_triangle_holonomy":phase_hol},indent=2))


if __name__=="__main__":
    main()
