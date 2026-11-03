#!/usr/bin/env python3
"""Exact anomaly recheck and conditional Dirac-messenger Higgs naturalness floor.

Independent of any uncommitted mechanism source: only uses published sterile
charges. Assumptions: single rank-one tree messenger, positive physical mass
mnu>=.05eV, mixing factor epsilon<=1, no cancellations and one-loop threshold
delta mH²~ yL² M²/(8pi²). Does NOT exclude protected UV models.
"""
from pathlib import Path
import math,json
from fractions import Fraction as Q
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
def main():
 old=json.loads((ROOT/'data/toe_20261103_sterile_anomaly_operators.json').read_text())
 assert [-15,12,12]in old['all_quark_normalized_integer_sectors']
 # One SM generation as left-handed Weyl fields, integer Q=3(B-L).
 # The second number is hypercharge Y (ordinary rational).
 sm=[('QL',6,1,Q(1,6)),('uC',3,-1,Q(-2,3)),
     ('dC',3,-1,Q(1,3)),('L',2,-3,Q(-1,2)),('eC',1,3,Q(1,1))]
 anomalies={}
 for name,power in [('gravity',1),('cubic',3)]:
  anomalies[name]=sum(mult*(q**power) for _,mult,q,_ in sm)
 assert anomalies=={'gravity':-3,'cubic':-27}
 assert sum(mult*y*y*q for _,mult,q,y in sm)==0
 assert sum(mult*y*q*q for _,mult,q,y in sm)==0
 # Three generations: -9,-81 and exotic Q=(-15,+12,+12): +9,+81.
 extra=[-15,12,12]
 assert sum(extra)==9 and sum(z**3 for z in extra)==81
 # Conventional baryon minus lepton charges for all new vectorlikes
 heavy=[-3,3]*3+[-6,6]
 assert sum(heavy)==0 and sum(z**3 for z in heavy)==0
 # EW SU2 Witten doublet count 4 per generation.
 assert 3*(3+1)%2==0
 v=174.0  # GeV; neutrino Yukawa vev convention <H0>=174
 mh=125.0
 mnu=.05e-9  # GeV
 M=1e16
 cases=[]
 for epsilon in (1,.1,.01):
  ymin=mnu/(v*epsilon)
  coeff=(1/(8*math.pi**2))
  mincorr=coeff*ymin*ymin*M*M
  mmax=mh/(math.sqrt(coeff)*ymin)
  cases.append({'sterile_mixing_or_suppression_max':epsilon,
    'minimum_left_Yukawa_for_0p05eV':ymin,
    'minimum_Higgs_mass_squared_threshold_at_M1e16_GeV_squared':mincorr,
    'minimum_threshold_over_higgs_mass_squared':mincorr/(mh*mh),
    'largest_M_for_threshold_less_mh_squared_GeV':mmax})
 assert cases[0]['minimum_threshold_over_higgs_mass_squared']>1
 assert cases[-1]['minimum_threshold_over_higgs_mass_squared']>10000
 # Holomorphicity issue: the non-SUSY messenger construction includes conjugate
 # Phi^dag terms which cannot be identical to chiral superpotential terms.
 holomorphic_required=True
 out={'status':'PASS_EXACT_ANOMALIES_AND_CONDITIONAL_DIRAC_MESSENGER_FLOOR',
  'standard_model_per_generation_anomalies_quark_norm':anomalies,
  'mixed_Y_squared_Q_and_Y_Q_squared':[0,0],
  'three_generation_SM_linear_and_cubic':[-9,-81],
  'exotic_left_singlet_Q_charges':extra,
  'singlet_linear_cubic':[9,81],
  'vectorlike_messenger_Q_charges':heavy,
  'Witten_SU2_number_doublets':12,
  'three_neutrino_mass_input_eV':0.05,'higgs_mass_reference_GeV':mh,
  'higgs_VEV_convention_GeV':v,'heavy_messenger_scale_input_GeV':M,
  'naturalness_cases':cases,
  'derivation':'In minimal rank-one Dirac messenger mnu=v*yL*epsilon with |epsilon|<=1. One-loop unsuppressed threshold |delta mH²|~|yL|² M²/(8 pi²); hence M<=sqrt(8 pi²)*mh*v*epsilon/mnu to satisfy the chosen no-tuning benchmark. Eigenvalues/partner cancellations can evade it.',
  'holomorphy':'Phi-dagger is not a chiral holomorphic superfield; a SUSY completion requires independent oppositely charged chiral scalars and an audited D-flat F-flat breaking sector.',
  'provenance':'Prior sterile anomaly class: data/toe_20261103_sterile_anomaly_operators.json. Uncommitted local mechanism_neutrino_messengers.py contains a tree full rank chain and 1e16 GeV Higgs threshold; this independent threshold lower bound uses no uncommitted code and does not claim the anomalous charge spectrum as new.',
  'scope':'A necessary condition under a single-entry rank-one Yukawa and no cancellation; not a universal see-saw bound, not a 3-generation mixing prediction, no physical continuum regulator/gauge measure tested.',
  'external_prior':['https://doi.org/10.1103/PhysRevD.57.7027',
                    'https://link.springer.com/article/10.1007/JHEP07%282026%29271',
                    'https://arxiv.org/abs/2610.09093']}
 (ROOT/'data/toe_20261103_chiral_messenger_naturalness_floor.json').write_text(json.dumps(out,indent=2)+'\n')
 print('CHIRAL_FLOOR',json.dumps({'anomalies':anomalies,'mmax':[(r['sterile_mixing_or_suppression_max'],r['largest_M_for_threshold_less_mh_squared_GeV']) for r in cases],'higgs_tension':cases[0]['minimum_threshold_over_higgs_mass_squared']}),flush=True)
if __name__=='__main__':main()
