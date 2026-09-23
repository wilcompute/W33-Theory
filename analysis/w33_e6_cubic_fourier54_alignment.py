#!/usr/bin/env python3
"""Prove that one explicit E6-cubic background covers the full 54D Fourier-retyped quotient.

The source address module decomposes under the CURRENT physical-Clifford K=H27 x C3_external gauge as
    Reg(K) = S1(27) + S2(27) + L(27),
where S1 is the unique 27-dimensional operator-compatible isotypic sector.
The minimal symmetry-changing compiler must retype the complementary
54-dimensional Fourier quotient.

For a matter background v define the canonical cubic Jacobian
    D_v(x)=[v,x]: g1 -> g2.
Transport g2 back to the paired (e6id,phase) labels.  The question is not just
rank(D_v)>=54; the relevant condition is
    rank(S1 + Im D_v) = 81.
Equivalently, the quotient projection Im(D_v) -> Reg(K)/S1 has rank 54.

This producer first loads the explicit canonical-e6id -> current-H27 gauge bridge,
then constructs the 27 S1 matrix coefficients directly from the frozen H27 Schrodinger representation and checks the combined rank modulo
two split primes p=103,109 of Z[omega].  At each prime omega is sent to a root
of x^2+x+1.

Because all matrix entries lie in Z[omega], rank 81 after reduction modulo a
prime ideal implies that an 81x81 minor is nonzero already over Q(omega).
Thus the modular full-rank witness is an exact characteristic-zero certificate.

Results:
  root0:     rank D=20, quotient rank 20
  uniform:   rank D=54, quotient rank 36
  linear:    rank D=54, quotient rank 45
  quadratic: rank D=78, quotient rank 54, combined rank 81

Hence the explicit quadratic background v_n=(n+1)^2 is sufficient, at the
finite tangent level, to access every one of the 54 representation-retyped
Fourier directions.  This is a surjectivity statement onto the quotient, not
an equality Im(D_v)=S2+L.
"""
from __future__ import annotations

import importlib.util
import itertools
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_e6_cubic_fourier54_alignment.json"

def load(path,name):
    s=importlib.util.spec_from_file_location(name,path); assert s and s.loader
    m=importlib.util.module_from_spec(s); sys.modules[name]=m; s.loader.exec_module(m); return m

def eps3(a,b,c):
    if len({a,b,c})<3:return 0
    inv=(a>b)+(a>c)+(b>c)
    return -1 if inv%2 else 1

def ordered_records():
    canonical=json.loads((ROOT/"extracted_v13/W33-Theory-master/artifacts/canonical_su3_gauge_and_cubic.json").read_text())
    d={tuple(sorted(map(int,x["triple"]))):int(x["sign"]) for x in canonical["solution"]["d_triples"]}
    idx=lambda i,a:3*i+a
    rec=[]
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

def prime_rank_certificate(p,v,e6_to_h,records):
    def mod(x):return int(x)%p
    def power(a,e):
        r=1;a%=p
        while e:
            if e&1:r=(r*a)%p
            a=(a*a)%p;e//=2
        return r
    roots=[x for x in range(2,p) if (x*x+x+1)%p==0]
    assert len(roots)==2
    omega=min(roots)
    def inv(x):return power(x,p-2)

    def mm(A,B):
        R=[[0]*len(B[0]) for _ in range(len(A))]
        for i in range(len(A)):
            for k in range(len(B)):
                if not A[i][k]:continue
                for j in range(len(B[0])):
                    if B[k][j]:
                        R[i][j]=(R[i][j]+A[i][k]*B[k][j])%p
        return R
    def mpow(A,e):
        R=[[1,0,0],[0,1,0],[0,0,1]];B=A
        while e:
            if e&1:R=mm(R,B)
            B=mm(B,B);e//=2
        return R

    X=[[0,0,1],[1,0,0],[0,1,0]]
    Z=[[1,0,0],[0,omega,0],[0,0,pow(omega,2,p)]]
    def rho1(h):
        a,b,c=h
        R=mm(mpow(Z,a),mpow(X,b))
        scalar=power(omega,c)
        return [[scalar*x%p for x in row] for row in R]
    def wpow(e):return power(omega,e%3)

    # 27 canonical S1 matrix coefficients: three copies of V_omega for each
    # external character t.  Column labels are (t, regular-multiplicity r,
    # representation component i).
    S1=[]
    for t,r,i in itertools.product(range(3),repeat=3):
        col=[]
        for eid in range(27):
            R=rho1(e6_to_h[eid])
            for phase in range(3):
                col.append(R[i][r]*wpow(t*phase)%p)
        S1.append(col)

    D=[[0]*81 for _ in range(81)]
    for u,x,o,c in records:
        D[o][x]=(D[o][x]+c*v[u])%p
    image=[[D[row][col] for row in range(81)] for col in range(81)]

    def rank_columns(columns):
        A=[[columns[j][i]%p for j in range(len(columns))] for i in range(81)]
        r=0
        for c in range(len(columns)):
            pivot=next((i for i in range(r,81) if A[i][c]),None)
            if pivot is None:continue
            A[r],A[pivot]=A[pivot],A[r]
            q=inv(A[r][c])
            A[r]=[(x*q)%p for x in A[r]]
            for i in range(r+1,81):
                q=A[i][c]
                if q:
                    A[i]=[(x-q*y)%p for x,y in zip(A[i],A[r])]
            r+=1
            if r==81:break
        return r

    s1=rank_columns(S1)
    rd=rank_columns(image)
    combined=rank_columns(S1+image)
    assert s1==27
    return {
      "prime":p,
      "omega_mod_p":omega,
      "S1_rank":s1,
      "jacobian_rank":rd,
      "combined_rank":combined,
      "quotient_projection_rank":combined-s1,
      "S1_image_intersection_dimension":s1+rd-combined,
    }

def main(write=True):
    bridge=json.loads((ROOT/"data/w33_e6id_current_h27_gauge_bridge.json").read_text())
    e6_to_h={int(i):tuple(map(int,h)) for i,h in bridge["maps"]["e6id_to_current_H27_address"].items()}
    assert bridge["incidence"]["mapped_full45_equal"] is True
    assert bridge["incidence"]["mapped_bad9_equal"] is True
    assert len(set(e6_to_h.values()))==27
    records=ordered_records()

    backgrounds={
      "root0":[1]+[0]*80,
      "uniform":[1]*81,
      "linear":[i+1 for i in range(81)],
      "quadratic":[(i+1)**2 for i in range(81)],
    }
    cert={}
    for name,v in backgrounds.items():
        cert[name]=[prime_rank_certificate(p,v,e6_to_h,records) for p in (103,109)]

    expected={
      "root0":(20,47,20,0),
      "uniform":(54,63,36,18),
      "linear":(54,72,45,9),
      "quadratic":(78,81,54,24),
    }
    for name,(rd,combined,quot,inter) in expected.items():
        for row in cert[name]:
            assert (
              row["jacobian_rank"],row["combined_rank"],
              row["quotient_projection_rank"],row["S1_image_intersection_dimension"]
            )==(rd,combined,quot,inter)

    prior=json.loads((ROOT/"data/w33_e6_cubic_jacobian_rank_stratification.json").read_text())
    minimal=json.loads((ROOT/"data/w33_minimal_symmetry_changing_81_compiler.json").read_text())
    assert prior["exact_rank_strata"]["quadratic"]["rank"]==78
    assert minimal["compiler"]["symmetry_changing_coordinates"]==54

    out={
      "schema":"w33.e6_cubic_fourier54_alignment.v1",
      "status":"PASS_QUADRATIC_CUBIC_BACKGROUND_SURJECTS_ONTO_THE_FULL_54D_RETYPE_FOURIER_QUOTIENT",
      "headline":"The remaining alignment gap is closed at the finite tangent level. The 27-dimensional S1 Fourier sector is the operator-compatible part of Reg(H27 x C3). For the explicit quadratic background v_n=(n+1)^2, the cubic Jacobian has exact rank 78 and rank(S1+Im D_v)=81 after reduction at both split Eisenstein primes 103 and 109. Because the entries lie in Z[omega], this proves characteristic-zero combined rank 81. Therefore Im(D_v) projects with rank 54 onto Reg(K)/S1, exactly the full symmetry-retyped quotient required by the minimal compiler.",
      "Fourier_decomposition":{
        "source":"Reg(K)=S1(27)+S2(27)+L(27)",
        "operator_compatible_sector":"S1",
        "operator_compatible_dimension":27,
        "retyped_quotient":"Reg(K)/S1 ~= S2 + L after choosing the canonical Fourier splitting",
        "retyped_dimension":54
      },
      "background_results":{
        name:{
          "formula":{
            "root0":"v=(1,0,...,0)",
            "uniform":"v_n=1",
            "linear":"v_n=n+1",
            "quadratic":"v_n=(n+1)^2"
          }[name],
          "split_prime_certificates":rows,
          "characteristic_zero_jacobian_rank":prior["exact_rank_strata"][name]["rank"],
          "quotient_projection_rank":rows[0]["quotient_projection_rank"],
          "S1_image_intersection_dimension":rows[0]["S1_image_intersection_dimension"]
        } for name,rows in cert.items()
      },
      "exactness_argument":{
        "coefficient_ring":"Z[omega]",
        "split_primes":[103,109],
        "prime_condition":"p=1 mod 3, so x^2+x+1 splits and omega has an F_p image",
        "logic":"an 81x81 minor nonzero after reduction modulo either prime ideal was already nonzero in Z[omega], so combined rank 81 holds over Q(omega)",
        "quadratic_combined_rank_over_Qomega":81,
        "quadratic_quotient_projection_rank_over_Qomega":54
      },
      "compiler_consequence":{
        "required_retyped_dimension":54,
        "quadratic_background_covers_all_retyped_quotient_directions":True,
        "raw_rank_margin":24,
        "remaining_finite_linear_alignment_obstruction":False,
        "image_equals_canonical_S2_plus_L_subspace":False,
        "projection_to_that_complement_is_surjective":True
      },
      "singular_strata":{
        "uniform_rank54_but_quotient_rank36":True,
        "linear_rank54_but_quotient_rank45":True,
        "lesson":"Jacobian rank alone does not measure useful symmetry-changing capacity; orientation relative to S1 matters."
      },
      "boundary":"This establishes an exact finite quotient-surjectivity mechanism for one algebraic matter background. It does not select that background dynamically, prove it is a stable or D/F-flat vacuum, determine a coupling coefficient, exponentiate the tangent map into a unitary gate, or certify hardware.",
      "parents":[
        "data/w33_e6_cubic_jacobian_rank_stratification.json",
        "data/w33_minimal_symmetry_changing_81_compiler.json",
        "analysis/w33_e8_matter81_hybrid_cubic_dark_basis.py",
        "data/w33_e6id_current_h27_gauge_bridge.json"
      ],
      "checks":{
        "S1_rank27_at_both_split_primes":True,
        "root_projection20":True,
        "uniform_projection36":True,
        "linear_projection45":True,
        "quadratic_projection54":True,
        "quadratic_combined_rank81_at_both_split_primes":True,
        "split_prime_witness_lifts_to_Qomega":True,
        "all_54_retyped_quotient_directions_covered":True,
        "subspace_equality_not_overclaimed":True
      }
    }
    if write:OUT.write_text(json.dumps(out,indent=2)+"\n")
    return out

if __name__=="__main__":print(json.dumps(main(True),indent=2))
