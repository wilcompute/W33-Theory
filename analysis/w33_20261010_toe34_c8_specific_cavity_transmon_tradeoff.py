"""Round34 one *specific* device blueprint screen: tunable bosonic cQED.

Use published 2024 experiment cavity lifetime ~200us and g/2pi
6.65MHz, transmon 2018 T1 15..40us and transmon typical
anharmonicity ~250MHz from 2020 published review. These came from
DIFFERENT platforms: mixing is hypothetical, not a measured chip.
Phenomenological dispersive participation r and Kerr K=Ktransmon*r².
"""
from pathlib import Path
import json,math
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261010_toe34_c8_specific_cavity_transmon_tradeoff.json'
def run():
 Tc=200.;Kt=250.;g=6.65
 desired=.5
 Ttarget=120/math.log(2)
 entries=[]
 for trans in (15.,40.,100.):
  # Tmix^-1=(1-r)/Tc+r/Ttrans, for effective Fock-one population.
  max_r=(1/Ttarget-1/Tc)/(1/trans-1/Tc)
  max_r=min(1,max(0,max_r))
  Kerrmax=Kt*max_r**2
  delta_min=g/math.sqrt(max_r) if max_r>0 else math.inf
  cases=[]
  for r in (.01,.02,.04,.10,.25,.50,.80):
   T_eff=1/((1-r)/Tc+r/trans)
   Kerr=Kt*r*r
   surv=math.exp(-120/T_eff)
   cases.append(dict(anharmonic_mode_participation=r,
       lifetime_us=T_eff,inherited_attractive_Kerr_over_h_MHz=Kerr,
       two_particle_survival_60us=surv,
       passes_50_percent_pair_survival=surv>=.5,
       passes_160MHz_inherited_Kerr=Kerr>=160))
  assert all(not (c['passes_50_percent_pair_survival'] and c['passes_160MHz_inherited_Kerr']) for c in cases)
  entries.append(dict(referenced_transmon_T1_us=trans,max_transmon_participation_for_50percent_pair_survival=max_r,
    largest_inherited_Kerr_MHz_at_survival_limit=Kerrmax,
    required_detuning_min_MHz_in_perturbative_r_g_over_delta_squared_model=delta_min,
    sampled_cases=cases))
 # To obtain K=160 MHz from Kt=250, r>=sqrt(.64)=.8,
 # which ruins lifetime for 15-100 us transmon.
 r_required=math.sqrt(160/Kt)
 assert abs(r_required-.8)<1e-12
 result=dict(status='PASS',device_architecture='eight copies of tunable cQED high-Q storage cavities each coupled to a flux-tunable transmon, coupled as an eight-link periodic bosonic ring (PROPOSED, NOT BUILT)',
  measured_reference_components=[
    {'paper':'2024 Nature Communications on-demand interaction regimes','url':'https://www.nature.com/articles/s41467-024-50201-7',
     'observed':'one 200us average lifetime bosonic cavity; cavity-transmon coupling g/2pi=6.65MHz; rapid transmon tuning; NOT an eight-site ring or Kerr 160MHz'},
    {'paper':'2018 npj Quantum Information tunable coupled transmons','url':'https://www.nature.com/articles/s41534-018-0088-9',
     'observed':'two-transmon unit with measured relaxation T1 15–40us; independent from 2024 cavity'},
    {'paper':'2020 npj Quantum Information transmon BH design','url':'https://www.nature.com/articles/s41534-020-0269-1',
     'observed':'typical transmon anharmonicity approx -250MHz, an indicative design value NOT measured for 2024 storage device'}],
  target=dict(sites=8,links=8,t_MHz=5,K_required_MHz=160,window_us=60,pair_survival_min=.5),
  equations='Independent Markov loss T_eff^-1=(1-r)/T_cavity+r/T_transmon; K_eff≈K_transmon*r² in perturbative participation model, with r≈(g/Delta)² for far-detuned mixing. Both are explicitly hypothetical scaling assumptions; nonlinear devices require full circuit quantization.',
  minimum_r_to_reach_160MHz_Kerr=r_required,
  survival_requisite_effective_T1_us=Ttarget,
  parameter_grid=entries,
  conditional_conclusion='With 200us cavity and representative 15-100us transmon lifetimes, no sampled participation point simultaneously meets Kerr160MHz and 50% two-photon survival at 60us in this simplified inherited-Kerr model. This rules out THIS NAIVE DISPERSIVE IMPLEMENTATION under its assumptions; not all possible transmon/tunable-coupler/nonlinear-resonator architectures.',
  source_boundary='Physical measurements belong to three DIFFERENT published devices. Combining figures is a speculative design; no physical 8-ring, T2, Kerr value, pair driving, readout fidelity or lab characterization exists.')
 OUT.write_text(json.dumps(result,indent=2)+'\n')
 print('ROUND34 C8 participation required',r_required,'Trequired',Ttarget,'max inherited K by Ttrans',[round(e['largest_inherited_Kerr_MHz_at_survival_limit'],3) for e in entries],flush=True)
 return result
if __name__=='__main__':run()
