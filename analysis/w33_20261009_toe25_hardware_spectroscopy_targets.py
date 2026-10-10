"""Round25 engineering certificate for five-band two-boson spectroscopy.
All parameter numbers HYPOTHETICAL engineering targets, NOT a claim
that a device has been constructed or can meet specifications.
"""
import math,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261009_toe25_hardware_spectroscopy_targets.json'
def run():
 t_freq_mhz=5.0  # t/h, i.e. t angular/(2pi), not angular rate.
 entries=[]
 existing=json.loads((ROOT/'data/w33_20261009_toe23_universal_pair_ratios.json').read_text())
 for ratio in (16,32,64,128):
  U_mhz=t_freq_mhz*ratio
  gap_mhz=2*t_freq_mhz**2/U_mhz*(4-math.sqrt(6))
  rayleigh_time_us=1/gap_mhz
  T10=10/gap_mhz
  precision=float(existing['finite_U_numeric'][str(ratio)]['relative_error'])
  entries.append(dict(U_over_t=ratio,t_over_h_MHz=t_freq_mhz,U_over_h_MHz=U_mhz,
   leading_first_gap_over_h_MHz=gap_mhz,
   exact_first_gap_over_h_MHz=gap_mhz*(1+precision),
   max_frequency_resolution_time_one_beat_us=rayleigh_time_us,
   nominal_10_gap_cycles_acquisition_time_us=T10,
   finite_U_relative_error=precision))
  print('HARDWARE',ratio,'U MHz',U_mhz,'gap MHz',gap_mhz,
   '10cycles microseconds',T10,flush=True)
 # Third band separation from lowest = 2t²/U * 4; last=2t²/U*8.
 # Finite-size Rayleigh uncertainty ~ 1/T, dephasing broadens.
 f0=entries[1]['exact_first_gap_over_h_MHz']
 assert .47<f0<.49
 T_coh_us=100
 dephasing_fwhm_khz=1000/(math.pi*T_coh_us)
 assert dephasing_fwhm_khz<5
 targets=dict(min_vertices=80,min_links=160,
  required_local_double_occupancy='Bosonic 2-particle doublon |i,i>, with attractive on-site interaction U; hard-core qubit-only arrays cannot host this state',
  site_specific_double_boson_loading=True,
  site_resolved_two_boson_coincidence_or_parity=True,
  independently_calibrated_hopping_and_on_site_Kerr=True,
  programmable_all_160_link_hopping_with_independently_checkable_topology=True,
  proposed_coherent_simulator_type='Nonlinear multimode bosonic lattice (e.g., superconducting circuit resonators with Kerr sites and tunable couplers). Not established as a realizable 80x160 device.',
  single_photon_holonet_boundary='A single-photon linear-optical system does not realize the assumed two-boson attractive onsite U; a real nonlinear or measurement-induced effective interaction must be independently demonstrated.')
 out=dict(status='PASS',counts=targets,
  assumed_single_boson_hopping_frequency_MHz=t_freq_mhz,
  hypotheses=entries,
  selected_U_over_t=32,
  selected_ideal_fh_gap_MHz=f0,
  selected_Tcoh_hypothesis_us=T_coh_us,
  corresponding_lorentzian_dephasing_FWHM_kHz=dephasing_fwhm_khz,
  measurement_protocol='Calibrate all 80 site frequencies and 160 graph links; isolate the two-boson sector; verify local doublon population and attractive U; initialize |i,i>; measure coherent return probability or frequency-selective transitions to resolve 5 doublon bands. Record at least ten cycles of smallest gap, repeat on point and line node classes, and compare local integrated band weights [1,24,30,24,1]/80. Vary U/t=16,32,64,128 and extrapolate finite-U corrections; measure loss and spectral broadening independently.',
  conservative_targets='Under the illustrative t/h=5MHz, U/t=32 hypothesis, first doublon gap/h is about 0.48MHz and ten beating periods require >20 microseconds; low-dephasing target T2~100 microseconds gives Lorentzian FWHM ~3.2kHz, excluding other disorder/loss. These are dimensionally consistent engineering specifications, not empirical device measurements.',
  failure_conditions='No direct two-boson onsite attractive Hubbard U; incomplete 160-link W33 connectivity; coherence shorter than Fourier integration; link-frequency spread comparable to first gap; inability to resolve local doublon vs separated bosons; nonuniform coupling invalidating predicted degeneracies.',
  literature_links=['https://journals.aps.org/prresearch/abstract/10.1103/PhysRevResearch.7.L022038',
     'https://journals.aps.org/pra/abstract/10.1103/PhysRevA.109.053317'],
  caution='Published demonstrations of tunneling spectroscopy or Rydberg Hubbard proposals DO NOT demonstrate this exact 80-node, 160-link implementation. Targets are conditional and not a feasibility commitment.')
 OUT.write_text(json.dumps(out,indent=2)+'\n')
 return out
if __name__=='__main__':run()
