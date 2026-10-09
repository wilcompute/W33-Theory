"""Unbroken-E8 root-count sieve for 2008 benchmark shift versus W33 bases."""
from fractions import Fraction as F
from itertools import product,combinations
from pathlib import Path
import json,gzip,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261008_heterotic_benchmark_shift_screen as src
import w33_20261008_heterotic_benchmark_class_gate as gate
def roots():
    zero=(0,)*8
    for i,j in combinations(range(8),2):
        for a,b in product((-1,1),repeat=2):
            v=list(zero);v[i]=a;v[j]=b;yield tuple(F(z) for z in v)
    for v in product((-1,1),repeat=8):
        if sum(z<0 for z in v)%2==0:yield tuple(F(z,2) for z in v)
def root_counts(v):
    R=list(roots());assert len(R)==240
    return tuple(sorted(sum((sum(x*y for x,y in zip(r,v[base:base+8]))).denominator==1 for r in R) for base in (0,8)))
def main():
    benchmark=(gate.factor_signature(src.BENCH),root_counts(src.BENCH))
    ledger=json.load(gzip.open(ROOT/'data/w33_pass10960_heterotic_left_chiral_ledger.json.gz','rt'))
    names=sorted({k.split('|',1)[1].split('__',1)[0] for k in ledger if k.startswith('Z6-II|')})
    survivors=[]
    counts={}
    for label in names:
        lines=(Path.home()/'orb'/'scan'/(label+'.txt')).read_text().splitlines()
        vec=tuple(F(x) for x in lines[lines.index('Shifts and Wilsonlines:')+1].split())
        s=(gate.factor_signature(vec),root_counts(vec))
        counts[label]=s[1]
        if s==benchmark:survivors.append(label)
    out=dict(status='PASS',benchmark_E8_root_counts=benchmark[1],
        shift_invariant_survivors=survivors,distinct_bases_checked=len(names),
        caveat='Root-count necessary condition for fixed Z6 twist generator only, not Wilson line class or full orbifold equivalence.')
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':main()
