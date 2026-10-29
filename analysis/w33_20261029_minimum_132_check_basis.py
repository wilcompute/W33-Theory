#!/usr/bin/env python3
"""Exact minimum total-weight stabilizer generator basis for W33 CSS.
Also exhibits single-ancilla hook faults beyond t=2 correction.
"""
import itertools,json
from collections import Counter

CHECKS_HEX=['0x101072041','0x8040201f','0x8812140060','0x312220a00',
'0x31c0020104','0x5044090060','0x424c80082','0x244400ca00',
'0x40201010b8','0x882800c480','0x2049410402','0x2428220060',
'0x100804391','0x9282080402','0x84011b004','0x80b1184644']

def graph():
 def norm(v):
  u=pow(next(x for x in v if x),-1,3)
  return tuple(x*u%3 for x in v)
 P=sorted({norm(v) for v in itertools.product(range(3),repeat=4) if any(v)})
 def B(x,y):return (x[0]*y[1]-x[1]*y[0]+x[2]*y[3]-x[3]*y[2])%3
 A=[sum(1<<j for j,y in enumerate(P) if i!=j and B(x,y)==0) for i,x in enumerate(P)]
 assert len(A)==40 and all(x.bit_count()==12 for x in A)
 return A

def basis(W):
 B={}
 for a in W:
  x=a
  while x:
   p=x.bit_length()-1
   if p in B:x^=B[p]
   else:B[p]=x;break
 return list(B.values())

def syndrome(A,x):
 return sum(((r&x).bit_count()%2)<<j for j,r in enumerate(A))

def verify():
 A=graph();C=basis(A)
 assert len(C)==16
 words=[0]
 for b in C:words += [x^b for x in words]
 hist=Counter(x.bit_count() for x in words)
 expected={0:1,8:45,12:1120,16:15570,20:32064,24:15570,28:1120,32:45,40:1}
 assert hist==expected
 octads=[x for x in words if x.bit_count()==8]
 assert len(basis(octads))==15
 M=[int(x,16) for x in CHECKS_HEX]
 assert [x.bit_count() for x in M]==[8]*15+[12]
 assert len(basis(M))==16
 assert all(syndrome(A,x)==0 for x in M)
 assert sum(x.bit_count() for x in M)==132
 degrees=[sum((x>>i)&1 for x in M) for i in range(40)]
 assert max(degrees)==5 and min(degrees)>=2
 leader={0:0}
 for w in (1,2):
  for indices in itertools.combinations(range(40),w):
   e=sum(1<<j for j in indices);s=syndrome(A,e)
   assert s not in leader
   leader[s]=e
 assert len(leader)==821
 # For a naive Z stabilizer measurement (data control, one ancilla target),
 # Z on the ancilla spreads onto the last 3 data controls.
 # No weight-3 syndrome can equal a <=2 error syndrome when d(ker A)>=6.
 hooks=[]
 for h in M:
  sites=[j for j in range(40) if h>>j&1]
  suffix=sum(1<<j for j in sites[-3:])
  assert suffix.bit_count()==3 and syndrome(A,suffix) not in leader
  hooks.append(dict(check=hex(h),last_three_sites=sites[-3:],
                    full_syndrome=hex(syndrome(A,suffix))))
 return dict(status='PASS',n=40,stabilizer_rank=16,logical_qubits=8,
             codeword_weight_histogram=dict(sorted(hist.items())),
             minimum_total_check_weight=132,comparison_row_basis_weight=192,
             fraction_couplings_saved=0.3125,
             count_weight8=45,weight8_span_rank=15,
             check_masks_hex=CHECKS_HEX,per_qubit_check_incidences=degrees,
             max_incidence=5,uncorrectable_hook_examples=len(hooks),
             first_hook=hooks[0],scope='One Pauli sector; ideal syndrome, no full fault-tolerant extraction or noise threshold.')

if __name__=='__main__':print(json.dumps(verify(),indent=2))
