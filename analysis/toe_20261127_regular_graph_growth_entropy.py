"""Degree-four geometry controls for the regular-graph entropy bound."""
import json
from math import ceil, exp, lgamma, log, pi, sin

import networkx as nx
import numpy as np
from scipy.sparse.linalg import eigsh


def ball_layers(graph, seed, radius, allowed):
    ball, layer = {seed}, {seed}
    layers = [ball.copy()]
    for _ in range(radius):
        layer = {v for u in layer for v in graph[u]} & allowed - ball
        ball |= layer
        layers.append(ball.copy())
    return layers


def partition(graph, radius):
    """Greedily choose the smallest consecutive-ball growth ratio."""
    remaining = set(graph)
    blocks = []
    cuts = 0
    while remaining:
        balls = ball_layers(graph, min(remaining), radius, remaining)
        ratios = [len(balls[r+1])/len(balls[r]) for r in range(radius)]
        r = min(range(radius), key=lambda i: (ratios[i], -len(balls[i])))
        block = balls[r]
        boundary = sum(v in remaining and v not in block for u in block for v in graph[u])
        assert boundary <= 4*(len(balls[r+1])-len(block))
        blocks.append(block)
        cuts += boundary
        remaining.difference_update(block)
    lookup = {vertex: i for i, block in enumerate(blocks) for vertex in block}
    assert len(lookup) == len(graph)
    assert cuts == sum(lookup[u] != lookup[v] for u, v in graph.edges)
    return {"blocks": len(blocks), "max_block": max(map(len, blocks)), "cut_edges": cuts}


def observe(graph, seed):
    n = len(graph)
    rng = np.random.default_rng(seed)
    radii = (2, 4, 6)
    samples = rng.choice(n, size=24, replace=False)
    volumes = [ball_layers(graph, int(v), max(radii), set(graph)) for v in samples]
    matrices = nx.laplacian_matrix(graph).astype(float)
    eigenvalues = np.sort(eigsh(matrices, k=3, which="SM", v0=rng.normal(size=n),
                               tol=1e-9, return_eigenvectors=False))
    assert abs(eigenvalues[0]) < 1e-8 and eigenvalues[1] > 0
    return {"mean_ball_counts": [float(np.mean([len(v[r]) for v in volumes])) for r in radii],
            "laplacian_gap": float(eigenvalues[1]), "partition_at_radius_8": partition(graph,8)}


def build():
    rows = []
    for side in (16,32,64):
        n = side**2
        torus = nx.convert_node_labels_to_integers(nx.grid_2d_graph(side,side,periodic=True))
        random = nx.random_regular_graph(4,n,seed=271828+side)
        a,b = observe(torus,side),observe(random,side)
        assert a["mean_ball_counts"] == [13.,41.,85.]
        assert abs(a["laplacian_gap"]-4*sin(pi/side)**2) < 1e-9
        assert b["laplacian_gap"] > .4 and b["mean_ball_counts"][-1] > 3*85
        # Fixed-degree configuration count, with asymptotic simple-graph correction.
        log_count = lgamma(4*n+1)-2*n*log(2)-lgamma(2*n+1)-n*lgamma(5)-15/4
        rows.append({"side":side,"n":n,"periodic_square_lattice":a,"random_degree_four":b,
                     "leading_asymptotic_entropy_per_vertex_excess_over_log_n_factorial":
                         (log_count-lgamma(n+1))/n})
    return {"status":"PASS","radii":[2,4,6],"fixed_seeds":True,"rows":rows,
            "leading_log_probability_coefficient_for_uniform_polynomial_growth":-1}


if __name__ == "__main__":
    print(json.dumps(build(),indent=2))
