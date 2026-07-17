#!/usr/bin/env python3
"""Pass 395: classify the W33 Cayley section under Aut(H).

The 81 inverse-closed sections of the exponent-three Heisenberg quotient split
into exactly two Aut(H)-orbits, of sizes 9 and 72. The canonical W33 section is
in the 9-orbit, which is exactly the linear sections and uniquely satisfies the
Godsil-Hensel distance-regular criterion.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, deque
from itertools import product
from pathlib import Path

import numpy as np

P = 3
Vector = tuple[int, int]
Element = tuple[Vector, int]
V = [(a, b) for a, b in product(range(P), repeat=2)]
V_NONZERO = [v for v in V if v != (0, 0)]
H = [(v, c) for v in V for c in range(P)]
H_INDEX = {h: i for i, h in enumerate(H)}
PAIR_REPRESENTATIVES = [(0, 1), (1, 0), (1, 1), (1, 2)]


def add(u: Vector, v: Vector) -> Vector:
    return ((u[0] + v[0]) % P, (u[1] + v[1]) % P)


def neg(u: Vector) -> Vector:
    return ((-u[0]) % P, (-u[1]) % P)


def alternating(u: Vector, v: Vector) -> int:
    return (u[1] * v[0] - u[0] * v[1]) % P


def multiply(x: Element, y: Element) -> Element:
    u, c = x
    v, d = y
    return add(u, v), (c + d + alternating(u, v)) % P


def all_inverse_closed_sections() -> list[tuple[int, ...]]:
    sections = []
    for values in product(range(P), repeat=4):
        f: dict[Vector, int] = {}
        for vector, value in zip(PAIR_REPRESENTATIVES, values):
            f[vector] = value
            f[neg(vector)] = (-value) % P
        sections.append(tuple(f[v] for v in V_NONZERO))
    return sections


def gl2() -> list[tuple[tuple[int, int, int, int], int]]:
    result = []
    for a, b, c, d in product(range(P), repeat=4):
        determinant = (a*d - b*c) % P
        if determinant:
            result.append(((a,b,c,d), determinant))
    return result


def mat_apply(matrix: tuple[int,int,int,int], vector: Vector) -> Vector:
    a,b,c,d = matrix
    return ((a*vector[0]+b*vector[1])%P, (c*vector[0]+d*vector[1])%P)


def automorphisms():
    return [(m, det, ell) for m, det in gl2() for ell in V]


def transform_section(section, automorphism):
    function = dict(zip(V_NONZERO, section))
    matrix, determinant, linear = automorphism
    image = {}
    for vector in V_NONZERO:
        target = mat_apply(matrix, vector)
        image[target] = (determinant*function[vector] + linear[0]*vector[0] + linear[1]*vector[1]) % P
    return tuple(image[v] for v in V_NONZERO)


def section_orbits(sections, autos):
    remaining = set(sections)
    orbits = []
    while remaining:
        representative = min(remaining)
        orbit = {transform_section(representative, auto) for auto in autos}
        orbits.append(orbit)
        remaining.difference_update(orbit)
    return sorted(orbits, key=lambda orbit: (len(orbit), min(orbit)))


def is_linear(section) -> bool:
    f = {(0,0): 0, **dict(zip(V_NONZERO, section))}
    return all(f[add(u,v)] == (f[u]+f[v])%P for u in V for v in V)


def connection_set(section):
    f = dict(zip(V_NONZERO, section))
    return [(v, f[v]) for v in V_NONZERO]


def cayley_adjacency(section):
    A = np.zeros((27,27), dtype=np.int8)
    for i,h in enumerate(H):
        for step in connection_set(section):
            A[i, H_INDEX[multiply(h,step)]] = 1
    assert np.array_equal(A,A.T)
    return A


def distances(A):
    D = np.full(A.shape, -1, dtype=np.int8)
    neighbors = [np.flatnonzero(A[i]).tolist() for i in range(27)]
    for source in range(27):
        D[source,source] = 0
        queue: deque[int] = deque([source])
        while queue:
            u = queue.popleft()
            for v in neighbors[u]:
                if D[source,v] < 0:
                    D[source,v] = D[source,u] + 1
                    queue.append(v)
    return D


def graph_summary(section):
    A = cayley_adjacency(section)
    D = distances(A)
    intersection: dict[int,set[tuple[int,int,int]]] = {}
    for source in range(27):
        for target in range(27):
            distance = int(D[source,target])
            if distance == 0:
                continue
            neighbors = np.flatnonzero(A[target])
            triple = (
                int(np.count_nonzero(D[source,neighbors] == distance-1)),
                int(np.count_nonzero(D[source,neighbors] == distance)),
                int(np.count_nonzero(D[source,neighbors] == distance+1)),
            )
            intersection.setdefault(distance,set()).add(triple)
    c2 = Counter()
    same = Counter()
    for i in range(27):
        for j in range(i+1,27):
            if A[i,j]:
                continue
            common = int(np.dot(A[i],A[j]))
            (same if H[i][0] == H[j][0] else c2)[common] += 1
    return {
        "degree": sorted(set(int(x) for x in A.sum(1))),
        "diameter": int(D.max()),
        "distance_regular": all(len(values)==1 for values in intersection.values()),
        "intersection_profiles": {str(d): [list(v) for v in sorted(values)] for d,values in sorted(intersection.items())},
        "different_fibre_common_neighbor_profile": {str(k): int(v) for k,v in sorted(c2.items())},
        "same_fibre_common_neighbor_profile": {str(k): int(v) for k,v in sorted(same.items())},
    }


def stable_hash(payload):
    return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":")).encode()).hexdigest()


def build_certificate():
    sections = all_inverse_closed_sections()
    autos = automorphisms()
    orbits = section_orbits(sections, autos)
    zero = tuple(0 for _ in V_NONZERO)
    canonical = next(o for o in orbits if zero in o)
    nonlinear = next(o for o in orbits if zero not in o)
    canonical_summary = graph_summary(zero)
    nonlinear_summary = graph_summary(min(nonlinear))
    stabilizer = sum(transform_section(zero,a)==zero for a in autos)
    linear_sections = {s for s in sections if is_linear(s)}
    checks = {
        "heisenberg_order_27": len(H)==27,
        "aut_order_432": len(autos)==432,
        "sections_81": len(sections)==81,
        "two_orbits_9_72": sorted(len(o) for o in orbits)==[9,72],
        "canonical_orbit_equals_linear_sections": canonical==linear_sections,
        "canonical_stabilizer_48": stabilizer==48,
        "canonical_distance_regular": canonical_summary["distance_regular"],
        "canonical_array": canonical_summary["intersection_profiles"]=={"1":[[1,1,6]],"2":[[3,4,1]],"3":[[8,0,0]]},
        "canonical_c2_3": canonical_summary["different_fibre_common_neighbor_profile"]=={"3":216},
        "nonlinear_not_distance_regular": not nonlinear_summary["distance_regular"],
        "nonlinear_c2_not_constant": len(nonlinear_summary["different_fibre_common_neighbor_profile"])>1,
    }
    payload = {
        "pass":395,
        "status":"PASS" if all(checks.values()) else "FAIL",
        "group":{"order":27,"aut_order":432,"aut_structure":"Hom(F3^2,F3):GL(2,3)"},
        "section_space":{"count":81,"orbit_sizes":[len(o) for o in orbits]},
        "canonical_orbit":{"orbit_size":len(canonical),"stabilizer_order":stabilizer,"characterization":"the nine linear functionals F3^2->F3","graph":canonical_summary,"verdict":"unique Aut(H)-orbit satisfying the distance-regular (9,3,3)-cover criterion"},
        "nonlinear_orbit":{"orbit_size":len(nonlinear),"stabilizer_order":len(autos)//len(nonlinear),"graph":nonlinear_summary,"verdict":"regular covers of K9, but not distance-regular"},
        "checks":checks,
    }
    payload["certificate_sha256"] = stable_hash(payload)
    return payload


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,default=Path("data/w33_pass395_cayley_section_classification.json"))
    parser.add_argument("--check",action="store_true")
    args=parser.parse_args()
    payload=build_certificate()
    text=json.dumps(payload,indent=2,sort_keys=True)+"\n"
    if args.check:
        if not args.output.exists() or args.output.read_text()!=text:
            raise SystemExit("Pass 395 certificate drift")
    else:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text)
    print(json.dumps({"status":payload["status"],"orbit_sizes":payload["section_space"]["orbit_sizes"],"canonical_stabilizer":payload["canonical_orbit"]["stabilizer_order"],"certificate_sha256":payload["certificate_sha256"]}))


if __name__=="__main__":
    main()
