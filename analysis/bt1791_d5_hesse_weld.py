#!/usr/bin/env python3
"""BT1791: D5 x Hesse weld."""
from __future__ import annotations
import json
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'bt1791_d5_hesse_weld.json'
F=range(3); SHIFTS=[2,0,3,1,3,0,3,4]
def rep(v):
    v=tuple(x%3 for x in v)
    for x in v:
        if x:
            inv=1 if x==1 else 2
            return tuple((inv*y)%3 for y in v)
    raise ValueError('zero')
def form(u,v): return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%3
def pts(): return sorted({rep(v) for v in product(F, repeat=4) if any(v)})
def pline(u,v): return frozenset(rep(tuple((a*u[i]+b*v[i])%3 for i in range(4))) for a,b in product(F,F) if a or b)
def shell_coord(v):
    if v[2]==2: v=tuple((2*x)%3 for x in v)
    return (v[0],v[1],v[3])
def build():
    P=pts(); anchor=rep((1,0,0,0)); shell=set(p for p in P if p!=anchor and form(anchor,p)!=0)
    lines=sorted({pline(u,v) for u,v in combinations(P,2) if form(u,v)==0}, key=lambda L: sorted(L))
    old=[]
    for L in lines:
        if anchor in L: continue
        sh=tuple(sorted(shell_coord(x) for x in L if x in shell)); assert len(sh)==3
        old.append(sh)
    new=[tuple((a,b,d) for a in F) for b,d in product(F,F)]
    all_lines=[]
    for i,L in enumerate(old): all_lines.append((f'O{i:02d}',L,'old_W33_shell'))
    for i,L in enumerate(new): all_lines.append((f'N{i:02d}',L,'new_H27_vertical'))
    coords=sorted({p for _,L,_ in all_lines for p in L})
    return coords, all_lines
def main():
    coords,lines=build(); incident=defaultdict(list)
    for name,L,kind in lines:
        for p in L: incident[p].append((name,kind))
    assert len(coords)==27 and len(lines)==45 and all(len(v)==5 for v in incident.values())
    type_hist=Counter(tuple(sorted(Counter(k for _,k in incident[p]).items())) for p in coords)
    assert type_hist=={(('new_H27_vertical',1),('old_W33_shell',4)):27}
    local_flags=[]
    for p in coords:
        inc=sorted(incident[p], key=lambda nk: (0 if nk[1]=='new_H27_vertical' else 1, nk[0]))
        for phase,(line,kind) in enumerate(inc):
            for orient in (1,-1): local_flags.append({'point':p,'phase':phase,'line':line,'kind':kind,'orientation':orient})
    assert len(local_flags)==270
    cycle_flags=len(SHIFTS)*len(local_flags); assert cycle_flags==2160
    payload={'bt':'BT1791','title':'D5 x Hesse weld','inputs':{'bt1783_rephase_shifts':SHIFTS,'bt1783_cycles':8,'bt1790_h27_points':27,'h27_line_patches':45},'local_d5_pencil':{'pencils':27,'phases_per_pencil':5,'local_D5_order':10,'phase_0':'the unique new Heisenberg vertical fibre through the point','phases_1_to_4':'the four old W33 shell triples through the point','pencil_type_histogram':{str(k):v for k,v in type_hist.items()},'oriented_flags_per_h27_boundary':270},'mirror_bus_weld':{'formula':'8 Coxeter cycles * 27 H27 points * 5 D5 phases * 2 orientations','value':cycle_flags,'equals_mirror_bus_slots':True,'factorization':'2160 = 8 * 27 * 5 * 2','compare_existing':'also 2160 = 45 * 48 = 30 * 72 in the holonet runtime ledger'},'boundary':'local phase/pencil weld; not a global D5^27 automorphism claim','conclusion':'BT1783 D5 phase bus and BT1790 H27/Payne sheaf meet at the five-line pencil through each H27 point; the eight-cycle lift gives 2160 mirror slots.'}
    OUT.write_text(json.dumps(payload,indent=2,sort_keys=True))
    print(json.dumps({'local_flags':270,'cycles':8,'cycle_flags':2160,'factorization':'8*27*5*2'},indent=2,sort_keys=True))
if __name__=='__main__': main()
