#!/usr/bin/env python3
"""Exhaustive stage-4 Hessian compiler and metric-entropy negative control.

Works with 236359 exact representatives of H (D N)^4 and all 648
left-H factors: 153,160,632 unique matrices, per seeded target. Four-stage
matrix cardinality is rechecked by integer double-coset classification.
The torus packing bound is a weak rigorous no-uniform-accuracy statement.
"""
from __future__ import annotations
from pathlib import Path
import json,math
import numpy as np
from scipy.stats import unitary_group
import toe_20261122_stage3_hessian_exact as T
import toe_20261122_further_two_D_exact as E
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_round5_hessian_stage4_compiler.json'

def packing(N,eps,a=math.pi/24):
    # Diagonal special-unitary torus T(theta)=diag(e^i theta_1,
    # e^i theta_2,e^i theta_3,e^-i sum(theta)). Grid inside [-a,a]^3.
    # For distinct points separated by s in at least one parameter,
    # some pair of relative eigenphases differs by >=s. Since all
    # relative differences <=8a < pi, chord >=2*s/pi.
    # d=sqrt(2-2|Tr(U^dagger V)|/4)>=s/(2*pi).
    # If s >4*pi*eps, disjoint eps-balls about grid points.
    s=4*math.pi*eps*1.001
    k=math.floor(2*a/s)+1
    return dict(epsilon=eps,grid_side=k,grid_points=k**3,
                stage4_count=N,strict_packing_obstruction=k**3>N,
                lower_bound_distinct_target_separation=s/(2*math.pi))

def verify():
    words,nidx,H,D,_,R3,v=T.candidates()
    chosen3,info3=T.partition_left_H(R3,H,v,729)
    assert len(chosen3)==12027
    DN=E.mulz(D,H[nidx])
    R4=E.mulz(R3[np.array(chosen3)][:,None],DN[None,:]).reshape(-1,4,4,2)
    chosen4,info4=T.partition_left_H(R4,H,v,6561)
    assert len(chosen4)==236359
    count=len(chosen4)*648
    assert count==153160632
    # Limit numerical benchmark to the same three seeded Haar targets
    # used in previous one-/two-/three-stage exhaustive comparisons.
    rep=T.complex_matrix(R4[np.array(chosen4)],6561)
    group=T.complex_matrix(H,3)
    rng=np.random.default_rng(20261122)
    targets=[unitary_group.rvs(4,random_state=rng) for _ in range(3)]
    out=[]
    for ix,U in enumerate(targets):
        left=(U.conj().T@group).reshape(648,16)
        best=(-1.,None,None)
        for start in range(0,len(rep),2048):
            block=rep[start:start+2048]
            # tr(U^dagger H R) = <(U^dagger H)^T, R> without conjugation
            products=left@block.transpose(0,2,1).reshape(-1,16).T
            score=np.abs(products)/4.
            flat=np.argmax(score)
            h,j=np.unravel_index(int(flat),score.shape)
            if score[h,j]>best[0]:best=(float(score[h,j]),int(h),int(start+j))
        overlap,hi,ri=best
        assert hi is not None
        num=float(abs(np.trace(U.conj().T@group[hi]@rep[ri]))/4)
        assert abs(num-overlap)<2e-12,(num,overlap)
        d=math.sqrt(max(0.,2-2*overlap))
        out.append(dict(target_index=ix,projective_trace_overlap=overlap,
             projective_Frobenius_distance=d,
             process_infidelity=1-overlap**2,
             H_word=words[hi][0],coset_rep_position=ri,
             checked_distinct_matrices=count))
    prev=[.3283394617549869,.45381311536491464,.4653453895703442]
    for row,previous in zip(out,prev):
        row['previous_exact_stage3_distance']=previous
        row['best_through_stage4_inclusive']=min(previous,row['projective_Frobenius_distance'])
    grid=[packing(count,x) for x in (1e-5,3e-5,4e-5)]
    assert grid[0]['strict_packing_obstruction'] and grid[1]['strict_packing_obstruction']
    assert not grid[2]['strict_packing_obstruction']
    return dict(status='PASS_EXACT_HESSIAN_STAGE4_ALL_MATRICES_HAAR_BENCHMARK_AND_TORUS_PACKING',
      stage4_exact_left_H_cosets=len(chosen4),stage4_matrices=count,
      exact_classification=info4,
      three_Haar_target_exhaustive_benchmarks=out,
      compact_diagonal_SU4_torus_packing=grid,
      packing_proof='For diagonal SU4 targets with 3 independent phases in [-pi/24,pi/24], projective Frobenius distance between grid neighbors with phase step s is at least s/(2pi). An epsilon-net of N gates needs at least as many gates as any grid with >2epsilon separation. If grid count>N, worst-case error>epsilon. This is deliberately a very weak 3D subtorus bound, not the 15D volume bound.',
      warning='Target-specific exhaustive finite-depth compiler; counts finite unique complex matrices (up to left H accounting), not synthesized fault-tolerant operations. No scaling guarantee, global shortest gate words or physical throughput certificate.')
if __name__=='__main__':
 d=verify();OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');print(d['status']);print([(z['target_index'],z['projective_Frobenius_distance']) for z in d['three_Haar_target_exhaustive_benchmarks']])
