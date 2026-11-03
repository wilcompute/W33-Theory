#!/usr/bin/env python3
"""Dimensional-selection and q-selection no-go for Pascal portal law.

At physical spacing a=R/L, choosing p=c/L² gives O(1) mean fiber mass
in ANY d, with relative fluctuations vanishing for d>2.
Thus the law does not select d=4, q=3, or an absolute length.
"""
from pathlib import Path
import json,math
ROOT=Path(__file__).resolve().parents[1]
def main():
    rows=[]
    for q in (2,3,5,7,11):
        c=(q+1)/(q*q+q+1)
        assert c>0 and c<1
        for d in (2,3,4,5,6):
            L=81
            p=c/L**2
            n=L**d
            # mass coefficient lambda*L²*(count/n)
            std=10*L*L*math.sqrt(n*p*(1-p))/n
            expected=10*c
            rows.append({'q':q,'dimension_d':d,'base_resolution_L':L,
              'line_selector_fraction_c':c,
              'mean_effective_mass_squared':expected,
              'standard_deviation_mass_squared_for_Bernoulli_portals':std,
              'coefficient_of_variation':std/expected,
              'asymptotic_std_scaling':'L^((2-d)/2)'})
    assert abs(next(x['mean_effective_mass_squared'] for x in rows if x['q']==3 and x['dimension_d']==4)-40/13)<1e-12
    std2=next(x['standard_deviation_mass_squared_for_Bernoulli_portals'] for x in rows if x['q']==3 and x['dimension_d']==2)
    std4=next(x['standard_deviation_mass_squared_for_Bernoulli_portals'] for x in rows if x['q']==3 and x['dimension_d']==4)
    assert std2>10*std4
    out={'status':'PASS_Q_AND_SPACETIME_DIMENSION_UNDERDETERMINATION_OF_PORTAL_DENSITY',
      'rows':rows,
      'selection_fraction':'c(q)=[(q+1)(q²+1)]/([4 2]_q)=(q+1)/(q²+q+1). For q=3, c=4/13; the q=3 input does not arise uniquely from this fraction.',
      'variance_formula':'For independent xi_x~Bernoulli(c/L²) on d-dimensional L^d cells and H_L=L²(Delta+lambda diag xi), normalized constant trial internal coefficient M_L=lambda L² * L^-d *sum xi. E[M_L]=lambda c, Var[M_L]=lambda² c (1-c/L²) L^(2-d). Thus concentration of this specific constant-trial coefficient requires d>2, not uniquely d=4.',
      'dimension_claim':'The critical codimension-two density law does NOT select four-dimensional spacetime. Every d>=3 has concentration of that constant trial energy; actual operator gaps require additional spectral/homogenization checks and can still differ or vanish.',
      'gauge_and_gravity_gap':'Independent physical requirements such as local Lorentz signature, chiral anomaly index in d=4, gauge dynamics and Einstein equations must select dimension and the correct continuum limit; counts alone do not.',
      'status_scope':'Exact elementary variance and Gaussian-binomial formulas. No claim of spacetime dimensional selection, unique q, or derived fundamental coupling.'}
    (ROOT/'data/toe_20261103_pascal_portal_dimension_no_go.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PORTAL_DIMENSION_FIREWALL',json.dumps({'q3_d2_std':std2,'q3_d4_std':std4,'fractions':{q:(q+1)/(q*q+q+1) for q in (2,3,5,7,11)}}),flush=True)
if __name__=='__main__':main()
