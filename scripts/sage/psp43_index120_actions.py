#!/usr/bin/env python3
"""Search index-120 subgroups of PSp(4,3) and test conjugacy to W(E6) line action.

Uses GAP via Sage interface.
"""
from __future__ import annotations

import json
from pathlib import Path
from sage.interfaces.gap import gap

ROOT = Path(__file__).resolve().parents[2]


def build_line_perms_from_we6():
    data = json.loads((ROOT / 'artifacts' / 'we6_true_action.json').read_text())
    roots = [tuple(r) for r in data['roots_int2']]
    root_to_idx = {r: i for i, r in enumerate(roots)}

    # lines
    line_id = [-1] * len(roots)
    line_reps = []
    for i, r in enumerate(roots):
        if line_id[i] != -1:
            continue
        j = root_to_idx[tuple(-x for x in r)]
        lid = len(line_reps)
        line_id[i] = lid
        line_id[j] = lid
        rep = i if i < j else j
        line_reps.append(rep)

    gens = data['we6_even_generators']  # 1-based perms on roots
    line_perms = []
    for g in gens:
        perm = [0] * len(line_reps)
        for lid, rep in enumerate(line_reps):
            img = g[rep] - 1
            lid2 = line_id[img]
            perm[lid] = lid2 + 1
        line_perms.append(perm)

    return line_perms


def main():
    line_perms = build_line_perms_from_we6()
    gap_line_perms = [gap.PermList(p) for p in line_perms]
    Gline = gap.Group(gap_line_perms)

    # PSp(4,3)
    try:
        G = gap.PSp(4,3)
    except Exception:
        G = gap.ProjectiveSymplecticGroup(4,3)

    classes = gap.ConjugacyClassesSubgroups(G)
    count = int(gap.Length(classes))

    matches = []
    Sn = gap.SymmetricGroup(120)

    for i in range(1, count + 1):
        c = gap.List(classes, "x->x")[i-1]
        H = gap.Representative(c)
        idx = int(gap.Index(G, H))
        if idx != 120:
            continue
        action = gap.Action(G, gap.RightCosets(G, H), gap.OnRight)
        is_conj = gap.IsConjugate(Sn, action, Gline)
        if is_conj == True:
            matches.append({"class_index": i, "index": idx})

    out = {
        "index120_classes_checked": count,
        "matches": matches,
        "match_count": len(matches),
    }
    out_path = ROOT / 'artifacts' / 'psp43_index120_actions.json'
    out_path.write_text(json.dumps(out, indent=2))
    print(f"Wrote {out_path}")


if __name__ == '__main__':
    main()
