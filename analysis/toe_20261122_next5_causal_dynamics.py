#!/usr/bin/env python3
"""Well-defined finite W33 causal-order Metropolis toy model and null controls.

State space = total orders of 40 W33 vertices, inducing acyclic orientations
of all 240 edges. Energy built from transitive-closure interval abundances.
Metropolis uses symmetric adjacent swaps. This is NOT Einstein gravity.
"""
from __future__ import annotations
import itertools,json,math
from pathlib import Path
import numpy as np
from sympy.combinatorics import Permutation,PermutationGroup
import toe_20261122_causal_orientation_no_go as C
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_next5_causal_dynamics.json'
THETA=(.06,-.09,.045)


def symplectic(x,y):
    return (x[0]*y[1]-x[1]*y[0]+x[2]*y[3]-x[3]*y[2])%3


def automorphism(pts,edges,v=None):
    if v is None:v=pts[1]
    ix={x:i for i,x in enumerate(pts)}
    def norm(t):
        i=next(k for k,x in enumerate(t) if x%3)
        inv=pow(t[i],-1,3)
        return tuple((z*inv)%3 for z in t)
    pi=tuple(ix[norm(tuple((x[k]+symplectic(x,v)*v[k])%3 for k in range(4)))] for x in pts)
    assert len(set(pi))==40
    assert {tuple(sorted((pi[i],pi[j]))) for i,j in edges}==edges
    assert any(pi[i]!=i for i in range(40))
    return pi


def causal_stats(order,edges):
    n=len(order);rank={v:i for i,v in enumerate(order)}
    future=[0]*n
    for a,b in edges:
        if rank[a]<rank[b]:future[a]|=1<<b
        else:future[b]|=1<<a
    # Transitive closure is simple reverse-topological dynamic programming.
    reach=[0]*n
    for a in reversed(order):
        mask=future[a]
        while mask:
            low=mask&-mask;mask-=low
            b=low.bit_length()-1
            reach[a]|=1<<b
            reach[a]|=reach[b]
    past=[0]*n
    for a in range(n):
        mask=reach[a]
        while mask:
            bit=mask&-mask;mask-=bit
            past[bit.bit_length()-1]|=1<<a
    counts=[0,0,0];far=0
    longest=[1]*n
    for a in order:
        mask=reach[a]
        while mask:
            bit=mask&-mask;mask-=bit
            b=bit.bit_length()-1
            interior=(reach[a]&past[b]).bit_count()
            if interior<=2:counts[interior]+=1
            far+=interior>2
            longest[b]=max(longest[b],longest[a]+1)
    compared=sum(k.bit_count() for k in reach)
    assert sum(counts)+far==compared
    return dict(N0=counts[0],N1=counts[1],N2=counts[2],Ngt2=far,
                comparable_pairs=compared,chain_height=max(longest),
                order_fraction=compared/(n*(n-1)/2))


def energy(d,theta=THETA):
    return theta[0]*d['N0']+theta[1]*d['N1']+theta[2]*d['N2']


def sim(pts,edges,steps=1800,seed=20261122):
    rng=np.random.default_rng(seed)
    order=[int(v) for v in rng.permutation(len(pts))]
    initial=causal_stats(order,edges);s=energy(initial)
    accepts=0;observables=[]
    for it in range(steps):
        i=int(rng.integers(len(order)-1))
        order[i],order[i+1]=order[i+1],order[i]
        next_d=causal_stats(order,edges);ns=energy(next_d)
        if ns<=s or rng.random()<math.exp(s-ns):
            accepts+=1;s=ns;current=next_d
        else:
            order[i],order[i+1]=order[i+1],order[i]
        if it>=steps//2 and it%10==0:
            observables.append([s,*(current[k] for k in ('N0','N1','N2','comparable_pairs','chain_height'))])
    return dict(seed=seed,steps=steps,accepted=accepts,acceptance_rate=accepts/steps,
                initial=initial,final=causal_stats(order,edges),
                final_energy=s,mean_burnin_removed_statistics=np.mean(observables,axis=0).tolist(),
                final_order=order)


def four_cycle_exact():
    E={(0,1),(0,2),(1,3),(2,3)}
    all_s=[(o,causal_stats(o,E)) for o in itertools.permutations(range(4))]
    weights=np.array([math.exp(-energy(d)) for _,d in all_s]);weights/=weights.sum()
    expected={k:float(sum(weights[i]*d[k] for i,(_,d) in enumerate(all_s)))
              for k in ('N0','N1','N2','comparable_pairs','chain_height')}
    same_hist=sorted(set((d['N0'],d['N1'],d['N2']) for _,d in all_s))
    assert len(all_s)==24 and len(same_hist)>1
    # Connected adjacent-transposition proposal graph; detailed balance exact.
    for i,(o,d) in enumerate(all_s):
        for k in range(3):
            v=list(o);v[k],v[k+1]=v[k+1],v[k];j=next(j for j,(p,_) in enumerate(all_s) if tuple(v)==p)
            p_ij=min(1,math.exp(energy(d)-energy(all_s[j][1])))/3
            p_ji=min(1,math.exp(energy(all_s[j][1])-energy(d)))/3
            assert abs(weights[i]*p_ij-weights[j]*p_ji)<1e-12
    return dict(total_orders=24,distinct_interval_abundance_vectors=len(same_hist),
                finite_boltzmann_mean=expected,exact_detailed_balance_verified=True)


def verify():
    pts,edges=C.w33();pi=automorphism(pts,edges)
    order=tuple(range(40)); stats=causal_stats(order,edges)
    transvections=[automorphism(pts,edges,v) for v in pts]
    pg=PermutationGroup([Permutation(p) for p in transvections])
    assert pg.order()==25920
    assert all(causal_stats(tuple(p[i] for i in order),edges)==stats for p in transvections)
    mapped=tuple(pi[i] for i in order)
    assert causal_stats(mapped,edges)==stats
    # Compare with a different acyclic order, with no redefinition of W33.
    reversed_order=tuple(reversed(order))
    assert causal_stats(reversed_order,edges)['comparable_pairs']==stats['comparable_pairs']
    # But order reversal exchanges future/past; the interval action is symmetric.
    # Nontrivial random order need not have same interval histogram.
    alt=tuple(int(v) for v in np.random.default_rng(712).permutation(40))
    alternative=causal_stats(alt,edges)
    assert (stats['N0'],stats['N1'],stats['N2'])!=(alternative['N0'],alternative['N1'],alternative['N2'])
    chain=sim(pts,edges);small=four_cycle_exact()
    assert 0<chain['acceptance_rate']<1
    return dict(status='PASS_FINITE_W33_CAUSAL_INTERVAL_METROPOLIS',date='2026-11-22',
       vertices=40,edges=240,action='S=0.06*N0-0.09*N1+0.045*N2 (in arbitrary dimensionless units)',
       state_space='40! total vertex orders; each induces a directed acyclic W33 orientation',
       transition='Uniform random adjacent transposition in total order, accepted with min(1, exp(-Delta S))',
       canonical_initial_order=stats,seeded_alternative_order=alternative,
       symplectic_automorphism=pi,automorphism_relabel_invariant=True,
       all_40_projective_symplectic_transvections_checked=True,
       symplectic_transvection_generated_projective_group_order=int(pg.order()),
       small_cycle_exact_partition_control=small,
       metropolized_chain=chain,
       main_result='Causal interval observables and a reversible finite-state action can be defined explicitly, but no action coefficients are derived from W33 or from Einstein gravity.',
       physical_boundary='This is an illustrative classical finite graph-order model with a prescribed action and no continuum metric, spin-2 pole, Lorentz invariance, quantum amplitudes or derived cosmological predictions.')


def main():
    d=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
    print('PASS causal toy detailed balance and symplectic relabeling',d['metropolized_chain']['acceptance_rate'])

if __name__=='__main__':main()
