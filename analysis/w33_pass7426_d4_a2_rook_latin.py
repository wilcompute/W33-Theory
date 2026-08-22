#!/usr/bin/env python3
"""Pass7426: the 16 A2 subsystems inside D4 form the 4x4 rook graph.

Consequences verified from the 24 D4 roots themselves:
- 16 A2 root subsystems;
- disjoint-root relation is SRG(16,6,2,2) and canonically L_2(4);
- 8 maximal K4s are exactly the root partitions D4 = A2 sqcup A2 sqcup A2 sqcup A2;
- 24 maximum cocliques are the 4x4 transversals;
- 24 partitions into four transversals; labeling the four classes gives 576 Latin squares.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7426_D4_A2_ROOK_LATIN.json'

def neg(v):return tuple(-x for x in v)
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def d4roots():
    R=[]
    for i,j in itertools.combinations(range(4),2):
      for a in (1,-1):
       for b in (1,-1):
        v=[0]*4;v[i]=a;v[j]=b;R.append(tuple(v))
    return sorted(set(R))
def a2s(R):
    RS=set(R);A=set()
    for a,b in itertools.combinations(R,2):
        if dot(a,b)!=-1:continue
        c=tuple(a[i]+b[i] for i in range(4))
        if c not in RS:continue
        A.add(frozenset((a,neg(a),b,neg(b),c,neg(c))))
    return sorted(A,key=lambda S:tuple(sorted(S)))
def cliques(adj,target):
    n=len(adj);out=[]
    for C in itertools.combinations(range(n),target):
        if all(j in adj[i] for i,j in itertools.combinations(C,2)):out.append(frozenset(C))
    return out

def main():
    R=d4roots();A=a2s(R);assert len(R)==24 and len(A)==16
    adj=[set() for _ in A]
    share=[set() for _ in A]
    for i,j in itertools.combinations(range(16),2):
        z=len(A[i]&A[j]);assert z in (0,2)
        if z==0:adj[i].add(j);adj[j].add(i)
        else:share[i].add(j);share[j].add(i)
    assert set(map(len,adj))=={6} and set(map(len,share))=={9}
    # SRG(16,6,2,2).
    lam=set();mu=set()
    for i,j in itertools.combinations(range(16),2):
        c=len(adj[i]&adj[j]);(lam if j in adj[i] else mu).add(c)
    assert lam=={2} and mu=={2}
    K4=cliques(adj,4);assert len(K4)==8
    # Every K4 consists of four disjoint 6-root A2s and partitions all 24 D4 roots.
    for C in K4:
        U=set().union(*(A[i] for i in C));assert len(U)==24 and U==set(R)
    # The 8 K4s split into two parallel classes of four: disjoint within a class,
    # one-cell intersection across classes.  This reconstructs the 4x4 rook coordinates.
    kgraph=[set() for _ in K4]
    for i,j in itertools.combinations(range(8),2):
        if len(K4[i]&K4[j])==1:kgraph[i].add(j);kgraph[j].add(i)
        else:assert len(K4[i]&K4[j])==0
    assert set(map(len,kgraph))=={4}
    # bipartition K4,4
    color={0:0};stack=[0]
    while stack:
        i=stack.pop()
        for j in kgraph[i]:
            if j not in color:color[j]=1-color[i];stack.append(j)
            else:assert color[j]!=color[i]
    fam0=[i for i in range(8) if color[i]==0];fam1=[i for i in range(8) if color[i]==1]
    assert len(fam0)==len(fam1)==4
    assert all(len(K4[i]&K4[j])==1 for i in fam0 for j in fam1)
    # Give each A2 its unique row/column coordinate.
    coord={}
    for r,i in enumerate(fam0):
      for c,j in enumerate(fam1):
        x=K4[i]&K4[j];assert len(x)==1;coord[next(iter(x))]=(r,c)
    assert len(coord)==16
    assert all((j in adj[i]) == (coord[i][0]==coord[j][0] or coord[i][1]==coord[j][1]) for i,j in itertools.combinations(range(16),2))
    # Maximum cocliques are transversals/permutations.
    coc=[frozenset(C) for C in itertools.combinations(range(16),4) if all(j not in adj[i] for i,j in itertools.combinations(C,2))]
    assert len(coc)==24
    assert all(len({coord[i][0] for i in C})==4 and len({coord[i][1] for i in C})==4 for C in coc)
    # Unlabelled Latin squares = partitions of 16 cells into four transversals.
    parts=set()
    for T in coc:
        rem=set(range(16))-set(T)
        others=[U for U in coc if U<=rem]
        for comb in itertools.combinations(others,3):
            blocks=(T,)+comb
            if len(set().union(*map(set,blocks)))==16 and sum(len(x) for x in blocks)==16:
                parts.add(tuple(sorted(tuple(sorted(x)) for x in blocks)))
    assert len(parts)==24
    labeled_latin=len(parts)*24;assert labeled_latin==576
    out={'schema':'w33.pass7426.d4_a2_rook_latin.v1','status':'PASS',
      'D4_roots':24,'A2_subsystems_in_D4':16,
      'disjoint_root_graph':'L_2(4) = SRG(16,6,2,2)','complement_degree':9,
      'maximal_K4_root_partitions':8,'root_partition_families':'4+4 with intersection graph K4,4',
      'maximum_coclique_transversals':24,'unlabelled_partitions_into_four_transversals':24,'labelled_order4_Latin_squares':576,
      'full_grid_automorphism_group':'S4 wr C2, order 1152 = full D4 root-system automorphism group W(F4)',
      'row_column_preserving_subgroup':'S4 x S4, order 576',
      'global_leaf_factorization':'Using the certified 64 Eisenstein leaves through each global D4 and transitivity of N_E8(D4) on the eight root partitions, each of the eight D4=A2^4 root partitions lies in exactly eight leaves; hence 64=8 x 8.',
      'theorem':'The recurring 4x4 grid is intrinsic to D4: its 16 A2 subsystems are the cells of L2(4). The eight rows/columns are exactly the eight partitions of the 24 D4 roots into four disjoint A2 hexagons, while the 24 transversals and their 24 four-way partitions give the classical 576 labelled Latin squares of order four.',
      'firewall':'The two appearances of 576 here (|S4xS4| and the number of labelled Latin squares) are internal consequences of the same 4x4 rook object. No identification with an unrelated order-576 stabilizer is claimed without an explicit action map.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','A2':16,'K4':8,'transversals':24,'Latin':576}))
if __name__=='__main__':main()
