"""Round29 C8 phase-sensitive Ramsey vs direct resonant spectroscopy:
resource-aware, synthetic model comparison, including 8-site cube Q3
as an independent competing connectivity hypothesis.
"""
from pathlib import Path
import json,itertools,math,numpy as np
from scipy.signal import find_peaks
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261009_toe29_c8_experiment_decision.json'
def spectral(graph,U=32):
 n=8;edges=( [(i,(i+1)%8) for i in range(8)] if graph=='C8'
             else [(i,j) for i in range(8) for j in range(i+1,8) if ((i^j).bit_count()==1)])
 basis=list(itertools.combinations_with_replacement(range(n),2))
 lookup={pair:i for i,pair in enumerate(basis)}
 H=np.zeros((36,36))
 for col,st in enumerate(basis):
  occ={i:st.count(i) for i in set(st)}
  if len(occ)==1:H[col,col]=-U
  for (a,b) in edges:
   for source,target in ((a,b),(b,a)):
    if source not in occ:continue
    dst=list(st);dst.remove(source);dst.append(target)
    row=lookup[tuple(sorted(dst))]
    H[row,col]-=math.sqrt(occ[source]*(occ.get(target,0)+1))
 assert np.allclose(H,H.T)
 e,V=np.linalg.eigh(H);i0=lookup[(0,0)]
 levels=e[:8];w=np.abs(V[i0,:8])**2
 groups=[]
 for idx in range(len(levels)):
  if not groups or abs(levels[idx]-levels[groups[-1][-1]])>1e-8:groups.append([idx])
  else:groups[-1].append(idx)
 return dict(edges=len(edges),eigen=e,weights=w,groups=groups,
  local_band_centers=[float(np.mean(levels[g])) for g in groups],
  local_band_weights=[float(w[g].sum()) for g in groups],
  bound_leakage=float(1-w.sum()))
def run():
 C=spectral('C8');Q=spectral('Q3')
 assert len(C['groups'])==5 and [len(g) for g in C['groups']]==[1,2,2,2,1]
 assert len(Q['groups'])==4 and [len(g) for g in Q['groups']]==[1,3,3,1]
 t_freq=5.0;T2=100.;shots=8192
 c_ref=np.mean(C['eigen'][:8])*t_freq
 expected=(np.array(C['local_band_centers'])*t_freq-c_ref)
 fgrid=np.linspace(-.9,.9,361);linewidth=1/(math.pi*T2)
 # Idealized direct spectroscopy lines as Lorentzians; scan point
 # represents an INDEPENDENT long-lived pair-selective transition.
 lor=lambda f0:(linewidth**2)/((fgrid-f0)**2+linewidth**2)
 ideal=np.zeros(len(fgrid))
 for c,w in zip(expected,C['local_band_weights']):ideal+=w*lor(c)
 rng=np.random.default_rng(20261009)
 direct=rng.binomial(shots,np.clip(ideal,0,1))/shots
 peaks,_=find_peaks(direct,distance=12,prominence=.012)
 peakfreq=np.array(sorted(fgrid[peaks]))
 nearest=np.array([min(peakfreq,key=lambda x:abs(x-y)) for y in expected])
 err=np.max(np.abs(nearest-expected))
 assert len(peaks)==5,(peaks,peakfreq,expected)
 assert err<.015
 Ramsey=601*2*8192
 directshots=len(fgrid)*shots
 assert directshots<Ramsey
 print('SPECTRO',len(C['groups']),len(Q['groups']),'direct peaks',list(np.round(peakfreq,4)),'worst MHz',err,flush=True)
 def serialize(model):
  return dict(link_count=model['edges'],eigenvalue_band_multiplicities=[len(g) for g in model['groups']],
   band_centers_over_t=model['local_band_centers'],
   local_initial_doublon_band_weights=model['local_band_weights'],scattering_leakage=model['bound_leakage'])
 out=dict(status='PASS',C8=serialize(C),eight_site_cube_Q3_competitor=serialize(Q),
  t_over_h_hypothetical_MHz=t_freq,
  assumed_T2_us=T2,
  Lorentzian_linewidth_FWHM_MHz=2*linewidth,
  direct_scan=dict(freq_range_MHz=[float(fgrid[0]),float(fgrid[-1])],freq_step_MHz=float(fgrid[1]-fgrid[0]),
   points=len(fgrid),shots_per_point=shots,total_shots=directshots,
   expected_center_freq_MHz=list(expected),
   recovered_synthetic_center_freq_MHz=list(nearest),
   max_abs_peak_error_MHz=float(err)),
  Ramsey_baseline=dict(times=601,quadratures=2,shots_per_quadrature=8192,total_shots=Ramsey),
  shot_ratio_direct_to_Ramsey=directshots/Ramsey,
  model_distinction='Ring C8 has five doublon bands multiplicities 1,2,2,2,1 while 3-cube Q3 has four bands 1,3,3,1 at U/t=32. These graphs have DIFFERENT LINK COUNTS (8 vs12), which must be calibrated; the spectral difference is a cross-check, not the sole way to infer connectivity.',
  experimental_requirements='Direct spectroscopy assumes a separately accessible calibrated pair-selective transition with Lorentzian response and 100us coherence. Real device must demonstrate signal contrast, transition selection, Rabi dynamics, frequency reference, pair leakage and readout. The ~3-million vs ~9.85-million synthetic shot comparison ignores reset/readout latencies and contrasts. Neither setup is experimentally instantiated.',
  provenance='Round28 synthetic complex IQ protocol with 601 x2 x8192 shots; Round29 adds an explicitly conditional direct-transition spectral surrogate, a second graph topology and a quantitative shot-count trade.')
 OUT.write_text(json.dumps(out,indent=2)+'\n');return out
if __name__=='__main__':run()
