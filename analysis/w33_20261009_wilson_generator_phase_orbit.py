"""Small declared generator-redefinition orbit: V-> +/-V; W2-> +/-W2+3a V;
W3-> +/-W3+2b V. This is a conservative finite necessary sieve ONLY.
"""
import itertools,json
from fractions import Fraction as F
from pathlib import Path
import w33_20261009_joint_root_phase_sieve as joint
import w33_20261009_heterotic_benchmark_full_roots as B
ROOT=Path(__file__).resolve().parents[1]
def lin(a,v,b,w):
    return tuple(a*x+b*y for x,y in zip(v,w))
def orbit(rows):
    V,W2,W3=rows
    seen=set()
    for signV,sign2,sign3,a,b in itertools.product((-1,1),(-1,1),(-1,1),(0,1),(0,1,2)):
        x=tuple(signV*v for v in V)
        y=lin(sign2,W2,3*a,V)
        z=lin(sign3,W3,2*b,V)
        seen.add(tuple(tuple(sorted(k.items())) for k in joint.joint([x,y,z])))
    return seen
def main():
    bench={}
    for name,x in B.BENCH.items():
        bench[name]=tuple(tuple(sorted(k.items())) for k in joint.joint([B.vector(B.BENCH_V),B.vector(x['W2']),B.vector(x['W3'])]))
    names=list(B.analyze()['candidate_model_results'])
    out={}
    for name in names:
        rows=B.source_model(B.SCAN/(name+'.model'))
        possible=orbit([rows[0],rows[7],rows[4]])
        out[name]=[nameb for nameb,finger in bench.items() if finger in possible]
    matches={b:[n for n,v in out.items() if b in v] for b in bench}
    payload=dict(status='PASS',matches=matches,models=len(names),redefinitions_per_model=48,
       scope='Fixed E8 bases plus +/- generator signs and W2+=3V, W3+=2bV; not a complete Z6-II space-group automorphism or gauge equivalence classification.')
    (ROOT/'data/w33_20261009_wilson_generator_phase_orbit.json').write_text(json.dumps(payload,indent=2)+'\n')
    print(payload)
if __name__=='__main__':main()
