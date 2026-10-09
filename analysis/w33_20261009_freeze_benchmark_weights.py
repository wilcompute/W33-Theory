"""Freeze 24 raw orbifolder gauge-weight readouts for independent B-L testing."""
from pathlib import Path
from fractions import Fraction as F
import gzip,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
NAME='Z6II_34__SM_20260917_1558'
def main():
    src=Path.home()/'orb'/'scan'/'cp2'/'out'/(NAME+'.w')
    assert src.is_file()
    raw=src.read_bytes()
    sp=json.load(gzip.open(ROOT/'data/w33_pass10960_heterotic_left_chiral_ledger.json.gz','rt'))
    names={f['name'] for f in sp['Z6-II|'+NAME]['left']}
    anchors={}
    for line in raw.decode().splitlines():
        if not line.startswith('W ') or 'P=' not in line:continue
        label=line.split()[1]
        if label not in names or label in anchors:continue
        p=[float(v) for v in line.split('P=',1)[1].split()[0].split(',')]
        if len(p)!=16:continue
        rationals=[F(v).limit_denominator(216) for v in p]
        assert max(abs(float(v)-x) for v,x in zip(rationals,p))<1e-6
        anchors[label]=[str(v) for v in rationals]
    assert len(anchors)>=24
    out=dict(status='PASS',source_relpath='~/orb/scan/cp2/out/'+NAME+'.w',
        source_sha256=hashlib.sha256(raw).hexdigest(),count=len(anchors),
        model=NAME,anchors=anchors,
        boundary='One gauge momentum representative per raw field; fractions recovered from printed decimals with residual below 1e-6.')
    path=ROOT/'data/w33_20261009_benchmark_weight_anchors_24.json'
    path.write_text(json.dumps(out,indent=2)+'\n')
    print('FROZEN',len(anchors),'gauge weights')
if __name__=='__main__':main()
