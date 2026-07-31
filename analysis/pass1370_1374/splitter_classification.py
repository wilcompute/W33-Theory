#!/usr/bin/env python3
"""Exhaustive support-minimal classification of Schur-defect splitters."""
from __future__ import annotations
import collections, hashlib, itertools, json
import numpy as np

P=1000003
class Basis:
    def __init__(self): self.piv={}; self.v=[]
    def add(self,row):
        x=np.array(row,dtype=np.int64)%P
        for j in sorted(self.piv):
            if x[j]: x=(x-int(x[j])*self.piv[j])%P
        nz=np.flatnonzero(x)
        if not len(nz): return False
        j=int(nz[0]); x=x*pow(int(x[j]),-1,P)%P
        for q,old in list(self.piv.items()):
            if old[j]: self.piv[q]=(old-int(old[j])*x)%P
        self.piv[j]=x; self.v.append(x); return True

def analyze(g, core):
    shell=[next(s for s,R in enumerate(g['relations']) if R[0,i]) for i in range(120)]
    blocks=collections.defaultdict(list)
    for k,(i,j) in enumerate(g['reps']): blocks[shell[i],shell[j]].append(k)
    transpose=[int(g['label'][j,i]) for i,j in g['reps']]
    tcols=np.array(g['T_evals'].tolist(),dtype=np.int64).T%P
    A=np.array([int(g['A'][i,j])%P for i,j in g['reps']],dtype=np.int64)
    D=np.array([int(g['D'][i,j])%P for i,j in g['reps']],dtype=np.int64)
    def mul(l,r): return core.mul_mod(g,l,r,P)
    def closure(extra):
        basis=Basis()
        for v in tcols: basis.add(v)
        ex=np.zeros(83,dtype=np.int64)
        for k in extra: ex[k]=1
        queue=collections.deque()
        if basis.add(ex): queue.append(basis.v[-1])
        gens=[A,D,ex]
        while queue:
            v=queue.popleft()
            for h in gens:
                for z in (mul(v,h),mul(h,v)):
                    if basis.add(z): queue.append(basis.v[-1])
        return len(basis.v)
    b22=blocks[2,2]; b44=blocks[4,4]
    single={k:closure([k]) for k in b22+b44}
    records=[]
    for a,b in itertools.product(b22,b44):
        records.append({'a':a,'b':b,'dimension':closure([a,b]),
            'support':len(g['orbits'][a])+len(g['orbits'][b]),
            'symmetric':transpose[a]==a and transpose[b]==b,
            'a_size':len(g['orbits'][a]),'b_size':len(g['orbits'][b])})
    full=[r for r in records if r['dimension']==83]; minimum=min(r['support'] for r in full)
    mins=[r for r in full if r['support']==minimum]
    symmetric=[r for r in full if r['symmetric']]
    symsets=[]; seen=set()
    for a,b in itertools.product(b22,b44):
        extra=tuple(sorted({a,transpose[a],b,transpose[b]}))
        if extra in seen: continue
        seen.add(extra)
        symsets.append({'orbitals':list(extra),'dimension':closure(extra),
            'support':sum(len(g['orbits'][k]) for k in extra)})
    symfull=[r for r in symsets if r['dimension']==83]; symmin=min(r['support'] for r in symfull)
    result={
      'block_22':[{'orbital':k,'size':len(g['orbits'][k]),'transpose':transpose[k],'single_closure_dimension':single[k]} for k in b22],
      'block_44':[{'orbital':k,'size':len(g['orbits'][k]),'transpose':transpose[k],'single_closure_dimension':single[k]} for k in b44],
      'ordered_orbital_pairs_tested':len(records),'full_completion_pairs':len(full),
      'minimum_support_arbitrary':minimum,'minimum_arbitrary_pairs':mins,
      'symmetric_single_orbital_pairs_full':len(symmetric),
      'minimum_support_two_symmetric_orbitals':min(r['support'] for r in symmetric),
      'minimum_two_symmetric_pairs':[r for r in symmetric if r['support']==min(x['support'] for x in symmetric)],
      'transpose_closed_generators_tested':len(symsets),'transpose_closed_full':len(symfull),
      'minimum_support_transpose_closed':symmin,
      'minimum_transpose_closed_generators':[r for r in symfull if r['support']==symmin],
      'previous_splitter':[18,63],'previous_splitter_support':len(g['orbits'][18])+len(g['orbits'][63]),
      'geometric_minimum_splitters':[
        {'orbitals':[18,63],'description':'intersecting-shell transport splitter plus equal pulled-back partners'},
        {'orbitals':[18,64],'description':'intersecting-shell transport splitter plus base-matched pulled-back partners'},
      ],
    }
    raw=json.dumps(result,sort_keys=True,separators=(',',':')); result['sha256']=hashlib.sha256(raw.encode()).hexdigest()
    return result
