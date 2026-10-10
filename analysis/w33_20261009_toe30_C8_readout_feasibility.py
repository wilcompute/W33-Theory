"""Round30 C8 real-world timing *assumption sensitivity*, not hardware data.

Compare exact Round29 synthetic shot counts with contrast, T2, repeated
reset/readout overhead; demonstrate no unconditional direct-scan win.
"""
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data/w33_20261009_toe29_c8_experiment_decision.json'
OUT=ROOT/'data/w33_20261009_toe30_C8_readout_feasibility.json'
def run():
 base=json.loads(SRC.read_text())
 assert base['direct_scan']['total_shots']==361*8192
 assert base['Ramsey_baseline']['total_shots']==601*2*8192
 t2choices=(25,50,100)
 reset=(5,50,500)
 readout_contrast=((.2,.6),(.6,.6),(1.,1.))
 threshold=8192
 direct_evolution=20. # microseconds, an ASSUMPTION
 iq_mean_evolution=30. # mean sweep delay
 cases=[]
 for t2 in t2choices:
  for r in reset:
   for cd,ci in readout_contrast:
    cd_eff=cd*math.exp(-direct_evolution/t2)
    ci_eff=ci*math.exp(-iq_mean_evolution/t2)
    Ndir=math.ceil(threshold/cd_eff**2)
    Niq=math.ceil(threshold/ci_eff**2)
    shotsdir=361*Ndir;shotsiq=601*2*Niq
    # per shot reset+measure 5us + nominal coherent evolution.
    timesdir=shotsdir*(r+5+direct_evolution)/1e6
    timesiq=shotsiq*(r+5+iq_mean_evolution)/1e6
    cases.append(dict(T2_us=t2,reset_us=r,direct_intrinsic_contrast=cd,
       IQ_intrinsic_contrast=ci,
       direct_shots=shotsdir,IQ_shots=shotsiq,
       direct_total_seconds=timesdir,IQ_total_seconds=timesiq,
       direct_time_over_IQ_time=timesdir/timesiq,
       faster_protocol='direct' if timesdir<timesiq else 'IQ'))
 # With 0.2 direct vs 0.6 IQ contrast, direct can lose badly
 # despite 361 vs1202 sample locations.
 assert any(c['faster_protocol']=='IQ' for c in cases if c['direct_intrinsic_contrast']==.2)
 assert any(c['faster_protocol']=='direct' for c in cases if c['direct_intrinsic_contrast']==1)
 # Frequency resolution contrast: five levels first gap 0.1817MHz
 # spectral width from T2 is 1/(pi T2). At T2=25 still resolved.
 first_gap=base['direct_scan']['expected_center_freq_MHz'][1]-base['direct_scan']['expected_center_freq_MHz'][0]
 assert .17<first_gap<.19
 maxFWHM=max(1/(math.pi*t2) for t2 in t2choices)
 assert maxFWHM<first_gap
 optimal=min(cases,key=lambda x:x['direct_total_seconds'])
 rec=dict(status='PASS',native_geometry='eight-site C8 Bose-Hubbard pair model, not an experimentally constructed W33 machine',
  tested_T2_us=list(t2choices),tested_reset_overhead_us=list(reset),
  contrast_pairs=[list(x) for x in readout_contrast],
  readout_model='For target ideal binomial IQ shot noise corresponding to 8192 shots at contrast1, require ceil(8192/[intrinsic_contrast*exp(-t_interrogate/T2)]²) shots per point. Direct scan:361 frequency points, model assumed 20us interrogation; IQ:601 delays times2 quadratures, mean30us interrogation. Time per shot = reset +5us readout + duration.',
  scenario_grid=cases,
  idealized_first_gap_MHz=first_gap,
  decay_limited_linewidth_FWHM_MHz_by_T2={str(t2):1/(math.pi*t2) for t2 in t2choices},
  least_cost_direct_scenario=optimal,
  crucial_nonrobustness='The Round29 30% shot-count win assumes equal readout contrast. A threefold smaller direct-transition contrast (0.2 vs 0.6) can make direct readout slower despite fewer scan points; which protocol wins depends on T2, contrast and reset time. Assumed overhead dominates absolute time. None of these assumptions is calibrated to a physical instrument.',
  next_hardware_gate='Require experimentally measured pair transition contrast, per-site T2 under nonlinear U, reset/readout time, calibration drift, independently adjustable 8 links, 8 detunings and pair-loss channel before claiming a practical spectroscopy improvement.')
 OUT.write_text(json.dumps(rec,indent=2)+'\n')
 print('C8 FEASIBILITY scenarios',len(cases),'direct faster',sum(x['faster_protocol']=='direct' for x in cases),'IQ faster',sum(x['faster_protocol']=='IQ' for x in cases),'worst direct/IQ',round(max(x['direct_time_over_IQ_time'] for x in cases),2),flush=True)
 return rec
if __name__=='__main__':run()
