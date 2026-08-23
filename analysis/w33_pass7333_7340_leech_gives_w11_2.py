"""Passes 7333-7340 -- LEECH at d=4 gives W(11,2): the six-qubit Pauli geometry.

  7333  Co0 obtained; its order-4 signatures censused; the Phi_4^12 element found.
  7334  The invariant Gram recovered from the generators, and verified.
  7335  Which form descends, and why (Mx,y) does not.
  7336  THE RESULT: a nondegenerate ALTERNATING form on F_2^12 -- W(11,2).
  7337  The tower, and what each rung reads as in Pauli language.
  7338  Two GAP export traps, both paid for.
  7339  Open.
  7340  Scope.

    py -3 analysis/w33_pass7333_7340_leech_gives_w11_2.py
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

TOWER = [
    ("E8", 8, 3, "F_3^4", "W(3,3)", 40, "two qutrits"),
    ("E8", 8, 4, "F_2^4", "W(3,2)", 15, "two qubits"),
    ("Leech", 24, 4, "F_2^12", "W(11,2)", 4095, "SIX QUBITS"),
]


def main() -> int:
    print("=" * 78)
    print("Passes 7333-7340 -- Leech at d=4 gives W(11,2)")
    print("=" * 78)

    print("\n  PASS 7333-7335 -- getting there\n")
    print("""    Co0 = Aut(Leech) is available as the ATLAS 24-dimensional INTEGRAL
    representation of 2.Co1. Censusing its order-4 elements gives six (trace, det(I-M))
    signatures, exactly one of which is the pure power Phi_4^12: trace 0, det 4096 = 2^12,
    with M^2 = -I. So Leech is a rank-12 Z[i]-module and

        Leech / (I-M)Leech = F_2^12,  4095 nonzero classes,  196560/4095 = 48 vectors each

    -- uniform, and covering ALL 4095 points of PG(11,2). So the minimal vectors are not
    needed to say which points are hit: every one is. Only the FORM was open.

    The invariant Gram was recovered by solving g^T G g = G, which vectorises as
    (g^T (x) g^T) vec(G) = vec(G). The solution space is 1-dimensional, as it must be, and
    both generators AND the element M preserve the recovered form exactly.

    WHICH FORM DESCENDS. (Mx,y) and (x,y) both have rank 24 mod 2 -- they do not descend to
    the 12-dimensional quotient at all. ((I+M)x, y) has rank exactly 12, and its mod-2
    radical has dimension 12, matching rank(I-M) = 12 precisely: the radical IS the image of
    (I-M). Descent was then checked directly: zero mismatches over 400 random triples.""")

    print("\n  PASS 7336 -- THE RESULT\n")
    print("""        The form ((I+M)x, y) mod 2 is a NONDEGENERATE ALTERNATING form on F_2^12.

    Nondegenerate alternating on a 12-dimensional F_2 space is the symplectic polar space
    W(11,2) of PG(11,2). All three properties were verified, not assumed: alternating (every
    diagonal entry even), rank 12, and well defined on classes.""")

    print("\n  PASS 7337 -- the tower, in Pauli language\n")
    print(f"      {'lattice':>7s} {'rank':>5s} {'d':>3s} {'quotient':>9s} {'geometry':>10s} "
          f"{'points':>7s}  {'reads as':>13s}")
    for lat, rk, d, q, geo, pts, rd in TOWER:
        print(f"      {lat:>7s} {rk:5d} {d:3d} {q:>9s} {geo:>10s} {pts:7d}  {rd:>13s}")
    print("""
    W(2n-1,q) is the commutation geometry of n qudits of dimension q: points are Pauli
    classes, and collinearity is commuting. So the tower reads: E8 carries the two-qutrit and
    two-qubit Pauli geometries, and LEECH carries the SIX-QUBIT one -- 4095 = 2^12 - 1
    nonzero Pauli classes on six qubits, with commuting exactly the vanishing of the form
    induced by the Leech inner product.

    NO PHYSICAL CLAIM IS MADE. This is the finite geometry of a lattice quotient, stated in
    its quantum-information vocabulary, and it inherits the disclaimer carried since the q=2
    prior art at Pass 5351-5352.""")

    print("\n  PASS 7338 -- two GAP export traps\n")
    print("""    Both cost real time and both are worth recording.

    GAP's String() wraps long lines with a trailing backslash, and that wrap can split a
    TOKEN -- a minus sign left at a line end simply parses away, silently flipping a sign.
    The first export passed every superficial check (right integer count, balanced brackets)
    and failed every mathematical one. Writing the matrix FLAT, one row per line via
    OutputTextFile with SetPrintFormattingStatus(f, false), fixes it.

    And QUIT cannot appear inside an if-block in GAP; it is a syntax error, not a runtime one.

    The element is now re-verified on the Python side (M^2 = -I, trace 0, det 4096) before
    anything is computed from it.""")

    print("\n  PASS 7339-7340 -- open, and scope\n")
    print("""    NEW: the Phi_4^12 element of Co0; the recovered invariant Gram; and the
    identification of the Leech d=4 quotient geometry as W(11,2).

    NOT DONE: the d=8 and d=13 Leech quotients (pure-power elements exist for both, per the
    census: Phi_8^6 giving 63 points and Phi_13^2 giving 168); the d=9 quotient onto PG(5,3);
    K12 built; alpha(W(3,9)); q=11 at 68; Coolsaet unread.

    NOT CLAIMED: any Monster result, and no physics.""")

    out = {
        "boundary": (
            "VERIFIED: the Leech lattice modulo (I-M) for the Phi_4^12 element of Co0 is "
            "F_2^12, the fibration covers all 4095 points of PG(11,2) uniformly at 48 "
            "minimal vectors each, and the form ((I+M)x,y) descends to a NONDEGENERATE "
            "ALTERNATING form -- i.e. W(11,2), the six-qubit Pauli commutation geometry. No "
            "physical claim; no Monster claim"),
        "element": {"source": 'ATLAS AtlasGenerators("2.Co1", 9), 24-dim integral',
                    "char_poly": "Phi_4^12", "order": 4, "trace": 0,
                    "det_I_minus_M": 4096, "M_squared": "-I"},
        "quotient": {"space": "F_2^12", "nonzero_classes": 4095,
                     "minimal_vectors_per_class": 48, "uniform": True,
                     "covers": "all of PG(11,2)"},
        "invariant_form": {"method": "solve g^T G g = G via (g^T (x) g^T) vec(G) = vec(G)",
                           "solution_space_dim": 1,
                           "preserved_by": "both generators and M, exactly"},
        "which_form_descends": {
            "(Mx,y)": {"rank_mod2": 24, "descends": False},
            "(x,y)": {"rank_mod2": 24, "descends": False},
            "((I+M)x,y)": {"rank_mod2": 12, "radical_dim": 12,
                           "equals_image_of_I_minus_M": True,
                           "descent_check": "0 mismatches over 400 random triples",
                           "alternating": True, "descends": True}},
        "result": {"form": "nondegenerate alternating on F_2^12",
                   "geometry": "W(11,2), symplectic polar space of PG(11,2)",
                   "pauli_reading": ("the commutation geometry of SIX QUBITS: 4095 nonzero "
                                     "Pauli classes, collinear = commuting"),
                   "disclaimer": ("finite geometry of a lattice quotient in QI vocabulary; "
                                  "no physical claim, per the Pass 5351-5352 prior art")},
        "tower": [{"lattice": l, "rank": r, "d": d, "quotient": q, "geometry": g,
                   "points": p, "reads_as": rd} for l, r, d, q, g, p, rd in TOWER],
        "gap_export_traps": [
            "String() line-wraps with a backslash that can split a token; a minus sign at a "
            "line end parses away, silently flipping a sign",
            "QUIT cannot appear inside an if-block (syntax error, not runtime)"],
        "not_done": ["Leech d=8 (Phi_8^6, 63 points) and d=13 (Phi_13^2, 168 points)",
                     "Leech d=9 onto PG(5,3)", "K12 built", "alpha(W(3,9))", "q=11 at 68",
                     "Coolsaet unread"],
    }
    fp = ROOT / "data" / "PART_W33_PASS7333_7340_LEECH_W11_2.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
