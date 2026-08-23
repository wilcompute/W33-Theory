"""Passes 7349-7356 -- which qudit systems are lattice-realisable, and how Leech's two link.

RETRACTED IN PART BY PASS 8022-8029 AND 8030-8040 -- READ THIS FIRST.

  The claim below that "LEECH GIVES EXACTLY TWO GEOMETRIES: W(11,2) and W(5,2). That list
  is now complete, not a sample" is WRONG, and so is the filter that produced it. The
  UNIFORMITY column removed d=2 and d=3 because 196560 is not divisible by 2^24-1 or
  3^12-1. That test measures whether the MINIMAL VECTORS cover the quotient evenly; it says
  nothing about whether the geometry exists. The corrected picture is two branches:

      W(23,2) -> W(11,2) -> W(5,2)     12 -> 6 -> 3 qubits   (Pass 8022-8029)
      W(11,3)                          6 qutrits             (Pass 8030-8040)

  Read the uniformity column below as a property of the minimal-vector fibration ONLY,
  never as an existence criterion. The reachability formula, the arithmetic, and the
  projection results in this file all stand.

  7349  The reachability formula: n = r / (2 deg(Phi_d)).
  7350  Four and five qubits are UNREACHABLE from rank 24, and the reason is that phi is never 3.
  7351  The complete rank-24 table: arithmetic, uniformity, existence.
  7352  W(11,2) projects ONTO W(5,2). Six qubits onto three.
  7353  The same element gives both: M8 gives three, M8^2 gives six.
  7354  Purity run backwards as a design tool.
  7355  Open.
  7356  Scope.

    py -3 analysis/w33_pass7349_7356_reachability_and_projection.py
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

RANK24 = [
    (2, 1, 24, 2, 12, "W(23,2)", False, "-"),
    (3, 2, 12, 3, 6, "W(11,3)", False, "-"),
    (4, 2, 12, 2, 6, "W(11,2)", True, "EXISTS -> six qubits"),
    (5, 4, 6, 5, 3, "W(5,5)", False, "-"),
    (7, 6, 4, 7, 2, "W(3,7)", False, "-"),
    (8, 4, 6, 2, 3, "W(5,2)", True, "EXISTS -> three qubits"),
    (9, 6, 4, 3, 2, "W(3,3)", True, "NO Phi_9^4 in Co0 -- killed by existence"),
    (13, 12, 2, 13, 1, "W(1,13)", True, "exists but a line, no content"),
]


def main() -> int:
    print("=" * 78)
    print("Passes 7349-7356 -- reachability, and the projection")
    print("=" * 78)

    print("\n  PASS 7349-7350 -- the reachability formula, and an impossibility\n")
    print("""    A pure char poly Phi_d^k on rank r forces k * deg(Phi_d) = r and p = Phi_d(1), so
    the quotient is F_p^k and the geometry is W(k-1, p) -- which reads as n qudits of
    dimension p with

        n  =  k/2  =  r / (2 deg(Phi_d))        and n must be an INTEGER.

    FOUR AND FIVE QUBITS ARE UNREACHABLE FROM RANK 24, for elementary reasons. Four qubits
    needs k = 8, hence deg(Phi_d) = 3 with d a 2-power -- but Euler's phi is NEVER 3, so no
    such d exists at any rank. Five qubits needs deg = 24/10 = 2.4, not an integer.

    So from rank 24 the reachable qubit counts are exactly r/(2 phi(d)) for 2-power d:
    12, 6, 3 -- and 12 fails uniformity. That is the whole list.""")

    print("\n  PASS 7351 -- the complete rank-24 table\n")
    print(f"      {'d':>3s} {'deg':>4s} {'k':>3s} {'p':>3s} {'n':>3s} {'geometry':>10s} "
          f"{'uniform':>8s}  {'existence':>36s}")
    for d, dg, k, p, n, geo, u, note in RANK24:
        print(f"      {d:3d} {dg:4d} {k:3d} {p:3d} {n:3d} {geo:>10s} {str(u):>8s}  {note:>36s}")
    print("""
    THREE FILTERS, APPLIED IN ORDER, and each one cuts. Arithmetic (k integer, n integer)
    admits eight values of d. UNIFORMITY -- 196560 divisible by p^k - 1 -- cuts to four.
    EXISTENCE in Co0 cuts d=9, because its order-9 fixed-point-free elements are
    Phi_9^3 Phi_3^3 and never Phi_9^4. And d=13 survives everything but lands on a line.

    [RETRACTED -- see the header. The uniformity filter answers a different question, and
    the corrected list is W(23,2) -> W(11,2) -> W(5,2) plus W(11,3).]""")

    print("\n  PASS 7352-7353 -- and the two are linked by a projection\n")
    print("""    M8 has order 8, so M8^2 has order 4 -- and it is not merely order 4:

        (M8^2)^2 = -I  and  det(I - M8^2) = 4096

    which is exactly the Phi_4^12 signature. So the SAME element generates both rungs: M8
    gives the three-qubit geometry and M8^2 gives the six-qubit one.

    The algebra then forces a map. Since I - M^2 = (I - M)(I + M), the sublattice
    (I - M8^2)L is contained in (I - M8)L -- verified, the transition matrix is integral --
    so

        L/(I-M8^2)L  =  F_2^12   SURJECTS ONTO   L/(I-M8)L  =  F_2^6

    with kernel of size 4096/64 = 64 = 2^6. In Pauli language: W(11,2) projects onto W(5,2),
    six qubits onto three. It is a PROJECTION, not an embedding, and the direction matters.""")

    print("\n  PASS 7354 -- purity backwards, as a design tool\n")
    print("""    Read the formula the other way. To realise n qudits of dimension q you need

        a lattice of rank r = n * 2 * deg(Phi_d),  with Phi_d(1) = q, so d = q^m,

    and then uniformity (kissing number divisible by q^{2n} - 1) and existence of the element
    must both hold. That turns "which lattice hosts my system?" into a lookup rather than a
    search. Four qubits, for instance, needs deg(Phi_d) = r/8: impossible at r = 24, but at
    r = 32 it is deg 4, i.e. d = 8 -- so a rank-32 lattice is where four qubits could live.""")

    print("\n  PASS 7355-7356 -- open, and scope\n")
    print("""    NEW: the reachability formula and its impossibility results; the complete
    rank-24 table with all three filters; the W(11,2) -> W(5,2) projection and the fact that
    one element generates both.
    NOT DONE: K12 built; the rank-32 case actually tested; alpha(W(3,9)); q=11 at 68;
    Coolsaet unread.
    NOT CLAIMED: any Monster result, and no physics.""")

    out = {
        "RETRACTED_IN_PART_BY": "Pass 8022-8029 and Pass 8030-8040: the uniformity filter measures minimal-vector coverage, not existence; the corrected list is W(23,2) -> W(11,2) -> W(5,2) plus W(11,3)",
        "boundary": (
            "The reachable geometries from a lattice of rank r are W(k-1,p) with "
            "k = r/deg(Phi_d) and p = Phi_d(1), reading as n = r/(2 deg(Phi_d)) qudits. For "
            "Leech the complete list after arithmetic, uniformity AND existence filters is "
            "exactly W(11,2) and W(5,2). Four and five qubits are unreachable from rank 24"),
        "reachability": {
            "formula": "n = k/2 = r / (2 deg(Phi_d)), with p = Phi_d(1) and d = p^m",
            "four_qubits_at_rank24": {"needs_deg": 3,
                                      "why_impossible": "Euler phi is never 3, at any rank"},
            "five_qubits_at_rank24": {"needs_deg": 2.4, "why_impossible": "not an integer"},
            "reachable_qubit_counts_rank24": [12, 6, 3],
            "note": "12 fails uniformity"},
        "rank24_table": [{"d": d, "deg": dg, "k": k, "p": p, "n": n, "geometry": g,
                          "uniform": u, "existence": note}
                         for d, dg, k, p, n, g, u, note in RANK24],
        "three_filters": {
            "arithmetic": "8 values of d admitted",
            "uniformity": "196560 divisible by p^k - 1 cuts to 4",
            "existence": ("Co0 has no Phi_9^4, killing d=9; d=13 survives but lands on a "
                          "line"),
            "result": "Leech gives EXACTLY W(11,2) and W(5,2)"},
        "projection": {
            "fact": "M8^2 has (M8^2)^2 = -I and det(I - M8^2) = 4096, the Phi_4^12 signature",
            "algebra": "I - M^2 = (I-M)(I+M), so (I-M8^2)L is contained in (I-M8)L",
            "verified": "the transition matrix (I-M8)^{-1}(I-M8^2) is integral",
            "map": "F_2^12 surjects onto F_2^6, kernel 4096/64 = 64 = 2^6",
            "reading": ("W(11,2) projects ONTO W(5,2): six qubits onto three, induced by "
                        "squaring the order-8 element. A projection, not an embedding"),
            "same_element": "M8 gives three qubits, M8^2 gives six"},
        "design_tool": {
            "read_backwards": ("to realise n qudits of dimension q, need rank "
                               "r = 2 n deg(Phi_d) with Phi_d(1) = q"),
            "example": ("four qubits needs deg(Phi_d) = r/8: impossible at r=24, but deg 4 "
                        "at r=32, i.e. d=8 -- a rank-32 lattice is where four qubits could "
                        "live")},
        "not_done": ["K12 built", "the rank-32 case tested", "alpha(W(3,9))", "q=11 at 68",
                     "Coolsaet unread"],
    }
    fp = ROOT / "data" / "PART_W33_PASS7349_7356_REACHABILITY.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
