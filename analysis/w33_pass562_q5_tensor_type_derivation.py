#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from collections import Counter,defaultdict
from pathlib import Path
from w33_pass543_547_common import charpoly_prime
from w33_pass553_five_point_core_geometry import A
from w33_pass555_all_fixed_magnitude_fibres import f2rank,translation_space,anf_terms

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass562_q5_tensor_type_derivation.json'

def fwht(a):
    a=list(a);h=1
    while h<len(a):
        for i in range(0,len(a),2*h):
            for j in range(i,i+h):
                x,y=a[j],a[j+h];a[j]=x+y;a[j+h]=x-y
        h*=2
    return a

def mobius(a):
    a=list(a)
    for i in range(12):
        bit=1<<i
        for m in range(4096):
            if m&bit:a[m]^=a[m^bit]
    return a

def tensor_rows():
    rows=[]
    for m in range(4096):
        offs=tuple(a*(4 if (m>>i)&1 else 1)%5 for i,a in enumerate(A))
        cp=tuple(charpoly_prime(5,offs)[0])
        rows.append((cp[3],cp[4],cp[5]))
    return rows

def transform_type(S):
    indicator=[1 if m in S else 0 for m in range(4096)]
    W=fwht(indicator)
    support=[m for m,x in enumerate(W) if x]
    constant_chars=[m for m,x in enumerate(W) if abs(x)==len(S)]
    td=12-f2rank(support)
    ad=12-f2rank(constant_chars)
    anf=mobius(indicator)
    generator=anf[:];generator[0]^=1
    deg=max(m.bit_count() for m,x in enumerate(generator) if x)
    return (len(S),ad,td,len(S)//(1<<td),deg),{'walsh_support_rank':f2rank(support),'constant_character_rank':f2rank(constant_chars),'walsh_support_size':len(support),'constant_character_count':len(constant_chars),'principal_generator_terms':sum(generator)}

def payload():
    rows=tensor_rows();fibres=defaultdict(set)
    for m,key in enumerate(rows):fibres[key].add(m)
    types=Counter();records=[];cross=True
    for key,S0 in sorted(fibres.items(),key=lambda kv:str(kv[0])):
        S=frozenset(S0);typ,meta=transform_type(S);types[typ]+=1
        # Independent geometry cross-check, not used to derive typ.
        T=translation_space(S);base=min(S);gterms=set(anf_terms(S))^{0}
        geo=(len(S),f2rank(x^base for x in S),f2rank(T),len(S)//len(T),max(m.bit_count() for m in gterms))
        cross &= typ==geo
        records.append({'tensor_level_sha256':__import__('hashlib').sha256(json.dumps(key,separators=(',',':')).encode()).hexdigest(),'type':typ,**meta})
    expected=Counter({(16,4,4,1,8):1,(40,11,1,20,9):44,(40,11,2,10,9):48,(80,8,4,5,8):3,(80,12,1,40,8):2})
    type_digest=__import__('hashlib').sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    checks={
      'tensor_level_sets_are_exact_98_fibres':len(fibres)==98,
      'tensor_rows_cover_all_4096_sections':sum(map(len,fibres.values()))==4096,
      'walsh_translation_theorem_matches_geometry':cross,
      'exactly_five_transform_types':len(types)==5,
      'five_type_census_exact':types==expected,
      'translation_dimension_from_walsh_annihilator':all(r['type'][2]==12-r['walsh_support_rank'] for r in records),
      'affine_dimension_from_constant_characters':all(r['type'][1]==12-r['constant_character_rank'] for r in records),
      'principal_generator_degrees_eight_or_nine':Counter(r['type'][4] for r in records)==Counter({9:92,8:6}),
      'three_triality_fibres_transform_type':types[(80,8,4,5,8)]==3,
    }
    return {'schema':'w33.pass562.q5_tensor_type_derivation.v1','status':'PASS' if all(checks.values()) else 'FAIL','derivation':{'level_set':'S_(a,b,c)={s : (e3(s),e4(s),e5(s))=(a,b,c)}; e2 is constant on the magnitude cube.','translation_theorem':'For f=1_S, T(S) is the orthogonal complement of span(supp Walsh(f)); therefore dim T=12-rank(supp Walsh(f)).','affine_hull_theorem':'Characters with |Walsh(f)(w)|=|S| are exactly those constant on S; their rank is the codimension of the affine hull.','boolean_ideal_theorem':'The principal generator 1+1_S is obtained by the Boolean Möbius transform; its maximum monomial weight gives the generator degree.','consequence':'The five geometry types are derived directly from the invariant-tensor level indicators and their transforms, without first computing translations or affine hulls.'},'type_fields':['size','affine_hull_dimension','translation_dimension','parallel_cosets','principal_generator_degree'],'type_counts':{str(k):v for k,v in sorted(types.items())},'record_count':len(records),'transform_catalog_sha256':type_digest,'checks':checks,'boundary':'This is a theorem-backed finite derivation for the fixed q=5 magnitude cube. It replaces the post hoc geometric classifier by Walsh and Möbius transforms of the A5-invariant coefficient level sets; it does not yet give a symbolic all-magnitudes classification.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 562 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'types':len(p['type_counts'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
