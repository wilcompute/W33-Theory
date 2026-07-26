#!/usr/bin/env python3
"""Pass 1034: selector correction is a binary torsor, not an invariant cochain."""
from __future__ import annotations

import json
import sys
from collections import Counter
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass1031_dual_120_phase_carriers import (
    act_line, act_point_matching, build_w33, compose, generate_psp,
    perfect_matchings,
)

DATA = ROOT / "data"
OUT = DATA / "w33_pass1034_selector_correction_torsor.json"


def canonical_cycle(cycle):
    variants = []
    for seq in (list(cycle), list(reversed(cycle))):
        for shift in range(4):
            variants.append(tuple(seq[shift:] + seq[:shift]))
    return min(variants)


def build_draft_geometry():
    points, _ = build_w33()
    point_index = {p: i for i, p in enumerate(points)}
    def omega(u, v):
        return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1]) % 3
    adjacency = [[0]*40 for _ in range(40)]
    for i,u in enumerate(points):
        for j,v in enumerate(points):
            if i != j and omega(u,v) == 0:
                adjacency[i][j] = 1
    lines = []
    seen = set()
    for i in range(40):
        for j in range(i+1,40):
            if not adjacency[i][j]:
                continue
            line = set()
            for a,b in product(range(3), repeat=2):
                if a == 0 and b == 0:
                    continue
                raw = tuple((a*points[i][c]+b*points[j][c]) % 3 for c in range(4))
                for x in raw:
                    if x:
                        inv = pow(int(x),-1,3)
                        canon = tuple(y*inv % 3 for y in raw)
                        break
                line.add(point_index[canon])
            key = frozenset(line)
            if key not in seen:
                seen.add(key)
                lines.append(tuple(sorted(line)))
    sigma = {}
    for left,L1 in enumerate(lines):
        for right,L2 in enumerate(lines):
            if left == right:
                continue
            common = list(set(L1)&set(L2))
            if len(common) != 1:
                continue
            point = common[0]
            v1 = points[next(x for x in L1 if x != point)]
            v2 = points[next(x for x in L2 if x != point)]
            sigma[(point,left,right)] = 1 if omega(v1,v2) == 1 else -1
    edges = []
    edge_index = {}
    line_adj = [[False]*40 for _ in range(40)]
    for left,right in combinations(range(40),2):
        if len(set(lines[left])&set(lines[right])) == 1:
            edge_index[(left,right)] = len(edges)
            edges.append((left,right))
            line_adj[left][right] = line_adj[right][left] = True
    quadrangles = []
    seen_quads = set()
    for l0 in range(40):
        for l1 in range(40):
            if not line_adj[l0][l1]:
                continue
            p01 = next(iter(set(lines[l0])&set(lines[l1])))
            for l2 in range(40):
                if l2 == l0 or not line_adj[l1][l2]:
                    continue
                p12 = next(iter(set(lines[l1])&set(lines[l2])))
                if p12 == p01:
                    continue
                for l3 in range(40):
                    if l3 == l1 or not line_adj[l2][l3] or not line_adj[l3][l0]:
                        continue
                    p23 = next(iter(set(lines[l2])&set(lines[l3])))
                    p30 = next(iter(set(lines[l3])&set(lines[l0])))
                    if len({p01,p12,p23,p30}) < 4:
                        continue
                    cycle = canonical_cycle((l0,l1,l2,l3))
                    if cycle in seen_quads:
                        continue
                    seen_quads.add(cycle)
                    hol = sigma[(p01,l0,l1)]*sigma[(p12,l1,l2)]*sigma[(p23,l2,l3)]*sigma[(p30,l3,l0)]
                    mask = 0
                    for a,b in zip(cycle,cycle[1:]+cycle[:1]):
                        mask ^= 1 << edge_index[tuple(sorted((a,b)))]
                    quadrangles.append((cycle,hol,mask))
    return points,lines,edges,edge_index,quadrangles


def solve_gf2(rows, variable_count):
    pivots = {}
    pivot_rhs = {}
    for mask,rhs in rows:
        current,value = mask,rhs
        while current:
            column = current.bit_length()-1
            if column not in pivots:
                pivots[column] = current
                pivot_rhs[column] = value
                break
            current ^= pivots[column]
            value ^= pivot_rhs[column]
        else:
            if value:
                return None,len(pivots),variable_count-len(pivots)
    solution = 0
    for column in sorted(pivots):
        rest = pivots[column] & ~(1<<column)
        if ((rest & solution).bit_count() % 2) ^ pivot_rhs[column]:
            solution |= 1<<column
    return solution,len(pivots),variable_count-len(pivots)


def act_mask(edge_permutation, mask):
    out = 0
    for edge,target in enumerate(edge_permutation):
        if (mask>>edge)&1:
            out |= 1<<target
    return out


def main():
    p1032 = json.loads((DATA/"w33_pass1032_selector_orbital_fusion_shadow.json").read_text())
    points,lines,edges,edge_index,quadrangles = build_draft_geometry()
    group = generate_psp(points)
    line_index = {line:i for i,line in enumerate(lines)}
    failures = {cycle for cycle,hol,_ in quadrangles if hol == -1}
    line_permutations = {g:tuple(line_index[act_line(g,line)] for line in lines) for g in group}
    def act_cycle(lp,cycle):
        return canonical_cycle(tuple(lp[x] for x in cycle))
    H = [g for g in group if {act_cycle(line_permutations[g],c) for c in failures} == failures]
    edge_permutations = {}
    for g in H:
        lp = line_permutations[g]
        edge_permutations[g] = tuple(edge_index[tuple(sorted((lp[a],lp[b])))] for a,b in edges)
    unseen = set(range(len(edges)))
    edge_orbits = []
    while unseen:
        edge = min(unseen)
        orbit = sorted({edge_permutations[g][edge] for g in H})
        edge_orbits.append(orbit)
        unseen -= set(orbit)
    edge_orbits.sort(key=lambda orbit:(len(orbit),orbit))
    orbit_of = {edge:i for i,orbit in enumerate(edge_orbits) for edge in orbit}
    full_rows = [(mask,0 if hol == 1 else 1) for _,hol,mask in quadrangles]
    solution,rank,free = solve_gf2(full_rows,len(edges))
    assert solution is not None
    invariant_rows = []
    for cycle,hol,_ in quadrangles:
        mask = 0
        for a,b in zip(cycle,cycle[1:]+cycle[:1]):
            mask ^= 1 << orbit_of[edge_index[tuple(sorted((a,b)))]]
        invariant_rows.append((mask,0 if hol == 1 else 1))
    invariant_solutions = [x for x in range(1<<len(edge_orbits)) if all(((m&x).bit_count()%2)==r for m,r in invariant_rows)]
    correction_orbit = {act_mask(edge_permutations[g],solution) for g in H}
    correction_pair = sorted(correction_orbit)
    correction_kernel = {g for g in H if act_mask(edge_permutations[g],solution) == solution}
    difference = correction_pair[0]^correction_pair[1]
    def satisfies(mask,inhomogeneous=True):
        return all(((row&mask).bit_count()%2)==(rhs if inhomogeneous else 0) for row,rhs in full_rows)
    matchings = perfect_matchings(list(lines[0]))
    matching_permutation = {g:tuple(matchings.index(act_point_matching(g,m)) for m in matchings) for g in H}
    identity3 = (0,1,2)
    inversion_kernel = {g for g in H if matching_permutation[g] == identity3}
    correction_char = {g:int(act_mask(edge_permutations[g],solution) != solution) for g in H}
    inversion_char = {g:int(matching_permutation[g] != identity3) for g in H}
    joint_profile = Counter((correction_char[g],inversion_char[g]) for g in H)
    chars_are_homs = all(correction_char[compose(g,h)] == (correction_char[g]^correction_char[h]) and inversion_char[compose(g,h)] == (inversion_char[g]^inversion_char[h]) for g in H for h in H)
    corrected_failures = [sum(1 for _,hol,mask in quadrangles if hol*(-1 if (mask&corr).bit_count()%2 else 1) != 1) for corr in correction_pair]
    checks = {
        "source_fusion_certificate_passes": p1032["status"] == "PASS",
        "w33_counts_are_40_lines_240_edges": len(lines)==40 and len(edges)==240,
        "unique_quadrangles_are_1620": len(quadrangles)==1620,
        "failure_sheet_has_108_quadrangles": len(failures)==108,
        "sheet_stabilizer_order_is_216": len(H)==216,
        "edge_orbits_are_12_12_108_108": sorted(map(len,edge_orbits))==[12,12,108,108],
        "no_sheet_stabilizer_invariant_correction": invariant_solutions==[],
        "full_system_rank_is_200": rank==200,
        "full_solution_space_dimension_is_40": free==40,
        "deterministic_correction_has_weight_54": solution.bit_count()==54,
        "correction_orbit_has_two_elements": len(correction_pair)==2,
        "both_corrections_have_weight_54": {x.bit_count() for x in correction_pair}=={54},
        "both_corrections_flatten_all_quadrangles": corrected_failures==[0,0],
        "correction_stabilizer_has_order_108": len(correction_kernel)==108,
        "difference_is_weight_108_homogeneous_cocycle": difference.bit_count()==108 and satisfies(difference,False),
        "one_local_matching_is_fixed": [i for i in range(3) if all(act_point_matching(g,matchings[i])==matchings[i] for g in H)]==[0],
        "local_phase_inversion_kernel_has_order_108": len(inversion_kernel)==108,
        "correction_and_inversion_characters_are_homomorphisms": chars_are_homs,
        "characters_are_independent": joint_profile==Counter({(0,0):54,(0,1):54,(1,0):54,(1,1):54}),
        "joint_kernel_has_order_54": len(correction_kernel & inversion_kernel)==54,
    }
    if not all(checks.values()):
        raise AssertionError([k for k,v in checks.items() if not v])
    result = {
        "schema":"w33.pass1034.selector_correction_torsor.python.v1",
        "status":"PASS",
        "headline":"The golden-selector flatness correction cannot be chosen invariantly under the order-216 sheet stabilizer. The deterministic 54-edge correction instead belongs to an exact two-element torsor; its exchange character is independent of the local S3 phase-inversion character, yielding a C2 x C2 quotient with kernel order 54.",
        "cochain_system":{"variables":len(edges),"equations":len(quadrangles),"rank":rank,"free_dimension":free,"failure_rhs_weight":len(failures)},
        "sheet_stabilizer":{"order":len(H),"edge_orbit_sizes":sorted(map(len,edge_orbits)),"invariant_variable_count":len(edge_orbits),"invariant_solution_count":len(invariant_solutions)},
        "correction_torsor":{"orbit_size":len(correction_pair),"correction_weights":[x.bit_count() for x in correction_pair],"stabilizer_order":len(correction_kernel),"difference_weight":difference.bit_count(),"difference_is_homogeneous":satisfies(difference,False),"corrected_failure_counts":corrected_failures},
        "two_binary_characters":{"correction_exchange_kernel_order":len(correction_kernel),"local_phase_inversion_kernel_order":len(inversion_kernel),"joint_kernel_order":len(correction_kernel & inversion_kernel),"joint_image":"C2 x C2","joint_profile":{f"{a}{b}":count for (a,b),count in sorted(joint_profile.items())},"interpretation":"The correction orientation and residual S3 inversion are independent bits. A flat implementation needs a separate correction-frame choice."},
        "checks":checks,"check_count":len(checks),
        "boundary":"The pair is canonical as the orbit of the deterministic gauge-fixed correction. This does not claim these are the only weight-54 solutions in the full 2^40-element affine solution space."
    }
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("Pass1034 PASS")


if __name__ == "__main__":
    main()
