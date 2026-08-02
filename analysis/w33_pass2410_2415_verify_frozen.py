#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FILES=[ROOT/'data'/f'w33_pass{p}_'+n for p,n in [(2410,'tomotope_tie_selector.json'),(2411,'global_u6_collision_ledger.json'),(2412,'proof_producing_nine_colour_search.json'),(2413,'pgsp_rank22_shell_fusion.json'),(2414,'e8_coexact_central_extension_ladder.json')]]
def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None);return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
h=[];checks=0
for f in FILES:
 d=json.loads(f.read_text());assert d['sha256_without_hash_field']==digest(d);h.append(d['sha256_without_hash_field']);checks+=1
 for v in d.get('checks',{}).values():assert v;checks+=1
assert hashlib.sha256('\n'.join(h).encode()).hexdigest()=='3e95c30283235a2cd56b879613a13a07c695bc66a4c741ff256e120483a5679b'
for p in ('w33_paper.tex','photonic_holonet.tex'):assert 'BT2415_five_frontiers_insert' in (ROOT/p).read_text();checks+=1
print(json.dumps({'status':'PASS','checks':checks,'aggregate_sha256':'3e95c30283235a2cd56b879613a13a07c695bc66a4c741ff256e120483a5679b'},sort_keys=True))
