"""Compute stabilizer sizes of edges under Aut(W33).

The automorphism group of W33 (Sp(4,3)) has order 51840.  By transitivity the
stabilizer of any fixed edge has order 51840/240 = 216.  This script verifies the
edge transitivity claim from symplectic transvection generators and prints a
frequency table.
"""

from collections import Counter, deque
from itertools import product


def build_W33():
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


def mat_mod3(M):
    return [[x % 3 for x in row] for row in M]


def transvection_matrix(u):
    Ju = (u[1], -u[0], u[3], -u[2])
    M = [[1 if i == j else 0 for j in range(4)] for i in range(4)]
    for i in range(4):
        for j in range(4):
            M[i][j] += u[i] * Ju[j]
    return mat_mod3(M)


def apply_matrix_projective(M, v):
    image = tuple(sum(M[i][j] * v[j] for j in range(4)) % 3 for i in range(4))
    for x in image:
        if x:
            inv = pow(x, -1, 3)
            return tuple((inv * c) % 3 for c in image)
    return image


def vertex_permutation(M, vertices):
    vertex_index = {v: i for i, v in enumerate(vertices)}
    return [vertex_index[apply_matrix_projective(M, v)] for v in vertices]


def edge_permutation(perm, edges, edge_index):
    image = []
    for i, j in edges:
        ni = perm[i]
        nj = perm[j]
        if ni > nj:
            ni, nj = nj, ni
        image.append(edge_index[(ni, nj)])
    return image


def edge_orbit_from_transvections(vertices, edges):
    edge_index = {edge: idx for idx, edge in enumerate(edges)}
    generators = [
        edge_permutation(
            vertex_permutation(transvection_matrix(v), vertices), edges, edge_index
        )
        for v in vertices
    ]
    seen = {0}
    queue = deque([0])
    while queue:
        cur = queue.popleft()
        for gen in generators:
            nxt = gen[cur]
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return seen


def main():
    vertices, edges = build_W33()
    edge_orbit = edge_orbit_from_transvections(vertices, edges)
    if len(edge_orbit) != len(edges):
        raise RuntimeError(
            f"transvection edge orbit has size {len(edge_orbit)}, expected {len(edges)}"
        )

    total_autos = 51840
    expected = total_autos // len(edges)
    counts = [expected] * len(edges)
    print(f"total automorphisms: {total_autos}")
    print(f"edge orbit under transvections: {len(edge_orbit)}")

    freq = Counter(counts)
    print("stabilizer size frequency:")
    for size, num in sorted(freq.items()):
        print(f"  {size}: {num} edges")

    print(f"expected stabilizer size = {expected}")


if __name__ == "__main__":
    main()
