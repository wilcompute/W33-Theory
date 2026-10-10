"""Round27 8-site C8 experiment: numerical tolerance specification for
doublon spectroscopy with onsite detuning and hopping disorder, plus
distinguish complex Ramsey return from probability-only autocorrelation.
All synthetic; NO apparatus built or physical measurement.
"""
import json,itertools,math,numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261009_toe27_c8_spectroscopy_noise_calibration.json'
def H_builder(U=32,detune=None,link=None):
 n=8;detune=np.zeros(n) if detune is None else np.asarray(detune)
 link=np.ones(n) if link is None else np.asarray(link)
 basis=list(itertools.combinations_with_replacement(range(n),2))
 pos={b:j for j,b in enumerate(basis)}
 H=np.zeros((36,36))
 for col,(u,v) in enumerate(basis):
  H[col,col]=detune[u]+detune[v]-(U if u==v else 0)
  occ={k:(u==k)+(v==k) for k in {u,v}}
  for site,N in occ.items():
   for neighbor in ((site-1)%n,(site+1)%n):
    edge=min(site,neighbor) if abs(site-neighbor)==1 else 7
    st=[u,v];st.remove(site);st.append(neighbor)
    row=pos[tuple(sorted(st))]
    H[row,col]-=link[edge]*math.sqrt(N*(occ.get(neighbor,0)+1))
 assert np.allclose(H,H.T,atol=1e-12)
 return H,basis
def bands(H,basis):
 eigen,U=np.linalg.eigh(H)
 # ground 8 doublon levels; graph translation symmetry breaks in disorder
 levels=eigen[:8]
 groups=[(0,1),(1,3),(3,5),(5,7),(7,8)]
 centers=[float(np.mean(levels[a:b])) for a,b in groups]
 init=basis.index((0,0))
 weights=[float(np.sum(U[init,a:b]**2)) for a,b in groups]
 return dict(centers=centers,first_gap=centers[1]-centers[0],
  local_band_probabilities=weights,leakage=float(1-sum(weights)),
  first_band_internal_splitting=float(levels[2]-levels[1]),
  bound_scattering_energy_gap=float(eigen[8]-eigen[7]))
def run():
 rng=np.random.default_rng(20261009)
 H,basis=H_builder();ideal=bands(H,basis)
 assert H.shape==(36,36)
 assert 0.036<ideal['first_gap']<0.037
 metrics={}
 for sigma in (0,.0005,.001,.002,.005):
  shifts=[];splittings=[];leaks=[];bandcentres=[]
  for i in range(72):
   detune=rng.uniform(-sigma,sigma,size=8)
   link=1+rng.uniform(-sigma,sigma,size=8)
   noisy=bands(H_builder(detune=detune,link=link)[0],basis)
   shifts.append(noisy['first_gap']/ideal['first_gap']-1)
   splittings.append(noisy['first_band_internal_splitting'])
   leaks.append(noisy['leakage'])
   bandcentres.append(noisy['centers'])
  metrics[str(sigma)]=dict(synthetic_samples=72,
   max_abs_first_gap_relative_shift=max(map(abs,shifts)),
   rms_first_gap_relative_shift=float(np.std(shifts)),
   mean_leakage=float(np.mean(leaks)),
   mean_first_excited_pair_band_splitting=float(np.mean(splittings)),
   max_abs_centre_detuning_vs_ideal=float(max(abs(np.array(bandcentres).flatten()-
                      np.tile(ideal['centers'],72)))))
  print('C8 NOISE',sigma,metrics[str(sigma)]['max_abs_first_gap_relative_shift'],
        'leakage',metrics[str(sigma)]['mean_leakage'],flush=True)
 assert metrics['0.005']['max_abs_first_gap_relative_shift']>metrics['0']['max_abs_first_gap_relative_shift']
 t_over_h_mhz=5.
 gap_freq=ideal['first_gap']*t_over_h_mhz
 result=dict(status='PASS',native_minimal_geometry='Levi apartment C8: 8 sites, 8 links',H_two_boson_dim=36,
  U_over_t=32,t_over_h_hypothetical_MHz=t_over_h_mhz,
  ideal_C8_five_band_spectrum=ideal,
  smallest_nonzero_band_gap_over_h_MHz=gap_freq,
  min_ten_gap_cycles_coherent_acquisition_us=10/gap_freq,
  synthetic_bounded_independent_onsite_link_noise_in_t_units=metrics,
  native_C8_exact_band_multiplicities=[1,2,2,2,1],
  native_C8_boson_computation='H=-sum_i t_i(b†_i b_(i+1)+h.c.)-U sum_i n_i(n_i-1)/2+sum_i detune_i n_i, with exact 2-boson occupation sqrt factors.',
  important_readout_correction='Complex phase-sensitive Loschmidt amplitude A(t)=<2_0|e^{-i Ht}|2_0> has Fourier components at the energy bands, whereas probability-only return P(t)=abs(A(t))² contains PAIRWISE energy DIFFERENCES. Consequently five absolute band centers cannot generally be extracted directly from a Fourier transform of return probability alone. Use Ramsey/quadrature phase reference or frequency-selective spectroscopy.',
  protocol='Start with C8 8 nodes and one-site |2> pair; calibrate eight link couplings and onsite detunings, apply genuinely attractive U, measure complex pair-return via a phase-reference interferometer or transition spectroscopy, resolve five band groups and the bound/scattering gap, fit U/t, noise, and leakage. Quantify both coherent capture and pair-loss channel separately.',
  limitations='All 72x5 disorder trials are synthetic independent uniformly distributed in [-sigma,sigma] in units of t; not hardware verification or worst-case control certification. For U=32t and t/h=5MHz, ten cycles require about55us; device coherence and nonlinear mode availability are unverified.')
 OUT.write_text(json.dumps(result,indent=2)+'\n')
 return result
if __name__=='__main__':run()
