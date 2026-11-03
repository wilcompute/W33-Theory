#!/usr/bin/env python3
"""Exploratory codimension-two Pascal portal that can stabilize a finite
internal-mode energy gap against a refining 4D nearest-neighbor base.

Critical distinction:
- Formal: independent Bernoulli portals of probability c/L^2 homogenize a
  *quadratic form on fixed smooth test functions* and produce a finite mean
  internal graph Laplacian coefficient when link kinetic strength is L^2.
- NOT established: local causal dynamical realization of independent portals,
  operator norm/strong-resolvent convergence, quantum radiative stability, or
  an invariant physical scale without choosing the parent length R.
"""
from pathlib import Path
import math,json
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
rng=np.random.default_rng(20261103)
# Symplectic line-selector ratio at q=3: 40/130=4/13.
C=4/13
def expr(L,coords):
    x=coords*(2*np.pi/L)
    return 1+.3*np.cos(x[:,0])+.2*np.cos(x[:,1]+x[:,2])
def measure_one(L,c=C,nrep=350):
    sites=L**4
    p=c/L**2
    assert p<=1
    counts=rng.binomial(sites,p,size=nrep)
    integrated=counts/L**2
    theory_var=c*(1-c/L**2)/L**2
    # Independent Poissonized random positions with a fixed number of points.
    # Profiles evaluate smooth bulk observables, not singular localized modes.
    vals=[]
    for count in counts[:60]:
        sample=rng.integers(0,L,size=(int(count),4))
        vals.append(float(expr(L,sample).sum()/L**2))
    return {'L':L,'base_sites':sites,'portal_probability':p,
            'expected_portal_count':c*L*L,
            'measured_portal_count_mean':float(counts.mean()),
            'predicted_effective_c':c,
            'measured_effective_c':float(integrated.mean()),
            'predicted_effective_c_std':math.sqrt(theory_var),
            'measured_effective_c_std':float(integrated.std(ddof=1)),
            'smooth_profile_mean_integrated':float(np.mean(vals)),
            'smooth_profile_std_integrated':float(np.std(vals,ddof=1)),
            'positive_low_mode_W33_24sector_mass_squared_in_unit_R':10*c,
            'positive_high_mode_W33_15sector_mass_squared_in_unit_R':16*c}
def heat_w33(t):
    z=1+24*math.exp(-10*t)+15*math.exp(-16*t)
    derivative=240*math.exp(-10*t)+240*math.exp(-16*t)
    return {'diffusion_time_internal_units':t,'heat_trace':z,
            'internal_heat_spectral_dimension_at_t':2*t*derivative/z}
def main():
    Ls=[3,9,27,81,243]
    trials=[measure_one(L) for L in Ls]
    # q=3 Lucas mod-3 active support has 6^m cells at resolution L=3^m.
    # If used as a codimension two portal alone, effective internal weight
    # c_L = count/L^2 = (6/9)^m -> 0.
    fractal=[]
    for m in range(1,9):
        L=3**m
        D=math.log(6)/math.log(3)
        c_pure=(6/9)**m
        c_two=(36/9)**m
        fractal.append({'m':m,'L':L,'mod3_Pascal_fractal_dimension':D,
            'single_Pascal_support_count':6**m,'pure_fractal_effective_mass_coefficient':c_pure,
            'two_Pascal_products_count':6**(2*m),
            'two_fractals_effective_mass_coefficient':c_two,
            'critical_two_dimensional_support_count':L**2,
            'critical_effective_mass_coefficient':1.})
    # If the portal rule keeps exactly one portal child in q^2 children per
    # refinement step, p_m=(1/q^2)^m=1/L^2, critical in d=4.
    # Appending the isotropic selector multiplies it by 4/13.
    asserted=[{'level':m,'base_linear_resolution':3**m,
      'portal_access_probability':C*3**(-2*m),
      'physical_internal_gap_squared_24sector':10*C,
      'base_first_physical_laplacian_eigenvalue':(2-2*math.cos(2*math.pi/3**m))*3**(2*m),
      'dimensionless_internal_to_base_mass_ratio':math.sqrt(10*C)/
             math.sqrt((2-2*math.cos(2*math.pi/3**m))*3**(2*m))}
      for m in range(1,7)]
    assert abs(C-40/130)<1e-15
    assert all(abs(e['physical_internal_gap_squared_24sector']-40/13)<1e-12 for e in asserted)
    # Exact formula Var[C_L]=c (1-c/L^2)/L^2.
    assert abs(trials[-1]['measured_effective_c']-C)<.03
    heat=[heat_w33(t) for t in (.001,.01,.03,.05,.1,.2,.4,1)]
    out={'status':'PASS_CRITICAL_CODIMENSION_TWO_PASCAL_PORTAL_QUADRATIC_FORM',
      'hypothesis':'At four-dimensional lattice scale a=R/L, base links have physical kinetic coefficient a^-2. A fiber edge is available at each base site independently with probability p_L=c/L^2 (one of L^2 branches), and if available has physical strength a^-2. The average fiber coefficient is c/R². A q=3 symplectic-isotropic 2-subspace selector sets c=(40/130)=4/13 only if added as a separate microscopic rule.',
      'symplectic_selector_fraction_c':C,
      'W33_internal_Laplacian_eigenspaces':{'0':1,'10':24,'16':15},
      'Bernoulli_portal_trials':trials,
      'q3_mod3_Pascal_support_critical_comparison':fractal,
      'one_portal_among_9_per_level_example':asserted,
      'heat_trace_internal':heat,
      'mathematical_result':'In a unit physical 4-torus with L^4 cells, weighted internal fiber quadratic form has contribution a^4 sum_x a^-2 xi_x Q_I(f(x)), xi_x independent Bernoulli(c/L²). For fixed bounded smooth fiber profile Q_I(f), E[form] approaches c int_T4 Q_I(f) d^4x and Var[form]=O(L^-2). For constant profile Q_I=1, exact Var = c(1-c/L²)/L². This gives convergence in probability of that quadratic form for such test functions, not convergence of the full random operator or its spectrum.',
      'selection_mechanism':'Codimension-two portal density 1/L² cancels the L² ultraviolet factor of the internal graph Laplacian. A hierarchical q=3 selection with one active portal among 3² child options each refinement generates this scaling without level-by-level retuning. Selector factor 4/13 can be inherited from q-Gaussian symplectic lines, but both choice of a 2-of-4 dimensional portal and its dynamics are additional postulates.',
      'null_models':'A raw mod-3 Pascal triangle with branching 6 and scale factor 3 has Hausdorff D=log_3 6<2; its portal coefficient (6/9)^m dies out. Two independent mod-3 Pascal fractal supports have D=2log_3 6>2, producing divergent coefficient 4^m under the same normalization. Thus the ordinary Pascal fractal does NOT by itself solve scale selection.',
      'hard_limitations':'A spatially fixed two-dimensional portal is localized and breaks bulk homogeneity; the independent randomized model averages it over the 4D bulk but injects a stochastic microdynamical postulate. Pointwise gates get arbitrarily strong as a->0; concentration of smooth quadratic forms does not prove strong-resolvent spectral convergence, uniform locality, Lorentzian dynamics or radiative stability. The parent physical length R and field normalization still have to come from a proper action; this is a conditional scale RATIO mechanism, not derived particle masses or gravity.',
      'sources':['https://oeis.org/A153459','https://pressbooks.howardcc.edu/jrip1/chapter/fee-fi-fo-fum-deriving-e-latex-theta%CE%B8-and-latex-pi%CF%80-from-pascals-triangle/']}
    (ROOT/'data/toe_20261103_pascal_codim_two_portal_bridge.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PORTAL_BRIDGE',json.dumps({'c':C,'q3_dimension':fractal[0]['mod3_Pascal_fractal_dimension'],
                'last_2_trials':trials[-2:], 'asymptotic_mass_squared':10*C,
                'first_last_mass_ratio':asserted[0]['dimensionless_internal_to_base_mass_ratio'],
                'last_mass_ratio':asserted[-1]['dimensionless_internal_to_base_mass_ratio']})[:5600],flush=True)
if __name__=='__main__':main()
