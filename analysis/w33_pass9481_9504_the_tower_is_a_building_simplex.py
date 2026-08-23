"""Passes 9481-9504 -- the tower is a simplex in a Bruhat-Tits building.

  9481  The incidence condition in a building is pL < L' < L. My filtration satisfies it.
  9482  So the four levels are PAIRWISE INCIDENT: a 3-simplex in the building of PGL_24(Q_2).
  9483  Their vertex types are 6, 12, 18, 0 -- an arithmetic progression of step 24/4.
  9484  WHY THE DEPTH IS deg(Phi): it is the RAMIFICATION INDEX of Q_p(zeta)/Q_p.
  9485  Verified at three points: (p,d) = (2,8), (3,9), (3,3) give e = 4, 6, 2. All match.
  9486  And (I-M) is not "an operator that happened to work" -- it IS the uniformizer.
  9487  Which retroactively explains the unit twists too.
  9488  Where this touches physics, and where it does not.
  9489  Open.
  9490  Scope.

WHAT THIS IS AND IS NOT. That a chain of lattices L > L_1 > ... > pL is a simplex in a
Bruhat-Tits building is STANDARD p-adic algebra, not a discovery. What this pass does is
recognise the tower of Passes 8022-9464 as one such simplex, and read off the consequences
-- which turn out to explain three things that were previously just measured.

    py -3 analysis/w33_pass9481_9504_the_tower_is_a_building_simplex.py
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
from sympy import totient  # noqa: E402
from w33_pass7333_leech_d4_form import load_flat, rank_mod2  # noqa: E402

# (p, d, measured filtration depth) from Pass 8861-8884 and Pass 8030-8040
MEASURED = [(2, 8, 4), (3, 9, 6), (3, 3, 2)]


def main() -> int:
    print("=" * 78)
    print("Passes 9481-9504 -- the tower is a Bruhat-Tits simplex")
    print("=" * 78)

    I = np.eye(24, dtype=np.int64)
    M = load_flat(ROOT / "analysis" / "_co0_M8.txt")[0]
    N = I - M

    print("\n  PASS 9481-9482 -- the incidence condition\n")
    print("""    In the Bruhat-Tits building of PGL_n(Q_p), vertices are homothety classes of
    Z_p-lattices, and two classes [L], [L'] are INCIDENT exactly when

        p L  <  L'  <  L .

    The filtration of Passes 8861-8884 is L > NL > N^2 L > N^3 L > N^4 L = 2L with
    N = I - M. Since N^4 L = 2L, every N^j L with j <= 4 contains 2L and sits inside L, so
    all four classes are pairwise incident.""")
    N4 = np.linalg.matrix_power(N, 4)
    U = np.rint(N4 / 2.0)
    inc = {"(I-M)^4 = 2U": bool(np.allclose(N4 / 2.0, U)),
           "U unimodular": abs(int(round(np.linalg.det(U)))) == 1}
    for k, v in inc.items():
        print(f"      {k:34s} {v}")
    print("""
        => [L], [NL], [N^2 L], [N^3 L] span a 3-SIMPLEX in the building of PGL_24(Q_2).

    A chamber there has 24 vertices, so this is a face, not a chamber. And M fixes every
    vertex of it, since M(N^j L) = N^j (M L) = N^j L: M is an ELLIPTIC element whose fixed
    set contains the simplex.""")

    print("\n  PASS 9483 -- vertex types\n")
    print(f"      {'j':>3s} {'rank(N^j mod 2)':>16s} {'dim L/N^j L':>13s} {'type mod 24':>12s}")
    types = []
    for j in range(1, 5):
        r = rank_mod2(np.linalg.matrix_power(N, j))
        d = 24 - r
        types.append({"j": j, "rank_mod2": r, "dim_quotient": d, "type": d % 24})
        print(f"      {j:3d} {r:16d} {d:13d} {d % 24:12d}")
    print("""
    Types 6, 12, 18, 0 -- an arithmetic progression of step 6 = 24/4. That is the type
    signature of an equally-spaced simplex, and it is the same [6,6,6,6] uniformity that
    Pass 9441-9464 read as a uniform multilevel code stack. Two names for one fact.""")

    print("\n  PASS 9484-9486 -- and the depth is the RAMIFICATION INDEX\n")
    print("""    The element with char poly Phi_{p^m}^k generates Q_p(zeta_{p^m}) over Q_p. That
    extension is TOTALLY RAMIFIED of degree phi(p^m) = deg Phi_{p^m}, and its uniformizer is

        pi = 1 - zeta.

    So (I - M) is not an operator that happened to work -- it IS the uniformizer acting on
    the lattice, and the filtration by its powers IS the ramification filtration. The depth
    must therefore equal the ramification index e = phi(p^m). Against what was measured:\n""")
    print(f"      {'p':>3s} {'d = p^m':>8s} {'phi(d) = e':>11s} {'measured depth':>15s} {'match':>6s}")
    ram = []
    allm = True
    for p, d, depth in MEASURED:
        ph = int(totient(d))
        ok = ph == depth
        allm &= ok
        ram.append({"p": p, "d": d, "phi": ph, "measured_depth": depth, "match": bool(ok)})
        print(f"      {p:3d} {d:8d} {ph:11d} {depth:15d} {str(ok):>6s}")
    print(f"\n      all three match: {allm}")
    print("""
    THREE THINGS THIS EXPLAINS RETROACTIVELY.

      1. THE DEPTH. Pass 8861-8884 measured e = 4 at p=2 and e = 6 at p=3 and reported them
         as facts. They are the ramification indices, forced.

      2. THE OPERATOR. Every pass since 8022 has used p(I-M)^{-1} and powers of (I-M)
         without a reason beyond "it is integral and it works". The reason is that 1-zeta
         is the uniformizer.

      3. THE UNIT TWISTS. Pass 8861-8884 found level 5 at p=3 only after sweeping A = s g^a
         (I-g)^{e-j}, and could not say why a twist was needed. A uniformizer is defined only
         up to UNITS of Z_p[zeta], and the units acting here are exactly the powers of zeta.
         The sweep was a search over the unit group, which is why it had to be done and why
         it was finite.""")

    print("\n  PASS 9488 -- where this touches physics, and where it does not\n")
    print("""    p-ADIC HOLOGRAPHY IS A REAL FIELD AND IT IS CITED, NOT CLAIMED. Gubser,
    Knaute, Parikh, Samberg and Witaszczyk (Comm. Math. Phys. 2016) put AdS/CFT on the
    Bruhat-Tits TREE, the rank-1 building, with boundary P^1(Q_p). Heydeman, Marcolli, Saberi
    and Stoica (arXiv:1801.09623) construct holographic CODES on Bruhat-Tits buildings and
    Drinfeld symmetric spaces. So "codes on buildings" already exists as a subject, and this
    pass does not claim it.

    THE FRACTAL POINT, STATED HONESTLY. The Bruhat-Tits TREE has boundary P^1(Q_p), which is
    a Cantor set -- genuinely fractal, and that is what the p-adic holography literature
    exploits. The object here is a HIGHER-RANK building, PGL_24(Q_2), whose boundary is a
    spherical building rather than a Cantor set. So the fractal reading applies to the rank-1
    case and I am NOT claiming it for this one. What is shared is the ultrametric setting,
    not the fractal boundary.

    WHAT WOULD BE A REAL BRIDGE, and is not done: the holographic-code constructions are
    built on TREES, so they use rank 1. The tower here is a rank-24 object with a
    distinguished 3-simplex. Whether the code stack of Pass 9441-9464 is an instance of the
    building codes in that literature is an open comparison, not a result.""")

    print("\n  PASS 9489-9490 -- open, and scope\n")
    print("""    NEW HERE: the recognition that the filtration is a simplex in the building of
    PGL_24(Q_2), its vertex types 6/12/18/0, and the identification of the depth with the
    ramification index -- which explains the depth law, the choice of operator, and the unit
    twists, all of which were previously measured without reason.
    STANDARD, NOT CLAIMED: that lattice chains are building simplices; that cyclotomic
    p-power extensions are totally ramified with uniformizer 1 - zeta.
    CITED, NOT CLAIMED: p-adic AdS/CFT (Gubser et al. 2016) and holographic codes on
    Bruhat-Tits buildings (Heydeman-Marcolli-Saberi-Stoica, arXiv:1801.09623).
    NOT DONE: whether the Pass 9441-9464 code stack is an instance of those building codes;
    the higher-rank boundary, which is NOT a Cantor set and carries no fractal claim here;
    alpha(W(3,9)); K12 built.
    NOT CLAIMED: any physical implementation, and no fractal property of this object.""")

    out = {
        "boundary": (
            "The pi-adic filtration used since Pass 8022 is a 3-SIMPLEX in the Bruhat-Tits "
            "building of PGL_24(Q_2): the incidence condition pL < L' < L holds because "
            "(I-M)^4 L = 2L, and the vertex types are 6, 12, 18, 0. The filtration DEPTH is "
            "the RAMIFICATION INDEX e = phi(p^m) of Q_p(zeta_{p^m})/Q_p, verified at "
            "(p,d) = (2,8), (3,9), (3,3) giving 4, 6, 2. That identifies (I-M) as the "
            "uniformizer 1-zeta and explains the depth law, the operator choice, and the "
            "unit twists, all previously measured without reason"),
        "incidence": {**{k: bool(v) for k, v in inc.items()},
                      "condition": "p L < L' < L, the building's incidence relation",
                      "conclusion": ("[L], [NL], [N^2 L], [N^3 L] are pairwise incident and "
                                     "span a 3-simplex; a chamber has 24 vertices so this is "
                                     "a face"),
                      "M_is_elliptic": ("M fixes every vertex, since M(N^j L) = N^j(ML) = "
                                        "N^j L")},
        "vertex_types": types,
        "type_signature": ("6, 12, 18, 0 -- an arithmetic progression of step 24/4, the same "
                           "uniformity Pass 9441-9464 read as a uniform code stack"),
        "ramification": {
            "identification": ("the element generates Q_p(zeta_{p^m}), totally ramified of "
                               "degree phi(p^m), with uniformizer pi = 1 - zeta"),
            "table": ram, "all_match": bool(allm),
            "explains": {
                "depth": "e = phi(p^m) is forced, not measured",
                "operator": ("p(I-M)^{-1} and powers of (I-M) were used since Pass 8022 with "
                             "no reason beyond integrality; 1-zeta being the uniformizer is "
                             "the reason"),
                "unit_twists": ("a uniformizer is defined only up to units of Z_p[zeta], and "
                                "those units are the powers of zeta -- so the A = s g^a "
                                "sweep at Pass 8861-8884 was a search over the unit group, "
                                "which is why it was needed and why it was finite")}},
        "physics": {
            "cited_not_claimed": [
                "p-adic AdS/CFT on the Bruhat-Tits tree (Gubser, Knaute, Parikh, Samberg, "
                "Witaszczyk, Comm. Math. Phys. 2016)",
                "holographic codes on Bruhat-Tits buildings and Drinfeld symmetric spaces "
                "(Heydeman, Marcolli, Saberi, Stoica, arXiv:1801.09623)"],
            "fractal_honesty": ("the rank-1 building (the TREE) has boundary P^1(Q_p), a "
                                "Cantor set, and that is what the p-adic holography "
                                "literature uses. This object is rank 24, whose boundary is "
                                "a spherical building, NOT a Cantor set. No fractal property "
                                "is claimed for it; what is shared is the ultrametric "
                                "setting"),
            "open_comparison": ("whether the Pass 9441-9464 code stack is an instance of the "
                                "building codes in that literature -- those are built on "
                                "trees, i.e. rank 1")},
        "standard_not_claimed": ["lattice chains are building simplices",
                                 "cyclotomic p-power extensions are totally ramified with "
                                 "uniformizer 1 - zeta"],
        "not_done": ["comparison with the tree-based holographic codes",
                     "anything fractal about this rank-24 object",
                     "alpha(W(3,9))", "K12 built"],
    }
    fp = ROOT / "data" / "PART_W33_PASS9481_9504_BUILDING_SIMPLEX.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
