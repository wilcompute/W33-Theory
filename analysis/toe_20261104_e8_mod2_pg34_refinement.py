#!/usr/bin/env python3
"""E8/2E8 exact quadratic isometry to GF(4)^4 and incompatible 25/60 vs 45/40 strata.

E8 mod2 orthogonal Q+(7,2), 135/120, F4 Hermitian H(3,4) 45/40
are PRIOR ART in repository Pass 8925-8940, Pass 9961-9984,
and incidence E8 shadow Pass 176. Independent here:
 - construct explicit 8x8 binary isometry between E8 Cartan quadratic
   and q=sum GF4-coordinate norms;
 - transport fixed-point-free order-three J into E8 root coordinates;
 - give exact 25 24-cell /60 axes vs H(3,4) 45/40 cross tab
   in the user's new icosian PG(3,4) matrix coordinate convention;
 - furnish a counterexample showing natural row-A5/PGL2 action
   does not preserve this chosen Hermitian form (noncanonical).
Not E8 spacetime dynamics or a physical TOE.
"""
from __future__ import annotations
import itertools,json,collections,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT/"analysis") not in sys.path:sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261104_pg34_icosian_quadric import geometry,det,mul
OUT=ROOT/"data"/"toe_20261104_e8_mod2_pg34_refinement.json"

E8_EDGES=((0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(2,7))
def parity(k):return k.bit_count()&1
def qe(v):
    return (parity(v)+sum(((v>>i)&1)*((v>>j)&1) for i,j in E8_EDGES))&1
def qh(v):
    return sum(((v>>(2*i))&1)^((v>>(2*i+1))&1)^
       (((v>>(2*i))&1)*((v>>(2*i+1))&1)) for i in range(4))&1
def b(q,u,v):return q(u^v)^q(u)^q(v)
def hyperbolic_basis(q):
    out=[];pairs=[]
    while len(out)<8:
        cand=[x for x in range(1,256) if q(x)==0 and all(b(q,x,y)==0 for y in out)]
        assert cand
        e=cand[0]
        f=next(x for x in cand if b(q,e,x)==1)
        pairs.append((e,f));out.extend([e,f])
        assert all(b(q,out[i],out[j])==int(i//2==j//2 and i!=j) for i in range(len(out)) for j in range(len(out)))
    images={0}
    for v in out:images|={z^v for z in list(images)}
    assert len(images)==256
    return out
def jh(v):
    out=0
    for k in range(4):
        a=(v>>(2*k))&1;b=(v>>(2*k+1))&1
        out|=(b<<(2*k))|((a^b)<<(2*k+1))
    return out
def f4matrix_to_int(m):
    return sum(((x&1)<<(2*i))|(((x>>1)&1)<<(2*i+1)) for i,x in enumerate(m))
def leftmul(g,m):
    a,b,c,d=g
    x,y,z,w=m
    return (mul(a,x)^mul(b,z),mul(a,y)^mul(b,w),
            mul(c,x)^mul(d,z),mul(c,y)^mul(d,w))
def main():
    be=hyperbolic_basis(qe);bh=hyperbolic_basis(qh)
    map_eh={};inv_he={}
    for c in range(256):
        e=h=0
        for i in range(8):
            if c>>i&1:e^=be[i];h^=bh[i]
        map_eh[e]=h;inv_he[h]=e
        assert qe(e)==qh(h)
    assert len(map_eh)==len(inv_he)==256
    assert sum(qe(v)==0 for v in range(256))==136
    assert sum(qh(v)==0 for v in range(256))==136
    assert sum(qe(v)==1 for v in range(256))==120
    J={e:inv_he[jh(h)] for e,h in map_eh.items()}
    assert len(J)==256 and J[0]==0
    assert all(J[J[J[e]]]==e and qe(J[e])==qe(e) for e in range(256))
    assert all(J[e]!=e for e in range(1,256))
    assert all(J[a^b]==J[a]^J[b] for a in range(256) for b in range(256))
    orbits={frozenset([x,J[x],J[J[x]]]) for x in range(1,256)}
    assert len(orbits)==85 and all(len(o)==3 for o in orbits)
    qorbit=collections.Counter(qe(next(iter(o))) for o in orbits)
    assert qorbit=={0:45,1:40}

    G=geometry()
    points=G["projective_point_coordinates_85"]
    assert len(points)==85
    qstrata=collections.Counter()
    for j,m in enumerate(points):
        v=f4matrix_to_int(m)
        qstrata[("quadric25" if j<25 else "invertible60",qh(v))]+=1
        assert v!=0 and qh(v)==qh(jh(v))
    assert qstrata=={("quadric25",0):21,("quadric25",1):4,
                     ("invertible60",0):24,("invertible60",1):36}
    # Rows of the 5x5 quadric grid are natural SL2(F4) actions.
    g=(1,1,0,1)
    assert det(g)==1
    counterexamples=[]
    for j,m in enumerate(points):
        new=leftmul(g,m)
        if qh(f4matrix_to_int(m))!=qh(f4matrix_to_int(new)):
            counterexamples.append(dict(index=j,m=m,g_times_m=new,
                q_before=qh(f4matrix_to_int(m)),q_after=qh(f4matrix_to_int(new))))
    assert counterexamples
    # q=sum Norm coordinate is not invariant under natural row action,
    # though row action preserves rank-one determinant quadric.
    assert all(det(m)==det(leftmul(g,m)) for m in points)
    # E8 Dynkin Cartan determinant 1 via exact sympy.
    import sympy as sy
    C=sy.eye(8)*2
    for i,j in E8_EDGES:C[i,j]=C[j,i]=-1
    assert C.det()==1
    return dict(status="PASS_E8_MOD2_HERMITIAN_45_40_VS_600CELL_25_60_REFINEMENT",
      E8_Cartan_determinant=1,
      E8_Cartan_dynkin_edges=[list(x) for x in E8_EDGES],
      E8_nonzero_singular_q0=135,
      E8_anisotropic_q1=120,
      explicit_E8_hyperbolic_basis_bitmasks=be,
      explicit_F4_Hermitian_hyperbolic_basis_bitmasks=bh,
      binary_isometry_E8_to_F4_Hermitian=[map_eh[i] for i in range(256)],
      E8_transport_order3_isometry=[J[i] for i in range(256)],
      E8_order3_nonzero_orbits=85,
      resulting_Hermitian_GF4_projective_isotropic_points=45,
      resulting_Hermitian_GF4_projective_nonsingular_points=40,
      icosian_quadric25_vs_hermitian_q0_q1={"q0":21,"q1":4},
      icosian_invertible60_vs_hermitian_q0_q1={"q0":24,"q1":36},
      qh_coordinate_example_not_invariant_under_PGL2_left_action=counterexamples[0],
      PGL2_left_shear_is_determinant_quadric_automorphism_but_not_qh_isometry=True,
      no_equating_25_quadric_to_45_Hermitian_points="The 25 24-cells form Q+(3,4), a 25-point quadratic quadric. The 45 Hermitian H(3,4) points are the 45 F4 lines inside E8 mod2 singular Q+(7,2) under an order3 orthogonal isometry. Even after a concrete F4 vector-space identification, these subvarieties differ (25 vs 45), and the chosen Hermitian q is not preserved by full row PGL2(4).",
      prior_art="Pass8925-8940 E8 quadratic refinement and Pass9961-9984 E8/2E8 Hermitian H(3,4) counts and Q+(7,2) refinement already in repo. New computation here is explicit Cartan bit-coordinate isometry and cross-stratum tests against the newly built icosian PG(3,4).",
      physics_boundary="Pure finite field/lattice residue; not a physical E8-to-600cell vacuum map or field-linear embedding of W33/F3.")
def write():
    result=main()
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(result["status"],result["icosian_quadric25_vs_hermitian_q0_q1"],flush=True)
    return result
if __name__=="__main__":write()
