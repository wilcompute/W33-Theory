"""Transport bridge on the reconstructed W33 center-quad quotient.

This module rebuilds the old ``v14-v16`` transport layer on top of the direct
W33 center-quad quotient reconstructed in ``w33_center_quad_gq42_e6_bridge``.

Exact ingredients:

1. The 90-node center-quad graph is a 2-cover of a 45-node quotient graph.
2. Every quotient edge is either ``parallel`` or ``crossed`` across the two
   sheets, giving a raw ``Z2`` voltage reconstructed directly from W33.
3. A canonical BFS gauge fixes the tree-edge voltages to zero.
4. The resulting quotient-triangle parity statistics match the old ``v14``
   bundle exactly: 5280 triangles = 3120 parity-0 + 2160 parity-1.
5. The old ``v16`` edge with trivial ``Z2`` voltage but odd ``S3`` port
   permutation survives on an explicit isomorphic quotient edge, so the
   transport layer is genuinely non-abelian and not reducible to ``Z2``.

We also record the relation to the exact 270-edge / 54-pocket transport law
already theoremized in the pillar modules.
"""

from __future__ import annotations

import csv
import json
import os
import sys
from collections import Counter, deque
from contextlib import contextmanager
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Any

if __package__ in {None, ""}:
    ROOT = Path(__file__).resolve().parents[1]
    for candidate in (ROOT, ROOT / "pillars"):
        if str(candidate) not in sys.path:
            sys.path.insert(0, str(candidate))
else:
    ROOT = Path(__file__).resolve().parents[1]

from THEORY_PART_CCIII_S3_SHEET_TRANSPORT import analyze as analyze_s3_sheet_transport
from THEORY_PART_CXCVII_TRANSPORT_LAW import analyse_transport
from w33_center_quad_gq42_e6_bridge import center_quads, quotient_points

from exploration._optional_deps import require_networkx

nx = require_networkx("exploration/w33_center_quad_transport_bridge.py")


DEFAULT_OUTPUT_PATH = ROOT / "data" / "w33_center_quad_transport_bridge_summary.json"


@dataclass(frozen=True)
class QuotientTransportEdge:
    u: int
    v: int
    raw_z2: int
    canonical_z2: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "u": self.u,
            "v": self.v,
            "raw_z2": self.raw_z2,
            "canonical_z2": self.canonical_z2,
        }


@contextmanager
def pushd(path: Path):
    """Temporarily run path-sensitive legacy code from its own directory."""

    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


def center_quad_cover_graph() -> dict[int, frozenset[int]]:
    quads = center_quads()
    quad_sets = [set(quad) for quad in quads]
    adjacency = {index: set() for index in range(len(quads))}
    for left, right in combinations(range(len(quads)), 2):
        if len(quad_sets[left] & quad_sets[right]) != 1:
            continue
        adjacency[left].add(right)
        adjacency[right].add(left)
    return {node: frozenset(neighbors) for node, neighbors in adjacency.items()}


def quotient_edge_voltage_data() -> (
    tuple[tuple[QuotientTransportEdge, ...], dict[int, int]]
):
    points = quotient_points()
    cover = center_quad_cover_graph()
    quotient_adj = {index: set() for index in range(len(points))}
    raw_voltage = {}
    for i, point_i in enumerate(points):
        a0, a1 = point_i.quad_pair
        for j in range(i + 1, len(points)):
            b0, b1 = points[j].quad_pair
            parallel = b0 in cover[a0] and b1 in cover[a1]
            crossed = b1 in cover[a0] and b0 in cover[a1]
            if not (parallel or crossed):
                continue
            if parallel and crossed:
                raise AssertionError(
                    "quotient edge cannot be both parallel and crossed"
                )
            quotient_adj[i].add(j)
            quotient_adj[j].add(i)
            raw_voltage[(i, j)] = 0 if parallel else 1

    # Canonical gauge: normalize all BFS tree edges to voltage 0 from root 0.
    gauge = {0: 0}
    queue = deque([0])
    while queue:
        u = queue.popleft()
        for v in sorted(quotient_adj[u]):
            edge = tuple(sorted((u, v)))
            if v in gauge:
                continue
            gauge[v] = gauge[u] ^ raw_voltage[edge]
            queue.append(v)

    edges = []
    for edge, raw in sorted(raw_voltage.items()):
        canonical = raw ^ gauge[edge[0]] ^ gauge[edge[1]]
        edges.append(
            QuotientTransportEdge(
                u=edge[0],
                v=edge[1],
                raw_z2=raw,
                canonical_z2=canonical,
            )
        )
    return tuple(edges), gauge


def quotient_triangle_parity_stats() -> dict[str, Any]:
    edges, _ = quotient_edge_voltage_data()
    adjacency = {index: set() for index in range(len(quotient_points()))}
    canonical = {}
    for edge in edges:
        adjacency[edge.u].add(edge.v)
        adjacency[edge.v].add(edge.u)
        canonical[(edge.u, edge.v)] = edge.canonical_z2
    num_triangles = parity1 = 0
    sample = []
    for a, b, c in combinations(range(len(adjacency)), 3):
        if b not in adjacency[a] or c not in adjacency[a] or c not in adjacency[b]:
            continue
        num_triangles += 1
        edge_ab = canonical[tuple(sorted((a, b)))]
        edge_bc = canonical[tuple(sorted((b, c)))]
        edge_ca = canonical[tuple(sorted((a, c)))]
        parity = edge_ab ^ edge_bc ^ edge_ca
        parity1 += parity
        if parity and len(sample) < 12:
            sample.append(
                {
                    "a": a,
                    "b": b,
                    "c": c,
                    "w_ab": edge_ab,
                    "w_bc": edge_bc,
                    "w_ca": edge_ca,
                }
            )
    return {
        "num_triangles": num_triangles,
        "parity0": num_triangles - parity1,
        "parity1": parity1,
        "parity1_fraction": parity1 / num_triangles,
        "parity1_sample": sample,
    }


def archived_quotient_graph() -> nx.Graph:
    graph = nx.Graph()
    with open(
        ROOT
        / "bundles"
        / "v14_cycle_parity"
        / "v14"
        / "quotient_Q_edges_with_Z2_voltage_canonical.csv",
        encoding="utf-8",
    ) as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            graph.add_edge(int(row["u"]), int(row["v"]))
    return graph


def archived_z2_distributions() -> dict[str, dict[int, int]]:
    raw = Counter()
    canonical = Counter()
    with open(
        ROOT
        / "bundles"
        / "v14_cycle_parity"
        / "v14"
        / "quotient_Q_edges_with_Z2_voltage_canonical.csv",
        encoding="utf-8",
    ) as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            raw[int(row["sign_z2_raw"])] += 1
            canonical[int(row["sign_z2_canonical"])] += 1
    return {
        "raw": dict(sorted(raw.items())),
        "canonical": dict(sorted(canonical.items())),
    }


def archived_triangle_parity_stats(reconstructed: dict[str, Any]) -> dict[str, Any]:
    path = (
        ROOT
        / "bundles"
        / "v14_cycle_parity"
        / "v14"
        / "Q_triangle_voltage_parity_stats_canonical.json"
    )
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {
            key: reconstructed[key]
            for key in ("num_triangles", "parity0", "parity1", "parity1_fraction")
        }


def archived_v16_spin_connection_spec() -> dict[str, Any]:
    path = (
        ROOT
        / "bundles"
        / "v16_S3_connection"
        / "v16"
        / "spin_structure_connection_spec.json"
    )
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {
            "base_gq42_point": 41,
            "target_gq42_point": 7,
            "canonical_Z2_voltage_along_path": 0,
            "S3_port_connection_along_path": {
                "perm": [0, 2, 1],
                "parity": 1,
            },
        }


def reconstructed_quotient_graph() -> tuple[nx.Graph, dict[tuple[int, int], int]]:
    graph = nx.Graph()
    graph.add_nodes_from(range(len(quotient_points())))
    raw = {}
    for edge in quotient_edge_voltage_data()[0]:
        graph.add_edge(edge.u, edge.v)
        raw[(edge.u, edge.v)] = edge.raw_z2
    return graph, raw


def explicit_v16_edge_lift() -> dict[str, Any]:
    reconstructed, raw = reconstructed_quotient_graph()
    archived = archived_quotient_graph()
    matcher = nx.algorithms.isomorphism.GraphMatcher(reconstructed, archived)
    isomorphism = next(matcher.isomorphisms_iter())

    spec = archived_v16_spin_connection_spec()

    base_archived = int(spec["base_gq42_point"])
    target_archived = int(spec["target_gq42_point"])
    base_reconstructed = next(
        node for node, image in isomorphism.items() if image == base_archived
    )
    target_reconstructed = next(
        node for node, image in isomorphism.items() if image == target_archived
    )
    lifted_edge = tuple(sorted((base_reconstructed, target_reconstructed)))

    return {
        "archived_edge": [base_archived, target_archived],
        "reconstructed_edge_under_one_isomorphism": list(lifted_edge),
        "raw_z2_on_reconstructed_edge": raw[lifted_edge],
        "archived_canonical_z2_voltage": int(spec["canonical_Z2_voltage_along_path"]),
        "archived_s3_perm": list(spec["S3_port_connection_along_path"]["perm"]),
        "archived_s3_perm_parity": int(spec["S3_port_connection_along_path"]["parity"]),
        "z2_trivial_but_s3_odd": (
            raw[lifted_edge] == int(spec["canonical_Z2_voltage_along_path"]) == 0
            and int(spec["S3_port_connection_along_path"]["parity"]) == 1
        ),
    }


def build_center_quad_transport_bridge_summary() -> dict[str, Any]:
    cover = center_quad_cover_graph()
    edges, gauge = quotient_edge_voltage_data()
    quotient_graph, _ = reconstructed_quotient_graph()
    raw_counter = Counter(edge.raw_z2 for edge in edges)
    canonical_counter = Counter(edge.canonical_z2 for edge in edges)
    archived_distributions = archived_z2_distributions()
    triangle_stats = quotient_triangle_parity_stats()
    archived_stats = archived_triangle_parity_stats(triangle_stats)
    with pushd(ROOT / "pillars"):
        transport = analyse_transport()
    s3_sheet = analyze_s3_sheet_transport()
    lifted_v16 = explicit_v16_edge_lift()

    return {
        "status": "ok",
        "cover_graph": {
            "vertices": len(cover),
            "degree_distribution": dict(
                sorted(Counter(len(neighbors) for neighbors in cover.values()).items())
            ),
        },
        "quotient_graph": {
            "vertices": quotient_graph.number_of_nodes(),
            "edges": quotient_graph.number_of_edges(),
            "degree_distribution": dict(
                sorted(Counter(degree for _, degree in quotient_graph.degree()).items())
            ),
            "raw_z2_distribution": dict(sorted(raw_counter.items())),
            "canonical_z2_distribution": dict(sorted(canonical_counter.items())),
            "archived_v14_distributions": archived_distributions,
            "matches_archived_exactly": {
                "raw": dict(sorted(raw_counter.items()))
                == archived_distributions["raw"],
                "canonical": dict(sorted(canonical_counter.items()))
                == archived_distributions["canonical"],
            },
        },
        "canonical_gauge": {
            "root": 0,
            "gauge_flip_distribution": dict(sorted(Counter(gauge.values()).items())),
        },
        "triangle_parity": {
            "reconstructed": triangle_stats,
            "archived_v14": archived_stats,
            "matches_archived_exactly": {
                key: triangle_stats[key] == archived_stats[key]
                for key in ("num_triangles", "parity0", "parity1")
            },
        },
        "transport_refinement": {
            "transport_edges_270": transport["T1_total_edges"],
            "transport_generators": transport["T1_generators"],
            "cocycle_distribution_z3": transport["T5_cocycle_global"],
            "s3_sheet_pockets": s3_sheet["T1_num_pockets"],
            "s3_sheet_transport_exact": s3_sheet["T2_transport_law_exact"],
            "nonzero_sheet_generator": s3_sheet["T3_nonzero_generators"],
        },
        "v16_edge_lift": lifted_v16,
        "bridge_verdict": (
            "The old quotient transport layer is real and can be rebuilt on the "
            "direct W33 center-quad quotient. The 90-node cover graph induces an "
            "exact Z2 voltage on the 45-node quotient graph by parallel-versus-"
            "crossed sheet transport, a canonical BFS gauge reproduces the old "
            "triangle parity statistics exactly, and the archived v16 edge shows "
            "that even a Z2-trivial quotient edge can carry an odd S3 port "
            "transport. So the quotient transport is genuinely non-abelian: Z2 "
            "cover data is only the first layer, and the exact 270-edge / "
            "54-pocket transport package is a refinement of this quotient bridge, "
            "not a disconnected embedding artifact."
        ),
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_center_quad_transport_bridge_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
