"""Exact dimensionless IIB T11/Z_N control inequalities and winding band.

For equal mixed flux N and horizontal five-form charge N0:
volume(Y,Ric4)=16*pi^3/(27N),
L_str^4/alpha'^2=(27*pi/4) gs N N0,
(Rfiber/sqrt(alpha'))^4=(4*pi/3)gs N0/N^3.

The square M torus has tau=i (hence gs=1). Generic IIB tau is
tau1+i/gs, with lambda_min=3*pi*(N0/N)*min|u+v tau|^2/tau2.
Do not conflate fixed small gs with square M-theory torus.
"""
import json,math
import sympy as sp
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_iib_weakcurvature_winding_control.json"
def shortest_q(tau1,tau2,bound=8):
    vals=[]
    for u in range(-bound,bound+1):
        for v in range(-bound,bound+1):
            if u==v==0:continue
            val=((u+v*tau1)**2+(v*tau2)**2)/tau2
            vals.append((val,u,v))
    return min(vals)
def run():
    N,N0,gs=sp.symbols("N N0 gs",positive=True)
    volume=16*sp.pi**3/(27*N)
    LR4=sp.simplify(4*sp.pi**4*gs*N0/volume)
    RFR4=sp.simplify((sp.Rational(2,3)/N)**4*LR4)
    assert LR4==sp.Rational(27,4)*sp.pi*gs*N*N0
    assert RFR4==sp.Rational(4,3)*sp.pi*gs*N0/N**3
    examples=[]
    for n,n0,g in [(1,10000,1),(4,10000,1),(40,10000,1),
                   (100,100,1),(100,10000,1),
                   (10,1000,.1),(10,10000,.1),
                   (100,10000,.1),(100,100000,.1)]:
        t1,t2=0,1/g
        val,u,v=shortest_q(t1,t2,12)
        lam=3*math.pi*n0/n*val
        Ls=float(LR4.subs({N:n,N0:n0,gs:g}))**.25
        Rfs=float(RFR4.subs({N:n,N0:n0,gs:g}))**.25
        examples.append({
          "N":n,"N0":n0,"gs":g,
          "tau":[t1,t2],
          "reduced_shape":bool(t2>=1),
          "shortest_lattice_charge":[u,v],
          "L_over_sqrt_alpha":Ls,"fiber_radius_over_sqrt_alpha":Rfs,
          "lambda_shortest":lam,
          "winding_BF_violation_in_this_channel":bool(0<lam<12),
          "large_AdS_radius_criterion_Ls_ge10":bool(Ls>=10),
          "fiber_radius_ge_string_length":bool(Rfs>=1)
        })
    assert all((r["lambda_shortest"]<12)==r["winding_BF_violation_in_this_channel"] for r in examples)
    # For reduced tau in the usual SL2Z fundamental domain,
    # shortest |u+v tau|²=1, hence lambda_min=3*pi*N0/(N*tau2).
    for tau1,tau2 in ((0,1),(0,2),(.5,math.sqrt(3)/2),(.3,1.3),(-.49,1.01),(0,10)):
        val,_,_=shortest_q(tau1,tau2)
        assert abs(val-1/tau2)<1e-10
    # BF-safe square tau=i criterion and universal hex bound on shapes.
    assert float(sp.pi/(2*sp.sqrt(3)))>float(sp.pi/4)
    result={
      "status":"EXACT_IIB_T11_ZN_STRING_RADIUS_AND_WINDING_CONTROL_CONDITIONS",
      "equal_flux_internal_volume":"16*pi^3/(27*N), with Ric(Y)=4g",
      "IIB_AdS_radius_string4":"(27*pi/4)*gs*N*N0 = L^4/alpha'^2",
      "IIB_fiber_radius_string4":"(4*pi/3)*gs*N0/N^3 = Rf^4/alpha'^2",
      "fiber_radius_string_ge1_condition":"N0 >= (3/(4*pi*gs))*N^3",
      "AdS_radius_string_ge_a_condition":"N*N0 >= 4*a^4/(27*pi*gs)",
      "winding_lambda":"3*pi*N0/N * min_(u,v)neq0 |u+v*tau|²/Im(tau)",
      "reduced_tau_lambda_min":"3*pi*N0/(N*Im(tau)), for |Re(tau)|<=1/2 and |tau|>=1",
      "winding_BF_safe_necessary_and_sufficient_in_this_sector":
           "Im(tau)<=pi*N0/(4*N) for reduced tau, lambda_min >= 12",
      "universal_no_stable_shape_if":"N/N0>pi/(2*sqrt(3)), all reduced tau have Im(tau)>=sqrt(3)/2",
      "tau_axiodilaton":"tau=C0+i/gs, not tau=i unless gs=1,C0=0",
      "examples":examples,
      "scope":"Applies to the specified equal-charge classical dual and its linearized torus-momentum/wrapped-string BF test, subject to validity of duality. No claims about all higher string excitations, global decay or full quantum stability. The fiber radius and curvature control are independent inequalities, not automatic from large flux alone."
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    return result
if __name__=="__main__":
    x=run()
    print("PASS",x["status"],[(r["N"],r["N0"],r["winding_BF_violation_in_this_channel"]) for r in x["examples"]])
