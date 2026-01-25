#!/usr/bin/env python3
"""Reproduce v9 port-law stability under random Aut(W33) conjugation.

Assumes you have these bundles in /mnt/data:
- W33_N12_58_portlaw_rewrite_bundle_v7_20260112.zip  (for flip audit w/ matching indices)
- N12_58_snapshot_bundle_20260112.zip               (for 2T cycles)
- W33_N12_58_triad_alignment_bundle_20260112.zip    (for W33 line map + rays + candidate points)
- W33_validation_aut_group_bundle_20260112.zip      (for Aut(W33) generators)
- W33_N12_58_portlaw_stability_bundle_v8_20260112.zip (for reference stable law)

Outputs are written to the current directory.
"""
from __future__ import annotations
import math, random, json, zipfile, io
from itertools import combinations
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

# --- load bundles
ztri = Path('/mnt/data/W33_N12_58_triad_alignment_bundle_20260112.zip')
z7   = Path('/mnt/data/W33_N12_58_portlaw_rewrite_bundle_v7_20260112.zip')
zsnap= Path('/mnt/data/N12_58_snapshot_bundle_20260112.zip')
zaut = Path('/mnt/data/W33_validation_aut_group_bundle_20260112.zip')
z8   = Path('/mnt/data/W33_N12_58_portlaw_stability_bundle_v8_20260112.zip')

def read_csv_from_zip(zpath, inner):
    with zipfile.ZipFile(zpath,'r') as zf:
        return pd.read_csv(io.BytesIO(zf.read(inner)))

# W33 lines + rays + candidate points
w33 = read_csv_from_zip(ztri,'inputs/W33_line_phase_map.csv')
rays= read_csv_from_zip(ztri,'inputs/W33_point_rays_C4_complex.csv')
df_cp = read_csv_from_zip(ztri,'inputs/n12_58_candidate_w33_points_40_from_tau_cycles_and_fixed_complements_20260109t134000z.csv')

# cycles and audit
cyc = read_csv_from_zip(zsnap,'_n12/n12_58_2t_holonomy_nontrivial_cycles.csv')
audit = read_csv_from_zip(z7,'W33_N12_58_portlaw_rewrite_bundle_v7/n12_58_flip_delta_audit_with_matching_indices.csv')

# stable reference law
stable = read_csv_from_zip(z8,'portlaw_stability_v8/stable_port_law.csv')
ref={}
for r in stable.itertuples(index=False):
    key=(int(r.delta), int(r.rem_idx), int(r.add_idx))
    ref[key]=set(int(x) for x in str(r.allowed_ports).split())

# Aut generators
import os, subprocess, tempfile
tmp = Path('/tmp/_aut_extract')
tmp.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(zaut,'r') as zf:
    zf.extract('W33_automorphism_generators_sympy.json', path=tmp)
gen=json.loads((tmp/'W33_automorphism_generators_sympy.json').read_text())
gens=[np.array(g, dtype=np.int16) for g in gen['point_generators_array_form']]

def inv_perm(p):
    inv=np.empty_like(p)
    inv[p]=np.arange(len(p))
    return inv

def compose(p,q): # p∘q
    return p[q]

rng = random.Random(7)
def random_aut(word_len=30):
    p=np.arange(40, dtype=np.int16)
    for _ in range(word_len):
        g=rng.choice(gens)
        if rng.random()<0.5:
            p=compose(g,p)
        else:
            p=compose(inv_perm(g),p)
    return p

def conjugate_mapping(mapping, p):
    p_inv=inv_perm(p)
    return {i: mapping[int(p_inv[i])] for i in range(40)}

# --- build W33 collinearity
lines=[tuple(map(int,s.split())) for s in w33['point_ids'].astype(str)]
col=[set() for _ in range(40)]
for L in lines:
    for i in range(4):
        for j in range(i+1,4):
            a,b=L[i],L[j]
            col[a].add(b); col[b].add(a)

# --- four-center triads
triads=[]
for a,b,c in combinations(range(40),3):
    if (b in col[a]) or (c in col[a]) or (c in col[b]): continue
    if len(col[a] & col[b] & col[c])==4:
        triads.append((a,b,c))
triads=np.array(triads, dtype=np.int16)
assert triads.shape==(360,3)

# adjacency + self
pair_to_tri=defaultdict(list)
for i,(a,b,c) in enumerate(triads):
    for u,v in [(a,b),(a,c),(b,c)]:
        pair_to_tri[tuple(sorted((u,v)))].append(i)
adj=[set() for _ in range(360)]
for lst in pair_to_tri.values():
    if len(lst)>1:
        for i in lst:
            adj[i].update(j for j in lst if j!=i)
adj_self=[list(adj[i])+[i] for i in range(360)]

# --- rays to Z12 edge phases + triad holonomy
def parse_c(s): return complex(str(s).replace(' ',''))
V=np.zeros((40,4), dtype=np.complex128)
for _,r in rays.iterrows():
    p=int(r.point_id)
    V[p,0]=parse_c(r.v0); V[p,1]=parse_c(r.v1); V[p,2]=parse_c(r.v2); V[p,3]=parse_c(r.v3)

twopi=2*math.pi
def quant12(z):
    ang=math.atan2(z.imag, z.real)
    return int(round(12*ang/twopi))%12

edge_k={}
for p in range(40):
    for q in range(40):
        if p==q: continue
        if q in col[p]: continue
        edge_k[(p,q)]=quant12(np.vdot(V[p],V[q]))

triad_h=np.zeros(360, dtype=np.int8)
for i,(a,b,c) in enumerate(triads):
    triad_h[i]=(edge_k[(a,b)]+edge_k[(b,c)]+edge_k[(c,a)])%12
assert set(triad_h.tolist())=={3,9}

# --- N12 label masks
sym_map={**{str(i):i for i in range(10)}, 'a':10, 'b':11}
def tri_mask(tri):
    tri=str(tri).strip().strip(',')
    m=0
    for ch in tri:
        if ch in sym_map:
            m |= 1<<sym_map[ch]
    return m
def members_mask(members):
    m=0
    for t in str(members).split(','):
        t=t.strip()
        if t: m |= tri_mask(t)
    return m
label_to_mask={r.point_id: members_mask(r.members) for r in df_cp.itertuples(index=False)}

# --- audit dict
audit_key={}
for r in audit.itertuples(index=False):
    u=int(r.u); v=int(r.v)
    key=(u,v) if u<v else (v,u)
    sm=0
    for s in str(r.flip_support_4set).split():
        sm |= 1<<int(s)
    audit_key[key]=dict(delta=int(r.delta_from_nodes),
                        rem_idx=int(r.rem_idx), add_idx=int(r.add_idx),
                        rem_sum=int(r.removed_phase_sum_mod8), add_sum=int(r.added_phase_sum_mod8),
                        support_mask=sm)

# --- parse cycles
def parse_cycle_nodes(s):
    return [int(x) for x in str(s).split('-') if x.strip()]
cycles=[]
for r in cyc.itertuples(index=False):
    nodes=parse_cycle_nodes(r.cycle_nodes)
    L=int(r.length)
    edges=[]
    for i in range(L):
        u=nodes[i]; v=nodes[(i+1)%L]
        key=(u,v) if u<v else (v,u)
        e=audit_key[key].copy()
        edges.append(e)
    cycles.append(edges)

# --- port index between triads (matching on union 4-set)
def port_idx_between(t1, t2):
    if t1==t2: return -1
    s1=set(triads[t1].tolist()); s2=set(triads[t2].tolist())
    sym=list(s1 ^ s2)
    if len(sym)!=2: return None
    x,y=sorted(sym)
    u=sorted(list(s1|s2))
    p0,p1,p2,p3=u
    pair={x,y}
    if pair=={p0,p1} or pair=={p2,p3}: return 0
    if pair=={p0,p2} or pair=={p1,p3}: return 1
    if pair=={p0,p3} or pair=={p1,p2}: return 2
    return None

def derive_portlaw_feasible(mapping):
    mask_p=np.zeros(40, dtype=np.int32)
    for p in range(40):
        mask_p[p]=label_to_mask[mapping[p]]
    tri_mask=mask_p[triads[:,0]] | mask_p[triads[:,1]] | mask_p[triads[:,2]]
    law=defaultdict(set)
    for edges in cycles:
        L=len(edges)
        eligible=[]
        for e in edges:
            ok=(tri_mask & e['support_mask'])==e['support_mask']
            if e['delta']==2: ok &= (triad_h==9)
            elif e['delta']==6: ok &= (triad_h==3)
            eligible.append(ok)
        if any(not np.any(ok) for ok in eligible):
            return None
        for i,e in enumerate(edges):
            next_i=(i+1)%L
            ok_from=np.where(eligible[i])[0]
            ok_to=eligible[next_i]
            dprev=e['delta']; rs=e['rem_sum']; ads=e['add_sum']
            key=(e['delta'], e['rem_idx'], e['add_idx'])
            for tp in ok_from:
                holp=int(triad_h[tp])
                for tc in adj_self[tp]:
                    if not ok_to[tc]: continue
                    holc=int(triad_h[tc])
                    if dprev==0 and holc!=holp: continue
                    if dprev==4 and holc==holp: continue
                    if dprev==0 and rs==ads==0 and holc!=9: continue
                    if dprev==0 and rs==ads==4 and holc!=3: continue
                    if dprev==4 and (rs,ads)==(6,2) and not (holp==3 and holc==9): continue
                    law[key].add(port_idx_between(tp,tc))
    return law

def load_some_mappings():
    out=[]
    for zp in Path('/mnt/data').glob('*.zip'):
        try:
            with zipfile.ZipFile(zp) as zf:
                for n in zf.namelist():
                    if n.lower().endswith('w33_to_n12_mapping.csv') or n.lower().endswith('best_w33_to_n12_mapping.csv'):
                        try:
                            df=pd.read_csv(io.BytesIO(zf.read(n)))
                            wcol=df.columns[0]; ncol=df.columns[1]
                            if 'w33' in df.columns[0].lower():
                                wcol=df.columns[[c.lower() for c in df.columns].index('w33_point')]
                                ncol=df.columns[[c.lower() for c in df.columns].index('n12_point')]
                            m={int(w): str(x) for w,x in zip(df[wcol], df[ncol])}
                            if set(m.keys())==set(range(40)):
                                out.append((f'{zp.name}::{n}', m))
                        except Exception:
                            pass
        except zipfile.BadZipFile:
            pass
    # de-dup by mapping string
    seen=set()
    uniq=[]
    for tag,m in out:
        key=tuple(m[i] for i in range(40))
        if key not in seen:
            seen.add(key); uniq.append((tag,m))
    return uniq[:10]

mappings = load_some_mappings()
rows=[]
for tag,m in mappings:
    law=derive_portlaw_feasible(m)
    ok=(law is not None) and all(law.get(k,set())==v for k,v in ref.items())
    rows.append({'mapping':tag,'variant':'base','match':int(ok)})
    for j in range(5):
        p=random_aut(30)
        mg=conjugate_mapping(m,p)
        lawg=derive_portlaw_feasible(mg)
        okg=(lawg is not None) and all(lawg.get(k,set())==v for k,v in ref.items())
        rows.append({'mapping':tag,'variant':f'aut{j+1}','match':int(okg)})
pd.DataFrame(rows).to_csv('aut_conjugate_law_match_check.csv', index=False)
stable.to_csv('stable_port_law.csv', index=False)
from utils.json_safe import dump_json
summary_file = 'summary.json'
dump_json({'tested':len(rows),'all_matched':all(r['match'] for r in rows)}, summary_file, indent=2)
print('Wrote aut_conjugate_law_match_check.csv, stable_port_law.csv, summary.json')
