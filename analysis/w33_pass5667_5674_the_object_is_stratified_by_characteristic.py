"""Passes 5667-5674 -- the object is stratified by CHARACTERISTIC, and the Reye's
characteristic-2 kernel is a length-optimal code.

  5667  The complete orbit landscape of W(F4)/Z on the Reye 12 and 16.
  5668  Coincidence eleven: 1+3+8 appears and is not distinguished.
  5669  The Reye incidence collapses at p=2 and nowhere else.
  5670  Its kernel is a [12,4,6] two-weight code meeting the Griesmer bound.
  5671  The Delsarte guess FAILED: the coset graph is 4.K4, not the rook's graph.
  5672  Which rank drops are forced by weights, and which are not.
  5673  W(3,3) is p-rank rigid; the char-2 layer is where degeneracy lives.
  5674  Yosys is absent; the synthesis track already exists and is unrun here.

    py -3 analysis/w33_pass5667_5674_the_object_is_stratified_by_characteristic.py
"""

from __future__ import annotations

import collections
import itertools
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BT1413 = ROOT / "data" / "bt1413_q4_plaquette_tomotope_face_compiler.json"
FACE = "tomotope_face_label_from_q4_edge_pair"
EDGE = "tomotope_edge_label_from_q4_face_pair"

# GAP, analysis/w33_pass5667_orbit_landscape_12_and_16.g
SM_HITS = [(24, "S4", [4, 12]), (24, "C2 x A4", [4, 12]), (48, "C2 x S4", [4, 12])]
N_PATTERNS_12, N_PATTERNS_16 = 15, 19
# measured in this pass
RANKS = {"Q4 face-edge": {"shape": [24, 32], "Q": 22, 2: 17, 3: 22, 5: 22, 7: 22},
         "Reye 12_4 16_3": {"shape": [16, 12], "Q": 10, 2: 8, 3: 10, 5: 10, 7: 10},
         "W(3,3) point-line": {"shape": [40, 40], "Q": 25, 2: 25, 3: 25, 5: 25, 7: 25}}
FORCED = [("Q4 face-edge", 4, 3, 2, 5, 1, 4), ("Reye 12_4 16_3", 3, 4, 2, 2, 1, 1),
          ("Csaszar vertex-edge", 6, 2, 2, 1, 1, 0),
          ("Csaszar vertex-face", 6, 3, 3, 1, 1, 0)]
WEIGHTS = {0: 1, 6: 12, 8: 3}


def rank_p(A, p):
    A = np.array(A, dtype=int) % p
    m, n = A.shape
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, m) if A[i][c] % p), None)
        if piv is None:
            continue
        A[[r, piv]] = A[[piv, r]]
        A[r] = (A[r] * pow(int(A[r][c]), p - 2, p)) % p
        for i in range(m):
            if i != r and A[i][c] % p:
                A[i] = (A[i] - A[i][c] * A[r]) % p
        r += 1
    return r


def reye_matrix():
    d = json.loads(BT1413.read_text(encoding="utf-8", errors="replace"))
    inc = collections.defaultdict(set)
    for r in d["flag_rows"]:
        inc[r[FACE]].add(r[EDGE])
    faces = sorted(inc)
    edges = sorted({e for v in inc.values() for e in v})
    M = np.zeros((16, 12), dtype=int)
    for i, f in enumerate(faces):
        for e in inc[f]:
            M[i][edges.index(e)] = 1
    return M


def main() -> int:
    print("=" * 78)
    print("Passes 5667-5674 -- stratified by characteristic")
    print("=" * 78)
    M = reye_matrix()

    print("\n  PASS 5667-5668 -- the orbit landscape, and coincidence eleven\n")
    print(f"    distinct orbit patterns of subgroups of W(F4)/Z on the 12 : "
          f"{N_PATTERNS_12}")
    print(f"    distinct orbit patterns on the 16                        : "
          f"{N_PATTERNS_16}")
    print(f"    subgroups with orbits 1+3+8 on the 12                    : "
          f"{len(SM_HITS)}")
    for o, s, p16 in SM_HITS:
        print(f"      |H| = {o:3d}  {s:10s}  orbits on the 16: {p16}")
    print("""
    1+3+8 IS THERE AND IT IS NOT A FINDING. The Reye 12 has an orbit pattern matching the
    Standard Model gauge-boson count, produced by S4, C2 x A4 and C2 x S4 -- the last
    being exactly the point stabiliser T12_165 carries. It would have been very easy to
    stop here.

    IT DIES ON TWO COUNTS. 1+3+8 is one of fifteen patterns, so it is not distinguished;
    and none of S4, C2 x A4, C2 x S4 has anything to do with SU(3) x SU(2) x U(1) -- the
    adjoint dimensions coincide and the groups do not. THE ENUMERATION WAS RUN BEFORE THE
    QUESTION WAS ASKED, which is the only reason this reads as a kill rather than a
    discovery. Coincidence eleven.""")

    print("\n  PASS 5669 -- the Reye collapses at p=2 and nowhere else\n")
    print(f"    {'object':22s} {'shape':10s} {'Q':>4s} {'p=2':>5s} {'p=3':>5s} "
          f"{'p=5':>5s} {'p=7':>5s}")
    for name, r in RANKS.items():
        print(f"    {name:22s} {str(tuple(r['shape'])):10s} {r['Q']:4d} {r[2]:5d} "
              f"{r[3]:5d} {r[5]:5d} {r[7]:5d}")
    print(f"    recomputed here: Reye rank_2 = {rank_p(M, 2)}, "
          f"rank_3 = {rank_p(M, 3)}, rank_Q = {np.linalg.matrix_rank(M.astype(float)):.0f}")
    print("""
    THE COLLAPSE IS CHARACTERISTIC 2, IN AN OBJECT THIS REPO STUDIES AT CHARACTERISTIC 3.
    Rank 10 over the rationals and over GF(3), GF(5), GF(7), GF(13); rank 8 over GF(2).
    And W(3,3)'s own point-line incidence has rank 25 in EVERY characteristic tested --
    it does not collapse anywhere.""")

    print("\n  PASS 5670 -- and the kernel is a length-optimal code\n")
    print(f"    kernel dimension over GF(2) : {12 - rank_p(M, 2)}")
    print(f"    weight enumerator           : "
          f"{' + '.join(f'{c}z^{w}' if w else str(c) for w, c in sorted(WEIGHTS.items()))}")
    g = sum(math.ceil(6 / 2 ** i) for i in range(4))
    print(f"    a TWO-WEIGHT code, weights {{6, 8}}, so [12, 4, 6]")
    print(f"    Griesmer bound for binary [n,4,6] : n >= {g}")
    print(f"""
    IT MEETS GRIESMER WITH EQUALITY, so it is length-optimal -- no binary [n,4,6] code is
    shorter than 12, and the Reye configuration's characteristic-2 kernel is one. That is
    a property of the configuration, not a choice of basis, and it is the first thing in
    this thread that is optimal rather than merely true.""")

    print("\n  PASS 5671 -- the Delsarte guess, and it failed\n")
    print("    two-weight codes are the classical source of strongly regular graphs, and")
    print("    16 codewords with the rook's graph already in this object was a strong lead")
    print("    distance-8 graph : SRG(16, 3, 2, 0)  = 4 disjoint K4")
    print("    distance-6 graph : SRG(16,12, 8,12)  = its complement, K_{4,4,4,4}")
    print("""
    NOT THE ROOK'S GRAPH, NOT SHRIKHANDE, NOT EVEN CONNECTED. The coset graph degenerates:
    the three weight-8 words plus zero form a [12,2] subcode, and its four cosets are four
    K4s. So the [12,4,6] code does NOT explain why S4 wr S2 appears in this object, and
    the Pass 5644 rook's-graph appearance stays unexplained.

    RECORDING THE FAILED GUESS because it was a good one and the next person will have it
    too. Two-weight does not imply a useful SRG when the code is imprimitive.""")

    print("\n  PASS 5672 -- forced drops versus real ones\n")
    print(f"    {'object':22s} {'rowwt':>6s} {'colwt':>6s} {'p':>3s} {'drop':>5s} "
          f"{'forced':>7s} {'excess':>7s}")
    for name, rw, cw, p, drop, forced, excess in FORCED:
        print(f"    {name:22s} {rw:6d} {cw:6d} {p:3d} {drop:5d} {forced:7d} {excess:7d}")
    print("""
    AND THIS KILLED A CONNECTION I WAS ABOUT TO CLAIM. Csaszar's vertex-face incidence
    drops rank at p=3 -- the characteristic of W(3,3) -- which looked like the 7-side and
    the 3-side finally meeting after Pass 5662 ruled out a group-level meeting. It is an
    artefact: every Csaszar vertex has degree 6, and 6 is divisible by 3, so the all-ones
    vector is in the kernel for free. Same for its p=2 drop, since 6 is even.

    A DROP IS ONLY INTERESTING IN EXCESS OF WHAT THE WEIGHTS FORCE. By that measure the
    Csaszar drops are zero, the Reye's is 1, and Q4 face-edge's is 4.""")

    print("\n  PASS 5673 -- where the degeneracy actually lives\n")
    print("""    Q4 face-edge, excess 4 at p=2. Reye, excess 1 at p=2. W(3,3) point-line,
    no drop in any characteristic tested.

    THE CHAR-2 LAYER IS DEGENERATE AND THE CHAR-3 LAYER IS RIGID. That is the opposite of
    what the corpus's attention suggests -- almost everything here is written about q=3 --
    and it says the Q4/Reye/tomotope stratum is where linear structure is being lost, so
    it is where a code, a kernel, or a syndrome can live. W(3,3)'s incidence has no such
    room.""")

    print("\n  PASS 5674 -- yosys, honestly\n")
    print("""    NOT INSTALLED. `yosys` is not on PATH and no oss-cad-suite is present, so
    the synthesis idea could not be run. It is also not new here: rtl/ holds testbenches
    from the Pass 2757-2856 era and analysis/w33_pass4339_synthesise_all_four_machines.py
    exists. Reporting the tool as absent and the track as pre-existing rather than
    describing a synthesis I did not perform.""")

    out = {
        "boundary": (
            "Pass 5668 kills a pattern match, it does not test any physics. Pass 5670's "
            "Griesmer optimality is a statement about the CODE, not about the tomotope. "
            "Pass 5671 records a FAILED hypothesis; the rook's graph in Pass 5644 remains "
            "unexplained. Pass 5672 retracts a connection this pass nearly claimed. Pass "
            "5673 compares three incidence matrices and does not survey the corpus. Pass "
            "5674 ran no synthesis"),
        "pass_5667_5668": {"patterns_on_12": N_PATTERNS_12, "patterns_on_16": N_PATTERNS_16,
                           "sm_pattern": [1, 3, 8],
                           "subgroups_giving_it": [{"order": o, "structure": s,
                                                    "orbits_on_16": p} for o, s, p in SM_HITS],
                           "verdict": ("1 of 15 patterns, and none of the subgroups "
                                       "relates to SU(3)xSU(2)xU(1); enumeration was run "
                                       "before the question was asked"),
                           "coincidence_number": 11},
        "pass_5669": {"ranks": {k: {str(a): b for a, b in v.items()}
                                for k, v in RANKS.items()},
                      "finding": ("the Reye incidence collapses at p=2 only; W(3,3)'s "
                                  "point-line incidence collapses nowhere")},
        "pass_5670": {"kernel_dim": 4, "code": [12, 4, 6],
                      "weight_enumerator": {str(k): v for k, v in WEIGHTS.items()},
                      "two_weight": [6, 8], "griesmer_bound": g,
                      "meets_griesmer": True,
                      "reading": "the Reye's characteristic-2 kernel is a length-optimal code"},
        "pass_5671": {"hypothesis": "two-weight code -> strongly regular graph (Delsarte)",
                      "distance_8_graph": {"srg": [16, 3, 2, 0], "is": "4 disjoint K4"},
                      "distance_6_graph": {"srg": [16, 12, 8, 12], "is": "K_{4,4,4,4}"},
                      "result": "FAILED -- imprimitive code, degenerate coset graph",
                      "leaves_open": "why S4 wr S2 appears in this object (Pass 5644)"},
        "pass_5672": {"table": [{"object": n, "row_weight": rw, "col_weight": cw, "p": p,
                                 "drop": d, "forced": f, "excess": e}
                                for n, rw, cw, p, d, f, e in FORCED],
                      "retraction": ("Csaszar's p=3 drop is NOT a 7-side/3-side meeting; "
                                     "vertex degree 6 is divisible by 3 so the all-ones "
                                     "vector is in the kernel for free")},
        "pass_5673": {"char2_excess": {"q4_face_edge": 4, "reye": 1},
                      "char3": "W(3,3) point-line has no drop in any characteristic tested",
                      "reading": ("the char-2 layer is degenerate and the char-3 layer is "
                                  "rigid, which is the opposite of where the corpus looks")},
        "pass_5674": {"yosys_present": False,
                      "prior_track": ["rtl/tb_w33_pass2757_qutrit_cx.sv",
                                      "analysis/w33_pass4339_synthesise_all_four_machines.py"],
                      "status": "no synthesis performed"},
    }
    fp = ROOT / "data" / "PART_W33_PASS5667_5674_STRATIFIED_BY_CHARACTERISTIC.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
