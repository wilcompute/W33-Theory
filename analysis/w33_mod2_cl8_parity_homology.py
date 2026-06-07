#!/usr/bin/env python3
"""BT525: Mod-2 Cl8 Parity Homology Theorem.

Executes the parity-protection branch.

BT523 proved the integer factorization F M = 4 R.  Over F2 this becomes
F M = 0, so we have a genuine chain complex
    F2^1620 --M--> F2^320 --F--> F2^240.

This script computes its mod-2 homology:
    rank_2(F)=160, rank_2(M)=120, rank_2(FM)=0.
Therefore:
    H2 = ker(M)                 has dimension 1620-120 = 1500,
    H1 = ker(F)/im(M)           has dimension (320-160)-120 = 40,
    H0 = coker(F)               has dimension 240-160 = 80.

The key protected result is H1(F2)=40: the parity shadow of the signed-Xmin
quadrangle lift leaves exactly one W33 point/line carrier in first homology.
"""
from __future__ import annotations

import itertools, json
from collections import Counter, defaultdict
from pathlib import Path

P=3
Vec=tuple[int,int,int,int]

def canonical(v)->Vec:
    vv=tuple(int(x)%P for x in v)
    if vv==(0,0,0,0): raise ValueError('zero')
    for x in vv:
        if x:
            inv=1 if x==1 else 2
            return tuple((inv*y)%P for y in vv)  # type: ignore[return-value]
    raise AssertionError

def omega(u:Vec,v:Vec)->int:
    return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%P

def rank_gf2(rows:list[int])->int:
    basis={}
    for x0 in rows:
        x=x0
        while x:
            b=x.bit_length()-1
            if b in basis: x ^= basis[b]
            else:
                basis[b]=x; break
    return len(basis)

def geom():
    pts=[]; seen=set()
    for raw in itertools.product(range(P), repeat=4):
        if raw==(0,0,0,0): continue
        c=canonical(raw)
        if c not in seen: seen.add(c); pts.append(c)
    pidx={p:i for i,p in enumerate(pts)}; A=[[False]*40 for _ in range(40)]; edges=[]
    for i,j in itertools.combinations(range(40),2):
        if omega(pts[i],pts[j])==0: A[i][j]=A[j][i]=True; edges.append((i,j))
    lines=set()
    for i,j in edges:
        u,v=pts[i],pts[j]; line=set()
        for a,b in itertools.product(range(P), repeat=2):
            if a==0 and b==0: continue
            line.add(pidx[canonical((a*u[t]+b*v[t] for t in range(4)))])
        lines.add(tuple(sorted(line)))
    lines=sorted(lines); point_lines=defaultdict(list); edge_to_line={}
    for li,L in enumerate(lines):
        for p in L: point_lines[p].append(li)
        for e in itertools.combinations(L,2): edge_to_line[tuple(sorted(e))]=li
    return A,point_lines,edge_to_line

def quads(A):
    qs=[]; seen=set()
    for a,b in itertools.combinations(range(40),2):
        if A[a][b]: continue
        common=[x for x in range(40) if A[a][x] and A[b][x]]
        for c,d in itertools.combinations(common,2):
            cyc=tuple(sorted(tuple(sorted(e)) for e in ((a,c),(c,b),(b,d),(d,a))))
            if cyc not in seen: seen.add(cyc); qs.append(cyc)
    return qs

def local(p,Ls):
    Ls=sorted(Ls); verts=[]; faces=[]; v2f=defaultdict(list)
    for pair in itertools.combinations(Ls,2): verts.append((p,tuple(sorted(pair))))
    for L in Ls:
        others=[x for x in Ls if x!=L]
        fp=(p,L,1); fm=(p,L,-1); faces += [fp,fm]
        for M in others: v2f[(p,tuple(sorted((L,M))))].append(fp)
        for pair in itertools.combinations(others,2): v2f[(p,tuple(sorted(pair)))].append(fm)
    return verts,faces,v2f

def main()->dict:
    A,point_lines,edge_to_line=geom(); qs=quads(A)
    verts=[]; signed=[]; v2f={}
    for p in range(40):
        vs,fs,loc=local(p,point_lines[p]); verts+=vs; signed+=fs; v2f.update(loc)
    verts=sorted(verts); signed=sorted(signed); vi={v:i for i,v in enumerate(verts)}; si={f:i for i,f in enumerate(signed)}

    F_rows=[0]*240
    for v,fs in v2f.items():
        r=vi[v]; x=0
        for f in fs: x |= 1 << si[f]
        F_rows[r]=x

    M_rows=[0]*320; R_rows=[0]*240
    for qi,cyc in enumerate(qs):
        inc=defaultdict(list)
        for u,v in cyc: inc[u].append((u,v)); inc[v].append((u,v))
        for p,es in inc.items():
            lpair=tuple(sorted(edge_to_line[tuple(sorted(e))] for e in es))
            R_rows[vi[(p,lpair)]] |= 1 << qi
            for f in v2f[(p,lpair)]: M_rows[si[f]] |= 1 << qi

    FM_rows=[]
    for rbits in F_rows:
        y=0; x=rbits
        while x:
            lsb=x & -x; idx=lsb.bit_length()-1
            y ^= M_rows[idx]; x ^= lsb
        FM_rows.append(y)

    rank_F=rank_gf2(F_rows); rank_M=rank_gf2(M_rows); rank_R=rank_gf2(R_rows); rank_FM=rank_gf2(FM_rows)
    assert rank_FM==0 and all(x==0 for x in FM_rows)
    H2=1620-rank_M
    H1=(320-rank_F)-rank_M
    H0=240-rank_F
    assert (rank_F,rank_M,rank_R,H2,H1,H0)==(160,120,200,1500,40,80)

    results={
        'theorem':'BT525 Mod-2 Cl8 Parity Homology Theorem',
        'complex':'F2^1620 --M--> F2^320 --F--> F2^240',
        'chain_condition':'F M = 0 over F2 because integer F M = 4 R',
        'ranks_over_F2':{'rank_M':rank_M,'rank_F':rank_F,'rank_R':rank_R,'rank_FM':rank_FM},
        'homology_dimensions':{'H2_ker_M':H2,'H1_kerF_mod_imM':H1,'H0_coker_F':H0},
        'interpretation':{'H1_40':'the parity-protected first homology is exactly one W33 point/line carrier','H0_80':'two W33 carriers survive as fold cokernel','H2_1500':'large quadrangle parity-cycle reservoir'},
        'substrate_reading':{'40':'mod-2 protected W33 carrier','80':'two 40-carrier parity boundary residues','120':'rank of M over F2 equals E8 root-pair count','160':'ker F over F2 and signed/projective rank scale'}
    }
    out=Path('data/PART_BT525_MOD2_CL8_PARITY_HOMOLOGY_results.json')
    out.parent.mkdir(exist_ok=True); out.write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results,indent=2)); return results
if __name__=='__main__': main()
