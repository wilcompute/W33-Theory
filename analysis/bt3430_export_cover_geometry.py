#!/usr/bin/env python3
"""Export the canonical 540x240 frame-edge incidence and PSp frame generators."""
from pathlib import Path
import hashlib
from w33_pass1801_1805_common import build_geometry

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_BT3430_CANONICAL_COVER_GEOMETRY.txt"

def main():
    data = build_geometry()
    M = data["M"]
    acts = data["acts"]
    assert M.shape == (540, 240)
    assert set(map(int, M.sum(axis=1))) == {4}
    assert set(map(int, M.sum(axis=0))) == {9}
    assert len(acts) == 5
    lines = [f"540 240 {len(acts)}"]
    for row in M:
        support = [int(x) for x in row.nonzero()[0]]
        assert len(support) == 4
        lines.append(" ".join(map(str, support)))
    for act in acts:
        perm = list(map(int, act[3]))
        assert sorted(perm) == list(range(540))
        lines.append(" ".join(map(str, perm)))
    payload = "\n".join(lines) + "\n"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(payload)
    print("PASS_CANONICAL_540x240_GEOMETRY", hashlib.sha256(payload.encode()).hexdigest())

if __name__ == "__main__":
    main()
