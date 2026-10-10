"""Round33 experimentally grounded C8 feasibility discriminator.

Actual reported T1 from tunable two-transmon coupler 2018: 15–40us;
new nonlinear oscillator >=70MHz multi-photon terms and 200kHz
linewidth 2025; 21-site pumped chain 2026 switching up to143s.
None is the required 8-site attractive C8 doublon device.
"""
from pathlib import Path
import math,json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261010_toe33_C8_measured_comparator.json'
def survival(T1,t):return math.exp(-2*t/T1)
def run():
 t1_reported=[15.,40.] # measured in two-transmon circuit npj 2018
 delay=[20.,60.]
 vals=[dict(T1_us=T1,interrogation_us=t,no_loss_two_excitations=survival(T1,t))
       for T1 in t1_reported for t in delay]
 assert abs(vals[-1]['no_loss_two_excitations']-math.exp(-3))<1e-12
 threshold={str(t):2*t/math.log(2) for t in delay}
 assert threshold['60.0']>173 and threshold['20.0']<58
 # report explicitly 2025 nonmonotonic oscillator is not Kerr
 # and 21site ms--143 seconds is BISTABILITY switch not T1.
 papers=[
  dict(platform='Two coupled transmons with tunable hopping and cross-Kerr',
    year=2018,doi='10.1038/s41534-018-0088-9',
    observed='Tunable hopping and nonlinear cross-Kerr in single/two excitation manifolds; reported typical T1 of 15–40 microseconds at coupler bias points',
    measured_T1_us_range=[15,40],
    mismatch='Only two transmons, not C8 ring; under Markov pair loss this published T1 interval gives <5% pair survival at 60us. A redesigned platform might have better T1.'),
  dict(platform='Single Cooper-pair-pairing high-impedance superconducting oscillator',
    year=2025,doi='10.1038/s41467-025-62047-8',
    observed='Nonmonotonic interaction processes of orders2,3,4 with amplitudes >70MHz, linewidth about200kHz',
    mismatch='High-order interaction spectrum alternating sign is NOT the assumed simple uniform attractive Kerr U/h=160MHz; single nonlinear resonator, not 8-site coherent pair ring. No measured 60us pair survival provided.'),
  dict(platform='21-resonator driven-dissipative Bose-Hubbard chain',
    year=2026,doi='10.1103/rvhv-ms4t',
    observed='21 resonators, driven-dissipative multimode first-order phase transition; switching times range from milliseconds to143seconds',
    mismatch='143s is metastable PHASE SWITCHING, not coherence T1 or two-boson survival; no exact 8-site pair-level U/t=32 laboratory demonstration.')]
 result=dict(status='PASS',
   specified_target=dict(sites=8,links=8,U_over_h_MHz=160.,t_over_h_MHz=5.,U_over_t=32.,
    target_first_pair_band_gap_MHz=.181747201118),
   primary_empirical_calibration='Coupled transmons npj Quantum Information (2018): typical relaxation T1 15–40 us. Actual published numbers; not measured for the proposed C8 device.',
   measured_reference_T1_pair_survival_if_reused_under_independent_markov_model=vals,
   half_pair_survival_required_T1_us=threshold,
   relevant_published_devices=papers,
   unmeasured_requirements=['exact attractive -U n(n-1)/2 on each of 8 sites','all 8 hopping links closed in ring','two-excitation coherent hopping t/h near5MHz','pair preparation/readout contrast','T1 and T2 under actual nonlinear coupler biases','two-photon correlated loss, detuning and drift'],
   no_go_scope='Existing 2018 2-transmon reported lifetime does NOT meet this hypothetical 60us C8 survival criterion under the stated independent exponential loss model. It does NOT rule out other transmon platforms. Large nonlinear terms in a 2025 oscillator do NOT prove a 160MHz uniform attractive Kerr ring. Metastable classical 143-second phase switching does NOT imply 143-second photon lifetime.',
   key_external_sources=['https://www.nature.com/articles/s41534-018-0088-9','https://www.nature.com/articles/s41467-025-62047-8','https://journals.aps.org/prxquantum/abstract/10.1103/rvhv-ms4t'])
 OUT.write_text(json.dumps(result,indent=2)+'\n')
 print('C8 EMPIRICAL 2018 two-transmon 60us pair survival at T1=15..40us',survival(15,60),survival(40,60),flush=True)
 return result
if __name__=='__main__':run()
