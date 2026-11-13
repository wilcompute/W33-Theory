#!/usr/bin/env python3
"""Independent bitset exact-cover search for 5-qubit size-eight Pauli MUB.

Two S3 representative classes, each after fixed 0,infinity,I,S2 anchors,
using Python arbitrary-precision integer bitsets rather than the parent
NumPy all-pairs branch matrix. Exhaustive if no timeout; otherwise UNDECIDED.
"""
from pathlib import Path
from collections import Counter
import sys,time,json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_five_qubit_size8_dlx as DLX
OUT=ROOT/"data/toe_20261113_fivequbit_two_s3_classes_bitset_search.json"

def prepare(s2,cache):
    pos,sing,ns,I,candidates,reps=cache
    universe=ns[~sing[ns^I]&~sing[ns^s2]&(ns!=I)&(ns!=s2)]
    n=len(universe)
    assert n==2336 and s2 in reps
    compat=[]
    for a in universe:
        raw=~sing[universe ^ a]
        raw[universe==a]=False
        packed=np.packbits(raw.astype(np.uint8),bitorder="little")
        compat.append(int.from_bytes(packed.tobytes(),"little"))
    return I,universe,compat,(1<<n)-1

def run_rep(s2,cache,seconds):
    I,universe,compat,allbits=prepare(s2,cache)
    start=time.perf_counter()
    state={"nodes":0,"timeout":False,"found":None,"deepest":2,"leaf_uncovered":[],"best_uncovered":len(universe)}
    n=len(universe)
    def indices(bits):
        while bits:
            q=bits&-bits
            yield q.bit_length()-1
            bits-=q
    def rec(chosen,R,C,remaining):
        if state["found"] is not None or state["timeout"]:return
        state["nodes"]+=1
        if state["nodes"]%1024==0 and time.perf_counter()-start>=seconds:
            state["timeout"]=True
            return
        state["deepest"]=max(state["deepest"],len(chosen))
        rlen=R.bit_count()
        state["best_uncovered"]=min(state["best_uncovered"],rlen)
        if R==0:
            if remaining==0:state["found"]=chosen.copy()
            return
        if remaining<=0 or C==0:return
        # Any unhit R can be chosen as the exact-cover pivot. Sampling the
        # first 40 R bits gives a fast, complete, if weaker, branching order.
        best=None
        for t,r in enumerate(indices(R)):
            killers=C&~compat[r]
            count=killers.bit_count()
            if count==0:return
            if best is None or count<best[0]:
                best=(count,r,killers)
            if count<=2 or t>=39:break
        count,r,killers=best
        # Branch over every killer, excluding prior sibling branches to
        # avoid duplication (same rule as the validated original DLX).
        ordered=list(indices(killers))
        ordered.sort(key=lambda c:(R&compat[c]).bit_count()) # max coverage first
        excluded=0
        for c in ordered:
            child_candidates=(C&compat[c])&~excluded
            child_R=R&compat[c]
            rec(chosen+[int(universe[c])],child_R,child_candidates,remaining-1)
            if state["found"] is not None or state["timeout"]:return
            excluded|=1<<c
    rec([int(I),int(s2)],allbits,allbits,4)
    elapsed=round(time.perf_counter()-start,2)
    out={"s2":int(s2),"status":"exists" if state["found"] else ("undecided" if state["timeout"] else "none"),
         "nodes":state["nodes"],"elapsed_seconds":elapsed,
         "wall_limit_seconds":seconds,"timeout":state["timeout"],
         "deepest":state["deepest"],"lowest_uncovered_count_seen":state["best_uncovered"],
         "example":state["found"]}
    if state["found"]:
        chosen=state["found"]
        assert len(chosen)==6
        for a in chosen:
            for b in chosen:
                if a!=b: assert not sing[a^b]
        for t in ns:
            assert t in chosen or any(sing[t^c] for c in chosen)
    if out["status"]=="none":
        assert not out["timeout"]
    return out

def main():
    prep=DLX.prep(5)
    reps=prep[-1]
    assert reps==[692,693,694,695,700,701,702,703]
    outputs=[]
    for r in (692,694):
        v=run_rep(r,prep,45)
        outputs.append(v)
        print("REP",r,json.dumps({k:v[k] for k in ("status","nodes","elapsed_seconds","deepest","lowest_uncovered_count_seen")}),flush=True)
    found=next((r["example"] for r in outputs if r["example"]),None)
    status="exists" if found else ("undecided" if any(r["timeout"] for r in outputs) else "none")
    res={"schema":"toe.size8_twoS3_orbit_bitset.v1",
         "status":status,"algorithm":"bounded exact-cover branching with Python integer compatibility bitsets; 40-candidate pivot sampling changes performance, NOT completeness when fully searched",
         "two_S3_orbit_representatives":[692,694],
         "rank_code_uncovered_after_I_s2":2336,
         "states":outputs,"example":found,
         "logic":"If any timeout, status remains undecided; no negative conclusion. Independent algorithm from vectorized numpy DLX."}
    OUT.write_text(json.dumps(res,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return res
if __name__=="__main__":main()
