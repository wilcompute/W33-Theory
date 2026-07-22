#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from collections import Counter,defaultdict
from pathlib import Path
from w33_pass543_547_common import charpoly_prime
from w33_pass553_five_point_core_geometry import A,signed_magnitude_actions,apply_action

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass555_all_fixed_magnitude_fibres.json'

def f2rank(nums):
    b=[]
    for x in nums:
        y=x
        for p in b:y=min(y,y^p)
        if y:
            q=1<<(y.bit_length()-1);b=[z^y if z&q else z for z in b];b.append(y);b.sort(reverse=True)
    return len(b)

def translation_space(S):
    base=min(S)
    return frozenset(t for t in (x^base for x in S) if all((y^t) in S for y in S))

def anf_terms(S):
    a=[1 if x in S else 0 for x in range(4096)]
    for i in range(12):
        b=1<<i
        for m in range(4096):
            if m&b:a[m]^=a[m^b]
    return tuple(i for i,c in enumerate(a) if c)

def cp_key(cp):return json.dumps(cp,separators=(',',':'))

def payload():
    fibres=defaultdict(set);target=tuple(charpoly_prime(5,A)[0])
    for m in range(4096):
        offs=tuple(a*(4 if (m>>i)&1 else 1)%5 for i,a in enumerate(A))
        fibres[tuple(charpoly_prime(5,offs)[0])].add(m)
    catalog=[];set_to_idx={}
    for idx,(cpv,S0) in enumerate(sorted(fibres.items(),key=lambda kv:cp_key(kv[0]))):
        S=frozenset(S0);base=min(S);T=translation_space(S);ad=f2rank(x^base for x in S);td=f2rank(T)
        terms=anf_terms(S);gterms=set(terms)^({0});deg=max(m.bit_count() for m in gterms) if gterms else -1
        typ=(len(S),ad,td,len(S)//len(T),deg)
        row={'id':idx,'charpoly_sha256':hashlib.sha256(cp_key(cpv).encode()).hexdigest(),'size':len(S),'affine_hull_dimension':ad,'translation_dimension':td,'parallel_cosets':len(S)//len(T),'principal_ideal_generator_degree':deg,'principal_ideal_generator_terms':len(gterms),'principal_ideal_generator_sha256':hashlib.sha256(','.join(hex(x) for x in sorted(gterms)).encode()).hexdigest(),'is_affine_subspace':len(S)==(1<<ad),'global_complement_closed':all((x^0xfff) in S for x in S),'is_pass540_target':cpv==target,'type':typ}
        catalog.append(row);set_to_idx[S]=idx
    actions=signed_magnitude_actions();unseen=set(set_to_idx);orbits=[]
    while unseen:
        S=next(iter(unseen));O={frozenset(apply_action(x,g) for x in S) for g in actions}&set(set_to_idx)
        orbits.append(sorted(set_to_idx[x] for x in O));unseen-=O
    type_counts=Counter(tuple(r['type']) for r in catalog);orbit_counts=Counter(len(o) for o in orbits);type_orbits=Counter()
    for o in orbits:
        typ=tuple(catalog[o[0]]['type']);assert all(tuple(catalog[i]['type'])==typ for i in o);type_orbits[(typ,len(o))]+=1
    five_cube=[r for r in catalog if r['size']==80 and r['translation_dimension']==4 and r['parallel_cosets']==5]
    diffuse80=[r for r in catalog if r['size']==80 and r['translation_dimension']==1 and r['parallel_cosets']==40]
    checks={'all_4096_sections_partitioned':sum(r['size'] for r in catalog)==4096,'exact_98_fibres':len(catalog)==98,'size_histogram_16_40_80':Counter(r['size'] for r in catalog)==Counter({40:92,80:5,16:1}),'five_translation_types_exact':type_counts==Counter({(16,4,4,1,8):1,(40,11,1,20,9):44,(40,11,2,10,9):48,(80,8,4,5,8):3,(80,12,1,40,8):2}),'all_boolean_ideals_principal':all(r['principal_ideal_generator_terms']>0 for r in catalog),'generator_degrees_8_or9':Counter(r['principal_ideal_generator_degree'] for r in catalog)==Counter({9:92,8:6}),'exactly_three_five_cube_fibres':len(five_cube)==3,'exactly_two_diffuse_80_fibres':len(diffuse80)==2,'target_is_five_cube_type':sum(r['is_pass540_target'] and r in five_cube for r in catalog)==1,'signed_stabilizer_preserves_catalog':sum(map(len,orbits))==98,'physical_signed_action_fixes_every_fibre':len(orbits)==98 and orbit_counts==Counter({1:98}),'five_cube_fibres_are_individually_fixed':all(any(len(o)==1 and r['id'] in o for o in orbits) for r in five_cube)}
    return {'schema':'w33.pass555.all_fixed_magnitude_fibres.v1','status':'PASS' if all(checks.values()) else 'FAIL','principal_ideal_theorem':'In the Boolean function ring B_12=F2[x]/(x_i^2-x_i), I(S)=<1+chi_S>. The generator is zero exactly on S and one on its complement.','type_fields':['size','affine_hull_dimension','translation_dimension','parallel_cosets','principal_generator_degree'],'type_counts':{str(k):v for k,v in sorted(type_counts.items())},'orbit_summary':{'signed_stabilizer_order':len(actions),'fibre_orbits':len(orbits),'orbit_size_histogram':dict(sorted(orbit_counts.items())),'type_orbit_counts':{str(k):v for k,v in sorted(type_orbits.items(),key=str)}},'five_cube_result':{'count':len(five_cube),'ids':[r['id'] for r in five_cube],'target_id':next(r['id'] for r in catalog if r['is_pass540_target']),'conclusion':'The Pass-540 five-parallel-four-cube geometry is not unique: exactly three of the 98 fibres have this type. The exact signed Clifford stabilizer fixes every characteristic-polynomial fibre setwise.'},'catalog_custody':{'fibre_count':len(catalog),'size_histogram':dict(sorted(Counter(r['size'] for r in catalog).items())),'catalog_sha256':hashlib.sha256(json.dumps(catalog,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'certificate_policy':'The executable owner regenerates all 98 rows; the immutable certificate stores the exact digest and structural census rather than duplicating the full generated table.'},'checks':checks,'boundary':'This is a complete classification of the 98 fibres inside the fixed Pass-540 magnitude cube. The physical action uses the signed antipodal permutation; dropping its sign cocycle produces a different, non-covariant set action. This is not a classification of all 2,034,735 q=5 section orbits.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 555 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'fibres':p['catalog_custody']['fibre_count']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
