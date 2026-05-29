"""Produce a small algebraic seed for the transport CSP using E6/E8 artifacts.

This heuristic generator uses the exact E8 -> E6 x A2 decomposition and the
minuscule E6 27x3 phase factorization to propose a small set of initial edge->root
assignments (seed_edges) that can be supplied to the repo search/harness as
guiding seeds.  The produced JSON is intentionally conservative: it fills only
the first K packet indices with a deterministic, well-distributed selection of
roots drawn from the E8 root packet and aligned to A2 phase indices.

Usage (run locally inside the repo venv):
  python scripts/transport_algebraic_seeder.py --out data/transport_algebraic_seed.json --count 48

This is a heuristic: any produced seed must be verified by the existing
verification flow (scripts/transport_result_verify.py) after running a full
solver or backtrack search seeded with the produced file.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import List, Tuple

ROOT = Path(__file__).resolve().parents[1]
import sys
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def load_packet_data() -> dict:
    from scripts.w33_h4_orbital_no_go import compute_quadrangle_adjacent_transport_packet_action_data

    return compute_quadrangle_adjacent_transport_packet_action_data()


def load_e8_roots() -> List[Tuple]:
    from analysis.w33_tetracode_e8_root_system_bridge import e8_roots_from_w33_tetracode

    roots_map = e8_roots_from_w33_tetracode()
    # canonical sorted list used elsewhere in repo
    roots = sorted(roots_map.keys())
    return roots


def block_pair(root, coordinate: int):
    # same as analysis helper: return (a,b) for A2 block
    return (root[2 * coordinate], root[2 * coordinate + 1])


def find_candidate_root_for_cell(roots, coordinate: int, phase_index: int):
    """Find a root index among `roots` whose block_pair at `coordinate` matches
    one of the A2 coset minima that corresponds to the requested `phase_index`.
    We prefer tetracode-derived roots (source startswith 'tetracode') when available.
    If no exact phase match is found, fall back to a distributed pick.
    """
    from analysis.w33_tetracode_e8_root_system_bridge import A2_COSET_ONE_MINIMA, e8_roots_from_w33_tetracode

    # canonical phase candidates for phase_index 0..2
    try:
        phase_candidates = [A2_COSET_ONE_MINIMA[phase_index % 3]]
    except Exception:
        phase_candidates = []

    # prefer roots labelled by tetracode glue and matching the block pair
    root_sources = e8_roots_from_w33_tetracode()
    for idx, root in enumerate(roots):
        src = root_sources.get(root, "")
        pair = block_pair(root, coordinate)
        if src.startswith("tetracode") and pair in phase_candidates:
            return idx

    # fallback: pick the first tetracode root with matching pair
    for idx, root in enumerate(roots):
        pair = block_pair(root, coordinate)
        if pair in phase_candidates:
            return idx

    # final fallback: distributed pick to spread selections across index space
    return (coordinate * 37 + phase_index * 13) % len(roots)


def build_seed(count: int = 48) -> dict:
    data = load_packet_data()
    packet_cycles = data.get("packet_cycles") or []
    n = len(packet_cycles)
    roots = load_e8_roots()

    seed_edges = []
    # conservative: only fill up to min(count, n) representative indices
    for i in range(min(count, n)):
        coordinate = i % 4  # cycle across the 4 A2 coordinates
        phase_index = i % 3
        root_idx = find_candidate_root_for_cell(roots, coordinate, phase_index)
        seed_edges.append({"edge_index": int(i), "root_index": int(root_idx)})

    return {"seed_edges": seed_edges, "note": "algebraic heuristic seed: assign first K packet indices using E8->E6xA2 phase alignment"}


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="data/transport_algebraic_seed.json")
    parser.add_argument("--count", type=int, default=48, help="number of seed assignments to produce")
    args = parser.parse_args()

    out = Path(args.out)
    out.parent.mkdir(exist_ok=True)
    seed = build_seed(count=args.count)
    out.write_text(json.dumps(seed, indent=2))
    print(json.dumps({"status": "wrote_seed", "path": str(out), "n_seed_edges": len(seed["seed_edges"])}))


if __name__ == "__main__":
    main()
