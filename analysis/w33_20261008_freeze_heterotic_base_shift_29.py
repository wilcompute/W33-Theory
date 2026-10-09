"""Freeze exact Z6-II base-shift rows needed to reproduce comparison off WSL.

Source: local orbifolder scan ~/orb/scan/Z6II_nn.txt; never its spectra.
"""
import gzip,hashlib,json
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261008_heterotic_base_shift_29.json'
def main():
    ledger=json.load(gzip.open(ROOT/'data/w33_pass10960_heterotic_left_chiral_ledger.json.gz','rt'))
    models=sorted(k for k in ledger if k.startswith('Z6-II|'))
    prefixes=sorted({k.split('|')[1].split('__')[0] for k in models})
    rows={}
    for label in prefixes:
        path=Path.home()/'orb'/'scan'/(label+'.txt')
        raw=path.read_bytes()
        lines=raw.decode().splitlines()
        v=lines[lines.index('Shifts and Wilsonlines:')+1].split()
        assert len(v)==16 and all(F(x).denominator>0 for x in v)
        rows[label]={'V':[str(F(x)) for x in v],
                     'source_relpath':'~/orb/scan/'+label+'.txt',
                     'raw_sha256':hashlib.sha256(raw).hexdigest(),
                     'ledger_model_count':sum(k.split('|')[1].split('__')[0]==label for k in models)}
    assert len(rows)==29 and sum(v['ledger_model_count'] for v in rows.values())==128
    obj={'schema':'w33.20261008.heterotic_shift_fixture.v1',
         'origin':'W33 215-model Pass10960 ledger base labels; original orbifolder scan',
         'z6ii_model_count':len(models),'base_shifts':rows}
    OUT.write_text(json.dumps(obj,indent=2)+'\n')
    print('FROZEN',len(rows),'base shifts,',len(models),'model labels; output',OUT)
if __name__=='__main__':main()
