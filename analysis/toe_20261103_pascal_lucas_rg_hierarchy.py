#!/usr/bin/env python3
"""Lucas Pascal-mod-p exact fractal growth and one-loop dimensional transmutation.

Separates non-dimensional combinatorial counts from an actual RG mechanism.
The beta coefficient and UV coupling must be supplied by physical field
content, not inferred from a suggestive triangle integer.
"""
from pathlib import Path
import math,json
ROOT=Path(__file__).resolve().parents[1]
def digits(n,p):
    while n:
        yield n%p
        n//=p
def is_binomial_nonzero_lucas(n,k,p):
    while n or k:
        if k%p>n%p:return False
        n//=p;k//=p
    return True
def one_prime(p):
    scale=[]
    for m in (1,2,3):
        L=p**m
        actual=sum(is_binomial_nonzero_lucas(n,k,p) for n in range(L) for k in range(n+1))
        theoretical=(p*(p+1)//2)**m
        assert actual==theoretical
        scale.append({'depth':m,'L':L,'actual_nonzero_binomials_mod_p':actual,
                      'theoretical_branch_product':theoretical,
                      'critical_L_squared':L**2,
                      'relative_bulk_two_dimensional_density':actual/L**2})
    D=math.log(p*(p+1)/2)/math.log(p)
    return {'p':p,'branch_count_per_refinement':p*(p+1)//2,
            'Hausdorff_box_dimension':D,
            'dimension_product_two_independent_copies':2*D,
            'codimension_vs_two_support':2-D,
            'finite_depth_checks':scale}
def running():
    # One-loop alpha_s / SU(3) with Nf=3: beta(g)=-b0*g^3/(16 pi²), b0=9.
    b0=9
    values=[]
    for g in (.3,.35,.4,.45,.5,.55,.6,.7):
        logR=-8*math.pi**2/(b0*g*g)
        ratio=math.exp(logR)
        # UV scale changes mu->mu e^s, one-loop 1/g^2 increase b0*s/(8pi²).
        for s in (0,2,5):
            g_new=1/math.sqrt(1/g**2+b0*s/(8*math.pi**2))
            ratio_check=math.exp(s-8*math.pi**2/(b0*g_new**2))
            assert abs(ratio_check-ratio)<ratio*1e-11
        values.append({'SU3_Nf3_one_loop_g_uv':g,
                       'Lambda_over_mu_reference':ratio,
                       'log_scale_ratio':logR,
                       'lnLambda_sensitivity_to_ln_g':16*math.pi**2/(b0*g*g)})
    # q-Pascal counts alone fix neither the UV gauge coupling nor the length.
    # g^2=1/40 is OPTIONAL toy identification, visibly different.
    chosen=1/math.sqrt(40)
    fantasy=math.exp(-8*math.pi**2/(b0*chosen**2))
    return {'gauge_beta_assumption':'SU3 with 3 light Dirac fundamental flavors at one-loop: b0=11-2*Nf/3=9; NOT derived from W33 or q-Pascal.',
      'formula':'Lambda/mu=exp[-8*pi²/(b0*g(mu)²)] with fixed beta-function convention; one-loop asymptotic freedom, neglect thresholds.',
      'coupling_sensitivity_table':values,
      'tempting_unjustified_g2_equals_inverse_40':{'g2_assumed':1/40,
                'scale_ratio':fantasy},
      'rigorous_underdetermination':'For any desired ratio R in (0,1), choose g²=8*pi²/(b0*ln(1/R)). Thus the one-loop RG mechanism generates a hierarchy from a dimensionless input but does not predict its value without UV coupling boundary conditions. The dimensionful parent mu and scheme are external.',
      'source':'https://qft.org/courses/qft-ii/18-dimensional-transmutation-and-mass-gaps/'}
def main():
    rows=[one_prime(p) for p in (2,3,5)]
    assert abs(rows[1]['Hausdorff_box_dimension']-math.log(6)/math.log(3))<1e-14
    assert rows[1]['branch_count_per_refinement']==6
    R=running()
    out={'status':'PASS_LUCAS_PASCAL_FRACTAL_AND_RG_HIERARCHY_UNDERDETERMINATION',
     'p_prime_fractal_rows':rows,'RG_transmutation':R,
     'interpretation':'For p=3, Pascal mod-3 support is a 6-branch self-similar subset of a 9-cell refined triangle, with Hausdorff D=log_3 6=1.63093. It does not supply a codimension-two portal in 4D by itself. Even a two-copy support has D=3.26186, not exactly 4. An explicit candidate microscopic selection rule is required. Independently, logarithmic RG running can produce exponentially separated physical scales, but the UV coupling / renormalization condition is a free input unless a microscopic action selects it.',
     'classification':'Known Lucas theorem and textbook asymptotic-freedom RG, new integration as a falsifier of an otherwise attractive TOE scale hypothesis. No claimed original theorem or physical TOE.',
     'sources':['https://oeis.org/A153459',
                'https://qft.org/courses/qft-ii/18-dimensional-transmutation-and-mass-gaps/',
                'https://ir.cwi.nl/pub/28797/28797.pdf']}
    (ROOT/'data/toe_20261103_pascal_lucas_rg_hierarchy.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASCAL_RG',json.dumps({'rows':rows,'g05':next(z for z in R['coupling_sensitivity_table'] if z['SU3_Nf3_one_loop_g_uv']==.5),'unjustified_g2':R['tempting_unjustified_g2_equals_inverse_40']}),flush=True)
if __name__=='__main__':main()
