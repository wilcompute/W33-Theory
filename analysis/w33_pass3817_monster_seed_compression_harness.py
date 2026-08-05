#!/usr/bin/env python3
"""Fail-closed 36-seed promotion harness for Pass 3817.

A candidate target-group action supplies a 36x36 adjacency matrix already aligned
with the reference labels, plus optional permutation generators. The harness
refuses order-only coincidences: it requires the exact graph, then delegates to
the Passes 3813-3820 verifier whose Norton product reconstructs the 135 K4
frames, 120 triples, [36,6] code, and 45+216+270+120 line split.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from collections import deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "analysis" / "w33_pass3813_3820_quadratic_discriminant_multiport_holonomy.py"


def load_verifier():
    spec = importlib.util.spec_from_file_location("w33_pass3813_3820", VERIFIER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def compose(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def generated_group_order(generators, cap=100000):
    identity = tuple(range(36))
    gens = [tuple(map(int, g)) for g in generators]
    for g in gens:
        if sorted(g) != list(range(36)):
            raise ValueError("generator is not a permutation of 0..35")
    seen = {identity}
    queue = deque([identity])
    while queue:
        x = queue.popleft()
        for g in gens:
            y = compose(g, x)
            if y not in seen:
                seen.add(y)
                if len(seen) > cap:
                    raise ValueError(f"generated group exceeds cap {cap}")
                queue.append(y)
    return len(seen)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    candidate = json.loads(args.candidate.read_text())
    adjacency = np.asarray(candidate.get("adjacency"), dtype=np.int64)
    if adjacency.shape != (36, 36):
        raise SystemExit("candidate adjacency must be 36x36")
    if not np.array_equal(adjacency, adjacency.T) or np.any(np.diag(adjacency)):
        raise SystemExit("candidate adjacency must be symmetric with zero diagonal")

    verifier = load_verifier()
    geometry = verifier.build_geometry()
    reference = np.asarray(geometry["A36"], dtype=np.int64)
    if not np.array_equal(adjacency, reference):
        raise SystemExit("candidate graph is not equal to the aligned frozen 36-seed")

    tower = verifier.build_norton_compression(geometry)
    result = {
        "schema": "w33.pass3817.monster_seed_compression_candidate.v1",
        "status": "PASS_ALIGNED_36_SEED",
        "candidate_label": candidate.get("label", "unnamed"),
        "tower": tower,
        "generator_group_order": None,
        "boundary": "Passing this harness certifies the aligned finite 36-seed and its functorial tower, not a Monster embedding or Monster character fusion.",
    }
    generators = candidate.get("generators")
    if generators is not None:
        order = generated_group_order(generators)
        if order not in {25920, 51840}:
            raise SystemExit(f"unexpected generated permutation-group order {order}")
        for g in generators:
            p = np.asarray(g, dtype=np.int64)
            if not np.array_equal(reference[np.ix_(p, p)], reference):
                raise SystemExit("generator does not preserve the 36-seed graph")
        result["generator_group_order"] = order

    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
