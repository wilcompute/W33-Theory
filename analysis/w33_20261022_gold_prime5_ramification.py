#!/usr/bin/env python3
"""The ramified golden prime 5 produces length-three Jordan chains on W(3,5).

Exact computation over F5. The golden polynomial x²-x-1 becomes (x-3)²,
whereas in char3 it is irreducible. On W(3,5), B=J-I-A has B²=0 and
rank35. The scaled golden companion has nilpotent rank1 and square zero.
Their tensor product has nilpotency index3, with Jordan blocks J3^35,
J2^86,J1^35 in dimension312. The unscaled product has exact order20.
These are characteristic-5 modular facts, NOT real-unitary optics or RH.
"""
from __future__ import annotations
import itertools, json, math
from pathlib import Path
import numpy as np
from analysis.w33_20261022_golden_dualnumber_clock import F,matrix_power_mod
from analysis.w33_20261022_six_algebra_optics_frontiers import rank_modp

def certificate():
    p=5
    n=(p+1)*(p*p+1)
    pts=np.array([(0,)*k+(1,)+tail for k in range(4)
                  for tail in itertools.product(range(p),repeat=3-k)],dtype=np.int64)
    assert len(pts)==n==156
    sym=(pts[:,0,None]*pts[None,:,2]-pts[:,2,None]*pts[None,:,0]+
         pts[:,1,None]*pts[None,:,3]-pts[:,3,None]*pts[None,:,1])%p
    B=(sym!=0).astype(np.int64)
    I=np.eye(n,dtype=np.int64);I2=np.eye(2,dtype=np.int64)
    assert not np.any((B@B)%p)
    rb=rank_modp(B,p)
    assert rb==math.comb(7,3)==35
    assert (3*3-3-1)%p==0
    assert np.array_equal((F-3*I2)@(F-3*I2)%p,np.zeros((2,2),dtype=np.int64))
    # 3^-1 mod5 = 2; N²=0, rank N=1, and F=3(I+N).
    N=(2*F-I2)%p
    assert rank_modp(N,p)==1
    assert not np.any((N@N)%p)
    # R=(I+N) tensor (I+B) = I+M, product of commuting unipotents.
    M=(np.kron((I2+N)%p,(I+B)%p)-np.eye(2*n,dtype=np.int64))%p
    M2=(M@M)%p
    assert np.array_equal(M2,2*np.kron(N,B)%p)
    assert not np.any((M2@M)%p)
    assert np.count_nonzero(M2)>0
    rm=rank_modp(M,p)
    rm2=rank_modp(M2,p)
    assert (rm,rm2)==(156,35)
    blocks3=rm2
    blocks2=rm-2*rm2
    blocks1=2*n-3*blocks3-2*blocks2
    assert (blocks3,blocks2,blocks1)==(35,86,35)
    U=np.kron(F%p,(I+B)%p)%p
    identity=np.eye(2*n,dtype=np.int64)
    for exponent in (4,5,10):assert not np.array_equal(matrix_power_mod(U,exponent,p),identity)
    assert np.array_equal(matrix_power_mod(U,20,p),identity)
    return {"status":"PASS_EXACT_MODULAR","classical_RH_proved":False,
      "characteristic":5,"q":5,"W3q_vertices":156,
      "golden_polynomial_mod5":"x²-x-1=(x-3)²",
      "golden_nilpotent_rank":1,"graph_square_zero_rank":35,
      "tensor_nilpotency_index":3,"rank_M":rm,"rank_M_squared":rm2,
      "Jordan_unipotent_blocks":{"J3":blocks3,"J2":blocks2,"J1":blocks1},
      "dimension":312,"order_unscaled_U_mod5":20,
      "proof":"F=3(I+N), N²=0; B²=0; [(I+N)⊗(I+B)-I]²=2N⊗B and cube=0. Scalar3 order4 and nontrivial unipotent order5.",
      "boundary":"The field at p5 is ramified (dual numbers), not F25 by adjoining golden phi; the integer/complex operator has no order20."}

if __name__=="__main__":
    d=certificate()
    path=Path(__file__).resolve().parents[1]/"data"/"w33_20261022_gold_prime5_ramification.json"
    path.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
    print({k:v for k,v in d.items() if k in ("status","Jordan_unipotent_blocks","order_unscaled_U_mod5")})
