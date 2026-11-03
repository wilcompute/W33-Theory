#!/usr/bin/env python3
"""Rank-one amplitude-degeneracy falsifier from ACTUAL patched CLASS results.

At z=0, fixed-cosmology fading/off response for growth z=5->0 is
almost scale independent k in [0.05,3] h/Mpc. If an arbitrary amplitude
is marginalized, the scale-dependent component is tiny.
"""
from pathlib import Path
import numpy as np,json,math
ROOT=Path(__file__).resolve().parents[1]
def main():
 r=json.loads((ROOT/'data/toe_20261103_real_CLASS_fading_species_transfers.json').read_text())
 z=r['k_diagnostics']
 k=np.array([x['k_h_per_Mpc'] for x in z])
 ratio=np.array([x['fading_vs_cp0_normalized_z5_to_z0_growth_ratio'] for x in z])
 y=np.log(ratio)
 projection=y-y.mean()
 rms=float(np.sqrt(np.mean(projection**2)))
 maxabs=float(np.max(abs(projection)))
 abs_signal=float(np.mean(y))
 # For n scales with independent relative log-growth error 1%, after
 # nuisance (constant overall log amplitude) fitted, chi2 shape:
 def shape_chi2(sig):return float(np.sum((projection/sig)**2))
 # With one published PV measurement and no nuisance, simple rough precision.
 rsd=json.loads((ROOT/'data/toe_20261103_class_PV_real_RSD_singlepoint.json').read_text())
 delta=abs(rsd['fading_vs_same_params_zero_cprime_delta_fsigma8'])
 sig=.055
 rho=delta/sig
 s3=delta/3
 n_indep=(3*sig/delta)**2
 # We must not conflate fσ8 amplitude with transfer growth ratio.
 assert rms<1e-5 and abs_signal>.003
 assert shape_chi2(.01)<1e-4
 assert n_indep>600
 out={'status':'PASS_PROJECTED_CLASS_GROWTH_SHAPE_IDENTIFIABILITY_NO_GO',
 'source':'data/toe_20261103_real_CLASS_fading_species_transfers.json and independent linear P(k) DR1 PV comparison',
 'k_h_per_Mpc':k.tolist(),
 'fixed_background_parameter_fading_cprime_off_normalized_growth_z5_to_z0':ratio.tolist(),
 'mean_log_growth_offset':abs_signal,
 'log_growth_relative_scale_residual':projection.tolist(),
 'rms_scale_dependent_fractional_response':rms,
 'maximum_abs_scale_dependent_fractional_response':maxabs,
 'illustrative_independent_per_scale_fractional_error_for_chi2':.01,
 'shape_only_chi2_after_exact_constant_amplitude_marginalization':shape_chi2(.01),
 'public_PV_fsigma8_absolute_offset':delta,
 'public_PV_reported_1sigma':sig,
 'single_point_max_snr_if_parameter_fixed':rho,
 'idealized_one_point_sigma_needed_to_reach_3sigma':s3,
 'absurd_independent_same_precision_PV_bins_needed_for_3sigma':n_indep,
 'math':'For response vector g_i=ln(D_fading/D_off) and unknown scale-independent amplitude a, least-squares min_a sum[(g_i-a)/sigma]^2 = sum[(g_i-mean g)/sigma]^2 for equal errors. This projects the response out of the nuisance direction (1,...,1).',
 'scope':'NO survey likelihood. A formal shape-only Fisher null test under independent 1% equal log-growth errors and a single free amplitude. Real k covariances, redshift dependence, baryon-tracer bias, cosmic variance, AP correction and nonlinear scale response not evaluated. The same-observation-independent-duplicates count is a deliberately unrealistic precision illustration.',
 'conclusion':'On sampled linear scales and this fixed-background control, scale variation offers little leverage once amplitude is free. Multi-redshift and species-sensitive galaxy+lensing combinations, not more modes in same z bin, are the promising discriminants.'}
 (ROOT/'data/toe_20261103_class_growth_nuisance_projection.json').write_text(json.dumps(out,indent=2)+'\n')
 print('GROWTH_NULL',json.dumps({'mean':abs_signal,'rms_shape':rms,'maxshape':maxabs,
  'chi2_shape':shape_chi2(.01),'PV_snr':rho,'precision_3sigma':s3,'ideal_N':n_indep}),flush=True)
if __name__=='__main__':main()
