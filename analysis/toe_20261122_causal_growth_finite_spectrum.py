#!/usr/bin/env python3
"""Growing W33-induced causal-order stochastic quantum spectra, n=4..7.

All n! configurations for each nested induced graph are included. The
Metropolis chain is reversible with exact order reversal, so the stationary
positive quantum ground state has no arrow. Gaps are numerical toy values,
not a Lorentzian continuum or a graviton pole.
"""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
import numpy as np
from scipy.sparse import coo_matrix,eye,diags
from scipy.sparse.linalg import eigsh
import toe_20261122_causal_orientation_no_go as G
import toe_20261122_next5_causal_dynamics as C
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_causal_growth_finite_spectrum.json'


def nested_graphs():
    pts,E=G.w33();E={tuple(sorted(q)) for q in E}
    C4s=G.quad_cycles(E)
    # deterministically select lexicographically first induced chordless C4
    vertices=list(min(tuple(sorted(x)) for x in C4s))
    assert len(vertices)==4
    result=[]
    for n in range(4,8):
        ix={x:i for i,x in enumerate(vertices)}
        edges={tuple(sorted((ix[i],ix[j]))) for i,j in E if i in ix and j in ix}
        result.append((list(vertices),edges))
        if n<7:
            candidates=[v for v in range(40) if v not in ix]
            # Extend along the most connected new vertex to avoid a disconnected tail.
            best=max(candidates,key=lambda v:(sum(tuple(sorted((v,u))) in E for u in vertices),-v))
            assert any(tuple(sorted((best,u))) in E for u in vertices)
            vertices.append(best)
    return result


def solve_order_graph(vertices,edges):
    n=len(vertices)
    orders=list(itertools.permutations(range(n)));idx={o:i for i,o in enumerate(orders)}
    assert len(orders)==math.factorial(n)
    energies=np.array([C.energy(C.causal_stats(o,edges)) for o in orders],dtype=float)
    w=np.exp(-energies+energies.min());w/=w.sum()
    diag=np.ones(len(orders),dtype=float)
    ii=[];jj=[];vv=[]
    flips=[]
    for i,o in enumerate(orders):
        jrev=idx[o[::-1]]
        if i<jrev:flips.append((i,jrev))
        assert abs(energies[i]-energies[jrev])<1e-12
        for a in range(n-1):
            q=list(o);q[a],q[a+1]=q[a+1],q[a];j=idx[tuple(q)]
            rate=min(1.,math.exp(energies[i]-energies[j]))/(n-1)
            diag[i]-=rate
            # Symmetric quantum-conjugated offdiagonal, H=I-S.
            sym=math.sqrt(w[i]/w[j])*rate
            ii.append(i);jj.append(j);vv.append(-sym)
    ii.extend(range(len(orders)));jj.extend(range(len(orders)))
    vv.extend(1-diag)
    H=coo_matrix((vv,(ii,jj)),shape=(len(orders),len(orders))).tocsr()
    assert max(abs(H-H.T).data,default=0.)<1e-12
    gs=np.sqrt(w)
    assert np.linalg.norm(H@gs)<2e-12
    eigen=np.linalg.eigvalsh(H.toarray())[:3] if n<=5 else eigsh(H,k=3,which='SA',tol=1e-10)[0]
    eigen=sorted(float(x) for x in eigen)
    assert abs(eigen[0])<1e-11 and eigen[1]>0
    reversal_odd=np.array([1 if o.index(0)<o.index(n-1) else -1 for o in orders])
    mean=float(np.dot(w,reversal_odd))
    assert abs(mean)<1e-12
    # Gap theorem is finite irreducible reversible Markov chain. No
    # spectral continuum is inferred from four finite sizes.
    return dict(n_vertices=n,original_W33_vertices=vertices,
        induced_undirected_edges=sorted([list(x) for x in edges]),
        number_of_total_order_states=len(orders),
        number_of_adjacent_swap_directed_transitions=len(orders)*(n-1),
        distinct_action_energy_values=len({round(x,12) for x in energies}),
        first_three_quantum_H_eigenvalues=eigen,
        first_excitation_gap=eigen[1],
        exact_order_reversal_invariance_of_action=True,
        reversal_odd_ground_state_expectation=mean,
        ground_state_residual_norm=float(np.linalg.norm(H@gs)),
        full_sparse_quantum_H_nonzero_count=int(H.nnz))


def verify():
    rows=[solve_order_graph(v,e) for v,e in nested_graphs()]
    assert [x['number_of_total_order_states'] for x in rows]==[24,120,720,5040]
    assert all(x['first_excitation_gap']>0 for x in rows)
    return dict(status='PASS_W33_NESTED_FINITE_CAUSAL_SPECTRAL_SCALING_AND_NO_ARROW',
        date='2026-11-22',nested_W33_induced_graphs=rows,
        exact_theorem='For any finite connected adjacent-order Metropolis chain with reversal-invariant interval action, the symmetrized Hamiltonian has a unique strictly positive reversal-even ground state; stationary reversal-odd observables vanish.',
        numerical_boundaries='Numerical gaps are only for n=4..7 and chosen interval-action coefficients; no finite-n graviton, no Lorentzian light cone, no continuum scaling proof, no physical energy units.',
        external_prior='Reversible Markov symmetrization and causal-set interval actions are established methods, not novel physics.')

def main():
    d=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
    print(d['status'],[(x['n_vertices'],x['number_of_total_order_states'],x['first_excitation_gap']) for x in d['nested_W33_induced_graphs']])
if __name__=='__main__':main()
