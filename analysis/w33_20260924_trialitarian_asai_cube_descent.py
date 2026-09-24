#!/usr/bin/env python3
"""2026-09-24: exact trialitarian / cubic tensor-induction descent certificate."""
from __future__ import annotations
import contextlib, importlib.util, io, json
from fractions import Fraction
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20260924_trialitarian_asai_cube_descent.json"

def load_quiet(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    return mod

cm=load_quiet(ROOT/"analysis/w33_20260923_cubic_jacobi_char0_modules.py","cm")
residual=json.loads((ROOT/"data/w33_20260923_cubic_jacobi_residual.json").read_text())
split=json.loads((ROOT/"data/w33_20260923_cubic_jacobi_stu_split.json").read_text())
assert residual["ambient"]["dimension"]==24
assert residual["radical"]["dimension"]==15
assert residual["levi_quotient"]["dimension"]==9

def comm_basis(mats,n):
    xs=sp.symbols("x0:"+str(n*n))
    X=sp.Matrix(n,n,xs); eq=[]
    for A in mats:
        eq.extend(list(X*A-A*X))
    M,_=sp.linear_eq_to_matrix(eq,xs)
    return [sp.Matrix(n,n,list(v)) for v in M.nullspace()]

def altform_dim(mats,n):
    pairs=[(i,j) for i in range(n) for j in range(i+1,n)]
    xs=sp.symbols("a0:"+str(len(pairs)))
    J=sp.zeros(n)
    for z,(i,j) in zip(xs,pairs):
        J[i,j]=z; J[j,i]=-z
    eq=[]
    for A in mats:
        eq.extend(list(A.T*J+J*A))
    M,_=sp.linear_eq_to_matrix(eq,xs)
    return len(M.nullspace())

def assoc_dim(mats,n):
    B=cm.dw.RationalBasis()
    def vec(M):
        return [Fraction(sp.Rational(x).p,sp.Rational(x).q) for x in list(M)]
    I=sp.eye(n); B.add(vec(I),0); q=[I]
    while q:
        X=q.pop()
        for G in mats:
            Y=X*G
            if B.add(vec(Y),0):
                v=B.vectors[-1]
                q.append(sp.Matrix(n,n,[sp.Rational(x.numerator,x.denominator) for x in v]))
    return len(B.rows)

C6=comm_basis(cm.acts6,6)
C8=comm_basis(cm.acts8,8)
assert len(C6)==3 and len(C8)==1
assert C8[0]==sp.eye(8)

T=C6[0]
a=sp.Rational(104871216804430401138728488244357508,
              490911288408909443328849525019831075)
b=sp.Rational(73738537872963509415473834655,
              4023490764400871053252753562)
c=-sp.Rational(506547027866427733563,
               824409537601361483308)
Theta=sp.simplify(a*T**2+b*T+c*sp.eye(6))
theta_residual=sp.simplify(Theta**3-Theta**2-53*Theta-120*sp.eye(6))
assert theta_residual==sp.zeros(6)
assert sp.factor(Theta.charpoly().as_expr())==(sp.Symbol("lambda")**3-sp.Symbol("lambda")**2-53*sp.Symbol("lambda")-120)**2

def action_rank(mats,n):
    return sp.Matrix.hstack(*[sp.Matrix(A).reshape(n*n,1) for A in mats]).rank()

assert action_rank(cm.acts6,6)==9
assert action_rank(cm.acts8,8)==9
assert assoc_dim(cm.acts6,6)==12
assert assoc_dim(cm.acts8,8)==64

# Exact Heisenberg symplectic decomposition.
z=cm.Z.vectors[0]
zp=sorted(cm.Z.rows)[0]
zinv=Fraction(1,1)/z[zp]

def omega(A,B):
    M=sp.zeros(len(A),len(B))
    for i,u in enumerate(A):
        for j,v in enumerate(B):
            w=cm.br(u,v)
            coeff=Fraction(w[zp])*zinv
            assert all(Fraction(x)==coeff*Fraction(y) for x,y in zip(w,z))
            M[i,j]=sp.Rational(coeff.numerator,coeff.denominator)
    return M

O8=omega(cm.W8,cm.W8)
O6raw=omega(cm.U6,cm.U6)
Cross=omega(cm.W8,cm.U6)
assert O8.rank()==8 and O6raw.rank()==6
Acoef=-O8.inv()*Cross

U6orth=[]
for j,u in enumerate(cm.U6):
    v=[Fraction(x) for x in u]
    for i,w in enumerate(cm.W8):
        q=sp.Rational(Acoef[i,j])
        if q:
            qc=Fraction(int(q.p),int(q.q))
            v=[x+qc*Fraction(y) for x,y in zip(v,w)]
    U6orth.append(v)

assert omega(cm.W8,U6orth)==sp.zeros(8,6)
O6orth=omega(U6orth,U6orth)
assert O6orth.rank()==6

# Objectwise central-product audit.  The orthogonal complement is not merely a
# quotient-level copy of U6: it is preserved exactly by all nine rational Levi
# basis elements, commutes with W8, and joins W8 along the common center.
phase_basis=cm.W8+U6orth+[z]
phase_matrix=sp.Matrix.hstack(*[sp.Matrix(v) for v in phase_basis])
_,phase_pivot_rows=phase_matrix.T.rref()
phase_pivot_rows=list(phase_pivot_rows)
assert len(phase_pivot_rows)==15
phase_minor=phase_matrix.extract(phase_pivot_rows,range(15))
phase_minor_det=sp.Rational(phase_minor.det())
assert phase_minor_det==-1
phase_minor_inv=phase_minor.inv()
levi_complement_checks=0
for s in cm.Q9:
    for u in U6orth:
        v=sp.Matrix([
            sp.Rational(q.numerator,q.denominator) for q in cm.br(s,u)
        ])
        coeff=phase_minor_inv*v.extract(phase_pivot_rows,[0])
        assert phase_matrix*coeff==v
        assert coeff[:8,0]==sp.zeros(8,1)
        assert coeff[14,0]==0
        levi_complement_checks+=1
cross_brackets_zero=all(
    not any(cm.br(w,u)) for w in cm.W8 for u in U6orth
)
assert cross_brackets_zero and levi_complement_checks==54

x=sp.symbols("x")
kpoly=x**3-x**2-53*x-120
kdisc=int(sp.discriminant(kpoly,x))
assert sp.factor(kpoly)==kpoly and kdisc==94557
assert int(sp.sqrt(kdisc))**2!=kdisc
galois_closure="S3"

# Over a splitting field, an irreducible sl2^3 module with highest weights
# (a,b,c) has dimension (a+1)(b+1)(c+1).  Rational descent through the full
# S3 Galois action requires an S3-fixed triple.  Enumerate the dimension-eight
# possibilities instead of leaving this representation-theoretic step implicit.
dimension_eight_highest_weights=[]
for a in range(8):
    for b in range(8):
        for c in range(8):
            if (a+1)*(b+1)*(c+1)==8:
                dimension_eight_highest_weights.append([a,b,c])
s3_fixed_dimension_eight=[w for w in dimension_eight_highest_weights if len(set(w))==1]
assert s3_fixed_dimension_eight==[[1,1,1]]

alt8=altform_dim(cm.acts8,8)
alt6=altform_dim(cm.acts6,6)
assert (alt8,alt6)==(1,3)

for run in split["runs"]:
    assert run["factor_derived_dimensions"]==[3,3,3]
    assert run["factor_cross_brackets_zero"] is True
    assert run["associative_algebra_dimensions"]=={"W8":64,"U6":12}
    assert run["commutant_dimensions"]=={"W8":1,"U6":3}

d4=json.loads((ROOT/"data/w33_pass409_d4_contact_root_census.json").read_text())
assert d4["comparison_to_repo_core"]["fingerprint_matches"] is True
assert d4["derived_contact_parabolic_dimension"]==18

out={
    "schema":"w33.20260924.trialitarian_asai_cube_descent.v1",
    "status":"PASS_TRIALITARIAN_D4_ASAI_CUBE_DESCENT",
    "cubic_field":{
        "polynomial":"x^3 - x^2 - 53*x - 120",
        "discriminant":kdisc,
        "galois_closure":galois_closure,
        "ramified_primes":[3,43,733],
    },
    "levi":{
        "Q_dimension":9,
        "type":"Res_{K/Q} sl2(K)",
        "source":"Pass 409 exact cubic-Jacobi quotient",
    },
    "restricted_standard_U6":{
        "Q_dimension":6,
        "commutant_dimension":len(C6),
        "commutant_generator_charpoly":"(lambda^3-lambda^2-53*lambda-120)^2",
        "theta_relation_exact":True,
        "action_rank":9,
        "associative_envelope_Q_dimension":12,
        "identification":"Res_{K/Q}(K^2), with End_{S9}(U6)=K and envelope End_K(K^2)=M2(K)",
        "invariant_alternating_form_dimension":alt6,
    },

    "asai_cube_W8":{
        "Q_dimension":8,
        "commutant_dimension":len(C8),
        "action_rank":9,
        "associative_envelope_Q_dimension":64,
        "absolutely_irreducible":True,
        "dimension_eight_highest_weights":dimension_eight_highest_weights,
        "S3_fixed_dimension_eight_highest_weights":s3_fixed_dimension_eight,
        "split_highest_weight":"(1,1,1)",
        "identification":"cubic tensor induction / Asai-cube representation of the standard K^2 module",
        "invariant_alternating_form_dimension":alt8,
        "quartic_invariant_dimension":1,
        "quartic_name_after_splitting":"Cayley 2x2x2 hyperdeterminant",
    },
    "heisenberg_phase_space":{
        "dimension_mod_center":14,
        "W8_symplectic_rank":O8.rank(),
        "raw_U6_symplectic_rank":O6raw.rank(),
        "raw_cross_rank":Cross.rank(),
        "orthogonalized_cross_rank":omega(cm.W8,U6orth).rank(),
        "orthogonal_U6_symplectic_rank":O6orth.rank(),
        "decomposition":"h7/Z = AsaiCube_8 orthogonal_sum ResStd_6",
        "phase_basis_pivot_minor_determinant":int(phase_minor_det),
        "levi_preserves_orthogonal_U6_checks":levi_complement_checks,
        "W8_U6orth_cross_brackets_zero":cross_brackets_zero,
        "central_product":"h7 = h4 *_Z h3",
        "virtual_hardware_ABI":"8-coordinate Asai-cube data lane and 6-coordinate restricted-standard control lane commute and share one central phase register",
    },
    "trialitarian_D4_core":{
        "dimension":18,
        "structure":"Res_{K/Q} sl2(K) semidirect h4",
        "identification":"derived contact parabolic of the trialitarian D4 form attached to K",
        "why":"Over the Galois closure the Levi splits as sl2^3, W8 is the (2,2,2) tensor module, and its invariant alternating form is unique up to scale.",
        "outer_galois_action":"S3 triality",
    },

    "literature_alignment":[
        "Henniart-Lomeli: trialitarian D4 attached to a cubic extension has Levi derived group Res SL2; Asai cube is cubic tensor induction.",
        "Knus-Tignol: D4 triality is governed by the S3 outer symmetry and cubic etale data.",
        "Bremner-Bickis-Soltanifar: the 2x2x2 tensor representation has its first nonconstant invariant in degree 4, Cayley's hyperdeterminant.",
    ],
    "boundary":"This is an exact finite/rational Lie-module descent theorem. It does not imply an automorphic L-function is physically realized, nor derive spacetime, particle generations, couplings, black-hole entropy, or laboratory dynamics."
}
OUT.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
print(json.dumps({
    "status":out["status"],
    "K":out["cubic_field"],
    "U6_end":out["restricted_standard_U6"]["commutant_dimension"],
    "W8_end":out["asai_cube_W8"]["commutant_dimension"],
    "orthogonal_cross_rank":out["heisenberg_phase_space"]["orthogonalized_cross_rank"],
},indent=2))
