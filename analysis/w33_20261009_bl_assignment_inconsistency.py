"""Audit Pass10960 B-L obstruction for the exact gauge-matched benchmark candidate.
Find a minimal inconsistent set of ALL fields with labels q,bu,bd,be.
This is a gauge-charge linear-system obstruction, not a no-go for a
chosen three-family assignment and not a string-vacuum equivalence test.
"""
from pathlib import Path
import gzip,json,sys
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_pass10960_matter_even_dflat_closure import BL
MODEL='Z6-II|Z6II_34__SM_20260917_1558'
def constraints():
    raw=json.load(gzip.open(ROOT/'data/w33_pass10960_heterotic_left_chiral_ledger.json.gz','rt'))
    recs=[]
    for f in raw[MODEL]['left']:
        base=f['name'].rsplit('_',1)[0]
        if base in BL:
            recs.append(dict(name=f['name'],base=base,dim=f['dim'],
              q=[s.Rational(x) for x in f['q']],b=s.Rational(str(BL[base]))))
    return recs
def inconsistent(rows):
    if not rows:return False
    a=s.Matrix([r['q'] for r in rows])
    b=s.Matrix([r['b'] for r in rows])
    return a.rank()!=a.row_join(b).rank()
def main():
    records=constraints()
    assert inconsistent(records)
    core=list(records)
    changed=True
    while changed:
        changed=False
        for r in list(core):
            remain=[x for x in core if x is not r]
            if inconsistent(remain):
                core=remain;changed=True;break
    assert all(not inconsistent([x for x in core if x is not y]) for y in core)
    matrix=s.Matrix([r['q'] for r in core])
    b=s.Matrix([r['b'] for r in core])
    null=matrix.T.nullspace()
    y=next(vec for vec in null if (vec.dot(b))!=0)
    assert (matrix.T*y)==s.zeros(9,1)
    residual=y.dot(b)
    return dict(status='PASS',model=MODEL,
       total_constrained_labelled_fields=len(records),
       minimal_unsatisfiable_rows=[dict(name=r['name'],base=r['base'],dim=r['dim'],
           u1_charges=[str(q) for q in r['q']],target_BL=str(r['b'])) for r in core],
       linear_inconsistency_witness=[str(x) for x in y],
       weighted_BminusL_residual=str(residual),
       global_scope='All fields named q,bu,bd,be are required to carry the same canonical B-L. No choices of family assignments, exotic pair charges or benchmark singlet supports are tested.')
if __name__=='__main__':
    out=main()
    (ROOT/'data/w33_20261009_bl_assignment_inconsistency.json').write_text(json.dumps(out,indent=2)+'\n')
    print('B-L minimal core',len(out['minimal_unsatisfiable_rows']),'of',out['total_constrained_labelled_fields'],'labels')
    print('names',[r['name'] for r in out['minimal_unsatisfiable_rows']])
    print('coeffs',out['linear_inconsistency_witness'],'residual',out['weighted_BminusL_residual'])
