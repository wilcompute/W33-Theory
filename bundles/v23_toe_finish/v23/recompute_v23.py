#!/usr/bin/env python3
import zipfile, pandas as pd, itertools, re, json, collections
from pathlib import Path

def parse_perm(s):
    nums=[int(x) for x in re.findall(r'\d+', str(s))]
    if len(nums)!=3:
        raise ValueError(s)
    return tuple(nums)

def comp(p,q):  # p∘q for image-form permutations
    return tuple(p[i] for i in q)

def perm_cycles(p):
    n=len(p); seen=[False]*n; cycles=[]
    for i in range(n):
        if seen[i]: continue
        j=i; cyc=[]
        while not seen[j]:
            seen[j]=True; cyc.append(j); j=p[j]
        cycles.append(cyc)
    return cycles

def cycle_type(p):
    lens=[len(c) for c in perm_cycles(p)]
    return tuple(sorted(lens, reverse=True))

def build():
    root=Path('.')
    v17zip=root/'W33_Q45_global_S3_connection_triangle_holonomy_bundle_v17_20260113.zip'
    v13zip=root/'W33_center_quad_GQ42_reconstruction_bundle_v13_20260112.zip'
    out=root/'out_v23'
    out.mkdir(exist_ok=True)
    tmp=root/'_tmp_v23'
    tmp.mkdir(exist_ok=True)

    with zipfile.ZipFile(v17zip,'r') as z:
        z.extractall(tmp/'v17')
    edges=pd.read_csv(tmp/'v17/v17/quotient_Q_edges_with_S3_transport.csv')
    tris=pd.read_csv(tmp/'v17/v17/Q_triangles_S3_holonomy_startsheet0.csv')

    with zipfile.ZipFile(v13zip,'r') as z:
        z.extractall(tmp/'v13')
    lines_df=pd.read_csv(tmp/'v13/center_quad_gq42_v13/gq42_lines_points.csv')
    lines=[tuple(map(int,str(s).split())) for s in lines_df.points]
    Hnbr=[set() for _ in range(45)]
    for L in lines:
        for a,b in itertools.combinations(L,2):
            Hnbr[a].add(b); Hnbr[b].add(a)
    def centers_count(u,v,w):
        return len(Hnbr[u] & Hnbr[v] & Hnbr[w])

    edge_map={}
    for r in edges.itertuples(index=False):
        u=int(r.u); v=int(r.v); w=int(r.z2_voltage)
        pu0=parse_perm(r.perm_u0_to_v); pu1=parse_perm(r.perm_u1_to_v)
        pv0=parse_perm(r.perm_v0_to_u); pv1=parse_perm(r.perm_v1_to_u)
        edge_map[(u,v)] = (w, pu0, pu1)
        edge_map[(v,u)] = (w, pv0, pv1)

    def step(u,v,s,p):
        w,perm0,perm1=edge_map[(u,v)]
        perm=perm0 if s==0 else perm1
        return s^w, perm[p]

    def edge_S6_perm(u,v):
        img=[]
        for s in [0,1]:
            for p in [0,1,2]:
                s2,p2=step(u,v,s,p)
                img.append(3*s2+p2)
        return tuple(img)

    def tri_hol6(u,v,w):
        return comp(edge_S6_perm(w,u), comp(edge_S6_perm(v,w), edge_S6_perm(u,v)))

    rows=[]
    for r in tris.itertuples(index=False):
        u,v,w=int(r.u),int(r.v),int(r.w)
        H6=tri_hol6(u,v,w)
        rows.append({
            'u':u,'v':v,'w':w,
            'centers':centers_count(u,v,w),
            'z2_parity':int(r.z2_triangle_parity),
            'fiber6_cycle_type':'+'.join(map(str,cycle_type(H6))),
            'fiber6_perm':str(H6),
            's3_holonomy_startsheet0':r.holonomy_perm,
            's3_type_startsheet0':r.holonomy_type,
        })
    df=pd.DataFrame(rows)
    df.to_csv(out/'Q_triangles_core.csv', index=False)

    counts=collections.Counter((int(x.centers),int(x.z2_parity),x.fiber6_cycle_type) for x in df.itertuples(index=False))
    with open(out/'counts.json','w') as f:
        json.dump({str(k):int(v) for k,v in counts.items()},f,indent=2)

if __name__=='__main__':
    build()
