#!/usr/bin/env python3
"""Pass5307 (bonkers): order-4 Latin isotopy census and the MOLS(4)/PG(3,2) spread bridge.

Enumerate all 576 Latin squares of order4 and recover the two isotopy classes:
144 Klein-V4 type and 432 cyclic-C4 type.  The V4 chart has autotopy stabilizer96;
the C4 chart has stabilizer32 inside S4^3, giving 13824/96=144 and
13824/32=432.

On the 16 V4 cells = F2^4, a complete set of three MOLS(4) is equivalent to the
five parallel-class directions of AG(2,4), i.e. a five-line spread of PG(3,2).
There are exactly56 line spreads in PG(3,2).  GL4(2) is transitive on them, so a
spread stabilizer has order 20160/56=360.  The q5 A5-invariant five-line spread
of Pass5296 is therefore GL4(2)-conjugate to this MOLS spread, but an objectwise
canonical conjugacy is not asserted here.
"""
from __future__ import annotations
import itertools,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5307_ORDER4_LATIN_MOLS_PG32_SPREAD.json'

def all_latin():
    perms=list(itertools.permutations(range(4)));out=[]
    def rec(rows):
        if len(rows)==4:out.append(tuple(rows));return
        for r in perms:
            if all(len({*(rows[i][c] for i in range(len(rows))),r[c]})==len(rows)+1 for c in range(4)):rec(rows+(r,))
    rec(tuple());return out

def autotopy(op):
    S4=list(itertools.permutations(range(4)));cnt=0
    for a in S4:
        for b in S4:
            mp={};ok=True
            for r in range(4):
                for c in range(4):
                    t=op(r,c);v=op(a[r],b[c])
                    if t in mp and mp[t]!=v:ok=False;break
                    mp[t]=v
                if not ok:break
            if ok and len(mp)==4 and len(set(mp.values()))==4:cnt+=1
    return cnt

def rank(cols):
    piv={}
    for x in cols:
        while x:
            p=x.bit_length()-1
            if p in piv:x^=piv[p]
            else:piv[p]=x;break
    return len(piv)

def apply(A,x):
    y=0
    for i,e in enumerate((1,2,4,8)):
        if x&e:y^=A[i]
    return y

def main():
    L=all_latin();assert len(L)==576
    aV=autotopy(lambda r,c:r^c);aC=autotopy(lambda r,c:(r+c)%4)
    assert (aV,aC)==(96,32)
    isoV=24**3//aV;isoC=24**3//aC;assert (isoV,isoC)==(144,432) and isoV+isoC==576
    lines=sorted({tuple(sorted((a,b,a^b))) for a,b in itertools.combinations(range(1,16),2)})
    assert len(lines)==35
    spreads=[]
    for S in itertools.combinations(range(35),5):
        U=set();ok=True
        for i in S:
            T=set(lines[i])
            if U&T:ok=False;break
            U|=T
        if ok and len(U)==15:spreads.append(S)
    assert len(spreads)==56
    standard=[(1,2,3),(4,8,12),(5,10,15),(6,11,13),(7,9,14)]
    assert all(tuple(sorted(x)) in lines for x in standard)
    # GL4(2) orbit of the standard spread.
    std={frozenset(x) for x in standard};orbit=set();stab=0;gl=0
    for A in itertools.permutations(range(1,16),4):
        if rank(A)!=4:continue
        gl+=1;S=frozenset(frozenset(apply(A,x) for x in L0) for L0 in std);orbit.add(S)
        if S==frozenset(std):stab+=1
    assert gl==20160 and len(orbit)==56 and stab==360
    out={'pass':5307,'status':'THEOREM_ORDER4_LATIN_576_SPLITS_144_PLUS432_AND_MOLS_COMPLETION_IS_PG32_SPREAD',
      'latin_squares_order4':576,'isotopy_classes':2,
      'V4_type':{'autotopy_order':96,'isotopy_class_size':144},
      'C4_type':{'autotopy_order':32,'isotopy_class_size':432},
      'PG3_2':{'points':15,'lines':35,'line_spreads':56,'GL4_2_order':20160,'spread_stabilizer_order':360},
      'standard_MOLS_spread':[list(x) for x in standard],
      'spread_meaning':'row, column, and three Latin symbol directions form the five parallel classes of an affine plane of order4 / complete set of three MOLS(4).',
      'q5_fiber_bridge':'Pass5296 independently finds an A5-invariant five-line spread in each q5 PG(3,2) K0 fiber. Since GL4(2) is transitive on all56 spreads, it is conjugate to a complete-MOLS(4) spread.',
      'boundary':'Conjugacy of spreads is proved; a canonical objectwise identification between the particular q5 fiber labels and the particular Latin chart is not yet fixed.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
