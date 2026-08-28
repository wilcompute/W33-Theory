#!/usr/bin/env python3
"""Exact test of the 576 minimum-vector stabilizer against all 4x4 Latin squares.

There are 576 labelled Latin squares of order four.  The W33 minimum-vector
stabilizer H also has order 576, with certified central quotient

    H/Z(H) ~= (A4 x A4) : C2 = A4 wr C2,

acting naturally on the two dual tetrads.  This file asks whether the repeated
integer 576 can be upgraded to a canonical Latin-square G-set bridge.

Two exact obstructions kill that route.

1. The FULL standard paratopy group S4^3 : S3 on labelled Latin squares has
   two invariant main classes, of sizes 144 and 432.  Therefore no subgroup of
   the standard row/column/symbol/parastrophe group can be transitive on all
   576 squares.  In particular the 576 squares cannot be a regular H-set under
   standard Latin-square symmetries.

2. The canonical tetrad quotient A4 wr C2 acts by even row permutations, even
   column permutations, and transpose.  Its exact orbit decomposition on the
   576 squares is

       36, 36, 72, 72, 72, 72, 72, 72, 72.

   Thus even the quotient action singled out by the W33 geometry is very far
   from transitive.

The 144 main class remains a legitimate residual comparison target: 144 divides
576, so an H-orbit of size 144 would have stabilizer 4.  The 432 main class
cannot be a transitive H-orbit because 432 does not divide 576.  No positive
identification of the 144 class is claimed here.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260828_LATIN576_STABILIZER_NOGO.json'

def parity(p):
    return sum(p[i]>p[j] for i in range(len(p)) for j in range(i+1,len(p)))%2

def latin_squares():
    rows=list(itertools.permutations(range(4)));out=[]
    def rec(chosen):
        if len(chosen)==4:
            out.append(tuple(x for r in chosen for x in r));return
        for r in rows:
            if all(all(prev[c]!=r[c] for prev in chosen) for c in range(4)):
                rec(chosen+[r])
    rec([]);return out

def grid_action(S,rp,cp,tr=False):
    out=[None]*16
    for r in range(4):
        for c in range(4):
            rr,cc=(c,r) if tr else (r,c)
            out[rp[rr]*4+cp[cc]]=S[r*4+c]
    return tuple(out)

def paratopy(S,rp,cp,sp,coord):
    out=[None]*16
    for r in range(4):
        for c in range(4):
            t=(rp[r],cp[c],sp[S[r*4+c]])
            u=(t[coord[0]],t[coord[1]],t[coord[2]])
            out[u[0]*4+u[1]]=u[2]
    return tuple(out)

def full_paratopy_orbit(S,S4,coords):
    out=set()
    for rp in S4:
        for cp in S4:
            for sp in S4:
                for co in coords:out.add(paratopy(S,rp,cp,sp,co))
    return out

def main():
    LS=latin_squares();assert len(LS)==576 and len(set(LS))==576
    S4=list(itertools.permutations(range(4)));A4=[p for p in S4 if parity(p)==0]
    coords=list(itertools.permutations(range(3)))
    assert len(S4)==24 and len(A4)==12 and len(coords)==6

    reduced=[S for S in LS if tuple(S[:4])==(0,1,2,3) and tuple(S[4*r] for r in range(4))==(0,1,2,3)]
    assert len(reduced)==4

    # Full paratopy main classes.
    C1=full_paratopy_orbit(LS[0],S4,coords);assert len(C1) in (144,432)
    S2=next(S for S in LS if S not in C1);C2=full_paratopy_orbit(S2,S4,coords)
    sizes=sorted([len(C1),len(C2)])
    assert sizes==[144,432] and not (C1&C2) and C1|C2==set(LS)
    small=C1 if len(C1)==144 else C2;large=C2 if len(C2)==432 else C1
    reduced_split=Counter('144' if S in small else '432' for S in reduced)
    assert reduced_split==Counter({'432':3,'144':1})

    # Canonical H/Z(H)=A4 wr C2 tetrad action: even rows, even columns,
    # optionally transpose.  It acts on all Latin squares without symbol moves.
    Q=[(r,c,t) for r in A4 for c in A4 for t in (False,True)]
    assert len(Q)==288
    unseen=set(LS);orbits=[]
    while unseen:
        S=next(iter(unseen));O={grid_action(S,r,c,t) for r,c,t in Q}
        assert O<=set(LS);orbits.append(O);unseen-=O
    od=Counter(map(len,orbits));assert od==Counter({72:7,36:2}) and len(orbits)==9
    class_orbits=Counter()
    for O in orbits:
        tag='144' if next(iter(O)) in small else '432'
        assert all((S in small)==(tag=='144') for S in O)
        class_orbits[(tag,len(O))]+=1
    assert class_orbits==Counter({('144',36):2,('144',72):1,('432',72):6})

    out={
      'schema':'w33.20260828.latin576-stabilizer-nogo.v1','status':'PASS',
      'latin_squares':{'order':4,'labelled_total':576,'reduced_total':4,'reduced_main_class_split':dict(reduced_split)},
      'full_standard_paratopy':{'group_order':24**3*6,'main_class_sizes':sizes,
        'consequence':'All standard row/column/symbol/parastrophe symmetries preserve the 144/432 partition; no subgroup is transitive on all 576 squares.'},
      'W33_stabilizer_input':{'order':576,'structure':'2^{1+4}_+ : (S3 x C3)',
        'central_quotient':'A4 wr C2','quotient_order':288,
        'source_certificate':'PART_W33_20260828_MINIMUM_STABILIZER_576_STRUCTURE.json'},
      'canonical_tetrad_quotient_action':{'orbit_size_distribution':dict(sorted(od.items())),
        'number_of_orbits':9,'main_class_refinement':{str(k):v for k,v in sorted(class_orbits.items(),key=str)}},
      'no_go':'The equality |H|=576=#LatinSquares(4) is not an equivariant G-set bridge under standard Latin-square symmetry. The canonical A4 wr C2 quotient has nine orbits, and the full paratopy group itself has two invariant main classes.',
      'residual_target':{'main_class_size':144,'possible_H_stabilizer_if_transitive':4,
        'status':'OPEN comparison target, not identified'},
      '432_class':{'size':432,'can_be_transitive_H_orbit':False,'reason':'432 does not divide 576'},
      'boundary':'This rules out the standard/canonical symmetry-preserving 576-square bridge. It does not rule out an externally defined non-paratopic action on the bare 576-element set.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','Latin':576,'main_classes':sizes,'A4wrC2_orbits':dict(od)}))
if __name__=='__main__':main()
