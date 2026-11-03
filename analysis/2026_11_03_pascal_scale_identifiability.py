#!/usr/bin/env python3
"""Scale-identifiability controls for the exact Pascal electrical RG.

Separates a relevant power-law geometric conductance flow from dimensional
transmutation in a declared quantum gauge theory. Proves integer-factor
equal-clock product of the standard Pascal diffusion has ds != 4.
"""
from __future__ import annotations
from pathlib import Path
from fractions import Fraction
import math,json
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"2026_11_03_pascal_scale_identifiability.json"
x=s.symbols("x",positive=True)
F=s.factor(x*(9*x+7)/(15*x*x+31*x+15))
assert s.limit(F/x,x,0)==s.Rational(7,15)
assert s.limit((F-s.Rational(7,15)*x)/x**2,x,0)==-s.Rational(82,225)
assert s.simplify(F-x)!=0
assert s.solve(s.together(F-x),x)==[] # positive x assumed
# The unconstrained equation factors as -x(15x²+22x+8)/positive;
# there is no strictly positive fixed point, only zero.
assert s.simplify((F-x)+x*(15*x*x+22*x+8)/(15*x*x+31*x+15))==0
limit_r=s.Rational(15,7)
limit_time=6*limit_r
# For m independent copies with common clock, d_s=2m ln 6 / ln(90/7).
# d_s=4 => 6**m = (90/7)**2 = 8100/49: impossible for integer m.
rhs=limit_time**2
assert rhs.denominator==49
assert rhs.numerator==8100
assert all(6**m!=rhs for m in range(1,16))
for N in (1,2,3,4,5):
    ds=2*N*math.log(6)/math.log(float(limit_time))
    assert ds!=4
# One-loop RG beta0 for SU3,Nf3 is an external field theory.
b0=9
sample=[]
for g in (.3,.5,.7,1.0,2.0):
    ratio=math.exp(-8*math.pi**2/(b0*g*g))
    sample.append({"uv_g":g,"Lambda_over_mu_one_loop":ratio,
                   "loop_expansion_g2_over_16pi2":g*g/(16*math.pi**2)})
# Find couplings chosen AFTER the fact to reproduce Pascal ratios.
targets={}
for target in (limit_r,limit_time):
    t=float(target)
    g2=8*math.pi**2/(b0*math.log(t))
    assert abs(math.exp(8*math.pi**2/(b0*g2))-t)<1e-11
    targets[str(target)]={"g2_required":g2,"alpha_g2_over_4pi":g2/(4*math.pi),
                          "scheme":"one-loop SU3 with Nf3, benchmark only"}
# Graph Hamiltonian H=J L with J in hbar/time units:
# normalized transfer probabilities depend only on theta=J*time/hbar.
ans={
 "status":"PASS_SCALE_NONIDENTIFIABILITY_AND_PRODUCT_SPECTRAL_DIMENSION_NOGO",
 "exact_conductance_fixed_point":"only c=0 for c>=0; numerator F(c)-c=-c(15c²+22c+8)/(15c²+31c+15)",
 "linearization_at_zero":"F'(0)=7/15",
 "second_order_term":"F(c)=7c/15 - 82 c²/225+O(c³)",
 "relative_conductance_anomalous_exponent":math.log(7/15)/math.log(3),
 "negative_control":"This is a hyperbolic power-law contraction, not a marginal logarithmic beta function; the circuit alone does not generate an exponential transmutation scale.",
 "exact_mass_time_ratio":str(limit_time),
 "equal_clock_product_no_go":{
     "theorem":"No positive integer tensor power of identical six-copy Pascal limiting diffusions has exact spectral dimension 4 under the standard common-clock scaling.",
     "proof":"m*2log(6)/log(90/7)=4 implies 6^m=(90/7)^2=8100/49, contradicting integrality of 6^m.",
     "m_tests":{str(m):2*m*math.log(6)/math.log(float(limit_time)) for m in range(1,7)},
     "scope":"Assumes standard time rescaling 90/7 and independent equal-clock product; variable q, anisotropy, interactions, dynamical fibers can evade the restricted statement."
 },
 "physical_scale_gauge":{
     "continuous_time_photonic_model":"H=J*L, U(t)=exp(-i J t L/hbar). Dimensionless normalized data fix only tau=Jt/hbar; J and t cannot be separately identified without external calibration.",
     "electrical_model":"R_n scales as 1/g0 for common edge conductance g0; its ratio 15/7 is invariant and cannot fix g0. Physical length ℓ0 is likewise absent.",
     "parameter_underdetermination":"Multiplying all edge conductances by a positive factor leaves the exact resistance ratios unchanged; multiplying J by a and t by 1/a preserves all quantum-walk probabilities."
 },
 "one_loop_su3_benchmark":{
      "external_beta_coefficient_b0":b0,
      "one_loop_formula":"Lambda/mu=exp(-8*pi²/(b0*g_UV²)); g_UV and mu are externally supplied.",
      "coupling_sensitivity":sample,
      "posthoc_couplings_for_pascal_ratios":targets,
      "warning":"Choosing g_UV to match a graph ratio is parameter fitting and does not derive a prediction. The 15/7 choice requires alpha close to 1, outside a reliable perturbative regime."
 },
 "literature_scope":"Ordinary one-loop asymptotic freedom and dimensional transmutation are established QFT; the exact graph RG and product no-go are restricted mathematical checks, not a complete UV quantum theory."
}
OUT.parent.mkdir(exist_ok=True,parents=True)
OUT.write_text(json.dumps(ans,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print("PASS dimensionless RG and integer-product ds=4 no-go",rhs,"g2 targets",targets,flush=True)
