#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, math
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20260924_positive_null_counter_cover.json"

D=[
    np.array([[1,0],[0,0]],dtype=int),
    np.array([[0,0],[0,1]],dtype=int),
    np.array([[1,1],[1,1]],dtype=int),
    np.array([[1,-1],[-1,1]],dtype=int),
]
NAMES=["0","infinity","plus","minus"]

def coords(S):
    return (int(S[0,0])%3,int(S[0,1])%3,int(S[1,1])%3)

def lift(n):
    S=np.zeros((2,2),dtype=int)
    for a,M in zip(n,D):
        S+=int(a)*M
    return S

def rank_mod3(A):
    A=np.array(A,dtype=int)%3
    r=0
    m,n=A.shape
    for c in range(n):
        piv=next((i for i in range(r,m) if A[i,c]),None)
        if piv is None:
            continue
        A[[r,piv]]=A[[piv,r]]
        A[r]=(A[r]*pow(int(A[r,c]),-1,3))%3
        for i in range(m):
            if i!=r and A[i,c]:
                A[i]=(A[i]-A[i,c]*A[r])%3
        r+=1
    return r
def main():
    # Real future cone: each generator is nonzero PSD rank one.
    gen=[]
    for name,M in zip(NAMES,D):
        eig=np.linalg.eigvalsh(M.astype(float))
        assert eig.min()>-1e-10
        assert np.linalg.matrix_rank(M)==1
        assert round(np.linalg.det(M))==0
        gen.append({
          "name":name,
          "matrix":M.tolist(),
          "trace":int(np.trace(M)),
          "eigenvalues":[float(x) for x in eig],
        })

    A=np.array([
        [coords(M)[j] for i,M in enumerate(D)]
        for j in range(3)
    ],dtype=int)
    assert A.shape==(3,4)
    assert rank_mod3(A)==3

    kernel=[]
    image={}
    for n in itertools.product(range(3),repeat=4):
        y=tuple(int(x) for x in (A@np.array(n,dtype=int))%3)
        image.setdefault(y,[]).append(n)
        if y==(0,0,0):
            kernel.append(n)
    assert len(image)==27
    assert len(kernel)==3
    assert set(kernel)=={(0,0,0,0),(1,1,1,1),(2,2,2,2)}
    assert set(len(v) for v in image.values())=={3}
    cycle=np.ones(4,dtype=int)
    C=lift(cycle)
    assert np.array_equal(C,3*np.eye(2,dtype=int))
    assert coords(C)==(0,0,0)

    # Adding the common pulse returns to the same finite history and advances
    # monotonically in the integer PSD cone.
    examples=[]
    seed=np.array([2,0,1,4],dtype=int)
    base=coords(lift(seed))
    prev=None
    for m in range(8):
        n=seed+m*cycle
        S=lift(n)
        assert coords(S)==base
        if prev is not None:
            diff=S-prev
            assert np.array_equal(diff,3*np.eye(2,dtype=int))
        prev=S
        examples.append({
          "winding":m,
          "counters":list(map(int,n)),
          "lift":S.tolist(),
          "finite_history":list(base),
          "trace":int(np.trace(S)),
          "determinant":int(round(np.linalg.det(S))),
        })
    assert [r["trace"] for r in examples]==[
        examples[0]["trace"]+6*m for m in range(8)
    ]

    # Any positive update strictly raises trace, hence no positive loop exists
    # in the integer cover although loops exist after mod-three projection.
    assert all(np.trace(M)>0 for M in D)
    # Common S4 permutation symmetry of the four null counters preserves winding.
    perms=list(itertools.permutations(range(4)))
    assert len(perms)==24
    assert all(tuple(cycle[list(p)])==(1,1,1,1) for p in perms)

    out={
      "schema":"w33.20260924.positive_null_counter_cover.v1",
      "status":"PASS_27_HISTORIES_ARE_FOUR_NULL_COUNTERS_MOD_COMMON_WINDING",
      "null_generators":gen,
      "finite_quotient":{
        "linear_map_matrix_F3":A.tolist(),
        "rank":3,
        "domain":"F3^4 null-direction counters",
        "kernel":[list(x) for x in kernel],
        "kernel_description":"span_F3{(1,1,1,1)}",
        "quotient":"F3^4/<1111> ~= Sym2(F3)",
        "image_size":len(image),
        "fibres":3,
      },
      "integer_cover":{
        "positive_monoid":"N^4 -> Sym2(Z), n |-> sum_i n_i D_i",
        "fundamental_winding_counts":[1,1,1,1],
        "fundamental_winding_matrix":C.tolist(),
        "identity":"D0+Dinf+Dplus+Dminus=3*I2",
        "projection_mod3":"fundamental winding projects to zero",
        "trace_increment_per_winding":6,
        "positive_loop_upstairs":False,
        "same_finite_history_examples":examples,
      },
      "symmetry":{
        "null_direction_permutation_group":"S4",
        "order":24,
        "common_winding_1111_fixed":True,
      },
      "theorem":(
        "The four projective null directions give four integral positive-"
        "semidefinite rank-one update matrices. Modulo three their counter map "
        "F3^4 -> Sym2(F3) has rank three and exact kernel <1111>, hence the 27 "
        "finite histories are F3^4/<1111>. Over the integer positive cover the "
        "kernel generator does not vanish: one pulse in every null direction "
        "adds 3I2. Repeating it returns to the same finite history while trace "
        "increases by six each winding. Thus recurrence of the finite state and "
        "monotone lifted history are simultaneously exact."
      ),
      "boundary":(
        "Trace is an operational monotone on this chosen positive integer cover, "
        "not a derivation of relativistic proper time or thermodynamic entropy. "
        "The S4-fixed winding here is not identified with the separate invariant "
        "cycle in the 108-edge null-history graph without an explicit chain map."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "rank":out["finite_quotient"]["rank"],
      "kernel":out["finite_quotient"]["kernel"],
      "winding":out["integer_cover"]["identity"],
      "trace_sequence":[x["trace"] for x in examples],
    },indent=2,sort_keys=True))

if __name__=="__main__":
    main()
