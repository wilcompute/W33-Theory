"""Exact larger-torus tunneling, a cut integral bound, and a distance-one audit.

The all9720 ground palettes and4x4 coefficient are owned by the prior Nov3
all-quartet producer. Kagome itself is established geometry, not a new object.
"""
import collections,itertools,json,math,pathlib,sys
from fractions import Fraction
import networkx as nx
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261102_chiral_surface_development import torus

def active_graph(m,n):
    faces=torus(m,n)
    # Use the producer's actual face list and vertex labeling.
    active=[x*n+y for x in range(m)for y in range(n)if (x%2,y%2)!=(0,0)]
    G=nx.Graph();G.add_nodes_from(active)
    for f in faces:
        G.add_edges_from((a,b)for a,b in itertools.combinations(f,2)if a in G and b in G)
    return G,faces

def coefficient(G,weight=Fraction(3,2)):
    nodes=list(G);idx={v:i for i,v in enumerate(nodes)};n=len(nodes);masks=[sum(1<<idx[u]for u in G[v])for v in nodes]
    size=1<<n;cut=np.zeros(size,dtype=np.int16)
    for S in range(1,size):
        bit=S&-S;v=bit.bit_length()-1;T=S^bit;cut[S]=int(cut[T])+len(G[nodes[v]])-2*(T&masks[v]).bit_count()
    assert not cut[-1] and np.all(cut[1:-1]>0)
    energies=[Fraction(int(k))*weight for k in sorted(set(cut[1:-1]))]
    # Multiply by a shared integer L so each stage is an exact integer recurrence.
    L=math.lcm(*(q.numerator for q in energies));den={int(k):int(Fraction(L)/(int(k)*weight))for k in set(cut[1:-1])}
    A=[0]*size;A[0]=1
    for S in range(1,size):
        T=S;total=0
        while T:
            bit=T&-T;total+=A[S^bit];T^=bit
        A[S]=total if S==size-1 else total*den[int(cut[S])]
    return Fraction(A[-1],L**(n-1)),cut

def build():
    old=json.loads((ROOT/'data/w33_20261103_all_quartet_tunneling.json').read_text())
    C=np.array(json.loads((ROOT/'data/w33_20261102_chiral_surface_development.json').read_text())['completion_table'])
    palettes=np.array(old['ground_palettes']);rows=[]
    for m,n in [(4,4),(4,6)]:
        G,faces=active_graph(m,n);N=m*n;k=len(G)
        assert k==3*N//4 and set(dict(G.degree()).values())=={4} and nx.is_connected(G)
        triangles=sum(nx.triangles(G).values())//3;assert triangles==N//2
        # Replay every native ground coloring on every face of the larger torus.
        slots=np.array([2*(x%2)+(y%2)for x in range(m)for y in range(n)])
        for a,b,c in faces:assert np.all(C[palettes[:,slots[a]],palettes[:,slots[b]]]==palettes[:,slots[c]])
        coeff,cut=coefficient(G)
        if (m,n)==(4,4):
            assert coeff==Fraction(19657590887,45916502400000)
            assert nx.is_isomorphic(G,nx.line_graph(nx.cubical_graph()))
        # Independently compute face excitation counts on every binary hybrid.
        nodes=list(G);pos={v:i for i,v in enumerate(nodes)}
        fm=[sum(1<<pos[v]for v in f if v in pos)for f in faces]
        assert all(mask.bit_count()in[2,3]for mask in fm)
        # All4x4 subsets and a deterministic spread of4x6 subsets.
        subset=range(1<<k)if k==12 else sorted({0,(1<<k)-1,*range(0,1<<k,97)})
        for S in subset:
            E=sum((S&mask)!=0 and (S&mask)!=mask for mask in fm)
            assert 2*E==3*int(cut[S])
        upper=Fraction(4,3)**(k-1);assert coeff<=upper
        rows.append(dict(torus=[m,n],sites=N,active_sites=k,active_edges=G.number_of_edges(),active_triangles=triangles,
            exact_leading_coefficient=str(coeff),decimal_coefficient=float(coeff),leading_tunneling_order=k,
            leading_gap_coefficient=str(216*coeff),spanning_tree_coefficient_upper_bound=str(upper),
            native_ground_palettes_replayed=len(palettes),faces_checked_per_palette=len(faces),hybrid_energy_identity_checks=len(subset),
            positive_cut_sizes=sorted(map(int,set(cut[1:-1])))))
        print('EXACT_KAGOME',m,n,k,str(coeff),flush=True)
    # Independent exact tests of the integral equality on all unlabeled trees up to7 vertices.
    tree_checks=0
    for n in range(2,8):
        trees=[nx.path_graph(2)]if n==2 else nx.nonisomorphic_trees(n)
        for T in trees:
            c,_=coefficient(T);assert c==Fraction(4,3)**(n-1);tree_checks+=1
    a,b=palettes[0],next(row for row in palettes if row[0]!=palettes[0,0])
    assert a[0]!=b[0]
    return dict(status='PASS_KAGOME_LEADING_TUNNELING_BOUND_AND_DISTANCE_ONE',tori=rows,
        active_graph='Remove the unchanged parity sublattice from the triangular torus: periodic kagome,4-regular. The4x4 instance is the cuboctahedral graph L(Q3).',
        energy_identity='For a binary hybrid subset S, E(S)=(3/2)*|delta_G S|. Each active edge meets one face with two active vertices and one with three; the latter contributes half its cut-edge count.',
        projected_spin_model='H_hybrid=(3/4) sum_edges(1-Z_i Z_j)-h sum_i X_i. This is a projected binary sector; the full120-state driver does not leave it invariant.',
        integral_identity='c_G=sum_orders product_(k=1)^(n-1)1/E(S_k)=integral_(t_root=0) exp[-sum_edges w_uv*abs(t_u-t_v)] product_(v!=root)dt_v.',
        integral_proof='Partition relative event times by their total order, and change coordinates to the positive consecutive spacings. The exponent is sum_k E(S_k)*spacing_k and the Jacobian is1. Each sector integrates to the path-denominator product.',
        tree_bound_proof='Dropping cycle edges increases the integrand. On a spanning tree the rooted edge-difference map has determinant+-1; every edge integral is2/w. Thus c_G<=product_tree(2/w)=(4/3)^(n-1).',
        exact_tree_checks=tree_checks,leading_amplitude_bound='c_N*h^(3N/4) <= h*(4h/3)^(3N/4-1), even periodic m,n>=4, h>=0',
        leading_gap_bound='216*c_N*h^(3N/4) <=216*h*(4h/3)^(3N/4-1)',
        thermodynamic_boundary='Uniform exponential bound on the leading perturbative term only. No volume-uniform convergence/remainder estimate or full fixed-h thermodynamic spectral gap is proved.',
        ground_code_quantum_distance=1,
        local_indistinguishability_counterexample='For two ground product states a,b differing at sitev, O=|a_v><a_v| has diagonal expectations1 and0. Hence P O P is not scalar and the quantum Knill-Laflamme condition fails already at weight1.',
        symmetry_breaking_field='At h=0, -epsilon sum_v |a_v><a_v| selects ground palette a within the9720-dimensional ground manifold. Other palettes differ at3N/4 or N sites, giving a projected splitting at least3epsilon*N/4. This is explicit symmetry breaking, not proof of spontaneous order.',
        ownership='Prior all-quartet tunneling owns9720 palettes, effective degree320, gap adjacency difference216 and4x4 coefficient. BT1331 discusses a different proposed kagome/W33 embedding; no unverified folding or CSS-code claim from that note is used.',
        boundary='Finite declared Hamiltonian and a leading-order theorem. Extensive classical Hamming separation does not imply topological quantum protection or a completed TOE.')

if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261103_kagome_tunneling_bounds.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print(d['status'],flush=True)
