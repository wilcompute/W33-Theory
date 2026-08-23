"""Passes 7309-7316 -- the rank-24 rung works on E8^3, and is a DIAGONAL. Leech is still the test.

  7309  E8^3 at d=9 gives W(3,3). Verified SRG(40,12,2,4).
  7310  But it is a diagonal of three copies. My own result, deflated.
  7311  Which sharpens why Leech matters: it is not a direct sum.
  7312  A hardcoded np.eye(8) that made every 24x24 order look infinite.
  7313  The spread selection: 5 distinct spreads out of 36 so far.
  7314  What the three verified rungs actually are.
  7315  Open.
  7316  Scope.

    py -3 analysis/w33_pass7309_7316_the_diagonal_proxy.py
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


def main() -> int:
    print("=" * 78)
    print("Passes 7309-7316 -- the diagonal proxy, and why Leech is still the test")
    print("=" * 78)

    print("\n  PASS 7309 -- E8^3 at d=9 gives W(3,3)\n")
    print("""    The element is FORCED, not searched: on E8^3 put M(x,y,z) = (Jz, x, y) with J the
    order-3 element of W(E8). Then M^3 = J (+) J (+) J so M has order 9, and M(x,y,z) =
    (x,y,z) forces x = y = z with Jz = z, hence z = 0 -- fixed-point-free with no search.

    det(I - M) = Phi_9(1)^4 = 81, and E8^3's 720 minimal vectors fall into 80 classes of
    EXACTLY 9, giving 40 projective points of 18 vectors each. With the form
    A(x,y) = (M^3 x, y) - (x, M^3 y) the induced graph has degree 12 and spectrum
    12^1 2^24 (-4)^15: SRG(40,12,2,4), i.e. W(3,3).

    So the rank-24 rung of the tower is realised, on a Niemeier lattice, without Co0.""")

    print("\n  PASS 7310-7311 -- and it is a DIAGONAL, which deflates it\n")
    print("""    The form that works is built from M^3 = J (+) J (+) J -- the order-3 part -- and
    that is a warning. Checked directly:

        every one of the 80 classes draws exactly 3 vectors from EACH of the three blocks
        in every block, the E8-class determines the E8^3-class bijectively (80 of 80)

    So each E8^3 class is a MERGE of one class from each copy, and the 40 points are the
    DIAGONAL of three copies of the E8 d=3 fibration. It is a genuine rank-24 realisation of
    W(3,3), and it is not a new geometry. Recording that rather than reporting a rank-24
    result and leaving the reader to assume it was independent.

    AND THAT SHARPENS WHY LEECH IS STILL THE TEST. Leech is NOT a direct sum, so its d=9
    fibration -- if the element exists -- cannot be a diagonal of anything. E8^3 shows the
    arithmetic carries through to rank 24; it cannot show the geometry is new there. Only a
    non-decomposable rank-24 lattice can, and Leech is the one the census flags as richest.""")

    print("\n  PASS 7312 -- a bug that made 24x24 orders look infinite\n")
    print("""    order_of() hardcoded `I = np.eye(8)`. For a 24x24 matrix that comparison can
    never succeed, so it returned None for EVERY rank-24 element -- an order-9 map looked
    like it had no finite order at all. The first E8^3 run aborted on exactly that, with
    det(I-M) = 81 and M^3 = J(+)J(+)J both already correct on screen.

    THE TELL WAS THE DISAGREEMENT: two checks passed and the third was not merely false but
    None. A helper written for one rank and reused at another is worth suspecting first.""")

    print("\n  PASS 7313-7314 -- the tower as it now stands\n")
    print(f"      {'lattice':>7s} {'rank':>5s} {'d':>3s} {'classes':>8s} {'per class':>10s} "
          f"{'geometry':>10s}  {'independent?':>13s}")
    for lat, rk, d, cl, pc, geo, ind in (
            ("E8", 8, 3, 80, 3, "W(3,3)", "yes"),
            ("E8", 8, 4, 15, 16, "W(3,2)", "yes"),
            ("E8^3", 24, 9, 80, 9, "W(3,3)", "NO -- diagonal"),
            ("Leech", 24, 9, 80, 2457, "?", "would be, UNTESTED")):
        print(f"      {lat:>7s} {rk:5d} {d:3d} {cl:8d} {pc:10d} {geo:>10s}  {ind:>13s}")
    print("""
    Also from the spread work: sampling order-4 elements produced 5 DISTINCT spreads of the
    36 that W(3,3) has. Whether the map from order-4 elements onto spreads is surjective is
    not established -- 5 of 36 is what was seen, not a claim about the rest.""")

    print("\n  PASS 7315-7316 -- open, and scope\n")
    print("""    NEW: the E8^3 d=9 realisation, and its identification as a diagonal.
    CORRECTED: the order_of helper, which silently broke every rank-24 order test.
    NOT DONE: Leech d=9 (needs Co0 generators); K12 built; whether the order-4 -> spread map
    is onto; alpha(W(3,9)); q=11 at 68; Coolsaet unread.
    NOT CLAIMED: any Monster result, and no physics.""")

    out = {
        "boundary": (
            "E8^3 at d=9 DOES give W(3,3), verified SRG(40,12,2,4) -- but it is a DIAGONAL "
            "of three copies of the E8 d=3 fibration, not a new geometry. Since Leech is not "
            "a direct sum, its d=9 fibration could not be a diagonal, so Leech remains the "
            "real test and is UNTESTED"),
        "e8cubed": {
            "element": "M(x,y,z) = (Jz, x, y), forced not searched",
            "order": 9, "det_I_minus_M": 81, "M3": "J (+) J (+) J",
            "minimal_vectors": 720, "classes": 80, "per_class": 9,
            "projective_points": 40, "vectors_per_point": 18,
            "form": "(M^3 x, y) - (x, M^3 y)",
            "graph": "SRG(40,12,2,4), spectrum 12^1 2^24 (-4)^15",
            "gives_W33": True},
        "the_deflation": {
            "block_distribution": "every class draws exactly 3 vectors from each of 3 blocks",
            "bijective_per_block": "E8-class determines E8^3-class, 80 of 80, all three blocks",
            "verdict": ("a DIAGONAL of three copies of the d=3 fibration; a genuine rank-24 "
                        "realisation of W(3,3) but not a new geometry"),
            "why_leech_still_matters": ("Leech is not a direct sum, so its d=9 fibration "
                                        "cannot be a diagonal of anything")},
        "order_of_bug": {
            "what": "order_of() hardcoded I = np.eye(8)",
            "effect": "returned None for EVERY 24x24 matrix; an order-9 map looked orderless",
            "how_caught": ("two checks passed and the third returned None rather than False, "
                           "with det(I-M) = 81 and M^3 = J(+)J(+)J already correct on screen"),
            "fixed": "I = np.eye(M.shape[0])"},
        "tower": [
            {"lattice": "E8", "rank": 8, "d": 3, "geometry": "W(3,3)", "independent": True},
            {"lattice": "E8", "rank": 8, "d": 4, "geometry": "W(3,2)", "independent": True},
            {"lattice": "E8^3", "rank": 24, "d": 9, "geometry": "W(3,3)",
             "independent": False, "note": "diagonal"},
            {"lattice": "Leech", "rank": 24, "d": 9, "geometry": None,
             "independent": "would be", "status": "UNTESTED, needs Co0"}],
        "spreads": {"distinct_found": 5, "total_in_W33": 36,
                    "surjectivity": "NOT established"},
        "not_done": ["Leech d=9 (needs Co0 generators)", "K12 built",
                     "whether order-4 -> spread is onto", "alpha(W(3,9))", "q=11 at 68",
                     "Coolsaet unread"],
    }
    fp = ROOT / "data" / "PART_W33_PASS7309_7316_DIAGONAL_PROXY.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
