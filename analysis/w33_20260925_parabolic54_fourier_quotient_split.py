#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
OUT=ROOT/"data/w33_20260925_parabolic54_fourier_quotient_split.json"

from analysis.w33_e6_cubic_fourier54_alignment import ordered_records

def mm(A,B,p):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B)))%p
             for j in range(len(B[0]))] for i in range(len(A))]

def mpow(A,e,p):
    R=[[1,0,0],[0,1,0],[0,0,1]]; B=A
    while e:
        if e&1:R=mm(R,B,p)
        B=mm(B,B,p); e//=2
    return R

def rank_columns(columns,p,nrows=81):
    if not columns:return 0
    A=[[columns[j][i]%p for j in range(len(columns))]
       for i in range(nrows)]
    r=0
    for c in range(len(columns)):
        q=next((i for i in range(r,nrows) if A[i][c]),None)
        if q is None:continue
        A[r],A[q]=A[q],A[r]
        z=pow(A[r][c],p-2,p)
        A[r]=[(x*z)%p for x in A[r]]
        for i in range(r+1,nrows):
            z=A[i][c]
            if z:
                A[i]=[(x-z*y)%p for x,y in zip(A[i],A[r])]
        r+=1
        if r==nrows:break
    return r

def build_prime(p,e6_to_h,background):
    roots=[x for x in range(2,p) if (x*x+x+1)%p==0]
    assert len(roots)==2
    w=min(roots)
    X=[[0,0,1],[1,0,0],[0,1,0]]
    Z=[[1,0,0],[0,w,0],[0,0,pow(w,2,p)]]

    def rho(h):
        a,b,c=h
        M=mm(mpow(Z,a,p),mpow(X,b,p),p)
        s=pow(w,c,p)
        return [[s*x%p for x in row] for row in M]

    S1=[]
    for t,r,i in itertools.product(range(3),repeat=3):
        col=[]
        for eid in range(27):
            M=rho(e6_to_h[eid])
            for phase in range(3):
                col.append(M[i][r]*pow(w,(t*phase)%3,p)%p)
        S1.append(col)

    P=[]; Q=[]
    for eid in range(27):
        for phase in (0,1):
            col=[0]*81
            col[3*eid+phase]=1
            P.append(col)
        col=[0]*81
        col[3*eid+2]=1
        Q.append(col)

    D=[[0]*81 for _ in range(81)]
    for u,x,o,c in ordered_records():
        D[o][x]=(D[o][x]+c*background[u])%p
    image=[[D[row][col] for row in range(81)] for col in range(81)]

    rs=rank_columns(S1,p)
    rp=rank_columns(P,p); rq=rank_columns(Q,p)
    rsp=rank_columns(S1+P,p); rsq=rank_columns(S1+Q,p)
    rspq=rank_columns(S1+P+Q,p)
    rsd=rank_columns(S1+image,p)
    rspd=rank_columns(S1+P+image,p)
    rsqd=rank_columns(S1+Q+image,p)
    return {
      "prime":p,"omega":w,
      "rank_S1":rs,"rank_P":rp,"rank_Q":rq,
      "rank_S1_plus_P":rsp,
      "rank_S1_plus_Q":rsq,
      "rank_S1_plus_P_plus_Q":rspq,
      "intersection_S1_P":rs+rp-rsp,
      "intersection_S1_Q":rs+rq-rsq,
      "P_quotient_rank":rsp-rs,
      "Q_quotient_rank":rsq-rs,
      "PQ_quotient_rank":rspq-rs,
      "D_quotient_rank":rsd-rs,
      "rank_S1_P_D":rspd,
      "rank_S1_Q_D":rsqd,
      "extra_beyond_P_from_D":rspd-rsp,
      "extra_beyond_Q_from_D":rsqd-rsq,
    }

def main():
    bridge=json.loads(
      (ROOT/"data/w33_e6id_current_h27_gauge_bridge.json").read_text()
    )
    e6_to_h={int(i):tuple(map(int,h))
              for i,h in bridge["maps"]["e6id_to_current_H27_address"].items()}
    assert len(set(e6_to_h.values()))==27
    coords=[(e6_to_h[eid],phase)
            for eid in range(27) for phase in range(3)]
    lift=lambda x:1+(int(x)%3)
    backgrounds={
      "center":[lift(h[2]) for h,p in coords],
      "external":[lift(p) for h,p in coords],
      "center_plus_external":[lift(h[2]+p) for h,p in coords],
      "center_minus_external":[lift(h[2]-p) for h,p in coords],
    }

    cert={name:[build_prime(p,e6_to_h,v) for p in (103,109)]
          for name,v in backgrounds.items()}

    for rows in cert.values():
        for row in rows:
            assert (row["rank_S1"],row["rank_P"],row["rank_Q"])==(27,54,27)
            assert (row["rank_S1_plus_P"],row["rank_S1_plus_Q"])==(63,45)
            assert row["rank_S1_plus_P_plus_Q"]==81
            assert (row["intersection_S1_P"],row["intersection_S1_Q"])==(18,9)
            assert (row["P_quotient_rank"],row["Q_quotient_rank"],
                    row["PQ_quotient_rank"])==(36,18,54)

    expected={"center":36,"external":36,
              "center_plus_external":54,"center_minus_external":54}
    for name,rows in cert.items():
        assert {row["D_quotient_rank"] for row in rows}=={expected[name]}
    for name in ("center_plus_external","center_minus_external"):
        assert {row["extra_beyond_P_from_D"] for row in cert[name]}=={18}

    par=json.loads(
      (ROOT/"data/w33_20260925_e8_parabolic_cubic_clock_lift.json").read_text()
    )
    assert par["selected_now_decomposition"]["grade_plus1_external_labels"]=={
      "0":27,"1":27
    }
    assert par["selected_now_decomposition"]["grade_plus2_external_label"]=={
      "2":27
    }

    out={
      "schema":"w33.20260925.parabolic54_fourier_quotient_split.v1",
      "status":"PASS_FOURIER_RETYPE_QUOTIENT_IS_36_PLUS18_ACROSS_PARABOLIC_SLICES",
      "coordinate_identification":{
        "P":"positive integer grade +1 slice, external labels 0,1",
        "dim_P":54,
        "Q":"integer grade -2 slice in CE2 g1, external label 2",
        "dim_Q":27,
        "ambient":"CE2 g1 = P direct_sum Q, dimension 81",
      },
      "exact_split_prime_certificate":{
        "primes":[103,109],
        "rank_S1":27,
        "rank_P":54,
        "rank_Q":27,
        "rank_S1_plus_P":63,
        "rank_S1_plus_Q":45,
        "rank_total":81,
        "S1_intersection_P":18,
        "S1_intersection_Q":9,
        "quotient_image_P":36,
        "quotient_image_Q":18,
        "quotient_direct_sum":"54 = 36 + 18",
      },
      "backgrounds":cert,
      "consequence":{
        "naive_54_equals_positive_grade1_coordinate_slice":False,
        "positive_grade1_projection_rank_to_retyped_quotient":36,
        "opposite_second_order_slice_projection_rank":18,
        "together_cover_full_retyped_quotient":True,
        "diagonal_weld_adds_all_18_directions_missing_from_P":True,
      },
      "theorem":(
        "The 54-dimensional Fourier-retyped quotient is not the literal positive "
        "grade-one coordinate slice of the E8 |3|-grading. The operator-compatible "
        "S1 sector meets that 54-space in dimension 18, so only 36 independent "
        "quotient directions survive. The complementary 27-coordinate integer "
        "grade -2 slice meets S1 in dimension 9 and supplies the remaining 18. "
        "Thus the quotient splits relative to the parabolic coordinate decomposition "
        "as 54=36+18. Either diagonal center/external weld contributes all 18 "
        "directions missing from the positive grade-one slice and reaches rank 54."
      ),
      "boundary":(
        "This is an exact characteristic-zero rank certificate lifted from two "
        "split Eisenstein primes. It refutes only the literal coordinate-slice "
        "identification. Abstract 54-dimensional modules may still be related by "
        "a nontrivial change of symmetry or basis, which requires an explicit "
        "intertwiner."
      ),
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
      "status":out["status"],
      "split":out["exact_split_prime_certificate"]["quotient_direct_sum"],
      "diagonal_plus_missing18":
        cert["center_plus_external"][0]["extra_beyond_P_from_D"],
      "diagonal_minus_missing18":
        cert["center_minus_external"][0]["extra_beyond_P_from_D"],
    },indent=2))

if __name__=="__main__":
    main()
