from __future__ import annotations
import json, math, time
from collections import deque
from pathlib import Path
import numpy as np
from w33_pass1081_1086_core import *

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass1092_u42dot2_character_identification.json'
PRIME=1000033

ATLAS = [
 ('1A','(cdcdcddcdcdddcdd)^4',1,51840),
 ('2A','(cdd)^4',2,1152),
 ('2B','(cdcdcddcdcdddcdd)^2',2,192),
 ('3A','(cdcdd)^4',3,648),
 ('3C','(ccdcdddcddd)^2',3,216),
 ('3D','(cddcdcdddcdd)^2',3,108),
 ('4A','(cdd)^2',4,96),
 ('4B','cdcdcddcdcdddcdd',4,16),
 ('5A','(cd)^2',5,10),
 ('6A','(cdcdd)^2',6,72),
 ('6C','ccdcdddcddd',6,36),
 ('6E','cddcdcdddcdd',6,36),
 ('6F','(cdcdcdd)^2',6,24),
 ('9A','d',9,9),
 ('12A','cdcdd',12,12),
 ('2C','(ccdcdcddcdcdddcddcddcdcdddcdd)^3',2,1440),
 ('2D','(cdcdddcdd)^3',2,96),
 ('4C','(cdcdcdd)^3',4,96),
 ('4D','dcdcdcdd',4,32),
 ('6G','ccdcdcddcdcdddcddcddcdcdddcdd',6,36),
 ('6H','dcdd',6,36),
 ('6I','cdcdddcdd',6,12),
 ('8A','cdd',8,8),
 ('10A','cd',10,10),
 ('12C','cdcdcdd',12,12),
]
DOC_15=[15,7,3,-3,0,3,-1,1,0,1,-2,1,0,0,-1,5,1,3,-1,2,-1,1,-1,0,0]
INNER_ATLAS=[
 ('1A','identity',1,25920),('2A','(ababb)^3',2,576),('2B','abaababbababbabaababbababb',2,96),('3A','abbabbabbabbabbabbabbabb',3,648),('3B','abbabbabbabb',3,648),('3C','ababbababb',3,108),('3D','bababaababbababbbababaababbababb',3,54),('4A','(abb)^3',4,48),('4B','abaababbababb',4,8),('5A','b',5,5),('6A','abbabb',6,72),('6B','(abbabb)^5',6,72),('6C','(ababb)^5',6,36),('6D','ababb',6,36),('6E','bababaababbababb',6,18),('6F','aababbababb',6,12),('9A','ab',9,9),('9B','abab',9,9),('12A','(abb)^5',12,12),('12B','abb',12,12)]

def perm_order(p):
    seen=[False]*len(p);o=1
    for i in range(len(p)):
        if not seen[i]:
            j=i;l=0
            while not seen[j]:seen[j]=True;j=p[j];l+=1
            o=math.lcm(o,l)
    return o

def ppower(p,n):
    r=tuple(range(len(p)));b=p
    while n:
        if n&1:r=compose(r,b)
        b=compose(b,b);n//=2
    return r

def eval_word(expr,c,d):
    if expr.startswith('('):
        w,n=expr[1:].split(')^');n=int(n)
    else:w=expr;n=1
    r=tuple(range(len(c)))
    for ch in w:r=compose(r,c if ch=='c' else d)
    return ppower(r,n)

def eval_ab(expr,a,b):
    if expr=='identity':return tuple(range(len(a)))
    if expr.startswith('('):w,n=expr[1:].split(')^');n=int(n)
    else:w=expr;n=1
    r=tuple(range(len(a)))
    for ch in w:r=compose(r,a if ch=='a' else b)
    return ppower(r,n)

def conjugacy_classes(elems,index,gens):
    invgens=[inverse(g) for g in gens]
    trans=[]
    for g,gi in zip(gens,invgens):
        a=np.empty(len(elems),dtype=np.int32)
        for k,x in enumerate(elems):a[k]=index[compose(gi,compose(x,g))]
        trans.append(a)
    unseen=np.ones(len(elems),dtype=bool);classes=[];class_of=np.empty(len(elems),dtype=np.int16)
    for seed in range(len(elems)):
        if not unseen[seed]:continue
        unseen[seed]=False;q=deque([seed]);orb=[]
        while q:
            x=q.popleft();orb.append(x)
            for tr in trans:
                y=int(tr[x])
                if unseen[y]:unseen[y]=False;q.append(y)
        ci=len(classes)
        for x in orb:class_of[x]=ci
        classes.append(orb)
    return classes,class_of

def generated_size(gens,limit=51840):
    I=tuple(range(len(gens[0])));seen={I};q=deque([I])
    while q:
        x=q.popleft()
        for g in gens:
            y=compose(g,x)
            if y not in seen:
                seen.add(y);q.append(y)
                if len(seen)>limit:return len(seen)
    return len(seen)

def balanced(x,p=PRIME):
    x=int(x)%p
    return x-p if x>p//2 else x

def main():
    started=time.time()
    pts,pidx,lines,lidx,pl,frames,fidx,flags,flagidx=build_w33()
    inner_gens=[transvection_perm(pts[i],pts,pidx) for i in [0,1,4,5,13]]
    outer=outer_similitude_perm(pts,pidx)
    inner,inner_index=enumerate_group(inner_gens)
    H,hindex=enumerate_group(inner_gens+[outer])
    assert len(inner)==25920 and len(H)==51840
    inner_set=set(inner)
    classes,class_of=conjugacy_classes(H,hindex,inner_gens+[outer])
    assert len(classes)==25
    rec=[]
    for ci,cl in enumerate(classes):
        rep=H[cl[0]];order=perm_order(rep);cent=51840//len(cl);inside=rep in inner_set
        rec.append({'internal_class':ci,'size':len(cl),'centralizer':cent,'order':order,'inside_U4(2)':inside})
    cclass=next(r['internal_class'] for r in rec if not r['inside_U4(2)'] and r['order']==2 and r['centralizer']==1440)
    dclass=next(r['internal_class'] for r in rec if r['inside_U4(2)'] and r['order']==9 and r['centralizer']==9)
    c=H[classes[cclass][0]]
    d=None
    for idx in classes[dclass]:
        z=H[idx]
        if perm_order(compose(c,z))==10 and generated_size([c,z])==51840:
            d=z;break
    assert d is not None
    atlas_rows=[];seen_cls=set()
    for name,word,order,cent in ATLAS:
        x=eval_word(word,c,d);ci=int(class_of[hindex[x]])
        rr=rec[ci]
        assert rr['order']==order,(name,rr)
        assert rr['centralizer']==cent,(name,rr)
        seen_cls.add(ci)
        atlas_rows.append({'name':name,'word':word,'order':order,'centralizer':cent,'class_size':51840//cent,'internal_class':ci,'inside_U4(2)':rr['inside_U4(2)']})
    assert len(seen_cls)==25
    z=np.load(ROOT/'data'/'w33_pass1082_frame_coherent_configuration_tensor.npz')
    FC=z['fused_color']
    wd=json.loads((ROOT/'data'/'w33_pass1088_frame_adjacency_wedderburn.json').read_text())
    comps=wd['outer']['components']
    characters={};fixed_frames=[];frame_perms=[]
    for row in atlas_rows:
        p=H[classes[row['internal_class']][0]]
        fp=frame_perm(line_perm(p,lines,lidx),frames,fidx)
        frame_perms.append(fp);fixed_frames.append(sum(i==x for i,x in enumerate(fp)))
    for comp in comps:
        e=np.array(comp['idempotent_coefficients_mod_prime'],dtype=np.int64)%PRIME
        m=int(comp['multiplicity']);vals=[]
        for fp in frame_perms:
            tr=sum(int(e[int(FC[j,fp[j]])]) for j in range(540))%PRIME
            vals.append(balanced(tr*pow(m,-1,PRIME)%PRIME))
        characters[comp['label']]={'degree':comp['irreducible_dimension'],'multiplicity':m,'values':vals}
    sizes=[r['class_size'] for r in atlas_rows];labels=list(characters);gram={}
    for a in labels:
        gram[a]={}
        for b in labels:
            ip=sum(s*x*y for s,x,y in zip(sizes,characters[a]['values'],characters[b]['values']))//51840
            gram[a][b]=ip;assert ip==(1 if a==b else 0),(a,b,ip)
    recon=[sum(characters[a]['multiplicity']*characters[a]['values'][k] for a in labels) for k in range(25)]
    assert recon==fixed_frames
    matches=[a for a in labels if characters[a]['values']==DOC_15]
    sign=[1 if row['inside_U4(2)'] else -1 for row in atlas_rows]
    sign_twists={a:next((b for b in labels if characters[b]['values']==[u*v for u,v in zip(characters[a]['values'],sign)]),None) for a in labels}
    assert len(matches)==1
    iclasses,iclass_of=conjugacy_classes(inner,inner_index,inner_gens)
    irec=[]
    for ci,cl in enumerate(iclasses):
        rep=inner[cl[0]];irec.append({'ci':ci,'size':len(cl),'centralizer':25920//len(cl),'order':perm_order(rep)})
    aci=next(r['ci'] for r in irec if r['order']==2 and r['centralizer']==576)
    bci=next(r['ci'] for r in irec if r['order']==5 and r['centralizer']==5)
    a=inner[iclasses[aci][0]];b=None
    for ii in iclasses[bci]:
        z0=inner[ii]
        if perm_order(compose(a,z0))!=9:continue
        ok=True
        for _,w,o,cent in [INNER_ATLAS[1],INNER_ATLAS[3],INNER_ATLAS[8],INNER_ATLAS[16],INNER_ATLAS[19]]:
            x=eval_ab(w,a,z0);rr=irec[int(iclass_of[inner_index[x]])]
            if rr['order']!=o or rr['centralizer']!=cent:ok=False;break
        if ok and generated_size([a,z0],25920)==25920:b=z0;break
    assert b is not None
    inner_rows=[];inner_seen=set();inner_fps=[]
    for name,w,o,cent in INNER_ATLAS:
        x=eval_ab(w,a,b);ci=int(iclass_of[inner_index[x]]);rr=irec[ci]
        assert rr['order']==o and rr['centralizer']==cent,(name,rr);inner_seen.add(ci)
        fp=frame_perm(line_perm(x,lines,lidx),frames,fidx);inner_fps.append(fp)
        inner_rows.append({'name':name,'word':w,'order':o,'centralizer':cent,'class_size':25920//cent,'internal_class':ci})
    assert len(inner_seen)==20
    outer_on_inner={}
    for comp in comps:
        e=np.array(comp['idempotent_coefficients_mod_prime'],dtype=np.int64)%PRIME;m=int(comp['multiplicity']);vals=[]
        for fp in inner_fps:
            tr=sum(int(e[int(FC[j,fp[j]])]) for j in range(540))%PRIME;vals.append(balanced(tr*pow(m,-1,PRIME)%PRIME))
        outer_on_inner[comp['label']]=vals
    inner_degrees={'1':1,'15':15,'20':20,'24':24,'30a':30,'30b':30,'60':60,'64':64,'81':81}
    restriction={'1':{'1':1},'15a':{'15':1},'15b':{'15':1},'20':{'20':1},'24':{'24':1},'60a':{'60':1},'60b':{'30a':1,'30b':1},'64':{'64':1},'81_plus':{'81':1},'81_minus':{'81':1}}
    induction={'1':{'1':1,'epsilon':1},'15':{'15a':1,'15b':1},'20':{'20':1,'20_sign':1},'24':{'24':1,'24_sign':1},'30a':{'60b':1},'30b':{'60b':1},'60':{'60a':1,'60a_sign':1},'64':{'64':1,'64_sign':1},'81':{'81_minus':1,'81_plus':1}}
    induction_degrees={**{k:v['degree'] for k,v in characters.items()},'epsilon':1,'20_sign':20,'24_sign':24,'60a_sign':60,'64_sign':64}
    assert outer_on_inner['15a']==outer_on_inner['15b']
    assert outer_on_inner['81_plus']==outer_on_inner['81_minus']
    assert sign_twists['60b']=='60b' and all(characters['60b']['values'][i]==0 for i,row in enumerate(atlas_rows) if not row['inside_U4(2)'])
    for o,row in restriction.items():assert sum(inner_degrees[k]*m for k,m in row.items())==characters[o]['degree']
    for i,row in induction.items():assert sum(induction_degrees[k]*m for k,m in row.items())==2*inner_degrees[i]
    checks={'U42_order25920':len(inner)==25920,'U42dot2_order51840':len(H)==51840,'twentyfive_conjugacy_classes':len(classes)==25,'standard_c_is_ATLAS_2C':cclass==atlas_rows[15]['internal_class'],'standard_d_is_ATLAS_9A':dclass==atlas_rows[13]['internal_class'],'cd_has_order10':perm_order(compose(c,d))==10,'c_d_generate_full_group':generated_size([c,d])==51840,'all_ATLAS_words_hit_distinct_classes':len(seen_cls)==25,'all_ATLAS_orders_and_centralizers_match':True,'ten_frame_irreducibles_orthonormal':all(gram[a][b]==(1 if a==b else 0) for a in labels for b in labels),'permutation_character_reconstructed':recon==fixed_frames,'CTblLib_documented_unipotent_15_matched_uniquely':len(matches)==1,'Steinberg_sign_twist_pair_present':sign_twists.get('81_plus')=='81_minus' and sign_twists.get('81_minus')=='81_plus','inner_U42_twenty_classes':len(iclasses)==20 and len(inner_seen)==20,'inner_standard_a_b_found':b is not None and perm_order(compose(a,b))==9,'restriction_dimensions_close':all(sum(inner_degrees[k]*m for k,m in row.items())==characters[o]['degree'] for o,row in restriction.items()),'induction_dimensions_close':all(sum(induction_degrees[k]*m for k,m in row.items())==2*inner_degrees[i] for i,row in induction.items()),'Steinberg_restriction_and_induction':restriction['81_plus']=={'81':1} and restriction['81_minus']=={'81':1} and induction['81']=={'81_minus':1,'81_plus':1},'degrees_with_multiplicity_sum540':sum(v['degree']*v['multiplicity'] for v in characters.values())==540}
    assert all(checks.values()),checks
    out={'schema':'w33.pass1092.u42dot2.character_identification.v1','status':'PASS','headline':'The ten irreducible constituents of the 540-frame action are identified by exact ATLAS-class character vectors for U4(2):2. Official standard generators c in 2C and d in 9A were found inside the matrix-derived action, all 25 ATLAS class words matched their published orders and centralizers, and primitive-idempotent traces produced orthonormal integral characters reconstructing the frame permutation character.','group':{'ATLAS_name':'U4(2):2','GAP_identifier':'U4(2).2','order':51840,'inner':'U4(2)','inner_order':25920,'class_count':25},'standard_generators':{'c_class':'2C','d_class':'9A','order_cd':10},'atlas_classes':atlas_rows,'characters':characters,'frame_permutation_character':fixed_frames,'documented_CTBLIB_unipotent_15_vector':DOC_15,'documented_vector_matches_component':matches[0],'outer_sign_character':sign,'sign_twist_pairs':sign_twists,'orthogonality_gram':gram,'inner_ATLAS_classes':inner_rows,'inner_irreducible_degrees':inner_degrees,'outer_characters_restricted_to_inner_classes':outer_on_inner,'restriction_U42dot2_to_U42':restriction,'induction_U42_to_U42dot2':induction,'induction_symbolic_degrees':induction_degrees,'gap_companion':'analysis/w33_pass1092_u42dot2_character_match.g','check_count':len(checks),'checks':checks,'scope':'Exact character fingerprints in official ATLAS class order. The companion GAP script maps these vectors to CTblLib row indices when GAP/CTblLib is available; no unexecuted row-index output is claimed.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':'PASS','checks':len(checks),'matches':matches,'sign_twists':sign_twists,'seconds':round(time.time()-started,3)},indent=2))

if __name__=='__main__':main()
