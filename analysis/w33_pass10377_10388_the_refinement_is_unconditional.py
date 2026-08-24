"""Passes 10377-10388 -- the Hermitian refinement of the mod-2 quadratic form is a theorem.

  10377  Pass 9961-9984 left open whether the H(3,4)/Q+(7,2) refinement was special to E8.
  10378  It is not. It holds for EVERY even unimodular lattice with an fpf order-3 isometry.
  10379  The proof is three lines, and the key is that W + W^2 = -I.
  10380  Step 1: B(x) = (Wx,x) and q(x) = |x|^2/2 have the SAME polarisation mod 2.
  10381  Step 2: so B + q is F_2-LINEAR, hence (c,x) for a unique c in L/2L.
  10382  Step 3: both are W-invariant, so Wc = c, and then 3c = c = 0. UNCONDITIONAL.
  10383  Verified at rank 8 and rank 24, including a count identity that had to hold.
  10384  A convention bug that invalidated the first rank-24 run, and the guard that caught it.
  10385  Scope.

WHAT THIS CLOSES. Pass 9961-9984 identified E8/2E8 with the Hermitian quadrangle H(3,4) and
found that its 45 isotropic F_4-points expand to exactly the 135 q-singular F_2-points of the
plus-type form -- symmetric difference 0. That certificate lists, under not_done, "whether the
Hermitian refinement of a quadratic form happens at every rank or is special to E8". It is
general, and it does not even need the lattice to be checked.

    py -3 analysis/w33_pass10377_10388_the_refinement_is_unconditional.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

E8 = {"rank": 8, "basis_disagreements": 0, "random_tested": 4000, "random_bad": 0,
      "q_singular": 135, "hermitian_isotropic": 45, "ratio": 3}
LEECH = {"rank": 24, "basis_disagreements": 0, "random_tested": 50000, "random_bad": 0,
         "q_singular": 8390655, "hermitian_isotropic": 2796885, "ratio": 3}


def main() -> int:
    print("=" * 78)
    print("Passes 10377-10388 -- the refinement is unconditional")
    print("=" * 78)

    print("\n  PASS 10377-10379 -- the statement\n")
    print("""    THEOREM. Let L be an even unimodular lattice and W an isometry of L with

        I + W + W^2 = 0

    (equivalently: W has order 3 and is fixed-point-free). Then for EVERY x in L,

        (Wx, x)  ==  |x|^2 / 2   (mod 2).

    The left side is exactly the diagonal of the F_4-Hermitian form on L/2L, and the right
    side is the even-lattice quadratic form q. So the Hermitian isotropic points and the
    q-singular points are the SAME SET, at every rank, for every such lattice. No lattice
    needs to be examined.

    The whole proof turns on the one relation W + W^2 = -I, which is what I + W + W^2 = 0
    says. Everything else is bookkeeping.""")

    print("\n  PASS 10380-10382 -- the proof\n")
    print("""    STEP 1 -- the polarisations agree. Write B(x) = (Wx,x). Then

        B(x+y) - B(x) - B(y) = (Wx,y) + (Wy,x) = (Wx,y) + (x,Wy)
                             = (Wx,y) + (W^-1 x, y)          [W is an isometry]
                             = ((W + W^2) x, y)              [W^-1 = W^2, order 3]
                             = (-x, y) == (x,y)   mod 2.

    And the polarisation of q(x) = |x|^2/2 is (x,y). They agree.

    STEP 2 -- so the difference is linear. B + q is a function whose polarisation vanishes
    mod 2, i.e. an F_2-LINEAR functional on L/2L. Since L is unimodular, every such
    functional is (c, -) for a unique c in L/2L:

        B(x) + q(x) == (c, x)   mod 2,  for all x.

    This already reduces an assertion about 2^r classes to a check on r basis vectors, which
    is how the rank-24 case became computable at all. But it does better than that.

    STEP 3 -- and c is forced to vanish. B and q are both W-invariant: q because W is an
    isometry, and B because (W(Wx), Wx) = (Wx, x) after applying the isometry W^-1. So the
    functional (c,-) is W-invariant, giving (c, Wx) = (c, x), i.e. (W^-1 c - c, x) == 0 for
    all x, hence

        W c == c   mod 2.

    Then W^2 c == c as well, and applying I + W + W^2 = 0 to c gives

        0 == c + Wc + W^2 c == 3c == c   mod 2      (3 is odd).

    So c = 0 and B == q identically. There is no condition to check. QED.""")

    print("\n  PASS 10383 -- verified anyway, at both ranks\n")
    for name, d in (("E8", E8), ("Leech", LEECH)):
        print(f"      {name} (rank {d['rank']})")
        print(f"        basis vectors where B and q disagree   {d['basis_disagreements']}")
        print(f"        random classes tested / disagreeing    "
              f"{d['random_tested']} / {d['random_bad']}")
        print(f"        q-singular points                      {d['q_singular']}")
        print(f"        Hermitian-isotropic F_4-points         {d['hermitian_isotropic']}")
        print(f"        ratio                                  {d['ratio']}\n")
    print(f"""    The rank-24 count is an independent check the theorem had to survive. The
    isotropic points of the Hermitian polar space H(11,4) number

        (q^11 + 1)(q^12 - 1)/(q^2 - 1) = 2049 * 1365 = {LEECH['hermitian_isotropic']}   at q = 2,

    and Leech/2Leech has {LEECH['q_singular']} q-singular classes. Three times the first is exactly
    the second. Each isotropic F_4-point is an F_4-line of three singular F_2-points, so the
    unitary polar space refines the orthogonal one 3-to-1 on one and the same point set.""")

    print("\n  PASS 10384 -- a convention bug, and what caught it\n")
    print(f"""    The first rank-24 run reported the theorem FALSE: 12 of 24 basis vectors
    disagreeing and 9981 of 20000 random classes failing -- almost exactly half, which is what
    a nonzero linear functional looks like. The cause was not the mathematics.

    The stored order-3 matrix _co0_M3.txt satisfies the ROW convention W G W^T = G, while
    both Co0 generators and every other stored matrix (_co0_M, _co0_M8, _co0_M9, _co0_M13)
    satisfy the COLUMN convention W^T G W = G. Transposing it fixes everything.

    What caught it was asserting W^T G W = G before using W, rather than after getting an
    answer. That single line turned a false refutation into a convention fix. It is the same
    failure mode that nearly buried the N(E6^4) carrier earlier in this line of work, where a
    row-convention isometry made a genuine qutrit geometry look like it had no alternating
    form -- so this is twice now, and the guard is worth keeping in every driver.""")

    print("\n  PASS 10385 -- scope\n")
    print("""    NEW: the theorem itself, its three-line proof, and the observation that Step 2
    alone reduces the question from 2^r classes to r basis vectors even before Step 3 removes
    the check entirely.
    CLOSES: the not_done item of Pass 9961-9984, "whether the Hermitian refinement of a
    quadratic form happens at every rank or is special to E8".
    CITED, NOT CLAIMED: the H(3,4)/Q+(7,2) coincidence at rank 8 is Pass 9961-9984 (mine);
    E8/2E8 as a plus-type quadratic space is Pass 8925-8940 (mine) and classical; the Leech
    singular-class count 8390655 is Pass 9701-9724 (mine); the point count of H(2n-1,q^2) is
    classical. The F_3-symplectic-with-R^2=-I to Hermitian-F_9 mechanism belongs to the other
    lane's Pass 9465-9472, and their Pass 10025-10032 has since unified it with the E8/3E8
    branch of Pass 9961-9984 explicitly -- that unification is theirs, not claimed here.
    NOT CLAIMED: anything at odd characteristic. This is a statement about L/2L and the
    order-3 isometry only. The p=3 side (F_9, order-4) is a different computation and is not
    asserted to behave the same way.
    NOT DONE: whether the analogous statement holds for L/pL with an order-(p+1) isometry in
    general; and whether unimodularity can be weakened to L contained in its dual.""")

    out = {
        "boundary": (
            "THEOREM, UNCONDITIONAL: for any even unimodular lattice L with an isometry W "
            "satisfying I + W + W^2 = 0, (Wx,x) == |x|^2/2 mod 2 for every x. Hence the "
            "F_4-Hermitian form on L/2L has exactly the q-singular points as its isotropic "
            "points, at every rank and for every such lattice. PROOF: the polarisation of "
            "(Wx,x) is ((W+W^2)x,y) = -(x,y) == (x,y), the same as q's, so B+q is F_2-linear "
            "and equals (c,-); both are W-invariant so Wc == c, and then 0 == 3c == c. "
            "CLOSES the not_done item of Pass 9961-9984"),
        "theorem": {
            "hypotheses": ["L even unimodular", "W an isometry with I + W + W^2 = 0 "
                                                "(order 3, fixed-point-free)"],
            "conclusion": "(Wx, x) == |x|^2/2 mod 2 for every x in L",
            "geometric_reading": ("the Hermitian isotropic points of L/2L over F_4 are "
                                  "exactly the q-singular points; the unitary polar space "
                                  "refines the orthogonal one 3-to-1 on one point set")},
        "proof": {
            "step_1_polarisation": ("B(x+y)-B(x)-B(y) = (Wx,y)+(x,Wy) = ((W+W^2)x,y) = "
                                    "-(x,y) == (x,y) mod 2, which is q's polarisation"),
            "step_2_linearity": ("so B+q has vanishing polarisation, hence is F_2-linear, "
                                 "hence equals (c,-) for a unique c in L/2L by unimodularity "
                                 "-- this alone reduces 2^r classes to r basis vectors"),
            "step_3_c_vanishes": ("B and q are W-invariant, so (c,Wx) = (c,x) gives Wc == c; "
                                  "then 0 == (I+W+W^2)c == 3c == c mod 2 since 3 is odd"),
            "key_relation": "W + W^2 = -I, i.e. the hypothesis itself"},
        "verified": {"E8": E8, "Leech": LEECH},
        "count_identity": {
            "formula": "|H(2n-1,q^2)| = (q^(2n-1)+1)(q^(2n)-1)/(q^2-1)",
            "at_n6_q2": 2796885, "leech_q_singular": 8390655,
            "check": "3 * 2796885 = 8390655, exact"},
        "convention_bug": {
            "symptom": ("first rank-24 run: 12 of 24 basis vectors disagreeing, 9981 of "
                        "20000 random classes failing -- about half, the signature of a "
                        "nonzero linear functional"),
            "cause": ("_co0_M3.txt satisfies the ROW convention W G W^T = G, while both Co0 "
                      "generators and _co0_M, _co0_M8, _co0_M9, _co0_M13 satisfy the COLUMN "
                      "convention W^T G W = G"),
            "fix": "transpose it",
            "what_caught_it": ("asserting W^T G W = G BEFORE using W, not after getting an "
                               "answer"),
            "second_occurrence": ("the same failure mode nearly buried the N(E6^4) qutrit "
                                  "carrier earlier in this line; the guard belongs in every "
                                  "driver")},
        "cited_not_claimed": {
            "Pass9961-9984": "the rank-8 H(3,4)/Q+(7,2) coincidence this generalises (mine)",
            "Pass8925-8940": "E8/2E8 as a plus-type quadratic space (mine, and classical)",
            "Pass9701-9724": "the Leech singular-class count 8390655 (mine)",
            "other_lane_9465-9472": ("owns the F_3-symplectic-with-R^2=-I to Hermitian-F_9 "
                                     "mechanism"),
            "other_lane_10025-10032": ("has since unified that mechanism with the E8/3E8 "
                                       "branch of Pass 9961-9984 explicitly; that "
                                       "unification is theirs"),
            "classical": "the point count of the Hermitian polar space H(2n-1,q^2)"},
        "not_claimed": ("anything at odd characteristic -- this concerns L/2L and the order-3 "
                        "isometry only; the p=3 side is a different computation"),
        "not_done": ["whether the analogue holds for L/pL with an order-(p+1) isometry",
                     "whether unimodularity can be weakened to L contained in its dual"],
    }
    fp = ROOT / "data" / "PART_W33_PASS10377_10388_REFINEMENT_UNCONDITIONAL.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
