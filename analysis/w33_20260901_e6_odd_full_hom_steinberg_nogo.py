#!/usr/bin/env python3
"""Full PSp-equivariant Hom audit: 1080 E6-even triangles -> 120 odd/Steiner triangles.

The first odd-triangle audit tested only the three coarse relations by triangle
intersection size.  Here we compute the actual PSp(4,3) pair orbitals.  For a
transitive 1080 carrier, the equivariant Hom space has one basis incidence map
per stabilizer orbit on the 120 target points.  We construct every such basis
map and test its exact Gram on the central 3*St_81 block.

If every basis map has zero Steinberg Gram, then every equivariant linear map
from the 1080 carrier to the 120 odd-triangle permutation module annihilates the
entire Steinberg isotypic component.  This is a complete Hom-space no-go, not a
claim based on three coarse intersection classes.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
import sympy as sp

from w33_pass4992_4999_common import build_base,build_group,comp
from w33_20260901_steinberg_frame_common import build
from w33_20260831_c5_wedderburn_kernel import mulvec

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260901_E6_ODD_FULL_HOM_STEINBERG_NOGO.json'

def paired_closure(A,B,n,m):
    I=(tuple(range(n)),tuple(range(m)));S={I};D=deque([I])
    while D:
        a,b=D.popleft()
        for ga,gb in zip(A,B):
            z=(comp(ga,a),comp(gb,b))
            if z not in S:S.add(z);D.append(z)
    return S

def main():
    F=build(); b=build_base(); grp=build_group(b)
    q4,K33,kof=F['q4'],F['K33'],F['kof']; rel,T,E=F['rel'],F['T'],F['E']
    phi,q0=F['phi'],F['q0']
    DS,E36,H36,ei=b['DS'],b['E'],b['H36'],b['ei']
    edge_of_k={frozenset(DS[a]&DS[c]):e for e,(a,c) in enumerate(E36)}
    assert set(edge_of_k)==set(K33)
    even=[]
    for i,C in enumerate(q4):
        es=[edge_of_k[K33[k]] for k in sorted(kof[i])]
        V=frozenset(x for e in es for x in E36[e]);assert len(V)==3
        even.append(V)
    assert len(set(even))==1080
    odd=[]
    for tri in b['triangles']:
        es=[ei[tuple(sorted(e))] for e in itertools.combinations(tri,2)]
        if sum(int(b['sigma'][e]) for e in es)&1:odd.append(frozenset(tri))
    assert len(odd)==120 and set(odd)==set(map(frozenset,b['steiner']))
    eidx={V:i for i,V in enumerate(even)};oidx={V:i for i,V in enumerate(odd)}

    # DPp is the native inner-PSp action on the 36 *double-six* coordinates.
    # SpP is the conjugate action on the 36 spread coordinates and cannot be
    # applied directly to DS-index triples; the first CI attempt deliberately
    # caught that coordinate mismatch.
    GE=[];GO=[]
    for g in grp['DPp']:
        GE.append(tuple(eidx[frozenset(g[x] for x in V)] for V in even))
        GO.append(tuple(oidx[frozenset(g[x] for x in V)] for V in odd))
    G=paired_closure(GE,GO,1080,120);assert len(G)==25920
    H=[z for z in G if z[0][q0]==q0];assert len(H)==24

    unseen=set(range(120));horbits=[]
    while unseen:
        o=min(unseen);O={go[o] for _ge,go in H};unseen-=O;horbits.append(sorted(O))
    horbits=sorted(horbits,key=lambda O:(len(O),O[0]))

    # For each stabilizer orbit, form the full pair-orbit incidence relation.
    records=[];all_zero=True
    for hi,O in enumerate(horbits):
        o0=O[0]; rows=[set() for _ in range(1080)]
        for ge,go in G:rows[ge[q0]].add(go[o0])
        assert {len(r) for r in rows}=={len(O)}
        base=rows[q0]
        gramrow=[len(base & rows[phi[j]]) for j in range(1080)]
        oval=[None]*59
        for j,v in enumerate(gramrow):
            r=int(rel[0,j])
            if oval[r] is None:oval[r]=v
            else:assert oval[r]==v
        assert all(v is not None for v in oval)
        Gvec=sp.Matrix(oval);GEvec=mulvec(E,Gvec,T)
        zero=(GEvec==sp.zeros(59,1));all_zero &= zero
        ih=Counter(len(even[q0]&odd[o]) for o in O)
        records.append({'stabilizerOrbit':hi,'targetOrbitSize':len(O),
                        'intersectionHistogram':{str(k):v for k,v in sorted(ih.items())},
                        'steinbergGramZero':zero})

    out={'schema':'w33.20260901.e6-odd-full-hom-steinberg-nogo.v1','status':'PASS',
      'sourceCarrier':1080,'targetCarrier':120,'groupOrder':25920,
      'sourceStabilizerOrder':24,'equivariantHomDimension':len(horbits),
      'targetStabilizerOrbits':records,
      'allOrbitalBasisMapsAnnihilateSteinberg':all_zero,
      'consequence':('Hom_PSp(St_81, Q[Odd120]) = 0; the 120 odd/Steiner triangle permutation module contains no Steinberg constituent'
                     if all_zero else 'at least one equivariant orbital map sees the Steinberg block'),
      'theorem':('The full PSp-equivariant Hom space from the 1080 E6-even/obstruction carrier to the 120 E6-odd/Steiner triangle carrier is exhausted by the listed stabilizer-orbit incidence maps. If all listed Steinberg Grams vanish, every equivariant linear map annihilates all three Steinberg copies, proving the odd120 permutation module has no Steinberg constituent.'),
      'boundary':'Characteristic-zero finite representation no-go only; it does not rule out nonlinear, subgroup-equivariant, modular, or physically augmented couplings.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','HomDim':len(horbits),'orbitSizes':[len(O) for O in horbits],
                      'allZero':all_zero},sort_keys=True))

if __name__=='__main__':main()
