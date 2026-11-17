"""EXACT full E6 -> SU5 -> SM stabilizer by cubic-invariant derivations.

For the 27 in trinification sectors A(3,bar3,1),
B(1,3,bar3), C(bar3,1,3), cubic I3=det A+det B+det C-Tr(ABC).
Let two Higgs VEVs be A_32 and A_33, plus aligned dual 27bar VEVs.
Linear infinitesimal cubic stabilizer is e6(C), dim78.
Imposing two vector and dual VEVs leaves A4=sl5, dim24.
An adjoint Higgs along the explicit Y below leaves
sl3_C + sl2_L + u1, dim12, with correct 27 hypercharges.
These are LIE ALGEBRAS, not a fully stabilized chiral SUSY model.
"""
import collections,itertools,json,math
from fractions import Fraction as F
from pathlib import Path
import sympy as S
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_E6_full_cubic_SM_roadblock.json"
N=27

def cubic_monomials():
    p=collections.defaultdict(int)
    for base in (0,9,18):
        for q in itertools.permutations(range(3)):
            inversions=sum(q[i]>q[j] for i in range(3) for j in range(i+1,3))
            p[tuple(sorted(base+3*i+q[i] for i in range(3)))]+=(-1)**inversions
    for i,j,k in itertools.product(range(3),repeat=3):
        p[tuple(sorted((3*i+j,9+3*j+k,18+3*k+i))) ]-=1
    assert len(p)==45 and all(v for v in p.values())
    return dict(p)

def cubic_derivation_rows(monomials):
    rows=collections.defaultdict(lambda:collections.defaultdict(int))
    for m,coefficient in monomials.items():
        for k in range(3):
            for target in range(N):
                changed=list(m);source=changed[k];changed[k]=target
                rows[tuple(sorted(changed))][N*source+target]+=coefficient
    return [{j:v for j,v in row.items() if v} for row in rows.values()]

def exact_sparse_rank(rows):
    """Exact rational row echelon elimination, no floating tolerance."""
    piv={}
    for raw in rows:
        row={k:F(v) for k,v in raw.items() if v}
        while row:
            k=min(row)
            if k not in piv:
                z=row[k];piv[k]={j:v/z for j,v in row.items() if v};break
            factor=row[k]
            for j,v in piv[k].items():
                rem=row.get(j,0)-factor*v
                if rem:row[j]=rem
                elif j in row:del row[j]
    return len(piv)

def modular_sparse_rank(rows,prime):
    """Independent finite-field rank check, primes not dividing any input coefficients."""
    piv={}
    for raw in rows:
        row={k:int(v)%prime for k,v in raw.items() if int(v)%prime}
        while row:
            k=min(row)
            if k not in piv:
                scale=pow(row[k],-1,prime)
                piv[k]={j:(v*scale)%prime for j,v in row.items() if v%prime}
                break
            factor=row[k]
            for j,v in piv[k].items():
                t=(row.get(j,0)-factor*v)%prime
                if t:row[j]=t
                elif j in row:del row[j]
    return len(piv)

def vev_constraints():
    # Higgs in (L row3,R col2) and (row3,col3);
    # dual bar27 partners require the corresponding ROWS to vanish.
    return [{i*N+c:1} for c in (7,8) for i in range(N)]+[
        {r*N+i:1} for r in (7,8) for i in range(N)]

def hypercharge_integer_weights():
    l=(1,1,-2);r=(4,-2,-2)
    weights=[l[i]-r[j] for i in range(3) for j in range(3)]
    weights.extend(r[j] for j in range(3) for _ in range(3))
    weights.extend(-l[i] for _ in range(3) for i in range(3))
    assert len(weights)==27 and weights[7]==weights[8]==0
    return weights

def root_counts(monomials,der_rows,vev_rows,weights):
    inc=S.zeros(len(monomials),N)
    for idx,(triplet,sign) in enumerate(monomials.items()):
        for i in triplet:inc[idx,i]+=sign
    H=inc.nullspace()
    assert len(H)==6
    restriction=S.Matrix([[v[i] for v in H] for i in (7,8)])
    Hlocal=[S.Matrix.hstack(*H)*w for w in restriction.nullspace()]
    assert len(Hlocal)==4
    groups=collections.defaultdict(list)
    for i in range(N):
        for j in range(N):
            if i!=j:
                wt=tuple(v[i]-v[j] for v in H)
                assert any(wt)
                groups[wt].append(i*N+j)
    ordinary=survivors=neutral=0
    for wt, cols in groups.items():
        convert={c:k for k,c in enumerate(cols)}
        def restricted_rank(extra=()):
            subset=[]
            for row in itertools.chain(der_rows,extra):
                z={convert[j]:v for j,v in row.items() if j in convert}
                if z:subset.append(z)
            return exact_sparse_rank(subset)
        dim=len(cols)-restricted_rank()
        assert dim in (0,1)
        ordinary+=dim
        if dim:
            survivor=len(cols)-restricted_rank(vev_rows)
            assert survivor in (0,1)
            survivors+=survivor
            if survivor:
                i,j=divmod(cols[0],N)
                proj=tuple(v[i]-v[j] for v in Hlocal)
                assert any(proj), "Unbroken off-diagonal zero-weight root invalidates A4 inference"
                neutral+=int(weights[i]==weights[j])
    assert ordinary==72 and survivors==20 and neutral==8
    return {"original_Cartan_rank":6,
            "original_nonzero_roots":ordinary,
            "Higgs_surviving_Cartan_rank":4,
            "Higgs_surviving_nonzero_roots":survivors,
            "adjoint_Y_neutral_nonzero_roots":neutral,
            "Higgs_root_type":"A4 (the simply-laced rank-4 root system with 20 roots)",
            "after_adjoint_root_type":"A2 + A1 and one U1 Cartan"}

def anomaly_table():
    # label, dimension per multiplet, multiplicity, SU3 representation,
    # SU2 representation, hypercharge Y=-integer_weight/6.
    rows=[("Q",6,1,"3","2",F(1,6)),
          ("u_c",3,1,"bar3","1",F(-2,3)),
          ("e_c",1,1,"1","1",F(1)),
          ("d_c",3,2,"bar3","1",F(1,3)),
          ("L",2,2,"1","2",F(-1,2)),
          ("H_u_or_exotic",2,1,"1","2",F(1,2)),
          ("D_exotic",3,1,"3","1",F(-1,3)),
          ("neutral_singlet",1,2,"1","1",F(0))]
    assert sum(dim*mult for _,dim,mult,_,_,_ in rows)==27
    grav=sum(dim*mult*y for _,dim,mult,_,_,y in rows)
    y3=sum(dim*mult*y**3 for _,dim,mult,_,_,y in rows)
    su3=sum(mult*F(dim,3)*F(1,2)*y for _,dim,mult,c,_,y in rows if c in ("3","bar3"))
    su2=sum(mult*F(dim,2)*F(1,2)*y for _,dim,mult,_,w,y in rows if w=="2")
    color=sum(mult*dim//3*(1 if c=="3" else -1) for _,dim,mult,c,_,y in rows if c in ("3","bar3"))
    doublets=sum(mult*dim//2 for _,dim,mult,_,w,y in rows if w=="2")
    assert (grav,y3,su3,su2,color)==(0,0,0,0,0) and doublets%2==0
    return {"multiplets":[{"name":name,"dimension":dim,"copies":mult,"SU3":c,
            "SU2":w,"hypercharge":str(y)}
             for name,dim,mult,c,w,y in rows],
            "anomaly_checks_exact":{"grav_U1":str(grav),"U1_cubed":str(y3),
              "SU3_squared_U1":str(su3),"SU2_squared_U1":str(su2),
              "SU3_cubed":color,"Witten_SU2_doublets":doublets}}

def verify():
    p=cubic_monomials();rows=cubic_derivation_rows(p)
    vev=vev_constraints(); Y=hypercharge_integer_weights()
    adj=[{i*N+j:1} for i in range(N) for j in range(N) if Y[i]!=Y[j]]
    r0=exact_sparse_rank(rows)
    r1=exact_sparse_rank(rows+vev)
    r2=exact_sparse_rank(rows+vev+adj)
    assert (r0,r1,r2)==(651,705,717)
    prime_checks={str(pr):[modular_sparse_rank(group,pr) for group in (rows,rows+vev,rows+vev+adj)] for pr in (101,103)}
    assert all(values==[651,705,717] for values in prime_checks.values())
    roots=root_counts(p,rows,vev,Y)
    anomaly=anomaly_table()
    return {"status":"PASS_FULL_E6_CUBIC_STABILIZER_SU5_TO_SM_ADJOINT",
      "method":"Exact rational rank of cubic derivation linear constraints; 45 cubic monomials, 27x27=729 unknown entries, 2475 independent row labels",
      "cubic_derivation_rank":r0,"E6_Lie_dim":729-r0,
      "two_Higgs_dual_vev_rank":r1,"surviving_SU5_Lie_dim":729-r1,
      "after_adjoint_rank":r2,"SM_Lie_dim":729-r2,
      "independent_prime_field_rank_crosschecks":prime_checks,
      "root_data":roots,
      "hypercharge_integer_operator":{"L_diag":[1,1,-2],"R_diag":[4,-2,-2],"C_diag":[0,0,0]},
      "SM_hypercharge_normalization":"Y_SM = -Y_integer/6",
      "anomaly_free_27_branching":anomaly,
      "scope":"Exact complex E6 and compact-real Lie algebra stabilizer for vectorlike aligned Higgs/dual VEVs plus a diagonal adjoint VEV; global gauge quotients, full F/D potential with adjoint, exotics masses, anomaly of all added families, and physical scales not determined.",
      "critical_negative_result":"Two rank-one vectorlike 27-Higgs pairs alone leave SU5, NOT the SM; the additional adjoint SU5 hypercharge-direction VEV is necessary within this minimal ansatz."}

if __name__=="__main__":
    cert=verify();OUT.parent.mkdir(exist_ok=True,parents=True)
    OUT.write_text(json.dumps(cert,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(cert["status"],cert["E6_Lie_dim"],cert["surviving_SU5_Lie_dim"],cert["SM_Lie_dim"])
