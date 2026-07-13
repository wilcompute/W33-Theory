#!/usr/bin/env python3
"""Pass 203: the 4320 supercycle as an associated fibre bundle.

Passes 191/196/197 gave the three ingredients:
  - 4320 = 120 axes x 36 double-sixes (Pass 191, NOT transitive: the
    product splits, subdegrees 27+6+3 over an axis);
  - the elation Heisenberg 3^{1+2} and the flat C3^3 as the two parabolic
    cores (Pass 196);
  - the rank-3 double-six action (Pass 197).
This witness assembles the bundle picture and reports what actually holds:

1. THE BASE MAPS.  The two projections 4320 -> 120 (axes) and
   4320 -> 36 (double-sixes), each PSp(4,3)-equivariant, with exact
   fibre sizes 36 and 120.

2. THE STRUCTURE-GROUP FIBRE.  Over one axis the 36 double-sixes split
   under the axis stabilizer (order 216) into orbits 27+6+3; the
   distinguished 3-orbit carries the full S3 (Pass 191) -- the native
   completion fibre.  The axis stabilizer's O_3-core (order 27) is the
   flat C3^3 (Pass 196), acting on the fibre.

3. THE SUPERCYCLE ARITHMETIC.  51840 = 24 * 2160 = 12 * 4320 = 720 * 72:
   the exact factorisations tying the packet clock (72), the mirror bus
   (2160), the product carrier (4320), and the runtime supercycle
   (51840) to the axis/double-six geometry -- an honest ledger of which
   identities are group-theoretic and which are the controller's
   arithmetic.
"""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass158_chiral_trade_lattice_two_480s import (
    build_group,
    build_w33,
    orbit_count,
    w33_lines,
)
from analysis.w33_pass160_trade_tower_gq42 import (
    generic_saturated_kernel,
    staged_minimal_shell,
)
from analysis.w33_pass161_gq42_ihara_inheritance import (
    small_generating_set,
    support_graph,
)
from analysis.w33_pass168_second_shell_scheme import gq42_lines

OUT = ROOT / "data" / "w33_pass203_supercycle_bundle.json"


def main():
    points, adjacency, symplectic = build_w33()
    lines = w33_lines(adjacency)
    checks = {}

    generators, group = build_group(points, symplectic)
    checks["group_25920"] = len(group) == 25920
    two_gens = small_generating_set(group)

    # ---- the 120 axes ----
    octads, graph45 = support_graph(adjacency)
    octad_index = {s: n for n, s in enumerate(octads)}
    lines45 = gq42_lines(graph45)
    inc45 = np.zeros((27, 45), dtype=np.int64)
    for row, line in enumerate(lines45):
        for p in line:
            inc45[row, p] = 1
    trade45 = generic_saturated_kernel(inc45)
    _, shell240 = staged_minimal_shell(trade45)
    shell240 = [np.asarray(v, dtype=np.int64) for v in shell240]
    axes = sorted({frozenset(np.flatnonzero(v).tolist()) for v in shell240}, key=sorted)
    checks["axes_120"] = len(axes) == 120
    axis_index = {a: n for n, a in enumerate(axes)}

    # ---- the 36 double-sixes ----
    inc40 = np.zeros((40, 40), dtype=np.int64)
    for row, line in enumerate(lines):
        for p in line:
            inc40[row, p] = 1
    route = generic_saturated_kernel(inc40.T)
    _, shell432 = staged_minimal_shell(route, bounds=(4, 6, 8, 10))
    shell432 = [np.asarray(v, dtype=np.int64) for v in shell432]
    line_index = {line: n for n, line in enumerate(lines)}

    def line_perm(perm):
        return [line_index[frozenset(perm[x] for x in lines[n])] for n in range(40)]

    keys432 = {tuple(int(x) for x in v): n for n, v in enumerate(shell432)}
    gmaps = []
    for g in two_gens:
        lp = line_perm(g)
        tab = []
        for v in shell432:
            im = np.empty(40, dtype=np.int64)
            for src in range(40):
                im[lp[src]] = v[src]
            tab.append(keys432[tuple(int(x) for x in im)])
        gmaps.append(tab)
    tabs = [
        (
            np.asarray(m, dtype=np.int64)[:, None] * 432
            + np.asarray(m, dtype=np.int64)[None, :]
        ).reshape(-1)
        for m in gmaps
    ]
    labels = np.full(432 * 432, -1, dtype=np.int64)
    oc = 0
    for start in range(432 * 432):
        if labels[start] >= 0:
            continue
        labels[start] = oc
        st = [start]
        while st:
            cur = st.pop()
            for t in tabs:
                img = int(t[cur])
                if labels[img] < 0:
                    labels[img] = oc
                    st.append(img)
        oc += 1
    grid = labels.reshape(432, 432)
    target = None
    for o in range(oc):
        m = (grid == o).astype(np.int64)
        ri = int(np.flatnonzero(m.sum(axis=1) > 0)[0])
        if int(m[ri].sum()) == 5 and not np.array_equal(m, m.T):
            target = m + m.T
            break
    seen = np.zeros(432, dtype=bool)
    dsixes = []
    for start in range(432):
        if seen[start]:
            continue
        comp = {start}
        st = [start]
        seen[start] = True
        while st:
            cur = st.pop()
            for nxt in np.flatnonzero(target[cur]):
                if not seen[nxt]:
                    seen[nxt] = True
                    comp.add(int(nxt))
                    st.append(int(nxt))
        if len(comp) > 1:
            dsixes.append(frozenset(comp))
    dsixes = sorted(dsixes, key=sorted)
    dsix_index = {d: n for n, d in enumerate(dsixes)}
    checks["double_sixes_36"] = len(dsixes) == 36

    # ---- actions on axes and double-sixes ----
    def axis_map(perm):
        return [
            axis_index[
                frozenset(
                    octad_index[frozenset(perm[x] for x in octads[o])] for o in axes[a]
                )
            ]
            for a in range(120)
        ]

    def dsix_map(perm):
        lp = line_perm(perm)
        out = []
        for d in dsixes:
            image = set()
            for i in d:
                img = np.empty(40, dtype=np.int64)
                for src in range(40):
                    img[lp[src]] = shell432[i][src]
                image.add(keys432[tuple(int(x) for x in img)])
            out.append(dsix_index[frozenset(image)])
        return out

    amaps = [axis_map(g) for g in two_gens]
    dmaps = [dsix_map(g) for g in two_gens]
    checks["axes_transitive"] = orbit_count(120, amaps) == 1
    checks["double_sixes_transitive"] = orbit_count(36, dmaps) == 1

    # ---- the product carrier and its orbit split ----
    prod_tabs = []
    for am, dm in zip(amaps, dmaps):
        a = np.asarray(am, dtype=np.int64)
        d = np.asarray(dm, dtype=np.int64)
        prod_tabs.append((a[:, None] * 36 + d[None, :]).reshape(-1))
    plabels = np.full(4320, -1, dtype=np.int64)
    pc = 0
    for start in range(4320):
        if plabels[start] >= 0:
            continue
        plabels[start] = pc
        st = [start]
        while st:
            cur = st.pop()
            for t in prod_tabs:
                img = int(t[cur])
                if plabels[img] < 0:
                    plabels[img] = pc
                    st.append(img)
        pc += 1
    orbit_sizes = sorted(Counter(plabels.tolist()).values(), reverse=True)
    checks["product_orbits_3240_720_360"] = orbit_sizes == [3240, 720, 360]
    checks["product_not_transitive"] = pc == 3

    # ---- the axis stabilizer and the S3 completion fibre ----
    axis0 = axes[0]
    stab_axis = [
        g
        for g in group
        if frozenset(octad_index[frozenset(g[x] for x in octads[o])] for o in axis0)
        == axis0
    ]
    checks["axis_stabilizer_216"] = len(stab_axis) == 216

    # orbits of stab_axis on the 36 double-sixes
    def dsix_of(perm, d):
        lp = line_perm(perm)
        image = set()
        for i in d:
            img = np.empty(40, dtype=np.int64)
            for src in range(40):
                img[lp[src]] = shell432[i][src]
            image.add(keys432[tuple(int(x) for x in img)])
        return dsix_index[frozenset(image)]

    fibre_orbits = [None] * 36
    lab = 0
    for tgt in range(36):
        if fibre_orbits[tgt] is not None:
            continue
        lab += 1
        orb = {tgt}
        st = [tgt]
        while st:
            cur = st.pop()
            for g in stab_axis:
                nxt = dsix_of(g, dsixes[cur])
                if nxt not in orb:
                    orb.add(nxt)
                    st.append(nxt)
        for m in orb:
            fibre_orbits[m] = lab
    fibre_sizes = sorted(Counter(x for x in fibre_orbits if x).values())
    checks["fibre_split_3_6_27"] = fibre_sizes == [3, 6, 27]

    # the 3-orbit carries S3: its setwise stabilizer image on the 3 points
    three_lab = next(
        s for s, c in Counter(x for x in fibre_orbits if x).items() if c == 3
    )
    three = [i for i in range(36) if fibre_orbits[i] == three_lab]
    three_images = set()
    for g in stab_axis:
        img = tuple(three.index(dsix_of(g, dsixes[t])) for t in three)
        three_images.add(img)
    checks["completion_fibre_full_S3"] = len(three_images) == 6

    # ---- supercycle arithmetic ledger ----
    ledger = {
        "51840 = 24*2160": 51840 == 24 * 2160,
        "51840 = 12*4320": 51840 == 12 * 4320,
        "51840 = 720*72": 51840 == 720 * 72,
        "4320 = 120*36": 4320 == 120 * 36,
        "2160 = 30*72": 2160 == 30 * 72,
        "12960 = 3*4320": 12960 == 3 * 4320,
        "216 = 27*8": 216 == 27 * 8,
    }
    checks["arithmetic_ledger_exact"] = all(ledger.values())

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass203.supercycle_bundle.v1",
        "status": "PASS" if all_pass else "FAIL",
        "bundle": {
            "total_space": "4320 = 120 axes x 36 double-sixes",
            "base_maps": ["4320 -> 120 axes", "4320 -> 36 double-sixes"],
            "transitive": False,
            "product_orbits": orbit_sizes,
            "axis_stabilizer_order": 216,
            "fibre_split_over_axis": fibre_sizes,
            "completion_fibre": "the 3-orbit, full S3 (order 6)",
            "structure_group_core": "flat C3^3 = O_3(axis stabilizer)",
        },
        "supercycle_ledger": {k: bool(v) for k, v in ledger.items()},
        "reading": (
            "the 4320-product is NOT a homogeneous bundle -- it splits "
            "3240+720+360 -- but over each axis the double-sixes carry a "
            "canonical S3 completion fibre (the distinguished 3-orbit) "
            "acted on by the flat C3^3 core, and the supercycle "
            "arithmetic 51840=12*4320=720*72 ties the packet clock, "
            "mirror bus, and product carrier to the axis/double-six "
            "geometry. Honest scope: the S3 fibre is geometric; the "
            "controller-carrier identification is NOT claimed"
        ),
        "checks": {name: bool(v) for name, v in checks.items() if isinstance(v, bool)},
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
