"""Round34 spectral dimension under cover size & invariant edge weights.

Compute FULL Laplacian spectrum of W33 Levi and cyclic p17,p83
covers via Bloch blocks; compare deterministic positive anisotropic
coupling weights on p17. Same one-decade plateau criterion.
"""
import sys,json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe26_css_matching_family import wilson
from w33_20261010_toe33_bloch_spectral_spacetime import heat_record,longest_plateau
OUT=ROOT/'data/w33_20261010_toe34_weighted_cover_dimensional_scaling.json'
def compute(p,voltage,weights):
 ed,D,C=wilson();weights=np.asarray(weights)
 degree=np.zeros(80)
 for (a,b),w in zip(ed,weights):degree[a]+=w;degree[b]+=w
 spectra=[]
 for k in range(p):
  L=np.diag(degree).astype(np.complex128)
  for (a,b),v,w in zip(ed,voltage,weights):
   ph=np.exp(2j*np.pi*k*int(v)/p)
   L[a,b]-=w*ph
   L[b,a]-=w*ph.conjugate()
  spectra.extend(np.linalg.eigvalsh(L))
 return np.sort(np.array(spectra))
def screen(vals):
 grid=np.geomspace(.03,300.,240)
 records=[heat_record(vals,t) for t in grid]
 return {str(d):longest_plateau(records,d-.25,d+.25) for d in (3,4)}
def run():
 ed,D,C=wilson()
 p17=json.loads((ROOT/'data/w33_20261009_toe31_compact_voltage_cover.json').read_text())['smallest_connected_cover_found_in_this_search']['voltages']
 p83=json.loads((ROOT/'data/w33_20261009_toe30_explicit_girth10_cover.json').read_text())['voltages']
 scenarios=[
   ('native80',1,[0]*160,np.ones(160)),
   ('p17_uniform',17,p17,np.ones(160)),
   ('p17_modest_edge_weight',17,p17,np.array([.8 if i%2 else 1.2 for i in range(160)])),
   ('p17_strong_edge_weight',17,p17,np.array([.5 if i%2 else 1.5 for i in range(160)])),
   ('p83_uniform',83,p83,np.ones(160))]
 outputs=[]
 for name,p,v,w in scenarios:
  eig=compute(p,v,w)
  assert len(eig)==p*80
  assert -1e-8<eig[0]<1e-8 and eig[1]>1e-6
  plateau=screen(eig)
  samples=[heat_record(eig,t) for t in (.2,.5,1,2,4,8,16)]
  row=dict(scenario=name,deck_degree=p,n=len(eig),spectral_gap=float(eig[1]),
   plateaus=plateau,has_3D_decade=plateau['3']['span_ratio']>=10,
   has_4D_decade=plateau['4']['span_ratio']>=10,
   diffusion_samples=samples)
  outputs.append(row)
  print('DIMSCALE',name,'gap',round(eig[1],6),'near3',round(plateau['3']['span_ratio'],2),'near4',round(plateau['4']['span_ratio'],2),flush=True)
 result=dict(status='PASS',
  method='Exact 80×80 Hermitian Bloch blocks for cyclic 1,17,83 voltages, with invariant positive edge weights on all sheets. Weighted Laplacian diag(sum weights)-weighted adjacency. Heat trace and d_s=2t*weighted mean lambda.',
  scenarios=outputs,
  one_decade_criterion='Peak uninterrupted sampled time ratio ≥10 with 3D band [2.75,3.25] or 4D [3.75,4.25], 240 log samples t∈[0.03,300].',
  interpretation='Tests TWO explicit girth10 covers and fixed edge-weight toy Hamiltonians, not a thermodynamic sequence proving a dimension. Edge weights imposed externally, not dynamically selected or spontaneous. No Einstein or Lorentzian continuum inferred.')
 OUT.write_text(json.dumps(result,indent=2)+'\n')
 return result
if __name__=='__main__':run()
