import json
import numpy as np
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

FANO_LINES = [
    (0, 1, 3),
    (1, 2, 4),
    (2, 3, 5),
    (3, 4, 6),
    (4, 5, 0),
    (5, 6, 1),
    (6, 0, 2),
]


def build_heawood_graph():
    G = nx.Graph()
    points = list(range(7)); lines = list(range(7,14))
    G.add_nodes_from(points, bipartite=0); G.add_nodes_from(lines, bipartite=1)
    for li,line in enumerate(FANO_LINES,start=7):
        for p in line: G.add_edge(p,li)
    return G


def laplacian(G):
    A = nx.to_numpy_array(G, dtype=float)
    return np.diag(np.sum(A, axis=1)) - A


def main():
    # load spiral closedform json
    with open('heawood_spiral_closedform.json','r',encoding='utf-8') as f:
        spiral = json.load(f)
    mid_vals = np.array(spiral.get('mid_vals', []))
    phases = np.array(spiral.get('permutation_7cycle_phases', []))

    # eigenvalue histogram
    plt.figure(figsize=(6,3))
    plt.hist(mid_vals, bins=12, color='#58a6ff', edgecolor='k')
    plt.title('Heawood Mid-shell Eigenvalues')
    plt.xlabel('Eigenvalue')
    plt.tight_layout()
    plt.savefig('eigen_hist.png', dpi=150)
    plt.close()

    # phase rose plot (polar)
    if phases.size:
        plt.figure(figsize=(5,5))
        ax = plt.subplot(111, projection='polar')
        angles = phases
        # wrap angles into [0,2pi)
        angles = np.mod(angles, 2*np.pi)
        bins = 12
        counts, bin_edges = np.histogram(angles, bins=bins, range=(0,2*np.pi))
        widths = np.diff(bin_edges)
        ax.bar(bin_edges[:-1], counts, width=widths, bottom=0.0, color='#d2a8ff', edgecolor='k')
        ax.set_title('7-cycle Phase Distribution')
        plt.tight_layout()
        plt.savefig('phase_rose.png', dpi=150)
        plt.close()

    # projector eigenmodes: recompute P_mid_sub
    G = build_heawood_graph()
    L = laplacian(G)
    eigvals, eigvecs = np.linalg.eigh(L)
    mask = ~(np.isclose(eigvals, 0.0, atol=1e-9) | np.isclose(eigvals, 6.0, atol=1e-9))
    mid_vals = eigvals[mask]
    mid_vecs = eigvecs[:, mask]

    # mid sub operator H_mid_sub diagonal in mid basis
    H_mid_sub = np.diag(mid_vals / np.sqrt(2.0))
    P_mid_sub = 0.5 * (np.eye(H_mid_sub.shape[0]) + H_mid_sub)
    p_eigs = np.linalg.eigvalsh(P_mid_sub)

    plt.figure(figsize=(6,3))
    plt.plot(sorted(p_eigs), 'o-', color='#3fb950')
    plt.title('Eigenvalues of $P_{mid}^{sub}$')
    plt.ylabel('Eigenvalue')
    plt.xlabel('Index')
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('projector_eigs.png', dpi=150)
    plt.close()

    print('Saved eigen_hist.png, phase_rose.png, projector_eigs.png')

if __name__=='__main__':
    main()
