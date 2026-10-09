"""W33 Z6II_34 versus both Lebedev benchmark models: unbroken E8-root sieve.

Necessary fixed-background equivalence test, not a full orbifold classification.
Public benchmarks: arXiv:0708.2691 E.1/F.1, rational 16-coordinate data.
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import combinations,product
from collections import Counter
import gzip,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
SCAN=Path.home()/'orb'/'scan'/'cp2'/'out'
BENCH_V='1/3 -1/2 -1/2 0 0 0 0 0 1/2 -1/6 -1/2 -1/2 -1/2 -1/2 -1/2 1/2'
BENCH={
 'model1':{
 'W2':'0 -1/2 -1/2 -1/2 1/2 0 0 0 4 -3 -7/2 -4 -3 -7/2 -9/2 7/2',
 'W3':'-1/2 -1/2 1/6 1/6 1/6 1/6 1/6 1/6 1/3 0 0 2/3 0 5/3 -2 0'},
 'model2':{
 'W2':'1/4 -1/4 -1/4 -1/4 -1/4 1/4 1/4 1/4 1 -1 -5/2 -3/2 -1/2 -5/2 -3/2 3/2',
 'W3':'-1/2 -1/2 1/6 1/6 1/6 1/6 1/6 1/6 10/3 0 -6 -7/3 -4/3 -5 -3 3'}}
def vector(line):
    v=tuple(Q(x.strip()) for x in line.replace(',',' ').split())
    assert len(v)==16
    return v
def e8roots():
    out=[]
    for i,j in combinations(range(8),2):
        for a,b in product((-1,1),repeat=2):
            r=[Q(0)]*8;r[i]=Q(a);r[j]=Q(b);out.append(tuple(r))
    for signs in product((-1,1),repeat=8):
        if sum(x<0 for x in signs)%2==0:out.append(tuple(Q(x,2) for x in signs))
    assert len(out)==240
    return out
ROOTS=e8roots()
def invariant(rows):
    answer=[]
    for side in (0,8):
        count=0
        for root in ROOTS:
            if all(sum(root[i]*v[side+i] for i in range(8)).denominator==1 for v in rows):
                count+=1
        answer.append(count)
    return tuple(sorted(answer))
def source_model(path):
    if path.is_file():
        lines=path.read_text().splitlines()
        i=lines.index('Shifts and Wilsonlines:')
        rows=[vector(lines[i+1+j]) for j in range(8)]
        assert lines[i+9]=='end model'
        return rows
    frozen=json.loads((ROOT/'data/w33_20261009_heterotic_full_models_15.json').read_text())
    record=frozen['models'][path.stem]
    return [tuple(Q(x) for x in row) for row in record['rows']]
def analyze():
    v=vector(BENCH_V)
    benchmarks={name:invariant([v,vector(b['W2']),vector(b['W3'])]) for name,b in BENCH.items()}
    ledger=json.load(gzip.open(ROOT/'data/w33_pass10960_heterotic_left_chiral_ledger.json.gz','rt'))
    names=sorted(k.split('|',1)[1] for k in ledger if k.startswith('Z6-II|Z6II_34__'))
    assert len(names)==15
    results={}
    for name in names:
        f=SCAN/(name+'.model')
        rows=source_model(f)
        provenance=(hashlib.sha256(f.read_bytes()).hexdigest() if f.is_file()
                    else json.loads((ROOT/'data/w33_20261009_heterotic_full_models_15.json').read_text())['models'][name]['source_sha256'])
        results[name]=dict(unbroken_e8_root_counts=invariant(rows),
                           raw_sha256=provenance,
                           nonzero_wilson_rows=sum(any(q!=0 for q in row) for row in rows[1:]))
    match={name:[k for k,x in results.items() if x['unbroken_e8_root_counts']==counts] for name,counts in benchmarks.items()}
    return dict(status='PASS',benchmark_root_counts=benchmarks,
                candidate_models=len(names),candidate_model_results=results,
                necessary_root_count_matches=match,
                caveat='Strict necessary full gauge-algebra root-count sieve under same E8xE8 factor embedding; not a Wilson equivalence proof or comprehensive orbifold equivalence.')
if __name__=='__main__':
    result=analyze()
    print('BENCHMARKS',result['benchmark_root_counts'])
    print('RESULT ROOT COUNTS',Counter(tuple(v['unbroken_e8_root_counts']) for v in result['candidate_model_results'].values()))
    print('MATCHES',result['necessary_root_count_matches'])
    p=ROOT/'data/w33_20261009_heterotic_benchmark_full_roots.json'
    p.write_text(json.dumps(result,indent=2)+'\n')
