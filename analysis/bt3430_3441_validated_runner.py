#!/usr/bin/env python3
"""Canonical runner for Passes 3430--3441.

It patches the derivation module's overly strong presentation assertion: a
spectrally compatible equitable quotient need only be reducible/disconnected,
not diagonal on every individual cell.
"""
import itertools
import sympy as sp
import networkx as nx
import bt3430_3441_cover_perkel_oracle_shell as core


def equitable_partition_falsifier():
    sizes = (12, 30, 15)
    compositions = [row for row in itertools.product(range(7), repeat=3) if sum(row) == 6]
    x = sp.symbols("x")
    alpha = (3 + sp.sqrt(5)) / 2
    beta = (3 - sp.sqrt(5)) / 2
    allowed = {
        sp.expand((x - 6) ** 3),
        sp.expand((x - 6) ** 2 * (x + 3)),
        sp.expand((x - 6) * (x + 3) ** 2),
        sp.expand((x - 6) * (x - alpha) * (x - beta)),
    }
    balanced = []
    spectral = []
    for rows in itertools.product(compositions, repeat=3):
        if not all(sizes[i] * rows[i][j] == sizes[j] * rows[j][i] for i in range(3) for j in range(3)):
            continue
        matrix = sp.Matrix(rows)
        polynomial = sp.expand(matrix.charpoly(x).as_expr())
        balanced.append([list(row) for row in rows])
        if polynomial in allowed:
            support = nx.Graph()
            support.add_nodes_from(range(3))
            for i in range(3):
                for j in range(i + 1, 3):
                    if rows[i][j] or rows[j][i]:
                        support.add_edge(i, j)
            spectral.append({
                "matrix": [list(row) for row in rows],
                "characteristic_polynomial": str(sp.factor(polynomial)),
                "connected_support": nx.is_connected(support),
            })
    assert len(balanced) == 10
    assert len(spectral) == 3
    assert all(not item["connected_support"] for item in spectral)
    return {
        "status": "PASS_NO_CONNECTED_PERKEL_EQUITABLE_12_30_15_PARTITION",
        "balanced_quotients": len(balanced),
        "spectrally_compatible_quotients": spectral,
        "conclusion": "Every spectrally compatible quotient is reducible; a connected Perkel graph cannot preserve the cap stabilizer partition equitably.",
    }


core.equitable_partition_falsifier = equitable_partition_falsifier
core.main()
