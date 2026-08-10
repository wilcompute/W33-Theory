#!/usr/bin/env python3
"""Pass 4653 — characteristic-three obstruction to the sheet Fourier split.

For the three canonically aligned degree-36 spread sheets, the sheet factor is
the natural permutation module V=k^3 for S3.  Away from characteristic three,
V splits canonically as bright trivial line <(1,1,1)> plus the sum-zero dark
plane.  The projectors are J/3 and I-J/3.

At characteristic three, 1+1+1=0: the bright diagonal vector itself lies in the
dark sum-zero plane.  J^2=0, im J=<111> is contained in ker J, and V has the
nonsplit S3 filtration trivial | sign | trivial.  Consequently the coupling
[R R R] still factors through the sum quotient V/W, but there is no S3-
equivariant bright complement/section.  This is an exact modular obstruction,
not a physical phase statement.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS4653_CHARACTERISTIC3_SHEET_FOURIER_OBSTRUCTION.json"


def rank_mod_p(M,p):
    A=np.asarray(M,dtype=np.int64).copy()%p; r=0
    for c in range(A.shape[1]):
        rows=np.flatnonzero(A[r:,c])
        if not len(rows): continue
        rr=r+int(rows[0])
        if rr!=r: A[[r,rr]]=A[[rr,r]]
        inv=pow(int(A[r,c]),-1,p); A[r]=(A[r]*inv)%p
        for i in range(A.shape[0]):
            if i!=r and A[i,c]: A[i]=(A[i]-int(A[i,c])*A[r])%p
        r+=1
    return r


def main():
    I=np.eye(3,dtype=np.int64); J=np.ones((3,3),dtype=np.int64)
    c=np.array([[0,1,0],[0,0,1],[1,0,0]],dtype=np.int64)
    s=np.array([[0,1,0],[1,0,0],[0,0,1]],dtype=np.int64)
    t=np.ones((3,1),dtype=np.int64)
    sumrow=np.ones((1,3),dtype=np.int64)
    assert np.array_equal(c@c@c,I) and np.array_equal(s@s,I) and np.array_equal(s@c@s,c@c)

    # Characteristic not 3: exact central idempotents.
    # 3*Pbright=J and 3*Pdark=3I-J; algebraically J^2=3J.
    assert np.array_equal(J@J,3*J)
    D=3*I-J
    assert np.array_equal(D@D,3*D) and not (D@J).any()

    # Characteristic 3 degeneration.
    J3=J%3
    assert not ((J3@J3)%3).any()
    assert rank_mod_p(J3,3)==1
    assert not (sumrow@t%3).any()  # diagonal vector lies in sum-zero plane

    # W=ker(sum) basis; T=<111> lies inside W.
    w1=np.array([1,-1,0],dtype=np.int64)%3
    w2=np.array([0,1,-1],dtype=np.int64)%3
    W=np.column_stack([w1,w2])
    assert rank_mod_p(W,3)==2 and not ((sumrow@W)%3).any()
    assert rank_mod_p(np.column_stack([W,t%3]),3)==2

    # Fixed space of full S3 in V is exactly T.  Since sum(T)=0, no invariant
    # line can map isomorphically to V/W; hence 0->W->V->triv->0 is nonsplit.
    fixed=np.vstack([(c-I)%3,(s-I)%3])
    assert 3-rank_mod_p(fixed,3)==1

    # Inside W, T is the only fixed line.  W/T is sign: a transposition sends
    # w1 to -w1 modulo T, while a 3-cycle is identity modulo T.
    def in_T(v):
        return rank_mod_p(np.column_stack([t%3,v.reshape(3,1)%3]),3)==1
    assert in_T((s@w1 + w1)%3)
    assert in_T((c@w1 - w1)%3)
    # No sign eigenline complement exists: A3 fixed space is only T.
    assert 3-rank_mod_p((c-I)%3,3)==1

    # In characteristic 2 the diagonal line is NOT in W and the split survives;
    # the 2D dark plane is the irreducible C3 module (x^2+x+1).
    assert int((sumrow@t)[0,0]%2)==1
    assert rank_mod_p(W,2)==2
    Cstd=np.array([[0,1],[-1,-1]],dtype=np.int64)
    assert rank_mod_p(Cstd-np.eye(2,dtype=np.int64),2)==2

    out={
      "pass":4653,
      "generic_characteristic_not_3":{
        "sheet_module":"trivial_1 + Std_2",
        "bright_projector":"J/3",
        "dark_projector":"I-J/3",
        "identity":"J^2=3J"
      },
      "characteristic_3":{
        "J_rank":1,
        "J_square":"0",
        "image_J":"T=<111>",
        "kernel_J":"W={x1+x2+x3=0}, dimension 2",
        "containment":"T subset W",
        "filtration":"0 < T(trivial) < W < V, with factors trivial | sign | trivial",
        "top_extension_split":false,
        "lower_extension_split":false,
        "diagonal_bright_vector_is_dark":true,
        "coupling_statement":"[R R R] factors through the trivial quotient V/W, but there is no S3-equivariant bright section"
      },
      "characteristic_2":{
        "bright_dark_split_survives":true,
        "dark_C3_module":"irreducible 2D, minimal polynomial x^2+x+1"
      },
      "theorem":"Characteristic three destroys the semisimple bright/dark sheet Fourier decomposition: the diagonal sheet vector lies inside the dark plane and the S3 permutation module becomes the nonsplit filtration trivial|sign|trivial.",
      "boundary":"Modular representation theorem only; it is not a physical three-generation or phase-decoherence claim."
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,indent=2,sort_keys=True)); return 0

if __name__=="__main__": raise SystemExit(main())
