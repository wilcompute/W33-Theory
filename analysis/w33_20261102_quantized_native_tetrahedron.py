"""A supplied local transverse quantization of a native oriented quartet.

Uses the actual completion table from w33_20261102_chiral_surface_development.py.
The positive-face projector and K4 driver are declared quantum-model choices.
Perron-Frobenius uniqueness is standard, not a derived cosmological vacuum.
"""
import collections
import itertools
import json
import pathlib
import sys

import numpy as np
import sympy as s
from scipy.linalg import eigh

ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261102_chiral_surface_development import torus


FACES=[(1,2,3),(0,3,2),(0,1,3),(0,2,1)]


def model():
    native=json.loads((ROOT/'data/w33_20261102_chiral_surface_development.json').read_text())
    colors=[0,12,16,20];C=native['completion_table']
    states=list(itertools.product(range(4),repeat=4));idx={v:i for i,v in enumerate(states)}
    energy=np.array([sum(C[colors[v[a]]][colors[v[b]]]!=colors[v[c]] for a,b,c in FACES) for v in states],dtype=int)
    hopping=np.zeros((256,256),dtype=int)
    for j,v in enumerate(states):
        for site in range(4):
            for color in range(4):
                if color!=v[site]:
                    w=list(v);w[site]=color;hopping[idx[tuple(w)],j]=1
    assert np.array_equal(hopping,hopping.T) and set(hopping.sum(axis=0))=={12}
    ground=np.flatnonzero(energy==0);excited=np.flatnonzero(energy>0)
    assert len(ground)==12
    assert not np.any(hopping[np.ix_(ground,ground)])
    return colors,states,energy,hopping,ground,excited


def build():
    colors,states,E,T,P,Q=model()
    inv=s.diag(*[s.Rational(1,int(E[j])) for j in Q])
    TPQ=s.Matrix(T[np.ix_(P,Q)]);TQQ=s.Matrix(T[np.ix_(Q,Q)])
    second=-TPQ*inv*TPQ.T
    third=-TPQ*inv*TQQ*inv*TPQ.T
    assert second==-4*s.eye(12)
    third_eigs={str(k):v for k,v in third.eigenvals().items()}
    rows=[]
    for h in [0.01,0.03,0.1,0.3,1.0]:
        H=np.diag(E)-h*T
        vals,vec=eigh(H,subset_by_index=[0,2],driver='evr')
        psi=vec[:,0]
        if psi.sum()<0:psi=-psi
        residual=float(np.linalg.norm(H@psi-vals[0]*psi))
        assert residual<1e-11 and np.min(psi)>0 and vals[1]>vals[0]
        row=dict(h=h,energy=float(vals[0]),gap=float(vals[1]-vals[0]),residual=residual,
                 weight_in_classical_ground_space=float(np.sum(psi[P]**2)))
        # Entanglement of one supplied ququart with the other three.
        rho=psi.reshape(4,64)@psi.reshape(4,64).T
        eigen=np.linalg.eigvalsh(rho);row['single_site_entropy_nats']=float(-sum(x*np.log(x) for x in eigen if x>1e-15))
        rows.append(row)
    # Every ordered A4 relabeling gives a valid torus ground coloring.
    native=json.loads((ROOT/'data/w33_20261102_chiral_surface_development.json').read_text())
    labels=dict(native['examples']['even_period_torus_4x4']['labels'])
    inverse={v:i for i,v in enumerate(colors)};coloring=[inverse[labels[v]] for v in range(16)]
    even=[]
    for p in itertools.permutations(range(4)):
        parity=sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2
        if not parity:even.append(tuple(p[c] for c in coloring))
    distance=collections.Counter(sum(a!=b for a,b in zip(x,y)) for x,y in itertools.combinations(even,2))
    assert distance=={12:48,16:18}
    assert all(native['completion_table'][colors[x[a]]][colors[x[b]]]==colors[x[c]] for x in even for a,b,c in torus(4,4))
    return dict(status='PASS_SUPPLIED_QUANTIZED_NATIVE_QUARTET',native_colors=colors,faces=FACES,
        classical_energy_histogram={str(k):v for k,v in collections.Counter(E.tolist()).items()},
        classical_ground_state_indices=P.tolist(),classical_ground_states=[states[j] for j in P],
        second_order_effective_matrix=[list(map(str,row)) for row in second.tolist()],
        third_order_effective_matrix=[list(map(str,row)) for row in third.tolist()],third_order_eigenvalues=third_eigs,
        numerical_low_energy=rows,torus_ground_coloring_Hamming_distances={str(k):v for k,v in distance.items()},
        torus_first_possible_offdiagonal_perturbation_order=12,
        uniqueness='For h>0 the full4^N configuration graph of single-site K4 changes is connected and all offdiagonal Hamiltonian entries are nonpositive. Perron-Frobenius gives a unique strictly positive finite-volume ground state for this supplied model. No thermodynamic gap is asserted.',
        tunneling_scope='Within a frozen quartet the12 oriented ground colorings differ on at least3N/4 sites on an evenly colored even torus. A single-site driver cannot connect them before that perturbative order. This does not prove stability against diagonal splitting across all810 native quartets or a topological degeneracy.',
        boundary='Exact256-dimensional quartet-sector quantization plus a locality/perturbative selection rule on16 sites. The full120-level native many-body Hamiltonian, its thermodynamic phase, a physical time scale and a continuum limit are not solved.')


if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261102_quantized_native_tetrahedron.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
    print(d['status'],d['third_order_eigenvalues'],d['numerical_low_energy'][:2],flush=True)
