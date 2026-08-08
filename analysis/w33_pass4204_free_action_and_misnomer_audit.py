#!/usr/bin/env python3
"""Pass 4204 -- the well-posed question, and what the misnomer actually cost.

Pass 4203 established that the 81-frame graph is a SCHREIER graph on a coset space, not a
Cayley graph of ASp(4,3).  The Schreier framing makes "is there a regular universal
presentation" into a question about POINT STABILISERS, which is decidable directly instead
of by searching subsets.  Three things follow, and the second one is a retraction.

(a) NO OPCODE ACTS FREELY.  A Schreier graph is regular whenever every generator is
    fixed-point-free.  Every linear map fixes the origin, so no Clifford opcode is free;
    only the four translations are.  That looks like a one-line proof that no universal
    presentation is ever regular.

(b) IT IS NOT A PROOF, AND THE COUNTEREXAMPLE IS OUR OWN PASS 4201.  Freeness is
    SUFFICIENT, not necessary: a fixed point costs degree only if the resulting loop is not
    already absorbed.  Pass 4201's "regular computing presentation" S_f + Z0..Z3 is
    8-regular even though S_f fixes 27 frames -- because every edge S_f draws duplicates an
    edge Z3 already drew.  S_f contributes NOTHING to the graph.  What Pass 4201 measured
    was the Cayley graph of the translation group alone: the 4-dimensional discrete torus
    C_3^4.  Its Ramanujan property is a textbook fact about an abelian group, not a
    discovery about the machine.  This pass checks that by predicting the whole spectrum
    from the torus character formula and comparing.

(c) THE CORRECT STATEMENT, AND THE CONTAMINATION AUDIT.  Regularity is not freeness but
    constancy of the DEFICIENCY -- loops plus collapsed multi-edges, per frame.  For the
    real universal ISA the deficiency is supported on the opcodes' fixed-point subspaces,
    which is a structural description of the irregularity rather than a degree range.  And
    the diameter results of Pass 2866 were computed on the group, not on the 81 frames, so
    the misnomer cannot have touched them -- verified against the certificate.

    py -3 analysis/w33_pass4204_free_action_and_misnomer_audit.py
"""

from __future__ import annotations

import json
from collections import Counter
from itertools import combinations
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
TV = [(a, b, c, d) for a in range(3) for b in range(3)
      for c in range(3) for d in range(3)]
TI = {t: i for i, t in enumerate(TV)}
ID4 = tuple(tuple(1 if i == j else 0 for j in range(4)) for i in range(4))

LIN = {"F_p": ((0, 2, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
       "F_f": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 2), (0, 0, 1, 0)),
       "S_p": ((1, 0, 0, 0), (1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
       "S_f": ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 1, 1)),
       "CX_pf": ((1, 0, 0, 0), (0, 1, 0, 2), (1, 0, 1, 0), (0, 0, 0, 1)),
       "CX_fp": ((1, 0, 1, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 2, 0, 1))}


def mv(A, v):
    return tuple(sum(A[i][k] * v[k] for k in range(4)) % 3 for i in range(4))


def pool():
    c = {nm: (A, (0, 0, 0, 0)) for nm, A in LIN.items()}
    for i in range(4):
        c[f"Z{i}"] = (ID4, tuple(1 if j == i else 0 for j in range(4)))
    return c


def act(g, x):
    M, t = g
    return tuple((mv(M, x)[k] + t[k]) % 3 for k in range(4))


def fixed(g):
    return sum(1 for x in TV if act(g, x) == x)


def graph(gens):
    A = np.zeros((81, 81))
    for g in gens:
        for i, x in enumerate(TV):
            j = TI[act(g, x)]
            A[i, j] = 1
            A[j, i] = 1
    np.fill_diagonal(A, 0)
    return A


def edge_set(g):
    """Undirected edges a generator draws, loops discarded."""
    return {frozenset((TI[x], TI[act(g, x)])) for x in TV if act(g, x) != x}


def main() -> int:
    C = pool()

    print("=" * 78)
    print("Pass 4204(a) -- which generators act FREELY on the 81 frames?")
    print("=" * 78)
    print("  freeness is SUFFICIENT for a regular Schreier graph.  Who has it?\n")
    print("  generator   fixed frames   free?")
    fx = {}
    for nm in list(LIN) + [f"Z{i}" for i in range(4)]:
        f = fixed(C[nm])
        fx[nm] = f
        print(f"  {nm:9s}   {f:9d}      {'yes' if f == 0 else 'NO'}")
    free = [nm for nm, f in fx.items() if f == 0]
    print(f"\n  free generators: {', '.join(free)} -- the four translations, and only those.")
    print("  Every linear map fixes the origin, so no Clifford opcode can ever be free.")
    print("  The free part of the machine is exactly its abelian address arithmetic:")
    print("  <Z0..Z3> has order 81 and acts sharply transitively on the frames.")

    print()
    print("=" * 78)
    print("Pass 4204(b) -- RETRACTION: freeness is not necessary, and Pass 4201 shows it")
    print("=" * 78)
    combo = ["S_f", "Z0", "Z1", "Z2", "Z3"]
    A = graph([C[nm] for nm in combo])
    d = A.sum(axis=1)
    e_sf = edge_set(C["S_f"])
    e_z3 = edge_set(C["Z3"])
    absorbed = e_sf <= e_z3
    A_trans = graph([C[f"Z{i}"] for i in range(4)])
    identical = bool(np.array_equal(A, A_trans))
    print(f"  Pass 4201's set: {' + '.join(combo)}")
    print(f"  degrees {sorted(set(d.tolist()))}  -> regular, yet S_f fixes {fx['S_f']} frames")
    print(f"  S_f draws {len(e_sf)} edges; every one of them is already a Z3 edge: {absorbed}")
    print(f"  so the graph equals the translation graph alone: {identical}")

    # Predict the whole spectrum from the C_3^4 character formula, independently of numpy.
    pred = Counter()
    for a in range(5):
        from math import comb
        pred[3 * a - 4] += comb(4, a) * 2 ** (4 - a)
    obs = Counter(int(round(v)) for v in np.linalg.eigvalsh(A))
    match = pred == obs
    print("\n  predicted from the discrete-torus characters (each coordinate gives 2 or -1):")
    for lam in sorted(pred, reverse=True):
        print(f"     {lam:+3d} x{pred[lam]:<3d}   observed x{obs.get(lam, 0)}")
    print(f"  spectra agree exactly: {match}")
    print(f"""
  So Pass 4201's headline is WITHDRAWN.  It reported "the instruction layer CAN be
  Ramanujan -- at five generators, not four".  The five-generator graph is the
  4-dimensional discrete torus C_3^4 with its four standard generators, and S_f is
  invisible in it.  |lambda_2| = 5 <= 2*sqrt(7) = 5.2915 is true and is a fact about an
  abelian group of order 81 that has been known for as long as anyone has taken characters
  of Z/3.  It is not a fact about the instruction layer, because the instruction is not in
  the graph.

  Pass 4201's own numbers already said so and were not read: it reported group order 243,
  i.e. translations times an order-3 element, nowhere near the 4,199,040 of ASp(4,3).  A
  presentation that is regular because its only non-abelian generator draws no edges is
  regular in the way an empty room is quiet.""")

    print()
    print("=" * 78)
    print("Pass 4204(c) -- the correct criterion, and where the irregularity lives")
    print("=" * 78)
    print("""  Regular is not 'free'; it is 'the DEFICIENCY is constant', where the deficiency of a
  frame is the number of loops at it plus the number of multi-edges collapsed at it.  For
  the universal 4-opcode ISA, where does the deficiency sit?\n""")
    isa = ["F_p", "F_f", "CX_pf", "CX_fp"]
    Ai = graph([C[nm] for nm in isa])
    di = Ai.sum(axis=1)
    full = 2 * len(isa)
    defic = {TV[i]: int(full - di[i]) for i in range(81)}
    by_def = Counter(defic.values())
    print(f"  ISA {' + '.join(isa)}: degrees {int(di.min())} to {int(di.max())}"
          f" (max possible {full})")
    print("  deficiency   frames")
    for k in sorted(by_def):
        print(f"  {k:9d}   {by_def[k]}")

    fixloci = {nm: {x for x in TV if act(C[nm], x) == x} for nm in isa}
    union = set().union(*fixloci.values())
    positive = {x for x, v in defic.items() if v > 0}
    contained = positive <= union
    print(f"\n  frames with positive deficiency : {len(positive)}")
    print(f"  union of the opcodes' fixed loci : {len(union)}")
    print(f"  the first sits inside the second : {contained}")
    print(f"""
  So the irregularity of the instruction graph is not a degree range, it is a LOCUS: every
  frame that loses degree lies on some opcode's fixed-point subspace, and those subspaces
  are linear, so they all pass through the origin.  The graph is irregular because the
  machine has a distinguished address and the opcodes cannot move it.  That is the same
  fact as Pass 2774's synthesis result -- a Clifford-only register with no load port is
  provably constant because symplectic maps fix zero -- arriving from the other side, on
  the graph rather than in the netlist.""")

    print()
    print("=" * 78)
    print("Pass 4204(d) -- did the misnomer contaminate the diameter results?")
    print("=" * 78)
    src = ROOT / "data" / "PART_W33_PASS2866_2867_ISA_DIAMETER_AND_SCRAMBLING.json"
    clean = False
    if src.exists():
        d2866 = json.loads(src.read_text(encoding="utf-8"))["pass_2866"]
        clean = d2866.get("group_order") == 4199040
        print(f"  Pass 2866 searched {d2866.get('group_order'):,} elements; "
              f"that is the GROUP ASp(4,3), not the 81-frame quotient: {clean}")
        print("""
  UNAFFECTED.  Diameter 19, mean 14.18 and the growth series were computed on the group's
  own Cayley graph, where the action is free by construction and the graph really is
  regular.  The misnomer applied to the 81-frame Schreier graph, a different object those
  passes never touched.  One wrong name, on one object; the results on the other object
  stand.""")
    else:
        print("  Pass 2866 certificate not found; contamination NOT verified")

    out = {
        "fixed_points": fx,
        "free_generators": free,
        "free_generators_are_exactly_the_translations": sorted(free) == [f"Z{i}" for i in range(4)],
        "pass4201_retraction": {
            "set": combo,
            "regular": bool(d.min() == d.max()),
            "S_f_fixed_frames": fx["S_f"],
            "S_f_edges_absorbed_by_Z3": bool(absorbed),
            "graph_equals_translation_graph": identical,
            "torus_spectrum_matches": bool(match),
            "verdict": ("Pass 4201's regular 'computing' presentation is the discrete torus "
                        "C_3^4; its Clifford generator draws no edges, so its Ramanujan "
                        "property is a fact about an abelian group, not the instruction layer"),
        },
        "irregularity_locus": {
            "isa": isa,
            "degree_min": int(di.min()), "degree_max": int(di.max()),
            "deficient_frames": len(positive),
            "union_of_fixed_loci": len(union),
            "deficiency_supported_on_fixed_loci": bool(contained),
        },
        "criterion": ("a Schreier graph is regular iff the deficiency (loops plus collapsed "
                      "multi-edges) is constant; freeness is sufficient, not necessary"),
        "diameter_results_unaffected": bool(clean),
    }
    path = ROOT / "data" / "PART_W33_PASS4204_FREE_ACTION_AUDIT.json"
    path.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    text = json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    print(f"\nwrote {path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
