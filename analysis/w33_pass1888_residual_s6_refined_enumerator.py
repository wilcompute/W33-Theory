#!/usr/bin/env python3
"""Pass 1888: exact exceptional-S6 refined enumerator of the 15-row residual subcode."""
from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROWS = ROOT / "data" / "w33_pass1876_rows45_hex.txt"
COMP = ROOT / "data" / "w33_pass1837_middle_layer_compression.json"
OUT = ROOT / "data" / "w33_pass1888_residual_s6_orbit_enumerator.json"


def read_rows() -> list[int]:
    rows = []
    for line in ROWS.read_text().splitlines():
        limbs = [int(x, 16) for x in line.split()]
        assert len(limbs) == 4
        rows.append(sum(x << (64 * i) for i, x in enumerate(limbs)))
    assert len(rows) == 45
    return rows


def transport(mask: int, perm: tuple[int, ...]) -> int:
    out = 0
    while mask:
        b = (mask & -mask).bit_length() - 1
        out |= 1 << perm[b]
        mask &= mask - 1
    return out


def canonical_hash(d: dict) -> str:
    x = dict(d)
    x.pop("sha256_without_hash_field", None)
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def main() -> dict:
    rows = read_rows()
    comp = json.loads(COMP.read_text())
    residual = [int(v) for v in comp["residual_vertices"]]
    vertex_to_duad = {int(k): int(v) for k, v in comp["residual_to_duad_index"].items()}
    duads = list(itertools.combinations(range(6), 2))
    pos_to_duad = [duads[vertex_to_duad[v]] for v in residual]
    duad_to_pos = {d: i for i, d in enumerate(pos_to_duad)}

    perms = set()
    for p in itertools.permutations(range(6)):
        perms.add(tuple(duad_to_pos[tuple(sorted((p[a], p[b])))] for a, b in pos_to_duad))
    assert len(perms) == 720

    # Classify the 240 coordinates from their row-incidence profiles.
    masks = {"R": 0, "P": 0, "H": 0}
    for e in range(240):
        fw = sum((rows[i] >> e) & 1 for i in range(30))
        rw = sum((rows[i] >> e) & 1 for i in range(30, 45))
        if (fw, rw) == (0, 3):
            masks["R"] |= 1 << e
        elif (fw, rw) == (2, 1):
            masks["P"] |= 1 << e
        elif (fw, rw) == (3, 0):
            masks["H"] |= 1 << e
        else:
            raise AssertionError((e, fw, rw))
    assert [masks[k].bit_count() for k in ("R", "P", "H")] == [20, 180, 40]

    rrows = rows[30:]
    words = [0] * (1 << 15)
    for x in range(1, 1 << 15):
        b = (x & -x).bit_length() - 1
        words[x] = words[x ^ (1 << b)] ^ rrows[b]

    unseen = set(range(1 << 15))
    records = []
    aggregate = Counter()
    while unseen:
        rep = min(unseen)
        orbit = {transport(rep, p) for p in perms}
        unseen.difference_update(orbit)
        values = {
            (
                (words[x] & masks["R"]).bit_count(),
                (words[x] & masks["P"]).bit_count(),
                (words[x] & masks["H"]).bit_count(),
            )
            for x in orbit
        }
        assert len(values) == 1
        wr, wp, wh = values.pop()
        assert wh == 0
        records.append({"representative": rep, "orbit_size": len(orbit), "weights": [wr, wp, wh]})
        aggregate[(wr, wp, wh)] += len(orbit)

    checks = {
        "s6_action_order720": len(perms) == 720,
        "orbit_count156": len(records) == 156,
        "orbit_partition_2pow15": sum(r["orbit_size"] for r in records) == 1 << 15,
        "coordinate_partition_20_180_40": [masks[k].bit_count() for k in ("R", "P", "H")] == [20, 180, 40],
        "phase_weight_zero": all(r["weights"][2] == 0 for r in records),
        "aggregate_total": sum(aggregate.values()) == 1 << 15,
    }
    out = {
        "schema": "w33.pass1888.residual_s6_orbit_enumerator.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "residual_dimension": 15,
        "s6_action_order": len(perms),
        "orbit_count": len(records),
        "assignment_total": 1 << 15,
        "coordinate_partition": {"residual": 20, "pair": 180, "phase": 40},
        "orbit_records": records,
        "aggregate_histogram": [[*k, v] for k, v in sorted(aggregate.items())],
        "aggregate_bin_count": len(aggregate),
        "boundary": "This is the residual subcode only. It does not replace the unresolved mixed fiber-residual contraction.",
    }
    assert all(checks.values())
    out["sha256_without_hash_field"] = canonical_hash(out)
    OUT.write_text(json.dumps(out, sort_keys=True, separators=(",", ":")) + "\n")
    print(json.dumps({"status": out["status"], "orbits": len(records), "bins": len(aggregate), "sha256": out["sha256_without_hash_field"]}, indent=2))
    return out


if __name__ == "__main__":
    main()
