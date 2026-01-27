#!/usr/bin/env python3
"""Repair a partial point decode using inversion cycles and bucket disjointness.

This script is designed for the W33 q=11 decode workflow described in the
research notes. It completes a partial mapping of 66 positions to unordered
label pairs from PG(1,11), honoring:
  - fixed positions that must map to inversion-fixed label pairs,
  - 2-cycles that must map to inversion partner pairs,
  - per-bucket disjointness of labels (perfect matching constraint).

Input formats:
  --partial-csv: CSV with headers: pos,label_u,label_v
  --bucket-map: JSON mapping string/int position -> bucket id
  --cycle-map: JSON with keys:
      {"fixed": [pos,...], "pairs": [[pos_a,pos_b], ...]}
  --label-inversion: JSON mapping label -> inversion(label)

Outputs:
  --output-csv: CSV with columns: pos,bucket,pair_idx,label_u,label_v
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple


@dataclass(frozen=True)
class Position:
    pos: int
    bucket: str


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def normalize_int_key_map(raw: dict) -> Dict[int, str]:
    normalized: Dict[int, str] = {}
    for key, value in raw.items():
        normalized[int(key)] = str(value)
    return normalized


def read_partial_csv(path: Path) -> Dict[int, Tuple[int, int]]:
    partial: Dict[int, Tuple[int, int]] = {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            pos = int(row["pos"])
            u = int(row["label_u"])
            v = int(row["label_v"])
            if u == v:
                raise ValueError(f"Invalid pair at pos {pos}: labels must differ")
            partial[pos] = tuple(sorted((u, v)))
    return partial


def build_pairs(labels: Iterable[int]) -> List[Tuple[int, int]]:
    pairs = [tuple(sorted(pair)) for pair in itertools.combinations(sorted(labels), 2)]
    return pairs


def build_pair_index(pairs: List[Tuple[int, int]]) -> Dict[Tuple[int, int], int]:
    return {pair: idx for idx, pair in enumerate(pairs)}


def build_pair_inversion(
    pairs: List[Tuple[int, int]],
    pair_index: Dict[Tuple[int, int], int],
    label_inversion: Dict[int, int],
) -> Dict[int, int]:
    inversion: Dict[int, int] = {}
    for idx, (u, v) in enumerate(pairs):
        inv_pair = tuple(sorted((label_inversion[u], label_inversion[v])))
        inversion[idx] = pair_index[inv_pair]
    return inversion


def bucket_used_labels(assignments: Dict[int, int], pairs: List[Tuple[int, int]], positions: Dict[int, Position]) -> Dict[str, Set[int]]:
    used: Dict[str, Set[int]] = {}
    for pos, pair_idx in assignments.items():
        bucket = positions[pos].bucket
        used.setdefault(bucket, set()).update(pairs[pair_idx])
    return used


def compute_domains(
    positions: Dict[int, Position],
    fixed_positions: Set[int],
    paired_positions: Dict[int, int],
    fixed_pairs: Set[int],
    pair_inversion: Dict[int, int],
    assignments: Dict[int, int],
) -> Dict[int, Set[int]]:
    domains: Dict[int, Set[int]] = {}
    all_pairs = set(pair_inversion.keys())
    for pos in positions:
        if pos in assignments:
            continue
        if pos in fixed_positions:
            domains[pos] = set(fixed_pairs)
        elif pos in paired_positions and paired_positions[pos] in assignments:
            domains[pos] = {pair_inversion[assignments[paired_positions[pos]]]} 
        else:
            domains[pos] = set(all_pairs)
    return domains


def is_bucket_feasible(
    bucket: str,
    assignments: Dict[int, int],
    pairs: List[Tuple[int, int]],
    positions: Dict[int, Position],
    domain_cache: Dict[int, Set[int]],
) -> bool:
    used = set()
    remaining = 0
    for pos, assignment in assignments.items():
        if positions[pos].bucket == bucket:
            used.update(pairs[assignment])
    for pos in positions:
        if positions[pos].bucket != bucket:
            continue
        if pos in assignments:
            continue
        remaining += 1
    available_labels = 0
    label_pool: Set[int] = set()
    for pos, domain in domain_cache.items():
        if positions[pos].bucket != bucket:
            continue
        for pair_idx in domain:
            label_pool.update(pairs[pair_idx])
    available_labels = len(label_pool.difference(used))
    return available_labels >= 2 * remaining


def solve_decode(
    positions: Dict[int, Position],
    pairs: List[Tuple[int, int]],
    pair_inversion: Dict[int, int],
    fixed_positions: Set[int],
    paired_positions: Dict[int, int],
    fixed_pairs: Set[int],
    assignments: Dict[int, int],
) -> Optional[Dict[int, int]]:
    used_labels = bucket_used_labels(assignments, pairs, positions)

    def backtrack(assignments_local: Dict[int, int]) -> Optional[Dict[int, int]]:
        if len(assignments_local) == len(positions):
            return assignments_local

        domains = compute_domains(
            positions, fixed_positions, paired_positions, fixed_pairs, pair_inversion, assignments_local
        )
        next_pos = min(domains, key=lambda p: len(domains[p]))
        domain_list = sorted(domains[next_pos])

        for pair_idx in domain_list:
            labels = set(pairs[pair_idx])
            bucket = positions[next_pos].bucket
            if labels & used_labels.get(bucket, set()):
                continue

            new_assignments = dict(assignments_local)
            new_assignments[next_pos] = pair_idx
            partner = paired_positions.get(next_pos)
            added = [(next_pos, pair_idx)]
            if partner is not None and partner not in new_assignments:
                partner_pair = pair_inversion[pair_idx]
                partner_labels = set(pairs[partner_pair])
                partner_bucket = positions[partner].bucket
                if partner_labels & used_labels.get(partner_bucket, set()):
                    continue
                new_assignments[partner] = partner_pair
                added.append((partner, partner_pair))

            for pos_added, pair_added in added:
                used_labels.setdefault(positions[pos_added].bucket, set()).update(pairs[pair_added])

            domain_cache = compute_domains(
                positions, fixed_positions, paired_positions, fixed_pairs, pair_inversion, new_assignments
            )
            buckets = {positions[pos].bucket for pos in positions}
            if all(is_bucket_feasible(bucket, new_assignments, pairs, positions, domain_cache) for bucket in buckets):
                result = backtrack(new_assignments)
                if result is not None:
                    return result

            for pos_added, pair_added in added:
                used_labels[positions[pos_added].bucket].difference_update(pairs[pair_added])

        return None

    return backtrack(assignments)


def main() -> None:
    parser = argparse.ArgumentParser(description="Repair a partial point decode.")
    parser.add_argument("--partial-csv", type=Path, required=True, help="CSV with pos,label_u,label_v")
    parser.add_argument("--bucket-map", type=Path, required=True, help="JSON mapping pos -> bucket")
    parser.add_argument("--cycle-map", type=Path, required=True, help="JSON with fixed positions and pair cycles")
    parser.add_argument("--label-inversion", type=Path, required=True, help="JSON mapping label -> inversion(label)")
    parser.add_argument("--output-csv", type=Path, required=True, help="Output CSV path")
    args = parser.parse_args()

    partial_pairs = read_partial_csv(args.partial_csv)
    bucket_map = normalize_int_key_map(load_json(args.bucket_map))
    cycle_map = load_json(args.cycle_map)
    label_inversion_raw = load_json(args.label_inversion)
    label_inversion = {int(k): int(v) for k, v in label_inversion_raw.items()}

    positions = {pos: Position(pos=pos, bucket=bucket) for pos, bucket in bucket_map.items()}
    labels = sorted(label_inversion.keys())
    pairs = build_pairs(labels)
    pair_index = build_pair_index(pairs)
    pair_inversion = build_pair_inversion(pairs, pair_index, label_inversion)

    fixed_positions = {int(pos) for pos in cycle_map.get("fixed", [])}
    paired_positions: Dict[int, int] = {}
    for a, b in cycle_map.get("pairs", []):
        paired_positions[int(a)] = int(b)
        paired_positions[int(b)] = int(a)

    fixed_pairs = {idx for idx, inv in pair_inversion.items() if idx == inv}

    assignments: Dict[int, int] = {}
    for pos, (u, v) in partial_pairs.items():
        pair_idx = pair_index[(u, v)]
        assignments[pos] = pair_idx
        if pos in fixed_positions and pair_idx not in fixed_pairs:
            raise ValueError(f"pos {pos} must be fixed but got non-fixed pair {u}-{v}")
        if pos in paired_positions:
            partner = paired_positions[pos]
            if partner in assignments and assignments[partner] != pair_inversion[pair_idx]:
                raise ValueError(
                    f"pos {pos} assigned pair {pair_idx} but partner {partner} mismatch"
                )

    solution = solve_decode(
        positions,
        pairs,
        pair_inversion,
        fixed_positions,
        paired_positions,
        fixed_pairs,
        assignments,
    )
    if solution is None:
        raise SystemExit("No solution found under provided constraints.")

    with args.output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["pos", "bucket", "pair_idx", "label_u", "label_v"])
        for pos in sorted(solution):
            pair_idx = solution[pos]
            u, v = pairs[pair_idx]
            writer.writerow([pos, positions[pos].bucket, pair_idx, u, v])


if __name__ == "__main__":
    main()
