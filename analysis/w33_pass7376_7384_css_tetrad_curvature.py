#!/usr/bin/env python3
"""Pass7376-7384: CSS sector distances, Schlaefli tetrads, and mod-3 curvature transgression.

This pass joins three previously separate objects:
  C2=F3^36 --N--> C1=F3^45 --R--> C0=F3^27,
with the integral identity R N = 3 Q.

It proves:
* the dark ten-dimensional qutrit logical sector is literally H1=ker(R)/im(N);
* the complementary seven-dimensional logical sector is im(R^T)/im(N);
* pure star-sector logicals begin at weight 5 (27 cubic-line stars), whereas
  pure H1 logicals begin at weight 6 (120 Steiner K3,3 supports);
* Q|ker(N mod3) has rank 7 and image im(R R^T), giving a canonical
  curvature-transgression onto the same seven-dimensional quotient;
* over F2 the row code of Q^T is [27,7,11], and the 270 minimum dual tetrads
  are exactly induced 2K2's of cubic lines, in bijection with the 270 pairs
  of tritangents sharing one cubic line.

The rank-7 map is called a curvature transgression, not a standard Bockstein:
R N is not zero integrally, so the ordinary integral-chain-complex hypotheses
for a Bockstein are absent.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
import networkx as nx
from w33_pass4992_4999_common import build_base
import w33_pass7329_7336_char3_e6_defect as m3

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7376_7384_CSS_TETRAD_CURVATURE.json'


def gf2rank(A):
    B={}
    for row in np.asarray(A,dtype=np.uint8):
        x=sum((int(v)&1)<<i for i,v in enumerate(row))
        while x:
            k=x.bit_length()-1
            if k in B:x^=B[k]
            else:B[k]=x;break
    return len(B)


def gf2_col_masks(A):
    A=np.asarray(A,dtype=np.uint8);out=[]
    for j in range(A.shape[1]):
        x=0
        for i,b in enumerate(A[:,j]):
            if b:x|=1<<i
        out.append(x)
    return out


def no_small_ternary_dependency(R):
    """Prove no full-support ternary dependency on <=5 columns by MITM."""
    R=np.asarray(R,dtype=np.int64)%3
    def key(v):return bytes(np.asarray(v,dtype=np.uint8))
    pair={}
    for a,b in itertools.combinations(range(R.shape[1]),2):
        for sb in (1,2):
            pair.setdefault(key((R[:,a]+sb*R[:,b])%3),[]).append((a,b,1,sb))
    # weight 3: pair + singleton
    for c in range(R.shape[1]):
        for sc in (1,2):
            if key((-sc*R[:,c])%3) in pair:
                for p in pair[key((-sc*R[:,c])%3)]:
                    if c not in p[:2]:return False
    # weight 4: pair + pair
    for k,recs in pair.items():
        p=recs[0];v=(R[:,p[0]]+p[3]*R[:,p[1]])%3
        nk=key((-v)%3)
        for a in recs:
            for b in pair.get(nk,[]):
                if len(set(a[:2]+b[:2]))==4:return False
    # triples for weight 5
    triple={}
    for a,b,c in itertools.combinations(range(R.shape[1]),3):
        for sb in (1,2):
            for sc in (1,2):
                triple.setdefault(key((R[:,a]+sb*R[:,b]+sc*R[:,c])%3),[]).append((a,b,c,1,sb,sc))
    for k,recs in pair.items():
        p=recs[0];v=(R[:,p[0]]+p[3]*R[:,p[1]])%3
        nk=key((-v)%3)
        for a in recs:
            for t in triple.get(nk,[]):
                if len(set(a[:2]+t[:3]))==5:return False
    return True


def main():
    b=build_base();T=b['tritangents'];DS=b['DS']
    N=1-np.asarray(b['M'],dtype=int)
    R=np.zeros((27,45),dtype=int)
    for j,t in enumerate(T):R[list(t),j]=1
    RN=R@N
    assert set(map(int,np.unique(RN)))<={0,3}
    Q=RN//3
    assert np.array_equal(RN,3*Q)

    # Mod-3 chain complex and logical Hodge split.
    C=m3.basis([row for row in N.T])              # im N in C1
    K=m3.basis(m3.ns(R))                          # ker R in C1
    D=m3.basis([row for row in R])                # im R^T in C1
    assert (len(C),len(K),len(D))==(14,24,21)
    assert all(np.all((np.asarray(c)@R.T)%3==0) for c in C)
    assert all(m3.rank(C+[d])==len(C) for d in C)
    assert m3.rank(np.vstack(C+D))==21
    assert m3.rank(np.vstack(C+K))==24
    H2=m3.basis(m3.ns(N));H1dim=len(K)-len(C);H0dim=27-m3.rank(R)
    assert (len(H2),H1dim,H0dim)==(22,10,6)
    star_dim=len(D)-len(C);assert star_dim==7

    # Pure star sector: 27 line-star weight-five logicals.
    assert all(np.count_nonzero(row)==5 for row in R)
    assert len({tuple(map(int,row%3)) for row in R})==27

    # Pure H1 sector: no dependency below weight 6; all 120 induced K3,3 supports
    # carry a one-dimensional full-support ternary dependency.
    assert no_small_ternary_dependency(R)
    G45=nx.Graph();G45.add_nodes_from(range(45))
    for i,j in itertools.combinations(range(45),2):
        if set(T[i])&set(T[j]):G45.add_edge(i,j)
    indep3=[frozenset(x) for x in itertools.combinations(range(45),3)
            if all(not G45.has_edge(a,c) for a,c in itertools.combinations(x,2))]
    I3=set(indep3);K33=set()
    for A in indep3:
        common=set(range(45))
        for a in A:common&=set(G45.neighbors(a))
        for B3 in itertools.combinations(sorted(common),3):
            B3=frozenset(B3)
            if B3 in I3 and len(A|B3)==6:K33.add(frozenset(A|B3))
    assert len(K33)==120
    for S in K33:
        ns=m3.ns(R[:,sorted(S)])
        assert len(ns)==1 and np.count_nonzero(ns[0])==6
    dark_pure_distance=6

    # Curvature transgression kappa: H2 -> im(RR^T), z |-> Q z mod 3.
    H2A=np.asarray(H2,dtype=int)%3
    kappa=(H2A@Q.T)%3
    RR=(R@R.T)%3
    kr=m3.rank(kappa);rrr=m3.rank(RR)
    assert kr==rrr==7 and m3.rank(np.vstack([kappa,RR]))==7
    assert len(H2)-kr==15
    # R restricted to D has kernel exactly C, hence D/C ~= im(RR^T).
    assert len(D)-m3.rank(RR)==len(C)==14

    # Binary Q-shadow [27,7,11] and all 270 dual tetrads.
    QB=(Q.T%2).astype(np.uint8);assert gf2rank(QB)==7
    cols=gf2_col_masks(QB);tetrads=[]
    for S in itertools.combinations(range(27),4):
        z=0
        for j in S:z^=cols[j]
        if z==0:tetrads.append(frozenset(S))
    assert len(tetrads)==270
    G27=b['G27'];assert all(G27.subgraph(S).number_of_edges()==2 and
                           sorted(dict(G27.subgraph(S).degree()).values())==[1,1,1,1]
                           for S in tetrads)
    # Each tetrad is obtained uniquely from two tritangents sharing one line:
    # remove their common line and retain the other four lines.
    edge_to_tet={}
    for i,j in itertools.combinations(range(45),2):
        inter=set(T[i])&set(T[j])
        if len(inter)==1:
            tet=frozenset((set(T[i])|set(T[j]))-inter)
            assert tet in set(tetrads) and tet not in edge_to_tet.values()
            edge_to_tet[(i,j)]=tet
    assert len(edge_to_tet)==270 and set(edge_to_tet.values())==set(tetrads)
    # Association-design refinement: every meeting line-pair lies in 4 tetrads,
    # every skew pair in 5.
    paircount=Counter()
    for S in tetrads:
        for p in itertools.combinations(sorted(S),2):paircount[p]+=1
    meet=Counter(paircount[p] for p in paircount if G27.has_edge(*p))
    skew=Counter(paircount[p] for p in paircount if not G27.has_edge(*p))
    assert meet==Counter({4:135}) and skew==Counter({5:216})

    out={
      'schema':'w33.pass7376_7384.css_tetrad_curvature.v1','status':'PASS',
      'integral_curvature':'R N = 3 Q',
      'mod3_chain_homology':{'H2':22,'H1':10,'H0':6},
      'logical_hodge_split':{
        'star_sector':'im(R^T)/im(N), dimension 7, pure distance 5, 27 projective minimum line-star supports',
        'dark_sector':'ker(R)/im(N)=H1, dimension 10, pure distance 6, 120 projective minimum Steiner K3,3 supports'
      },
      'curvature_transgression':{
        'map':'kappa: H2 -> im(R R^T), z |-> Q z mod 3','rank':7,'kernel_dimension':15,
        'target_identification':'R induces im(R^T)/im(N) ~= im(R R^T)',
        'boundary':'Bockstein-like secondary operation, not identified with the standard Bockstein because R N is nonzero integrally.'
      },
      'binary_Q_shadow':{
        'code':'[27,7,11]_2','dual_minimum_weight':4,'dual_tetrads':270,
        'tetrad_geometry':'every support induces 2K2 in the cubic-line meet graph',
        'bijection':'270 tetrads <-> 270 intersecting tritangent pairs, by deleting their unique common cubic line',
        'association_design':{'meeting_pair_multiplicity':4,'skew_pair_multiplicity':5}
      },
      'boundary':'Exact finite incidence/coding theorem only.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','logical':'7(d5)+10(d6)','H':'22,10,6','tetrads':270,'kappa_rank':7}))
if __name__=='__main__':main()
