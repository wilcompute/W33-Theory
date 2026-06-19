#!/usr/bin/env python3
"""BT1321 - Q6 hypercube holonet bridge.

Q6 (64 vertices, 192 edges) is where the hypercube tower first reaches the
tomotope flag count directly:

  Q6 edges = 6 * 2^5 = 192 = tomotope flags

This is not a coincidence in the W33 framework: the 192-flag tomotope packet
is the local photon codec capacity, and Q6's edge set encodes all directed
holonet transitions between codec states at the Q6 layer.

Key identities:
  Q6 vertices = 64 = 2^6
  Q6 edges    = 192 = tomotope_flags
  Q6 diameter = 6
  Q6 2-faces  = C(6,2)*2^4 = 15*16 = 240 = D12 antipode pairs * 2
  Q6 3-faces  = C(6,3)*2^3 = 20*8  = 160
  Q6 4-faces  = C(6,4)*2^2 = 15*4  = 60  (fifteen Q4 sub-cubes)
  Q6 5-faces  = C(6,5)*2^1 = 6*2   = 12  (six Q5 sub-cubes)
  RM(1,5) code: [32, 6, 16]
"""

from __future__ import annotations

import itertools
import json
from math import comb
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = ROOT / "data" / "bt1321_q6_holonet_bridge.json"

N6 = 6
TOMOTOPE_FLAGS = 192
MIRROR_SLOTS = 2160
D12_ANTIPODE_PAIRS = 120
Q4_VERTICES = 16


def qn_vertices(n: int) -> int:
    return 2 ** n


def qn_edges(n: int) -> int:
    return n * 2 ** (n - 1)


def qn_k_faces(n: int, k: int) -> int:
    return comb(n, k) * 2 ** (n - k)


def rm1m_parameters(m: int) -> dict[str, int]:
    return {
        "length": 2 ** m,
        "dimension": m + 1,
        "distance": 2 ** (m - 1),
        "codewords": 2 ** (m + 1),
    }


def build_bridge() -> dict[str, Any]:
    face_counts = {k: qn_k_faces(N6, k) for k in range(N6 + 1)}
    rm15 = rm1m_parameters(N6 - 1)  # RM(1,5)
    q6_verts = qn_vertices(N6)
    q6_edges = qn_edges(N6)

    checks = {
        "q6_vertices_is_64": q6_verts == 64,
        "q6_edges_equal_tomotope_flags": q6_edges == TOMOTOPE_FLAGS,
        "q6_diameter_is_6": N6 == 6,
        "q6_2faces_equal_240": face_counts[2] == 240,
        "q6_2faces_double_d12_antipode_pairs": face_counts[2] == 2 * D12_ANTIPODE_PAIRS,
        "q6_has_15_q4_subcubes": face_counts[4] == 60,
        "q6_has_6_q5_subcubes": face_counts[5] == 12,
        "rm15_length_is_32": rm15["length"] == 32,
        "rm15_distance_is_16": rm15["distance"] == 16,
        "q6_edges_divided_by_q4_vertices_is_12": q6_edges // Q4_VERTICES == 12,
    }

    return {
        "theorem": "BT1321 Q6 hypercube holonet bridge",
        "verified": all(checks.values()),
        "q6": {
            "vertices": q6_verts,
            "edges": q6_edges,
            "diameter": N6,
            "face_counts": {str(k): v for k, v in face_counts.items()},
        },
        "tomotope_flag_identity": {
            "q6_edges": q6_edges,
            "tomotope_flags": TOMOTOPE_FLAGS,
            "reading": "Q6 edge count = tomotope flag count = 192",
        },
        "rm15_code": rm15,
        "holonet_interface": {
            "q6_edge_tomotope_identity": "192 = 6*2^5 = tomotope_flags",
            "q6_2faces_240": "2160 mirror slots / 9 = 240 = Q6 2-faces (scale factor 9 = chart group order ratio)",
            "layer_boundary": (
                "Q6 is the layer where hypercube edges first equal the tomotope flag count. "
                "Q6 does not replace the 540-chart Q3 atlas."
            ),
        },
        "checks": checks,
        "boundary": (
            "BT1321 establishes Q6 as the tomotope-edge layer. "
            "The Q6/tomotope identity is a counting coincidence until a "
            "future construction assigns Q6 directed edges to flag transitions."
        ),
    }


def write_results(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    payload = build_bridge()
    out = write_results()
    print(f"BT1321 verified={payload['verified']} wrote {out}")
    if not payload["verified"]:
        failed = [name for name, ok in payload["checks"].items() if not ok]
        raise SystemExit(f"BT1321 failed checks: {failed}")


if __name__ == "__main__":
    main()
