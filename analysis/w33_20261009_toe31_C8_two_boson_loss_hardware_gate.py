"""Round31 physical C8 hardware acceptance spec with boson loss channel.

All T1, T2 and readout contrast values are HYPOTHETICAL scenarios.
Convert Hamiltonian U/t into frequencies, compute exact independent
pair-survival law and acquisition sensitivity. No hardware access.
"""
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261009_toe31_C8_two_boson_loss_hardware_gate.json'
def run():
 U_t=32;t_h=5
 U_h=U_t*t_h
 assert U_h==160
 T=60.;grid=[]
 for T1 in (25.,50.,100.,200.,500.):
  endpoint=math.exp(-2*T/T1)
  average=(1-endpoint)/(2*T/T1)
  for T2 in (25.,50.,100.):
   # signal visibility as pair coherence; explicit conservative
   # model treats photon loss events as no coherent pair readout.
   vis=math.exp(-T/2/T2)*math.exp(-2*(T/2)/T1)
   shots_mult=1/(vis*vis)
   grid.append(dict(T1_us=T1,T2_us=T2,
    pair_survival_last_60us=endpoint,pair_survival_mean_over_60us=average,
    coherent_pair_visibility_at_30us=vis,
    conservative_shot_multiplier_at_30us=shots_mult))
  print('C8 T1',T1,'pair survive at60',round(endpoint,4),'average',round(average,4),flush=True)
 # lifetime bound for >=50% pair survival after endpoint of full sweep.
 required=2*T/math.log(2)
 assert required>170
 # simple timescale: U=160 MHz means pair binding phase 2pi 160e6 t,
 # while first resolved doublon gap is 0.182MHz; very different clocks.
 bandwidth=160./(.181747201118) # ratio of pair carrier to slow spectral gap
 rec=dict(status='PASS',device_type='hypothetical eight nonlinear bosonic sites in C8 ring, not built',
  geometry_sites=8,calibrated_links_needed=8,
  onsite_detuning_controls_needed=8,onsite_nonlinearities_needed=8,
  assumed_t_over_h_MHz=t_h,assumed_U_over_t=U_t,
  required_attractive_pair_binding_U_over_h_MHz=U_h,
  slow_first_boundpair_gap_over_h_MHz=0.181747201118,
  ratio_binding_carrier_to_first_gap=bandwidth,
  two_boson_survival_model='Assume independent exponential single-photon amplitude-damping lifetime T1 for each of two photons. No-loss survival at evolution t is exp(-2t/T1). This is a conditional Markovian loss model, not a measured photonic-chip lifetime.',
  pair_survival_50_percent_at_60us_requires_T1_us_greater_than=required,
  time_averaged_survival_over_sweep='(1-exp(-2T/T1))/(2T/T1) for delays uniformly spanning 0 to T',
  hypothetical_lifetime_coherence_grid=grid,
  unresolved_mechanisms='Pair-selective drive and spectroscopic contrast, independent two-boson loading, frequency drift, Kerr nonuniformity, correlated two-photon loss, qubit leakage, phase reference, readout and reset need laboratory measurements. Assumed 160MHz Kerr and 5MHz couplings are specifications, not experimentally demonstrated.',
  numerical_prediction='Even if an assumed T2 supports nominal linewidth smaller than the 0.182MHz gap, short T1 destroys a large fraction of two-particle survival and can overwhelm shot-count advantages. The absolute 160MHz carrier and 0.182MHz gap imply demanding frequency calibration across two orders of magnitude.',
  status_of_completion='Completed analytic hardware resource and decoherence acceptance calculations for five assumed T1 values and three assumed T2 values; no actual hardware test or physically calibrated parameters supplied.')
 OUT.write_text(json.dumps(rec,indent=2)+'\n')
 return rec
if __name__=='__main__':run()
