"""Native interacting patch is a subdivided theta graph; exact gauge match.

11974 owns coupled patch quantization. Here pure-gauge equivalence and
heavy intermediate-matter decimation distinguish universal topology from
added light degrees. No W33-specific physical coupling claimed.
"""
from pathlib import Path
from itertools import combinations,product
import json
import sys
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import eigsh
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass11974_coupled_patch_matter import Patch


def matrix(c,L,penalty,kappa=.7,g=.8,beta=.4,mass=.3):
    occs=[sum(1<<i for i in q) for q in combinations(range(c.n),c.fermions)]
    states=[(bits,l) for bits in occs for l in product(range(-L,L+1),repeat=2)]
    ids={x:i for i,x in enumerate(states)};rr=[];cc=[];vv=[]
    deg=np.bincount(np.array(c.edges).ravel(),minlength=c.n);internal=deg==2
    for idx,(bits,l) in enumerate(states):
        occ=np.array([(bits>>j)&1 for j in range(c.n)]);n=c.flux(bits,l,np.zeros(c.n,int))
        diag=g*g*(n@n)/2+mass*((1-2*c.background)@occ)+len(c.P)*beta/g**2+penalty*sum(abs(occ-c.background)[internal])
        rr.append(idx);cc.append(idx);vv.append(diag)
        for e,(a,b) in enumerate(c.edges):
            oa,ob=(bits>>a)&1,(bits>>b)&1
            if oa==ob:continue
            direction=1 if oa else -1;new=list(l)
            if e in c.chords:new[c.chords.index(e)]-=direction
            target=(bits^(1<<a)^(1<<b),tuple(new))
            if target in ids:
                sign=(-1)**sum((bits>>j)&1 for j in range(min(a,b)+1,max(a,b)))
                rr.append(idx);cc.append(ids[target]);vv.append(-kappa*sign)
        for p in c.P:
            for sign in (1,-1):
                target=(bits,tuple(np.array(l)+sign*p[c.chords]))
                if target in ids:rr.append(idx);cc.append(ids[target]);vv.append(-beta/(2*g*g))
    H=coo_matrix((vv,(rr,cc)),shape=(len(states),)*2).tocsr()
    return H,states,internal


def payload():
    c=Patch();deg=np.bincount(np.array(c.edges).ravel(),minlength=c.n)
    branch=list(np.flatnonzero(deg==3));assert len(branch)==2 and sum(deg==2)==9
    adj=[[] for _ in range(c.n)]
    for a,b in c.edges:adj[a].append(b);adj[b].append(a)
    paths=[]
    for first in adj[branch[0]]:
        path=[branch[0],first]
        while path[-1]!=branch[1]:path.append(next(v for v in adj[path[-1]] if v!=path[-2]))
        paths.append(path)
    assert sorted(len(p)-1 for p in paths)==[4,4,4]
    bits=sum(1<<i for i in range(c.n) if c.background[i]);ext=np.zeros(c.n,int)
    cycle=np.array([c.flux(bits,l,ext) for l in ((1,0),(0,1))]);Gram=cycle@cycle.T
    assert np.array_equal(np.diag(Gram),[8,8]) and abs(Gram[0,1])==4
    small=np.array([[-1,1,0],[-1,0,1]])
    small[1]*=int(Gram[0,1]/4)
    assert np.array_equal(Gram,4*small@small.T)
    L=2;ls=list(product(range(-L,L+1),repeat=2));pos={l:i for i,l in enumerate(ls)}
    pure=np.zeros((len(ls),)*2);other=np.zeros_like(pure);g=.8;beta=.4
    for i,l in enumerate(ls):
        n=np.array(l)@cycle;ns=np.array(l)@small
        pure[i,i]=g*g*(n@n)/2+len(c.P)*beta/g**2
        other[i,i]=(2*g)**2*(ns@ns)/2+len(c.P)*(4*beta)/(2*g)**2
        for p in c.P:
            for sign in (1,-1):
                target=tuple(np.array(l)+sign*p[c.chords])
                if target in pos:pure[i,pos[target]]-=beta/(2*g*g);other[i,pos[target]]-=(4*beta)/(2*(2*g)**2)
    assert np.max(abs(pure-other))<1e-12
    ev,U=np.linalg.eigh(pure);prob=U[:,0]**2
    # Exact leading1/M coefficient for this hard-cutoff space. One hop
    # makes1 defect on a branch edge and2 on an internal/internal edge.
    internal=deg==2;coefficient=0.
    for l,pr in zip(ls,prob):
        for e,(a,b) in enumerate(c.edges):
            direction=1 if c.background[a] else -1;new=list(l)
            if e in c.chords:new[c.chords.index(e)]-=direction
            if tuple(new) in pos:coefficient+=pr*.7**2/(int(internal[a])+int(internal[b]))
    rows=[];base=float(ev[0]-.3*c.fermions)
    for M in (20.,40.,80.):
        H,states,_=matrix(c,L,M)
        e,u=eigsh(H,k=1,which='SA',tol=1e-10,v0=np.ones(len(states))/np.sqrt(len(states)))
        defects=np.array([sum(abs(np.array([(bits>>j)&1 for j in range(c.n)])-c.background)[internal]) for bits,l in states])
        rows.append(dict(penalty=M,E0=float(e[0]),energy_shift=float(e[0]-base),scaled_shift=float(M*(e[0]-base)),
                         predicted_scaled_shift=-coefficient,error=abs(float(M*(e[0]-base))+coefficient),
                         mean_internal_defects=float(np.dot(abs(u[:,0])**2,defects)),residual=float(np.linalg.norm(H@u[:,0]-e[0]*u[:,0]))))
        print('decimation',rows[-1],flush=True)
    assert rows[-1]['error']<rows[0]['error']
    return dict(status='PASS',branch_native_vertices=[c.native_vertices[v] for v in branch],path_lengths=[4,4,4],
        native_cycle_Gram=Gram.tolist(),collapsed_theta_cycle_Gram=(small@small.T).tolist(),
        exact_pure_gauge_equivalence='Native patch is a theta graph with each of3 edges subdivided4times. Neutral Gauss flux is constant on each path. Native cycle Gram is4times the3-edge theta Gram; g_small=2g_native and beta_small=4beta_native make the ENTIRE pure compact rotor Hamiltonian identical, including all contained plaquette shifts at every cutoff.',
        matter_difference='Native11sites have9 additional intermediate fermions. The two branch sites have the SAME original bipartite color. Freezing intermediate occupations in the native neutral half-filled sector fills both branches (or neither if colors reversed); it is NOT equivalent to a half-filled two-site spinless hopping model.',
        added_penalty='M sum_internal |occ-background|, with fixed original particle number; every gauge-invariant hop retained. This is an added decimation parameter, not a derived fermion mass.',
        flux_cutoff=L,dimension=25*462,pure_ground_with_frozen_matter=base,
        leading_virtual_hop_coefficient=coefficient,infinite_flux_leading_coefficient='9*kappa²=4.41:6branch/internal hops costM,6internal/internal hops cost2M. Finite-cutoff coefficient additionally excludes blocked chord hops.',
        heavy_matter_checks=rows,
        scope='Exact pure-gauge subdivision equivalence and numerical interacting heavy-matter approach on the specified finite patch. Shows these flux spectra are not W33-specific evidence. No full80site equivalence, continuum matching, physical coupling selection or interactingSM prediction.',
        prior=['11974 full two-loop matter patch','TOE57 pure-gauge flux/coupling scaling','11970 simpler free Dirac control'])


if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11979_native_patch_decimation.json').write_text(json.dumps(d,indent=2)+'\n')
    print('PASS exact subdivision',d['native_cycle_Gram'],d['leading_virtual_hop_coefficient'])
