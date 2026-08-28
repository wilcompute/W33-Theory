#!/usr/bin/env python3
"""Pass10901-10908: local 32 extension-pair carrier vs Hall-Janko 32 C13 cycles.

The characteristic-2 local repair pairs the 64 vectors of Fix(u)=F4^3 by a
translation along the unique s-fixed F4 line, where s=n^4 has order3.  Because
u=n^3 acts trivially on Fix(u), the full local C6 action factors through s.

This pass computes the induced permutation on the 32 pair-states exactly and
compares it with the certified C6 action on the 32 Hall-Janko C13 cycles.

Result:
  local pair carrier under s : 1^2 3^10,
  HJ32 under n^2            : 1^5 3^9.
Moreover the local n action has only 1- and3-cycles, whereas HJ32 under n has
1^1 2^2 3^5 6^2.  Thus the two 32-state carriers are inequivalent even before
the order-two defect test of Pass10797.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
import w33_pass10845_10852_normalizer_jordan_pg24 as N
import w33_pass10477_10484_h4_normalizer_27state_quotient as Q
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10901_10908_LOCAL32_VS_HJ32_NORMALIZER_NOGO.json'

def cycprof(p):
    seen=set();out=[]
    for i in range(len(p)):
      if i in seen:continue
      C=[];j=i
      while j not in seen:seen.add(j);C.append(j);j=p[j]
      out.append(len(C))
    return Counter(out)

def main():
    g8,n=N.build_normalizer();u=Q.pw(n,3);s=Q.pw(n,4)
    vecs=[np.array(v,dtype=np.uint8) for v in itertools.product(range(4),repeat=6)]
    F=[v for v in vecs if np.array_equal(Q.mv(u,v),v)];assert len(F)==64
    fi={tuple(map(int,v)):i for i,v in enumerate(F)}
    ps=[fi[tuple(map(int,Q.mv(s,v)))] for v in F]
    fixed=[F[i] for i in range(64) if ps[i]==i]
    a=next(v for v in fixed if any(v))
    trans=[fi[tuple(map(int,v^a))] for v in F]
    # quotient the 64 states by translation pairs
    pairs=[];pid={};seen=set()
    for i in range(64):
      if i in seen:continue
      j=trans[i];C=tuple(sorted((i,j)));seen|=set(C);k=len(pairs);pairs.append(C)
      for x in C:pid[x]=k
    assert len(pairs)==32
    pp=[]
    for C in pairs:
      z={pid[ps[x]] for x in C};assert len(z)==1;pp.append(next(iter(z)))
    local=cycprof(pp);assert local==Counter({3:10,1:2})
    # On Fix(u), u is identity, hence n=su induces the same quotient action.
    pn=[fi[tuple(map(int,Q.mv(n,v)))] for v in F]
    pnp=[]
    for C in pairs:
      z={pid[pn[x]] for x in C};assert len(z)==1;pnp.append(next(iter(z)))
    assert pnp==pp

    old=json.loads((ROOT/'data/PART_W33_PASS10797_10804_HJ32_NORMALIZER_QUOTIENT.json').read_text())
    hj_c6={int(k):int(v) for k,v in old['C6_on_32_C13_cycles']['cycle_counts'].items()}
    assert hj_c6=={1:1,2:2,3:5,6:2}
    # n^2 action on a d-cycle has gcd(d,2) cycles of length d/gcd(d,2)
    hj_c3=Counter()
    import math
    for d,m in hj_c6.items():
      g=math.gcd(d,2);hj_c3[d//g]+=m*g
    assert hj_c3==Counter({3:9,1:5})
    assert local!=hj_c3

    out={
      'schema':'w33.pass10901_10908.local32_vs_hj32_normalizer_nogo.v1','status':'PASS','passes':'10901-10908',
      'local_extension_pair_carrier':{
        'source':'64 vectors Fix(n^3)=F4^3 paired by one nonzero translation on the s-fixed F4 line',
        'states':32,'C6_action_factors_through_C3':True,'C3_profile':'1^2 3^10','full_n_profile':'1^2 3^10'},
      'Hall_Janko_32':{
        'source':'32 C13 cycles on G2(4)/J2','C6_profile':'1^1 2^2 3^5 6^2','C3_profile':'1^5 3^9'},
      'theorem':'The two natural 32-state carriers are not the same normalizer object. The local extension-pair quotient has order-three profile 1^2 3^10 and its C6 action factors through C3, while the Hall-Janko C13-cycle carrier has C3 profile 1^5 3^9 and genuine 2- and 6-cycles under C6. Thus the persistent number32 does not hide an equivariant identification.',
      'boundary':'Exact finite F4 permutation computation using the certified Wilson normalizer plus exact HJ32 class-fusion profile from Pass10797. This rules out equivariant equality of these two specific 32-carriers; it does not rule out a different external 32-dimensional correction module.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','local32':'1^2 3^10','HJ32_C3':'1^5 3^9','equivalent':False}))
if __name__=='__main__':main()
