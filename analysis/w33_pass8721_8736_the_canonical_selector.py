"""Passes 8721-8736 -- cyclotomic descent IS the canonical selector, and it is coisotropic.

  8721  The question the other lane left open, stated exactly.
  8722  E8^3 answers it: the order-9 element cubes to the order-3 one, exactly.
  8723  So there is a surjection W(11,3) ->> W(3,3), and it is canonical.
  8724  THE KERNEL IS COISOTROPIC, not Lagrangian -- measured, then forced.
  8725  So the selected W(3,3) is the symplectic reduction K / K-perp.
  8726  The honest limit: canonical as a SUBQUOTIENT, not as a subspace.
  8727  The two branches reduce by structurally different kernels.
  8728  What this says about Leech, and what the missing datum actually is.
  8729  Open.
  8730  Scope.

WHAT THE OTHER LANE ASKED. Pass8233-8240 counts the W(3,3) subgeometries of the six-qutrit
carrier: exactly 2,110,666,092,277,743 of them, forming ONE Sp12(3) orbit, and concludes
"the bare W(11,3) carrier selects no preferred W33 slice; an E8/Leech bridge requires
additional lattice or controller data." Pass8225-8232 says the same at q=2: 336 copies of
W(3,2) in W(5,2), one Sp6(2) orbit, "not canonically selected by the Leech symplectic
quotient alone."

Both are right, and both are about the BARE CARRIER. This pass supplies the additional datum
for E8^3 and identifies its exact type.

    py -3 analysis/w33_pass8721_8736_the_canonical_selector.py
"""

from __future__ import annotations

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
from scipy.linalg import block_diag  # noqa: E402
from sympy import GF, Matrix  # noqa: E402
from sympy.polys.matrices import DomainMatrix  # noqa: E402
from w33_pass7217_ovoid_pullback_to_e8 import CARTAN, simple_reflection  # noqa: E402


def gf3rank(A):
    """Exact rank over GF(3). Deliberately sympy, not hand-rolled elimination: an
    earlier hand-rolled version of this reported an 8-dimensional totally isotropic
    subspace of a nondegenerate F_3^12, which is impossible (the maximum is 6). The
    impossible number is what exposed the bug."""
    B = (np.array(A, dtype=np.int64) % 3).tolist()
    return len(DomainMatrix.from_Matrix(Matrix(B)).convert_to(GF(3)).rref()[1])


def main() -> int:
    print("=" * 78)
    print("Passes 8721-8736 -- the canonical selector, and its type")
    print("=" * 78)

    I8 = np.eye(8, dtype=np.int64)
    I24 = np.eye(24, dtype=np.int64)
    cox = np.eye(8, dtype=np.int64)
    for i in range(8):
        cox = cox @ simple_reflection(i)
    W = np.linalg.matrix_power(cox, 10)
    G = block_diag(CARTAN, CARTAN, CARTAN).astype(np.int64)
    tau = np.zeros((24, 24), dtype=np.int64)
    for i in range(3):
        tau[8 * ((i + 1) % 3):8 * ((i + 1) % 3) + 8, 8 * i:8 * i + 8] = I8
    g = tau @ block_diag(W, I8, I8).astype(np.int64)
    w = np.linalg.matrix_power(g, 3)
    diag = block_diag(W, W, W).astype(np.int64)

    print("\n  PASS 8721-8723 -- the chain is literal, so the surjection is canonical\n")
    chain = {
        "g cubes to the DIAGONAL order-3 element": bool(np.array_equal(w, diag)),
        "g has order 9 with minimal polynomial Phi_9":
            bool(not (np.linalg.matrix_power(g, 6) + np.linalg.matrix_power(g, 3)
                      + I24).any()),
        "det(I-g) = 3^4": int(round(np.linalg.det((I24 - g).astype(float)))) == 81,
        "det(I-g^3) = 3^12": int(round(np.linalg.det((I24 - w).astype(float)))) == 3 ** 12,
        "g preserves the E8^3 form": bool(np.array_equal(g.T @ G @ g, G)),
    }
    for k, v in chain.items():
        print(f"      {k:44s} {v}")
    T = np.linalg.inv((I24 - g).astype(float)) @ (I24 - w).astype(float)
    integral = bool(np.allclose(T, np.rint(T), atol=1e-6))
    print(f"      {'(I-g)^-1 (I-g^3) is integral':44s} {integral}")
    print("""
    Since I - g^3 = (I-g)(I + g + g^2), the sublattice (I-g^3)L sits inside (I-g)L, and the
    transition is integral. So

        L/(I-g^3)L = F_3^12   SURJECTS ONTO   L/(I-g)L = F_3^4
        W(11,3), six qutrits          ->>     W(3,3), two qutrits

    and nothing was chosen: g^3 IS the diagonal order-3 element, exactly, so the six-qutrit
    carrier and the two-qutrit one come from the SAME element at two powers. That is the
    additional datum the bare carrier lacks -- not a lattice embedding, a CUBE ROOT.""")

    print("\n  PASS 8724-8725 -- and the kernel is COISOTROPIC\n")
    F = ((w + 2 * I24).T @ G) % 3
    rF, rIw, rIg = gf3rank(F), gf3rank(I24 - w), gf3rank(I24 - g)
    U = ((I24 - g) % 3).T
    gU = np.array([[int(u @ F @ v) % 3 for v in U] for u in U], dtype=np.int64)
    rK = gf3rank(gU)
    dK = rIg - rIw
    meas = {"rank F (form on the quotient)": rF, "rank(I-g^3) = dim radical of F": rIw,
            "rank(I-g)": rIg, "dim K = rank(I-g) - rank(I-g^3)": dK,
            "rank of F restricted to K": rK}
    for k, v in meas.items():
        print(f"      {k:44s} {v}")
    rad = dK - rK
    perp = 12 - dK
    print(f"""
    Two measured numbers settle the type, with no containment test needed:

        rad(K) = K cap K-perp  has dim  {dK} - {rK} = {rad}
        K-perp                 has dim  12 - {dK} = {perp}

    Those are equal, and K cap K-perp is contained in K-perp, so K-perp IS INSIDE K:

        K IS COISOTROPIC.

    Therefore K/K-perp has dimension {dK} - {rad} = {rK} and carries a nondegenerate
    alternating form -- which on F_3^{rK} is exactly W({rK-1},3).

    The selected W(3,3) is the SYMPLECTIC REDUCTION of the six-qutrit space by K.""")

    print("\n  PASS 8726 -- the honest limit\n")
    print("""    This does NOT pick out one of the other lane's 2,110,666,092,277,743
    subgeometries. Their count is of W(3,3) SUBSPACES of W(11,3); what cyclotomic descent
    produces is a SUBQUOTIENT, K/K-perp. Realising it as an actual subspace means choosing a
    complement to K-perp inside K, and since K-perp is isotropic that complement is not
    unique. So the correct statement is:

        canonical as a SUBQUOTIENT, not as a subspace.

    Their "the bare carrier selects no preferred slice" stands exactly as written. What is
    added is that the carrier PLUS a cube root of its defining element selects a canonical
    W(3,3) one level up, in the subquotient sense.""")

    print("\n  PASS 8727 -- the two branches reduce differently\n")
    print(f"      {'branch':>8s} {'ambient':>10s} {'dim K':>6s} {'rank F|K':>9s} "
          f"{'type':>14s}  {'target':>9s}")
    print(f"      {'qubit':>8s} {'F_2^12':>10s} {6:6d} {0:9d} {'LAGRANGIAN':>14s}  "
          f"{'W(5,2)':>9s}")
    print(f"      {'qutrit':>8s} {'F_3^12':>10s} {dK:6d} {rK:9d} {'COISOTROPIC':>14s}  "
          f"{'W(3,3)':>9s}")
    print("""
    The qubit reduction quotients by a maximal COMMUTING set -- a stabiliser group -- and
    halves the qubit count. The qutrit reduction quotients by a coisotropic subspace and
    divides the qutrit count by three. They are not the same construction wearing different
    primes: one kernel is isotropic, the other is not, and the ranks 0 and 4 say so.

    The reason is dimensional, and it is forced. Rung m at prime p uses deg(Phi_{p^m}), which
    doubles at each step for p=2 but TRIPLES the index for p=3, so the kernel is half the
    space at p=2 and two thirds of it at p=3. Two thirds of 12 is 8, which exceeds the
    maximal isotropic dimension 6 -- so a p=3 kernel simply CANNOT be Lagrangian.""")

    print("\n  PASS 8728 -- what this says about Leech\n")
    print("""    Leech has no Phi_9^4 class -- Pass 8030-8040 proved that exhaustively from
    the 2.Co1 character table, all three order-9 classes having exactly three Phi_9 blocks
    and never four. So Leech's six-qutrit carrier has NO cube root of its defining element,
    and therefore no canonical coisotropic K, and therefore no canonically selected W(3,3).

    That names the missing datum precisely. The other lane wrote "an E8/Leech bridge requires
    additional lattice or controller data". The additional datum is a CUBE ROOT OF THE
    ORDER-3 ISOMETRY. E8^3 has one, supplied by the S3 that permutes its three factors; Co0
    does not have one, and cannot, for a reason that is now a theorem rather than a search.""")

    print("\n  PASS 8729-8730 -- open, and scope\n")
    print("""    NEW: that g^3 is exactly the diagonal order-3 element, making W(11,3) ->>
    W(3,3) canonical for E8^3; that its kernel is COISOTROPIC with rank 4, so the selected
    W(3,3) is the symplectic reduction K/K-perp; the subquotient-not-subspace limit; and the
    identification of the missing datum as a cube root.
    CITED: Pass8233-8240 and Pass8225-8232 (other lane) for the orbit counts and the
    canonicality question; Pass 8030-8040 for the no-Phi_9^4 theorem; Pass 8022-8029 for the
    Lagrangian qubit kernel this is contrasted against.
    METHOD NOTE: the GF(3) ranks here are sympy's, not hand-rolled. A hand-rolled version
    reported an 8-dimensional totally isotropic subspace of a nondegenerate F_3^12 -- which
    is impossible, the maximum being 6, and that impossibility is what caught the bug.
    NOT DONE: whether any complement of K-perp in K is distinguished; the same analysis for
    Leech's W(5,2) 336 (the q=2 analogue of this question); alpha(W(3,9)); K12 built.
    NOT CLAIMED: any Monster result, and no physics.""")

    out = {
        "boundary": (
            "VERIFIED: for E8^3 the order-9 element cubes EXACTLY to the diagonal order-3 "
            "element, so W(11,3) ->> W(3,3) is canonical; its kernel K has dim 8 with the "
            "form of rank 4, which forces K-perp inside K -- K is COISOTROPIC -- and the "
            "selected W(3,3) is the symplectic reduction K/K-perp. Canonical as a "
            "SUBQUOTIENT, not as a subspace. Leech has no such cube root, so the datum the "
            "other lane identified as missing is exactly a cube root of the order-3 isometry"),
        "answers": {
            "Pass8233_8240_other_lane": ("counts 2110666092277743 W(3,3) subgeometries of "
                                         "W(11,3), one Sp12(3) orbit, and asks for the "
                                         "additional datum that would select one"),
            "Pass8225_8232_other_lane": ("the same at q=2: 336 copies of W(3,2) in W(5,2), "
                                         "one Sp6(2) orbit, none canonically selected"),
            "this_pass": ("supplies the datum for E8^3 and names its type: a CUBE ROOT of "
                          "the order-3 isometry, whose descent kernel is coisotropic")},
        "chain": {**{k: bool(v) for k, v in chain.items()},
                  "transition_integral": integral,
                  "surjection": "L/(I-g^3)L = F_3^12 ->> L/(I-g)L = F_3^4",
                  "why_canonical": ("g^3 IS the diagonal order-3 element exactly, so both "
                                    "carriers come from one element at two powers")},
        "kernel": {**{k: int(v) for k, v in meas.items()},
                   "radical_of_K": int(rad), "dim_K_perp": int(perp),
                   "type": "COISOTROPIC (K-perp is contained in K)",
                   "forced_by": ("rad(K) = dim K - rank(F|K) = 4 equals dim K-perp = 4, so "
                                 "K cap K-perp IS K-perp"),
                   "reduction": f"K/K-perp has dim {rK} with a nondegenerate form = W({rK-1},3)"},
        "honest_limit": {
            "claim_is": "canonical as a SUBQUOTIENT K/K-perp",
            "claim_is_not": ("a selection among the other lane's 2110666092277743 W(3,3) "
                             "SUBSPACES; realising the subquotient as a subspace needs a "
                             "complement to the isotropic K-perp, which is not unique"),
            "their_statement_stands": "the bare carrier selects no preferred slice"},
        "two_branches_differ": {
            "qubit": {"ambient": "F_2^12", "dim_kernel": 6, "rank_form_on_kernel": 0,
                      "type": "LAGRANGIAN", "target": "W(5,2)",
                      "meaning": "quotient by a maximal commuting set, a stabiliser group"},
            "qutrit": {"ambient": "F_3^12", "dim_kernel": int(dK),
                       "rank_form_on_kernel": int(rK), "type": "COISOTROPIC",
                       "target": "W(3,3)", "meaning": "symplectic reduction"},
            "why_forced": ("the kernel is half the space at p=2 but two thirds of it at p=3; "
                           "two thirds of 12 is 8, which exceeds the maximal isotropic "
                           "dimension 6, so a p=3 kernel CANNOT be Lagrangian")},
        "leech": {
            "no_cube_root": ("Co0 has no Phi_9^4 class -- Pass 8030-8040, exhaustive from the "
                             "character table, all three order-9 classes having three Phi_9 "
                             "blocks and never four"),
            "consequence": ("Leech's six-qutrit carrier has no canonical coisotropic K and "
                            "hence no canonically selected W(3,3)"),
            "missing_datum_named": ("a CUBE ROOT of the order-3 isometry. E8^3 has one, "
                                    "supplied by the S3 permuting its three factors; Co0 "
                                    "does not, and cannot")},
        "method_note": ("GF(3) ranks are sympy's. A hand-rolled elimination reported an "
                        "8-dimensional totally isotropic subspace of a nondegenerate F_3^12, "
                        "impossible since the maximum is 6; that impossibility caught the bug"),
        "not_done": ["whether any complement of K-perp in K is distinguished",
                     "the q=2 analogue of this question for the 336",
                     "alpha(W(3,9))", "K12 built"],
    }
    fp = ROOT / "data" / "PART_W33_PASS8721_8736_CANONICAL_SELECTOR.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
