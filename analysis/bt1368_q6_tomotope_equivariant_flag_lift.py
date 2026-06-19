#!/usr/bin/env python3
"""BT1368: Q6 edge symmetry lift to the tomotope flag action.

BT1364 identified the common carrier size |E(Q6)| = 192 = tomotope flags.
This verifier upgrades the count statement to a group-action certificate.

It searches the Q6 edge automorphism group for an invariant 2^4:S3 subgroup
whose action on the 192 Q6 edges has the same two regular 96-point orbits and
the same order profile as Aut(tomotope) on the true 192-flag model.  GAP then
checks that the two permutation groups are isomorphic.  Because both actions
are regular on each 96-point orbit, the isomorphism plus a base edge/flag
choice gives an actual equivariant bijection orbit-by-orbit.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import math
import shutil
import subprocess
import zipfile
from collections import Counter, deque
from itertools import combinations
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1368_q6_tomotope_equivariant_flag_lift.json"
BUNDLE = ROOT / "pillars" / "TOE_tomotope_true_flag_model_v02_20260228_bundle.zip"


Perm = tuple[int, ...]


def compose(a: Perm, b: Perm) -> Perm:
    return tuple(a[b[i]] for i in range(len(a)))


def perm_order(p: Perm) -> int:
    seen = [False] * len(p)
    lcm = 1
    for i in range(len(p)):
        if seen[i]:
            continue
        j = i
        length = 0
        while not seen[j]:
            seen[j] = True
            length += 1
            j = p[j]
        lcm = math.lcm(lcm, length)
    return lcm


def order_profile(perms: Iterable[Perm]) -> dict[str, int]:
    return {str(k): v for k, v in sorted(Counter(perm_order(p) for p in perms).items())}


def closure(gens: list[Perm], n: int) -> list[Perm]:
    ident = tuple(range(n))
    group = {ident}
    frontier = [ident]
    while frontier:
        cur = frontier.pop()
        for gen in gens:
            nxt = compose(gen, cur)
            if nxt not in group:
                group.add(nxt)
                frontier.append(nxt)
    return sorted(group)


def orbit_sizes(items: range, perms: list[Perm]) -> list[int]:
    unseen = set(items)
    out = []
    while unseen:
        start = next(iter(unseen))
        orbit = {start}
        frontier = [start]
        while frontier:
            x = frontier.pop()
            for p in perms:
                y = p[x]
                if y not in orbit:
                    orbit.add(y)
                    frontier.append(y)
        out.append(len(orbit))
        unseen -= orbit
    return sorted(out)


def build_tomotope_aut_group() -> tuple[list[Perm], list[Perm], dict[str, object]]:
    with zipfile.ZipFile(BUNDLE) as zf:
        gens_raw = json.loads(zf.read("tomotope_r_generators_192.json"))
        r = [tuple(gens_raw[f"r{i}"]) for i in range(4)]
        reader = csv.DictReader(io.StringIO(zf.read("tomotope_flags_192.csv").decode()))
        flags = [row for row in reader]
    n = 192
    word_to = {0: []}
    queue: deque[int] = deque([0])
    while queue:
        flag = queue.popleft()
        for i, gen in enumerate(r):
            nxt = gen[flag]
            if nxt not in word_to:
                word_to[nxt] = word_to[flag] + [i]
                queue.append(nxt)

    def apply_word(start: int, word: list[int]) -> int:
        cur = start
        for i in word:
            cur = r[i][cur]
        return cur

    autos = []
    for target in range(n):
        phi = tuple(apply_word(target, word_to[flag]) for flag in range(n))
        if len(set(phi)) == n and all(
            phi[r[i][flag]] == r[i][phi[flag]] for flag in range(n) for i in range(4)
        ):
            autos.append(phi)
    if len(autos) != 96:
        raise AssertionError("tomotope automorphism count drift")

    greedy_gens: list[Perm] = []
    generated = [tuple(range(n))]
    for p in autos:
        trial = closure(greedy_gens + [p], n)
        if len(trial) > len(generated):
            greedy_gens.append(p)
            generated = trial
        if len(generated) == 96:
            break
    if set(generated) != set(autos):
        raise AssertionError("failed to generate tomotope Aut")

    metadata = {
        "flag_count": len(flags),
        "aut_order": len(autos),
        "generator_count": len(greedy_gens),
        "orbit_sizes": orbit_sizes(range(n), autos),
        "order_profile": order_profile(autos),
    }
    return autos, greedy_gens, metadata


def perm_apply6(p: tuple[int, ...], x: int) -> int:
    y = 0
    for i in range(6):
        if (x >> i) & 1:
            y |= 1 << p[i]
    return y


def compose6(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a[b[i]] for i in range(6))


def generate_s3_regular_direction_group() -> list[tuple[int, ...]]:
    def c3(a: tuple[int, int, int], b: tuple[int, int, int]) -> tuple[int, int, int]:
        return tuple(a[b[i]] for i in range(3))  # type: ignore[return-value]

    r = (1, 2, 0)
    s = (1, 0, 2)
    ident = (0, 1, 2)
    s3 = {ident}
    frontier = [ident]
    while frontier:
        cur = frontier.pop()
        for gen in (r, s):
            nxt = c3(gen, cur)
            if nxt not in s3:
                s3.add(nxt)
                frontier.append(nxt)
    ordered = sorted(s3)
    index = {g: i for i, g in enumerate(ordered)}
    dir_gens = [tuple(index[c3(gen, x)] for x in ordered) for gen in (r, s)]
    return closure6(dir_gens)


def closure6(gens: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    ident = tuple(range(6))
    group = {ident}
    frontier = [ident]
    while frontier:
        cur = frontier.pop()
        for gen in gens:
            nxt = compose6(gen, cur)
            if nxt not in group:
                group.add(nxt)
                frontier.append(nxt)
    return sorted(group)


def rank2(vectors: Iterable[int]) -> int:
    basis: list[int] = []
    for x in vectors:
        y = x
        for b in basis:
            y = min(y, y ^ b)
        if y:
            basis.append(y)
            basis.sort(reverse=True)
    return len(basis)


def span2(basis: Iterable[int]) -> frozenset[int]:
    out = {0}
    for b in basis:
        out |= {x ^ b for x in list(out)}
    return frozenset(out)


def invariant_dim4_subspaces(
    direction_group: list[tuple[int, ...]]
) -> list[frozenset[int]]:
    subspaces = set()
    for comb in combinations(range(1, 64), 4):
        if rank2(comb) == 4:
            subspaces.add(span2(comb))
    return sorted(
        [
            sub
            for sub in subspaces
            if all(
                frozenset(perm_apply6(p, x) for x in sub) == sub
                for p in direction_group
            )
        ],
        key=lambda row: sorted(row),
    )


def q6_edges() -> list[tuple[int, int, int]]:
    out = []
    for x in range(64):
        for dim in range(6):
            y = x ^ (1 << dim)
            if x < y:
                out.append((x, y, dim))
    return out


def edge_line_graph_adjacency(edges: list[tuple[int, int, int]]) -> list[set[int]]:
    adj = [set() for _ in edges]
    for i, j in combinations(range(len(edges)), 2):
        if {edges[i][0], edges[i][1]} & {edges[j][0], edges[j][1]}:
            adj[i].add(j)
            adj[j].add(i)
    return adj


def build_q6_candidate(
    tomotope_profile: dict[str, int]
) -> tuple[list[Perm], list[Perm], dict[str, object]]:
    direction_group = generate_s3_regular_direction_group()
    subspaces = invariant_dim4_subspaces(direction_group)
    edges = q6_edges()
    edge_index = {tuple(sorted((a, b))): i for i, (a, b, _d) in enumerate(edges)}

    def edge_image(
        translation: int, direction_perm: tuple[int, ...], edge: tuple[int, int, int]
    ) -> int:
        a, b, _dim = edge
        aa = perm_apply6(direction_perm, a) ^ translation
        bb = perm_apply6(direction_perm, b) ^ translation
        return edge_index[tuple(sorted((aa, bb)))]

    candidates = []
    for subspace in subspaces:
        perms = sorted(
            {
                tuple(edge_image(t, p, edge) for edge in edges)
                for t in subspace
                for p in direction_group
            }
        )
        profile = order_profile(perms)
        candidates.append(
            {
                "subspace": subspace,
                "perms": perms,
                "profile": profile,
                "orbit_sizes": orbit_sizes(range(len(edges)), perms),
            }
        )
    matching = [
        row
        for row in candidates
        if row["profile"] == tomotope_profile
        and row["orbit_sizes"] == [96, 96]
        and len(row["perms"]) == 96
    ]
    if len(matching) != 1:
        raise AssertionError(f"expected unique Q6 candidate, found {len(matching)}")
    chosen = matching[0]
    perms = list(chosen["perms"])  # type: ignore[arg-type]

    adj = edge_line_graph_adjacency(edges)
    preserves = all(
        all(
            (j in adj[i]) == (perm[j] in adj[perm[i]])
            for i in range(192)
            for j in adj[i]
        )
        for perm in perms
    )
    if not preserves:
        raise AssertionError("candidate does not preserve Q6 edge adjacency")

    gens: list[Perm] = []
    generated = [tuple(range(192))]
    for p in perms:
        trial = closure(gens + [p], 192)
        if len(trial) > len(generated):
            gens.append(p)
            generated = trial
        if len(generated) == 96:
            break
    if set(generated) != set(perms):
        raise AssertionError("failed to generate Q6 candidate")

    metadata = {
        "q6_edges": len(edges),
        "direction_group_order": len(direction_group),
        "invariant_dim4_subspaces": len(subspaces),
        "unique_matching_subspace": sorted(chosen["subspace"]),  # type: ignore[arg-type]
        "group_order": len(perms),
        "generator_count": len(gens),
        "orbit_sizes": chosen["orbit_sizes"],
        "order_profile": chosen["profile"],
        "preserves_q6_line_graph": preserves,
    }
    return perms, gens, metadata


def gap_perm_list(p: Perm) -> str:
    return "PermList([" + ",".join(str(x + 1) for x in p) + "])"


def run_gap_isomorphism(t_gens: list[Perm], q_gens: list[Perm]) -> dict[str, str]:
    script = f"""
T := Group([{','.join(gap_perm_list(p) for p in t_gens)}]);;
Q := Group([{','.join(gap_perm_list(p) for p in q_gens)}]);;
iso := IsomorphismGroups(T,Q);;
Print("tom_size=", Size(T), "\\n");
Print("q6_size=", Size(Q), "\\n");
Print("tom_id=", IdGroup(T)[1], "-", IdGroup(T)[2], "\\n");
Print("q6_id=", IdGroup(Q)[1], "-", IdGroup(Q)[2], "\\n");
Print("tom_structure=", StructureDescription(T), "\\n");
Print("q6_structure=", StructureDescription(Q), "\\n");
Print("isomorphic=", iso <> fail, "\\n");
QUIT;
"""
    gap = shutil.which("gap")
    if gap:
        proc = subprocess.run(
            [gap, "-q"],
            input=script,
            text=True,
            capture_output=True,
            check=True,
            timeout=60,
        )
        stdout = proc.stdout
    else:
        gap_bash = Path("C:/Program Files/GAP-4.15.1/runtime/bin/bash.exe")
        if not gap_bash.exists():
            raise FileNotFoundError("GAP is required for BT1368")
        tmp = ROOT / ".tmp"
        tmp.mkdir(exist_ok=True)
        gfile = tmp / "bt1368_q6_tomotope_equivariant_flag_lift.g"
        gfile.write_text(script, newline="\n")
        drive = str(gfile)[0].lower()
        rest = str(gfile)[2:].replace("\\", "/")
        cyg = f"/cygdrive/{drive}{rest}"
        proc = subprocess.run(
            [str(gap_bash), "--norc", "-c", f"/opt/gap-4.15.1/gap.exe -q -b '{cyg}'"],
            cwd=str(gap_bash.parent),
            text=True,
            capture_output=True,
            check=True,
            timeout=120,
        )
        stdout = proc.stdout
    out = {}
    for line in stdout.splitlines():
        if "=" in line:
            key, value = line.strip().split("=", 1)
            out[key] = value
    required = {
        "tom_size",
        "q6_size",
        "tom_id",
        "q6_id",
        "tom_structure",
        "q6_structure",
        "isomorphic",
    }
    missing = required - set(out)
    if missing:
        raise AssertionError(f"GAP output missing {sorted(missing)}\n{stdout}")
    return out


def build_result() -> dict[str, object]:
    tom_autos, tom_gens, tom = build_tomotope_aut_group()
    q6_autos, q6_gens, q6 = build_q6_candidate(tom["order_profile"])  # type: ignore[arg-type]
    gap = run_gap_isomorphism(tom_gens, q6_gens)

    checks = {
        "tomotope_aut_order_96": tom["aut_order"] == 96,
        "tomotope_two_regular_orbits": tom["orbit_sizes"] == [96, 96],
        "q6_candidate_order_96": q6["group_order"] == 96,
        "q6_candidate_two_regular_orbits": q6["orbit_sizes"] == [96, 96],
        "order_profiles_match": tom["order_profile"] == q6["order_profile"],
        "q6_candidate_preserves_line_graph": q6["preserves_q6_line_graph"] is True,
        "gap_identifies_isomorphic_groups": gap["isomorphic"] == "true"
        and gap["tom_size"] == "96"
        and gap["q6_size"] == "96"
        and gap["tom_id"] == gap["q6_id"],
    }

    return {
        "bt": 1368,
        "title": "Q6 tomotope equivariant flag lift",
        "verified": all(checks.values()),
        "tomotope_aut": tom,
        "q6_edge_subgroup": q6,
        "gap_witness": gap,
        "equivariant_map_certificate": {
            "carrier_size": 192,
            "orbit_pairing_count": 2,
            "construction": (
                "GAP gives Aut(tomotope) ~= G_Q6.  Both actions split the "
                "192-point carrier into two regular 96-point orbits.  After "
                "choosing an isomorphism and pairing the two orbits, each "
                "flag/edge is the unique group element sending the selected "
                "basepoint to it, giving an equivariant bijection."
            ),
        },
        "interpretation": (
            "The Q6/tomotope bridge is stronger than a shared count: Q6 has a "
            "unique S3-invariant 2^4 translation subgroup whose edge action is "
            "isomorphic to the true tomotope automorphism action on flags."
        ),
        "boundary": (
            "The visible CSV coordinate map from tomotope flags to Q6 edges is "
            "not asserted to be equivariant.  The verified map is the regular "
            "orbit-coordinate map supplied by the isomorphic group actions."
        ),
        "checks": checks,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=OUT)
    ns = ap.parse_args()
    result = build_result()
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "bt": result["bt"],
                "verified": result["verified"],
                "tomotope_id": result["gap_witness"]["tom_id"],
                "q6_id": result["gap_witness"]["q6_id"],
                "q6_orbits": result["q6_edge_subgroup"]["orbit_sizes"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
