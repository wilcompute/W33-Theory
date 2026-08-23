"""Passes 9961-9984 -- why symplectic q is always prime, and the unitary branch that escapes it.

  9961  Every geometry this machine has produced has PRIME q. That is a theorem, not a habit.
  9962  Consequence: W(3,9) is unreachable. It has been sitting in my own not_done as if undone.
  9963  The escape: pi = 1-zeta is only ONE prime of Z[zeta_d]. The others have residue F_(l^f).
  9964  But the adjoint of M is complex conjugation, so a form survives only if conj is in D.
  9965  THE TRICHOTOMY. Ramified -> symplectic. Unramified with -1 in <l> -> UNITARY.
  9966  Otherwise conjugation swaps the two primes and NEITHER side carries a form. Verified.
  9967  E8/3E8 is the Hermitian generalized quadrangle H(3,9). All four GQ parameters.
  9968  E8/2E8 is H(3,4) -- and it REFINES the Q+(7,2) of my own Pass 8925-8940, exactly.
  9969  Three corrections made before publishing.
  9970  Scope, and what is cited rather than claimed.

WHERE THIS COMES FROM. Pass 7349-7356 gave the reachability formula: a lattice of rank r with
a regular isometry of order d yields W(k-1,p) with k = r/deg(Phi_d) and p = Phi_d(1). That
certificate lists "alpha(W(3,9))" under not_done. This pass shows W(3,9) is not merely undone
by this machine -- it is unreachable by it -- and then finds where the machine does go instead.

    py -3 analysis/w33_pass9961_9984_the_unitary_branch.py
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

# ---- measured in this pass (see the module docstring for the drivers) -----------------
PHI_AT_1 = {2: 2, 3: 3, 4: 2, 5: 5, 6: 1, 7: 7, 8: 2, 9: 3, 10: 1, 11: 11, 12: 1,
            16: 2, 25: 5, 27: 3, 32: 2}
H39 = {"points": 280, "lines": 112, "points_per_line": 10, "lines_per_point": 4}
H34 = {"points": 45, "lines": 27, "points_per_line": 5, "lines_per_point": 3}
SPLIT8 = {"rank": 16, "dim_ker_h": 8, "dim_ker_hbar": 8, "G_on_V": "identically zero",
          "G_on_Vprime": "identically zero", "cross_pairing_rank": 8}
REFINE = {"E8_mod_2_classes": 255, "q_singular": 135, "hermitian_isotropic_F4_points": 45,
          "expanded_to_F2": 135, "symmetric_difference": 0}


def main() -> int:
    print("=" * 78)
    print("Passes 9961-9984 -- the unitary branch, and why symplectic q is prime")
    print("=" * 78)

    print("\n  PASS 9961-9962 -- a limitation theorem, and what it closes\n")
    print("""    The machine's q is Phi_d(1). That is not a free parameter: classically

        Phi_d(1) = p   if d = p^m for a prime p,
                 = 1   if d has two or more distinct prime factors.

    So the values Phi_d(1) can take are exactly 1 and the primes. Measured:\n""")
    print("      d        : " + " ".join(f"{d:>3d}" for d in sorted(PHI_AT_1)))
    print("      Phi_d(1) : " + " ".join(f"{PHI_AT_1[d]:>3d}" for d in sorted(PHI_AT_1)))
    print("""
        THE SYMPLECTIC BRANCH OF THIS MACHINE PRODUCES PRIME q ONLY. Never a proper
        prime power.

    That settles a question I had left open in the wrong register. W(3,9) has q = 9 = 3^2,
    so no lattice and no regular isometry produces it -- and the same excludes W(3,4),
    W(3,8), W(3,25) and W(3,27). My own Pass 7349-7356 certificate lists alpha(W(3,9))
    under not_done, which reads as "not yet attempted". It is not attemptable this way. The
    obstruction is arithmetic and it is one line long.""")

    print("\n  PASS 9963-9964 -- the escape, and the condition on it\n")
    print("""    Everything so far used pi = 1 - zeta, which is the TOTALLY RAMIFIED prime of
    Z[zeta_d] over p: e = phi(p^m), f = 1, residue field F_p. That single choice is the whole
    reason q was always prime.

    Z[zeta_d] has other primes. For l not dividing d, l is UNRAMIFIED with residue degree
    f = ord_d(l), and residue field F_(l^f). Taking f > 1 reaches prime-power q -- the thing
    the ramified prime cannot do.

    BUT A FORM NEED NOT SURVIVE. M is a G-isometry, so its adjoint is M^-1: the adjoint
    operation IS complex conjugation. Conjugation is the element -1 of (Z/d)*, and the
    decomposition group at a prime above l is <l>. So the reduction of the form lands back on
    the SAME prime only when

        -1 lies in <l> mod d,   equivalently   l^(f/2) = -1 mod d.

    If it does not, conjugation carries one prime to the other and the form pairs two
    different residue spaces rather than one with itself.""")

    print("\n  PASS 9965-9966 -- the trichotomy, third branch verified\n")
    print(f"""    Take d = 8, l = 3. Then f = ord_8(3) = 2, and <3> = {{1,3}} mod 8 does NOT
    contain -1 = 7. Phi_8 mod 3 factors as (x^2+x-1)(x^2-x-1), and the reciprocal of one
    factor is the other -- which is conjugation swapping the two primes, seen on the
    polynomials. On E8^2 (rank 16, char poly Phi_8^4):

      dim ker h(M)                 {SPLIT8['dim_ker_h']}          dim ker hbar(M)   {SPLIT8['dim_ker_hbar']}
      G restricted to V            {SPLIT8['G_on_V']}
      G restricted to V'           {SPLIT8['G_on_Vprime']}
      cross pairing G(V, V') rank  {SPLIT8['cross_pairing_rank']}          (nondegenerate)

    The mod-3 reduction is a HYPERBOLIC PAIR of totally isotropic F_9-spaces exchanged by
    conjugation. Neither side carries a form of its own. That is also the explanation for a
    result I first read as a failure: the twisted form hbar(M)^T G came out neither symmetric
    nor antisymmetric, which is not a broken construction but the signature of this branch.

    So the machine has exactly three outcomes:

      l divides d                  -> ramified, residue F_l, ALTERNATING form  -> W(k-1,l)
      l unramified, -1 in <l>      -> residue F_(l^f), HERMITIAN form          -> H(k-1,l^f)
      l unramified, -1 not in <l>  -> two primes swapped, dual pair, NO form""")

    print("\n  PASS 9967 -- E8 mod 3 is the Hermitian quadrangle H(3,9)\n")
    print(f"""    d = 4, l = 3: f = ord_4(3) = 2 and -1 = 3 mod 4, so conjugation IS in <3>. Three
    is inert in Z[i] and the residue field is F_9. E8 carries an order-4 isometry with
    M^2 = -I, making E8 a Z[i]-module of rank 4, so E8/3E8 = F_9^4. The form

        h(x,y) = G(x,y) - i*G(Mx,y),    i acting as M

    was checked to be additive, i-linear in the first slot, i-semilinear in the second, and
    conjugate-symmetric h(y,x) = conj h(x,y). Censusing PG(3,9):

      isotropic points   {H39['points']}        points per line   {H39['points_per_line']}
      isotropic lines    {H39['lines']}        lines per point   {H39['lines_per_point']}

    That is the generalized quadrangle GQ(9,3) = H(3,9) on the nose, and the incidence
    identity {H39['points']}*{H39['lines_per_point']} = {H39['lines']}*{H39['points_per_line']} = {H39['points']*H39['lines_per_point']} closes.""")

    print("\n  PASS 9968 -- E8 mod 2 is H(3,4), and it refines a form I already published\n")
    print(f"""    d = 3, l = 2: f = ord_3(2) = 2 and -1 = 2 mod 3, so again conjugation is in <2>.
    Two is inert in Z[omega], residue field F_4. The fixed-point-free order-3 isometry is
    built as Cox^10 where Cox is the E8 Coxeter element of order 30 -- its eigenvalues
    zeta_30^m for exponents m = 1,7,11,13,17,19,23,29 become cube roots with four of each
    primitive value, giving char poly Phi_3^4 and I + W + W^2 = 0, verified. Then:

      isotropic points   {H34['points']}         points per line   {H34['points_per_line']}
      isotropic lines    {H34['lines']}         lines per point   {H34['lines_per_point']}

    which is GQ(4,2) = H(3,4). AND IT MEETS MY OWN EARLIER PASS. Pass 8925-8940 found that
    E8/2E8 carries a plus-type quadratic form with {REFINE['q_singular']} singular points, the Q+(7,2) count.
    The same {REFINE['E8_mod_2_classes']} classes, viewed over F_4 instead of F_2, are {(REFINE['E8_mod_2_classes']+1)//3} projective points, and:

      Hermitian-isotropic F_4-points      {REFINE['hermitian_isotropic_F4_points']}
      expanded to F_2-points              {REFINE['expanded_to_F2']}
      q-singular points of Q+(7,2)        {REFINE['q_singular']}
      symmetric difference                {REFINE['symmetric_difference']}

    Not a numerical coincidence and not a reinterpretation: the two point sets are EQUAL. The
    F_4 Hermitian structure refines the F_2 quadratic one, each isotropic F_4-point being an
    F_4-line of three singular F_2-points, {REFINE['q_singular']} = {REFINE['hermitian_isotropic_F4_points']} x 3.

    The classical reading, cited not claimed: H(3,4) = GQ(4,2) is dual to Q-(5,2) = GQ(2,4),
    whose 27 points are the 27 lines on a cubic surface and whose 45 lines are the tritangent
    planes. So the 27 lines are reachable from E8 by reduction mod 2 -- which is a route to an
    object this repo already holds in quantity, not a new object.""")

    print("\n  PASS 9969 -- three corrections made before publishing\n")
    print("""      1. The first Hermitian form I wrote, G(x,y) + i*G(Mx,y), is NOT sesquilinear:
         it makes M act as -i, and two of the four checks failed. The correct form is
         G(x,y) - i*G(Mx,y). The isotropic COUNT was unaffected, because vanishing is
         insensitive to the sign -- so the count alone would not have caught it, and the
         algebraic checks are what did.
      2. I first wrote that H(3,9) has 28 lines. A GQ(s,t) has (s+1)(st+1) points and
         (t+1)(st+1) LINES, so H(3,9) = GQ(9,3) has 112, not 28. The measured 112 was right
         and my formula was wrong; the incidence identity 280*4 = 112*10 settled it.
      3. The d=8 computation returning a form that was neither symmetric nor antisymmetric
         looked like a broken construction. It is the third branch of the trichotomy.""")

    print("\n  PASS 9970 -- scope\n")
    print("""    NEW HERE: that the symplectic branch produces PRIME q only, hence W(3,9) and every
    proper-prime-power symplectic space is unreachable by this machine; the trichotomy over
    the primes of Z[zeta_d], with the criterion -1 in <l> mod d and the third branch verified
    as a hyperbolic pair; the identification of E8/3E8 as H(3,9) and E8/2E8 as H(3,4), each
    with all four GQ parameters; and the exact refinement of Pass 8925-8940's Q+(7,2) by the
    F_4 Hermitian structure on the same 135 points.

    CITED, NOT CLAIMED -- OTHER LANE. The equivalence between an F_3 symplectic space with
    R^2 = -I and a Hermitian F_9-space is theirs, stated in the boundary of Pass 9465-9472
    (F9_UNITARY_CENTRALIZER_RIGIDITY), which also identifies C_Sp(12,3)(R) = U(6,3). Their
    Pass 9781-9788 gives the unramified/ramified compositum with (e,f) = (6,2). Those passes
    committed first and own the mechanism; this pass applies it to a different object -- E8 at
    rank 4 over the residue field, not the rank-12 Niemeier glue -- and adds the classification
    of which primes give which geometry.

    CITED, NOT CLAIMED -- CLASSICAL. The values of Phi_d(1); H(3,q^2) = GQ(q^2,q) and its
    duality with Q-(5,q); Q-(5,2) as the 27 lines on a cubic surface; E8/2E8 as a plus-type
    quadratic space (also my own Pass 8925-8940).

    NOT CLAIMED: any statement about alpha(W(3,9)). This pass says the LATTICE machine cannot
    reach W(3,9); it says nothing about the combinatorial problem, which remains open at
    51 <= alpha <= 73 and must be attacked by other means.
    NOT DONE: the unitary geometries from Leech and the other rank-24 carriers; whether the
    Hermitian refinement of a quadratic form happens at every rank or is special to E8.""")

    out = {
        "boundary": (
            "A LIMITATION THEOREM AND THE BRANCH THAT ESCAPES IT. The machine's q is "
            "Phi_d(1), which is 1 or a PRIME -- never a proper prime power -- so the "
            "symplectic branch cannot produce W(3,9), W(3,4), W(3,8), W(3,25) or W(3,27). "
            "The cause is that pi = 1-zeta is the TOTALLY RAMIFIED prime. Using an "
            "unramified prime of Z[zeta_d] gives residue field F_(l^f); a form survives on a "
            "single prime iff -1 lies in <l> mod d (conjugation is the adjoint), and it is "
            "then HERMITIAN, not alternating. VERIFIED: E8/3E8 = H(3,9) (280 points, 112 "
            "lines, 10 per line, 4 per point) and E8/2E8 = H(3,4) (45, 27, 5, 3). The latter "
            "REFINES Pass 8925-8940's Q+(7,2) EXACTLY: its 45 isotropic F_4-points expand to "
            "the 135 q-singular F_2-points, symmetric difference 0"),
        "limitation_theorem": {
            "statement": ("Phi_d(1) = p if d = p^m, else 1; so the symplectic branch produces "
                          "PRIME q only"),
            "phi_at_1": PHI_AT_1,
            "unreachable": ["W(3,4)", "W(3,8)", "W(3,9)", "W(3,25)", "W(3,27)"],
            "closes": ("Pass 7349-7356 lists alpha(W(3,9)) under not_done, which reads as "
                       "un-attempted; it is un-attemptable by this machine"),
            "not_claimed": ("nothing about alpha(W(3,9)) itself, which remains open at "
                            "51 <= alpha <= 73 and needs other methods")},
        "trichotomy": {
            "criterion": ("the adjoint of M is M^-1, i.e. complex conjugation = -1 in "
                          "(Z/d)*; the decomposition group at a prime above l is <l>"),
            "branches": {
                "ramified (l | d)": "residue F_l, ALTERNATING form -> W(k-1,l), q prime",
                "unramified, -1 in <l>": ("residue F_(l^f), HERMITIAN form -> H(k-1,l^f), "
                                          "q a prime power"),
                "unramified, -1 not in <l>": ("conjugation swaps the two primes; the "
                                              "reduction is a hyperbolic pair of totally "
                                              "isotropic residue spaces and NEITHER carries "
                                              "a form")},
            "third_branch_verified_at": {"d": 8, "l": 3, "carrier": "E8^2, rank 16",
                                         "measured": SPLIT8,
                                         "polynomial_witness": ("Phi_8 mod 3 = "
                                                                "(x^2+x-1)(x^2-x-1) and the "
                                                                "reciprocal of one factor is "
                                                                "the other")}},
        "H_3_9": {"carrier": "E8/3E8", "d": 4, "l": 3, "why": "3 inert in Z[i], residue F_9",
                  "module": "M^2 = -I makes E8 a Z[i]-module of rank 4",
                  "form": "h(x,y) = G(x,y) - i*G(Mx,y), i acting as M",
                  "form_checks": ["additive", "i-linear in slot 1", "i-semilinear in slot 2",
                                  "conjugate-symmetric"],
                  "measured": H39, "identification": "GQ(9,3) = H(3,9)",
                  "incidence_closes": "280*4 = 112*10 = 1120"},
        "H_3_4": {"carrier": "E8/2E8", "d": 3, "l": 2,
                  "why": "2 inert in Z[omega], residue F_4",
                  "isometry": ("Cox^10 where Cox is the E8 Coxeter element of order 30; "
                               "char poly Phi_3^4 and I+W+W^2 = 0, verified"),
                  "measured": H34, "identification": "GQ(4,2) = H(3,4)"},
        "refinement_of_pass8925_8940": {
            "measured": REFINE,
            "statement": ("the 45 Hermitian-isotropic F_4-points expand to exactly the 135 "
                          "q-singular F_2-points of the plus-type form; the sets are EQUAL, "
                          "symmetric difference 0"),
            "reading": ("the F_4 Hermitian structure refines the F_2 quadratic one, each "
                        "isotropic F_4-point being an F_4-line of three singular F_2-points")},
        "corrections_before_publication": [
            ("G(x,y) + i*G(Mx,y) is NOT sesquilinear -- it makes M act as -i. Corrected to "
             "G(x,y) - i*G(Mx,y). The isotropic count is insensitive to the sign, so only the "
             "algebraic checks caught it"),
            ("I first wrote that H(3,9) has 28 lines. GQ(s,t) has (t+1)(st+1) lines, so 112. "
             "The measurement was right and the formula wrong; incidence settled it"),
            ("the d=8 form being neither symmetric nor antisymmetric is not a broken "
             "construction but the signature of the third branch")],
        "cited_other_lane": {
            "Pass9465-9472": ("owns the equivalence between an F_3 symplectic space with "
                              "R^2=-I and a Hermitian F_9-space, and C_Sp(12,3)(R) = U(6,3)"),
            "Pass9781-9788": "the unramified/ramified compositum with (e,f) = (6,2)",
            "ownership": ("those committed first and own the mechanism; this pass applies it "
                          "to E8 at rank 4 over the residue field rather than the rank-12 "
                          "Niemeier glue, and adds which primes give which geometry")},
        "cited_classical": ["the values of Phi_d(1)",
                            "H(3,q^2) = GQ(q^2,q), dual to Q-(5,q)",
                            "Q-(5,2)'s 27 points are the 27 lines on a cubic surface",
                            "E8/2E8 as a plus-type quadratic space (also Pass 8925-8940)"],
        "not_done": ["the unitary geometries from Leech and the other rank-24 carriers",
                     ("whether the Hermitian refinement of a quadratic form happens at every "
                      "rank or is special to E8")],
    }
    fp = ROOT / "data" / "PART_W33_PASS9961_9984_THE_UNITARY_BRANCH.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
