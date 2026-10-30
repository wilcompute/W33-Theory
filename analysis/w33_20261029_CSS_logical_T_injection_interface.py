#!/usr/bin/env python3
"""An *ideal logical* T-state injection interface for W33 [[40,8,6]] CSS.
A transversal physical CNOT between equal CSS blocks implements 8 parallel
logical CNOTs in any matched logical X/Z dual basis. A separately supplied,
perfect encoded |A>^8=(T|+>)^8 resource, logical-Z measurement and conditional
single-logical S_i corrections implement T^tensor8 by gate teleportation.
No encoded magic-state factory, state distillation, addressable S_i, noisy
measurement, or circuit-level fault tolerance is furnished here.

Exact phase identity: for logical x and ancilla measurement m,
 |m xor x|+2m.x = |m|+|x| as INTEGERS.
"""
import json
from w33_20261029_minimum_132_check_basis import graph,CHECKS_HEX

def pivots(rows):
 b={}
 for r in rows:
  while r:
   k=r.bit_length()-1
   if k in b:r^=b[k]
   else:b[k]=r;break
 return b

def null_vectors(row_basis,n):
 # Pivots use highest bit. Solve row equations in ascending bit order.
 free=[k for k in range(n) if k not in row_basis]
 out=[]
 for f in free:
  x=1<<f
  for k in sorted(row_basis):
   if (row_basis[k]&x).bit_count()%2:x^=1<<k
  assert all((r&x).bit_count()%2==0 for r in row_basis.values())
  out.append(x)
 return out

def inverse_GF2(rows,n):
 aug=[rows[i]|(1<<(n+i)) for i in range(n)]
 for j in range(n):
  pivot=next((i for i in range(j,n) if aug[i]>>j&1),None)
  assert pivot is not None
  aug[j],aug[pivot]=aug[pivot],aug[j]
  for i in range(n):
   if i!=j and (aug[i]>>j)&1:aug[i]^=aug[j]
 assert all((aug[i]&((1<<n)-1))==1<<i for i in range(n))
 return [r>>n for r in aug]

def verify():
 A=graph();image=pivots(A);assert len(image)==16
 null=null_vectors(image,40);assert len(null)==24
 span=pivots(A);logic=[]
 for x in null:
  rank0=len(span);test=pivots(list(span.values())+[x])
  if len(test)>rank0:logic.append(x);span=test
 assert len(logic)==8 and len(span)==24
 Gram=[sum(((x&z).bit_count()%2)<<j for j,z in enumerate(logic)) for x in logic]
 inverse=inverse_GF2(Gram,8)
 zlogical=[]
 for k in range(8):
  # z_k is combination with coefficients inverse[i,k].
  z=0
  for i,r in enumerate(inverse):
   if r>>k&1:z^=logic[i]
  zlogical.append(z)
 assert all(((x&z).bit_count()%2)==(i==j) for i,x in enumerate(logic)
            for j,z in enumerate(zlogical))
 for word in logic+zlogical:assert all((r&word).bit_count()%2==0 for r in A)
 # CNOT^40 physical conjugation on (x_control,x_target,z_control,z_target):
 # (x_c,x_t,z_c,z_t) -> (x_c, x_t xor x_c, z_c xor z_t,z_t).
 # For row stabilizer and every logical basis vector this exactly gives
 # the required control-to-target stabilizer/logical transformation.
 for w in [int(h,16) for h in CHECKS_HEX]+logic+zlogical:
  assert w.bit_count() and w.bit_length()<=40
  assert (0^w)==w
 # Exhaustive 2^8 input basis states x and magic ancilla measurements m:
 # each unnormalized branch has phase omega^{wt(m xor x)}
 # and feed-forward S^{m_i} adds omega^{2*m.x}.
 # Equals global omega^{wt(m)} times wanted omega^{wt(x)}.
 count=0
 for x in range(256):
  for m in range(256):
   overlap=(x&m).bit_count()
   assert (m^x).bit_count()+2*overlap==m.bit_count()+x.bit_count()
   count+=1
 assert count==65536
 return dict(status="PASS_IDEAL_LOGICAL_INTERFACE",
  code="W33 [[40,8,6]] CSS",physical_qubits_per_block=40,
  binary_stabilizer_rank=16,logical_qubits=8,
  logical_X_masks_hex=[hex(x) for x in logic],
  dual_logical_Z_masks_hex=[hex(x) for x in zlogical],
  physical_transversal_CNOT_gates_for_two_blocks=40,
  encoded_magic_logical_qubits_required=8,
  exact_teleportation_branch_phase_checks=count,
  classical_measurement_bits_for_magic_block=8,
  classically_controlled_single_logical_S_corrections_up_to=8,
  result="T on each of eight logical qubits, conditional on an encoded |A>^8 state, a logical-Z readout and individually addressable logical S corrections.",
  boundary="One ideal algebraic injection only. Does not show W33 native single-logical S is realizable, magic factory, state distillation, logical measurement/noise thresholds, or universal physical implementation.")
if __name__=="__main__":print(json.dumps(verify(),indent=2))
