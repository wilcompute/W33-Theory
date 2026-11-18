"""Exact E6 Spin10 16_-3 symmetric gamma-bilinear into 10_-2.

Independently rebuild all native 78 generators, test every one of the
136 unordered two-step adjoint-family action pairs. This goes beyond the
previous decuplet10 x decuplet10 -> five-dimensional rank proof.
"""
import json,itertools,sys
from pathlib import Path
from math import lcm
from collections import defaultdict
import numpy as np
import sympy as S
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261118_wire_Novikov_E6 as N
import w33_pass10950_clock_albert_lorentz_spinor as P
from toe_20261118_Albert_qubit_qutrit_SM_selector import independent

def run():
    J=P.build_clock_albert()
    den=lcm(*[x.denominator for x in J["prod"].flat])
    Prod=np.array([[[int(v*den) for v in row] for row in plane]
                   for plane in J["prod"]],dtype=np.int64)
    L=np.stack([Prod[i].T for i in range(27)])
    c=J["idx"][J["G"][0]]
    ec=S.eye(27)[:,c]
    Psi=6*S.Matrix(L[c])/den-2*S.eye(27)
    old=json.loads((ROOT/"data/toe_20261118_wire_Novikov_E6.json").read_text())
    Chi=S.Matrix(old["native_chi_matrix"])
    d=independent([L[i]@L[j]-L[j]@L[i] for i,j in itertools.combinations(range(27),2)])
    eye=np.eye(27,dtype=np.int64)
    frame=[J["idx"][g] for g in J["G"]]
    tl=[eye[:,i] for i in range(27) if i not in frame]
    tl +=[eye[:,i]-eye[:,frame[-1]] for i in frame[:-1]]
    E6=[S.Matrix(v) for v in d]+[S.Matrix(np.tensordot(v,L,axes=1)) for v in tl]
    assert len(E6)==78
    spinor=N.kernel_combinations(E6,[list(Psi*M-M*Psi+3*M) for M in E6])
    assert len(spinor)==16
    ten=N.kernel_combinations(spinor,[list(Chi*M-M*Chi+M) for M in spinor])
    five=N.kernel_combinations(spinor,[list(Chi*M-M*Chi-3*M) for M in spinor])
    one=N.kernel_combinations(spinor,[list(Chi*M-M*Chi+5*M) for M in spinor])
    assert tuple(map(len,(ten,five,one)))==(10,5,1)
    branches=[("10",ten,-1),("5bar",five,3),("1",one,-5)]
    result={}
    full=[]
    allM=ten+five+one
    for M in allM:
        assert Psi*M-M*Psi==-3*M
    for i in range(16):
        for j in range(i,16):
            assert allM[i]*allM[j]*ec==allM[j]*allM[i]*ec
            full.append(allM[i]*allM[j]*ec)
    fullrank=S.Matrix.hstack(*full).rank()
    assert fullrank==10
    for i,(a,aa,ca) in enumerate(branches):
        for b,bb,cb in branches[i:]:
            products=[X*Y*ec for X in aa for Y in bb]
            rank=S.Matrix.hstack(*products).rank()
            nz=sum(v!=S.zeros(27,1) for v in products)
            expect={( "10","10"):5,("10","5bar"):5,("10","1"):0,
                    ("5bar","5bar"):0,("5bar","1"):5,("1","1"):0}
            assert rank==expect[(a,b)],(a,b,rank)
            for v in products:
                assert Chi*v==(ca+cb)*v
                assert Psi*v==-2*v
            result[a+"x"+b]=dict(total_ordered_products=len(products),
                                 nonzero_in_basis=nz,image_rank=rank,
                                 output_Chi_charge=ca+cb)
    out=dict(status="PASS",spinor_dimension=16,full_symmetric_pairs=136,
             symmetric_square_image_rank=fullrank,
             native_E6_branch_dimensions={"10":10,"5bar":5,"1":1},
             SU5_branch_pair_ranks=result,
             symmetric_Clifford_map="Sym²(16_-3) -> 10_-2 has exact rank10 in native E6 27 module; two SU5 five-dimensional channels are independently generated",
             scope="Exact equivariant representation action only. No wavefunction overlap, 4D physical zero modes, superpotential coefficient, flavor hierarchy, anomaly cancellation or G2 compactification.")
    target=ROOT/"data/toe_20261118_E6_full_spinor_symmetric_gamma10.json"
    target.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print("PASS full native Sym2(16)->10, rank",fullrank,"branches",result)
    return out

if __name__=="__main__":run()
