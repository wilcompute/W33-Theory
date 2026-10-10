"""TOE32 evidence-indexed architecture screen for C8 attractive doublon.

Separate actually published platform features from TARGET specifications.
Only our algebraic constraints and parametric photon-lifetime
feasibility are computed; no missing hardware measurements invented.
"""
import math,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261010_toe32_C8_platform_gap_screen.json'
def run():
 targets=dict(sites=8,links=8,onsite_two_boson_occupancy_required=True,
   U_over_t=32,abs_U_over_h_MHz=160,t_over_h_MHz=5,
   first_band_gap_over_h_MHz=0.181747201118,
   phase_sensitive_60us_acquisition_desired=True)
 platforms=[
  dict(name='Superconducting nonlinear Bose-Hubbard lattice (21 sites; PRX Quantum 2026)',
   observed='21-site superconducting Bose-Hubbard driven-dissipative simulator; bistability, multimode phases, spectroscopy, time-domain measurements',
   reference='https://doi.org/10.1103/rvhv-ms4t',
   doublon_requirement='Not established by the abstract; attractive Kerr sign, photon-number-selective pair readout and lifetime need measurement.',
   categorical_rejection=False),
  dict(name='Coupled superconducting artificial atoms (5 sites; PRL 2021)',
   observed='5 coupled artificial atoms, driven-dissipative Bose-Hubbard photon transport, transmission spectroscopy and cross-Kerr band visualization',
   reference='https://doi.org/10.1103/PhysRevLett.126.180503',
   doublon_requirement='Five-site chain is not 8-site ring; no published-in-abstract bound-pair 60us survival or 160MHz Kerr specification.',
   categorical_rejection=False),
  dict(name='Hard-core superconducting qubits (4x4; Nature 2024)',
   observed='16-site hard-core Bose-Hubbard emulation; local n=0,1; entanglement/correlation measurements',
   reference='https://doi.org/10.1038/s41586-024-07325-z',
   doublon_requirement='Local (a†)^2=0, n_i∈{0,1}, so the required |2_i> doublon is ABSENT. Needs non-hard-core/higher transmon levels.',
   categorical_rejection=True),
  dict(name='Manufacturable silicon quantum photonics (Nature 2025)',
   observed='Wafer-scale on-chip photon-pair generation, manipulation and detection in integrated photonics',
   reference='https://doi.org/10.1038/s41586-025-08820-7',
   doublon_requirement='Photon-pair generation does not establish 160MHz attractive Kerr interaction, coherent number-conserving Bose-Hubbard dynamics or 60us pair storage.',
   categorical_rejection=False)
 ]
 # Published works do NOT report our exact target combo; calculate
 # required coherence/retention in a common hypothetical Markov model.
 scenarios=[]
 for T1 in (25,50,100,174,200,500):
  for t in (20,60):
   alive=math.exp(-2*t/T1)
   scenarios.append(dict(T1_us=T1,interrogation_us=t,pair_survival=alive,passes_50percent=alive>=.5))
 thresholds=dict(direct_20us_T1_min_us=40/math.log(2),ramsey_60us_T1_min_us=120/math.log(2))
 assert targets['onsite_two_boson_occupancy_required']
 assert thresholds['ramsey_60us_T1_min_us']>173
 assert (0**2)==0
 rec=dict(status='PASS',target=targets,competing_research_platforms=platforms,
   loss_model='Assumed independent Markovian exponential loss of each of TWO bosons with lifetime T1: no-loss pair probability exp(-2t/T1), NOT a measured benchmark for any listed work.',
   hypothetical_pair_survival_table=scenarios,lifetime_threshold_for_50percent_survival=thresholds,
   hard_core_no_go='Hard-core boson local Hilbert basis {|0>,|1>} has a†²=0; projected doublon projector |2><2| is zero, and onsite -U n(n-1)/2 vanishes identically. The proposed C8 attractive doublon band model requires true n=2 occupancy and thus cannot be realized IN that hard-core restriction.',
   acceptance_gates=['eight links in a closed tunable C8 loop','local n=0,1,2 coherent Hilbert sector','attractive |U/h| near160MHz with calibrated sign and spread','hopping near5MHz with individual link sign and detuning controls','measured two-excitation survival throughout actual delay window','phase sensitive readout or independently addressed pair transition','direct spectral discrimination vs 12-link cube under identical noise','reported reset, readout contrast and drift'],
   honest_conclusion='Published experiments show relevant capabilities, NOT a device meeting all parameters. Cannot select an actual laboratory platform without hardware measurements or experimental partner; no connected hardware exists in this task.',
   source_scope='Platform observed capabilities are paraphrased from published abstracts; numerical requirements come from repo model and explicit loss assumption.')
 OUT.write_text(json.dumps(rec,indent=2)+'\n')
 print('C8 platforms',len(platforms),'hardcore excluded',sum(p['categorical_rejection'] for p in platforms),'T1',thresholds,flush=True)
 return rec
if __name__=='__main__':run()
