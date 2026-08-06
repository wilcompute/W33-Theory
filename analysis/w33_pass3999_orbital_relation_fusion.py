#!/usr/bin/env python3
"""Pass 3999: materialize the literal orbital Fourier table and test relation-level fusion closure."""
from __future__ import annotations
import hashlib, importlib.util, json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FOURIER=ROOT/'data/PART_3983_ORBITAL_CENTRAL_FOURIER.json'
OUT=ROOT/'data/PART_3999_ORBITAL_RELATION_FUSION.json'

def sha(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def load_module():
 p=ROOT/'analysis/w33_pass3983_orbital_central_fourier.py'
 spec=importlib.util.spec_from_file_location('fourier3983',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def normalize_partition(part):return tuple(sorted((tuple(sorted(b)) for b in part),key=lambda b:(b[0],len(b),b)))
def closure_test(part,entries,n=48):
 for ai,A in enumerate(part):
  aset=set(A)
  for bi,B in enumerate(part):
   bset=set(B);row=[Fraction(0) for _ in range(n)]
   for i,j,k,v in entries:
    if i in aset and j in bset:row[k]+=Fraction(v)
   for C in part:
    vals={row[k] for k in C}
    if len(vals)!=1:return False,(ai,bi,C,sorted(map(str,vals)))
 return True,None

def refine(part,entries,n=48):
 part=[tuple(b) for b in part]
 while True:
  signatures={k:[] for k in range(n)}
  for A in part:
   aset=set(A)
   for B in part:
    bset=set(B);row=[Fraction(0) for _ in range(n)]
    for i,j,k,v in entries:
     if i in aset and j in bset:row[k]+=Fraction(v)
    for k in range(n):signatures[k].append(row[k])
  new=[]
  for C in part:
   buckets=defaultdict(list)
   for k in C:buckets[tuple(signatures[k])].append(k)
   new.extend(tuple(v) for _,v in sorted(buckets.items(),key=lambda kv:min(kv[1])))
  new=list(normalize_partition(new))
  if normalize_partition(part)==normalize_partition(new):return new
  part=new

def main():
 m=load_module()
 if not FOURIER.exists():m.main()
 fourier=json.loads(FOURIER.read_text());assert fourier['status']=='PASS'
 tensor=m.unpack_tensor();entries=m.normalize_entries(tensor);assert len(entries)>0
 chars=[[Fraction(x) for x in row] for row in fourier['irreducible_character_table']]
 sig=defaultdict(list)
 for i in range(48):sig[tuple(row[i] for row in chars)].append(i)
 initial=normalize_partition(sig.values());refined=refine(initial,entries);closed,_=closure_test(refined,entries);assert closed
 pairwise=[]
 for a in range(len(refined)):
  for b in range(a+1,len(refined)):
   merged=[refined[i] for i in range(len(refined)) if i not in (a,b)]+[tuple(sorted(refined[a]+refined[b]))]
   merged=normalize_partition(merged);ok,_=closure_test(merged,entries)
   if ok:pairwise.append({'blocks':[a,b],'sizes':[len(refined[a]),len(refined[b])],'rank_after_merge':len(merged)})
 payload={'schema':'w33.pass3999.orbital_relation_fusion.v1','status':'PASS_EXACT_LITERAL_FOURIER_AND_RELATION_FUSION_TEST','fourier_character_table_sha256':fourier['character_table_sha256'],'fourier_idempotent_sha256':fourier['idempotent_sha256'],'simple_degrees':fourier['simple_degrees'],'literal_relations':48,'tensor_nonzeros':len(entries),'equal_character_signature_blocks':[list(b) for b in initial],'equal_character_signature_rank':len(initial),'minimal_closed_refinement':[list(b) for b in refined],'minimal_closed_refinement_rank':len(refined),'pairwise_closed_mergers':pairwise,'pairwise_closed_merger_count':len(pairwise),'boundary':'The minimal closed refinement and listed pairwise mergers are exact relation-level subalgebras of the frozen 48-orbital tensor. This is not an exhaustive enumeration of every set partition of 48 relations unless the refined rank is small enough for a separate exhaustive search.'}
 payload['semantic_sha256']=sha(payload);OUT.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n');print('PASS_ORBITAL_RELATION_FUSION',len(initial),len(refined),len(pairwise),payload['semantic_sha256'])
if __name__=='__main__':main()
