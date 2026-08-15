#!/usr/bin/env python3
"""Pass5447: q=5 K0 weight-1040 support reduction.

A weight-1040 K0 word would have exactly 26 active P blocks, each carrying a
local even minimum word of weight40 (Pass5268).  Pass5262 says every weight-8
footprint-dual shell support D meets any nonzero K0 block support S in t_D != 1.
The complete shell has replication600 and pair codegrees, from Pass5236,

  R1:25,  R2:5,  R3:0,

where the three relations have valencies144,120,60.

For |S|=26 let a,b,c be the numbers of internal unordered pairs in R1,R2,R3.
Then a+b+c=325 and

  sum_D t_D = 600*26 = 15600,
  sum_D C(t_D,2) = 25a+5b.

Since t_D is never1, C(t_D,2)>=t_D/2, so 4a-c>=1235.
The 3-class association scheme has nonprincipal relation eigenvalue rows

  (R1,R2,R3)=(14,-10,-5), (-6,-5,10), (-6,10,-5)

with multiplicities90,104,130.  Delsarte positivity for a 26-set gives

  u1=a/10-39/5 >=0,
  u2=2c/15-26/75 >=0,
  u3=481/15-a/10-2c/15 >=0.

Together with a+b+c=325 this leaves exactly 21 integer profiles, all with
310<=a<=316 and only9..15 non-R1 pairs.

The producer also reconstructs the complete Pass5230 weight-8 shell and checks
all 156 known 25-block point footprints extended by one extra block.  None of the
46,800 extensions satisfies the no-singleton condition.  Hence any weight1040
candidate, if it exists, is an exotic 26-support rather than a minimum footprint
plus one block.
"""
from __future__ import annotations
import json
from pathlib import Path
from analysis import w33_pass5230_5237_footprint_rank4_breakthrough as p5230
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5447_Q5_K0_WEIGHT1040_SUPPORT_REDUCTION.json'

def feasible_profiles():
    out=[]
    for a in range(326):
        for c in range(326-a):
            b=325-a-c
            if 4*a-c < 1235: continue
            # u2>=0 is equivalent to c>=13/5, hence integer c>=3.
            if c < 3: continue
            # 30*u3 = 962-3a-4c.
            if 3*a+4*c > 962: continue
            u1=(a-78)/10
            u2=2*c/15-26/75
            u3=481/15-a/10-2*c/15
            assert min(u1,u2,u3)>=-1e-12
            out.append((a,b,c,25*a+5*b))
    return out

def main():
    prof=feasible_profiles()
    assert len(prof)==21
    assert min(a for a,b,c,s2 in prof)==310 and max(a for a,b,c,s2 in prof)==316
    assert min(b+c for a,b,c,s2 in prof)==9 and max(b+c for a,b,c,s2 in prof)==15

    O8=list(p5230.O8);F=p5230.F
    point_footprints=[set(F[p].nonzero()[0]) for p in range(F.shape[0])]
    assert len(point_footprints)==156 and {len(S) for S in point_footprints}=={25}
    def no_singleton(S):
        return all(sum(j in S for j in D)!=1 for D in O8)
    assert all(no_singleton(S) for S in point_footprints)
    tested=0;survivors=[]
    for p,S in enumerate(point_footprints):
        for u in range(325):
            if u in S: continue
            tested+=1
            T=S|{u}
            if no_singleton(T): survivors.append((p,u))
    assert tested==156*300==46800 and survivors==[]

    out={
      'pass':5447,'status':'THEOREM_Q5_K0_WEIGHT1040_SUPPORT_STRICT_REDUCTION',
      'candidate_block_support_size':26,
      'required_local_weight_per_active_block':40,
      'weight8_shell_checks':24375,
      'no_singleton_moment_inequality':'4a-c>=1235',
      'relation_pair_counts':'a+b+c=325 for R1(codegree25), R2(codegree5), R3(codegree0)',
      'delsarte_projection_norms':{
        'u1':'a/10-39/5','u2':'2c/15-26/75','u3':'481/15-a/10-2c/15'},
      'feasible_integer_profile_count':len(prof),
      'feasible_profiles_abcs2':[list(x) for x in prof],
      'R1_pair_range':[min(x[0] for x in prof),max(x[0] for x in prof)],
      'non_R1_pair_range':[min(x[1]+x[2] for x in prof),max(x[1]+x[2] for x in prof)],
      'point_footprint_plus_one_extensions_tested':tested,
      'point_footprint_plus_one_survivors':0,
      'conclusion':'Any weight1040 K0 word must use an exotic 26-block support with one of only21 association-scheme pair profiles; it cannot be a known 25-block point footprint plus one block.',
      'boundary':'This does not prove weight1040 nonexistent. The remaining task is to classify exotic26 supports and impose the 180-state local K6,6 minimum-word connected-L syndrome constraints.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
