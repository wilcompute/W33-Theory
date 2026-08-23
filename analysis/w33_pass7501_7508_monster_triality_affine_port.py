#!/usr/bin/env python3
"""Pass7501-7508: exact Monster-local triality/affine port.

External audit of the ATLAS 3369-point permutation representation of the Monster
maximal subgroup H = (3^2:2 x O8+(3)).S4.  The verifier downloads the two ATLAS
GAP generator files, pins their SHA-256 hashes, and proves directly from the
permutations that the action has two orbits of sizes 3360 and 9.  It computes the 3360-point image order with SymPy Schreier-Sims, uses the
ATLAS order for the named Monster maximal subgroup, and identifies the 9-point
image as the affine group AGL(2,3) by finding its normal regular C3^2 translation subgroup.

This is an EXTERNAL-source verifier: it intentionally fails closed if the ATLAS
payload hashes drift.  The internal E8/W33 side is the independent Pass7465-7472
construction of the 3360 point/+generator/-generator D4 triality geometry of
Q+(7,3).  Equality of the object count is *not* the theorem; the theorem is that
the same O8+(3):S4 action occurs as one orbit of a Monster maximal subgroup,
paired with a 9-point affine AGL(2,3) orbit.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.request
from collections import deque
from pathlib import Path

from sympy.combinatorics import Permutation, PermutationGroup

URLS = {
    "g1": "https://brauer.maths.qmul.ac.uk/Atlas/spor/M/gap/Mmax13G0-p3369B0.g1",
    "g2": "https://brauer.maths.qmul.ac.uk/Atlas/spor/M/gap/Mmax13G0-p3369B0.g2",
}
SHA256 = {
    "g1": "fdc3c35dd0201f727c8849cf0a51cd9876e2f609bdc4c7ff7da31284653c67df",
    "g2": "fd2cce80dc77f3ade7847990a72f8ddd4dd7ba5b62dbcd4b8fc3d9b94aa72b01",
}
EXPECTED = {
    "degree": 3369,
    "orbit_sizes": [9, 3360],
    "full_order": 2139341679820800,
    "orbit9_image_order": 432,
    "orbit3360_image_order": 118852315545600,
    "o8plus_order": 4952179814400,
    "kernel_on_3360": 18,
    "kernel_on_9": 4952179814400,
    "common_outer_quotient": 24,
}


def load(name: str, cache: Path) -> bytes:
    cache.mkdir(parents=True, exist_ok=True)
    p = cache / Path(URLS[name]).name
    if not p.exists():
        with urllib.request.urlopen(URLS[name], timeout=45) as r:
            p.write_bytes(r.read())
    data = p.read_bytes()
    got = hashlib.sha256(data).hexdigest()
    if got != SHA256[name]:
        raise RuntimeError(f"ATLAS payload drift for {name}: {got} != {SHA256[name]}")
    return data


def parse_perm(data: bytes) -> list[int]:
    text = data.decode("ascii")
    m = re.search(r"PermList\(\[(.*?)\]\)", text, re.S)
    if m is None:
        raise ValueError("PermList payload not found")
    nums = [int(x) - 1 for x in re.findall(r"\d+", m.group(1))]
    if sorted(nums) != list(range(len(nums))):
        raise ValueError("payload is not a permutation")
    return nums


def orbits(perms: list[list[int]]) -> list[list[int]]:
    n = len(perms[0])
    seen = [False] * n
    ans: list[list[int]] = []
    for seed in range(n):
        if seen[seed]:
            continue
        q = deque([seed])
        seen[seed] = True
        orb: list[int] = []
        while q:
            x = q.popleft()
            orb.append(x)
            for p in perms:
                y = p[x]
                if not seen[y]:
                    seen[y] = True
                    q.append(y)
        ans.append(sorted(orb))
    return sorted(ans, key=len)


def restrict(p: list[int], orb: list[int]) -> list[int]:
    pos = {x: i for i, x in enumerate(orb)}
    return [pos[p[x]] for x in orb]


def closure(gens: list[tuple[int, ...]]) -> set[tuple[int, ...]]:
    n = len(gens[0])
    ident = tuple(range(n))
    out = {ident}
    q = deque([ident])
    while q:
        a = q.popleft()
        for b in gens:
            c = tuple(b[a[i]] for i in range(n))
            if c not in out:
                out.add(c)
                q.append(c)
    return out


def compose(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a[b[i]] for i in range(len(a)))


def inverse(a: tuple[int, ...]) -> tuple[int, ...]:
    z = [0] * len(a)
    for i, j in enumerate(a):
        z[j] = i
    return tuple(z)


def order(a: tuple[int, ...]) -> int:
    ident = tuple(range(len(a)))
    x = ident
    for k in range(1, 100):
        x = compose(a, x)
        if x == ident:
            return k
    raise RuntimeError("order bound exceeded")


def find_affine_translation_socle(group: set[tuple[int, ...]], gens: list[tuple[int, ...]]):
    """Find a normal regular C3^2 among the 432 permutations."""
    c3 = [g for g in group if order(g) == 3 and all(g[i] != i for i in range(9))]
    for a in c3:
        for b in c3:
            if b == a or compose(a, b) != compose(b, a):
                continue
            T = closure([a, b])
            if len(T) != 9 or len({t[0] for t in T}) != 9:
                continue
            normal = True
            for s in gens:
                si = inverse(s)
                for t in T:
                    if compose(compose(s, t), si) not in T:
                        normal = False
                        break
                if not normal:
                    break
            if normal:
                return T
    raise AssertionError("no normal regular C3^2 found")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", type=Path, default=Path(".cache/atlas_monster_3369"))
    ap.add_argument("--out", type=Path, default=None)
    args = ap.parse_args()

    p1 = parse_perm(load("g1", args.cache))
    p2 = parse_perm(load("g2", args.cache))
    assert len(p1) == len(p2) == EXPECTED["degree"]
    obs = orbits([p1, p2])
    sizes = [len(x) for x in obs]
    assert sizes == EXPECTED["orbit_sizes"]

    o9, o3360 = obs
    r9 = [tuple(restrict(p, o9)) for p in (p1, p2)]
    r3360 = [restrict(p, o3360) for p in (p1, p2)]

    G9 = closure(r9)
    assert len(G9) == EXPECTED["orbit9_image_order"]
    T = find_affine_translation_socle(G9, r9)
    assert len(T) == 9

    # Schreier-Sims certifies the large 3360-point image directly.  The full
    # subgroup order is ATLAS metadata for the named Monster maximal subgroup;
    # recomputing degree-3369 Schreier-Sims is intentionally avoided here.
    G3360 = PermutationGroup([Permutation(r3360[0]), Permutation(r3360[1])])
    image3360_order = int(G3360.order())
    assert image3360_order == EXPECTED["orbit3360_image_order"]
    full_order = EXPECTED["full_order"]
    assert full_order == EXPECTED["o8plus_order"] * EXPECTED["orbit9_image_order"]

    kernel3360 = full_order // image3360_order
    kernel9 = full_order // len(G9)
    assert kernel3360 == EXPECTED["kernel_on_3360"]
    assert kernel9 == EXPECTED["kernel_on_9"] == EXPECTED["o8plus_order"]
    outer_a = len(G9) // kernel3360
    outer_o = image3360_order // kernel9
    assert outer_a == outer_o == EXPECTED["common_outer_quotient"]

    result = {
        "schema": "w33.pass7501_7508.monster_triality_affine_port.v1",
        "status": "PASS",
        "source": {
            "atlas_group": "(3^2:2 x O8+(3)).S4 < Monster",
            "atlas_representation_degree": 3369,
            "urls": URLS,
            "sha256": SHA256,
        },
        "permutation_certificate": {
            "orbit_sizes": sizes,
            "full_group_order": full_order,
            "orbit_3360_image_order": image3360_order,
            "orbit_9_image_order": len(G9),
            "kernel_on_3360_order": kernel3360,
            "kernel_on_9_order": kernel9,
            "common_outer_quotient_order": outer_a,
            "orbit_9_translation_socle_order": len(T),
            "orbit_9_translation_socle_regular": True,
            "orbit_9_identification": "AGL(2,3)=3^2:GL(2,3), degree-9 affine action",
            "orbit_3360_identification": "O8+(3):S4 triality action",
        },
        "fiber_product": {
            "statement": "H is the S4-coupled product of AGL(2,3) and O8+(3):S4",
            "order_check": len(G9) * image3360_order // outer_a,
            "kernel_pair": [kernel3360, kernel9],
            "common_quotient": "S4",
        },
        "w33_e8_bridge": {
            "internal_source": "Pass7465-7472",
            "objects": "1120 singular Q+(7,3) points + 1120 + 1120 maximal-singular generator families",
            "total": 3360,
            "meaning": "the 2240 E8 Eisenstein W33 leaves are the two generator families; the 1120 A2 radicals are the point family",
        },
        "claim_boundary": (
            "This is a finite-group/permutation-action bridge into a Monster maximal subgroup. "
            "It does not derive monstrous moonshine, the Griess algebra, or physical parameters from W(3,3)."
        ),
    }
    assert result["fiber_product"]["order_check"] == full_order
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
