#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FILES=[ROOT/'data'/f'w33_pass240{i}_{name}.json' for i,name in [(0,'syndrome_first_external_merge'),(1,'five_orbit_shell_algebra'),(2,'duad_first_coloring_base'),(3,'sl3_shell_parabolic_bridge'),(4,'e8_coexact_hom_obstruction'),(5,'tomotope_192_curved_duad_atlas')]]
EXPECTED_AGG='76b3ab373a7a8a59807a19841e8154db3fff986889f40600b55832393b364d98'
def digest(d):
    x=dict(d);x.pop('sha256_without_hash_field',None)
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def main():
    hashes=[]
    for p in FILES:
        d=json.loads(p.read_text());assert d['sha256_without_hash_field']==digest(d),p;hashes.append(d['sha256_without_hash_field'])
    assert hashlib.sha256(''.join(hashes).encode()).hexdigest()==EXPECTED_AGG
    for i in range(2400,2407):
        z=json.loads((ROOT/f'data/w33_pass_namespace_registry_v2.d/{i}.json').read_text())
        assert z['owner']=='six_frontier_shell_tomotope_execution' and z['status'].startswith('finalized')
    for p in (ROOT/'w33_paper.tex',ROOT/'photonic_holonet.tex'):
        assert 'BT2406_six_frontiers_insert' in p.read_text()
    cpp=(ROOT/'analysis/w33_pass2400_syndrome_first_external_merge.cpp').read_text();assert 'SHARD_BITS=7' in cpp and 'SHARD_MASK' in cpp
    t=(ROOT/'analysis/BT2400_BT2406_six_frontiers.md').read_text();assert '527' in t and 'three exact `96`' in t and 'chi(H)=9' in t
    print(json.dumps({'status':'PASS','checks':26,'aggregate_sha256':EXPECTED_AGG},indent=2))
if __name__=='__main__':main()
