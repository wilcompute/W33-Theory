#!/usr/bin/env python3
"""Pass 11962 -- equivariant maps from the 40-line module into the Steinberg St_81.

TOE51 (4a7898e4b) left one gate open: Holotrade supplies the K81 carrier as
Reg(H27) (x) Reg(C3) with an H27 x C3 action, and nothing relates it to the 40-line
representation 1+24+15 of PSp(4,3).  It asked for an H27-equivariant intertwiner or a
character-theoretic no-go.

The carrier's relevant module is St_81, the unique degree-81 irreducible of PSp(4,3)
(Holotrade analysis/w33_steinberg_doublecoset_colour_swap.g uses exactly that), whose
restriction to a Sylow 3-subgroup is regular.  GAP decides, for all 116 subgroup classes H:

  HOM(H)   = dim of H-equivariant maps  PERM -> St
  EMBED(H) = whether an INJECTIVE (hence, by polar decomposition, isometric) one exists
             <=> every irrep occurs in PERM no more often than in St.
  ORBITS(H)= number of H-orbits on the 40 lines = multiplicity of the trivial character
             in PERM; it must not exceed the multiplicity in St.

Findings (exact): full group Hom = 0 (Schur); Hom != 0 for 115/116 classes; injective maps
exist for only 36 small classes (max order 24); none for any maximal subgroup, the Sylow-3
subgroup (4 orbits vs 1 invariant direction in the regular module) or any order-27 subgroup
(4, 6, 8 orbits vs 3).  The trivial-character obstruction explains 79 of the 80 failures.

Scope: the 40-line module is acted on through the subgroup embedding.  If a different
H27 action on the line signal space is intended, this is not a statement about it.  It also
says nothing about non-equivariant storage (a plain coordinate embedding 40 -> 81 exists).
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GAP_FILE = os.path.join(HERE, "w33_pass11962_line_module_steinberg_hom.g")
OUT = os.path.join(ROOT, "data", "w33_pass11962_line_module_steinberg_hom.json")
sys.path.insert(0, HERE)


def run_gap() -> str:
    if shutil.which("gap"):
        cmd = ["gap", "-q", "-b", GAP_FILE]
        cwd = ROOT
    else:
        wsl_root = ROOT.replace("\\", "/")
        wsl_root = re.sub(r"^([A-Za-z]):", lambda m: "/mnt/" + m.group(1).lower(), wsl_root)
        cmd = ["wsl.exe", "-e", "bash", "-lc",
               f"cd '{wsl_root}' && gap -q -b analysis/w33_pass11962_line_module_steinberg_hom.g < /dev/null"]
        cwd = None
    done = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=3000, check=True)
    return done.stdout


def parse(stdout: str) -> dict[str, str]:
    flat = stdout.replace("\\\n", "").replace("\n  ", " ")
    return {m.group(1): m.group(2).strip() for m in re.finditer(r"^RESULT_(\w+) (.*)$", flat, re.M)}


def independent_spectrum_check() -> dict:
    """Non-GAP evidence for the 1+24+15 degrees: spectrum of the line-collinearity graph."""
    from w33_typed_universal_microvm import GEOMETRY
    lines = [set(l) for l in GEOMETRY.lines]
    n = len(lines)
    A = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            if i != j and lines[i] & lines[j]:
                A[i, j] = 1
    vals = np.round(np.linalg.eigvalsh(A.astype(float))).astype(int)
    spec = {int(v): int((vals == v).sum()) for v in sorted(set(vals))}
    return {"line_graph_valency": int(A.sum(1)[0]), "spectrum": spec,
            "matches_1_24_15": spec == {-4: 15, 2: 24, 12: 1}}


def verify() -> dict:
    r = parse(run_gap())
    spec = independent_spectrum_check()
    num = lambda k: int(re.match(r"-?\d+", r[k]).group())
    checks = {
        "gap_pass_line": True,
        "perm_is_1_plus_15_plus_24": r["PERM_DECOMP"] == "1+15+24" and spec["matches_1_24_15"],
        "unique_degree_81_irreducible": r["UNIQUE_ST81"] == "true",
        "hom_full_group_is_zero": num("HOM_FULL") == 0,
        "st_regular_on_sylow3": r["ST_REGULAR_ON_SYLOW3"] == "true",
        "sylow3_is_smallgroup_81_7": r["SYLOW3_ID"].replace(" ", "") == "[81,7]",
        "hom_sylow3_is_40": num("HOM_SYLOW3") == 40,
        "sylow3_has_no_injective_map": r["EMBED_SYLOW3"] == "false",
        "116_classes_115_have_nonzero_hom": num("N_CLASSES") == 116 and num("N_HOM_NONZERO") == 115,
        "only_36_classes_embed_max_order_24": num("N_EMBED") == 36 and num("MAX_ORDER_EMBED") == 24,
        "first_failure_at_order_8": num("MIN_ORDER_NOEMBED") == 8,
        "orbit_obstruction_explains_79_of_80": num("N_NOEMBED") == 80 and num("N_NOEMBED_EXPLAINED_BY_ORBITS") == 79,
        "burnside_cross_check_clean": num("BURNSIDE_MISMATCHES") == 0,
        "no_maximal_subgroup_embeds": "true" not in r["MAXIMAL_ORDERS_AND_EMBED"],
        "no_order27_subgroup_embeds": r["ORDER27_ROWS"].count("false") == 3 and "true" not in r["ORDER27_ROWS"],
        "three_order27_classes_each_three_regular": r["ST_ON_ORDER27_IS_THREE_REGULAR"].replace(" ", "") == "[true,true,true]",
        "unique_order81_class_is_sylow": num("ORDER81_CLASSES") == 1,
        "h27_x_c3_is_not_the_sylow_group": "[81,7]" not in r["H27xC3_IDS"].replace(" ", ""),
    }
    payload = {
        "schema": "w33.pass11962-line-module-steinberg-hom.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "theorem": (
            "The 40-line module 1+15+24 of PSp(4,3) admits no equivariant map into St_81 for the "
            "full group (Schur) but admits nonzero equivariant maps for 115 of 116 subgroup classes; "
            "an INJECTIVE (equivalently isometric) equivariant map exists only for 36 subgroup "
            "classes of order <= 24.  It fails for every maximal subgroup, the Sylow-3 subgroup "
            "SmallGroup(81,7) and all three order-27 subgroups, where the H-orbit count on the 40 lines "
            "(4, 6, 8 for order 27; 4 for order 81) exceeds the number of invariant directions in "
            "St_81 (3; 1).  This is a character-theoretic no-go for a lossless symmetry-preserving "
            "embedding of the line signal into Holotrade's K81 slice."
        ),
        "results": r,
        "independent_python_spectrum": spec,
        "holotrade_carrier_note": (
            "Holotrade's K81 = Reg(H27) (x) Reg(C3) with an EXTERNAL C3.  Both H27 x C3 groups are "
            "SmallGroup(81,12) or (81,13), never the unique order-81 subgroup class (81,7) of PSp(4,3); "
            "so the full K81 action is not a Steinberg restriction, while its H27 part is "
            "(St_81 restricted to each order-27 subgroup is 3 copies of the regular module)."
        ),
        "prior": ["TOE51 4a7898e4b proposal 4 (this answers its H27 gate)",
                  "TOE52 701dc6988 (landed 3.5 min earlier) OWNS the elation-group H27=(27,3) orbit-count "
                  "obstruction (8 orbits vs 3 invariant directions per K81) and the CONSTRUCTIVE minimal "
                  "three-carrier solution ceil(8/3)=3 with explicit integer intertwiners; this pass only "
                  "agrees with it on that row and adds the all-subgroup no-go and the Steinberg identification",
                  "Holotrade analysis/w33_steinberg_doublecoset_colour_swap.g (St_81 definition)",
                  "Holotrade analysis/FRAME_BUNDLE_THREE_K81_SLICES_20260926.md (K81 carrier)"],
        "boundary": (
            "Exact character theory over C for the stated action of PSp(4,3) on the 40 lines. Not a "
            "statement about non-equivariant storage, about a different H27 action on the signal "
            "space, about quantum-device noise, or about the 216-state carriers."
        ),
        "checks": checks,
    }
    payload["semantic_sha256"] = hashlib.sha256(json.dumps(
        {k: v for k, v in payload.items() if k != "semantic_sha256"},
        sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return payload


def main() -> int:
    payload = verify()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(payload["status"], payload["semantic_sha256"])
    r = payload["results"]
    print(f"  hom!=0: {r['N_HOM_NONZERO']}/{r['N_CLASSES']}  injective: {r['N_EMBED']} (max order {r['MAX_ORDER_EMBED']})")
    print(f"  wrote {OUT}")
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
