#!/usr/bin/env python3
"""Unit-coefficient vs actively parameterized native q=9 symplectic ticks.

Use F9=F3[z]/(z²+1), elements a+3*b -> a+b*z, z²=-1=2.
All group orders are obtained by exact 2x2 matrix closure; no GAP guess.
"""
from pathlib import Path
import json


def add(x,y):
    return (x%3+y%3)%3 + 3*((x//3+y//3)%3)


def neg(x):
    return (- (x%3))%3 + 3*((-(x//3))%3)


def mul(x,y):
    a,b=x%3,x//3
    c,d=y%3,y//3
    return ((a*c+2*b*d)%3)+3*((a*d+b*c)%3)


def matmul(a,b):
    return (add(mul(a[0],b[0]),mul(a[1],b[2])),
            add(mul(a[0],b[1]),mul(a[1],b[3])),
            add(mul(a[2],b[0]),mul(a[3],b[2])),
            add(mul(a[2],b[1]),mul(a[3],b[3])))


def determinant(m):
    return add(mul(m[0],m[3]),neg(mul(m[1],m[2])))


def generated_group(a):
    U=(1,2,0,1) # T_(1,0)(x,y)=(x-y,y)
    L=(1,0,a,1) # T_(0,lambda)(x,y)=(x,y+lambda²*x)
    generators=(U,L)
    identity=(1,0,0,1)
    group={identity}
    queue=[identity]
    for g in queue:
        for t in generators:
            product=matmul(g,t)
            assert determinant(product)==1
            if product not in group:
                group.add(product);queue.append(product)
    return len(group)


def certify():
    # All four projective scaling classes lambda modulo +/-1 for each
    # pair of native unit-coefficient transvections.
    squares={mul(lam,lam) for lam in range(1,9)}
    assert squares=={1,2,3,6}
    groups={a:generated_group(a) for a in range(1,9)}
    assert groups=={1:24,2:24,3:120,4:720,5:720,6:120,7:720,8:720}
    native=[{"lambda":lam,"lambda_square":mul(lam,lam),
             "order":groups[mul(lam,lam)]} for lam in range(1,9)]
    assert {x["order"] for x in native}=={24,120}
    active=[{"controlled_parameter":a,"order":groups[a]} for a in sorted(set(range(1,9))-squares)]
    assert all(x["order"]==720 for x in active)
    return {
       "schema":"w33.q9.native_vs_controlled_ticks.v1",
       "status":"EXACT_GF9_GROUP_CLOSURE_PHYSICAL_PUMP_UNPROVED",
       "field":"F9=F3[z]/(z^2+1), z^2=2; integer 0..8 encodes a+3b",
       "native_transvections":"T_u(x)=x+omega(x,u)u",
       "native_pair_matrices":"U=[[1,-1],[0,1]], L=[[1,0],[lambda^2,1]]",
       "native_possible_lower_parameters":sorted(squares),
       "native_all_scalings":native,
       "native_possible_generated_orders":[24,120],
       "active_control":"T_(u,c)(x)=x+c*omega(x,u)u, with a controlled non-square c",
       "active_nonsquare_parameters":active,
       "full_SL29_order":720,
       "meaning":"Field extension + native unit ticks insufficient for full SL(2,9) from only two transverse directions; independently controlled nonsquare transvection amplitude does generate full group.",
       "physics_boundary":"No physical evidence for adjustable nonsquare pump amplitude, no quantum Hamiltonian/dispersion/continuum derived.",
       "literature_boundary":"Finite subgroup generation is classical; this is an independently computed W33/Holonet control-design diagnostic, not priority claim."
    }


if __name__=="__main__":
    import sys
    result=json.dumps(certify(),indent=2)+"\n"
    if len(sys.argv)>1:
        Path(sys.argv[1]).write_text(result,encoding="utf-8")
    else:print(result,end="")
