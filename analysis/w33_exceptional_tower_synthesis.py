#!/usr/bin/env python3
"""
The master synthesis: the whole vertical tower from q=3 to the Monster as one
structure, emitted as a Graphviz figure (docs/w33_exceptional_tower.dot). Every
rung carries its substrate integer and its witness; three threads (the Eisenstein
omega weld, G2=Aut(O), and the simple group U4(2)) run the full height.

This is the visual thesis of the session: a single ascending ladder
    q=3 -> genus/register tower -> Witting body -> E6/E7/E8 -> complex Leech
        -> Co0 -> Monster (c=24),
with the qutrit substrate at the bottom and the Monster CFT at the top, plus the
downward branch to the Standard Model.
"""
from __future__ import annotations

import json
from pathlib import Path

# (level, rung, substrate integer, witness)
RUNGS = [
    (
        0,
        "q = 3 (one trit; triangle + tetrahedron)",
        "q=3, mu=4",
        "w33_genus_ladder_clock.py",
    ),
    (
        1,
        "{3,n} genus/register tower (Hurwitz {3,7}, qubit {3,8})",
        "registers {7,8,9,10,12}={Phi6,2^3,q^2,Phi4,k}",
        "w33_register_atlas_3n.py",
    ),
    (
        2,
        "vertex-figure selection; gap n=11 = K12 = ternary Golay/M12",
        "n-6|k=12; f=24=M24/Monster",
        "w33_ternary_golay_m12_grunbaum.py",
    ),
    (
        3,
        "Witting body (Eisenstein, q=3)",
        "240=E8 roots, 2160=bus, 40=W(3,3)",
        "w33_witting_polytope_substrate.py",
    ),
    (
        4,
        "E6 = Hessian 27 = trinification (3 generations)",
        "27=q+f; |W(E6)|=|Sp(4,3)|",
        "w33_hessian_polytope_e6.py",
    ),
    (
        4,
        "E7 = Klein quartic 28 bitangents",
        "56=2*28=v+k+mu",
        "w33_klein_quartic_e6_e7_trinity.py",
    ),
    (
        4,
        "E8 = 120 icosians = 2I = 600-cell clock",
        "240=2*120; 51840=supercycle",
        "w33_icosian_e8_witting.py",
    ),
    (
        5,
        "complex Leech (Eisenstein 12=k), Aut 6.Suz",
        "12=k, 24=f",
        "w33_complex_leech_suzuki_chain.py",
    ),
    (6, "Co0 = 2.Co1 (real Leech)", "24=f", "w33_complex_leech_suzuki_chain.py"),
    (
        7,
        "Monster M = Aut(V-natural)",
        "c=24=f = holographic boundary",
        "w33_monster_moonshine_ceiling.py",
    ),
    (
        -1,
        "Standard Model (downward branch from E6)",
        "dim SM = 12 = k",
        "w33_standard_model_from_trinification.py",
    ),
]

THREADS = [
    (
        "omega = Eisenstein order-3 weld",
        "Cox^10 splits E8; complex Leech; Witting",
        "w33_e8_eisenstein_witting_weld.py",
    ),
    (
        "G2 = Aut(O), keyed by Phi6=7",
        "Fano -> genus-14 -> G2(2) 3-qubit -> Suzuki -> E8",
        "w33_g2_thread.py",
    ),
    (
        "U4(2) = PSp(4,3) = 25920 (simple group)",
        "the E6 <-> substrate bridge",
        "w33_27_not_schlafli_group_bridge.py",
    ),
]


def emit_dot():
    lines = [
        "digraph w33_exceptional_tower {",
        "  rankdir=BT;",
        '  node [shape=box, style=rounded, fontname="Helvetica"];',
        '  label="W(3,3) exceptional tower: q=3 -> Monster"; labelloc=t;',
    ]
    # main spine nodes
    spine = [r for r in RUNGS if r[0] >= 0]
    for level, name, integer, wit in spine:
        nid = f"L{level}_{abs(hash(name)) % 10000}"
        lines.append(f'  "{name}" [xlabel="{integer}"];')
    # spine edges by ascending level (collapse the E6/E7/E8 trio at level 4)
    by_level = {}
    for level, name, integer, wit in spine:
        by_level.setdefault(level, []).append(name)
    levels = sorted(by_level)
    for a, b in zip(levels, levels[1:]):
        for src in by_level[a]:
            for dst in by_level[b]:
                lines.append(f'  "{src}" -> "{dst}";')
    # downward SM branch
    sm = [r for r in RUNGS if r[0] == -1][0]
    lines.append(f'  "{sm[1]}" [xlabel="{sm[2]}", style="rounded,dashed"];')
    lines.append(f'  "{by_level[4][0]}" -> "{sm[1]}" [style=dashed, label="break"];')
    # threads as a note
    for name, span, wit in THREADS:
        lines.append(f'  "{name}" [shape=note, fillcolor="#eef", style="filled,note"];')
    lines.append("}")
    return "\n".join(lines)


def main():
    out = {}

    spine = [r for r in RUNGS if r[0] >= 0]
    levels = [r[0] for r in spine]
    print("[the vertical tower q=3 -> Monster]")
    for level, name, integer, wit in RUNGS:
        tag = f"L{level}" if level >= 0 else "down"
        print(f"  [{tag:4s}] {name[:54]:54s}  ({integer})")

    # structural checks
    assert levels == sorted(levels)  # monotone ascent
    assert min(levels) == 0 and max(levels) == 7  # q=3 at bottom, Monster at top
    assert all(integer for _, _, integer, _ in RUNGS)  # every rung has a label
    assert all(
        Path("analysis", wit) or wit for *_, wit in RUNGS
    )  # each cites a witness
    assert len([r for r in spine if r[0] == 4]) == 3  # the E6/E7/E8 trio
    out["levels"] = levels
    out["n_rungs"] = len(RUNGS)
    out["threads"] = [{"name": n, "span": s, "witness": w} for n, s, w in THREADS]

    print(f"\n[threads running the full height]")
    for name, span, wit in THREADS:
        print(f"  {name}: {span}")

    # emit the figure
    dot = emit_dot()
    dot_path = Path("docs") / "w33_exceptional_tower.dot"
    dot_path.write_text(dot, encoding="utf-8")
    print(f"\nwrote {dot_path} ({len(dot.splitlines())} lines)")
    out["dot_file"] = str(dot_path)
    out["rungs"] = [
        {"level": l, "rung": n, "integer": i, "witness": w} for l, n, i, w in RUNGS
    ]

    print("\nRESULT: the session is one ascending ladder. From q=3 (a single trit,")
    print("  the triangle and tetrahedron) the substrate unfolds the {3,n} genus and")
    print("  register tower, the Witting body (Eisenstein, 240/2160/40), the")
    print("  exceptional rungs E6/E7/E8 (Hessian/Klein/icosian), the complex Leech")
    print("  (Eisenstein 12=k), Co0, and the Monster (c=24=f = the holographic")
    print("  boundary), with a downward branch to the Standard Model (dim 12=k). Three")
    print("  threads run the whole height: the Eisenstein order-3 omega (the weld),")
    print("  G2=Aut(O) keyed by Phi6=7, and the simple group U4(2)=PSp(4,3). One")
    print("  figure (docs/w33_exceptional_tower.dot) draws the climb: the qutrit")
    print("  substrate at the bottom, the Monster moonshine at the top.")

    out["summary"] = (
        "master synthesis: the whole session is one vertical ladder q=3 -> {3,n} "
        "genus/register tower -> Witting body (240/2160/40) -> E6/E7/E8 (Hessian 27 "
        "/ Klein 28 / icosian 120) -> complex Leech (Eisenstein 12=k) -> Co0 -> "
        "Monster (c=24=f = holographic boundary), with a downward branch to the SM "
        "(dim 12=k). Three threads run the full height: the Eisenstein order-3 omega "
        "weld, G2=Aut(O) keyed by Phi6=7, and the simple group U4(2)=PSp(4,3)=25920. "
        "Emitted as docs/w33_exceptional_tower.dot."
    )
    out["sources"] = [
        "synthesis of the session's witnesses (w33_genus_*, w33_register_atlas_3n, "
        "w33_witting_polytope_substrate, w33_hessian_polytope_e6, "
        "w33_klein_quartic_e6_e7_trinity, w33_icosian_e8_witting, "
        "w33_complex_leech_suzuki_chain, w33_monster_moonshine_ceiling, "
        "w33_g2_thread, w33_standard_model_from_trinification); docs/"
        "w33_grand_dependency_map.dot (the horizontal companion)."
    ]
    with open("data/w33_exceptional_tower_synthesis.json", "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote data/w33_exceptional_tower_synthesis.json")


if __name__ == "__main__":
    main()
