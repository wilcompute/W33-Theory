#!/usr/bin/env python3
"""Pass 4812 — classify every H10 radius-14 deep-hole coset by quotient SAT.

Pass4801 proved rho(H10)=14.  A deep-hole leader is therefore exactly a
weight-14 vector x satisfying d(x,c)>=14 for all c in H10.  Instead of
enumerating 2^30 cosets, use a 30-row parity check for H10 to attach a 30-bit
coset syndrome y to x.

The SAT instance contains:
  * wt(x)=14;
  * |supp(x) cap supp(c)| <= wt(c)/2 for every H10 codeword c;
  * y=H_perp x, encoded by XOR chains.

After a solution is found, its complete PSp(4,3) orbit of coset syndromes is
blocked by one 30-literal clause per coset.  Re-solving discovers another orbit
or proves UNSAT.  Thus the loop is an exhaustive orbit classifier.  The full
PGSp action is then applied to determine outer fusions.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import networkx as nx
import numpy as np
from pysat.formula import CNF,IDPool
from pysat.card import CardEnc,EncType
from pysat.solvers import Solver
from w33_pass4495_4502_distance_prism_reconstruction import geometry
from w33_pass4721_4724_support12_involution_square_root_cover import build_groups
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4812_H10_DEEP_HOLE_ORBITS.json'
WITNESS=253626779097
G=np.array([
[0,1,1,1,1,0,0,0,1,0,0,0,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[1,0,1,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0],
[1,1,0,1,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,1,0,0,1,0,0,1,0],
[1,1,1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,1,0,0,1,0,0,1],
[1,0,0,0,0,1,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0],
[1,0,0,1,1,0,0,1,0,1,1,0,0,1,1,0,1,0,0,1,0,0,0,0,1,0,0,0,0,1,1,0,1,0,0,1,1,0,0,0],
[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,0,1,1,1,0,0,1,1,0,0,0,1,0,1,0,1,1,1,1,0,0,0,0],
[1,0,0,1,0,1,1,0,0,1,1,0,1,0,0,1,1,0,0,1,0,0,1,1,0,0,0,0,1,0,0,1,0,1,1,0,0,0,0,0],
[0,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,0,1,0,0,1,0,0,1,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0],
[0,1,1,1,1,1,1,0,1,1,0,1,1,0,1,1,0,0,1,1,0,0,1,0,1,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0]],dtype=np.uint8)

def mask(v):return sum(int(b)<<i for i,b in enumerate(v))
def span():
    rows=[mask(r) for r in G];C=[]
    for a in range(1024):
        x=0
        for i,r in enumerate(rows):
            if a>>i&1:x^=r
        C.append(x)
    assert Counter(x.bit_count() for x in C)==Counter({0:1,12:40,16:135,20:672,24:135,28:40,40:1})
    return C

def nullspace_basis():
    A=G.copy();r=0;piv=[]
    for c in range(40):
        s=next((i for i in range(r,10) if A[i,c]),None)
        if s is None:continue
        A[[r,s]]=A[[s,r]]
        for i in range(10):
            if i!=r and A[i,c]:A[i]^=A[r]
        piv.append(c);r+=1
    free=[c for c in range(40) if c not in piv];B=[]
    for f in free:
        x=np.zeros(40,dtype=np.uint8);x[f]=1
        for i,c in enumerate(piv):x[c]=A[i,f]
        B.append(mask(x))
    assert len(B)==30
    return B

def code_coordinate_groups(C):
    # Intrinsically recover the W33 graph from the 40 weight-12 codewords.
    W=[c for c in C if c.bit_count()==12];assert len(W)==40
    H=nx.Graph();H.add_nodes_from(range(40))
    for i,j in itertools.combinations(range(40),2):
        if (W[i]&W[j]).bit_count()==2:H.add_edge(i,j)
    assert H.number_of_edges()==240 and set(dict(H.degree()).values())=={12}
    sig=[frozenset(i for i,w in enumerate(W) if w>>j&1) for j in range(40)]
    nbh=[frozenset(H.neighbors(i)) for i in range(40)]
    phi=[]
    for s in sig:
        hit=[i for i,n in enumerate(nbh) if n==s];assert len(hit)==1;phi.append(hit[0])
    invphi={h:j for j,h in enumerate(phi)}
    pts,pidx,lines,A,_,_,_=geometry();S=nx.Graph();S.add_nodes_from(range(40));S.add_edges_from((i,j) for i in range(40) for j in range(i+1,40) if A[i,j])
    m=next(nx.algorithms.isomorphism.GraphMatcher(S,H).isomorphisms_iter());mi={v:k for k,v in m.items()}
    _,inner,full=build_groups(pts,pidx,lines)
    def transfer(p):
        out=[]
        for j in range(40):
            h=phi[j];std=mi[h];h2=m[p[std]];out.append(invphi[h2])
        return tuple(out)
    return [transfer(p) for p in inner],[transfer(p) for p in full]

def pmask(x,p):
    y=0
    for i in range(40):
        if x>>i&1:y|=1<<p[i]
    return y

def syndrome(x,H):return sum(((x&r).bit_count()&1)<<i for i,r in enumerate(H))

def xor3(cnf,a,b,z):
    cnf.extend([[-a,-b,-z],[a,b,-z],[a,-b,z],[-a,b,z]])
def xor_equal(cnf,pool,lits,y):
    if not lits:cnf.append([-y]);return
    if len(lits)==1:cnf.extend([[-lits[0],y],[lits[0],-y]]);return
    cur=lits[0]
    for b in lits[1:]:
        z=pool.id();xor3(cnf,cur,b,z);cur=z
    cnf.extend([[-cur,y],[cur,-y]])

def base_sat(C,H):
    pool=IDPool(start_from=71);cnf=CNF();X=list(range(1,41));Y=list(range(41,71))
    cnf.extend(CardEnc.equals(X,bound=14,vpool=pool,encoding=EncType.seqcounter).clauses)
    for c in C:
        w=c.bit_count()
        if w in (0,40):continue
        supp=[i+1 for i in range(40) if c>>i&1]
        cnf.extend(CardEnc.atmost(supp,bound=w//2,vpool=pool,encoding=EncType.seqcounter).clauses)
    for k,r in enumerate(H):xor_equal(cnf,pool,[i+1 for i in range(40) if r>>i&1],Y[k])
    return cnf,X,Y

def block_syndrome(S,s):
    S.add_clause([-(41+i) if s>>i&1 else (41+i) for i in range(30)])
def coset_distribution(x,C):return dict(sorted(Counter((x^c).bit_count() for c in C).items()))

def main():
    C=span();H=nullspace_basis();inner,full=code_coordinate_groups(C);assert len(inner)==25920 and len(full)==51840
    cnf,X,Y=base_sat(C,H);orbits=[];blocked=set()
    # Seed the previously certified radius-14 witness orbit.
    seeds=[WITNESS]
    with Solver(name='glucose4',bootstrap_with=cnf.clauses) as S:
        while True:
            if seeds:x=seeds.pop()
            else:
                if not S.solve():break
                model=S.get_model();x=sum(1<<i for i in range(40) if model[i]>0)
                assert x.bit_count()==14 and min((x^c).bit_count() for c in C)==14
            synorb={syndrome(pmask(x,p),H) for p in inner}
            new=synorb-blocked
            if not new:continue
            assert len(new)==len(synorb)
            for s in synorb:block_syndrome(S,s)
            blocked|=synorb
            fullorb={syndrome(pmask(x,p),H) for p in full}
            leaders=[x^c for c in C if (x^c).bit_count()==14]
            orbits.append({'representative':x,'PSp_cosets':len(synorb),'PSp_stabilizer':25920//len(synorb),
              'full_cosets':len(fullorb),'full_stabilizer':51840//len(fullorb),
              'leaders_in_representative_coset':len(leaders),'coset_weight_distribution':coset_distribution(x,C)})
        # UNSAT here is the exhaustive completeness certificate after blocking every discovered orbit.
        assert not S.solve()
    # Outer fusion is read from equality/intersection of full syndrome orbits.
    total=sum(o['PSp_cosets'] for o in orbits)
    out={'pass':4812,'code':'H10=[40,10,12]','covering_radius':14,'PSp_order':25920,'full_order':51840,
      'PSp_deep_hole_orbits':len(orbits),'deep_hole_cosets_total':total,'orbits':orbits,
      'final_orbit_blocked_SAT':'UNSAT',
      'theorem':'The quotient-SAT orbit sieve exhausts all H10 radius-14 cosets under PSp(4,3); each discovered orbit is blocked in the 30-bit coset syndrome space and the final instance is UNSAT.',
      'boundary':'Deep holes are cosets, not individual weight-14 leaders. Outer fusion is computed on 30-bit coset syndromes; no classification is inferred from a single witness orbit without the final UNSAT certificate.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
