"""Round28 executable C8 experimental pulse-plan + phase-reference readout.
Simulates 36-state two-boson quantum dynamics and a demodulated complex
Ramsey measurement with synthetic dephasing and Gaussian shot noise.
Not connected to laboratory equipment.
"""
from pathlib import Path
import json,sys,math
import numpy as np
from scipy.signal import find_peaks
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe27_c8_spectroscopy_noise_calibration import H_builder
OUT=ROOT/'data/w33_20261009_toe28_c8_control_ramsey_spectrum.json'
def run():
 H,basis=H_builder(U=32)
 eig,U=np.linalg.eigh(H)
 site=basis.index((0,0))
 weights=np.abs(U[site,:])**2
 leakage=float(weights[8:].sum())
 assert .003<leakage<.005
 groups=[(0,1),(1,3),(3,5),(5,7),(7,8)]
 tFreq=5. # t/h MHz
 # Rotate at the mean of the first 8 levels to avoid resolving the
 # large carrier (~160 MHz); probe deviations under +/- 1.25 MHz.
 carrier=float(np.mean(eig[:8]))*tFreq
 f=(eig[:8]*tFreq-carrier)
 times=np.arange(0,60.0001,.1) # microseconds
 T2=100. # hypothetical
 # A(t)=sum_j p_j exp(-i 2pi (E_j/h-f_ref)t), bound subspace
 A=np.exp(-2j*np.pi*np.outer(times,f))@weights[:8]
 decayed=np.exp(-times/T2)*A
 rng=np.random.default_rng(20261009)
 shots=8192
 # one IQ experiment per delay, quadrature noise scale 1/sqrt(shots)
 signal=decayed+(rng.normal(size=len(times))+1j*rng.normal(size=len(times)))/math.sqrt(shots)
 window=np.hanning(len(times))
 fft=np.fft.fft(signal*window)
 freq=-np.fft.fftfreq(len(times),d=.1)
 order=np.argsort(freq)
 freq,absfft=freq[order],abs(fft[order])
 peaks,_=find_peaks(absfft,height=max(absfft)*.07,distance=5)
 candidates=sorted([(float(freq[j]),float(absfft[j])) for j in peaks],key=lambda x:-x[1])
 # Analyze first 8 bound energies grouped by symmetry.
 expected=[float(np.mean(f[a:b])) for a,b in groups]
 found=[min(candidates,key=lambda x:abs(x[0]-f0))[0] for f0 in expected]
 worst=max(abs(a-b) for a,b in zip(expected,found))
 print('C8 RAMSEY expected',expected,'detected',found,'maxerrMHz',worst,'peaks',candidates[:12],flush=True)
 assert worst<.03
 gap=(expected[1]-expected[0])
 assert .17<gap<.19
 assert 60>10/gap
 # For probability-only |A(t)|² the frequency lines arise from
 # differences E_j-E_k, so carrier absolute spectral recovery fails.
 prob=np.abs(decayed)**2
 fsprob=np.fft.fftfreq(len(prob),d=.1)
 pfft=np.abs(np.fft.fft(prob*window))
 dominant_nonzero=float(abs(fsprob[np.argsort(pfft[1:])[-1]+1]))
 # Pulse-flow specification (abstract operations, not instruments)
 steps=[
  {'step':1,'operation':'CALIBRATE_SITE_FREQUENCIES','targets':8,'fit':'site detunings'},
  {'step':2,'operation':'CALIBRATE_RING_HOPPING','targets':8,'fit':'eight t_i'},
  {'step':3,'operation':'CALIBRATE_ONSITE_ATTRACTION','targets':8,'fit':'U_i>0 in H=-U_i n_i(n_i-1)/2'},
  {'step':4,'operation':'PREPARE_DOUBLON','state':'|2_0> on site 0, others vacuum'},
  {'step':5,'operation':'REFERENCE_FRAME','frequency_MHz':carrier,'basis':'complex pair-coherence quadratures, not probability only'},
  {'step':6,'operation':'FREE_EVOLUTION_SWEEP','first_us':0.,'last_us':60.,'sample_step_us':.1,'n_samples':len(times)},
  {'step':7,'operation':'MEASURE_IQ','shots_per_quadrature_per_time':shots,'hypothetical_T2_us':T2},
  {'step':8,'operation':'FIT_FIVE_BINDING_BANDS','method':'demodulated complex Fourier spectrum and 36-state model'},
  {'step':9,'operation':'INDEPENDENT_VALIDATION','measure':'pair continuum leakage, site-resolved pair events, loss and phase reference'}]
 result=dict(status='PASS',n_physical_sites=8,n_links=8,two_boson_Fock_dimension=36,
  U_over_t=32,t_over_h_assumed_MHz=tFreq,
  phase_reference_carrier_MHz=carrier,acquisition_us=60.,sample_step_us=.1,
  shots_per_quadrature_per_time=shots,total_estimated_shots=int(len(times)*2*shots),
  assumed_T2_us=T2,
  expected_demodulated_five_band_freq_MHz=expected,
  recovered_synthetic_five_band_freq_MHz=found,
  max_abs_recovery_error_MHz=worst,
  bound_to_scattering_probability=leakage,
  first_gap_MHz=gap,ten_gap_cycles_us=10/gap,
  probability_only_dominant_positive_frequency_MHz=dominant_nonzero,
  reference_readout='Complex A(t) referenced to a known pair-energy oscillator retains signed band frequencies. |A(t)|² has only band differences; it cannot generally recover absolute band energies. Quantum control to perform this complex measurement must be designed and physically validated.',
  control_sequence=steps,
  caveat='All 60us simulated IQ traces and shot noise are synthetic. No instrument calibration, feasible entangled reference or 80-site W33 demonstration is claimed. Hypothetical long coherence and 8192 shots per quadrature per time imply about 9.85 million samples, a substantial resource requirement.')
 OUT.write_text(json.dumps(result,indent=2)+'\n');return result
if __name__=='__main__':run()
