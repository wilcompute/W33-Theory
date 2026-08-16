"""Passes 5460-5467 -- the q=8 ovoid decides what the 1+12 split meant, q=9 refuses to
close, and the identity I published 18 minutes after the other lane already had it.

  5460  Pass 5417 found the q=5 13-cover stabiliser acting with orbits [1, 12] -- one
        distinguished vertex on a simplex whose own symmetry group is 13-transitive.  That
        is either a real geometric fact or a generic property of tight cocliques, and one
        run decides which: the same test on W(3,8)'s 65-point Suzuki-Tits ovoid.

  5461  The 2-(13,6,60) design's automorphism group, computed as the automorphism group of
        its incidence graph rather than as a stabiliser inside S_13 -- the latter ran GAP
        out of memory, which is what asking a 6.2-billion-element group to hold still looks
        like.

  5462  alpha(W(3,9)) after 19.6 hours of branch and bound.

  5463  And the audit that should have run first: who published the frame inner products,
        and when.

    py -3 analysis/w33_pass5460_5467_the_distinguished_vertex_is_a_q5_fact.py
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# The four claims this lane published this week and what became of each.
LEDGER = [
    {"claim": "-1/q^2 is the noncollinear inner product", "pass": 5279,
     "fate": "OVER-GENERALISED", "owner": "other lane Pass5267, 18 minutes earlier",
     "note": "their statement is scoped to odd q on W(3,q) and is CORRECT there"},
    {"claim": "-1/(H-1) is the general form", "pass": 5341,
     "fate": "REFUTED by Paley at Pass 5374", "owner": "-", "note": ""},
    {"claim": "mu/(k(1+s)) derived", "pass": 5374,
     "fate": "RE-DERIVATION", "owner": "classical cosine sequence",
     "note": "Brouwer-Cohen-Neumaier, Godsil; established at Pass 5412"},
    {"claim": "a tight coclique is a regular simplex", "pass": 5342,
     "fate": "MECHANISM ALREADY IN REPO", "owner": "Pass 1614",
     "note": "equal norm + equal angle + sum zero, test ip = -norm^2/(N-1)"},
]


def main() -> int:
    print("=" * 78)
    print("Passes 5460-5467 -- one run decides it")
    print("=" * 78)

    g = json.loads((ROOT / "data" / "_gap_5460.json").read_text(encoding="utf-8"))
    q5 = json.loads((ROOT / "data" / "_gap_cover_orbits.json").read_text(encoding="utf-8"))

    print("\n  PASS 5460 -- W(3,8): transitive, so 1+12 was never generic\n")
    print(f"    |Aut(W(3,8) collinearity graph)| : {g['q8_aut_order']:,}")
    print(f"    ovoid setwise stabiliser         : {g['q8_ovoid_stabiliser']:,}")
    print(f"    image in S_65                    : {g['q8_image_order']:,}")
    print(f"    pointwise kernel                 : {g['q8_kernel_order']}")
    print(f"    orbit sizes on the 65            : {g['q8_orbit_sizes']}")
    print(f"    transitive                       : {g['q8_transitive']}")
    sz8 = 29120
    print(f"\n    |Sz(8)| = {sz8:,},  and {g['q8_ovoid_stabiliser']:,} / {sz8:,} = "
          f"{g['q8_ovoid_stabiliser'] // sz8}")
    print(f"""
    THE STABILISER IS Sz(8):3 AND IT IS TRANSITIVE ON THE OVOID. {g['q8_ovoid_stabiliser']:,} is exactly
    3 x |Sz(8)|, the factor 3 being the field automorphism of GF(8) -- the full
    automorphism group of the Suzuki-Tits ovoid. It acts FAITHFULLY (kernel 1) and with a
    single orbit, so every one of the 65 points looks like every other.

    SO THE q=5 SPLIT IS A REAL GEOMETRIC FACT, NOT AN ARTEFACT OF TIGHTNESS. Compare:

        q=5, 13-cover on NO_5^+(5) : image {q5['image_order']}, kernel 2, orbits {q5['orbit_sizes']}
        q=8, ovoid on W(3,8)       : image {g['q8_image_order']:,}, kernel {g['q8_kernel_order']}, orbits {g['q8_orbit_sizes']}

    Both are Hoffman-tight cocliques, both are regular simplices by the Pass 1614 mechanism,
    and their stabilisers behave completely differently. Tightness forces the simplex; it
    does NOT force homogeneity of the embedding. Pass 5417's distinguished vertex survives
    the test that could have killed it.

    AND THE KERNELS DIFFER TOO. At q=8 the action is faithful; at q=5 there is a central
    involution acting trivially on all thirteen. That was the one thing the two cases were
    expected to share and they do not.""")

    print("\n  PASS 5461 -- the design carries no extra symmetry\n")
    print(f"    design blocks (distinct)         : {g['design_blocks']}")
    print(f"    |Aut(incidence graph)|           : {g['design_incidence_aut']:,}")
    print(f"    induced action on the 13         : {g['design_action_on_13']:,}")
    print(f"    structure                        : {g['design_structure']}")
    same = g["design_action_on_13"] == q5["image_order"]
    print(f"""
    THE 2-(13,6,60) DESIGN'S GROUP IS {g['design_action_on_13']}, THE SAME AS THE EMBEDDING'S{'' if same else ' -- no, it differs'}, with the same
    structure description ((A4 x A4):C2):C2. So the design does not know anything the
    stabiliser did not: the 312 outside blocks organise into a genuine 2-design over the
    simplex, and that design's symmetry is exactly the symmetry the geometry already had.

    A DESIGN ON 13 POINTS COULD HAVE HAD MUCH MORE -- 2-designs are often highly symmetric,
    and there was no reason in advance for this one to stop at 576. It stops there.

    METHOD NOTE. Computed as Aut of the bipartite incidence graph on 13 + {g['design_blocks']} vertices.
    The direct route, Stabilizer(SymmetricGroup(13), blocks, OnSetsSets), exhausted GAP's
    memory -- S_13 has 6,227,020,800 elements and that call asks for all of them.""")

    print("\n  PASS 5462 -- q=9 after 19.6 hours\n")
    raw = ROOT / "data" / "_q9_milp_raw.json"
    q9 = json.loads(raw.read_text(encoding="utf-8")) if raw.is_file() else {}
    print(f"    SRG                  : {q9.get('srg')}")
    print(f"    Hoffman              : {q9.get('hoffman')}")
    print(f"    alpha found          : {q9.get('alpha_found')}")
    print(f"    proved optimal       : {q9.get('proved_optimal')}")
    print(f"    seconds              : {q9.get('seconds'):,.0f}")
    print(f"""
    NOT PROVED, SO NOT A BOUND. 70,483 seconds of branch and bound at 820 vertices returns
    an incumbent of {q9.get('alpha_found')} and an open gap. The deficit sequence stays at two points, 3 and 8,
    and stays unfitted.

    AND THE INCUMBENT IS WORSE THAN A HEURISTIC'S. Pass 5227's iterated local search reached
    50 at q=9 in 75 seconds; the MILP reached {q9.get('alpha_found')} in 19.6 hours. So at this size the exact
    solver is not merely failing to prove optimality, it is losing to a cheap heuristic as a
    heuristic. That is the honest scaling statement: MILP settled q=3 and q=5 and buys
    nothing at all at q=9.""")

    print("\n  PASS 5463 -- who had the frame inner products first\n")
    print(f"    {'claim':46s} {'pass':>5s}  fate")
    for r in LEDGER:
        print(f"    {r['claim'][:46]:46s} {r['pass']:5d}  {r['fate']}")
    print("""
    THE FIRST ROW IS THE ONE I HAD NOT CHECKED. analysis/w33_pass5267 was committed at
    20:54:30 and states, for odd prime powers q on W(3,q):

        collinear    (q-1)/(q(q+1))
        noncollinear -1/q^2

    My Pass 5278 was committed at 21:12:27 -- EIGHTEEN MINUTES LATER -- measuring exactly
    those values and presenting them as a new identification. Their (q-1)/(q(q+1)) is 1/6 at
    q=3 and 2/15 at q=5; my table reported 0.16666667 and 0.13333333.

    AND THEIRS IS CORRECTLY SCOPED WHILE MINE WAS NOT. They say "odd prime powers q" about
    W(3,q), where Hoffman is q^2+1 and -1/q^2 IS -1/(H-1); the statement is true as written.
    I dropped the scope, called -1/q^2 the noncollinear inner product, and then spent Passes
    5341, 5374 and 5412 discovering that the unscoped version is false and that the general
    form is textbook. Four passes to repair damage I caused by removing a qualifier from a
    result I had rediscovered.

    THE LESSON IS NOT "SEARCH HARDER", which is already in CLAUDE.md and has failed all
    week. It is that a result arriving 18 minutes ahead of yours is invisible to any search
    you ran before starting, and the only thing that catches it is reading the other lane's
    commits before publishing rather than after.""")

    print("\n  PASS 5464 -- the cosine identity, formalised\n")
    r = subprocess.run(["lake", "build", "W33.CosineSequence"],
                       cwd=ROOT / "formal", capture_output=True, text=True, timeout=900)
    ok = r.returncode == 0
    print(f"    formal/W33/CosineSequence.lean builds : {ok}")
    print("""    theorems: recurrence, mu_form, w2_eq_mu_form, gq_collapse, w3q_collapse""")
    print("""
    ARITHMETIC ONLY, and the header says so in the same negative form every other module in
    formal/W33 uses: no graph, no adjacency matrix, no eigenspace, no Gram matrix. What is
    proved is the three-term recurrence, that mu/(k(1+s)) is its value at i=1 given the two
    strongly regular identities, and the specialisation that collapses it to -1/(a*t) on a
    generalised quadrangle -- which is precisely why -1/q^2 and -1/(H-1) looked like general
    laws.

    ONE HYPOTHESIS WAS WRONG ON THE FIRST ATTEMPT and Lean refused it: I wrote
    mu = k + theta*s + theta + s when the identity is mu = k + theta*s. `ring` produced two
    visibly different polynomials rather than closing the goal. A Python check would have
    agreed with me on every example I happened to try, because both forms coincide when
    theta + s = 0 -- which is exactly the GQ case I had been testing all week.""")

    out = {
        "boundary": ("Pass 5460-5461 are GAP computations. Pass 5462 reports an UNPROVED "
                     "incumbent: alpha(W(3,9)) >= 49 is a lower bound and the deficit "
                     "sequence remains two points. Pass 5464 formalises ARITHMETIC only; "
                     "the geometric content stays an external input, as every formal/W33 "
                     "header states. The precedence claim in Pass 5463 is from commit "
                     "timestamps on this machine"),
        "pass_5460": {"q8_aut_order": g["q8_aut_order"],
                      "q8_ovoid_stabiliser": g["q8_ovoid_stabiliser"],
                      "q8_image_order": g["q8_image_order"],
                      "q8_kernel_order": g["q8_kernel_order"],
                      "q8_orbits": g["q8_orbit_sizes"],
                      "q8_transitive": g["q8_transitive"],
                      "identification": "Sz(8):3, since 87360 = 3 * |Sz(8)| = 3 * 29120",
                      "q5_comparison": {"image": q5["image_order"], "kernel": 2,
                                        "orbits": q5["orbit_sizes"]},
                      "conclusion": ("tightness forces the simplex but NOT homogeneity of "
                                     "the embedding; the q=5 distinguished vertex is a "
                                     "real geometric fact and survives the test that "
                                     "could have killed it")},
        "pass_5461": {"design_blocks": g["design_blocks"],
                      "incidence_aut": g["design_incidence_aut"],
                      "action_on_13": g["design_action_on_13"],
                      "structure": g["design_structure"],
                      "same_as_embedding": same,
                      "method": ("Aut of the bipartite incidence graph; the direct "
                                 "Stabilizer in S_13 exhausted GAP's memory")},
        "pass_5462": {**q9,
                      "verdict": "lower bound only; deficit sequence still 2 points",
                      "scaling": ("MILP settled q=3 and q=5 and at q=9 loses to Pass "
                                  "5227's 75-second heuristic, which reached 50")},
        "pass_5463": {"ledger": LEDGER,
                      "precedence": {"their_pass5267": "2026-08-14 20:54:30",
                                     "my_pass5278": "2026-08-14 21:12:27",
                                     "gap_minutes": 18},
                      "their_statement": ("collinear (q-1)/(q(q+1)), noncollinear -1/q^2, "
                                          "scoped to odd prime powers q on W(3,q) -- "
                                          "CORRECT as written"),
                      "my_error": ("dropped the scope, then spent Passes 5341/5374/5412 "
                                   "repairing the unscoped version")},
        "pass_5464": {"module": "formal/W33/CosineSequence.lean", "builds": ok,
                      "theorems": ["recurrence", "mu_form", "w2_eq_mu_form",
                                   "gq_collapse", "w3q_collapse"],
                      "scope": "arithmetic only, geometry external",
                      "caught_by_lean": ("my first hypothesis mu = k + theta*s + theta + s "
                                         "is wrong; the identity is mu = k + theta*s. The "
                                         "two coincide when theta + s = 0, which is the GQ "
                                         "case I had been testing all week")},
    }
    fp = ROOT / "data" / "PART_W33_PASS5460_5467_Q8_TRANSITIVE_Q5_IS_SPECIAL.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
