#!/usr/bin/env python3
"""F8: sample uncovered rank-5 isotropic subgroups and all 3 logical Pauli
coset cover counts, checking whether the prior [3,3,3] is universal.
Uses only exact F8 multiplication, trace and binary arrays.
"""
from collections import Counter
import json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261115_F8_mixed_purity_stabilizer_falsifier as base
OUT=ROOT/"data"/"toe_20261115_F8_rank5_logical_coset_census.json"
def run(trials=200,seed=6261):
  rng=np.random.default_rng(seed)
  hist=Counter();groups=0;ex={}
  for attempt in range(trials):
    basis=[];span=np.array([0],dtype=np.int64)
    for k in range(5):
      opts=base.candidates(span,basis)
      if not len(opts):break
      j=int(rng.choice(opts))
      basis.append(j)
      span=np.r_[span,span^j]
    if len(basis)!=5:continue
    assert len(set(span))==32 and not any(base.covered[s] for s in span if s)
    comm=np.ones(4096,dtype=bool)
    for b in basis:comm&=base.symp(b)
    assert int(comm.sum())==128
    unseen=set(int(z) for z in np.flatnonzero(comm))
    counts=[]
    while unseen:
      rep=min(unseen);coset={rep^int(s) for s in span}
      assert coset<=unseen
      unseen-=coset
      if rep not in span:counts.append(int(sum(base.covered[v] for v in coset)))
    assert len(counts)==3
    val=tuple(sorted(map(int,counts)))
    hist[val]+=1;groups+=1
    if val not in ex:ex[val]={"basis":basis,"counts":counts}
  assert groups>100
  result={"status":"FINITE_FIELD_UNCOVERED_RANK5_LOGICAL_COSET_CENSUS",
          "trials_requested":trials,"rank5_codes_found":groups,
          "logical_count_types":{"-".join(map(str,k)):v for k,v in sorted(hist.items())},
          "examples":{"-".join(map(str,k)):v for k,v in ex.items()},
          "scope":"Independent finite-field randomized census; not an exhaustive classification nor a global pure-state bound."}
  OUT.write_text(json.dumps(result,indent=2)+"\n")
  return result
if __name__=="__main__":
  print(json.dumps(run(),indent=2),flush=True)
