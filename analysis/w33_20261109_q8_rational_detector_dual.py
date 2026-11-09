#!/usr/bin/env python3
"""Rational dual feasibility certificate for the 8-setting W33 Q8 detector LP,
using a W chosen from the full trace-norm SDP. Every LP inequality is rational,
and a conservative allowance protects an algebraic A design bound.
This does NOT certify an actual experiment (qhat is the expected distribution).
"""
import json,math,sys
from fractions import Fraction as F
from pathlib import Path
import numpy as np
import cvxpy as cp
from scipy.optimize import linprog
from w33_20261109_q8_correlation_five import frames,hermitian_basis,frame_map,probabilities,tensor_direct,trace_norm
from w33_20261109_q8_tiles_ppt_exact import exact_tiles
from w33_20261109_q8_five_extensions import pyramid_state

DEN=10**12
def lo12(x):return F(math.floor(float(x)*DEN),DEN)
def hi12(x):return F(math.ceil(float(x)*DEN),DEN)
def near12(x):return F(round(float(x)*DEN),DEN)
def rational_duals(res, c, rowsub, rowseq, bounds):
    factor=10**10
    yu=[F(int(round(float(x)*factor)),factor) for x in res.ineqlin.marginals]
    ye=[F(int(round(float(x)*factor)),factor) for x in res.eqlin.marginals]
    yl=[F(max(0,int(round(float(x)*factor))),factor) for x in res.lower.marginals]
    yh=[F(min(0,int(round(float(x)*factor))),factor) for x in res.upper.marginals]
    assert all(x<=0 for x in yu+yh) and all(x>=0 for x in yl)
    residual=[]
    for j in range(19):
        e=sum((yu[i]*rowsub[i][j] for i in range(36)),F(0))
        e+=sum((ye[i]*rowseq[i][j] for i in range(2)),F(0))
        e+=yl[j]+yh[j]
        residual.append(c[j]-e)
    # Valid for ALL feasible x, including dual-variables with rounding residual.
    b=ye[0]
    for j,(l,u) in enumerate(bounds):
        b+=yl[j]*l+yh[j]*u
        b+=min(residual[j]*l,residual[j]*u)
    gap=float(res.fun-b)
    assert gap>-3e-7 and gap<5e-6,(gap,res.fun,float(b))
    return b,{"dual_ineq":[str(v) for v in yu],"dual_eq":[str(v) for v in ye],
              "dual_lower":[str(v) for v in yl],"dual_upper":[str(v) for v in yh],
              "stationarity_max_residual":float(max(abs(v) for v in residual)),
              "numeric_min_minus_exact_rational_certified_lower":gap}

def lp_certificate(Aint, Wint,Cnum,q,efflo,effhi,eps):
    objective=[F(sum(int(Aint[j,k])*int(Wint.flatten()[k]) for k in range(64)),DEN*Cnum)
               for j in range(72)]
    constant=-sum(objective,F(0))/9
    records=[];total=constant
    for b in range(8):
        rowsub=[]
        rowseq=[[F(0) for _ in range(19)] for _ in range(2)]
        for j in range(9):rowseq[0][j]=F(1)
        for j in range(9):rowseq[1][9+j]=F(1)
        rowseq[1][18]=F(-1)
        qlo=[max(F(0),lo12(q[b,j]-eps)) for j in range(9)]
        qhi=[min(F(1),hi12(q[b,j]+eps)) for j in range(9)]
        for j in range(9):
            R=[F(0)]*19;R[j]=-effhi[j];R[9+j]=1;rowsub.append(R)
            R=[F(0)]*19;R[j]=efflo[j];R[9+j]=-1;rowsub.append(R)
            R=[F(0)]*19;R[9+j]=1;R[18]=-qhi[j];rowsub.append(R)
            R=[F(0)]*19;R[9+j]=-1;R[18]=qlo[j];rowsub.append(R)
        bounds=[(F(0),F(1))]*9+[(F(0),max(effhi))]*9+[(min(efflo),max(effhi))]
        c=objective[b*9:(b+1)*9]+[F(0)]*10
        sol=linprog(np.array(list(map(float,c))),
                    A_ub=np.array([[float(x) for x in row] for row in rowsub]),
                    b_ub=np.zeros(36),
                    A_eq=np.array([[float(x) for x in row] for row in rowseq]),
                    b_eq=[1.,0.],
                    bounds=[(float(l),float(u)) for l,u in bounds],
                    method="highs")
        assert sol.success,sol.message
        bound,cert=rational_duals(sol,c,rowsub,rowseq,bounds)
        total+=bound
        records.append({"basis":b,"exact_LP_lower":str(bound),**cert})
    return total,records

def algebraic_A_guard(A):
    # Each projector is constructed from finite qutrit Clifford gates, and in
    # the chosen normalized Hermitian operator basis each coefficient belongs
    # to Z/18 or sqrt(3)*Z/18. Check this classification exhaustively at 4608 sites.
    candidates=[(m,0,m/18) for m in range(-12,13)]+[(0,n,n*math.sqrt(3)/18) for n in range(-12,13)]
    gaps=[]
    for x in A.flatten():
        m,n,v=min(candidates,key=lambda t:abs(float(x)-t[2]))
        gaps.append(abs(float(x)-v))
        assert abs(float(x)-v)<5e-13
    # Exact sqrt3 bracket and (conservative) coefficient bound.
    L=math.isqrt(3*10**24);Q=10**12
    assert L*L<3*Q*Q<(L+1)**2
    epsA=F(1,10**10) # 1e-10 > max coefficient 12/18 * interval width
    assert epsA>F(12,18*Q)+F(1,10**12)
    return epsA,{"distinct_Clifford_A_fields":"m/18 or n*sqrt(3)/18, |m|,|n|<=12",
                 "checked_entries":int(A.size),
                 "maximum_double_vs_field_residual":max(gaps),
                 "sqrt3_rational_enclosure":[str(F(L,Q)),str(F(L+1,Q))],
                 "adversarial_per_A_coefficient_bound":str(epsA),
                 "scope":"This interval allowance assumes the established exact Clifford field identities underlying the ideal matrix; it is not calibration of an actual optical instrument."}

def one_case(name,rho,A,E):
    eff=np.array([.63+.045*j for j in range(9)])
    low=eff*(1-.001);high=eff*(1+.001)
    p=np.array([probabilities(E[:,9*b:9*(b+1)],rho) for b in range(8)])
    q=p*eff[None,:];q/=q.sum(axis=1,keepdims=True)
    N=10000000;alpha=.05
    rad=math.sqrt(math.log(2*72/alpha)/(2*N))
    P=cp.Variable((8,9),nonneg=True)
    V=cp.Variable((8,9),nonneg=True)
    S=cp.Variable(8)
    lo=np.array([float(lo12(x)) for x in low])
    hi=np.array([float(hi12(x)) for x in high])
    qlo=np.array([[float(max(F(0),lo12(x-rad))) for x in row] for row in q])
    qhi=np.array([[float(min(F(1),hi12(x+rad))) for x in row] for row in q])
    cons=[cp.sum(P,axis=1)==1,cp.sum(V,axis=1)==S,
          S>=min(lo),S<=max(hi),
          V>=cp.multiply(P,lo[None,:]),V<=cp.multiply(P,hi[None,:]),
          V>=cp.multiply(cp.reshape(S,(8,1),order="C"),qlo),
          V<=cp.multiply(cp.reshape(S,(8,1),order="C"),qhi)]
    t=cp.reshape(A.T@(cp.reshape(P,(72,),order="C")-1/9),(8,8),order="C")
    opt=cp.Problem(cp.Minimize(cp.normNuc(t)),cons)
    value=opt.solve(solver="CLARABEL",tol_gap_abs=1e-9,tol_feas=1e-9,tol_gap_rel=1e-9,max_iter=400)
    assert opt.status=="optimal",opt.status
    u,s,vh=np.linalg.svd(t.value)
    W=u@vh
    wi=np.rint(W*10**6).astype(np.int64)
    gram=wi.T@wi
    maxrow=max(sum(abs(int(x)) for x in row) for row in gram)
    Cnum=math.isqrt(maxrow)+1
    assert Cnum*Cnum>maxrow # exact rational spectral norm <=1
    epsA,guard=algebraic_A_guard(A)
    Ai=np.rint(A*DEN).astype(np.int64)
    exact,duals=lp_certificate(Ai,wi,Cnum,q,
                              [lo12(x) for x in low],
                              [hi12(x) for x in high],rad)
    # For each of 8 bases sum_j p_bj=1 and each entry A error<=epsA:
    # |sum_j p_j <W, A_true_j-A_approx_j>|<=8 epsA ||W||_1.
    error_bound=8*epsA*F(sum(abs(int(x)) for x in wi.flatten()),Cnum)
    strict=exact-error_bound
    true=trace_norm(tensor_direct(rho,np.array(hermitian_basis())))
    assert float(strict)<=true+1e-7
    assert float(strict)>2/3
    print('DUAL_DIAG',name,'SDP',value,'rational',float(strict),'C',Cnum/1e6,'minSv',min(s),flush=True)
    assert abs(float(strict)-value)<.03
    return {"state":name,"numeric_SDP_minimum":float(value),
            "rational_Gram_max_row_numerator":maxrow,
            "rational_norm_guard_C":str(F(Cnum,10**6)),
            "rounded_W_integer_matrix":wi.tolist(),
            "operator_norm_proved_at_most_one_by_rational_Gershgorin":True,
            "exact_rational_LP_lower_in_model":str(exact),
            "all_coefficient_guard":guard,
            "exact_witness_error_budget":str(error_bound),
            "strict_rational_lower_after_frame_error":str(strict),
            "strict_decimal_lower":float(strict),
            "above_separability_limit":float(strict)>2/3,
            "true_trace_norm":true,
            "simulated_expected_probabilities_not_observed":True,
            "per_basis_accepted_samples_assumed":N,
            "confidence_synthetic_95pct_simultaneous_rad":rad,
            "lp_dual_certificates":duals,
            "limitations":"Exact rational inequality checks for the rounded model and an algebraic frame-error enclosure. The input expectations and efficiency intervals are synthetic; no real-detector calibration or empirical confidence claim."}

def main(path=None):
    E=frames()[1][0]
    A=frame_map(E,np.array(hermitian_basis()))
    tiles=np.array(exact_tiles()[0],dtype=float)
    pyr,_=pyramid_state()
    result={"status":"PASS_RATIONAL_8BASIS_DUAL_SCHMIDT_CERTIFICATES_WITH_SDP_SELECTED_W",
            "results":[one_case("Tiles",tiles,A,E),one_case("Pyramids",pyr,A,E)],
            "novelty":"Rational LP dual consistency check of a finite detector model, not a first-ever CCNR/PPT witness or fully audited physical experiment."}
    if path:Path(path).write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS rational-guarded selected-dual",json.dumps({x["state"]:x["strict_decimal_lower"] for x in result["results"]}))
    return result

if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else None)
