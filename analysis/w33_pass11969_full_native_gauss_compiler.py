"""Matrix-free FULL declared finite W33 compact U1/fermion Hamiltonian.

Native80 sites,160 links,1385 plaquette rows. Exact integer tree Gauss solve;
81 independent integer chord fluxes and half-filled80-site fermionic Fock
sector. This defines all operator moves, not a full-spectrum diagonalization.
"""
from pathlib import Path
from collections import defaultdict
from math import comb
import json
import sys
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261010_toe38_local_maxwell_2complex import prep,cycle_row
from w33_20261010_toe35_three_deck_kinematic_construction import spanning_chords


class NativeGaussCompiler:
    def __init__(self):
        self.edges,self.volts,lookup,octs,comm,*_=prep()
        self.chords=list(spanning_chords(self.edges));self.chord_index={e:i for i,e in enumerate(self.chords)}
        assert len(self.chords)==81
        self.B=np.zeros((160,80),dtype=int)
        adj=[[] for _ in range(80)];tree=[[] for _ in range(80)]
        for e,(a,b) in enumerate(self.edges):
            self.B[e,a]=-1;self.B[e,b]=1
            adj[a].append(b);adj[b].append(a)
            if e not in self.chord_index:
                tree[a].append((b,e,1));tree[b].append((a,e,-1))
        self.order=[0];self.parent={0:None};self.parent_edge={}
        self.color={0:0}
        for a in self.order:
            for b,e,sign in tree[a]:
                if b not in self.parent:
                    self.parent[b]=a;self.parent_edge[b]=(e,sign);self.order.append(b)
        assert len(self.order)==80
        queue=[0]
        for a in queue:
            for b in adj[a]:
                if b not in self.color:self.color[b]=1-self.color[a];queue.append(b)
                else:assert self.color[a]!=self.color[b]
        self.background=np.array([self.color[i] for i in range(80)],dtype=int)
        assert sum(self.background)==40
        self.P=np.rint(np.array([cycle_row(w,self.edges,self.volts,lookup,np.zeros(3)).real for w in octs+comm])).astype(int)
        assert self.P.shape==(1385,160) and np.max(abs(self.P@self.B))==0

    @staticmethod
    def occupation(bits):return np.array([(bits>>i)&1 for i in range(80)],dtype=int)

    def flux(self,state):
        bits,chord_flux=state;occ=self.occupation(bits)
        assert sum(occ)==40 and len(chord_flux)==81
        n=np.zeros(160,dtype=int);n[self.chords]=chord_flux
        residual=occ-self.background+self.B.T@n
        subtree=residual.copy()
        for b in reversed(self.order[1:]):
            e,sign=self.parent_edge[b]
            n[e]=-sign*subtree[b]
            subtree[self.parent[b]]+=subtree[b]
        assert subtree[0]==0
        assert np.array_equal(self.B.T@n+occ-self.background,np.zeros(80,dtype=int))
        return n

    def hop(self,state,edge):
        bits,l=state;a,b=self.edges[edge]
        oa,ob=(bits>>a)&1,(bits>>b)&1
        if oa==ob:return None
        direction=1 if oa else -1
        new_l=list(l)
        if edge in self.chord_index:new_l[self.chord_index[edge]]-=direction
        target=(bits^(1<<a)^(1<<b),tuple(new_l))
        sign=(-1)**sum((bits>>j)&1 for j in range(min(a,b)+1,max(a,b)))
        return target,sign,direction

    def plaquette(self,state,row,sign=1):
        bits,l=state
        target=tuple(int(x) for x in np.asarray(l)+sign*self.P[row,self.chords])
        return bits,target

    def apply_H(self,state,g=.8,beta=.4,kappa=.7,mass=.3):
        n=self.flux(state);occ=self.occupation(state[0]);out=defaultdict(float)
        out[state]+=g*g*float(n@n)/2+mass*float((1-2*self.background)@occ)
        for edge in range(160):
            result=self.hop(state,edge)
            if result is not None:
                target,sign,_=result;out[target]-=kappa*sign
        for row in range(1385):
            # Zero commutator-chain rows are identity Wilson operators;
            # their1-cos term cancels, rather than adding a spurious constant.
            if not np.any(self.P[row]):continue
            out[state]+=beta/(g*g)
            out[self.plaquette(state,row,1)]-=beta/(2*g*g)
            out[self.plaquette(state,row,-1)]-=beta/(2*g*g)
        return dict(out)


def payload():
    c=NativeGaussCompiler();rng=np.random.default_rng(119690)
    states=[];hops=0
    for _ in range(16):
        filled=sorted(map(int,rng.choice(80,40,replace=False)))
        bits=sum(1<<i for i in filled);l=tuple(map(int,rng.integers(-2,3,size=81)))
        state=(bits,l);n=c.flux(state);states.append(state)
        for edge in range(160):
            result=c.hop(state,edge)
            if result is None:continue
            target,sign,direction=result
            delta=c.flux(target)-n
            expected=np.zeros(160,dtype=int);expected[edge]=-direction
            assert np.array_equal(delta,expected)
            reverse=c.hop(target,edge)
            assert reverse[0]==state and reverse[1]==sign
            hops+=1
    state=states[0];n=c.flux(state)
    for row in range(1385):
        target=c.plaquette(state,row)
        assert np.array_equal(c.flux(target)-n,c.P[row])
        assert c.plaquette(target,row,-1)==state
    action=c.apply_H(state)
    assert all(np.isreal(x) for x in action.values())
    return dict(status='PASS',native_sites=80,native_links=160,plaquette_rows=1385,
                spanning_tree_links=79,integer_chord_fluxes=81,fermion_number=40,
                fermion_sector_dimension=str(comb(80,40)),
                physical_Hilbert_space='ell²(Z^81) tensor wedge^40(C^80), with fixed staggered background on the native40+40 bipartition',
                exact_Gauss_solution='Fill chord fluxes; solve tree fluxes by signed subtree charge sums. A reduced oriented tree incidence matrix is unimodular, so every integral neutral charge/chord assignment has one integral tree solution, and every Gauss-compatible flux is reached uniquely.',
                Hamiltonian='H=g² sum_e n_e²/2 +m sum_v(-1)^color_v occ_v -kappa sum_e(psi_b† U_lower,e psi_a+h.c.) +beta/g² sum_p[1-(S_p+S_p†)/2]. S_p shifts all electric fluxes by the integer plaquette boundary.',
                operator_coordinates='An oriented fermion hop lowers the crossed link; chord integer changes only if this is a chord. Plaquette shifts chord vector by P[row,chords]. Tree solve reconstructs exactly the complete link move in both cases.',
                well_definedness='Electric quadratic operator is self-adjoint on its natural diagonal domain. Finite sums of unitary plaquette shifts and bounded80-site fermion hopping are bounded symmetric perturbations; the displayed Hamiltonian is self-adjoint and semibounded. This is standard finite lattice gauge quantization, applied to the named native maps.',
                random_full_Gauss_states=len(states),legal_hops_verified=hops,
                plaquette_moves_verified=1385,zero_plaquette_chain_rows=int(sum(~np.any(c.P,axis=1))),
                one_state_Hamiltonian_action_support=len(action),
                scope='FULL declared finite native U1/fermion operator, including every supplied plaquette row and edge hop, compiled matrix-free. No full-spectrum diagonalization, chiral3+1D Weyl interpretation, interacting continuum limit, gravity or selected physical coupling. Background, masses and couplings are supplied; exterior freezing applies only to the separate octagon benchmark, not this compiler.',
                prior=['TOE38 native complex','TOE55 classical matter/Gauss','TOE56-57 quantum plaquette truncations','11969 coupled octagon and separate1D calibration'])


if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11969_full_native_gauss_compiler.json').write_text(json.dumps(d,indent=2)+'\n')
    print('PASS',d['legal_hops_verified'],d['one_state_Hamiltonian_action_support'],d['fermion_sector_dimension'],flush=True)
