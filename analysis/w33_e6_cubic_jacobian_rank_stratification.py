#!/usr/bin/env python3
"""Exact rank stratification of the E6 cubic Jacobian on one E8 matter-81 block.

Use the canonical source-locked bracket
    [e_(i,a),e_(j,b)] = d_ijk epsilon_abc ebar_(k,c),
with 45 signed E6 cubic triads.

For a background v in g1 define
    D_v(x) = [v,x] : g1 -> g2.

After identifying the paired root labels of g2 with those of g1, D_v is an
81x81 integer skew-symmetric matrix. Hence rank(D_v) is even and v itself is
always in the kernel.

This producer computes exact ranks over Q by fraction-free integer Gaussian
elimination for several deterministic backgrounds in the canonical
(e6id, external-phase) ordering:
    root      : v=e_0
    uniform   : v_n=1
    linear    : v_n=n+1
    quadratic : v_n=(n+1)^2

The surprise is that uniform and linear both have rank 54 exactly, while the
quadratic background has rank 78 exactly. Thus a SINGLE cubic background can
supply more than the 54-dimensional rank capacity required by the minimal
symmetry-changing compiler. Alignment with the particular 54 Fourier-retyped
coordinates remains a separate problem.

No generic-rank theorem is asserted here.
"""
from __future__ import annotations
import itertools,json,math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_e6_cubic_jacobian_rank_stratification.json"
ARCH=ROOT/"extracted_v13/W33-Theory-master/artifacts/canonical_su3_gauge_and_cubic.json"

def eps3(a,b,c):
    if len({a,b,c})<3:return 0
    inv=(a>b)+(a>c)+(b>c)
    return -1 if inv%2 else 1

def primitive_row(row,start):
    g=0
    for x in row[start:]:g=math.gcd(g,abs(x))
    if g>1:
        for j in range(start,len(row)):row[j]//=g

def exact_integer_rank(matrix):
    A=[list(map(int,row)) for row in matrix]
    if not A:return 0
    m,n=len(A),len(A[0]);r=0
    for c in range(n):
        p=next((i for i in range(r,m) if A[i][c]),None)
        if p is None:continue
        A[r],A[p]=A[p],A[r]
        primitive_row(A[r],c)
        pivot=A[r][c]
        for i in range(r+1,m):
            q=A[i][c]
            if not q:continue
            for j in range(c,n):
                A[i][j]=pivot*A[i][j]-q*A[r][j]
            primitive_row(A[i],c+1)
        r+=1
        if r==m:break
    return r

def build_records():
    canonical=json.loads(ARCH.read_text())
    d={tuple(sorted(map(int,x["triple"]))):int(x["sign"]) for x in canonical["solution"]["d_triples"]}
    assert len(d)==45
    rec=[]
    idx=lambda i,a:3*i+a
    for tri,sgn in d.items():
        i,j,k=tri
        for u,x,o in ((i,j,k),(i,k,j),(j,i,k),(j,k,i),(k,i,j),(k,j,i)):
            for a,b in itertools.product(range(3),repeat=2):
                c=3-a-b
                if c not in (0,1,2):continue
                e=eps3(a,b,c)
                if e:rec.append((idx(u,a),idx(x,b),idx(o,c),sgn*e))
    assert len(rec)==1620
    return rec

def jacobian(v,records):
    assert len(v)==81
    A=[[0]*81 for _ in range(81)]
    for u,x,o,c in records:A[o][x]+=c*v[u]
    assert all(A[i][j]==-A[j][i] for i in range(81) for j in range(81))
    assert all(sum(A[i][j]*v[j] for j in range(81))==0 for i in range(81))
    return A

def main(write=True):
    records=build_records()
    backgrounds={
      "root0":[1]+[0]*80,
      "uniform":[1]*81,
      "linear":[i+1 for i in range(81)],
      "quadratic":[(i+1)**2 for i in range(81)],
    }
    ranks={}
    for name,v in backgrounds.items():
        A=jacobian(v,records)
        ranks[name]=exact_integer_rank(A)
    assert ranks=={"root0":20,"uniform":54,"linear":54,"quadratic":78}

    minimal=json.loads((ROOT/"data/w33_minimal_symmetry_changing_81_compiler.json").read_text())
    deficit=minimal["compiler"]["symmetry_changing_coordinates"]
    assert deficit==54

    out={
      "schema":"w33.e6_cubic_jacobian_rank_stratification.v1",
      "status":"PASS_ONE_EXPLICIT_CUBIC_BACKGROUND_HAS_EXACT_RANK78_AND_SPECIAL_COHERENT_BACKGROUNDS_HAVE_RANK54",
      "headline":"The actual E6 cubic interaction is strong enough at the single-background level: exact integer elimination gives Jacobian ranks 20 for a root vector, 54 for both the uniform and linear coherent backgrounds, and 78 for the quadratic background v_n=(n+1)^2. Every Jacobian is exactly skew-symmetric and kills its own background vector. Therefore the previous 54-dimensional compiler deficit is not blocked by cubic tangent rank: one explicit background already has rank 78. What remains is to align the cubic image with the specific 54 Fourier-retyped operator coordinates.",
      "coordinate_gauge":{
        "basis":"(e6id, external qutrit phase) with index n=3*e6id+phase",
        "dimension":81,
        "root_tensor":"canonical signed 45-triad E6 cubic times epsilon_abc"
      },
      "exact_rank_strata":{
        "root0":{"formula":"v=(1,0,...,0)","rank":20,"kernel_dimension":61},
        "uniform":{"formula":"v_n=1","rank":54,"kernel_dimension":27},
        "linear":{"formula":"v_n=n+1","rank":54,"kernel_dimension":27},
        "quadratic":{"formula":"v_n=(n+1)^2","rank":78,"kernel_dimension":3}
      },
      "universal_checks":{
        "jacobian_skew_symmetric_on_tested_backgrounds":True,
        "background_vector_in_own_kernel":True,
        "all_tested_ranks_even":True
      },
      "compiler_consequence":{
        "minimal_symmetry_change_dimension":54,
        "explicit_single_background_rank":78,
        "rank_capacity_margin":24,
        "raw_rank_obstruction_to_54_retyping":False,
        "specific_54_coordinate_alignment_proved":False
      },
      "count_collision_firewall":"The uniform/linear Jacobian rank 54 equals the independent representation-theoretic 54-dimensional equivariance deficit. This certificate does not identify their image subspaces; equality of dimensions alone is not an intertwiner.",
      "external_context":"The ambient representation is the classical Vinberg E8 order-three representation SL3 x E6 on 3 tensor 27. This certificate does not import a generic-orbit classification from that theory.",
      "boundary":"This is an exact finite tangent-rank theorem for selected algebraic backgrounds. It does not prove the generic rank is 78, select a physical vacuum, align the rank-78 image with the 54 required Fourier retypings, or determine a coupling strength, mass matrix, or stability potential.",
      "parents":[
        "data/w33_e6_cubic_hybrid81_transport.json",
        "data/w33_minimal_symmetry_changing_81_compiler.json"
      ],
      "checks":{
        "canonical_45_signed_triads":True,
        "ordered_bracket_records_1620":True,
        "root_rank20":True,
        "uniform_rank54":True,
        "linear_rank54":True,
        "quadratic_rank78":True,
        "quadratic_kernel3":True,
        "single_background_exceeds_54_rank_requirement":True,
        "alignment_not_overclaimed":True
      }
    }
    if write:OUT.write_text(json.dumps(out,indent=2)+"\n")
    return out

if __name__=="__main__":print(json.dumps(main(True),indent=2))
