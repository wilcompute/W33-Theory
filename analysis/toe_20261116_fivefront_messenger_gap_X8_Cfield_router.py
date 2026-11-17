"""Five-front exact controls: messenger paths, KK modular BF gap, X8 form degrees,
flat C-field character sectors, and physically clocked active time-bin router.

Every result is a theorem or an explicitly conditional toy-model computation.
No 11D gauge-fixed unequal-flux eigenoperator, physical C-field action, proton
lifetime or laboratory photonics are claimed.
"""
from __future__ import annotations
import json,math,sys
from pathlib import Path
from fractions import Fraction
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from toe_20261116_IIB_circle_Gysin_linking import reduce_pair
from toe_20261116_fivefront_exact_negative_controls import lattice_modes
from toe_20261116_X8_Bianchi_metricjet_quadratic import verify as verify_x8

OUT=ROOT/"data"/"toe_20261116_fivefront_messenger_gap_Cfield_switch.json"

def messenger_walk_filter():
    m,mu,yu,yd=sp.symbols("m mu yu yd",nonzero=True)
    rows=[]
    for n in range(2,7):
        M=sp.diag(*([m]*n))
        for i in range(n-1):M[i,i+1]=M[i+1,i]=mu
        inv=sp.factor(M.inv()[0,n-1])
        det=sp.factor(M.det())
        assert sp.simplify(inv-(-mu)**(n-1)/det)==0
        coeff=sp.factor(-yu*yd*inv)
        leading=sp.expand(sp.series(coeff,mu,0,n+1).removeO()).coeff(mu,n-1)
        assert sp.simplify(leading-(-1)**n*yu*yd/m**n)==0
        rows.append({"messenger_pairs":n,"endpoint_operator_coefficient":str(coeff),
                     "determinant":str(det),"first_mixing_power":n-1,
                     "leading_coefficient":str(leading)})
    # Source MSSM charges in units of 3(B-L), and matter parity.
    q={"Q":1,"L":-3,"uc":-1,"dc":-1,"ec":3}
    dangerous={"QQQL":["Q","Q","Q","L"],
               "ucucdcec":["uc","uc","dc","ec"]}
    for fields in dangerous.values():
        assert sum(q[z] for z in fields)==0
        assert math.prod((-1)**q[z] for z in fields)==1
    return {
      "status":"PASS_E6_MESSENGER_CHAIN_SCHUR_AND_MATTER_PARITY_NO_GO",
      "schur_formula":"W_eff=-Ju*M^(-1)*Jd, with M=m*I+mu*adjacency(path_n), Ju on first and Jd on last messenger",
      "exact_endpoint_formula":"-(yu*yd)*(-mu)^(n-1)/det(M)",
      "leading_order":"(-1)^n*yu*yd*mu^(n-1)/m^n for |mu/m| sufficiently small",
      "paths":rows,
      "BminusL_and_Rparity_no_go":"QQQL and uc uc dc ec have B-L=0, and four odd matter superfields have even Z2 matter parity; neither a subgroup of U(1)_(B-L) nor ordinary matter parity can forbid these operators",
      "interpretation":"Longer heavy-messenger mixing paths suppress a particular D5 exchange amplitude algebraically; this is a CONDITIONAL texture, not an E6-consistent full symmetry or a complete proton-decay prediction."}

def delta(lamb):
    return math.sqrt(4+16*lamb)-lamb-2
def kk_two_mode_gap():
    # lambda_+-=3pi/y, y in (4/pi,pi), so 3<lambda<3*pi^2/4.
    low=3.
    high=3*math.pi**2/4
    dlow=delta(low); dhigh=delta(high)
    dmin=min(dlow,dhigh)
    assert dhigh<dlow and dmin>1.6
    opt=3.75
    assert low<opt<high
    maxd=delta(opt)
    assert abs(maxd-2.25)<1e-12
    for y in (4/math.pi+1e-4,1.4,2.,2.5,3.0,math.pi-1e-4):
        assert lattice_modes(0.2,y)==[(-1,0),(1,0)]
        l=3*math.pi/y
        assert delta(l)>dmin-1e-10
    return {
      "status":"PASS_EXACT_TWO_MODE_BF_STRIP_UNIFORM_GAP",
      "strip":"|Re tau| <=1/2, 4/pi < Im tau < pi",
      "two_real_unstable_modes":[[-1,0],[1,0]],
      "lambda_lower_open":low,"lambda_upper_open":high,
      "BF_deficit_infimum":dmin,
      "BF_deficit_supremum":maxd,
      "analytic_infimum":"sqrt(4+12*pi^2)-3*pi^2/4-2",
      "analytic_supremum":"9/4 attained when lambda=15/4 (y=4*pi/5)",
      "physical_operator_requirement":"If entire 11D physical fluctuation Hessian converges to equal-flux operator within norm strictly below this strip's gap, at least 2 real unstable modes persist; the norm is not calculated.",
      "translation_conservation":"Flux field-strength and square/flat torus geometry are torus-translation invariant; a translation-covariant physical linearized operator is block diagonal in torus momenta. Anti-linear reality pairs k and -k.",
      "limitation":"Equal-flux classical KK branch only; mode count changes across shape walls, and unequal-flux gauge constraints still unconstructed."}

def x8_C3_bidegree():
    jet=verify_x8()
    nonzero=jet["second_variation_coefficient_by_8form_mask"]
    result=[]
    for bitstr,value in nonzero.items():
        bits=[i for i in range(11) if (int(bitstr)>>i)&1]
        external=len([i for i in bits if i<5])
        internal=len([i for i in bits if i>=5])
        assert external+internal==8
        result.append({"bitmask":int(bitstr),"coeff":value,"external_degree":external,
                       "internal_degree":internal})
        assert internal>3
    assert result==[{"bitmask":495,"coeff":"-216","external_degree":4,"internal_degree":4}]
    # Background G4 is wholly internal; locally choose C3_bg wholly
    # internal. Then every term of bidegree (4,4) annihilates any
    # internal 3form by internal dimension 6.
    for mask in nonzero:
        for a in range(5,11):
            for b in range(a+1,11):
                for c in range(b+1,11):
                    assert int(mask) & ((1<<a)|(1<<b)|(1<<c))
    return {
      "status":"PASS_BIANCHI_X8_SAMPLE_WEDGES_TO_ZERO_WITH_INTERNAL_C3",
      "X8_t_squared_form":result,
      "background_C3_local_gauge":"Locally pure-internal C3_bg (background G4 has no external legs)",
      "sample_quadratic_C3bg_wedge_X8":"ZERO for every internal 3form in six internal dimensions because (4 internal)+(3 internal)>6",
      "critical_caveat":"This is a selection rule for the SPECIFIC Bianchi-valid example, not a theorem that the entire quadratic X8 variation vanishes after contraction with a physical background C3. X8 terms with >=5 external and <=3 internal legs could contribute; global C-field is a differential cocycle."}

def flat_Cfield_topology():
    # Flat degree-4 differential characters are H^3(M;R/Z).
    # For closed orientable Y5, H3(Y)=H^2(Y)=Z+Z_g by PD,
    # so H^3(Y;R/Z)=Hom(H3(Y),R/Z)=(R/Z) x Z_g.
    examples=[]
    for p,q in ((7,6),(6,6),(12,18),(0,8)):
        z=reduce_pair(p,q);g=z["gcd"]
        examples.append({"Euler_flux":[p,q],"torsion_order":g,
           "flat_degree4_differential_character":"U(1) x Z_"+str(g) if g>1 else "U(1)",
           "spin_structures":2 if g%2==0 else 1})
    # On S2xS2xT2: b3=4, no torsion in H3/H4, p1=0.
    return {"status":"PASS_TOPOLOGICAL_FLAT_CFIELD_SECTORS_IN_6D_VS_IIB_Y5",
       "IIB_Y5":{"H3_homology":"Z + Z_g by Poincare duality to H^2(Y,Z)",
          "flat_differential_4_characters":"H^3(Y;R/Z) = Hom(H_3(Y),R/Z) = U(1) x Z_g",
          "integral_half_shift":"lambda=p1(TY)/2=0, because TY stable pullback of T(S2xS2) and p1(base)=0",
          "winding_character_difference":"Abstract flat differential degree-4 characters (3-gerbes) on Y are NOT identical to flat U(1) line-bundle characters Hom(pi1,U1), even though both have Z_g components; IIB physical RR potentials are C0, C2 and C4, not an independent C3 field.",
          "examples":examples},
       "M6_product":{"manifold":"S2 x S2 x T2","H3_homology":"Z^4",
          "flat_differential_4_characters":"H^3(M6;R/Z)=(U1)^4, no torsion",
          "integral_half_shift":"lambda=p1(TM6)/2=0"},
       "large_scope_warning":"Differential character flat moduli of isolated spaces are topological, not the physical quantized Page-charge group. Actual M/IIB duality relates higher-dimensional backgrounds with nontrivial flux and couplings; this is NOT a charge-duality derivation."}

def active_router_budget():
    # Three temporally separated modes at slot 0,1,2 routed to
    # simultaneous three spatial rails at slot 4.
    # With group index n_g and bin interval Delta, delays are
    # (4-t)*c*Delta/n_g and require active time-dependent routing.
    c=299792458.0
    delta_t=1e-9
    group_index=1.47
    delays=[(4-t)*c*delta_t/group_index for t in (0,1,2)]
    assert delays[0]>delays[1]>delays[2]
    def gate_error(sigma_ps,guard_ps=100.):
        # Gaussian time jitter, centered gates of width Delta-2guard.
        sigma=sigma_ps*1e-12
        gate_half=delta_t/2-guard_ps*1e-12
        return math.erfc(gate_half/(math.sqrt(2)*sigma))
    assert gate_error(30)<1e-30 and gate_error(300)>.1
    # Illustrative each-arm two switches + optical coupling + delay:
    scenarios=[]
    for switch,pdelay,couple in ((.99,.995,.99),(.97,.99,.99),(.95,.98,.98)):
        f=switch**2*pdelay*couple
        scenarios.append({"per_switch":switch,"delay_transmission":pdelay,
                          "coupling":couple,"end_to_end_temporal_router":f,
                          "above_previous_91p96pct_benchmark":f>.9196})
    assert scenarios[0]["above_previous_91p96pct_benchmark"]
    assert not scenarios[-1]["above_previous_91p96pct_benchmark"]
    return {"status":"PASS_THREE_TIMEBIN_ACTIVE_ROUTING_AND_SWITCH_BUDGET",
      "time_bin_spacing_ns":1.,"chosen_common_output_slot":4,
      "group_index":group_index,
      "fiber_delays_m":delays,
      "minimum_switch_timing_slots":"Distinct routing operation must switch on 1 ns-separated time bins; insertion losses and spectral overlap are additional",
      "misroute_probability_gaussian_jitter_sigma30ps":gate_error(30),
      "misroute_probability_gaussian_jitter_sigma300ps":gate_error(300),
      "gate_guard_ps":100.,
      "illustrative_two_switch_loss_cases":scenarios,
      "measured_hardware":False,
      "limitations":"Ideal coherent switches and independent, unbiased detector loss; realistic insertion losses, mode matching, pulse shape, PMD, feedforward delay and randomized-basis implementation must be calibrated."}

def verify():
    parts=[messenger_walk_filter(),kk_two_mode_gap(),x8_C3_bidegree(),
           flat_Cfield_topology(),active_router_budget()]
    assert all(x["status"].startswith("PASS") for x in parts)
    return {"status":"PASS_FIVEFRONT_WILSONIAN_KK_X8_CFIELD_ROUTER_STRESS",
      "E6_messenger_and_parity":parts[0],"KK_uniform_gap":parts[1],
      "X8_local_bidegree":parts[2],"differential_Cfield_topology":parts[3],
      "optical_active_switch":parts[4]}
if __name__=="__main__":
    z=verify();OUT.parent.mkdir(exist_ok=True,parents=True)
    OUT.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(z["status"])
    for k,v in z.items():
        if isinstance(v,dict):print(k,v["status"])
