#!/usr/bin/env python3
from __future__ import annotations

import itertools
import json
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20260924_liouville_swap_cp_outer_bridge.json"
P=3

I2=np.eye(2,dtype=int)
J2=np.array([[0,1],[-1,0]],dtype=int)%P
Z2=np.zeros((2,2),dtype=int)
Jstd=np.block([[Z2,I2],[-I2,Z2]])%P
Jliou=np.block([[J2,Z2],[Z2,(-J2)%P]])%P
Swap=np.block([[Z2,I2],[I2,Z2]])%P
T=np.diag([1,1,2,2])%P

# w=(s,d), s=u+v, d=2 J (u-v)
H=np.block([[I2,I2],[(2*J2)%P,(-2*J2)%P]])%P


def inv_mod(A):
    A=A.copy()%P
    n=A.shape[0]
    aug=np.concatenate([A,np.eye(n,dtype=int)],axis=1)%P
    for c in range(n):
        r=next(i for i in range(c,n) if aug[i,c])
        aug[[c,r]]=aug[[r,c]]
        aug[c]=(aug[c]*pow(int(aug[c,c]),-1,P))%P
        for i in range(n):
            if i!=c and aug[i,c]:
                aug[i]=(aug[i]-aug[i,c]*aug[c])%P
    return aug[:,n:]%P
def canon(v):
    v=tuple(int(x)%P for x in v)
    for x in v:
        if x:
            s=1 if x==1 else 2
            return tuple((s*y)%P for y in v)
    raise ValueError


def projective_line(vectors):
    return sorted({
        canon(v) for v in vectors
        if any(int(x)%P for x in v)
    })


def main():
    Hi=inv_mod(H)
    assert np.array_equal((H.T@Jstd@H)%P,Jliou)
    assert np.array_equal((H@Swap@Hi)%P,T)

    diagonal=[]
    antidiagonal=[]
    for u in itertools.product(range(3),repeat=2):
        if u==(0,0):
            continue
        diagonal.append((np.array(H)@np.array((*u,*u)))%P)
        v=tuple((-x)%P for x in u)
        antidiagonal.append((np.array(H)@np.array((*u,*v)))%P)

    plus=projective_line(diagonal)
    minus=projective_line(antidiagonal)
    assert len(plus)==4 and len(minus)==4
    assert not (set(plus)&set(minus))
    # Every projective fixed point of T lies on one of these two lines.
    allpts=sorted({
        canon(v) for v in itertools.product(range(3),repeat=4) if any(v)
    })
    fixed=[]
    for v in allpts:
        w=tuple(int(x) for x in (T@np.array(v))%P)
        if canon(w)==v:
            fixed.append(v)
    assert len(fixed)==8
    assert set(fixed)==set(plus)|set(minus)

    # The + line is exactly the Liouville diagonal u=v.
    plus_from_inverse=[]
    for w in plus:
        l=(Hi@np.array(w))%P
        plus_from_inverse.append({
            "w33_point":list(w),
            "u":l[:2].astype(int).tolist(),
            "v":l[2:].astype(int).tolist(),
            "u_equals_v":bool(np.array_equal(l[:2],l[2:])),
        })
    assert all(x["u_equals_v"] for x in plus_from_inverse)
    out={
      "schema":"w33.20260924.liouville_swap_cp_outer_bridge.v1",
      "status":"PASS_LIOUVILLE_SWAP_IS_INTRINSIC_W33_TEMPORAL_OUTER",
      "forms":{
        "liouville":"diag(J2,-J2) on (u,v)",
        "w33":"[[0,I],[-I,0]] on (s,d)",
        "H_liouville_to_w33":H.astype(int).tolist(),
        "H_is_symplectic_isometry":True,
      },
      "reversal":{
        "liouville_action":"(u,v)->(v,u)",
        "w33_action":"(s,d)->(s,-d)",
        "w33_matrix":T.astype(int).tolist(),
        "exact_conjugacy":"H Swap H^-1 = diag(I2,-I2)",
        "fixed_projective_points":8,
        "fixed_lines":2,
      },
      "channel_line":{
        "plus_line_points":[list(x) for x in plus],
        "inverse_labels":plus_from_inverse,
        "meaning":"u=v, so Phi_(u,u)(A)=P_u A P_u^dagger is unitary CPTP",
      },
      "mirror_line":{
        "minus_line_points":[list(x) for x in minus],
        "meaning":"u=-v; fixed projectively by reversal but not selected as the CP diagonal",
      },
      "theorem":(
        "The canonical one-qutrit Liouville left/right reversal is symplectically "
        "conjugate to the W33 anti-symplectic outer matrix used by the intrinsic "
        "BT172 construction. Its eight fixed W33 rays split into two Lagrangian "
        "lines; the + line is exactly the unitary-channel diagonal u=v."
      ),
      "boundary":(
        "The minus fixed line is a projective mirror sector; no complete-positivity "
        "or physical reverse-channel interpretation is assigned to it here."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":out["status"],
        "fixed_points":8,
        "fixed_lines":2,
        "plus_is_CP_diagonal":True,
    },indent=2))


if __name__=="__main__":
    main()
