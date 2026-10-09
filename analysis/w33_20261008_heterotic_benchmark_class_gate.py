"""Necessary E8xE8 gauge-shift invariants for external benchmark model 1.
Only fixed space-group generator modulo E8 lattice/Weyl/factor-swap.
"""
from fractions import Fraction as F
from pathlib import Path
from collections import Counter
import gzip,json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261008_heterotic_benchmark_shift_screen as first
def e8_class(v):
    for order in range(1,25):
        if first.e8_lattice(tuple(order*x for x in v)):break
    else:raise AssertionError('order exceeds 24')
    norm=sum(x*x for x in v)
    q=(order*norm) % 2
    return (order,str(q))
def factor_signature(v):
    return tuple(sorted((e8_class(v[:8]),e8_class(v[8:]))))
def main():
    benchmark=factor_signature(first.BENCH)
    ledger=json.load(gzip.open(ROOT/'data/w33_pass10960_heterotic_left_chiral_ledger.json.gz','rt'))
    names=sorted({k.split('|',1)[1].split('__',1)[0] for k in ledger if k.startswith('Z6-II|')})
    model={}
    for name in names:
        lines=(Path.home()/'orb'/'scan'/(name+'.txt')).read_text().splitlines()
        v=tuple(F(x) for x in lines[lines.index('Shifts and Wilsonlines:')+1].split())
        model[name]=factor_signature(v)
    survivors=[name for name,sign in model.items() if sign==benchmark]
    orders=[name for name,sign in model.items() if sorted(x[0] for x in sign)==sorted(x[0] for x in benchmark)]
    result=dict(status='PASS',benchmark_factor_invariants=benchmark,
                distinct_base_shift_count=len(model),
                same_factor_orders=orders,
                same_orders_and_quadratic_classes=survivors,
                excluded_by_this_necessary_invariant=len(model)-len(survivors),
                scope='Only fixed shift V under independent E8 lattice+Weyl, and E8 factor swap. Not full orbifold equivalence, model or Wilson-line comparison.')
    print(json.dumps(result,indent=2))
    return result
if __name__=='__main__':main()
