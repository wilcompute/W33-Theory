#!/usr/bin/env python3
"""Seven-flag W33 syndrome extraction with a two-fault recovery certificate.

For EACH of sixteen independent Z checks, enumerate all zero, one, and two
fault histories from listed circuit fault locations. Key the observed record by
(ideal subsequent complete X/Z syndrome, all seven flag X measurements,
 current syndrome-ancilla Z measurement). Require a unique final DATA
Pauli coset modulo the full X/Z W33 CSS stabilizers for each record.

Scope: one check at a time, ideal later full syndrome, independent Pauli faults,
no leakage, no cross-check propagation, no noisy multi-round decoder.
"""
from collections import Counter
from itertools import combinations,product
import json
from w33_20261029_minimum_132_check_basis import CHECKS_HEX,graph
DATA=(1<<40)-1
F=7
# 7-label nonlinear binary code in F2^7:
# pairwise Hamming distance >=3; all pairwise XORs distinct (Sidon).
LABELS=[0,30,84,113,109,43,67]
LABELS_W8=[0,30,84,113,67]

def cert_labels():
 assert min((a^b).bit_count() for a,b in combinations(LABELS,2))==3
 xors=[a^b for a,b in combinations(LABELS,2)]
 assert len(set(xors))==len(xors)==21

def gates_for(h):
 sites=[j for j in range(40) if h>>j&1]
 groups=[sites[i:i+2] for i in range(0,len(sites),2)]
 labels=LABELS if h.bit_count()==12 else LABELS_W8
 assert 1<=len(groups)<len(labels)
 active=0;gates=[]
 for idx,group in enumerate(groups):
  target=labels[idx+1]
  for f in range(F):
   if ((active^target)>>f)&1:gates.append((41+f,40))
  active=target
  gates.extend((j,40) for j in group)
 for f in range(F):
  if (active>>f)&1:gates.append((41+f,40))
 assert len(gates) in (24,34)
 return gates

def after_gates(x,z,gates,start):
 for c,t in gates[start:]:
  if (x>>c)&1:x ^=1<<t
  if (z>>t)&1:z ^=1<<c
 return (x,z)

def fault_catalog(gates):
 out=[]
 # Nonidentity two-qubit Pauli errors after each CNOT.
 for pos,(a,b) in enumerate(gates):
  for pa,pb in product(range(4),repeat=2):
   if not(pa|pb):continue
   x=((pa&1)<<a)|((pb&1)<<b)
   z=(((pa>>1)&1)<<a)|(((pb>>1)&1)<<b)
   x,z=after_gates(x,z,gates,pos+1)
   out.append((x,z,("CNOT",pos,pa,pb)))
 # Pauli faults immediately following preparation of the syndrome and flags.
 for a in range(40,41+F):
  for pa in (1,2,3):
   x,z=after_gates((pa&1)<<a,((pa>>1)&1)<<a,gates,0)
   out.append((x,z,("prep",a,pa)))
 # Classical readout flips (X on measured-Z syndrome or Z on measured-X flag).
 out.append((1<<40,0,("syndrome_readout",)))
 for a in range(41,41+F):out.append((0,1<<a,("flag_readout",a)))
 # Data Pauli before the check, or after the check; arbitrary intermediate
 # data fault is equivalent to one of these since each data is coupled once.
 for a in range(40):
  for pa in (1,2,3):
   x,z=after_gates((pa&1)<<a,((pa>>1)&1)<<a,gates,0)
   out.append((x,z,("data_before",a,pa)))
   out.append(((pa&1)<<a,((pa>>1)&1)<<a,("data_after",a,pa)))
 return out

def independent_basis(rows):
 piv={}
 for v in rows:
  while v:
   p=v.bit_length()-1
   if p in piv:v^=piv[p]
   else:piv[p]=v;break
 return piv

def canonical(word,piv,desc):
 for k in desc:
  if (word>>k)&1:word^=piv[k]
 return word

def syndrome(word,rows):
 v=0
 while word:
  bit=word&-word;j=bit.bit_length()-1
  v^=rows[j]
  word^=bit
 return v

def check_one(h,rows,piv,desc):
 gates=gates_for(h)
 faults=fault_catalog(gates)
 outcomes={}
 histories=0
 for i in range(-1,len(faults)):
  if i<0:x1=z1=0
  else:x1,z1,*_=faults[i]
  for j in range(i+1,len(faults)):
   x2,z2,*_=faults[j]
   x=x1^x2;z=z1^z2
   xd=x&DATA;zd=z&DATA
   record=(syndrome(xd,rows),syndrome(zd,rows),
           (z>>41)&((1<<F)-1),(x>>40)&1)
   class_key=(canonical(xd,piv,desc),canonical(zd,piv,desc))
   if record in outcomes:
    assert outcomes[record]==class_key,(
       "Ambiguous recovery",hex(h),i,j,record,outcomes[record],class_key)
   else:outcomes[record]=class_key
   histories+=1
 n=len(faults)
 assert histories==n*(n+1)//2
 return dict(weight=h.bit_count(),CNOT_count=len(gates),
   elementary_fault_cases=n,histories=histories,
   unique_recovery_records=len(outcomes),ambiguous_recovery_records=0)

def verify():
 cert_labels()
 rows=graph();piv=independent_basis(rows);assert len(piv)==16
 desc=sorted(piv,reverse=True)
 results=[check_one(int(h,16),rows,piv,desc) for h in CHECKS_HEX]
 out=dict(status="PASS_WITH_EXPLICIT_SCOPE",
   code="W33 binary adjacency CSS [[40,8,6]]",
   flag_ancillas=F,syndrome_ancillas_per_check=1,
   Hamming_distance_of_code_labels=3,Sidon_pair_differences=21,
   check_count=len(results),total_CNOTs=sum(r["CNOT_count"] for r in results),
   total_elementary_fault_cases=sum(r["elementary_fault_cases"] for r in results),
   histories_examined=sum(r["histories"] for r in results),
   ambiguous_recovery_records=sum(r["ambiguous_recovery_records"] for r in results),
   results=results,
   fault_model="Each check independently: 15 Pauli CNOT faults per gate, 3 Pauli faults per syndrome/flag preparation, 1 readout-bit fault per ancilla, and 3 Pauli faults on each data site just before/after its one CNOT; every pair of distinct catalog entries plus zero faults.",
   observation="Perfect subsequent full 40-bit X/Z syndrome, current check readout, seven flag X readouts.",
   recovery_equivalence="Pair of data Pauli X,Z masks modulo full rank-16 X/Z W33 CSS stabilizers.",
   boundary="No claim of complete multi-check two-fault correction, syndrome-round noise, inter-check faults, repeated noisy measurements, leakage or full logical FT.")
 assert out["total_CNOTs"]==394
 assert out["total_elementary_fault_cases"]==10262
 assert out["histories_examined"]==3306573
 assert out["ambiguous_recovery_records"]==0
 return out
if __name__=="__main__":print(json.dumps(verify(),indent=2))
