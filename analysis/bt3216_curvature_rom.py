#!/usr/bin/env python3
"""Pass 3216: canonical 876-state curvature-aware Moore quotient and ROM.

The construction is independent of state numbering.  It rebuilds the frozen 48,826
D4 hypothesis universe, computes the 23-row collision classes, forms the recursive
output/action/child signatures, assigns canonical IDs by sorted signature text, and
emits a machine-checkable transition ROM plus a semantic digest.
"""
from __future__ import annotations

import itertools
import json
import math
import hashlib
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
ROM=DATA/'PART_BT3216_CURVATURE_QUOTIENT_ROM.json'
MEM=DATA/'PART_BT3216_CURVATURE_QUOTIENT_ROM.memh'
D4=[(a,b) for a in range(4) for b in range(2)]
DI={g:i for i,g in enumerate(D4)}
ONE=(0,0); FAULTS=[g for g in D4 if g!=ONE]
EDGES=list(itertools.combinations(range(10),2))
TRIANGLES=list(itertools.combinations(range(10),3))
FROZEN23=[(5,6,9),(2,5,9),(4,5,8),(2,4,7),(0,3,6),(0,1,8),
 (1,2,4),(1,3,5),(3,4,8),(0,4,9),(2,3,8),(4,8,9),(1,7,8),
 (1,4,6),(0,2,3),(3,7,9),(1,3,9),(2,6,9),(3,5,7),(0,1,7),
 (3,6,8),(0,4,5),(4,6,7)]
SELECTED=[TRIANGLES.index(t) for t in FROZEN23]
REMAINING=[i for i in range(120) if i not in set(SELECTED)]

def mul(g,h):
 a,b=g;c,d=h
 return ((a+(-1 if b else 1)*c)%4,(b+d)%2)

def inv(g):
 a,b=g
 return ((-((-1 if b else 1)*a))%4,b)

def directed(edge,g,u,v):
 if (u,v)==edge:return g
 if (v,u)==edge:return inv(g)
 return ONE

def syndrome(hyp):
 out=[]
 for i,j,k in TRIANGLES:
  product=ONE
  for u,v in ((i,j),(j,k),(k,i)):
   factor=ONE
   for edge,g in hyp: factor=mul(directed(edge,g,u,v),factor)
   product=mul(factor,product)
  out.append(DI[product])
 return tuple(out)

def universe():
 rows=[tuple()]
 rows.extend(((e,g),) for e in EDGES for g in FAULTS)
 rows.extend(((e,g),(f,h)) for e,f in itertools.combinations(EDGES,2)
             for g in FAULTS for h in FAULTS)
 assert len(rows)==48826
 return rows

def curvature_labels(rows):
 measured=set()
 for t in FROZEN23:
  es=[tuple(sorted(x)) for x in itertools.combinations(t,2)]
  measured.update(tuple(sorted(x)) for x in itertools.combinations(es,2))
 assert len(measured)==69
 def comm(a,b):return mul(mul(mul(a,b),inv(a)),inv(b))
 out=[]
 for row in rows:
  if len(row)!=2:out.append(0);continue
  (e,a),(f,b)=row
  if tuple(sorted((e,f))) not in measured:out.append(0)
  else:out.append(2 if comm(a,b)==(2,0) else 1)
 assert Counter(out)==Counter({0:45445,1:1725,2:1656})
 return out

def choose(indices,full):
 best=None
 for t in REMAINING:
  parts=defaultdict(list)
  for i in indices:parts[int(full[i,t])].append(i)
  key=(-len(parts),max(map(len,parts.values())),t)
  if best is None or key<best[0]:best=(key,t,parts)
 assert best
 return best[1],best[2]

def signature(indices,full,labels):
 hist=Counter(labels[i] for i in indices);typed=(hist[0],hist[1],hist[2])
 if len(indices)<=1:return ('STOP',typed)
 action,parts=choose(indices,full)
 return ('TEST',action,typed,tuple(sorted((o,signature(tuple(ch),full,labels)) for o,ch in parts.items())))

def collect(sig,out):
 out.add(sig)
 if sig[0]=='TEST':
  for _,child in sig[3]:collect(child,out)

def encode_row(row):
 # 102-bit word, LSB first: 8 child IDs x10, valid mask x8,
 # histogram none/flat/curved x2, action x7, terminal x1.
 word=0;shift=0
 trans={int(k):int(v) for k,v in row['transitions'].items()}
 for outcome in range(8):
  word|=(trans.get(outcome,0)&0x3ff)<<shift;shift+=10
 mask=sum(1<<o for o in trans);word|=mask<<shift;shift+=8
 for x in row['curvature_histogram']:
  word|=(int(x)&3)<<shift;shift+=2
 action=127 if row['action'] is None else int(row['action'])
 word|=(action&0x7f)<<shift;shift+=7
 word|=(1 if row['terminal'] else 0)<<shift;shift+=1
 assert shift==102
 return f'{word:026x}'

def main():
 rows=universe();full=np.array([syndrome(r) for r in rows],dtype=np.uint8)
 grouped=defaultdict(list)
 for i,key in enumerate(map(tuple,full[:,SELECTED])):grouped[key].append(i)
 collisions=[tuple(v) for v in grouped.values() if len(v)>1]
 assert len(grouped)==46284 and len(collisions)==1436 and max(map(len,collisions))==3
 labels=curvature_labels(rows)
 initial=[signature(c,full,labels) for c in collisions]
 nodes=set()
 for s in initial:collect(s,nodes)
 assert len(set(initial))==770 and len(nodes)==876
 ordered=sorted(nodes,key=repr);sid={s:i for i,s in enumerate(ordered)}
 rom=[]
 for i,s in enumerate(ordered):
  if s[0]=='STOP':
   row={'state_id':i,'terminal':True,'action':None,'curvature_histogram':list(s[1]),'transitions':{}}
  else:
   row={'state_id':i,'terminal':False,'action':int(s[1]),'curvature_histogram':list(s[2]),
        'transitions':{str(o):sid[ch] for o,ch in s[3]}}
  rom.append(row)
 initial_ids=[sid[s] for s in initial]
 assert len(set(initial_ids))==770
 for row in rom:
  assert sum(row['curvature_histogram']) in (1,2,3)
  assert all(0<=v<876 for v in row['transitions'].values())
 semantic={'states':rom,'initial_state_ids':initial_ids}
 digest=hashlib.sha256(json.dumps(semantic,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 payload={'schema':'w33.pass3216.curvature_quotient_rom.v1','status':'EXACT_SOURCE_ROM',
  'hypotheses':48826,'base_signatures':46284,'collision_classes':1436,
  'unique_initial_states':770,'all_recursive_states':876,'address_bits':10,
  'rom_word_bits':102,'semantic_sha256':digest,'states':rom,'initial_state_ids':initial_ids,
  'bisimulation_certificate':'State identity is equality of the complete recursive Moore signature: output curvature histogram, chosen action, and outcome-indexed child signatures.',
  'boundary':'Exact for the frozen noiseless future-action policy. ROM synthesis, placement and noisy-belief equivalence remain separate evidence gates.'}
 DATA.mkdir(exist_ok=True)
 ROM.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
 MEM.write_text('\n'.join(encode_row(r) for r in rom)+'\n')
 print(json.dumps({'states':876,'initial':770,'sha256':digest},sort_keys=True))
if __name__=='__main__':main()
