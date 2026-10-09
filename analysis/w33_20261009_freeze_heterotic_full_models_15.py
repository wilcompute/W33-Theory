"""Freeze 15 original orbifolder model gauge embeddings with SHA256.
Reproducible even when the original user's WSL scan tree is unavailable.
"""
from pathlib import Path
import hashlib,json,gzip
import w33_20261009_heterotic_benchmark_full_roots as B
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261009_heterotic_full_models_15.json'
def main():
    ledger=json.load(gzip.open(ROOT/'data/w33_pass10960_heterotic_left_chiral_ledger.json.gz','rt'))
    labels=sorted(x.split('|',1)[1] for x in ledger if x.startswith('Z6-II|Z6II_34__'))
    assert len(labels)==15
    models={}
    for name in labels:
        path=B.SCAN/(name+'.model')
        assert path.is_file(),str(path)
        raw=path.read_bytes()
        rows=B.source_model(path)
        models[name]={'rows':[[str(x) for x in r] for r in rows],
                      'source_sha256':hashlib.sha256(raw).hexdigest()}
    document=dict(schema='w33.20261009.full_orbifolder_model_fixture.v1',
                  source='~/orb/scan/cp2/out/<name>.model',
                  note='Raw charge model embeddings only; no copyright to model names or gauge vectors claimed.',
                  models=models)
    OUT.write_text(json.dumps(document,indent=2)+'\n')
    print('FROZEN MODEL EMBEDDINGS',len(models),OUT)
if __name__=='__main__':main()
