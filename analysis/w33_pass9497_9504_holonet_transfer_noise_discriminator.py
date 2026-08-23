#!/usr/bin/env python3
"""Pass9497-9504: W33-native transfer/noise robustness of the rank-24 optical discriminator.

Replace the equal-port toy readout by n stages of lazy W33 nearest-neighbour
crosstalk, bounded detector gain error, and a separate binary-confusion model for
the dark monitor.  The result is an exact interval separation theorem.
"""
from __future__ import annotations
import json
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9497_9504_HOLONET_TRANSFER_NOISE_DISCRIMINATOR.json'

def gain_low(p,d):return (1-d)*p/((1-d)*p+(1+d)*(1-p))
def gain_high(p,d):return (1+d)*p/((1+d)*p+(1-d)*(1-p))

def main():
 # A W33 line has 4 points. A line point has 3 of its 12 neighbours on the line;
 # every off-line point has exactly one neighbour on the line (GQ axiom).
 # For lazy transfer T_eta=(1-eta)I+eta A/12, line mass evolves about stationarity 1/10
 # with eigenfactor 1-5 eta/6.
 delta=F(1,4);e8=F(1,10);u8=gain_high(e8,delta);assert u8==F(5,32)
 # Exact detector-gain separation threshold: low(p,1/4)>high(1/10,1/4) iff p>25/106.
 pcrit=F(25,106);rcrit=(pcrit-F(1,10))*F(10,9);assert rcrit==F(8,53)
 stress=[]
 for eta in [F(1,10),F(1,5),F(3,10),F(2,5)]:
  f=1-F(5,6)*eta;n=0
  while f**(n+1)>rcrit:n+=1
  p=F(1,10)+F(9,10)*f**n
  stress.append({'eta':str(eta),'retention_factor':str(f),'max_stages_with_guaranteed_line_separation':n,'line_mass_at_max_stages':str(p),'gain_distorted_lower':str(gain_low(p,delta))})
 # Convenient strong one-stage envelope eta<=2/5 gives p>=7/10 and a large exact gap.
 pstrong=F(7,10);lstrong=gain_low(pstrong,delta);assert lstrong==F(7,12)
 assert lstrong-u8==F(41,96)
 # Dark monitor: binary symmetric false-dark/false-bright confusion rho<=1/10.
 # d'=rho+(1-2rho)d.  E8/A2 d=0 -> <=1/10; E6 d=1/4 -> >=1/4.
 rho=F(1,10);dark_zero_max=rho;dark_e6_min=F(1,4);dark_gap=dark_e6_min-dark_zero_max;assert dark_gap==F(3,20)
 out={'schema':'w33.pass9497_9504.holonet_transfer_noise_discriminator.v1','status':'PASS','passes':'9497-9504',
  'transfer_model':{'kernel':'T_eta=(1-eta)I + eta A_W33/12','n_stage_line_mass':'p_n=1/10 + (9/10)(1-5 eta/6)^n','reason':'the partition {fixed W33 line, 36 off-line points} is equitable with random-walk transition probabilities 1/4 and 1/12 into the line'},
  'gain_model':{'per_port_gain_range':'[1-delta,1+delta]','stress_delta':'1/4','E8_best_line_upper':'5/32','line_carrier_lower_formula':'(1-delta)p/((1-delta)p+(1+delta)(1-p))'},
  'exact_line_separation':{'condition':'(1-5 eta/6)^n > 8/53','equivalent_true_line_mass':'p_n > 25/106','one_stage_eta_le_2_5':{'line_lower':'7/12','E8_upper':'5/32','gap':'41/96'},'stage_budget_examples':stress},
  'dark_monitor':{'true_dark_fractions':{'E8^3':'0','E6^4':'1/4','A2^12':'0'},'binary_confusion_model':'d_obs=rho+(1-2rho)d','rho_le':'1/10','zero_dark_upper':'1/10','E6_dark_lower':'1/4','guaranteed_gap':'3/20'},
  'classification':'Under the stated bounds, the line statistic separates E8^3 from both line carriers and the dark statistic separates E6^4 from A2^12; therefore all three remain distinguishable after W33-native crosstalk and bounded readout error.',
  'theorem':'The root-shadow discriminator is not an equal-coupling artefact. For an n-stage W33 nearest-neighbour transfer channel with +/-25% unknown port gains, line-vs-delocalized support remains provably separated whenever the line-mode retention factor exceeds 8/53. A dark-monitor confusion rate <=10% still leaves an exact 3/20 dark-fraction gap between E6^4 and the zero-dark carriers.',
  'boundary':'This is a finite transfer/noise envelope, not a fabricated optical Hamiltonian. eta, delta and rho are stress parameters chosen for robustness analysis, not measured Holonet hardware specifications; coherent phase interference, mode-dependent scattering and detector shot noise remain to be inserted.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','retention_threshold':'8/53','strong_gap':'41/96','dark_gap':'3/20'}));return 0
if __name__=='__main__':raise SystemExit(main())
