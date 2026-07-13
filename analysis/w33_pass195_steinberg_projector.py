#!/usr/bin/env python3
"""Pass 195: the Steinberg projector -- the protected register, explicitly.

Pass 190 located St_81 with multiplicity 3 in the 480-dimensional
eigenlattice shell.  Because 3 does not divide |G|/81 = 320, the ordinary
Steinberg idempotent is 3-integral, so the isotypic projector reduces mod
3 and splits off the protected register as an explicit direct summand.
This witness constructs it:

1. THE INTEGER OPERATOR.  S = sum_g chi81(g) rho_shell(g), accumulated
   over all 25920 group elements (shell permutations carried through the
   BFS closure).  Element classes are identified by the fingerprint
   (order, fixed points, fixed lines, fixed shell vectors), matched to
   the GAP class data of the same combined action.

2. THE PROJECTOR IDENTITIES.  S^2 = 320 S exactly (so P = S/320 is
   idempotent), trace(S) = 320 * 243, rank(S) = 243 = 3 * 81.

3. THE PROTECTED REGISTER.  P is 3-integral; its reduction mod 3 is an
   idempotent of rank 243 on F3^480: the Steinberg component of the
   kinematic shell as an explicit 243-dimensional invariant register.
"""

from __future__ import annotations

from ast import literal_eval
from collections import Counter
import json
from pathlib import Path
import subprocess
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass158_chiral_trade_lattice_two_480s import (
    build_w33,
    minimal_shell,
    saturated_kernel,
    w33_lines,
)
from analysis.w33_pass161_gq42_ihara_inheritance import (
    small_generating_set,
    support_graph,
)
from analysis.w33_pass163_two480s_character_decomposition import (
    GAP_BASH,
    GAP_BINARY,
    cygwin_path,
    gap_tempdir,
)
from analysis.w33_pass158_chiral_trade_lattice_two_480s import build_group

OUT = ROOT / "data" / "w33_pass195_steinberg_projector.json"


def main():
    if not GAP_BASH.exists():
        print("GAP is required for Pass 195")
        return 1
    points, adjacency, symplectic = build_w33()
    lines = w33_lines(adjacency)
    checks = {}

    # the L2 shell as the 480 carrier (points + ordered line pairs)
    generators, group40 = build_group(points, symplectic)
    checks["group_order"] = len(group40) == 25920
    two_gens = small_generating_set(group40)

    pencils = {
        p: sorted((line for line in lines if p in line), key=lambda l: sorted(l))
        for p in range(40)
    }
    labels = []
    for p in range(40):
        for plus in pencils[p]:
            for minus in pencils[p]:
                if plus != minus:
                    labels.append((p, plus, minus))
    label_index = {l: n for n, l in enumerate(labels)}
    line_index = {line: n for n, line in enumerate(lines)}

    def shell_perm(perm):
        return np.array(
            [
                label_index[
                    (
                        perm[p],
                        frozenset(perm[x] for x in plus),
                        frozenset(perm[x] for x in minus),
                    )
                ]
                for (p, plus, minus) in labels
            ],
            dtype=np.int32,
        )

    def line_perm(perm):
        return np.array(
            [line_index[frozenset(perm[x] for x in lines[n])] for n in range(40)],
            dtype=np.int32,
        )

    gen40 = [np.array(g, dtype=np.int32) for g in two_gens]
    gen480 = [shell_perm(g) for g in two_gens]
    gen_lines = [line_perm(g) for g in two_gens]

    # BFS closure carrying (40-perm, line-perm, 480-perm) together
    identity = (tuple(range(40)),)
    seen = {tuple(range(40)): 0}
    perms40 = [np.arange(40, dtype=np.int32)]
    perms_lines = [np.arange(40, dtype=np.int32)]
    perms480 = [np.arange(480, dtype=np.int32)]
    frontier = [0]
    while frontier:
        new_frontier = []
        for idx in frontier:
            base40 = perms40[idx]
            baseL = perms_lines[idx]
            base480 = perms480[idx]
            for g40, gl, g480 in zip(gen40, gen_lines, gen480):
                comp40 = g40[base40]
                key = tuple(int(v) for v in comp40)
                if key not in seen:
                    seen[key] = len(perms40)
                    perms40.append(comp40)
                    perms_lines.append(gl[baseL])
                    perms480.append(g480[base480])
                    new_frontier.append(len(perms40) - 1)
        frontier = new_frontier
    checks["closure_25920"] = len(perms40) == 25920

    # element fingerprints
    def element_order(perm):
        order = 1
        current = perm.copy()
        while not np.array_equal(current, np.arange(40, dtype=np.int32)):
            current = perm[current]
            order += 1
        return order

    def cycle_type(perm, size):
        seen_c = np.zeros(size, dtype=bool)
        lengths = []
        for start in range(size):
            if seen_c[start]:
                continue
            length = 0
            cur = start
            while not seen_c[cur]:
                seen_c[cur] = True
                cur = int(perm[cur])
                length += 1
            lengths.append(length)
        return tuple(sorted(Counter(lengths).items()))

    fingerprints = []
    for i in range(len(perms40)):
        fingerprints.append(
            (
                cycle_type(perms40[i], 40),
                cycle_type(perms480[i], 480),
            )
        )
    profile = Counter(fingerprints)
    # cycle-type on the two actions is a conjugacy invariant; some classes
    # may share it (harmless as long as chi81 agrees, checked below)
    checks["fingerprints_computed"] = len(profile) >= 15

    # GAP: per-class order, size, point/line/shell permchar values, chi81
    combined = []
    for g40, gl, g480 in zip(gen40, gen_lines, gen480):
        image = (
            [int(v) + 1 for v in g40]
            + [int(v) + 41 for v in gl]
            + [int(v) + 81 for v in g480]
        )
        combined.append(image)
    program = []
    gens_str = ", ".join(
        "PermList([" + ",".join(str(v) for v in image) + "])" for image in combined
    )
    program.append(f"gens := [ {gens_str} ];;")
    program.append("G := Group(gens);;")
    program.append('Print("SIZE=", Size(G), ";\\n");')
    program.append("cc := ConjugacyClasses(G);;")
    program.append("reps := List(cc, Representative);;")
    program.append('Print("SIZES=", List(cc, Size), ";\\n");')
    program.append(
        "cyc40 := List(reps, r -> Collected(List(Cycles(r, [1..40]), "
        "Length)));;"
        'Print("CYC40=", cyc40, ";\\n");'
    )
    program.append(
        "cyc480 := List(reps, r -> Collected(List(Cycles(r, [81..560]), "
        "Length)));;"
        'Print("CYC480=", cyc480, ";\\n");'
    )
    program.append("t := CharacterTable(G);;")
    program.append("cct := ConjugacyClasses(t);;")
    program.append(
        "chi81 := First(Irr(t), x -> x[1] = 81);;"
        'Print("CHI81=", ValuesOfClassFunction(chi81), ";\\n");'
    )
    program.append(
        "match := List(cc, c -> First([1..Length(cct)], "
        "k -> Representative(c) in cct[k]));;"
    )
    program.append('Print("MATCH=", match, ";\\n");')
    program.append("QUIT;")

    workdir = gap_tempdir("w33_pass195_")
    script = workdir / "pass195.g"
    script.write_text("\n".join(program) + "\n", encoding="ascii")
    completed = subprocess.run(
        [
            str(GAP_BASH),
            "--login",
            "-c",
            f"{GAP_BINARY} -q '{cygwin_path(script)}'",
        ],
        capture_output=True,
        text=True,
        timeout=1800,
    )
    if completed.returncode != 0:
        raise RuntimeError(f"GAP failed: {completed.stderr[:1500]}")
    text = completed.stdout.replace("\\\n", "").replace("\n", "")

    def extract(marker):
        start = text.index(marker) + len(marker)
        end = text.index(";", start)
        return literal_eval(text[start:end].replace(" ", ""))

    checks["gap_size"] = extract("SIZE=") == 25920
    sizes = extract("SIZES=")
    cyc40 = extract("CYC40=")
    cyc480 = extract("CYC480=")
    chi81_by_ct = extract("CHI81=")
    match = extract("MATCH=")  # 1-indexed class-table position per cc
    checks["twenty_classes"] = len(sizes) == 20

    def norm_ct(gap_collected):
        # GAP Collected -> [[len, mult], ...]; normalize to sorted tuple
        return tuple(sorted((int(a), int(b)) for a, b in gap_collected))

    class_fingerprints = [
        (norm_ct(cyc40[c]), norm_ct(cyc480[c])) for c in range(len(sizes))
    ]
    chi81_per_cc = [int(chi81_by_ct[match[c] - 1]) for c in range(len(sizes))]

    # chi81 is the exact conjugacy invariant we need; group GAP classes by
    # their (cyc40, cyc480) fingerprint and require chi81 CONSTANT on each
    # group -- then the fingerprint suffices to assign chi81 to elements
    fp_to_chi81 = {}
    chi81_well_defined = True
    fp_to_size = Counter()
    for c, fp in enumerate(class_fingerprints):
        fp_to_size[fp] += sizes[c]
        if fp in fp_to_chi81:
            if fp_to_chi81[fp] != chi81_per_cc[c]:
                chi81_well_defined = False
        else:
            fp_to_chi81[fp] = chi81_per_cc[c]
    checks["chi81_constant_on_cycle_type"] = chi81_well_defined
    checks["all_elements_classified"] = all(fp in fp_to_chi81 for fp in profile)
    checks["fingerprint_sizes_match"] = all(
        fp_to_size[fp] == profile[fp] for fp in profile
    )
    checks["chi81_degree"] = fp_to_chi81[(((1, 40),), ((1, 480),))] == 81

    # accumulate S = sum chi81(g) rho(g)
    S = np.zeros((480, 480), dtype=np.int64)
    rows = np.arange(480)
    for i in range(len(perms40)):
        value = fp_to_chi81[fingerprints[i]]
        if value:
            S[rows, perms480[i]] += int(value)

    # projector identities
    s2 = S @ S
    checks["S_squared_320_S"] = bool(np.array_equal(s2, 320 * S))
    checks["trace_320_243"] = int(np.trace(S)) == 320 * 243
    rank = int(np.linalg.matrix_rank(S.astype(float)))
    checks["rank_243"] = rank == 243

    # mod 3: idempotent of rank 243 (320 = 2 mod 3, inverse of 2 is 2)
    s3 = (S % 3).astype(np.int64)
    p3 = (2 * s3) % 3  # P mod 3 = S/320 mod 3 = S * 320^{-1} = S*2 mod 3
    checks["mod3_idempotent"] = bool(np.array_equal((p3 @ p3) % 3, p3))

    def f3_rank(matrix):
        work = [[int(v) % 3 for v in row] for row in matrix]
        rank3 = 0
        for col in range(len(work[0])):
            pivot = next((r for r in range(rank3, len(work)) if work[r][col]), None)
            if pivot is None:
                continue
            work[rank3], work[pivot] = work[pivot], work[rank3]
            inv = 1 if work[rank3][col] == 1 else 2
            work[rank3] = [(inv * v) % 3 for v in work[rank3]]
            for r in range(len(work)):
                if r != rank3 and work[r][col]:
                    factor = work[r][col]
                    work[r] = [
                        (work[r][cc] - factor * work[rank3][cc]) % 3
                        for cc in range(len(work[0]))
                    ]
            rank3 += 1
        return rank3

    rank3 = f3_rank(p3)
    checks["mod3_rank_243"] = rank3 == 243

    all_pass = all(checks.values())
    payload = {
        "schema": "w33.pass195.steinberg_projector.v1",
        "status": "PASS" if all_pass else "FAIL",
        "gap_source": "live",
        "projector": {
            "operator": "S = sum_g chi81(g) rho_shell(g), integer 480x480",
            "identities": "S^2 = 320 S, trace = 320*243, rank = 243",
            "mod3": (
                "P = 2S mod 3 is an idempotent of rank 243 on F3^480: "
                "the protected register as an explicit direct summand of "
                "the kinematic shell (3 copies of St_81)"
            ),
        },
        "reading": (
            "the holonet's protected memory is no longer a multiplicity "
            "in a census: it is the image of an explicit integral "
            "projector on the E8-root carrier, 3-integral because 320 is "
            "prime to 3 -- projectivity of the Steinberg module made "
            "matrix-concrete"
        ),
        "checks": {name: bool(value) for name, value in checks.items()},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
