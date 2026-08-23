"""Passes 8909-8924 -- the Springer centraliser IS the Clifford group of its own geometry.

  8909  Two facts already known, sitting next to each other without being joined.
  8910  Order arithmetic is suggestive and cannot decide it. The ACTION can.
  8911  d = 4: C_W(M) surjects onto Sp(4,2) with kernel exactly 64. VERIFIED.
  8912  d = 8: C_W(M) surjects onto Sp(2,2) with kernel exactly 32. VERIFIED.
  8913  So the centraliser is the Clifford group OF the geometry the element produces.
  8914  And at odd primes it is NOT -- the kernel is far too small for a Pauli group.
  8915  Which is the same p=2 exceptionality as the Lagrangian/coisotropic split.
  8916  Open.
  8917  Scope.

THE TWO FACTS. (1) Springer: the centraliser of a d-regular element of W has order equal to
the product of the degrees divisible by d, and for W(E8) at d=4 that is 8*12*20*24 = 46080,
the Shephard-Todd group G31. This repo already records it at
analysis/w33_pass1039_springer_tower.g (2026-07-26), which names G31 and G32 explicitly.
(2) Planat and Kibler, "Unitary reflection groups for quantum fault tolerance"
(arXiv:0807.3650), identify G31 with the two-qubit Clifford group -- it is a maximal
index-2 subgroup of it. Planat's "Entangling gates in even Euclidean lattices such as the
Leech lattice" (arXiv:1002.4287) is already cited in this repo at BT7154, and shows the two-
and four-qubit REAL Clifford groups are the automorphism groups of D4 and BW16.

WHAT WAS NOT JOINED. Passes 8022-8900 show the SAME order-4 element produces the two-qubit
geometry W(3,2) as E8/(I-M)E8. So the centraliser of M and the Clifford group of the geometry
M builds are two descriptions of one group of order 46080 -- but matching orders is not a
proof that they are the same group acting the same way. A group of order 46080 could act on
F_2^4 through any quotient. This pass computes the action.

    py -3 analysis/w33_pass8909_8924_the_centraliser_is_the_clifford_group.py
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
from w33_pass7333_leech_d4_form import load_flat  # noqa: E402

DEGREES = [2, 8, 12, 14, 18, 20, 24, 30]


def sp_order(n, q):
    o = q ** (n * n)
    for i in range(1, n + 1):
        o *= q ** (2 * i) - 1
    return o


def rref2(rows):
    out, piv = [], []
    for r in rows:
        r = np.array(r, dtype=np.int64) % 2
        for b, pb in zip(out, piv):
            if r[pb]:
                r = (r + b) % 2
        nz = [i for i, v in enumerate(r) if v]
        if nz:
            out.append(r)
            piv.append(nz[0])
    return out, piv


def action_image(mfile, gfile, e, corder):
    """Order of the image of C_W(M) acting on E8/(I-M)E8, and the kernel order."""
    I8 = np.eye(8, dtype=np.int64)
    M = load_flat(ROOT / "analysis" / mfile, 8)[0]
    gens = load_flat(ROOT / "analysis" / gfile, 8)
    A = np.linalg.matrix_power(I8 - M, e - 1) % 2      # the level-1 class map
    B, piv = rref2(list(A.T))
    B = np.array(B, dtype=np.int64)
    k = B.shape[0]

    def coords(v):
        w = v % 2
        out = np.zeros(k, dtype=np.int64)
        for j in range(k):
            if w[piv[j]]:
                out[j] = 1
                w = (w + B[j]) % 2
        if w.any():
            raise AssertionError("image not inside the quotient model")
        return out

    acts = []
    for g in gens:
        acts.append(np.array([coords((g @ b) % 2) for b in B], dtype=np.int64) % 2)
    seen = {}
    fr = [np.eye(k, dtype=np.int64)]
    seen[fr[0].tobytes()] = 1
    while fr:
        nf = []
        for X in fr:
            for Am in acts:
                Y = (X @ Am) % 2
                kk = Y.tobytes()
                if kk not in seen:
                    seen[kk] = 1
                    nf.append(Y)
        fr = nf
    n = k // 2
    return {"k": k, "qubits": n, "geometry": f"W({k-1},2)", "centraliser_order": corder,
            "image_order": len(seen), "sp_order": sp_order(n, 2),
            "image_is_full_symplectic": len(seen) == sp_order(n, 2),
            "kernel_order": corder // len(seen) if corder % len(seen) == 0 else None,
            "generators_used": len(gens)}


def main() -> int:
    print("=" * 78)
    print("Passes 8909-8924 -- the centraliser is the Clifford group of its own geometry")
    print("=" * 78)

    print("\n  PASS 8909-8910 -- order arithmetic first, which cannot decide it\n")
    print(f"      {'d':>3s} {'degrees divisible by d':>24s} {'|C_W|':>9s} {'geometry':>9s} "
          f"{'|Sp|':>7s} {'ratio':>7s}")
    arith = {}
    for d, k, p in ((3, 4, 3), (4, 4, 2), (5, 2, 5), (8, 2, 2)):
        dd = [D for D in DEGREES if D % d == 0]
        C = 1
        for D in dd:
            C *= D
        S = sp_order(k // 2, p)
        arith[d] = {"degrees": dd, "centraliser_order": C, "geometry": f"W({k-1},{p})",
                    "sp_order": S, "ratio": C // S if C % S == 0 else C / S}
        print(f"      {d:3d} {str(dd):>24s} {C:9d} {'W(' + str(k-1) + ',' + str(p) + ')':>9s} "
              f"{S:7d} {arith[d]['ratio']:>7}")
    print("""
    The d=4 row is suggestive: 46080 = 4 * 11520, and 11520 = |Sp(4,2)| * 2^4 is the order
    of the two-qubit Clifford group modulo phases, so 46080 is that group with a Z_4 of
    phases. The d=8 row is equally suggestive: 192 = 8 * 24, and 24 is the single-qubit
    Clifford group modulo phases.

    BUT MATCHING ORDERS PROVES NOTHING ABOUT THE ACTION. A group of order 46080 could act on
    F_2^4 through any quotient at all -- an earlier draft of this computation, with a broken
    coordinate map, reported the image as order 6. The action has to be computed.""")

    print("\n  PASS 8911-8913 -- the action, computed\n")
    res = {}
    for tag, mf, gf, e, co in (("d = 4  (Phi_4^4)", "_e8_cen_M.txt", "_e8_cen_gens.txt",
                                2, 46080),
                               ("d = 8  (Phi_8^2)", "_e8_cen8_M.txt", "_e8_cen8_gens.txt",
                                4, 192)):
        r = action_image(mf, gf, e, co)
        res[tag] = r
        print(f"      {tag}")
        print(f"        quotient                 : F_2^{r['k']} -> {r['geometry']}, "
              f"{r['qubits']} qubit(s)")
        print(f"        |C_W(M)|                 : {r['centraliser_order']}")
        print(f"        image on the quotient    : {r['image_order']}   "
              f"|Sp({r['k']},2)| = {r['sp_order']}   full: {r['image_is_full_symplectic']}")
        print(f"        kernel                   : {r['kernel_order']}")
        print()
    print("""    BOTH ARE EXACT. The centraliser surjects onto the full symplectic group of the
    geometry, and the kernel has precisely the order of the phases-and-Pauli part:

        d=4:  46080 = 64 . 720,   64 = |Z_4 o 2^(1+4)|, the two-qubit Pauli group with phases
        d=8:  192   = 32 . 6,     32 = 4 . 8, the one-qubit Pauli group with Z_8 phases

    That IS the defining structure of a Clifford group: phases and Pauli in the kernel,
    Sp on the quotient. So the centraliser of the regular element is the Clifford group OF
    the geometry that the same element produces. The two known facts are one fact.""")

    print("\n  PASS 8914-8915 -- and at odd primes it is NOT\n")
    print(f"      {'d':>3s} {'|C_W|':>9s} {'|Sp|':>7s} {'kernel':>7s} "
          f"{'Pauli group would need':>23s}  verdict")
    odd = {}
    for d, k, p in ((3, 4, 3), (5, 2, 5)):
        a = arith[d]
        ker = a["centraliser_order"] // a["sp_order"]
        need = p ** k
        odd[d] = {"kernel": ker, "pauli_order_needed": need, "possible": ker >= need}
        print(f"      {d:3d} {a['centraliser_order']:9d} {a['sp_order']:7d} {ker:7d} "
              f"{need:23d}  {'impossible' if ker < need else 'possible'}")
    print("""
    At d=3 the kernel has order 3 and a two-qutrit Pauli group needs at least 3^4 = 81; at
    d=5 the kernel has order 5 against 5^2 = 25. So the odd-prime centralisers are SCALARS
    TIMES SYMPLECTIC -- G32 = Z_3 x Sp(4,3) -- with no Pauli part at all. Only p=2 gives a
    genuine Clifford group.

    THAT IS THE SAME EXCEPTIONALITY AS BEFORE. Pass 8737-8776 found the descent kernel is
    Lagrangian exactly at p=2 and merely coisotropic at odd primes, because (p-1)/p = 1/2
    only for p=2. Here p=2 is again the only prime where the extra structure appears. Two
    different computations, one distinguished prime -- stated as an observation, not as a
    claimed common cause, which is not established.""")

    print("\n  PASS 8916-8917 -- open, and scope\n")
    print("""    NEW: the verified ACTION. The centraliser of the d-regular element surjects
    onto the full symplectic group of the geometry that element produces, with kernel of
    exactly the phases-and-Pauli order, at both d=4 and d=8. Matching orders was already
    available; the action was not, and an earlier broken version of this computation gave
    image order 6, so it was worth computing.
    CITED, NOT CLAIMED: Springer's centraliser law and the identification of G31/G32, which
    this repo already has at Pass 1039; Planat and Kibler (arXiv:0807.3650) for G31 as the
    two-qubit Clifford group; Planat (arXiv:1002.4287), already cited here at BT7154, for
    D4 and BW16 as real Clifford automorphism groups.
    NOT DONE: the d=3 action computed rather than bounded (the order argument settles that no
    Pauli part FITS, but the image itself is not computed here); whether the kernel is
    literally the extraspecial group or only has its order; the same question for Leech.
    NOT CLAIMED: any Monster result, and no physics.""")

    out = {
        "boundary": (
            "VERIFIED BY ACTION, not by order arithmetic: for W(E8), the centraliser of the "
            "d-regular element surjects onto the FULL symplectic group of the geometry that "
            "same element produces, with kernel of exactly the phases-and-Pauli order -- "
            "d=4 gives 46080 = 64 . |Sp(4,2)| and d=8 gives 192 = 32 . |Sp(2,2)|. So the "
            "Springer centraliser IS the Clifford group of its own geometry. At odd primes "
            "it is not: the kernel is far too small to contain a Pauli group"),
        "prior_art": {
            "pass1039": ("analysis/w33_pass1039_springer_tower.g (2026-07-26) already states "
                         "Springer's centraliser law for W(E8) and names G31 and G32"),
            "planat_kibler": ("arXiv:0807.3650, Unitary reflection groups for quantum fault "
                              "tolerance: G31 is a maximal index-2 subgroup of the two-qubit "
                              "Clifford group; Shephard-Todd G9 (order 192) also appears"),
            "planat_leech": ("arXiv:1002.4287, already cited in this repo at BT7154: the two- "
                             "and four-qubit real Clifford groups are the automorphism groups "
                             "of D4 and BW16. A DIFFERENT construction from this one -- it "
                             "reads the 24-dimensional space as a tensor product of Hilbert "
                             "spaces, where this quotients the lattice"),
            "what_is_new_here": ("the ACTION. Matching orders does not show the centraliser "
                                 "acts as the Clifford group of the geometry it builds; an "
                                 "earlier broken coordinate map in this very pass reported "
                                 "the image as order 6")},
        "order_arithmetic": arith,
        "verified_action": res,
        "odd_primes": {
            "table": odd,
            "conclusion": ("the odd-prime centralisers are scalars times symplectic -- "
                           "G32 = Z_3 x Sp(4,3) -- with no Pauli part; only p=2 gives a "
                           "genuine Clifford group"),
            "echo": ("p=2 was also the unique prime with a Lagrangian descent kernel at Pass "
                     "8737-8776. Two computations, one distinguished prime; stated as an "
                     "observation, not a claimed common cause")},
        "method_note": ("the quotient is modelled as im((I-M)^(e-1) mod 2), which works "
                        "because that operator is the level-1 class map of the pi-adic "
                        "filtration (Pass 8861-8884). The row-versus-column convention was "
                        "caught by testing invariance of the model rather than assuming it"),
        "not_done": ["the d=3 action computed rather than bounded",
                     "whether the kernel is literally extraspecial or only has its order",
                     "the same question for Leech"],
    }
    fp = ROOT / "data" / "PART_W33_PASS8909_8924_CENTRALISER_CLIFFORD.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
