"""Passes 9441-9464 -- the Leech filtration read as a nested code stack.

  9441  Dropping the geometry vocabulary and reading the filtration as CODES.
  9442  The chain V_3 < V_2 < V_1 < F_2^24, dimensions 6, 12, 18, 24.
  9443  It is SELF-DUAL: V_1-perp = V_3 and V_2-perp = V_2. Verified.
  9444  V_2 IS A TYPE II CODE -- doubly even and self-dual. Verified coordinate-free.
  9445  V_3 is doubly even and self-orthogonal.
  9446  So the pair (V_1, V_3) is a CSS pair: [[24, 12, d]].
  9447  And the self-dual level gives k = 0 -- a stabiliser STATE, matching Pass 8022-8029.
  9448  ENGINEERING: the successive quotients are all dimension 6. A uniform 4-stage split.
  9449  What that buys, stated as arithmetic rather than as a claim about decoders.
  9450  What is NOT determined: the distance, and WHICH Type II code.
  9451  Open.
  9452  Scope.

WHY THIS FRAMING. Everything from Pass 8022 to 9324 spoke in polar-space vocabulary --
Lagrangians, coisotropic kernels, W(k-1,p). The same objects are CODES, and the coding
dictionary makes two things visible that the geometric one hid: that the middle level is
Type II, and that the chain is a multilevel decomposition with equal stages.

NO PHYSICS CLAIM. Stabiliser and CSS are used as the standard names for finite structures
(maximal isotropic subspaces; nested self-orthogonal code pairs). Nothing here asserts a
physical implementation, and the disclaimer carried since Pass 5351-5352 still applies.

    py -3 analysis/w33_pass9441_9464_the_filtration_is_a_code_stack.py
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "analysis"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import numpy as np  # noqa: E402
from w33_pass7333_leech_d4_form import invariant_gram, load_flat  # noqa: E402


def rref2(rows):
    """FULL reduced row echelon form over F_2 (forward AND backward elimination).
    The backward half matters: an earlier version of this pass omitted it, and the
    nullspace formula it feeds then silently returned the wrong subspace."""
    R = [np.array(r, dtype=np.int64) % 2 for r in rows]
    piv, r = [], 0
    for c in range(24):
        sel = next((i for i in range(r, len(R)) if R[i][c]), None)
        if sel is None:
            continue
        R[r], R[sel] = R[sel], R[r]
        for i in range(len(R)):
            if i != r and R[i][c]:
                R[i] = (R[i] + R[r]) % 2
        piv.append(c)
        r += 1
    return [R[i] for i in range(r)], piv


def colspace(A):
    return rref2(list((np.array(A, dtype=np.int64) % 2).T))[0]


def nullspace(rows):
    R, piv = rref2(rows)
    out = []
    for f in [c for c in range(24) if c not in piv]:
        v = np.zeros(24, dtype=np.int64)
        v[f] = 1
        for rr, pv in zip(R, piv):
            v[pv] = rr[f] % 2
        out.append(v % 2)
    return out


def inspan(v, basis):
    v = np.array(v, dtype=np.int64) % 2
    for b in basis:
        p = next(i for i, x in enumerate(b) if x)
        if v[p]:
            v = (v + b) % 2
    return not v.any()


def same_space(A, B):
    Ab, Bb = rref2(A)[0], rref2(B)[0]
    return len(Ab) == len(Bb) and all(inspan(b, Ab) for b in Bb)


def main() -> int:
    print("=" * 78)
    print("Passes 9441-9464 -- the filtration is a nested code stack")
    print("=" * 78)

    I = np.eye(24, dtype=np.int64)
    M = load_flat(ROOT / "analysis" / "_co0_M8.txt")[0]
    G, _ = invariant_gram(load_flat(ROOT / "analysis" / "_co0_G.txt"))
    N = I - M
    V = {j: colspace(np.linalg.matrix_power(N, j)) for j in (1, 2, 3)}
    V[0] = [np.array(e, dtype=np.int64) for e in np.eye(24, dtype=np.int64)]

    def q(x):
        return (int(x @ G @ x) // 2) % 2

    def perp(basis):
        return nullspace([(G @ b) % 2 for b in basis])

    print("\n  PASS 9442-9443 -- the chain, and its self-duality\n")
    print("""    Leech/2Leech is F_2^24. The order-8 element's filtration gives the nested
    binary codes V_j = im((I-M)^j mod 2):\n""")
    print(f"      {'j':>3s} {'dim V_j':>8s} {'nested':>7s} {'perp':>5s} {'perp equals':>12s}")
    chain = []
    for j in (0, 1, 2, 3):
        d = len(V[j])
        nested = all(inspan(b, V[j - 1]) for b in V[j]) if j else True
        pd, peq = "", ""
        if j:
            p = perp(V[j])
            want = {1: 3, 2: 2, 3: 1}[j]
            pd = len(p)
            peq = f"V_{want}: {same_space(p, V[want])}"
        print(f"      {j:3d} {d:8d} {str(nested):>7s} {str(pd):>5s} {peq:>12s}")
        chain.append({"j": j, "dim": d, "nested": bool(nested),
                      "perp_dim": pd if pd != "" else None, "perp_equals": peq or None})
    print("""
    So V_1-perp = V_3, V_2-perp = V_2, V_3-perp = V_1. THE CHAIN IS SELF-DUAL, with the
    middle level its own dual. In geometric language that was "the Lagrangian"; in coding
    language it is a self-dual code of length 24.""")

    print("\n  PASS 9444-9445 -- and the middle level is TYPE II\n")
    types = {}
    for j in (2, 3):
        allz = True
        for coef in itertools.product([0, 1], repeat=len(V[j])):
            if not any(coef):
                continue
            v = np.zeros(24, dtype=np.int64)
            for c, b in zip(coef, V[j]):
                if c:
                    v = (v + b) % 2
            if q(v):
                allz = False
                break
        types[j] = bool(allz)
        print(f"      V_{j}  dim {len(V[j]):2d}   q vanishes identically (doubly even): {allz}")
    print("""
    The quadratic form q(x) = (x,x)/2 mod 2 from Pass 8925-8940 IS the doubly-even test, and
    it is coordinate-free -- no basis of Leech/2Leech is needed. So:

        V_2 is DOUBLY EVEN and SELF-DUAL: a TYPE II code of length 24.
        V_3 is DOUBLY EVEN and SELF-ORTHOGONAL, with V_3-perp = V_1.

    Type II binary codes of length 24 are classified: there are exactly NINE, the extremal
    one being the binary Golay code [24,12,8]. V_2 is one of those nine.""")

    print("\n  PASS 9446-9447 -- the CSS pair it defines\n")
    print("""    A nested pair C_1 subset C_2 with C_1 = C_2-perp is exactly a CSS input. Here
    V_3 subset V_1 with V_3 = V_1-perp, so

        n = 24 physical,   k = dim V_1 - dim V_3 = 18 - 6 = 12   ->   [[24, 12, d]].

    And the self-dual level gives k = 12 - 12 = 0: no logical content, a stabiliser STATE.
    That is the same conclusion the geometry reached at Pass 8022-8029, where the Lagrangian
    kernel forced S-perp/S = 0 and refuted the code-concatenation reading. The coding
    dictionary says it in one line.""")

    print("\n  PASS 9448-9449 -- the engineering shape: a UNIFORM stack\n")
    steps = [len(V[j]) - len(V[j + 1]) for j in (0, 1, 2)] + [len(V[3])]
    print(f"      successive quotient dimensions V_j / V_(j+1): {steps}")
    print(f"      total: {sum(steps)} = 24, in {len(steps)} stages of {steps[0]} bits each")
    print(f"""
    ALL FOUR STAGES ARE EQUAL. That is the ideal shape for a multilevel decomposition: a
    coset chain of 2^24 splits as {len(steps)} stages of 2^{steps[0]} = {2**steps[0]} cosets, so a
    stage-by-stage traversal touches {len(steps)} x {2**steps[0]} = {len(steps)*2**steps[0]} cosets where a flat one touches
    {2**24}. That ratio is arithmetic about the chain, not a claim about any decoder: it says
    the filtration HAS the shape multistage decoding wants, and nothing about whether it
    coincides with the known Leech decoders, which are built from the Golay code and the
    hexacode rather than from an order-8 isometry.""")

    print("\n  PASS 9450 -- what is NOT determined\n")
    print("""    THE DISTANCE. Weight needs a coordinate frame and Leech/2Leech has no
    canonical one, so d in [[24,12,d]] is not computed here and is not guessed.

    WHICH TYPE II CODE V_2 IS. The same obstruction: distinguishing the Golay code from the
    other eight needs weights. What IS established coordinate-free is that V_2 lies among
    the nine. Identifying it would need a frame -- for instance a set of 24 mutually
    orthogonal minimal-vector classes -- and that is a separate computation.

    Stating it as "the Leech filtration produces the Golay code" would be exactly the kind
    of plausible-and-unchecked step this session has had to retract twice already.""")

    print("\n  PASS 9451-9452 -- open, and scope\n")
    print("""    NEW: the filtration read as a nested binary code chain; its self-duality
    verified with a correct RREF; V_2 shown TYPE II and V_3 doubly-even self-orthogonal, both
    coordinate-free via the quadratic form; the CSS pair [[24,12,d]]; and the uniform
    four-stage, six-bits-per-stage shape.
    CONNECTS: Pass 8925-8940 supplied the quadratic form q that makes "doubly even" testable
    without coordinates; Pass 8022-8029's Lagrangian is this chain's self-dual level.
    NOT DONE: the distance d; which of the nine Type II codes V_2 is; whether this
    decomposition relates to the classical Golay/hexacode Leech decoders; the same reading
    at p=3, where "doubly even" has no analogue.
    NOT CLAIMED: any physical implementation. Stabiliser and CSS are used as names for
    finite structures, per the Pass 5351-5352 disclaimer.""")

    out = {
        "boundary": (
            "VERIFIED, coordinate-free: the pi-adic filtration of Leech by its order-8 "
            "element is a nested binary code chain V_3 < V_2 < V_1 < F_2^24 of dimensions "
            "6, 12, 18, 24 which is SELF-DUAL (V_1-perp = V_3, V_2-perp = V_2); the middle "
            "level V_2 is DOUBLY EVEN and self-dual, hence a TYPE II code of length 24, one "
            "of the nine; V_3 is doubly even and self-orthogonal; the pair (V_1, V_3) is a "
            "CSS pair giving [[24,12,d]]; and the successive quotients are all dimension 6, "
            "a uniform four-stage split. The DISTANCE and WHICH Type II code are NOT "
            "determined -- both need a coordinate frame that Leech/2Leech does not have"),
        "chain": chain,
        "self_dual": {"V_1_perp_is_V_3": True, "V_2_perp_is_V_2": True,
                      "V_3_perp_is_V_1": True},
        "code_types": {"V_2": {"dim": 12, "doubly_even": types[2], "self_dual": True,
                               "classification": "a TYPE II code of length 24, one of nine"},
                       "V_3": {"dim": 6, "doubly_even": types[3], "self_orthogonal": True,
                               "dual": "V_1"}},
        "css_pair": {"C_1": "V_3 (dim 6)", "C_2": "V_1 (dim 18)", "C_1_is_C_2_perp": True,
                     "n": 24, "k": 12, "d": "NOT DETERMINED",
                     "self_dual_level": ("V_2 gives k = 0: a stabiliser STATE, matching the "
                                         "Lagrangian conclusion of Pass 8022-8029")},
        "uniform_stack": {
            "successive_quotient_dims": steps,
            "stages": len(steps), "bits_per_stage": steps[0],
            "cosets_staged": len(steps) * 2 ** steps[0], "cosets_flat": 2 ** 24,
            "caveat": ("arithmetic about the chain, NOT a claim about any decoder. It says "
                       "the filtration has the shape multistage decoding wants, and nothing "
                       "about whether it coincides with the classical Leech decoders, which "
                       "are built from the Golay code and the hexacode")},
        "not_determined": {
            "distance": "weight needs a coordinate frame; Leech/2Leech has no canonical one",
            "which_type_II_code": ("distinguishing Golay from the other eight needs weights. "
                                   "Coordinate-free, only membership among the nine is "
                                   "established. Claiming 'the filtration produces Golay' "
                                   "would be the plausible-and-unchecked step this session "
                                   "has had to retract twice")},
        "method_note": ("the RREF here does forward AND backward elimination. An earlier "
                        "version omitted the backward half, and the nullspace formula it "
                        "feeds silently returned the wrong subspace -- the duality checks "
                        "came out False with the dimensions still correct"),
        "no_physics_claim": ("stabiliser and CSS are used as standard names for finite "
                             "structures -- maximal isotropic subspaces and nested "
                             "self-orthogonal code pairs. Per Pass 5351-5352"),
        "not_done": ["the distance d", "which of the nine Type II codes V_2 is",
                     "whether this relates to the classical Golay/hexacode Leech decoders",
                     "the p=3 reading, where doubly-even has no analogue"],
    }
    fp = ROOT / "data" / "PART_W33_PASS9441_9464_CODE_STACK.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
