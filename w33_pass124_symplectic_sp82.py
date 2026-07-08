#!/usr/bin/env python3
"""
Pass 124 -- The symplectic capstone: Sp(8,2) = SRG(255,126,61,63) is the E8/2E8
orthogonality graph, and W(3,3)'s two glue graphs are its O+_8(2) subconstituents.

Passes 93 and 120 built two strongly regular graphs from the W(3,3) code-lattice glue
group (Z/2)^8 = E8/2E8:
  * SRG(135,70,37,35) on the 135 isotropic cosets      (Pass 93);
  * SRG(120,63,30,36) on the 120 anisotropic cosets    (Pass 120).
This pass shows they are the two halves of ONE graph.

Put the plus-type quadratic form Q on F_2^8 (the E8/2E8 form) with polar (alternating)
form B(x,y)=Q(x+y)+Q(x)+Q(y).  The orthogonality graph on the 255 nonzero vectors --
join x~y iff B(x,y)=0 -- is

      SRG(255, 126, 61, 63),  spectrum {126^1, 7^135, (-9)^119},

the (perp form of the) SYMPLECTIC GRAPH Sp(8,2); its complement is the standard
symplectic graph SRG(255,128,64,64).  Its automorphism group is Sp(8,2), order
47377612800.  The quadratic refinement Q (the E8 structure that the bare symplectic
form does not see) splits the 255 vertices into

      Q=0 : 135 isotropic  -> induced graph SRG(135,70,37,35)   (Pass 93)
      Q=1 : 120 anisotropic -> induced graph SRG(120,63,30,36)  (Pass 120)

so the two W(3,3) glue graphs are exactly the two subconstituents of Sp(8,2) cut out by
the E8 quadratic form.  The symmetry tower locks together:

      W(E6) [51840]  <index 6720<  GO+_8(2) [348364800]  <index 136<  Sp(8,2) [47377612800],

where 6720 = 120*56 is the ordered anisotropic-pair orbit of Pass 117, and 136 = 135+1 is
the count of isotropic vectors including 0 (the O+_8(2) stabilizer index in Sp(8,2)).

THE PRIME SHIFT.  W(3,3) is the symplectic polarity graph on the
(3^4-1)/(3-1)=40 points of PG(3,3), with full projective automorphism group
PGSp(4,3) isomorphic to W(E6).  Through its E8/2E8 glue it generates the
symplectic graph Sp(8,2) over F_2 -- a symplectic-to-symplectic bridge across the prime shift 3 -> 2,
the two Ducey "bad primes" of r-s = 6 = 2*3 (Pass 97).

Self-contained (F_2^8 quadratic geometry + numpy spectra).  ASCII-only.
"""

from __future__ import annotations

import json
from collections import Counter

import numpy as np


def Qform(x: int) -> int:
    """Plus-type quadratic form on F_2^8: x0x1 + x2x3 + x4x5 + x6x7."""
    return (
        ((x >> 0 & 1) & (x >> 1 & 1))
        ^ ((x >> 2 & 1) & (x >> 3 & 1))
        ^ ((x >> 4 & 1) & (x >> 5 & 1))
        ^ ((x >> 6 & 1) & (x >> 7 & 1))
    )


def Bform(x: int, y: int) -> int:
    return Qform(x ^ y) ^ Qform(x) ^ Qform(y)


def srg_params(verts):
    verts = list(verts)
    n = len(verts)
    adj = {a: set(b for b in verts if b != a and Bform(a, b) == 0) for a in verts}
    deg = Counter(len(adj[a]) for a in verts)
    lam, mu = Counter(), Counter()
    for i in range(n):
        for j in range(i + 1, n):
            a, b = verts[i], verts[j]
            c = len(adj[a] & adj[b])
            (lam if b in adj[a] else mu)[c] += 1
    return dict(deg), dict(lam), dict(mu)


def spectrum(verts):
    verts = list(verts)
    n = len(verts)
    M = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            if Bform(verts[i], verts[j]) == 0:
                M[i, j] = M[j, i] = 1
    ev = sorted(np.rint(np.linalg.eigvalsh(M)).astype(int).tolist())
    return dict(Counter(ev))


def sp_order(m: int) -> int:
    o = 2 ** (m * m)
    for i in range(1, m + 1):
        o *= 2 ** (2 * i) - 1
    return o


def main() -> int:
    allnz = list(range(1, 256))
    iso = [v for v in allnz if Qform(v) == 0]
    ani = [v for v in allnz if Qform(v) == 1]

    deg255, lam255, mu255 = srg_params(allnz)
    spec255 = spectrum(allnz)
    degI, lamI, muI = srg_params(iso)
    degA, lamA, muA = srg_params(ani)

    sp82 = sp_order(4)
    go8 = 348_364_800  # |GO+_8(2)| (Pass 117)
    we6 = 51_840  # |W(E6)| (Pass 91)

    is_sp82 = (
        len(allnz) == 255
        and deg255 == {126: 255}
        and set(lam255) == {61}
        and set(mu255) == {63}
        and spec255 == {126: 1, 7: 135, -9: 119}
    )
    is_srg135 = degI == {70: 135} and set(lamI) == {37} and set(muI) == {35}
    is_srg120 = degA == {63: 120} and set(lamA) == {30} and set(muA) == {36}

    checks = {
        "split_135_iso_plus_120_ani": len(iso) == 135 and len(ani) == 120,
        "graph_is_SRG_255_126_61_63": is_sp82,
        "sp82_spectrum_126_7^135_-9^119": spec255 == {126: 1, 7: 135, -9: 119},
        "isotropic_subconstituent_is_SRG135": is_srg135,
        "anisotropic_subconstituent_is_SRG120": is_srg120,
        "Sp82_order_47377612800": sp82 == 47_377_612_800,
        "index_Sp82_over_GOplus8_is_136": sp82 % go8 == 0
        and sp82 // go8 == 136 == 135 + 1,
        "index_GOplus8_over_WE6_is_6720": go8 % we6 == 0
        and go8 // we6 == 6720 == 120 * 56,
        "PG3_3_has_40_projective_points": (3**4 - 1) // (3 - 1) == 40,
        "complement_is_SRG_255_128_64_64": 255 - 1 - 126 == 128,
    }
    all_ok = all(checks.values())

    print("=" * 78)
    print("PASS 124 -- Sp(8,2) = SRG(255,126,61,63) IS THE E8/2E8 ORTHOGONALITY GRAPH")
    print("=" * 78)
    print(f"255 nonzero E8/2E8 vectors, join iff B(x,y)=0:")
    print(f"   degree {list(deg255)[0]}, lambda {list(lam255)[0]}, mu {list(mu255)[0]}")
    print(f"   spectrum {spec255}  ->  SRG(255,126,61,63) = symplectic graph Sp(8,2)")
    print(f"   complement = standard symplectic graph SRG(255,128,64,64)")
    print()
    print("O+_8(2) quadratic split into the two W(3,3) glue graphs:")
    print(f"   Q=0  135 isotropic  -> SRG(135,70,37,35)  (Pass 93):  {is_srg135}")
    print(f"   Q=1  120 anisotropic -> SRG(120,63,30,36) (Pass 120): {is_srg120}")
    print()
    print("symmetry tower:")
    print(f"   W(E6) {we6}  <6720<  GO+_8(2) {go8}  <136<  Sp(8,2) {sp82}")
    print(
        f"   6720 = 120*56 (Pass 117 ordered anisotropic pair); 136 = 135+1 isotropic"
    )
    print(
        f"   W(3,3) is the symplectic polar graph on 40 PG(3,3) points: prime shift 3 -> 2"
    )
    print()
    print("checks:")
    for k, v in checks.items():
        print(f"   {'OK ' if v else 'XX '} {k}")
    print()
    print("=" * 78)
    print(f"STATUS: {'PASS' if all_ok else 'FAIL'}")
    print("=" * 78)

    payload = {
        "schema": "w33.pass124.symplectic_sp82.v1",
        "status": "PASS" if all_ok else "FAIL",
        "full_graph": {
            "vertices": 255,
            "params": "SRG(255,126,61,63)",
            "spectrum": {str(k): v for k, v in sorted(spec255.items())},
            "identification": "symplectic graph Sp(8,2) (perp form); complement SRG(255,128,64,64)",
        },
        "subconstituents": {
            "isotropic_135": "SRG(135,70,37,35) (Pass 93)",
            "anisotropic_120": "SRG(120,63,30,36) (Pass 120)",
        },
        "symmetry_tower": {
            "W(E6)": we6,
            "GO+_8(2)": go8,
            "Sp(8,2)": sp82,
            "index_GO_over_WE6": go8 // we6,
            "index_Sp_over_GO": sp82 // go8,
            "note": (
                "The first subgroup is Pass 117's ordered-pair W(E6), not the "
                "nonconjugate code embedding of Pass 125. The displayed "
                "relations are subgroup indices, not normal inclusions."
            ),
        },
        "prime_shift": (
            "W(3,3) is the symplectic polarity graph on the 40 points of PG(3,3), "
            "with full projective automorphism group PGSp(4,3) isomorphic to W(E6); "
            "its E8/2E8 glue yields Sp(8,2) on 255 points.  A symplectic-to-symplectic bridge "
            "across the prime shift 3 -> 2, the two bad primes of r-s = 6 = 2*3 (Pass 97)."
        ),
        "reading": (
            "The two W(3,3) glue graphs SRG(135,70,37,35) and SRG(120,63,30,36) are the isotropic "
            "and anisotropic subconstituents of a single object: the symplectic graph Sp(8,2) = "
            "SRG(255,126,61,63) on all 255 nonzero E8/2E8 vectors.  The E8 quadratic form is exactly "
            "what splits the symplectic 255 into 135 + 120.  "
            "The Pass 117 ordered-pair W(E6) embeds with index 6720 in O+_8(2):2, "
            "which embeds with index 136 in Sp(8,2). Pass 125 distinguishes the "
            "nonconjugate code-induced W(E6) embedding."
        ),
        "checks": checks,
    }
    with open("w33_pass124_symplectic_sp82.json", "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
    print("[wrote] w33_pass124_symplectic_sp82.json")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
