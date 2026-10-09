"""Joint root-phase histogram of (V,W2,W3), a strict fixed-generator sieve."""
from collections import Counter
import json
from pathlib import Path
from fractions import Fraction as F
import w33_20261009_heterotic_benchmark_full_roots as M
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261009_joint_root_phase_sieve.json'
def joint(vectors):
    out=[]
    for side in (0,8):
        C=Counter()
        for root in M.ROOTS:
            phases=tuple(str(sum(root[i]*v[side+i] for i in range(8))%1) for v in vectors)
            C[phases]+=1
        out.append(C)
    return tuple(sorted(out,key=lambda x: sorted(x.items())))
def main():
    bench={}
    for b,x in M.BENCH.items():
        bench[b]=joint([M.vector(M.BENCH_V),M.vector(x['W2']),M.vector(x['W3'])])
    baseline=joint([M.vector(M.BENCH_V)])
    source=M.analyze()['candidate_model_results']
    result={}
    for name in source:
        data=M.source_model(M.SCAN/(name+'.model'))
        v,third,second=data[0],data[4],data[7]
        sig=joint([v,second,third])
        result[name]=dict(shift_phase_histogram_matches=joint([v])==baseline,
                          joint_phase_histogram_matches=[b for b,bins in bench.items() if sig==bins])
    result0={b:[name for name,r in result.items() if b in r['joint_phase_histogram_matches']] for b in bench}
    report=dict(status='PASS',joint_matches=result0,shift_profile_matches=[name for name,x in result.items() if x['shift_phase_histogram_matches']],
                individual=result,scope='Necessary equivalence for fixed ordered (V,W2,W3) phase characters on all 240 roots of each E8; NO exhaustive orbifold generator/gauge automorphism classification.')
    OUT.write_text(json.dumps(report,indent=2)+'\n')
    print('joint',result0,'V profiles',report['shift_profile_matches'])
if __name__=='__main__':main()
