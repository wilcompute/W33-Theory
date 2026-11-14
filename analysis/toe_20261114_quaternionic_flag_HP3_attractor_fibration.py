"""Exact Pauli/USp8 flag-to-projective attractor fibration.
24D full quaternionic flag -> 12D HP3; 12D lost angular directions.
Together with 2 STU radial directions explains the certified 14D
boundary-to-horizon tangent kernel for distinct charges.
"""
from pathlib import Path
import json,sys
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261114_exact_gaussian_us8_pauli_clock as E
OUT=ROOT/"data/toe_20261114_quaternionic_flag_HP3_fibration.json"

def main():
    P,quad,nonquad,_=E.pauli_data()
    triad=(16,32,48)
    assert all(t in quad for t in triad)
    assert all(E.omega(i,j)==0 for i in triad for j in triad)
    def tangent(coeff):
        X=sum((c*P[t] for t,c in zip(triad,coeff)),np.zeros((8,8),complex))
        cols=[]
        for a in nonquad:
            H=1j*(P[a]@X-X@P[a])
            assert np.array_equal(H.conj().T,H)
            values=[]
            for v in quad:
                z=np.trace(P[v]@H)/8
                assert abs(z.imag)<1e-10 and abs(z.real-round(z.real))<1e-10
                values.append(int(round(z.real)))
            assert np.array_equal(H,sum((values[i]*P[v] for i,v in enumerate(quad)),np.zeros((8,8),complex)))
            cols.append(sp.Matrix(values))
        return sp.Matrix.hstack(*cols)
    generic=tangent((1,2,4))
    two_equal=tangent((1,1,4))
    balanced=tangent((1,1,1))
    assert (generic.rank(),two_equal.rank(),balanced.rank())==(24,20,12)
    assert generic.col_join(balanced).rank()==24
    fiber=sp.Matrix.hstack(*(generic*v for v in balanced.nullspace()))
    assert fiber.rank()==12
    assert len(generic.nullspace())==12 and len(balanced.nullspace())==24
    # Sp(4)/Sp(1)^4 -> Sp(4)/(Sp(1)xSp(3)) = HP3;
    # fiber Sp(3)/Sp(1)^3.
    dim=lambda n:n*(2*n+1)
    assert (dim(4),dim(3),dim(1))==(36,21,3)
    assert dim(4)-4*dim(1)==24
    assert dim(4)-dim(1)-dim(3)==12
    assert dim(3)-3*dim(1)==12
    transfer=json.loads((ROOT/"data/toe_20261114_e6_stu_boundary_transfer.json").read_text())
    row=transfer["cases"][0]
    assert row["charges"]==[1,64,4096]
    assert (row["augmented_boundary_rank"],row["horizon_stabilizer_rank"],
            row["kernel_dimension_within_augmented_boundary"])==(42,28,14)
    assert row["boundary_stabilizer_rank"]-row["horizon_stabilizer_rank"]==12
    # Physical small-amplitude generic state and balanced endpoint
    # have the SAME top quaternionic eigenspace.
    Xg=sum((x/10*P[t] for t,x in zip(triad,(1,2,4))),np.zeros((8,8),complex))
    Xb=sum((0.2*P[t] for t in triad),np.zeros((8,8),complex))
    assert min(np.linalg.eigvalsh((np.eye(8)+Xg)/8))>0
    assert min(np.linalg.eigvalsh((np.eye(8)+Xb)/8))>0
    def proj(X):
        _,V=np.linalg.eigh(X)
        return V[:,-2:]@V[:,-2:].conj().T
    assert np.max(abs(proj(Xg)-proj(Xb)))<1e-12
    out=dict(status="PASS_EXACT_QUATERNIONIC_FLAG_TO_HP3_ATTRACTOR_FIBRATION",
        generic_quaternionic_flag_orbit_dimension=24,
        two_equal_eigenvalues_orbit_dimension=20,
        balanced_top_eigenline_orbit_dimension=12,
        exact_tangent_stacked_rank=24,
        exact_fiber_image_rank=12,
        full_flag="Sp(4)/Sp(1)^4",
        horizon_orbit="HP^3=Sp(4)/(Sp(1)xSp(3))",
        forgotten_fiber="Sp(3)/Sp(1)^3",
        boundary_to_horizon_tangent_rank="42->28",
        kernel_decomposition="14 = 12 angular quaternionic flag directions + 2 STU radial directions",
        physical_generic_example="Pauli triad (0.1,0.2,0.4), positive density",
        physical_balanced_example="Pauli triad (0.2,0.2,0.2), positive density",
        same_top_quaternionic_eigenline=True,
        limitations="Compact homogeneous-space fibration and local STU tangent dimension decomposition only, not global uniqueness of physical radial boundary-value solutions.")
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2),flush=True)
    return out
if __name__=="__main__":main()
