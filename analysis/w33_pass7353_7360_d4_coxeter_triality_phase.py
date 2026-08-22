#!/usr/bin/env python3
"""Pass7353-7360: Coxeter C6 phase reduces selected-D4 triality S3 to a cyclic C3 torsor."""
from __future__ import annotations
import itertools,json
from collections import defaultdict
from pathlib import Path
import sympy as sp
import w33_pass7163_7170_e8_hexagonal_lift as e8
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'data'/'PART_W33_PASS7353_7360_D4_COXETER_TRIALITY_PHASE.json'

def main():
 R,fib,phase,radj,adj,zero,twelve,diff=e8.e8_fibers();I={r:i for i,r in enumerate(R)}
 neg={i:I[tuple(-x for x in R[i])] for i in range(240)};rep=sorted({min(i,neg[i]) for i in range(240)});assert len(rep)==120
 rf={v:f for f,F in enumerate(fib) for v in F};line_fib=[];line_phase=[]
 for r in rep:
  f=rf[r];assert rf[neg[r]]==f and (phase[f][neg[r]]-phase[f][r])%6==3
  line_fib.append(f);line_phase.append(phase[f][r]%3)
 O=[set() for _ in range(120)]
 for i,j in itertools.combinations(range(120),2):
  if e8.dot(R[rep[i]],R[rep[j]])==0:O[i].add(j);O[j].add(i)
 frames=[]
 for a in range(120):
  for b in sorted(x for x in O[a] if x>a):
   X=O[a]&O[b]
   for c in sorted(x for x in X if x>b):
    for d in sorted(x for x in X&O[c] if x>c):frames.append((a,b,c,d))
 assert len(frames)==122850;RS=set(R);d4=[]
 for F in frames:
  V=[R[rep[x]] for x in F];ok=False
  for tail in itertools.product((1,-1),repeat=3):
   sg=(1,)+tail;n=[sum(sg[t]*V[t][k] for t in range(4)) for k in range(8)]
   if all(x%2==0 for x in n) and tuple(x//2 for x in n) in RS:ok=True;break
  if ok:
   S=tuple(i for i,r in enumerate(R) if sum(e8.dot(r,v)**2 for v in V)==64);assert len(S)==24;d4.append((S,F))
 assert len(d4)==9450
 by=defaultdict(list)
 for S,F in d4:by[S].append(F)
 assert len(by)==3150 and set(map(len,by.values()))=={3}
 selected=[];records=[]
 for S,Fs in by.items():
  fsets=[tuple(sorted(line_fib[x] for x in F)) for F in Fs]
  if len(set(fsets))!=1:continue
  assert len(set(fsets[0]))==4;selected.append(S);fib4=fsets[0]
  sig=[]
  for F in Fs:
   q={line_fib[x]:line_phase[x] for x in F};sig.append(tuple(q[f] for f in fib4))
  s0=sig[0];delta={tuple((x-y)%3 for x,y in zip(s,s0)) for s in sig}
  assert delta=={(0,0,0,0),(1,1,1,1),(2,2,2,2)}
  tau=sorted(sum(s)%3 for s in sig);assert tau==[0,1,2]
  records.append({'fibers':list(fib4),'phase_signatures':[list(x) for x in sig],'tau':[sum(x)%3 for x in sig]})
 assert len(selected)==90
 out={'schema':'w33.pass7353_7360.d4_coxeter_triality_phase.v1','status':'PASS','passes':'7353-7360','all_D4':3150,'triality_frames_per_D4':3,'selected_C6_supported_D4':90,'theorem':'For each of the selected 90 D4 subsystems, its three triality frames use the same four Coxeter C6 fibers and their antipodal-pair phases differ by the global shifts 0,1,2 in F3. Thus tau=sum(four phases) mod3 labels the three frames cyclically.','gauge_law':'Rephasing the four C6 fiber origins adds one common constant to all three tau labels, so differences/cyclic order are invariant but absolute tau=0 is not.','symmetry_reduction':'bare D4: S3 torsor -> marked oriented C6 fibration: C3 torsor -> choose a Coxeter phase origin/Weyl-chamber marking: one frame','triality_boundary':'The C6 structure gives a canonical cyclic ordering of v,s,c, not an absolute v/s/c name. A phase-zero/chamber marking is the additional datum required to choose one class.','sample':records[0]}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','D4':3150,'selected':90,'reduction':'S3->C3->1'}))
if __name__=='__main__':main()
