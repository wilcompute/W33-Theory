#!/usr/bin/env python3
"""Parse GAP fusion sieve and combine it with an mmgroup engine smoke certificate."""
from __future__ import annotations
import ast, hashlib, json, os, platform, re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def parse(path):
    lines=path.read_text(encoding='utf-8',errors='replace').splitlines(); data={}
    for line in lines:
        m=re.match(r'^(FUSION_COUNT|U_DEGREES|FUSION_\d+|DECOMP_\d+)=(.*)$',line.strip())
        if m: data[m.group(1)]=ast.literal_eval(m.group(2))
    count=int(data['FUSION_COUNT']); degrees=list(map(int,data['U_DEGREES']))
    fusions=[]
    for i in range(1,count+1):
        f=list(map(int,data[f'FUSION_{i}'])); dec=list(map(int,data[f'DECOMP_{i}']))
        assert len(dec)==len(degrees) and all(x>=0 for x in dec)
        assert sum(a*b for a,b in zip(degrees,dec))==196883
        fusions.append({'map':f,'decomposition':dec,'degree81_multiplicity':sum(dec[j] for j,d in enumerate(degrees) if d==81)})
    return degrees,fusions

def mmgroup_smoke():
    from mmgroup import MM, MM_from_int
    samples=[MM('t',1),MM('l',1),MM('d',1),MM('x',1)]
    rows=[]
    for g in samples:
        key=g.as_int(); h=MM_from_int(key); assert h.as_int()==key
        rows.append({'order':int(g.order()),'as_int':str(key),'roundtrip':True})
    return {'available':True,'python':sys.version.split()[0],'platform':platform.platform(),'samples':rows}

def main():
    gap=Path(os.environ.get('GAP_OUTPUT','/tmp/pass3985_gap.txt'))
    degrees,fusions=parse(gap)
    smoke=mmgroup_smoke()
    candidate=ROOT/'data/PART_3751_MONSTER_U42_CLASS_FUSION_EXECUTION.json'
    result={'schema':'w33.pass3985.monster_acquisition_gate.v1','status':'PASS_CHARACTER_TABLE_FUSION_SIEVE_WORDS_PENDING',
      'u42_character_degrees':degrees,'possible_class_fusions':len(fusions),'fusions':fusions,
      'degree81_multiplicity_values':sorted(set(x['degree81_multiplicity'] for x in fusions)),
      'mmgroup_smoke':smoke,'explicit_candidate_artifact_present':candidate.exists(),
      'embedding_promoted':False,
      'external_sources':['CTblLib character tables U4(2) and M','mmgroup canonical MM/as_int engine'],
      'boundary':'Character-table compatibility and mmgroup engine availability do not supply explicit embedded U4(2) words. Promotion still requires four serialized words passing the strict closure, order-census, object-action, and class-fusion harness.'}
    result['fusion_sha256']=hashlib.sha256(json.dumps(fusions,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    (ROOT/'data/PART_3985_MONSTER_ACQUISITION_GATE.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS_MONSTER_ACQUISITION_GATE',len(fusions),result['degree81_multiplicity_values'],result['fusion_sha256'])
if __name__=='__main__': main()
