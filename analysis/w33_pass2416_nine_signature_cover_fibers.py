#!/usr/bin/env python3
"""Pass 2416: exact cardinalities and literal witnesses for nine signature fibers."""
from __future__ import annotations
import itertools, collections, json, hashlib
import numpy as np
from pathlib import Path
Q=3

def normalize(v):
    w=tuple(int(x)%Q for x in v)
    for x in w:
        if x:
            z=pow(x,-1,Q); return tuple((z*y)%Q for y in w)
    raise ValueError

def symp(u,v):
    return (u[0]*v[3]-u[3]*v[0]+u[1]*v[2]-u[2]*v[1])%Q

def build_geom():
    points=sorted({normalize(v) for v in itertools.product(range(Q),repeat=4) if any(v)})
    pidx={p:i for i,p in enumerate(points)}
    A=np.zeros((40,40),dtype=np.int8)
    for i,u in enumerate(points):
        for j in range(i+1,40):
            if symp(u,points[j])==0: A[i,j]=A[j,i]=1
    line_sets=set()
    for i in range(40):
        for j in range(i+1,40):
            if not A[i,j]: continue
            u,v=points[i],points[j]; span=set()
            for a,b in itertools.product(range(3),repeat=2):
                w=tuple((a*u[k]+b*v[k])%3 for k in range(4))
                if any(w): span.add(pidx[normalize(w)])
            line_sets.add(tuple(sorted(span)))
    lines=sorted(line_sets); lidx={L:i for i,L in enumerate(lines)}
    edges=[(i,j) for i in range(40) for j in range(i+1,40) if A[i,j]]
    eidx={e:i for i,e in enumerate(edges)}
    frames=[]; match=[]
    for a,La in enumerate(lines):
        sa=set(La)
        for b in range(a+1,40):
            Lb=lines[b]
            if not sa.isdisjoint(Lb): continue
            m=[]
            for x in La:
                ys=[y for y in Lb if A[x,y]]; assert len(ys)==1
                m.append(eidx[tuple(sorted((x,ys[0])))])
            frames.append((a,b));match.append(tuple(sorted(m)))
    fidx={f:i for i,f in enumerate(frames)}
    M=np.zeros((540,240),dtype=np.int8)
    for i,m in enumerate(match): M[i,list(m)]=1
    octets=[];seen=set()
    for left in itertools.combinations(range(40),4):
        if any(A[a,b] for a,b in itertools.combinations(left,2)): continue
        right=tuple(v for v in range(40) if all(A[v,u] for u in left))
        if len(right)!=4 or any(A[a,b] for a,b in itertools.combinations(right,2)): continue
        key=tuple(sorted((tuple(left),tuple(right))))
        if key in seen: continue
        seen.add(key);octets.append((tuple(left),tuple(right)))
    oidx={tuple(sorted(o)):i for i,o in enumerate(octets)}
    return points,pidx,A,lines,lidx,edges,eidx,frames,fidx,M,octets,oidx

def trans(points,pidx,v):
    v=normalize(v);out=[]
    for x in points:
        c=symp(x,v);y=tuple((x[i]+c*v[i])%3 for i in range(4));out.append(pidx[normalize(y)])
    return tuple(out)

def perms_for_point_perm(p,lines,lidx,frames,fidx,octets,oidx):
    lp=tuple(lidx[tuple(sorted(p[x] for x in L))] for L in lines)
    fp=tuple(fidx[tuple(sorted((lp[a],lp[b])))] for a,b in frames)
    op=[]
    for left,right in octets:
        key=tuple(sorted((tuple(sorted(p[x] for x in left)),tuple(sorted(p[x] for x in right)))))
        op.append(oidx[key])
    return fp,tuple(op)

def pair_orbits(fgens,ogens):
    unseen=set(range(540*45)); out=[]
    while unseen:
        z=next(iter(unseen)); O={z}; q=collections.deque([z])
        while q:
            w=q.popleft(); f=w//45;o=w%45
            for fg,og in zip(fgens,ogens):
                zz=fg[f]*45+og[o]
                if zz not in O: O.add(zz); q.append(zz)
        unseen-=O;out.append(O)
    return sorted(out,key=len)

SIGNATURES=[[0,1,1,1,1,2,1,1,4,1,4,1,1,1,2,1,1,0,2,4,1,1,1,1,1,1,1,1,1,1,1,1,4,2,1,1,1,0,1,1,1,4,0,1,1],[0,1,1,1,1,2,1,1,4,1,4,1,1,1,2,1,1,0,2,4,1,1,1,1,1,1,1,1,1,1,1,1,4,2,1,1,1,0,1,1,1,4,0,1,1],[1,1,1,1,1,1,1,1,4,1,2,3,1,1,1,1,1,1,1,2,3,1,1,1,1,3,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,2,1,1,3],[0,1,1,1,1,2,1,1,4,1,4,1,1,1,2,1,1,0,2,4,1,1,1,1,1,1,1,1,1,1,1,1,4,2,1,1,1,0,1,1,1,4,0,1,1],[1,1,1,1,1,1,1,1,4,2,2,2,1,1,1,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,1,2,1,1,2,1,1,2],[0,1,1,1,1,3,1,1,3,1,3,1,1,1,3,1,1,0,3,3,1,1,1,1,1,1,1,1,1,1,1,1,3,3,1,1,1,0,1,1,1,4,0,1,1],[1,1,1,1,1,1,1,1,4,2,2,2,1,1,1,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,1,2,1,1,2,1,1,2],[1,1,1,1,1,1,1,1,4,1,2,3,1,1,1,1,1,1,1,2,3,1,1,1,1,3,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,2,1,1,3],[0,1,1,1,1,3,1,1,3,1,3,1,1,1,3,1,1,0,3,3,1,1,1,1,1,1,1,1,1,1,1,1,3,3,1,1,1,0,1,1,1,4,0,1,1]]
CLASS_LABELS=[0,0,2,0,3,1,3,2,1]
COVERS=[[9,14,15,20,29,32,34,66,77,79,92,96,110,113,124,152,155,169,177,184,187,195,211,213,224,257,260,269,277,289,299,303,313,320,325,327,330,362,364,370,371,373,376,382,410,416,424,426,431,438,440,457,461,479,489,494,502,527,529,538],[6,9,12,46,50,56,63,66,78,84,87,107,118,128,143,145,153,158,161,175,180,194,211,217,225,227,241,262,263,270,281,289,293,299,310,325,327,332,338,342,366,371,374,393,394,396,404,415,419,423,436,440,445,455,469,480,499,519,528,536],[2,13,24,30,37,54,62,73,77,95,96,106,126,132,147,149,160,162,164,167,189,206,208,218,224,228,236,249,260,261,265,291,293,297,301,323,326,329,345,349,362,365,366,377,385,398,424,426,431,437,451,456,464,477,485,494,508,516,521,537],[19,23,25,28,32,36,60,64,69,94,104,105,112,116,151,155,156,166,168,170,183,189,193,202,206,239,242,244,248,267,288,290,295,306,310,311,318,329,335,355,357,358,382,395,402,424,427,428,444,448,462,464,469,473,485,501,512,514,522,537],[2,10,27,35,44,50,52,57,67,74,97,103,123,125,128,130,134,137,144,170,172,183,186,188,196,209,217,221,223,247,252,259,277,287,290,294,297,309,320,328,342,355,376,381,393,427,435,441,453,455,457,462,475,478,503,510,512,518,519,537],[3,9,17,28,39,47,58,75,80,89,91,98,115,120,124,136,147,148,156,177,200,204,208,223,232,234,237,251,253,268,270,279,284,299,311,320,343,350,352,361,369,378,380,389,394,404,407,417,418,439,448,458,463,470,474,480,495,520,528,535],[18,21,24,28,31,35,63,66,69,99,103,105,109,113,117,145,149,169,173,177,181,184,188,190,235,238,242,249,256,260,262,266,272,298,323,328,330,338,345,361,365,366,372,385,389,410,417,419,430,433,448,453,474,477,481,494,505,514,520,536],[0,7,22,26,36,42,46,54,71,78,85,92,104,112,116,124,136,140,158,167,174,177,187,197,202,209,218,228,238,248,250,253,258,268,280,291,303,315,323,331,342,350,359,369,376,384,391,404,420,431,438,447,458,466,477,486,498,507,520,537],[4,8,15,20,33,43,54,57,68,72,86,94,101,111,121,127,137,139,156,167,176,184,193,201,210,218,226,239,248,251,258,269,278,287,296,307,316,325,334,343,352,361,370,379,388,397,406,415,424,433,442,451,460,469,478,487,496,505,514,523]]
CLASS_GLOBAL_COVERS={0:3149280,1:38880,2:233280,3:126360}
CLASS_SIGNATURE_ORBITS={0:270,1:135,2:270,3:45}
EXPECTED='22ad017b9bc29e99d5c1baac68197777473327267769aba2039deadd6ccd34c3'
OUT=Path(__file__).resolve().parents[1]/'data'/'w33_pass2416_nine_signature_cover_fibers.json'

def csha(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def certificate():
    points,pidx,A,lines,lidx,edges,eidx,frames,fidx,M,octets,oidx=build_geom()
    pgens=[trans(points,pidx,v) for v in ((1,0,0,0),(0,1,0,0),(0,0,0,1),(1,0,1,0))]
    fgens=[];ogens=[]
    for p in pgens:
        f,o=perms_for_point_perm(p,lines,lidx,frames,fidx,octets,oidx);fgens.append(f);ogens.append(o)
    pair_orbit_list=pair_orbits(fgens,ogens)
    degree_one=next(O for O in pair_orbit_list if len(O)==540)
    R=np.zeros((540,45),dtype=np.int64)
    for z in degree_one:R[z//45,z%45]=1
    fiber_sizes=[CLASS_GLOBAL_COVERS[c]//CLASS_SIGNATURE_ORBITS[c] for c in CLASS_LABELS]
    records=[]
    for i,(sig,cov,cl,fs) in enumerate(zip(SIGNATURES,COVERS,CLASS_LABELS,fiber_sizes)):
        rec={'fiber_index':i,'class_label':cl,'exact_fiber_cardinality':fs,'cover_frames':cov,
             'cover_sha256':csha(cov),'signature':sig,'signature_sha256':csha(sig),
             'checks':{'sixty_distinct_frames':len(cov)==len(set(cov))==60,
                       'edge_exact_cover':np.array_equal(M[cov].sum(axis=0),np.ones(240,dtype=np.int64)),
                       'signature_exact':np.array_equal(R[cov].sum(axis=0),np.array(sig,dtype=np.int64))}}
        records.append(rec)
    overlap=[[len(set(COVERS[i])&set(COVERS[j])) for j in range(9)] for i in range(9)]
    checks={'w33_counts':M.shape==(540,240),'frame_rows_4':set(map(int,M.sum(axis=1)))=={4},
            'edge_columns_9':set(map(int,M.sum(axis=0)))=={9},
            'pair_orbit_sizes':list(map(len,pair_orbit_list))==[540,3240,3240,4320,12960],
            'degree_one_relation':set(map(int,R.sum(axis=1)))=={1} and set(map(int,R.sum(axis=0)))=={12},
            'nine_signatures_sum_uniformly':np.array_equal(np.sum(np.array(SIGNATURES),axis=0),np.full(45,12)),
            'all_nine_fibers_nonempty':all(all(z['checks'].values()) for z in records),
            'fiber_sizes_integral':all(CLASS_GLOBAL_COVERS[c]%CLASS_SIGNATURE_ORBITS[c]==0 for c in CLASS_LABELS),
            'selected_fiber_universe_42912':sum(fiber_sizes)==42912,
            'independent_witnesses_not_disjoint':any(overlap[i][j]>0 for i in range(9) for j in range(i))}
    d={'schema':'w33.pass2416.nine_signature_cover_fibers.v1','status':'PASS_NINE_FIBERS_NONEMPTY_WITH_EXACT_CARDINALITIES',
       'sources':{'complete_cover_certificate':'data/w33_pass1821_1825_complete_cover_signature.json',
                  'signature_capacity_certificate':'data/w33_pass2309_signature_capacity_feasibility.json',
                  'geometry_reconstruction':'literal PG(3,3), isotropic lines, frames, octets, and PSp transvections'},
       'relation':{'shape':[540,45],'pair_orbit_sizes':list(map(len,pair_orbit_list)),'frame_degree':1,'octet_degree':12,
                   'sha256':hashlib.sha256(R.astype(np.uint8).tobytes()).hexdigest()},
       'class_arithmetic':{str(c):{'global_covers':CLASS_GLOBAL_COVERS[c],'signature_orbit_size':CLASS_SIGNATURE_ORBITS[c],
                                   'covers_per_signature':CLASS_GLOBAL_COVERS[c]//CLASS_SIGNATURE_ORBITS[c]}
                           for c in sorted(CLASS_GLOBAL_COVERS)},
       'selected_fiber_count':9,'selected_fiber_total_cardinality':sum(fiber_sizes),'fibers':records,
       'independent_witness_overlap_matrix':overlap,'checks':checks,
       'theorem':'Each of the nine capacity-compatible signature types has a nonempty exact-cover fiber. By transitivity and the complete cover census, their exact cardinalities are 11,664, 864, 2,808, or 288 according to signature class; the selected nine fibers contain 42,912 covers in total.',
       'boundary':'The nine displayed cover witnesses are verified individually but overlap. Nonempty fibers and exact cardinalities do not imply a frame-disjoint nine-way transversal or chi(H)=9.'}
    assert all(checks.values()) and all(all(z['checks'].values()) for z in records)
    d['sha256_without_hash_field']=csha(d)
    return d

def main():
    d=certificate();assert d['sha256_without_hash_field']==EXPECTED
    assert d==json.loads(OUT.read_text())
    print(json.dumps({'status':d['status'],'certificate':EXPECTED,'fiber_total':42912},sort_keys=True))
if __name__=='__main__':main()
