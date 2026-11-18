"""An explicit 3-periodic LOCAL W33 Levi cover with a homogenized 3-torus band.

Unlike the dense point-graph limit, this construction retains degree four.
The three voltage choices are noncanonical; no derived gravity is claimed.
"""
import itertools
import json
import math
from fractions import Fraction
from pathlib import Path
import networkx as nx
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
MOD = 3


def projective(x):
    first = next(v for v in x if v % MOD)
    inverse = pow(first, -1, MOD)
    return tuple(v * inverse % MOD for v in x)


def symplectic(u, v):
    return (u[0]*v[1]-u[1]*v[0]+u[2]*v[3]-u[3]*v[2]) % MOD


def levi():
    points = sorted({projective(x) for x in itertools.product(range(3), repeat=4)
                     if any(x)})
    assert len(points) == 40
    index = {v:i for i,v in enumerate(points)}
    lines = set()
    for u,v in itertools.combinations(points, 2):
        if symplectic(u, v) != 0:
            continue
        L = tuple(sorted(
            [index[projective(tuple((u[j]+t*v[j]) % 3 for j in range(4)))]
             for t in (0,1,2)] + [index[v]]))
        assert len(set(L)) == 4
        lines.add(L)
    lines = sorted(lines)
    assert len(lines) == 40
    G = nx.Graph()
    G.add_nodes_from(range(80))
    G.add_edges_from((i,40+j) for j,line in enumerate(lines) for i in line)
    assert G.number_of_edges() == 160 and nx.is_connected(G)
    assert set(dict(G.degree()).values()) == {4}
    return G, points, lines


def choose_voltages(G):
    tree = nx.bfs_tree(G, source=0).to_undirected()
    edges = sorted(tuple(sorted(e)) for e in G.edges())
    tedges = {tuple(sorted(e)) for e in tree.edges()}
    chords = sorted(set(edges)-tedges)
    assert len(chords) == 81
    chosen = [chords[i] for i in (0,27,54)]
    assert chosen == [(1,45),(16,45),(28,46)]
    voltages = {e:(0,0,0) for e in edges}
    for i,e in enumerate(chosen):
        voltages[e]=tuple(int(i==j) for j in range(3))
    return edges, chosen, voltages


def diffusion(G, edges, voltages):
    E=len(edges); V=80
    incidence = np.zeros((V,E))
    W=np.zeros((E,3))
    for i,(a,b) in enumerate(edges):
        incidence[a,i]=1
        incidence[b,i]=-1
        W[i,:]=voltages[(a,b)]
    Lap=incidence@incidence.T
    assert np.linalg.matrix_rank(Lap)==79
    # Exact integral polynomial for the Moore-Penrose inverse on 1-perp.
    # The connected Levi Laplacian has eigenvalues 0, 8, 4, 4+sqrt(6),
    # 4-sqrt(6). For any nonzero eigenvalue t, the integer polynomial
    # H(t)=-t^3+20*t^2-138*t+376 satisfies t*H(t)=320.
    Li=Lap.astype(np.int64)
    H=-Li@Li@Li+20*(Li@Li)-138*Li+376*np.eye(V,dtype=np.int64)
    assert np.array_equal(Li@H,320*np.eye(V,dtype=np.int64)-4*np.ones((V,V),dtype=np.int64))
    edgevec=incidence.astype(np.int64)
    wi=W.astype(np.int64)
    exact_K320=320*(wi.T@wi)-wi.T@edgevec.T@H@edgevec@wi
    exact_numer=np.array([[81,-27,9],[-27,81,-3],[9,-3,81]],dtype=np.int64)
    assert np.array_equal(exact_K320,2*exact_numer)
    lp=np.linalg.pinv(Lap,hermitian=True)
    K=W.T@(np.eye(E)-incidence.T@lp@incidence)@W
    expected=exact_numer/160
    assert np.max(np.abs(K-expected)) < 1e-11
    assert np.linalg.eigvalsh(K).min() > 0.3
    # Foster's first theorem: sum_e R_eff(e)=V-1, and flag transitivity
    # implies each edge's resistance equals (V-1)/E=79/160.
    r_eff=np.diag(incidence.T@lp@incidence)
    assert max(abs(r_eff-79/160)) < 1e-11
    assert max(abs(np.diag(K)-81/160)) < 1e-11
    return K, r_eff


def bloch_lowest(edges, voltages, theta):
    A=np.zeros((80,80), dtype=complex)
    for a,b in edges:
        w=voltages[(a,b)]
        phase=np.exp(1j*sum(t*wt for t,wt in zip(theta,w)))
        A[a,b]=phase; A[b,a]=phase.conjugate()
    eig=np.linalg.eigvalsh(4*np.eye(80)-A)
    return float(eig[0])


def cyclic_cover(G, edges, voltages, n):
    H=nx.Graph()
    for layer in itertools.product(range(n),repeat=3):
        for v in range(80):
            H.add_node((v,layer))
    for layer in itertools.product(range(n),repeat=3):
        for a,b in edges:
            w=voltages[(a,b)]
            shifted=tuple((layer[i]+w[i])%n for i in range(3))
            H.add_edge((a,layer),(b,shifted))
    assert H.number_of_nodes() == 80*n**3
    assert H.number_of_edges() == 160*n**3
    assert set(dict(H.degree()).values()) == {4}
    assert nx.is_connected(H)
    assert H.number_of_edges()-H.number_of_nodes()+1 == 80*n**3+1
    return dict(n=n, vertices=H.number_of_nodes(),
                edges=H.number_of_edges(), degree=4,
                cycle_rank=H.number_of_edges()-H.number_of_nodes()+1,
                connected=True)


def run():
    G,points,lines=levi()
    edges,chosen,voltage=choose_voltages(G)
    K,r=diffusion(G,edges,voltage)
    eps_diagnostics=[]
    axis=np.array([1.,-.5,.6])
    for eps in (.25,.125,.0625):
        theta=eps*axis
        lam=bloch_lowest(edges,voltage,theta)
        approx=float(theta@K@theta/80)
        relative=abs(lam/approx-1)
        eps_diagnostics.append(dict(epsilon=eps, lowest_eigenvalue=lam,
                                    homogenized_quadratic=approx,
                                    relative_error=relative))
    assert eps_diagnostics[2]["relative_error"] < 0.0005
    assert eps_diagnostics[2]["relative_error"] < eps_diagnostics[1]["relative_error"] < eps_diagnostics[0]["relative_error"]
    covers=[cyclic_cover(G,edges,voltage,n) for n in (2,3)]
    # Sufficient to verify positive definite and the analytic quadratic law:
    # the base graph's zero Laplacian eigenvalue is simple; all higher Bloch
    # bands remain uniformly separated at theta=0 by a finite gap.
    base_eig=np.linalg.eigvalsh(4*np.eye(80)-nx.to_numpy_array(G,nodelist=range(80)))
    assert abs(base_eig[0]) < 1e-12
    assert abs(base_eig[1]-(4-math.sqrt(6))) < 1e-10
    data=dict(status="PASS",base=dict(vertices=80,edges=160,degree=4,cycle_rank=81,
                                     point_count=40,line_count=40,
                                     base_laplacian_first_gap=float(base_eig[1])),
              selected_tree_chords=[list(x) for x in chosen],
              voltage_axes=3,deck_group="(Z/nZ)^3",
              conductance_matrix_K_over_160_numerators=[[81,-27,9],[-27,81,-3],[9,-3,81]],
              conductance_matrix_denominator=160,
              diffusion_D_over_12800_numerators=[[81,-27,9],[-27,81,-3],[9,-3,81]],
              diffusion_matrix_denominator=12800,
              eigenvalues_K=list(map(float,np.linalg.eigvalsh(K))),
              effective_edge_resistance="79/160",
              one_edge_cycle_conductance="81/160",
              n_covers=covers, bloch_diagnostics=eps_diagnostics,
              theorem="For each fixed m in Z^3, n^2 times the lowest Bloch eigenvalue at theta=2*pi*m/n converges to (2*pi)^2*m^T D m. Positive D yields the spectral law of an elliptic operator on T^3.",
              noncanonical="BFS tree and three selected chords fix an arbitrary voltage basis; different choices produce different tensors.",
              limits="Low-energy scalar graph continuum only; no local 3D manifold cell structure, Einstein dynamics, Lorentzian metric, quantum field theory, or continuum Planck scale.")
    out=ROOT/"data/toe_20261118_W33_triperiodic_Levi_homogenization.json"
    out.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    print("PASS W33 3D periodic covers; K/160=[[81,-27,9],[-27,81,-3],[9,-3,81]]; covers",covers)
    return data

if __name__=="__main__":
    run()
