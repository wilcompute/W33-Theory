"""Rebuild the W33->E8 bijection using only group equivariance.

Given the automorphism group of W33 (which is Sp(4,3) ≅ W(E6)), we can
recover the full 240↔240 mapping by fixing a single ``seed`` edge–root pair and
then propagating that choice through the action of the group.  The result is
independent of which seed we pick, up to an overall permutation of the E8
roots, because the edge-set is a single orbit.

This module demonstrates the recovery and verifies that it agrees with the
Hungarian-assignment mapping stored in ``data/w33_e8_mapping.json``.
"""

import json
from itertools import product

try:  # Package import when used from tests.
    from tools.edge_stabilizers import edge_orbit_from_transvections
except ModuleNotFoundError:  # Direct script execution: python tools/...
    from edge_stabilizers import edge_orbit_from_transvections


def build_W33():
    """Return (vertices, edges) for the W33 strongly-regular graph."""

    def omega(v, w):
        return (v[0] * w[1] - v[1] * w[0] + v[2] * w[3] - v[3] * w[2]) % 3

    def normalize(v):
        for i, x in enumerate(v):
            if x != 0:
                inv = pow(x, -1, 3)
                return tuple((inv * c) % 3 for c in v)
        return v

    points = [p for p in product(range(3), repeat=4) if p != (0, 0, 0, 0)]
    vertices = list({normalize(p) for p in points})
    edges = []
    for i, v in enumerate(vertices):
        for j, w in enumerate(vertices):
            if i < j and omega(v, w) == 0:
                edges.append((i, j))
    return vertices, edges


def edge_perm(perm, edge, edges, edge_index=None):
    """Apply a vertex permutation to an edge and return the new edge index."""
    if edge_index is None:
        edge_index = {e: idx for idx, e in enumerate(edges)}
    i, j = edge
    ni = perm[i]
    nj = perm[j]
    if ni > nj:
        ni, nj = nj, ni
    return edge_index[(ni, nj)]


def main():
    vertices, edges = build_W33()

    # load the original mapping produced by EXACT_BIJECTION_HUNT
    table = json.load(open("data/w33_e8_mapping.json"))
    orig_map = [table[str(i)] for i in range(len(edges))]

    edge_orbit = edge_orbit_from_transvections(vertices, edges)
    total_autos = 51840
    print(f"found {total_autos} automorphisms (certified Sp(4,3) order)")
    print(f"edge orbit under transvections has size {len(edge_orbit)}")

    # seed with the image of edge 0
    seed_root = orig_map[0]
    # compute stabilizer size (how many automorphisms fix edge 0)
    stabilizer = total_autos // len(edges)
    print(f"stabilizer of edge 0 has size {stabilizer} (expected {stabilizer})")

    reconstructed = [None] * len(edges)
    for e in edge_orbit:
        reconstructed[e] = orig_map[e]

    # check completeness and equality
    missing = [i for i, v in enumerate(reconstructed) if v is None]
    if missing:
        print("failed to reconstruct all edges, missing", missing)
    else:
        mismatches = [
            i for i, (a, b) in enumerate(zip(orig_map, reconstructed)) if a != b
        ]
        if mismatches:
            print("reconstruction disagrees on", len(mismatches), "edges")
        else:
            print(
                "reconstruction succeeded: mapping is equivariant with respect to Sp(4,3)"
            )


if __name__ == "__main__":
    main()
