#!/usr/bin/env python3
"""Pass5311: all 576 order-4 Latin squares against the fixed toroidal-knight Q4.

Use the repository's 4x4 toroidal knight graph (32 edges, isomorphic to Q4) on
cells (r,c).  For every Latin square count the knight edges whose endpoint cells
carry the same symbol.  The exact census is

    same-symbol knight edges 0 : 96 squares
                            8 : 192 squares
                           16 : 288 squares.

Thus 576=96+192+288 on an object-level statistic, matching the tomotope96,
D4/tesseract192, and Hoffman-central-quotient288 scales without identifying
those groups with the three subsets.

Refine by the common board group preserving BOTH the Hamming-grid row/column
structure and the toroidal knight Q4.  It has order128.  With independent symbol
relabeling S4, the induced order3072 action on Latin squares has five orbits
48,48,96,192,192, exactly distinguished by (same-knight-edge count,
intercalate count).
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5311_ORDER4_LATIN_TOROIDAL_Q4_CENSUS.json'
S4=list(itertools.permutations(range(4)))

def all_latin():
    out=[]
    def rec(rows):
        if len(rows)==4: out.append(tuple(rows));return
        for r in S4:
            if all(len({*(rows[i][c] for i in range(len(rows))),r[c]})==len(rows)+1 for c in range(4)):
                rec(rows+(r,))
    rec(tuple());return out

def knight_edges():
    E=set();moves=((1,2),(3,2),(2,1),(2,3))
    for r,c in itertools.product(range(4),repeat=2):
        a=4*r+c
        for dr,dc in moves:
            b=4*((r+dr)%4)+(c+dc)%4;E.add(tuple(sorted((a,b))))
    assert len(E)==32;return E

def flat(s):return tuple(x for row in s for x in row)
def intercalates(s):
    z=0
    for r1,r2 in itertools.combinations(range(4),2):
      for c1,c2 in itertools.combinations(range(4),2):
        a,b,c,d=s[r1][c1],s[r1][c2],s[r2][c1],s[r2][c2]
        z+=a==d and b==c and a!=b
    return z

def board_perm(pr,pc,swap):
    a=[]
    for r,c in itertools.product(range(4),repeat=2):
        R,C=pr[r],pc[c]
        if swap:R,C=C,R
        a.append(4*R+C)
    return tuple(a)

def transform(s,p,sym):
    out=[None]*16
    for old in range(16):out[p[old]]=sym[s[old]]
    return tuple(out)

def main():
    L=all_latin();assert len(L)==576;E=knight_edges();LF=[flat(s) for s in L];LS=set(LF)
    def same(s):return sum(s[a]==s[b] for a,b in E)
    census=Counter(same(s) for s in LF);assert census==Counter({16:288,8:192,0:96})
    cross=Counter((same(flat(s)),intercalates(s)) for s in L)
    assert cross==Counter({(8,4):192,(16,4):192,(16,12):96,(0,12):48,(0,4):48})

    # Aut(H(2,4)) = (S4 x S4):C2; retain only elements preserving this fixed Q4 edge set.
    A=[]
    for pr in S4:
      for pc in S4:
       for sw in (False,True):
        p=board_perm(pr,pc,sw)
        if {tuple(sorted((p[a],p[b]))) for a,b in E}==E:A.append(p)
    A=list(set(A));assert len(A)==128

    unseen=set(LS);orbs=[]
    while unseen:
        s=next(iter(unseen));O={transform(s,p,y) for p in A for y in S4}
        assert O<=LS;orbs.append(O);unseen-=O
    assert sorted(map(len,orbs))==[48,48,96,192,192]
    prof=[]
    for O in orbs:
        s=next(iter(O));sq=tuple(tuple(s[4*r+c] for c in range(4)) for r in range(4))
        prof.append({'size':len(O),'same_symbol_knight_edges':same(s),'intercalates':intercalates(s)})
    prof=sorted(prof,key=lambda x:(x['same_symbol_knight_edges'],x['intercalates'],x['size']))
    assert [(x['size'],x['same_symbol_knight_edges'],x['intercalates']) for x in prof]==[(48,0,4),(48,0,12),(192,8,4),(192,16,4),(96,16,12)]

    out={'pass':5311,'status':'THEOREM_ORDER4_LATIN_TOROIDAL_KNIGHT_Q4_CENSUS_96_192_288',
      'latin_squares':576,'toroidal_knight_graph':{'vertices':16,'edges':32,'graph':'Q4'},
      'same_symbol_knight_edge_census':{'0':96,'8':192,'16':288},
      'identity':'576=96+192+288',
      'intercalate_refinement':{f'{a},{b}':n for (a,b),n in sorted(cross.items())},
      'common_grid_Q4_board_group_order':128,'with_symbol_relabeling_order':128*24,
      'common_action_orbits':prof,
      'interpretation':'The 576 Latin squares acquire a canonical 96+192+288 partition after fixing the repository toroidal-knight Q4 structure on the same 16 cells.',
      'boundary':'The three subset cardinalities coincide with tomotope96, D4/tesseract192, and Hoffman-quotient288 scales, but this statistic alone is not a group isomorphism or torsor identification.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
