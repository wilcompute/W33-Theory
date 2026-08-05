#!/usr/bin/env python3
"""Independent validator for the compiled 327 representative ledger."""
from pathlib import Path
import collections
import hashlib
import json
import numpy as np
from w33_pass1801_1805_common import build_geometry

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "data/PART_BT3430_BT3433_CANONICAL_COVER_REPRESENTATIVES.json"

def main():
    data = json.loads(LEDGER.read_text())
    geometry = build_geometry()
    M = geometry["M"].astype(np.int64)
    reps = data["orbits"]
    assert data["status"] == "PASS_327_CANONICAL_REPRESENTATIVE_LEDGER"
    assert len(reps) == 327
    hist = collections.Counter()
    total = 0
    seen = set()
    for record in reps:
        rows = tuple(record["representative"])
        assert len(rows) == 60 and len(set(rows)) == 60
        assert rows == tuple(sorted(rows))
        assert all(0 <= r < 540 for r in rows)
        assert np.all(M[list(rows)].sum(axis=0) == 1)
        key = hashlib.sha256(bytes().join(int(r).to_bytes(2, "little") for r in rows)).hexdigest()
        assert key not in seen
        seen.add(key)
        orbit = int(record["orbit_size"])
        stabilizer = int(record["stabilizer_order"])
        assert orbit * stabilizer == 25920
        total += orbit
        hist[stabilizer] += 1
    assert total == 3_547_800
    assert hist == {2: 228, 4: 84, 8: 15}
    print("PASS_INDEPENDENT_327_LEDGER", hashlib.sha256(LEDGER.read_bytes()).hexdigest())

if __name__ == "__main__":
    main()
