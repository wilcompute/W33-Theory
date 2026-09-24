#!/usr/bin/env python3
"""Run and freeze the Pass 409 GAP qutrit-edge intertwiner witness."""
from __future__ import annotations

import json
import re
import subprocess, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAP = ROOT / "analysis/w33_pass409_qutrit_edge_intertwiner.g"
OUT = ROOT / "data/w33_pass409_qutrit_edge_intertwiner.json"


def ints(line: str):
    return [int(x) for x in re.findall(r"-?\d+", line)]


def main(write: bool = True):
    if shutil.which("gap"):
        cmd=["gap","-q",str(GAP)]
    else:
        raw=str(GAP).replace("\\","/")
        drive,rest=raw.split(":/",1)
        cmd=["wsl","gap","-q",f"/mnt/{drive.lower()}/{rest}"]
    run = subprocess.run(
        cmd, cwd=ROOT, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True,
    )
    lines = {line.split()[0]: line for line in run.stdout.splitlines() if line.startswith("PASS")}
    assert lines["PASS_QUTRIT_EDGE_EXPLICIT_INTERTWINER"].endswith("true")
    groups = ints(lines["PASS409_GROUPS"])
    characters = ints(lines["PASS409_CHARACTERS"])
    induced = ints(lines["PASS409_INDUCED_FACTORS"])
    edge = ints(lines["PASS409_EDGE_FACTORS"])
    intertwiner = ints(lines["PASS409_INTERTWINER"])
    assert groups == [409, 51840, 1296, 40]
    assert characters == [409, 11, 1, 90]
    assert sorted(induced[1:]) == [10, 60, 80, 90]
    assert sorted(edge[1:]) == [15, 24, 30, 81, 90]
    assert intertwiner[1:] == [90, 90, 90]
    out = {
        "schema": "w33.pass409.qutrit_edge_explicit_intertwiner.v1",
        "status": "PASS_EXPLICIT_RANK90_W_E6_INTERTWINER_OVER_GF103",
        "groups": {"W_E6_order": 51840, "point_stabilizer_order": 1296, "index": 40},
        "character_audit": {
            "canonical_local_H6_id": 11,
            "induced_degrees": [10, 60, 80, 90],
            "signed_edge_degrees": [15, 24, 30, 81, 90],
            "inner_product": 1,
            "unique_common_degree": 90,
        },
        "matrix_witness": {
            "field": "GF(103)",
            "reason_for_prime": "103 does not divide 51840 and contains primitive cube roots",
            "induced_module_dimension": 240,
            "signed_edge_module_dimension": 240,
            "induced_W90_basis_shape": [90, 240],
            "edge_W90_basis_shape": [90, 240],
            "intertwiner_shape": [90, 90],
            "intertwiner_rank": 90,
            "generator_equations": "M_ind(g) T = T M_edge(g) for all three frozen W(E6) generators",
            "all_generator_equations_hold": True,
            "basis_choice": "MeatAxe may choose different valid bases; the certificate freezes dimensions, rank, and all generator equations rather than a basis-dependent checksum.",
        },
        "theorem": "The unique common degree-90 constituent is realized by an explicit invertible 90x90 matrix over GF(103) intertwining the three frozen W(E6) generators. Thus the canonical qutrit fibre and orientation-signed W33 edge lane share an actual equivariant transducer, not merely a character overlap.",
        "boundary": "This is an exact modular representation-theoretic transducer. A characteristic-zero integral lift and optical amplitude normalization are not supplied.",
        "parents": [
            "analysis/w33_20260923_qutrit_edge_triality_transducer.g",
            "analysis/w33_20260923_corrected_weil6_e6_extension.g",
        ],
    }
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    return out


if __name__ == "__main__":
    print(json.dumps(main(True), indent=2))
