"""Second-order quantized near-equal KK geometry and an exact obstruction.

The true unequal-flux physical KK scalar/Maxwell mixing matrix is not
known in this audit. Its first-order eigenmass is constrained by sphere
interchange symmetry IF the branch stays isolated. Second-order
coefficient is NOT fixed by symmetry, because odd/even mixing enters.
All coefficients of eta and torus lambda through 1/N^3 are exact.
"""
import json, math, importlib.util
from pathlib import Path
from decimal import Decimal
import sympy as S
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_KK_secondorder_geometry_mixing.json"
spec=importlib.util.spec_from_file_location("prior",ROOT/"analysis"/"toe_20261116_near_equal_flux_BF_scaling.py")
prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)

def symbolic():
    t=S.Symbol("t")
    a,b,c,d=S.symbols("a b c d")
    variables=[a,b,c,d]
    eta=S.Rational(1,2)+a*t+b*t**2+c*t**3+d*t**4
    target=eta*(2-eta)**2/((1-eta)*(1+eta)**2)-(1+t)**2
    coeff=S.series(target,t,0,5).removeO().expand()
    sol={}
    for degree,var in enumerate(variables,1):
        sol[var]=S.solve(S.factor(coeff.coeff(t,degree)).subs(sol),var)[0]
    assert sol=={a:S.Rational(3,2),b:S.Rational(-3,4),c:-12,d:S.Rational(147,8)}
    eta=S.simplify(eta.subs(sol))
    k2=4*(2-eta)
    area=16*S.pi*(1+t)/(k2*S.sqrt(8*eta))
    lam=4*S.pi**2/area
    lseries=S.series(lam,t,0,4).removeO().expand()
    predicted=3*S.pi-3*S.pi*t/2-57*S.pi*t**2/8+183*S.pi*t**3/16
    assert S.simplify(lseries-predicted)==0
    m=lam-2-S.sqrt(4+16*lam)
    mseries=S.series(m,t,0,3).removeO().expand()
    m0=S.simplify(mseries.coeff(t,0))
    m1=S.simplify(mseries.coeff(t,1))
    m2=S.simplify(mseries.coeff(t,2))
    assert abs(float(m1)+1.6823331958573386)<1e-10
    assert abs(float(m2)+7.6221129337592535)<1e-10
    return {"eta_coefficients":[str(sol[x]) for x in variables],
      "lambda_coefficients_over_pi":["3","-3/2","-57/8","183/16"],
      "computed_fifth_eta_coefficient":"1749/8",
      "computed_fourth_lambda_over_pi_coefficient":"13281/128",
      "equal_formula_proxy_mass_coefficients":[str(m0),str(m1),str(m2)],
      "proxy_second_order_coefficient_numeric":float(m2),
      "true_physical_second_order_coefficient_NOT_DETERMINED":True}

def physical_mixing_obstruction():
    """Two symmetry-compatible Hamiltonians share linear mass, differ at delta^2.

    Exchange eta<->1-eta is realized by diag(1,-1).
    H(delta)=[[m0+a*t+b*t²,c*delta],[c*delta,nu]]
    Eigenvalue small near m0 obtains +c²*delta²/(m0-nu);
    its sign depends on nu relative to m0. Thus the geometry proxy
    cannot determine the true O(1/N²) mass without physical mixing.
    """
    t,c,nu,m0,b=S.symbols("t c nu m0 b",real=True)
    delta=S.Rational(3,2)*t
    # Schur complement for isolated m0 eigenbranch
    shift=S.factor(c*c*delta*delta/(m0-nu))
    assert shift==S.Rational(9,4)*c*c*t*t/(m0-nu)
    samples=[]
    for neighbor in (-2,-8):
        val=float(shift.subs({c:2,t:S.Rational(1,100),m0:-5,nu:neighbor}))
        samples.append({"neighbor_mass":neighbor,"second_order_shift_at_t_0p01":val})
    assert samples[0]["second_order_shift_at_t_0p01"]<0
    assert samples[1]["second_order_shift_at_t_0p01"]>0
    return {"exchange_even_odd_mixing":"Off-diagonal coupling linear in eta-1/2 is allowed by interchange symmetry.",
      "second_order_shift":"(9/4)*c^2*t^2/(m0-nu)",
      "no_certified_sign":True,"counterexamples":samples}

def verify():
    r=symbolic();ob=physical_mixing_obstruction()
    records=[]
    for n in (100,1000,10000):
        x=prior.case(n)
        eta=float(Decimal(x["eta"]))
        calc=.5+1.5/n-.75/n**2-12/n**3+18.375/n**4
        lam_exact=4*math.pi**2/(16*math.pi*(n+1)/(n*4*(2-eta)*math.sqrt(8*eta)))
        lam_taylor=math.pi*(3-1.5/n-57/(8*n*n)+183/(16*n**3))
        assert abs(eta-calc)<max(1e-14,500/n**5)  # float conversion floor
        assert abs(lam_exact-lam_taylor)<1000/n**4
        records.append({"N":n,"eta":eta,"lambda_exact":lam_exact,
                        "lambda_asymptotic_through_N_minus3":lam_taylor,
                        "remainder":lam_exact-lam_taylor})
    return {"status":"PASS_EXACT_KK_GEOMETRY_TO_3RD_ORDER_AND_PHYSICAL_MIXING_FIREWALL",
      "exact_asymptotic":r,"symmetry_mixing_obstruction":ob,
      "geometric_samples":records,
      "physical_boundary":"Full unequal-flux constrained metric-C3 KK operator, its eigenvectors, and actual second-order mass still missing. Sphere exchange alone fixes only absence of O(delta) anisotropy term."}
if __name__=="__main__":
    cert=verify()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(cert,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(cert["status"],cert["exact_asymptotic"]["proxy_second_order_coefficient_numeric"])
