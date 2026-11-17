"""Five independent exact controls for the W33 TOE research fronts, 2026-11-16.

Results are mathematical/conditional; no fully corrected 11D spectrum,
physical Page-charge group or photonic experiment is constructed.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction
from itertools import product
from math import gcd, pi, sqrt
from pathlib import Path
import json, sys
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261116_E6_full_cubic_SM_stabilizer import cubic_monomials, hypercharge_integer_weights
import toe_20261116_11D_X8_nilpotent_variation as oldx8
from toe_20261116_IIB_circle_Gysin_linking import reduce_pair
OUT=ROOT/"data"/"toe_20261116_fivefront_chambers_X8_symmetry_spin_router.json"

def e6_discrete_filter_no_go():
    """Commuting E6-family phase and hypercharge subgroup do not filter triplets."""
    weights=hypercharge_integer_weights()
    monomials=cubic_monomials()
    charge_totals=Counter(sum(weights[i] for i in tri) for tri in monomials)
    assert charge_totals=={0:len(monomials)}
    t=sp.symbols("t")
    F=(t*t-4)/5
    assert [F.subs(t,w) for w in (-3,-2,2)]==[1,0,0]
    m,mu,yu,yd=sp.symbols("m mu yu yd",nonzero=True)
    mass=sp.Matrix([[m,mu],[mu,m]])
    up=sp.Matrix([[0,yu]])
    down=sp.Matrix([yd,0])
    coefficient=sp.factor(-(up*mass.inv()*down)[0])
    assert sp.simplify(coefficient-mu*yu*yd/(m*m-mu*mu))==0
    assert sp.simplify(coefficient.subs(mu,0))==0
    assert sp.simplify(sp.diff(coefficient,mu).subs(mu,0)-yu*yd/m**2)==0
    return {
      "status":"PASS_E6_HYPERCHARGE_ONLY_DISCRETE_SYMMETRY_NO_GO",
      "cubic_monomial_count":len(monomials),
      "all_E6_cubic_monomials_have_total_hypercharge_zero":True,
      "filter_values_at_minus3_minus2_plus2":["1","0","0"],
      "group_theory":"By Schur's lemma, a discrete internal transformation commuting with irreducible E6 on a single 27 is proportional to identity. Residual discrete hypercharge also cannot forbid a subset of E6-invariant cubic monomials, because each already has total Y charge zero.",
      "perturbative_Wilsonian_theorem":"A fixed N=1 supersymmetric holomorphic Wilsonian superpotential is perturbatively nonrenormalized; this does not predict the tuned coefficients, forbid additional UV operators, remove heavy gauge-boson channels or protect against vacuum shifts and SUSY-breaking effects.",
      "two_messenger_mixing_mass_matrix":"[[m,mu],[mu,m]]",
      "zero_up_source_on_first_pair_but_nonzero_on_second":"Ju=(0,yu), Jd=(yd,0)",
      "induced_B_violating_coefficient":str(coefficient),
      "leading_mixing_coefficient":"mu*yu*yd/m^2 + O(mu^3)",
      "important_caveat":"The mixing counterexample requires an additional unfiltered up-type heavy state. Mixing among strictly zero-source states alone cannot generate the operator."
    }

def lattice_modes(tau_re,tau_im,limit=12):
    assert tau_im>0
    # Bound based on lambda<limit: n²*y² <= limit*y/(3pi),
    # and |m+n*x|<sqrt(limit*y/(3pi)).
    nmax=int(sqrt(limit/(3*pi*tau_im)))+1
    mmax=int(sqrt(limit*tau_im/(3*pi))+abs(tau_re)*nmax)+2
    modes=[]
    for n in range(-nmax,nmax+1):
        for m in range(-mmax,mmax+1):
            if m==0 and n==0:continue
            lam=3*pi*((m+n*tau_re)**2/tau_im+n*n*tau_im)
            if lam<limit-1e-10:modes.append((m,n))
    return sorted(modes)

def kk_modular_chambers():
    # Entire analytic strip is inside the modular fundamental domain:
    # x in [-1/2,1/2], y in (4/pi,pi).
    # For n!=0: lambda>=3pi*y>12.
    # For n=0 and |m|>=2: lambda>=12pi/y>12.
    # For n=0, |m|=1: lambda=3pi/y<12.
    for y in (1.30,1.4,2.,3.,3.13):
        for x in (-.5,-.21,0.,.17,.5):
            assert lattice_modes(x,y)==[(-1,0),(1,0)]
    square=lattice_modes(0.,1.)
    hexa=lattice_modes(.5,sqrt(3)/2)
    assert len(square)==4 and len(hexa)==6
    assert len(lattice_modes(0.,4.))==4 # n0, m=+-1,+-2
    return {
      "status":"PASS_MODULAR_BF_TWO_MODE_CHAMBER_THEOREM",
      "normalized_lambda":"3*pi*|m+n*tau|^2/Im(tau)",
      "BF_violating_iff":"0<lambda<12 for the proven equal-flux odd KK branch",
      "analytic_exact_two_mode_strip":{"x":"-1/2 <= Re(tau) <= 1/2",
        "y":"4/pi < Im(tau) < pi",
        "only_signed_wavevectors":[[-1,0],[1,0]],
        "proof":"n != 0 implies lambda>=3*pi*y>12; |m|>=2,n=0 implies lambda>=12*pi/y>12; m=+-1,n=0 has lambda=3*pi/y<12."},
      "square_tau_i_modes":[list(z) for z in square],
      "hexagonal_tau_1/2+i_sqrt3/2_modes":[list(z) for z in hexa],
      "false_conclusion_to_avoid":"Four BF modes is a square-torus statement, NOT a uniform lower bound over all torus shapes. An open modular strip has only two real unstable harmonics in this branch.",
      "spectrum_scope":"Classical equal-flux branch only; other sectors and flux-asymmetric physical mixing not counted."
    }

def add_forms(A,B,mult=1):
    out=dict(A)
    for w,v in B.items():out[w]=out.get(w,0)+mult*v
    return {w:v for w,v in out.items() if v}
def scale_form(A,k):
    return {w:k*v for w,v in A.items() if k*v}
def add_matrices(A,B,mult=1):
    return [[add_forms(A[i][j],B[i][j],mult) for j in range(11)] for i in range(11)]
def t4_polynomial(A):
    R2=oldx8.multiply(A,A)
    t2=oldx8.trace(R2)
    t4=oldx8.trace(oldx8.multiply(R2,R2))
    return add_forms(t4,oldx8.wedge(t2,t2),-Fraction(1,4))
def x8_quadratic_variation():
    R=oldx8.curvature()
    D=[[{} for _ in range(11)] for _ in range(11)]
    for a,b,u,v in [(0,1,2,3),(5,6,7,8)]:
        D[a][b]=oldx8.form(u,v)
        D[b][a]=scale_form(D[a][b],-1)
    assert all(not z for row in oldx8.multiply(R,R) for z in row)
    RD=oldx8.multiply(R,D)
    trRD=oldx8.trace(RD)
    RDRD=oldx8.trace(oldx8.multiply(oldx8.multiply(RD,R),D))
    coefficient=add_forms(scale_form(RDRD,2),oldx8.wedge(trRD,trRD),-1)
    assert coefficient
    xplus=t4_polynomial(add_matrices(R,D))
    xminus=t4_polynomial(add_matrices(R,D,-1))
    xr=t4_polynomial(R)
    xd=t4_polynomial(D)
    finite_diff=scale_form(add_forms(add_forms(add_forms(xplus,xminus),xr,-2),xd,-2),Fraction(1,2))
    assert coefficient==finite_diff,(coefficient,finite_diff)
    assert not xr
    return {
      "status":"PASS_X8_QUADRATIC_FORMULA_NONZERO_ALGEBRAIC_VARIATION",
      "R_wedge_R_matrix_zero":True,"X8_background_zero":True,
      "first_curvature_variation_X8_zero":True,
      "X8_polynomial_convention":"P(R)=tr(R^4)-(1/4)*(tr R^2)^2; overall physical normalization omitted",
      "t_squared_coefficient_exact_formula":"2 tr(R deltaR R deltaR) - [tr(R deltaR)] wedge [tr(R deltaR)]",
      "nonzero_example_coefficient_by_8form_mask":{str(k):str(v) for k,v in coefficient.items()},
      "independent_plus_minus_finite_polynomial_check_passed":True,
      "IMPORTANT":"Algebraic deltaR not required to be realizable Levi-Civita perturbation. Does not compute the physical second functional variation, full action, flux terms, or corrected BF masses."
    }

def iib_spin_topology():
    rows=[]
    for p,q in ((1,1),(2,2),(6,6),(7,6),(10,15),(0,4),(-6,9)):
        base=reduce_pair(p,q)
        g=base["gcd"]
        count=2 if g%2==0 else 1
        rows.append({"p":p,"q":q,"gcd":g,"spin_structures":count,
            "flat_U1_characters":g,
            "torsion_linking_generator":base["torsion_linking_H2_H4_unit"]})
    for p in range(-10,11):
        for q in range(-10,11):
            if p==q==0:continue
            g=gcd(p,q)
            count=2 if g%2==0 else 1
            assert count==len([k for k in range(g) if (2*k)%g==0])
    return {
      "status":"PASS_IIB_CIRCLE_SPIN_STRUCTURE_PARITY_AND_LINKING",
      "topological_fact":"TY is stably isomorphic to pi* T(S2xS2) plus trivial vertical line, so w2(TY)=0; every nontrivial Y(p,q) is spin.",
      "spin_structures":"Spin structures form a torsor over H^1(Y;Z2)=Hom(Z_g,Z2), so 1 structure for odd g and 2 for even g.",
      "flat_U1_local_systems":"Hom(pi1(Y),U(1)) has exactly g characters, distinct from number of spin structures.",
      "linking":"Tor H²(Y) paired perfectly with Tor H⁴(Y) with generator unit +/-1/g (mod 1).",
      "crucial_distinction":"Even g>2 has two spin structures, but that does not imply a globally descending Killing spinor; deck transformation phases and local Killing equations are separate.",
      "no_Page_charge_or_spectrum_claim":True,"examples":rows}

def photonic_active_routing():
    rails=3;times=8
    def index(r,t):return r*times+t
    permutation=list(range(rails*times))
    pairs=[(index(0,0),index(0,4)),(index(0,1),index(1,4)),(index(0,2),index(2,4))]
    for a,b in pairs:
        permutation[a],permutation[b]=permutation[b],permutation[a]
    assert len(set(permutation))==rails*times
    def shift(i):
        return index(i//times,(i%times+1)%times)
    a=index(0,0)
    lhs=permutation[shift(a)]
    rhs=shift(permutation[a])
    assert lhs!=rhs
    assert [permutation[index(0,t)] for t in range(3)]==[index(r,4) for r in range(3)]
    return {
      "status":"PASS_PASSIVE_TIME_TRANSLATION_INVARIANT_ROUTING_NO_GO",
      "desired_mapping":"|single_input_rail,time t=0,1,2> -> |distinct_output_rail r=0,1,2, common_time=4>",
      "constructed_lossless_24x24_permutation_unitary":True,
      "temporal_mode_and_spatial_mode_Hilbert_dimensions":[times,rails],
      "time_shift_commutes_with_stationary_U":False,
      "explicit_noncommutation_on_input_rail0_time0":{"U_then_shift":rhs,"shift_then_U":lhs},
      "theorem":"For a passive stationary shift-covariant network U*T=T*U, outputs from successive input time bins are time-translated copies, not different spatial rails at the same time. Exact coherent demultiplexing requires active time-dependence or equivalent nonstationary storage/control.",
      "scope":"The permutation is an abstract unitary routing schedule, NOT a tested fast optical switch or a realistic time-bin quantum memory. Active device losses and switching times require calibration."
    }

def verify():
    components=[e6_discrete_filter_no_go(),kk_modular_chambers(),
        x8_quadratic_variation(),iib_spin_topology(),photonic_active_routing()]
    assert all(x["status"].startswith("PASS") for x in components)
    return {"status":"PASS_TOE_FIVEFRONT_EXACT_NEGATIVE_CONTROLS",
        "e6_filter_symmetry":components[0],
        "KK_modular_chambers":components[1],
        "X8_second_variation":components[2],
        "IIB_spin_topology":components[3],
        "photon_active_router":components[4]}

if __name__=="__main__":
    z=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(z["status"])
    for k,v in z.items():
        if isinstance(v,dict):print(" ",k,v["status"])
