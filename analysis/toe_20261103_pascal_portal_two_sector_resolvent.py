#!/usr/bin/env python3
"""A second W33 sector and resolved localized-portal screening test.

The first real 4D sparse eigenvalue run showed true lowest eigenvalues
~0.39 times constant-field Rayleigh. Here test whether this is the
lattice Green-function T-matrix renormalization (not arbitrary 0.39 fit),
on BOTH the W33 24d and 15d internal sectors.
"""
from pathlib import Path
import sys,json,math
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import toe_20261103_pascal_portal_sparse_spectrum as B
def main():
    prior=json.loads((ROOT/'data/toe_20261103_pascal_portal_sparse_spectrum.json').read_text())
    prior_rows=prior['rows']
    assert len(prior_rows)==10
    summary=[]
    for r in prior_rows:
        g=B.green4(r['L'])
        prediction=r['mean_field_constant_Rayleigh_mass_squared']/(1+10*g)
        summary.append({'L':r['L'],'sample':r['sample'],
            'W33_internal_sector_dimension':24,'bare_internal_eigenvalue':10,
            'actual_physical_squared_mass':r['lowest_actual_sparse_mass_squared'],
            'constant_trial_squared_mass':r['mean_field_constant_Rayleigh_mass_squared'],
            'resummed_local_Green_predicted_squared_mass':prediction,
            'relative_to_actual_prediction_error':(prediction-r['lowest_actual_sparse_mass_squared'])/r['lowest_actual_sparse_mass_squared']})
    B.lam=16.
    for L in (6,9,12,16):
        for seed in (20261103,20261104):
            r=B.trial(L,seed)
            prediction=r['mean_field_constant_Rayleigh_mass_squared']/(1+16*B.green4(L))
            row={'L':L,'sample':seed,'W33_internal_sector_dimension':15,
                 'bare_internal_eigenvalue':16,
                 'actual_physical_squared_mass':r['lowest_actual_sparse_mass_squared'],
                 'constant_trial_squared_mass':r['mean_field_constant_Rayleigh_mass_squared'],
                 'resummed_local_Green_predicted_squared_mass':prediction,
                 'relative_to_actual_prediction_error':(prediction-r['lowest_actual_sparse_mass_squared'])/r['lowest_actual_sparse_mass_squared']}
            summary.append(row)
            print('DUAL_PORTAL',json.dumps(row),flush=True)
    g16=B.green4(16);g32=B.green4(32)
    predicted={str(l):{'m2':(4/13)*l/(1+l*g32),
                        'constant_field_upper_mass2':(4/13)*l,
                        'local_renormalization_factor':1/(1+l*g32)}
               for l in (10,16)}
    maxerr=max(abs(r['relative_to_actual_prediction_error']) for r in summary)
    print('DUAL_PORTAL_SUMMARY',json.dumps({'g16':g16,'g32':g32,'maxerr':maxerr,'prediction':predicted}),flush=True)
    assert maxerr<.055
    assert predicted['16']['m2']>predicted['10']['m2']
    out={'status':'PASS_TWO_W33_EIGEN_SECTORS_4D_LOCAL_GREEN_SCREENING',
         'source_scripts':['analysis/toe_20261103_pascal_portal_sparse_spectrum.py',
                           'analysis/toe_20261103_pascal_codim_two_portal_bridge.py'],
         'comparison_rows':summary,
         'maximum_relative_Tmatrix_error_18_sample_eigenvalues':maxerr,
         'four_D_green_function_samples':{'L16':g16,'L32':g32},
         'L32_Green_approximated_two_sector_gap':predicted,
         'screened_mass_squared_ratio_15sector_to_24sector':predicted['16']['m2']/predicted['10']['m2'],
         'math':'On a periodic 4D lattice, dilute site portal potential H_L=L²(Delta+lambda diag xi), p_L=(4/13)/L². For isolated impurities the point scatterer T-matrix at low k is T=lambda/(1+lambda G4), G4=(1/L⁴)sum_{k !=0} 1/(8-2sum cos k_mu). The guessed homogenized gap is c*T, not c*lambda. This is checked against actual sparse eigenvalues for two internal W33 Laplacian sectors lambda=10 multiplicity24 and lambda=16 multiplicity15.',
         'critical_warning':'The agreement is an observed finite-size numeric test and a perturbative impurity-resolvent heuristic, NOT proof of the random operator continuum limit or of a universal renormalized coupling. Both sectors here are mathematically independent because portal masks are scalars on the same internal graph. Random spatial disorder and source covariance, finite lattice, physical 4D Lorentzian theory and quantum gauge matter remain open.',
         'physics_scope':'The construction supplies a conditional dimensionless ratio between the two internal masses and the parent base length, not a prediction of any observed particle mass. c=4/13 and critical portal density are additional microscopic selection postulates. Even if the continuum limit holds, the absolute length R remains external.',
         'originality':'The underlying point impurity screening and homogenization are established methods; applying them to this hypothetical W33*4D portal action is the new research test, not a general theorem of quantum gravity.',
         'prior_research':['https://link.springer.com/article/10.1007/s00440-024-01320-1']}
    (ROOT/'data/toe_20261103_pascal_portal_two_sector_resolvent.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
