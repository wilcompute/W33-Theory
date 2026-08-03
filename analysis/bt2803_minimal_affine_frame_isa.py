#!/usr/bin/env python3
from __future__ import annotations
import itertools,json
from collections import Counter,deque
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];Q=3
I=tuple(tuple(int(i==j) for j in range(4)) for i in range(4))
G={
'F_p':((0,2,0,0),(1,0,0,0),(0,0,1,0),(0,0,0,1)),
'F_f':((1,0,0,0),(0,1,0,0),(0,0,0,2),(0,0,1,0)),
'S_p':((1,0,0,0),(1,1,0,0),(0,0,1,0),(0,0,0,1)),
'S_f':((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,1,1)),
'CX_pf':((1,0,0,0),(0,1,0,2),(1,0,1,0),(0,0,0,1)),
'CX_fp':((1,0,1,0),(0,1,0,0),(0,0,1,0),(0,2,0,1))}
def mm(a,b):return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(4))%3 for j in range(4)) for i in range(4))
def mv(a,v):return tuple(sum(a[i][k]*v[k] for k in range(4))%3 for i in range(4))
def closure(gs,lengths=False):
 d={I:0};q=deque([I])
 while q:
  x=q.popleft()
  for g in gs:
   y=mm(g,x)
   if y not in d:d[y]=d[x]+1;q.append(y)
 return d if lengths else set(d)
def span(vs):
 s={(0,0,0,0)}
 for v in vs:s|={tuple((x[i]+a*v[i])%3 for i in range(4)) for x in tuple(s) for a in (1,2)}
 return s
def main():
 names=list(G);triples=[]
 for c in itertools.combinations(names,3):
  if len(closure([G[x] for x in c]))==51840:triples.append(c)
 assert len(triples)==6 and not any(len(closure([G[x] for x in c]))==51840 for c in itertools.combinations(names,2))
 chosen=('F_p','CX_pf','CX_fp');d=closure([G[x] for x in chosen],True);dist=Counter(d.values())
 orbit={mv(g,(0,1,0,0)) for g in d};translations=span(orbit)
 checks={'six_minimal_triples':len(triples)==6,'chosen_order_51840':len(d)==51840,'orbit_80':len(orbit)==80,'translation_span_81':len(translations)==81,'affine_order_4199040':len(d)*len(translations)==4199040}
 assert all(checks.values())
 out={'schema':'w33.pass2803.minimal_affine_frame_isa.v1','status':'EXACT','minimal_linear_generators':3,'minimal_triples':[list(x) for x in triples],'selected_micro_isa':['F_p','CX_pf','CX_fp','Z_p'],'linear_order':len(d),'affine_order':len(d)*len(translations),'word_lengths':{'mean':sum(d.values())/len(d),'maximum':max(d.values()),'distribution':{str(k):dist[k] for k in sorted(dist)}},'boundary':'The four-operation 2-bit engine is an internal micro-ISA. Removing Z_f removes a register-select subencoding, not by itself a public 3-bit opcode.','checks':checks}
 p=ROOT/'data/PART_BT2803_MINIMAL_AFFINE_FRAME_ISA_results.json';p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
