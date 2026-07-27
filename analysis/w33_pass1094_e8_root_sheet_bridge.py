from __future__ import annotations
import json,math,time
from collections import deque
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass1094_e8_root_sheet_bridge.json'

ATLAS=[
('1A','(cdcdcddcdcdddcdd)^4',1,51840),('2A','(cdd)^4',2,1152),('2B','(cdcdcddcdcdddcdd)^2',2,192),('3A','(cdcdd)^4',3,648),('3C','(ccdcdddcddd)^2',3,216),('3D','(cddcdcdddcdd)^2',3,108),('4A','(cdd)^2',4,96),('4B','cdcdcddcdcdddcdd',4,16),('5A','(cd)^2',5,10),('6A','(cdcdd)^2',6,72),('6C','ccdcdddcddd',6,36),('6E','cddcdcdddcdd',6,36),('6F','(cdcdcdd)^2',6,24),('9A','d',9,9),('12A','cdcdd',12,12),('2C','(ccdcdcddcdcdddcddcddcdcdddcdd)^3',2,1440),('2D','(cdcdddcdd)^3',2,96),('4C','(cdcdcdd)^3',4,96),('4D','dcdcdcdd',4,32),('6G','ccdcdcddcdcdddcddcddcdcdddcdd',6,36),('6H','dcdd',6,36),('6I','cdcdddcdd',6,12),('8A','cdd',8,8),('10A','cd',10,10),('12C','cdcdcdd',12,12)]

def roots_e8():
    roots=[]
    for i in range(8):
      for j in range(i+1,8):
       for si in [1,-1]:
        for sj in [1,-1]:
         v=[0]*8;v[i]=2*si;v[j]=2*sj;roots.append(tuple(v))
    for m in range(256):
        v=tuple(-1 if (m>>k)&1 else 1 for k in range(8))
        if sum(x==-1 for x in v)%2==0:roots.append(v)
    return roots

def reflection_perm(r,roots,ridx):
    out=[]
    for x in roots:
        q=sum(a*b for a,b in zip(x,r))//4
        y=tuple(a-q*b for a,b in zip(x,r));out.append(ridx[y])
    return np.array(out,dtype=np.uint8)
def compose(a,b):return a[b]
def invperm(p):
    q=np.empty_like(p);q[p]=np.arange(len(p),dtype=p.dtype);return q
def order(p):
    seen=np.zeros(len(p),dtype=bool);o=1
    for i in range(len(p)):
        if not seen[i]:
            j=i;l=0
            while not seen[j]:seen[j]=True;j=int(p[j]);l+=1
            o=math.lcm(o,l)
    return o
def enum_group(gens):
    I=np.arange(len(gens[0]),dtype=np.uint8);keys={I.tobytes():0};elems=[I];parity=[0];q=deque([0])
    while q:
        xi=q.popleft();x=elems[xi]
        for g in gens:
            y=compose(g,x);k=y.tobytes()
            if k not in keys:keys[k]=len(elems);elems.append(y.copy());parity.append(parity[xi]^1);q.append(len(elems)-1)
    return np.stack(elems),keys,np.array(parity,dtype=np.uint8)
def classes(arr,index,gens):
    trs=[]
    for g in gens:
        gi=invperm(g);C=gi[arr[:,g]]
        trs.append(np.array([index[row.tobytes()] for row in C],dtype=np.int32))
    unseen=np.ones(len(arr),dtype=bool);out=[];class_of=np.empty(len(arr),dtype=np.int16)
    for seed in range(len(arr)):
        if not unseen[seed]:continue
        unseen[seed]=False;q=deque([seed]);orb=[]
        while q:
            x=q.popleft();orb.append(x)
            for tr in trs:
                y=int(tr[x])
                if unseen[y]:unseen[y]=False;q.append(y)
        ci=len(out);class_of[orb]=ci;out.append(orb)
    return out,class_of
def ppower(p,n):
    r=np.arange(len(p),dtype=np.uint8);b=p
    while n:
        if n&1:r=compose(r,b)
        b=compose(b,b);n//=2
    return r
def eval_word(expr,c,d):
    if expr.startswith('('):w,n=expr[1:].split(')^');n=int(n)
    else:w=expr;n=1
    r=np.arange(len(c),dtype=np.uint8)
    for ch in w:r=compose(r,c if ch=='c' else d)
    return ppower(r,n)
def gen_size(gens,limit=51840):
    I=np.arange(len(gens[0]),dtype=np.uint8);seen={I.tobytes()};q=deque([I])
    while q:
        x=q.popleft()
        for g in gens:
            y=compose(g,x);k=y.tobytes()
            if k not in seen:seen.add(k);q.append(y)
    return len(seen)

def main():
    started=time.time();roots=roots_e8();ridx={r:i for i,r in enumerate(roots)};assert len(roots)==240
    simples=[(1,-1,-1,-1,-1,-1,-1,1),(2,2,0,0,0,0,0,0),(-2,2,0,0,0,0,0,0),(0,-2,2,0,0,0,0,0),(0,0,-2,2,0,0,0,0),(0,0,0,-2,2,0,0,0)]
    gens=[reflection_perm(r,roots,ridx) for r in simples]
    G,index,parity=enum_group(gens);assert len(G)==51840
    cls,class_of=classes(G,index,gens);assert len(cls)==25
    rec=[]
    for ci,c in enumerate(cls):
        rep=G[c[0]];rec.append({'ci':ci,'size':len(c),'centralizer':51840//len(c),'order':order(rep),'inner':not bool(parity[c[0]])})
    cci=next(r['ci'] for r in rec if not r['inner'] and r['order']==2 and r['centralizer']==1440)
    dci=next(r['ci'] for r in rec if r['inner'] and r['order']==9 and r['centralizer']==9)
    c=G[cls[cci][0]];d=None
    for ii in cls[dci]:
        z=G[ii]
        if order(compose(c,z))!=10:continue
        ok=True
        for name,w,o,cent in [ATLAS[0],ATLAS[1],ATLAS[3],ATLAS[7],ATLAS[22],ATLAS[24]]:
            x=eval_word(w,c,z);rr=rec[int(class_of[index[x.tobytes()]])]
            if rr['order']!=o or rr['centralizer']!=cent:ok=False;break
        if ok and gen_size([c,z])==51840:d=z;break
    assert d is not None
    rows=[];fixed=[];fixed_lines=[];seen=set();neg=[ridx[tuple(-x for x in r)] for r in roots]
    for name,w,o,cent in ATLAS:
        x=eval_word(w,c,d);ci=int(class_of[index[x.tobytes()]]);rr=rec[ci]
        assert rr['order']==o and rr['centralizer']==cent;seen.add(ci)
        f=int(np.sum(x==np.arange(240,dtype=np.uint8)))
        fl=sum(1 for i in range(240) if i<neg[i] and int(x[i]) in (i,neg[i]))
        fixed.append(f);fixed_lines.append(fl);rows.append({'name':name,'class_size':51840//cent,'fixed_roots':f,'fixed_antipodal_lines':fl,'inner':rr['inner']})
    assert len(seen)==25
    char=json.loads((ROOT/'data'/'w33_pass1092_u42dot2_character_identification.json').read_text());chars=char['characters'];sizes=[r['class_size'] for r in rows]
    root_ips={k:sum(s*a*b for s,a,b in zip(sizes,fixed,v['values']))//51840 for k,v in chars.items()}
    line_ips={k:sum(s*a*b for s,a,b in zip(sizes,fixed_lines,v['values']))//51840 for k,v in chars.items()}
    unseen=set(range(240));orbits=[]
    while unseen:
        s=min(unseen);orb={int(g[s]) for g in G};orbits.append(sorted(orb));unseen-=orb
    profile=sorted(map(len,orbits))
    checks={'E8_roots240':len(roots)==240,'WE6_order51840':len(G)==51840,'twentyfive_classes':len(cls)==25,'ATLAS_standard_pair_found':d is not None,'all_ATLAS_classes_identified':len(seen)==25,'WE6_root_orbits_match_pass1020':profile==[1]*6+[27]*6+[72],'root_character_degree240':fixed[0]==240,'root_line_character_degree120':fixed_lines[0]==120,'St_plus_absent_from_roots':root_ips['81_plus']==0,'St_minus_absent_from_roots':root_ips['81_minus']==0,'St_plus_absent_from_root_lines':line_ips['81_plus']==0,'St_minus_absent_from_root_lines':line_ips['81_minus']==0}
    assert all(checks.values()),(checks,root_ips,line_ips,profile)
    out={'schema':'w33.pass1094.e8_root_sheet_bridge.v1','status':'PASS','headline':'The proposed bridge from the frame-kernel Steinberg modules 81_plus and 81_minus to the signed E8 root sheets is obstructed exactly. The faithful W(E6)=U4(2):2 action on the 240 E8 roots and on the 120 antipodal root lines contains neither 81_plus nor 81_minus: both character inner products are zero. Therefore every U4(2):2-equivariant linear map from either Steinberg copy to these root permutation modules is zero.','root_action':{'degree':240,'orbit_profile':profile,'character_ATLAS_order':fixed,'known_pass1020_profile':[1]*6+[27]*6+[72]},'antipodal_root_line_action':{'degree':120,'character_ATLAS_order':fixed_lines},'constituent_inner_products':{'roots240':root_ips,'root_lines120':line_ips},'decision':{'equivariant_bridge_exists':False,'reason':'Hom_G(81_plus,C[roots])=Hom_G(81_minus,C[roots])=0, and likewise for antipodal root lines.','important_group_boundary':'The transitive signed-root action belongs to Sp(4,3)=2.U4(2), whereas 81_plus/minus are modules of U4(2):2=W(E6). The faithful W(E6) restriction is intransitive and still has zero Steinberg multiplicity.'},'check_count':len(checks),'checks':checks,'seconds':time.time()-started,'scope':'Exact E8 root permutations from six Bourbaki E6 reflections, exact ATLAS class identification, and exact character inner products.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','checks':len(checks),'profile':profile,'root_81':{k:root_ips[k] for k in ['81_plus','81_minus']},'line_81':{k:line_ips[k] for k in ['81_plus','81_minus']},'seconds':round(time.time()-started,3)},indent=2))
if __name__=='__main__':main()
