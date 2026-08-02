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

SIGNATURE_STRINGS=['111111141024111111111240111402111111111111024','111111402141111111112011141110411121114211101','111113121211311111113112111121131111111111411','111141111111024111111402111111111024240111111','112211121211112211211112112141111111112211211','113110113311110131141111111113011311311113110','141111111111111222111222111111222111111222111','211311111111311211111111411113111121111131112','311113101101131113311011113110113311111111141']
COVER_MASK_HEX=['402800000404200800022000140850104000000412c1400000004a1020088020020201200000001002800080902020009000000100240011000a004000000052010c200','10100800008000100200080211000888010160000484000004410a000400822020040c00002000a02080004001080024202800100400800009040048104400000001240','200021010004020200101080020850000004002020064002200024800002228000002300200101104014000200000950028001040000401800022004040002041002004','200040500200020022140011000190000040800400000680000820040c40085000008000114800000004402208005401880000000110300400000211000001112880000','20000c140800000480042a002080800000002002100000800400101002002448020000810800000a2020010148014000001024528000082000004080214100808000404','0810100000080010440840100800006009004201402020140800001008008001080500028002500800111000002000010180100110800040a0108000400808010020208','008001201002200240000210002400a04000022001062000204050800000400000104510204480000000000512222000022000000222288000000248000000891240000','802200120003000200010184040000008046000528004802004804000128000414000008040082008004400008080000000408408801400021040900000001020501001','008801000803000300001008140080a40600010880400000c0001000000440000c030000808100500640008000012202020100000208880200020004048200040000284']
CLASS_LABELS=[0,0,2,0,3,1,3,2,1]
CLASS_GLOBAL_COVERS={0:3149280,1:38880,2:233280,3:126360}
CLASS_SIGNATURE_ORBITS={0:270,1:135,2:270,3:45}
EXPECTED='2408fdd9a60f285907b1d33b7d66b29a4454ffe90260cf9a077585a561bac4ea'
OUT=Path(__file__).resolve().parents[1]/'data'/'w33_pass2416_nine_signature_cover_fibers.json'

def csha(x): return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def decode_signature(s): assert len(s)==45; return [int(x) for x in s]
def decode_cover(h):
    m=int(h,16);return [i for i in range(540) if (m>>i)&1]

def certificate():
    signatures=[decode_signature(s) for s in SIGNATURE_STRINGS];covers=[decode_cover(h) for h in COVER_MASK_HEX]
    points,pidx,A,lines,lidx,edges,eidx,frames,fidx,M,octets,oidx=build_geom()
    pgens=[trans(points,pidx,v) for v in ((1,0,0,0),(0,1,0,0),(0,0,0,1),(1,0,1,0))]
    fgens=[];ogens=[]
    for p in pgens:
        f,o=perms_for_point_perm(p,lines,lidx,frames,fidx,octets,oidx);fgens.append(f);ogens.append(o)
    po=pair_orbits(fgens,ogens);degree_one=next(O for O in po if len(O)==540)
    R=np.zeros((540,45),dtype=np.int64)
    for z in degree_one:R[z//45,z%45]=1
    fs=[CLASS_GLOBAL_COVERS[c]//CLASS_SIGNATURE_ORBITS[c] for c in CLASS_LABELS]
    fibers=[]
    for i,(ss,h,sig,cov,cl,n) in enumerate(zip(SIGNATURE_STRINGS,COVER_MASK_HEX,signatures,covers,CLASS_LABELS,fs)):
        fibers.append({'fiber_index':i,'class_label':cl,'exact_fiber_cardinality':n,'signature_string':ss,
                       'cover_mask_hex':h,'cover_frame_count':len(cov),'cover_sha256':csha(cov),
                       'checks':{'sixty_distinct_frames':len(cov)==len(set(cov))==60,
                                 'edge_exact_cover':np.array_equal(M[cov].sum(0),np.ones(240,dtype=np.int64)),
                                 'signature_exact':np.array_equal(R[cov].sum(0),np.array(sig,dtype=np.int64))}})
    overlap=[[len(set(covers[i])&set(covers[j])) for j in range(9)] for i in range(9)]
    checks={'w33_counts':M.shape==(540,240),'frame_rows_4':set(map(int,M.sum(1)))=={4},
            'edge_columns_9':set(map(int,M.sum(0)))=={9},
            'pair_orbit_sizes':list(map(len,po))==[540,3240,3240,4320,12960],
            'degree_one_relation':set(map(int,R.sum(1)))=={1} and set(map(int,R.sum(0)))=={12},
            'nine_signatures_sum_uniformly':np.array_equal(np.sum(np.array(signatures),axis=0),np.full(45,12)),
            'all_nine_fibers_nonempty':all(all(x['checks'].values()) for x in fibers),
            'fiber_sizes_integral':all(CLASS_GLOBAL_COVERS[c]%CLASS_SIGNATURE_ORBITS[c]==0 for c in CLASS_LABELS),
            'selected_fiber_universe_42912':sum(fs)==42912,
            'independent_witnesses_not_disjoint':any(overlap[i][j]>0 for i in range(9) for j in range(i))}
    d={'schema':'w33.pass2416.nine_signature_cover_fibers.v2','status':'PASS_NINE_FIBERS_NONEMPTY_WITH_EXACT_CARDINALITIES',
       'sources':{'complete_cover_certificate':'data/w33_pass1821_1825_complete_cover_signature.json',
                  'signature_capacity_certificate':'data/w33_pass2309_signature_capacity_feasibility.json',
                  'geometry_reconstruction':'literal PG(3,3), isotropic lines, frames, octets, and PSp transvections'},
       'relation':{'shape':[540,45],'pair_orbit_sizes':list(map(len,po)),'frame_degree':1,'octet_degree':12,
                   'sha256':hashlib.sha256(R.astype(np.uint8).tobytes()).hexdigest()},
       'class_arithmetic':{str(c):{'global_covers':CLASS_GLOBAL_COVERS[c],
                                   'signature_orbit_size':CLASS_SIGNATURE_ORBITS[c],
                                   'covers_per_signature':CLASS_GLOBAL_COVERS[c]//CLASS_SIGNATURE_ORBITS[c]}
                           for c in sorted(CLASS_GLOBAL_COVERS)},
       'selected_fiber_count':9,'selected_fiber_total_cardinality':sum(fs),'fibers':fibers,
       'independent_witness_overlap_matrix':overlap,'checks':checks,
       'theorem':'Each of the nine capacity-compatible signature types has a nonempty exact-cover fiber. By transitivity and the complete cover census, their exact cardinalities are 11,664, 864, 2,808, or 288 according to signature class; the selected nine fibers contain 42,912 covers in total.',
       'boundary':'The nine displayed cover witnesses are verified individually but overlap. Nonempty fibers and exact cardinalities do not imply a frame-disjoint nine-way transversal or chi(H)=9.'}
    assert all(checks.values()) and all(all(x['checks'].values()) for x in fibers)
    d['sha256_without_hash_field']=csha(d);return d

def main():
    d=certificate();assert d['sha256_without_hash_field']==EXPECTED
    assert d==json.loads(OUT.read_text())
    print(json.dumps({'status':d['status'],'certificate':EXPECTED,'fiber_total':42912},sort_keys=True))
if __name__=='__main__':main()
