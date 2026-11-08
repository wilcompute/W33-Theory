#!/usr/bin/env python3
"""Five physical interfaces plus exact 27-mode Forty Points clock completion.

All results are conditional mathematical/computational certificates, not a TOE.
Uses numpy and sympy; runs without network; does not modify existing fixtures.
Original clock owners: Pass 20260924, Pass 11166, Pass 11541.
"""
from __future__ import annotations
import argparse, ast, itertools, json, math
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path
import numpy as np
import sympy as sp

F3 = list(itertools.product(range(3), repeat=3))
IDX = {v:i for i,v in enumerate(F3)}
OMEGA = np.exp(2j*np.pi/3)

def quad(v):
    a,b,c=v
    return (a*c-b*b)%3

def diff(u,v):
    return tuple((a-b)%3 for a,b in zip(u,v))

def null_clock():
    null=[v for v in F3 if v!=(0,0,0) and quad(v)==0]
    assert len(null)==8
    reps=[v for v in null if v<tuple((-x)%3 for x in v)]
    assert len(reps)==4
    phase={}
    adjacency_eigs={}
    for k in F3:
        n0=sum(sum(ki*ni for ki,ni in zip(k,n))%3==0 for n in reps)
        lamA=3*n0-4
        adjacency_eigs[k]=lamA
        phase[k]=(n0-4)%3
    assert Counter(adjacency_eigs.values())==Counter({8:1,2:12,-1:8,-4:6})
    table={}
    for d in F3:
        counts=[0,0,0]
        for k in F3:
            counts[(phase[k]+sum(x*y for x,y in zip(k,d)))%3]+=1
        category="origin" if d==(0,0,0) else "null" if quad(d)==0 else f"q={quad(d)}"
        table.setdefault(category,set()).add(tuple(counts))
    expected={"origin":(9,12,6),"null":(9,12,6),
              "q=1":(6,9,12),"q=2":(12,6,9)}
    assert {k:next(iter(v)) for k,v in table.items()}==expected
    A=np.zeros((27,27),float)
    for i,u in enumerate(F3):
        for j,v in enumerate(F3):
            if i!=j and diff(u,v) in null:A[i,j]=1.
    L=8*np.eye(27)-A
    eig,V=np.linalg.eigh(L)
    U=(V*np.exp(-2j*np.pi*eig/9))@V.conj().T
    H=np.array([[OMEGA**((1+quad(diff(u,v)))%3) for v in F3] for u in F3])
    closed=np.exp(-1j*np.pi/6)*H/np.sqrt(27)
    error=float(np.max(np.abs(U-closed)))
    flat_error=float(np.max(np.abs(U)**2-1/27))
    cubic_error=float(np.max(np.abs(U@U@U-np.eye(27))))
    assert max(error,flat_error,cubic_error)<1e-12
    # An invertible finite-linear change (a,b,c)->((a+c)/2,(a-c)/2,b).
    def diagonal_chart(v):
        a,b,c=v
        return (2*(a+c)%3,2*(a-c)%3,b)
    P=np.zeros((27,27),float)
    for i,v in enumerate(F3):P[IDX[diagonal_chart(v)],i]=1
    def chirp(s):
        return np.array([[OMEGA**(s*((i-j)**2)%3)/np.sqrt(3)
                          for j in range(3)] for i in range(3)])
    product=OMEGA*np.exp(-1j*np.pi/6)*np.kron(np.kron(chirp(1),chirp(-1)),chirp(-1))
    factor_error=float(np.max(abs(P@U@P.T-product)))
    assert factor_error<1e-12
    # In native (a,b,c) tensor factors, U|000> entangles a,c maximally.
    psi=U[:,IDX[(0,0,0)]].reshape((3,3,3))
    rhoa=np.einsum("abc,dbc->ad",psi,psi.conj())
    rhob=np.einsum("abc,adc->bd",psi,psi.conj())
    assert np.max(abs(rhoa-np.eye(3)/3))<1e-12
    assert abs(np.trace(rhob@rhob)-1)<1e-12
    # Mode phases can be gauged by input/output; plaquettes are gauge invariant.
    plaquettes=[]
    a=(0,0,0);b=(1,0,0);c=(0,0,0)
    for label,d in (("omega",(0,0,2)),("omega2",(0,0,1)),("unity",(0,1,0))):
        # For q(a,b,c)=ac-b², polar dot is a*c'+c*a'-2*b*b'.
        ab=tuple((x-y)%3 for x,y in zip(a,b))
        dc=tuple((x-y)%3 for x,y in zip(d,c))
        bilinear=(ab[0]*dc[2]+ab[2]*dc[0]-2*ab[1]*dc[1])%3
        exp=(bilinear)%3 # q sum cross difference equals B(a-b,d-c)
        z=U[IDX[a],IDX[c]]*U[IDX[b],IDX[d]]*np.conj(U[IDX[a],IDX[d]]*U[IDX[b],IDX[c]])
        z/=abs(z)
        assert abs(z-OMEGA**exp)<1e-12
        plaquettes.append({"label":label,"input_a":list(a),"input_b":list(b),
                           "output_c":list(c),"output_d":list(d),
                           "expected_root_power":exp,
                           "expected_complex":[float(z.real),float(z.imag)]})
    return {
        "status":"EXACT_CYCLOTOMIC_COUNTS_AND_FLOATING_MATRIX_CHECK",
        "input":"W33 27 transverse Lagrangians, symmetric binary forms over F3",
        "null_vectors":len(null),"vertices":27,"degree":8,
        "laplacian_spectrum":{"0":1,"6":12,"9":8,"12":6},
        "time":"2*pi/9",
        "exact_character_residue_counts":{k:list(v) for k,v in expected.items()},
        "exact_closed_kernel":"exp(-i*pi/6)/sqrt(27) * omega^(1+q(u-v))",
        "exact_uniform_probability":"1/27 for ALL 729 input/output pairs",
        "numeric_kernel_residual":error,"numeric_flatness_residual":flat_error,
        "numeric_order_three_residual":cubic_error,
        "diagonal_chart_Kronecker_residual":factor_error,
        "native_a_entanglement_entropy_trits":1,
        "native_b_entanglement_entropy_trits":0,
        "phase_plaquettes":plaquettes,
        "caveat":"Tensor factorization is chart dependent; the native a/c qudits entangle. This is finite qutrit Clifford quantum mechanics, not a new physical force."
    },A,U

def gauge_front(A):
    edges=[(i,j) for i in range(27) for j in range(i+1,27) if A[i,j]]
    E={edge:k for k,edge in enumerate(edges)}
    triangles=[(i,j,k) for i in range(27) for j in range(i+1,27)
               for k in range(j+1,27)
               if (i,j) in E and (i,k) in E and (j,k) in E]
    assert len(edges)==108 and len(triangles)==36
    B1=np.zeros((27,108),int)
    B2=np.zeros((108,36),int)
    for idx,(i,j) in enumerate(edges): B1[i,idx]=-1;B1[j,idx]=1
    for idx,(i,j,k) in enumerate(triangles):
        B2[E[i,j],idx]+=1;B2[E[i,k],idx]-=1;B2[E[j,k],idx]+=1
    assert np.max(abs(B1@B2))==0
    r1=int(np.linalg.matrix_rank(B1))
    r2=int(np.linalg.matrix_rank(B2))
    assert r1==26 and r2==36
    # Curvature F=B2^T A is invariant under A->A+B1^T lambda.
    edge_field=np.sin(np.arange(108)*0.31+.17)
    gauge=np.cos(np.arange(27)*0.47+.11)
    flux=B2.T@edge_field
    changed=B2.T@(edge_field+B1.T@gauge)
    err=float(np.max(abs(flux-changed)))
    assert err<1e-12
    action={str(g):float(flux@flux/(4*g*g)) for g in (1.,2.)}
    assert abs(action["1.0"]/action["2.0"]-4)<1e-10
    return {"status":"GAUGE_INVARIANT_ACTION_CONSTRUCTED_COUPLING_NOT_SELECTED",
            "vertices":27,"edges":108,"oriented_faces":36,
            "rank_d0":r1,"rank_d1":r2,"cohomology_H1_dimension":108-r1-r2,
            "boundary_squared_zero":True,"gauge_invariance_residual":err,
            "maxwell_F2_action_at_supplied_g":action,
            "claim":"All g>0 fit the same combinatorial incidence and Ward/gauge identities; an independent kinetic and charge normalization is required for physical alpha.",
            "scope":"Finite simplicial U(1) toy on Forty Points null complex; not a renormalized 3+1D Maxwell action or a derivation of e."}

def flavor_front():
    I=sp.I; w=(-1+I*sp.sqrt(3))/2
    # 3x3 qutrit real cyclic adjacency, real positive matrix Y_d.
    K=sp.Matrix([[0,1,1],[1,0,1],[1,1,0]])
    Yd=sp.diag(1,2,4)+K/3
    B=sp.Matrix([[1,w,-1]])
    M=Yd.row_join(sp.zeros(3,1)).col_join(B.row_join(sp.Matrix([[5]])))
    detM=sp.simplify(M.det())
    assert detM==sp.Rational(985,27) and detM>0
    H=sp.simplify(M*M.conjugate().T)
    Heff=H[:3,:3]-H[:3,3:4]*H[3:4,:3]/H[3,3]
    inv=sp.simplify(sp.im(Heff[0,1]*Heff[1,2]*Heff[2,0]))
    assert inv == -sp.Rational(170449,571536)*sp.sqrt(3)
    assert sp.simplify(inv)!=0
    # Exact generalized-CP restriction (all phases real) kills this CP witness.
    Mreal=Yd.row_join(sp.zeros(3,1)).col_join(sp.Matrix([[1,1,-1,5]]))
    Hr=Mreal*Mreal.T
    Ehr=Hr[:3,:3]-Hr[:3,3:4]*Hr[3:4,:3]/Hr[3,3]
    assert sp.im(Ehr[0,1]*Ehr[1,2]*Ehr[2,0])==0
    return {"status":"EXACT_CONDITIONAL_NELSON_BARR_QUTRIT_WITNESS",
            "construction":"M_down=[[diag(1,2,4)+(X+X^T)/3, 0], [(1,omega,-1), 5]], omega=exp(2*pi*i/3)",
            "determinant_exact":str(detM),
            "tree_arg_det":0,
            "effective_CP_weak_basis_invariant_exact":str(inv),
            "effective_CP_weak_basis_invariant_float":float(sp.N(inv)),
            "CP_invariant_when_row_real":0,
            "physical_boundary":"This explicit 3+1 block is a toy: the real Yd entries, vectorlike mass 5, and one phase are inputs. It does not derive D-flat E6 vacuum, measured Yukawas, full CKM/PMNS, loop-protected strong CP, or threshold stability."}

def transmutation_front():
    # For beta_g=-b0 g^3/(16*pi^2), Lambda/mu=exp[-8*pi^2/(b0 g(mu)^2)].
    rows=[]
    for b0 in (7,9,11): # supplied particle-content examples, NOT predictions
        for g2 in (0.25,0.5,1.0):
            log_lambda=-8*math.pi**2/(b0*g2)
            rows.append({"b0_input":b0,"g_squared_input":g2,
                         "log_Lambda_over_mu":log_lambda,
                         "Lambda_over_mu":math.exp(log_lambda)})
    for g in (0.4,0.6,0.8):
        assert math.exp(-8*math.pi**2/(9*g*g))>0
    return {"status":"DIMENSIONAL_TRANSMUTATION_WORKS_CONDITIONALLY_BUT_NO_SCALE_PREDICTION",
            "beta":"mu dg/dmu=-b0*g^3/(16*pi^2)",
            "one_loop_formula":"Lambda=mu_ref*exp[-8*pi^2/(b0*g(mu_ref)^2)]",
            "example_ratios":rows,"unfixed_inputs":["mu_ref in physical units","g(mu_ref)","b0 and charged matter spectrum","renormalization scheme"],
            "scheme_rescaling_example":"g_prime^2=g^2+c g^4 gives Lambda_prime/Lambda -> exp(8*pi^2*c/b0) in asymptotic weak-coupling limit",
            "conclusion":"Dimensionful scales do not arise uniquely from bare W33 incidence even after choosing an asymptotically free beta equation."}

def safe_rational(expression):
    """Parse only integer/rational arithmetic AST; never evaluate a source expression."""
    def calc(node):
        if isinstance(node,ast.Constant) and type(node.value) is int:
            return Fraction(node.value,1)
        if isinstance(node,ast.UnaryOp) and isinstance(node.op,(ast.UAdd,ast.USub)):
            a=calc(node.operand)
            return -a if isinstance(node.op,ast.USub) else a
        if isinstance(node,ast.BinOp):
            a,b=calc(node.left),calc(node.right)
            if isinstance(node.op,ast.Add):return a+b
            if isinstance(node.op,ast.Sub):return a-b
            if isinstance(node.op,ast.Mult):return a*b
            if isinstance(node.op,ast.Div):return a/b
            if isinstance(node.op,ast.Pow) and b.denominator==1 and abs(b.numerator)<=8:
                return a**b.numerator
        raise ValueError("unsupported syntax: only rational arithmetic")
    return calc(ast.parse(expression,mode="eval").body)

def provenance_front(root):
    catalog=Path(root)/"analysis/2026-11-07_natural_constants_derivation_catalog.md"
    text=catalog.read_text(encoding="utf-8") if catalog.exists() else ""
    formulas={
        "alpha_A":"137+1/28+4/14045",
        "alpha_B":"137+880/24445",
        "alpha_C":"137+40/1111",
        "weak_W33":"3/13+1/2200",
        "weak_lowdenominator_adversary":"197/852"}
    entries=[]
    for name,expr in formulas.items():
        r=safe_rational(expr)
        entries.append({"name":name,"expression":expr,"canonical_fraction":str(r),
                        "value":float(r),
                        "source_catalog_exact_text_seen":expr in "".join(text.split())})
    assert safe_rational("137+1/28+4/14045")==safe_rational("(137*28*14045 + 14045 + 112)/(28*14045)")
    assert safe_rational("3/13+1/2200")!=safe_rational("197/852")
    # Known CODATA22 alpha reference: data already used to choose candidate -> NOT prospective.
    alpha=137.035999177; alpha_sigma=.000000021
    for row in entries:
        if row["name"].startswith("alpha_"):
            row["residual_CODATA22_sigmas"]=(row["value"]-alpha)/alpha_sigma
    return {"status":"CANONICAL_EXACT_RATIONAL_COMPARISONS_WITH_PROVENANCE_GAPS",
            "repository_catalog_present":bool(text),"source_catalog":str(catalog) if text else None,
            "aliases_are_equivalent":True,"canonicalized_candidates":entries,
            "parser_limit":"Integer rational arithmetic only; no TeX, RG scheme, symbolic group actions or archived source proofs are normalized.",
            "caveat":"Found in catalog means mentioned, not derived; retrospectively closest formula gets no prospective evidence."}

def prospective_front(clock):
    return {"id":"FORTYPOINTS-NULL27-BUTSON-001",
            "status":"PREREGISTERED_SYNTHETIC_TARGET_NO_LAB_COUNTS",
            "physical_precondition":"Calibrated 27-mode optical circuit implements adjacency A of W33 null-history graph and Laplacian L=8I-A",
            "predeclared_tick":"t_star=2*pi/9 using pre-measured global coupling, no adjustment after output counts",
            "probabilities_per_mode":"1/27 for every one of 27 input x 27 output channel probabilities",
            "rowwise_shell_probability_targets":{"origin":"1/27","null":"8/27","q=1":"6/27","q=2":"12/27"},
            "phase_gauge_invariants":clock["phase_plaquettes"],
            "sample_plan":"At least 5000 independently heralded detections per input (135000 total), with loss and crosstalk calibrated using separate reference runs",
            "decision_rule":"Full 27x27 multinomial likelihood vs predeclared uniform target with a simultaneous familywise-corrected 95% criterion; the 3 plaquette phases must each agree within preregistered interferometer uncertainty. Do not omit failing inputs.",
            "null_models":["measured uncoupled waveguide intensities","non-null edge rewiring at fixed degree","miscalibrated tick t+delta","loss/crosstalk and detector bias","ordinary quantum Clifford optical network"],
            "identifiability":"Ordinary quantum mechanics predicts the same result for the specified circuit. A successful experiment tests engineering and the finite model, NOT the existence of a new force or TOE."}

def execute(root):
    clock,A,U=null_clock()
    return {"schema":"w33.20261108.forty_points.fivefronts.v1",
            "source_paper":"papers/forty_points/main.pdf and full main.tex inputs",
            "clock_extra":clock,"front1_gauge":gauge_front(A),
            "front2_flavor":flavor_front(),
            "front3_scale":transmutation_front(),
            "front4_provenance":provenance_front(root),
            "front5_pre_registration":prospective_front(clock),
            "scope":"Five independent mathematical/conditional fronts. No new measured coupling, physical scale or complete E6 Standard Model is established."}
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",type=Path,default=Path("."))
    ap.add_argument("--out",type=Path,default=Path("data/w33_20261108_forty_points_fivefronts.json"))
    args=ap.parse_args()
    obj=execute(args.root)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":"PASS","output":str(args.out),"flat":obj["clock_extra"]["numeric_flatness_residual"],
                      "H1":obj["front1_gauge"]["cohomology_H1_dimension"],
                      "CP":obj["front2_flavor"]["effective_CP_weak_basis_invariant_exact"]}))
if __name__=="__main__":
    main()
