"""Round33 full cyclic voltage Bloch spectral-dimension screen.

Exact decomposition 1360-dimensional adjacency into 17 Hermitian
80x80 momentum blocks. Check zero mode, trace and base-sector
spectrum. Numerically compute heat trace and running d_s.
"""
from pathlib import Path
import json,sys,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe26_css_matching_family import wilson
OUT=ROOT/'data/w33_20261010_toe33_bloch_spectral_spacetime.json'
def spectrum(voltage,p):
 edges,D,C=wilson()
 vals=[]; sector_spectra=[]
 for k in range(p):
  A=np.zeros((80,80),dtype=np.complex128)
  for (a,b),z in zip(edges,voltage):
   phase=np.exp(2j*np.pi*k*int(z)/p)
   A[a,b]+=phase;A[b,a]+=phase.conjugate()
  eig=np.linalg.eigvalsh(A)
  sector_spectra.append(eig)
  vals.extend(4.-eig)
 return np.sort(np.array(vals)),sector_spectra
def heat_record(lams,t):
 z=np.exp(-lams*t);partition=np.sum(z)
 return dict(t=float(t),heat_trace=float(partition/len(lams)),
     running_spectral_dimension=float(2*t*np.dot(lams,z)/partition))
def longest_plateau(rec,lo,hi):
 best=dict(start_t=None,end_t=None,span_ratio=1.,length_points=0)
 start=None
 for j,x in enumerate(rec+[{'t':float('inf'),'running_spectral_dimension':float('inf')}]):
  yes=lo<=x['running_spectral_dimension']<=hi
  if yes and start is None:start=j
  if not yes and start is not None:
   end=j-1
   span=rec[end]['t']/rec[start]['t']
   if span>best['span_ratio']:best=dict(start_t=rec[start]['t'],end_t=rec[end]['t'],span_ratio=span,length_points=end-start+1)
   start=None
 return best
def run():
 cert=json.loads((ROOT/'data/w33_20261009_toe31_compact_voltage_cover.json').read_text())
 v=cert['smallest_connected_cover_found_in_this_search']['voltages'];p=17
 lams,sector=spectrum(v,p)
 assert len(lams)==1360
 assert np.sum(lams<1e-8)==1 and min(lams)>-1e-10
 assert np.max(lams)<=8+1e-10
 assert abs(np.sum(lams)-5440)<1e-8
 assert abs(np.sum(lams*lams)-1360*20)<1e-7 # trace (4I-A)^2=16+deg4 =20 per vertex
 base=np.sort(sector[0])
 assert abs(base[-1]-4)<1e-8 and abs(base[0]+4)<1e-8
 assert sum(abs(base-0)<1e-7)==30
 assert sum(abs(base-np.sqrt(6))<1e-7)==24
 assert sum(abs(base+np.sqrt(6))<1e-7)==24
 near=np.geomspace(.03,300.,220)
 records=[heat_record(lams,t) for t in near]
 plateau3=longest_plateau(records,2.75,3.25)
 plateau4=longest_plateau(records,3.75,4.25)
 summary=[heat_record(lams,float(t)) for t in (.1,.25,.5,1,2,4,8,16,32,64,128,256)]
 print('BLOCH17 gap',lams[1],'3D plateau',plateau3,'4D plateau',plateau4,flush=True)
 res=dict(status='PASS',vertices=len(lams),deck_group='Z17',
   Fourier_decomposition='A(1360×1360) unitarily decomposes into 17 blocks A_k(80×80), A_k[a,b]=sum_{voltage z of edge a->b} exp(2πikz/17); reverse entries conjugate. Numerical Hermitian eigvalsh per block.',
   Laplacian_nonzero_gap=float(lams[1]),global_max_laplacian=float(lams[-1]),
   base_k0_sector_adjacency='±4 multiplicity1, ±sqrt6 multiplicity24, zero multiplicity30.',
   full_spectrum_first_ten=[float(x) for x in lams[:10]],
   normalized_heat_trace_formula='K(t)=1/1360 sum_{i=1}^{1360} exp(-t lambda_i), running d_s=2t sum lambda_i exp(-t lambda_i)/sum exp(-t lambda_i)',
   heat_dimension_samples=summary,
   spectral_dimension_near3_band_2p75_to3p25=plateau3,
   spectral_dimension_near4_band_3p75_to4p25=plateau4,
   plateau_criterion='Require a continuous log-time span ratio >=10 with running dimension in [d-0.25,d+0.25] before using the phrase one-decade dimension plateau. A crossing alone does not qualify. Finite spectrum eventually d_s->0.',
   one_decade_three_dim_plateau=bool(plateau3['span_ratio']>=10),
   one_decade_four_dim_plateau=bool(plateau4['span_ratio']>=10),
   meaning='Computed diffusion spectral dimension is on a STATIC unweighted finite W33-derived cover. This tests but does not construct an emergent 3D spatial or 3+1D Lorentzian continuum. Weighted/dynamical/thermodynamic refinements not excluded; finite graph no gravitational action.')
 OUT.write_text(json.dumps(res,indent=2)+'\n')
 return res
if __name__=='__main__':run()
