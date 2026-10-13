"""Two overlapping native loops WITH dynamical fermions on every patch site.

TOE57 owns pure gauge two-loop block;11969 owns one-loop matter and full
matrix-free operator. This solves a named connected patch, not the full graph.
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
from w33_pass11969_full_native_gauss_compiler import NativeGaussCompiler


class Patch:
    def __init__(self):
        c=NativeGaussCompiler()
        prior=json.loads((ROOT/'data/w33_20261013_toe57_two_plaquette_quantum.json').read_text())
        self.rows=prior['selected_native_plaquette_rows']
        support=np.flatnonzero(np.any(c.P[self.rows],axis=0))
        self.native_edges=list(map(int,support));self.native_vertices=sorted(set(c.edges[e][v] for e in support for v in (0,1)))
        vmap={v:i for i,v in enumerate(self.native_vertices)}
        self.edges=[(vmap[c.edges[e][0]],vmap[c.edges[e][1]]) for e in support]
        self.n=len(vmap);self.m=len(support)
        self.background=np.array([c.color[v] for v in self.native_vertices])
        self.B=np.zeros((self.m,self.n),int);adj=[[] for _ in range(self.n)]
        for e,(a,b) in enumerate(self.edges):self.B[e,a]=-1;self.B[e,b]=1;adj[a].append((b,e,1));adj[b].append((a,e,-1))
        self.order=[0];parent={0:None};self.parent_edge={}
        for a in self.order:
            for b,e,sgn in adj[a]:
                if b not in parent:parent[b]=a;self.parent_edge[b]=(a,e,sgn);self.order.append(b)
        tree={e for a,e,sgn in self.parent_edge.values()}
        self.chords=[e for e in range(self.m) if e not in tree]
        assert len(self.chords)==2 and len(self.order)==self.n
        # Every original native plaquette supported in this patch, deduplicated
        # up to orientation. Repeated native rows have multiplicity retained.
        contained=[r for r in c.P if np.any(r) and not np.any(r[np.setdiff1d(np.arange(160),support)])]
        self.P=np.array([r[support] for r in contained],int)
        assert np.max(abs(self.P@self.B))==0
        self.fermions=int(sum(self.background))

    def flux(self,bits,l,external):
        occ=np.array([(bits>>i)&1 for i in range(self.n)])
        n=np.zeros(self.m,int);n[self.chords]=l
        charge=occ-self.background+external+self.B.T@n
        for b in reversed(self.order[1:]):
            a,e,sgn=self.parent_edge[b];n[e]=-sgn*charge[b];charge[a]+=charge[b]
        assert charge[0]==0
        assert np.max(abs(self.B.T@n+occ-self.background+external))==0
        return n

    def sector(self,L,g=.8,beta=.4,kappa=.7,mass=.3,charged=False):
        external=np.zeros(self.n,int)
        if charged:
            a,b=self.edges[0];external[a]=1;external[b]=-1
        occs=[sum(1<<i for i in q) for q in combinations(range(self.n),self.fermions)]
        states=[(bits,l) for bits in occs for l in product(range(-L,L+1),repeat=2)]
        ids={x:i for i,x in enumerate(states)};rr=[];cc=[];vv=[]
        for idx,(bits,l) in enumerate(states):
            n=self.flux(bits,l,external);occ=np.array([(bits>>i)&1 for i in range(self.n)])
            diag=g*g*float(n@n)/2+mass*float((1-2*self.background)@occ)+len(self.P)*beta/(g*g)
            rr.append(idx);cc.append(idx);vv.append(diag)
            for e,(a,b) in enumerate(self.edges):
                oa,ob=(bits>>a)&1,(bits>>b)&1
                if oa==ob:continue
                direction=1 if oa else -1;new=list(l)
                if e in self.chords:new[self.chords.index(e)]-=direction
                target=(bits^(1<<a)^(1<<b),tuple(new))
                if target not in ids:continue
                sgn=(-1)**sum((bits>>j)&1 for j in range(min(a,b)+1,max(a,b)))
                rr.append(idx);cc.append(ids[target]);vv.append(-kappa*sgn)
            for p in self.P:
                for sign in (1,-1):
                    target=(bits,tuple(np.array(l)+sign*p[self.chords]))
                    if target in ids:rr.append(idx);cc.append(ids[target]);vv.append(-beta/(2*g*g))
        H=coo_matrix((vv,(rr,cc)),shape=(len(states),)*2).tocsr()
        difference=H-H.T;assert difference.nnz==0 or max(abs(difference.data))<1e-12
        ev,U=eigsh(H,k=3,which='SA',tol=1e-10,v0=np.ones(len(states))/np.sqrt(len(states)))
        ix=np.argsort(ev);ev=ev[ix];u=U[:,ix[0]]
        boundary=np.array([max(abs(z) for z in l)==L for bits,l in states])
        # Quantify screening: matter density responds to the static endpoints.
        mean=np.sum(np.array([[(bits>>j)&1 for j in range(self.n)] for bits,l in states])*abs(u[:,None])**2,axis=0)
        return dict(L=L,dimension=len(states),E0=float(ev[0]),gap=float(ev[1]-ev[0]),
                    boundary_probability=float(np.sum(abs(u[boundary])**2)),mean_occupations=mean.tolist(),
                    ground_residual=float(np.linalg.norm(H@u-ev[0]*u)),charged=charged)


def payload():
    c=Patch();rows=[]
    for L in (1,2,3):
        neutral=c.sector(L);charged=c.sector(L,charged=True)
        rows.append(dict(neutral=neutral,charged=charged,static_pair_energy=charged['E0']-neutral['E0'],
                         induced_density=(np.array(charged['mean_occupations'])-neutral['mean_occupations']).tolist()))
        print('patch',L,neutral['dimension'],neutral['E0'],charged['E0'],flush=True)
    assert all(rows[i+1]['neutral']['E0']<rows[i]['neutral']['E0'] for i in range(2))
    return dict(status='PASS',native_vertices=c.native_vertices,native_edges=c.native_edges,
                native_seed_plaquettes=c.rows,patch_sites=c.n,patch_links=c.m,independent_fluxes=2,
                contained_native_plaquette_rows=len(c.P),fermion_number=c.fermions,
                Hamiltonian='Restriction of11969 native electric/staggered-mass/link-dressed fermion hopping and every native plaquette whose support stays in this connected patch. Outside links and crossing plaquettes are omitted explicitly.',
                states='All fixed-number patch fermion configurations and two integer chord fluxes; exact signed tree Gauss solve. No fixed matter background ansatz.',
                parameters=dict(g=.8,beta=.4,kappa=.7,mass=.3),sectors=rows,
                scope='Interacting two-loop finite patch with dynamical charged matter and static opposite unit endpoints. Nested hard flux Galerkin truncations, not full80-site spectrum, certified infinite-flux convergence, physical confinement or native interacting4D matching. Exterior omitted;11969 full matrix-free operator is a distinct object.',
                prior=['TOE57 pure gauge two-native-loop benchmark','11969 coupled octagon','11969 full native Gauss compiler'])


if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass11974_coupled_patch_matter.json').write_text(json.dumps(d,indent=2)+'\n')
    print('PASS',[(r['neutral']['gap'],r['static_pair_energy']) for r in d['sectors']])
