"""Portable rational benchmark B-L comparison from frozen raw gauge-weight anchors.

Avoids requiring the user's original WSL orbifolder directory in CI. The
anchor source SHA, all 16-coordinate momenta and explicit Weyl matrix are
frozen independently. A 7-dimensional U1-span leaves two unconstrained
directions, so this probe is not a unique full B-L charge assignment.
"""
from pathlib import Path
from fractions import Fraction as F
import gzip,json,sys
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261009_benchmark_BL_weight_probe as source
NAME=source.NAME
def certificate():
    fixture=json.loads((ROOT/'data/w33_20261009_benchmark_weight_anchors_24.json').read_text())
    assert fixture['count']==24 and len(fixture['source_sha256'])==64
    t=source.derived_vector()
    gauge={name:sum(a*F(p) for a,p in zip(t,row))
           for name,row in fixture['anchors'].items()}
    ledger=json.load(gzip.open(ROOT/'data/w33_pass10960_heterotic_left_chiral_ledger.json.gz','rt'))
    rows={x['name']:x for x in ledger['Z6-II|'+NAME]['left']}
    A=s.Matrix([[s.Rational(v) for v in rows[n]['q']] for n in gauge])
    B=s.Matrix([s.Rational(str(v)) for v in gauge.values()])
    assert A.rank()==A.row_join(B).rank()==7
    x,parameters=A.gauss_jordan_solve(B)
    x=x.subs({p:0 for p in parameters})
    outputs={}
    for label,f in rows.items():
        if label.rsplit('_',1)[0] not in ('q','bu','bd','be','l','bl'):continue
        outputs[label]=str((s.Matrix([[s.Rational(v) for v in f['q']]])*x)[0])
    assert all(outputs['q_'+str(i)]=='1/3' for i in (1,2,3))
    assert all(outputs['bu_'+str(i)]=='-1/3' for i in (1,2,3))
    assert all(outputs['be_'+str(i)]=='1' for i in (1,2,3))
    assert {name:outputs[name] for name in ('bd_1','bd_2','bd_4','bd_6','bd_7','bd_8')}==dict.fromkeys(('bd_1','bd_2','bd_4','bd_6','bd_7','bd_8'),'2/3')
    assert {name:outputs[name] for name in ('bd_3','bd_5','bd_9','bd_10')}==dict.fromkeys(('bd_3','bd_5','bd_9','bd_10'),'-1/3')
    return dict(status='PASS',anchors=len(gauge),rank=7,U1_nullity=2,
       benchmark_BL_under_explicit_Weyl=[str(v) for v in t],
       frozen_weight_source_sha256=fixture['source_sha256'],
       assignments=outputs,scope='Source-field B-L reconstruction from 24 independent gauge-weight anchors, 2 U1 directions unanchored; no physical vacuum or full orbifold equivalence.')
if __name__=='__main__':
    out=certificate()
    (ROOT/'data/w33_20261009_portable_benchmark_BL.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS portable B-L',out['anchors'],'anchors, rank',out['rank'])
