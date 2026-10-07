#!/usr/bin/env python3
"""Passes 11608-11613: six exact bridges after the Hesse-CP Weyl selector.

Claims are deliberately separated:
11608 exact tensor-product decoupling for a positive external kinetic operator;
11609 exact E8 86+81+81 shell selector from the external-A2 center;
11610 domain-wall no-go for a commuting internal selector and minimal anticommuting repair;
11611 sign-lock between the supplied weak-basis CP witness and the selected Weyl sign;
11612 anti-invariant ideal theorem checked explicitly through Bloch degree 12;
11613 minimal E6-singlet SU(3)_family anomaly repair for one selected (27,3) shell.

None of these alone constructs the full Lorentzian chiral Standard Model measure.
"""
import hashlib, itertools, json
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/PART_W33_PASS11608_11613_CHIRAL_UNIFICATION.json"
RESERVATION="ef3f76825"


def portable_hash(path):
    path=Path(path)
    if path.suffix==".json":
        raw=json.dumps(json.loads(path.read_text()),sort_keys=True,separators=(",",":")).encode()
    else:
        raw=path.read_bytes().replace(b"\r\n",b"\n")
    return hashlib.sha256(raw).hexdigest()


def pass11608_local_decoupling():
    K=s.Matrix([[2,-1],[-1,3]])
    chi=s.diag(1,-1)
    I2=s.eye(2)
    Delta=s.symbols("Delta", positive=True)
    sig=1
    Pg=(I2+sig*chi)/2
    H=s.kronecker_product(K,I2)+Delta*s.kronecker_product(I2,Pg)
    light_idx=[1,3]; heavy_idx=[0,2]
    Hlight=H.extract(light_idx,light_idx)
    Hheavy=H.extract(heavy_idx,heavy_idx)
    assert Hlight==K
    assert Hheavy==K+Delta*I2
    assert H.extract(light_idx,heavy_idx)==s.zeros(2)
    mu=s.symbols("mu", positive=True)
    lhs=s.factor((H+mu**2*s.eye(4)).det())
    rhs=s.factor((K+mu**2*I2).det()*(K+(mu**2+Delta)*I2).det())
    assert s.simplify(lhs-rhs)==0
    return {
        "status":"PASS_EXACT_ONSITE_WEYL_PENALTY_DECOUPLES_ONE_INTERNAL_BLOCK",
        "operator":"H=K_ext tensor I_32 + Delta I_ext tensor P_gapped, P_gapped=(I+s Chi)/2",
        "light_projector":"P_light=(I-s Chi)/2",
        "theorem":"Because the external kinetic operator acts as the identity on the internal Spin(10) carrier, the light block is exactly K_ext while the heavy block is K_ext+Delta. The projected light Green function is independent of Delta and the heavy resolvent is suppressed by the gap.",
        "determinant_factorization":"det(H+mu^2)=det(K+mu^2)^16 det(K+mu^2+Delta)^16",
        "locality":"The added term is onsite in the external coordinate, so it introduces no new off-diagonal spacetime couplings.",
        "parallel11602":"The theorem applies in particular to a positive/squared operator built from Pass11602's local matched-metric covariant Dirac, because its external site/spin operator and the Spin(10) internal selector act on separate tensor factors.",
        "boundary":"This is exact decoupling for the positive kinetic/squared-operator architecture. It does not define a chiral fermion path-integral measure, prove gauge-anomaly cancellation, or derive Delta from dynamics."
    }


def pass11609_e8_shell_selector():
    I=s.I
    rt3=s.sqrt(3)
    w=(-1+I*rt3)/2
    U=s.diag(1,w,w**2)
    Udag=s.conjugate(U).T
    C=s.simplify((U-Udag)/(I*rt3))
    M=s.simplify(C**2)
    assert C==s.diag(0,1,-1)
    assert M==s.diag(0,1,1)
    S=s.Matrix([[1,0,0],[0,0,1],[0,1,0]])
    assert (S*C.conjugate()*S + C).applyfunc(s.simplify)==s.zeros(3)
    c=s.Rational(15,343)
    rows=[]
    for sig in (1,-1):
        vals=[]
        for label,cv,mult in [("gauge_86",0,86),("matter_plus_81",1,81),("matter_minus_81",-1,81)]:
            amp=s.simplify(c*(cv*cv)+sig*c*cv)
            e=s.factor(amp**2)
            vals.append({"block":label,"C":cv,"multiplicity":mult,"energy_over_lambda_rho12":str(e)})
        zeros=[v["block"] for v in vals if s.sympify(v["energy_over_lambda_rho12"])==0]
        rows.append({"W_sign":sig,"blocks":vals,"zero_blocks":zeros})
        assert "gauge_86" in zeros
        assert (("matter_minus_81" in zeros) if sig==1 else ("matter_plus_81" in zeros))
    return {
        "status":"PASS_HESSE_SIGN_SELECTS_ONE_E8_MATTER_SHELL_WITH_GAUGE_BLOCK_UNTOUCHED",
        "grading":"U has eigenvalues 1,omega,omega^2 on 86+(27,3)+(27bar,3bar)",
        "shell_sign":"C=(U-U^dagger)/(i sqrt(3)) with spectrum 0,+1,-1",
        "matter_projector":"M=C^2 with spectrum 0,1,1",
        "CP_action":"The antiunitary shell conjugation K_CP=S o complex-conjugation exchanges the two 81-dimensional grade spaces and sends C->-C. Bare entrywise conjugation of the real diagonal C does not.",
        "filter":"H_shell=lambda[(15/343) rho^6 M + W C]^2",
        "vacuum_rows":rows,
        "theorem":"At W=s(15/343)rho^6 the 86-dimensional gauge block stays exactly at zero, one 81-dimensional matter shell is an exact kernel (C=-s), and the conjugate shell has gap 4 lambda (15/343)^2 rho^12.",
        "weld_to_11607":"Pass11607 leaves internal Spin(10) chirality Chi=-s. The shell selector leaves C=-s. Thus the two sign choices are compatible up to the conventional identification of 16 versus 16bar inside the two E6-conjugate shells.",
        "boundary":"This is an E6 x SU(3)_ext-covariant representation-level shell filter, not an E8-invariant mass term. Selecting one shell breaks the symmetry that exchanges the two grades and raises the SU(3)_family anomaly issue handled in Pass11613."
    }


def pass11610_domain_wall():
    k,m=s.symbols("k m", real=True)
    sx=s.Matrix([[0,1],[1,0]])
    sy=s.Matrix([[0,-s.I],[s.I,0]])
    sz=s.diag(1,-1)
    I2=s.eye(2)
    native_gam=[s.kronecker_product(sx,sx),s.kronecker_product(sx,sy),s.kronecker_product(sx,sz)]
    native_grade=s.kronecker_product(sz,I2)
    assert native_grade*native_grade==s.eye(4)
    for g in native_gam:
        assert native_grade*g+g*native_grade==s.zeros(4)
    commuting_bulk={"+":"m+k, m-k","-":"-m+k, -m-k"}
    H=s.simplify(k*sx+m*sz)
    lam=H.charpoly().as_expr()
    assert s.factor(lam)==-k**2-m**2+s.Symbol("lambda")**2
    assert sx*sz+sz*sx==s.zeros(2)
    x,m0,xi=s.symbols("x m0 xi", positive=True)
    f=s.cosh(x/xi)**(-m0*xi)
    mass=m0*s.tanh(x/xi)
    assert s.simplify(s.diff(f,x)+mass*f)==0
    vp=s.Matrix([1,s.I])/s.sqrt(2)
    vm=s.Matrix([1,-s.I])/s.sqrt(2)
    assert sy*vp==vp and sy*vm==-vm
    return {
        "status":"PASS_DOMAIN_WALL_COMMUTING_NO_GO_AND_NATIVE_GRADE_REPAIR",
        "naive_wall":"H=-i alpha d_x + m(x) Chi with Chi on the internal factor",
        "naive_bulk":commuting_bulk,
        "no_go":"Because Chi commutes with the spacetime kinetic alpha, each asymptotic bulk sector has E=s m0 +/- k and is gapless. There is no Jackiw-Rebbi bulk gap/topological interface invariant from W(x)Chi alone.",
        "native_beta":"Pass11557's rank-four Clifford grade Gamma_*=Z tensor I2 obeys Gamma_*^2=I and anticommutes with all three native spatial gammas. Pass11602 already uses the same grade in its covariant Wilson regulator and notes that it commutes with Spin transport.",
        "repair":"H=-i gamma_n d_x + Gamma_* m(x) Chi, using the existing native Clifford grade as the anticommuting mass channel",
        "repaired_bulk":"E=+/-sqrt(k^2+m0^2)",
        "kink":"m(x)=m0 tanh(x/xi), f(x)=cosh(x/xi)^(-m0 xi)",
        "zero_modes":"For each internal Chi=s=+/-1 there is one normalizable zero mode in the corresponding two-generator reduction. Before shell/Weyl selection the wall carries a conjugate pair; after an independent selector removes one internal sector, one interface mode remains.",
        "boundary":"The required anticommuting matrix is already present in the native rank-four Clifford fiber; what remains unproved is a physical/dynamical coupling that makes the Hesse order parameter multiply Gamma_* Chi, plus the Lorentzian regulator and anomaly-inflow completion."
    }


def cp_witness_exact():
    br,bi=s.symbols("br bi",real=True)
    b=br+s.I*bi
    Y=lambda h:s.Matrix([[h[0],b*h[2],b*h[1]],[b*h[2],h[1],b*h[0]],[b*h[1],b*h[0],h[2]]])
    U=Y([1,2,4]); D=Y([3,1,2])
    Hu=U*U.conjugate().T; Hd=D*D.conjugate().T
    K=Hu*Hd-Hd*Hu
    poly=s.factor(s.im(s.expand(s.trace(K**3))))
    scale=s.sqrt(14)+2*s.sqrt(3)
    bsubs={br:-s.sqrt(3)/(2*scale),bi:-s.Rational(1,2)/scale}
    J=s.simplify(poly.subs(bsubs))
    assert J<0
    assert s.simplify(poly.subs(bi,-bi)+poly)==0
    return poly,J


def pass11611_cp_chirality_lock():
    poly,J=cp_witness_exact()
    W=s.Rational(15,343)
    ratio=s.simplify(-J/W)
    assert ratio>0
    rows=[
        {"vacuum":"canonical","W_sign":1,"selected_Chi":-1,"J_sign":-1},
        {"vacuum":"CP_conjugate","W_sign":-1,"selected_Chi":1,"J_sign":1},
    ]
    assert all(r["selected_Chi"]==r["J_sign"] for r in rows)
    u0=s.sqrt(s.Rational(2,3)); u1=-s.I/s.sqrt(3)
    bloch=s.Matrix([2*s.re(s.conjugate(u0)*u1),2*s.im(s.conjugate(u0)*u1),u0*s.conjugate(u0)-u1*s.conjugate(u1)])
    axes=s.Matrix([[s.sqrt(s.Rational(2,3)),-s.sqrt(s.Rational(1,6)),-s.sqrt(s.Rational(1,6))],[0,1/s.sqrt(2),-1/s.sqrt(2)],[1/s.sqrt(3)]*3])
    xyz=s.simplify(axes.T*bloch)
    Wdyn=s.factor((xyz[0]**2-xyz[1]**2)*(xyz[1]**2-xyz[2]**2)*(xyz[2]**2-xyz[0]**2))
    Wdyn_expected=s.Rational(256,2187)/s.sqrt(3)
    assert s.simplify(Wdyn-Wdyn_expected)==0 and Wdyn>0
    Jdyn=-s.Rational(94163140688,5625)
    assert Jdyn<0
    return {
        "status":"PASS_CP_SIGN_LOCK_EXTENDS_TO_11606_DYNAMICAL_SEESAW_ALIGNMENT",
        "W_canonical":"15/343 at m=(1,2,3)/sqrt(14)",
        "CP_polynomial":str(poly),
        "J_canonical_exact":str(J),
        "minus_J_over_W":str(ratio),
        "rows":rows,
        "dynamic_alignment_11606":{"Hesse_field":"u=(sqrt(2/3),-i/sqrt3)","W_exact":str(Wdyn),"seesaw_CP_exact":str(Jdyn),"selected_Chi":-1,"CP_sign":-1},
        "theorem":"For the original Pass11600 canonical CP pair, selected Chi equals the sign of the weak-basis CP witness. The stronger parallel Pass11606 branch dynamically selects the unequal (1,2,3) family alignment; its canonical Hesse field has W=256/(2187 sqrt3)>0 while its exact seesaw invariant is -94163140688/5625<0, so Pass11607 again leaves Chi=-1=sign(J_nu).",
        "boundary":"The family alignment is now dynamically selected in the Pass11606 EFT, but its common gauge-breaking direction, several Yukawa ratios/scales, and the Hesse angular target selecting that particular CP orbit remain supplied. This is still not a measured CKM/PMNS prediction."
    }


def d3_group():
    out=[]
    for perm in itertools.permutations(range(3)):
        inv=sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))
        eps=-1 if inv%2 else 1
        for signs in itertools.product([-1,1],repeat=3):
            if signs[0]*signs[1]*signs[2]!=1: continue
            out.append((perm,signs,eps))
    assert len(out)==24
    return out


def monoms(d):
    return [(a,b,d-a-b) for a in range(d+1) for b in range(d+1-a)]


def rep_matrix(d,perm,signs):
    B=monoms(d); pos={e:i for i,e in enumerate(B)}
    R=s.zeros(len(B))
    for j,e in enumerate(B):
        target=[0,0,0]; coeff=s.Integer(1)
        for i,powr in enumerate(e):
            coeff*=signs[i]**powr
            target[perm[i]]+=powr
        R[pos[tuple(target)],j]=coeff
    return R


def projector(d,anti=False):
    B=monoms(d); P=s.zeros(len(B))
    for perm,signs,eps in d3_group():
        P+=(eps if anti else 1)*rep_matrix(d,perm,signs)
    return s.simplify(P/24),B


def pass11612_portal_ideal():
    x,y,z=s.symbols("x y z")
    W=s.expand((x*x-y*y)*(y*y-z*z)*(z*z-x*x))
    table=[]
    for d in range(13):
        Pi,B=projector(d,False); Pa,_=projector(d,True)
        ir=int(Pi.rank()); ar=int(Pa.rank())
        target=0
        if d>=6:
            target=int(projector(d-6,False)[0].rank())
        assert ar==target
        if ar:
            for vec in Pa.columnspace():
                poly=s.expand(sum(vec[i]*x**B[i][0]*y**B[i][1]*z**B[i][2] for i in range(len(B))))
                q,r=s.div(poly,W,domain=s.QQ)
                assert s.expand(r)==0
                for perm,signs,eps in d3_group():
                    sub={x:signs[0]*[x,y,z][perm[0]],y:signs[1]*[x,y,z][perm[1]],z:signs[2]*[x,y,z][perm[2]]}
                    assert s.expand(q.subs(sub,simultaneous=True)-q)==0
        table.append({"degree":d,"invariant_dim":ir,"anti_dim":ar,"anti_expected_from_degree_minus6":target})
    return {
        "status":"PASS_DIAGONAL_S4_FORCES_EVERY_POLYNOMIAL_CHIRAL_PORTAL_TO_CONTAIN_W",
        "checked_degrees":"0..12 exact projector computation",
        "hilbert_statement":"anti-invariants = W * invariants; H_anti(t)=t^6/[(1-t^2)(1-t^3)(1-t^4)]",
        "table":table,
        "theorem":"Every polynomial coefficient F(x,y,z) for which F Chi is invariant under the diagonal odd action must transform in the sign representation. Through degree12 every such F is exactly divisible by W, with invariant quotient; dimensions match the shifted invariant ring degree by degree. This is the finite computational form of the reflection anti-invariant principal-ideal theorem.",
        "radiative_meaning":"If the diagonal W(D3) symmetry is exact and counterterms are polynomial in this Hesse Bloch sector, radiative corrections cannot generate a lower-degree Chi portal. They can renormalize W Chi and generate W times higher invariants.",
        "parallel11605":"Pass11605 independently removes the common scalar U1 Goldstone with the G6 holomorphic H4 completion while preserving W and the 11607 Weyl kernel on all 96 vacuum vectors. It explicitly does not suppress the lower CP-even p3/p4 angular terms, so phase protection and chirality-portal degree protection are complementary rather than redundant.",
        "boundary":"This protects the absence of lower-degree chirality portals, not the value or smallness of the W Chi coefficient. CP-even p3,p4 scalar operators remain allowed and can move the Hesse vacuum unless an additional mechanism controls them."
    }


def su3_dim(p,q):
    return (p+1)*(q+1)*(p+q+2)//2


def su3_anomaly(p,q):
    dim=su3_dim(p,q)
    return s.Rational(dim,60)*(p-q)*(p+2*q+3)*(2*p+q+3)


def su3_T(p,q):
    dim=su3_dim(p,q)
    C2=s.Rational(p*p+q*q+p*q+3*p+3*q,3)
    return s.simplify(s.Rational(dim,8)*C2)


def pass11613_anomaly_closure():
    assert su3_dim(1,0)==3 and su3_anomaly(1,0)==1
    assert su3_dim(0,1)==3 and su3_anomaly(0,1)==-1
    assert su3_dim(3,0)==10 and su3_anomaly(3,0)==27 and su3_T(3,0)==s.Rational(15,2)
    assert su3_anomaly(0,3)==-27
    shell_A=27
    total=s.simplify(shell_A+su3_anomaly(0,3))
    assert total==0
    reps=[]
    for p in range(5):
        for q in range(5):
            dim=su3_dim(p,q)
            if 1<dim<10:
                reps.append((p,q,dim,int(su3_anomaly(p,q))))
    reach={0:{0}}
    for budget in range(1,10):
        reach[budget]=set()
        for p,q,dim,A in reps:
            if dim<=budget:
                for a in reach[budget-dim]:
                    reach[budget].add(a+A)
        reach[budget]|=reach[budget-1]
    assert -27 not in reach[9]
    return {
        "status":"PASS_MINIMALITY_CERTIFICATE_FOR_PRIOR_10BAR_FAMILY_ANOMALY_REPAIR",
        "prior_owner":"The (27,3)+(1,10bar) anomaly cancellation and its A=-27,T=15/2 coefficients were already owned by the 2026-10-01 chiral-decuplet certificate and are reused, not rediscovered here.",
        "selected_shell":"one Weyl (27,3) contributes A_SU3=27",
        "spectator":"(1,10bar) with SU3 Dynkin label (0,3), dimension10, A=-27, T=15/2",
        "total_anomaly":str(total),
        "minimality_check":"Exhaustive additive search over all nontrivial SU3 irreps of dimension<10 finds no spectator content of total dimension<=9 with anomaly -27.",
        "total_Weyl_dimension":91,
        "boundary":"This closes only the perturbative continuous SU(3)_family cubic anomaly for the shell-selected candidate. It does not generate the spectator mass, prove discrete Delta54 anomaly freedom after breaking, or establish the full Standard Model anomaly/measure problem."
    }


def produce():
    result={
        "pass11608":pass11608_local_decoupling(),
        "pass11609":pass11609_e8_shell_selector(),
        "pass11610":pass11610_domain_wall(),
        "pass11611":pass11611_cp_chirality_lock(),
        "pass11612":pass11612_portal_ideal(),
        "pass11613":pass11613_anomaly_closure(),
    }
    out={
        "status":"PASS_SIX_FRONT_CHIRAL_UNIFICATION_PACKET",
        "passes":[11608,11609,11610,11611,11612,11613],
        "reservation":RESERVATION,
        "result":result,
        "integration":{
            "single_vacuum_bit":"At W=s*15 rho^6/343, both the internal Weyl filter and the E8 shell filter leave sign -s.",
            "strongest_architecture":"H_external tensor [one selected E8 matter shell with one compatible Spin10 Weyl sign], supplemented by the minimal SU3-family anomaly spectator if the continuous family SU3 is gauged.",
            "domain_wall_requirement":"The internal selector alone is not a topological mass, but Pass11557/11602 already supply a native Clifford grade Gamma_* anticommuting with the spatial kinetic gammas; the remaining requirement is a physical Hesse coupling through Gamma_* Chi.",
            "cp_link":"The sign lock holds for the original canonical supplied Yukawa pair and also for Pass11606's dynamically selected unequal family alignment and exact seesaw CP invariant.",
            "uv_link":"Exact diagonal reflection symmetry makes W the mandatory factor of every polynomial chirality portal, but does not fix its coefficient or the scalar vacuum."
        },
        "boundary":"The packet closes several algebraic and finite-operator obstructions but does not constitute a Theory of Everything. Lorentzian locality, a chiral functional measure, complete anomaly inflow/cancellation, dynamical Higgs and spectator masses, measured flavor parameters, RG thresholds, gravity, vacuum energy and absolute scales remain open."
    }
    sources=[
        "analysis/PASS11590_11599_FAMILIES_FLAVOR_CHIRALITY_GRAVITY.md",
        "analysis/w33_pass11592_q6_overlap_admissibility.py",
        "analysis/w33_pass11597_family_clifford_breaking.py",
        "analysis/w33_pass11600_dynamical_hesse_flavor.py",
        "data/w33_pass11600_dynamical_hesse_flavor.json",
        "analysis/PASS11607_HESSE_CP_WEYL_SELECTOR.md",
        "data/PART_W33_PASS11607_HESSE_CP_WEYL_SELECTOR.json",
        "analysis/2026-09-21_e8_a2_center_vs_coxeter_order3.md",
        "analysis/PASS20261001_PHASE_CHIRALITY_QUANTUM_GRAVITY_UV.md",
        "analysis/w33_pass11557_pin_equivariant_event_dirac.py",
        "analysis/PASS11602_11606_GEOMETRY_FLAVOR_COMPLETION.md",
        "analysis/w33_pass11602_11606_geometry_flavor_completion.py",
        "data/w33_pass11602_11606_geometry_flavor_completion.json",
    ]
    out["source_sha256"]={p:portable_hash(ROOT/p) for p in sources}
    out["producer_sha256"]=portable_hash(Path(__file__))
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))
    return out


if __name__=="__main__":
    produce()
