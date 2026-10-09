"""Gauge-shift benchmark screening for the selected W33 Z6-II models.

Conservative equality test: fixed orbifold generator, independent E8 Weyl,
root-lattice shifts, and swap of two factors. Does NOT quotient
space-group generator redefinitions or compare Wilson-line classes.
"""
import gzip,json
from fractions import Fraction as F
from pathlib import Path
BENCH=(F(1,3),-F(1,2),-F(1,2),F(0),F(0),F(0),F(0),F(0),
       F(1,2),-F(1,6),-F(1,2),-F(1,2),-F(1,2),-F(1,2),-F(1,2),F(1,2))
def e8_lattice(v):
    assert len(v)==8
    allint=all(x.denominator==1 for x in v)
    allhalf=all((x-F(1,2)).denominator==1 for x in v)
    return (allint or allhalf) and sum(v).denominator==1 and sum(v).numerator%2==0
def nontrivial_factors(v):
    return sum(not e8_lattice(v[i:i+8]) for i in (0,8))
def main():
    root=Path(__file__).resolve().parents[1]
    ledger=json.load(gzip.open(root/'data/w33_pass10960_heterotic_left_chiral_ledger.json.gz','rt'))
    subset=sorted({key.split('|',1)[1].split('__',1)[0] for key in ledger if key.startswith('Z6-II|')})
    base=Path.home()/'orb'/'scan'
    result={}
    for label in subset:
        path=base/(label+'.txt')
        if not path.exists():
            result[label]={'status':'BASE_SHIFT_MISSING'};continue
        lines=path.read_text().splitlines()
        k=lines.index('Shifts and Wilsonlines:')
        vec=tuple(F(x) for x in lines[k+1].split())
        assert len(vec)==16
        result[label]={'nontrivial_e8_factors':nontrivial_factors(vec),
                       'first_e8_zero':all(x==0 for x in vec[:8])}
    summary={'ledger_models':len(ledger),'z6_ii_models':sum(k.startswith('Z6-II|') for k in ledger),
       'distinct_z6_ii_base_shifts':len(subset),
       'present_shift_files':sum('nontrivial_e8_factors' in r for r in result.values()),
       'benchmark_0708_2691_E1_F1_nontrivial_factors':nontrivial_factors(BENCH),
       'baseline_nontrivial_factor_counts':{str(t):sum(r.get('nontrivial_e8_factors')==t for r in result.values()) for t in (0,1,2)},
       'base_labels_with_two_nontrivial_factors':[k for k,v in result.items() if v.get('nontrivial_e8_factors')==2]}
    print(json.dumps(summary,indent=2))
    return summary
if __name__=='__main__':main()
