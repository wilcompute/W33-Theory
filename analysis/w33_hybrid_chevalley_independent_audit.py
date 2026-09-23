#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
paths=[ROOT/'artifacts/e8_structure_constants_w33_discrete.json',ROOT/'data/w33_e8_full_hybrid_chevalley_compiler.json']
for p in paths: assert p.exists(),p
hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
c=json.loads(paths[1].read_text())
text=json.dumps(c,sort_keys=True).lower()
assert 'jacobi' in text and ('2511496' in text or '2,511,496' in text)
out={'schema':'w33.hybrid.chevalley.independent.audit.v1','status':'PASS_SOURCE_AND_CERTIFICATE_INTEGRITY_ONLY','source_sha256':hashes,'scope':'This audit verifies committed source presence and the declared exhaustive-Jacobi certificate; it is not a second exhaustive bracket computation.'}
(ROOT/'data/w33_hybrid_chevalley_independent_audit.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,sort_keys=True))
