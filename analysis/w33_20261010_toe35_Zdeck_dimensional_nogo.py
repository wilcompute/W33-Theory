"""Round35: cyclic W33 cover tower is a 1D periodic medium at long scales.

Fix the SAME 160 integer voltages supplied by Round31, reduce mod p
for p∈{17,31,67,127,257}. Fourier diagonalize exact 80x80 Bloch
Laplacian for each p. Estimate infinite-Z connectedness via gcd
fundamental fluxes and quadratic lowest Bloch band.
Conclude a fixed-voltage Z-deck tower can yield d_s=1 at asymptotic
intermediate times, not d_s=3; caution p-dependent data evade claim.
"""
from pathlib import Path
import math,sys,json,collections
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe26_css_matching_family import wilson
from w33_20261010_toe33_bloch_spectral_spacetime import heat_record,longest_plateau
OUT=ROOT/'data/w33_20261010_toe35_Zdeck_dimensional_nogo.json'
def flux_gcd(ed,v):
 G=[[] for _ in range(80)]
 for (a,b),z in zip(ed,v):
  G[a].append((b,int(z)));G[b].append((a,-int(z)))
 potential={0:0};q=collections.deque([0]);flux=[]
 while q:
  u=q.popleft()
  for w,d in G[u]:
   if w not in potential:potential[w]=potential[u]+d;q.append(w)
   else:flux.append(potential[u]+d-potential[w])
 assert len(potential)==80
 gcd=0
 for val in flux:gcd=math.gcd(gcd,abs(val))
 return gcd, sorted({abs(x) for x in flux if x})[:12]
def bloch_spectra(ed,v,p):
 Ns=[]
 for k in range(p):
  L=np.diag(np.full(80,4.,dtype=float)).astype(np.complex128)
  for (a,b),z in zip(ed,v):
   phase=np.exp(2j*np.pi*k*int(z)/p)
   L[a,b]-=phase;L[b,a]-=phase.conjugate()
  eigen=np.linalg.eigvalsh(L)
  Ns.extend(eigen)
 return np.sort(np.asarray(Ns))
def run():
 ed,D,C=wilson()
 prior=json.loads((ROOT/'data/w33_20261009_toe31_compact_voltage_cover.json').read_text())
 v=prior['smallest_connected_cover_found_in_this_search']['voltages']
 gcd,small=flux_gcd(ed,v)
 assert gcd==1,('infinite cyclic cover disconnected',gcd)
 # Bloch small k finite difference:
 def gap(k):
  L=np.eye(80,dtype=np.complex128)*4
  for (a,b),z in zip(ed,v):
   ph=np.exp(1j*k*z)
   L[a,b]-=ph;L[b,a]-=ph.conjugate()
  return float(np.linalg.eigvalsh(L)[0])
 coeffs=[gap(x)/x**2 for x in (1e-2,5e-3,2.5e-3)]
 assert coeffs[0]>0 and abs(coeffs[1]-coeffs[2])/coeffs[2]<.05,coeffs
 vdiff=coeffs[2];results=[]
 grid=np.geomspace(.1,1e4,320)
 for p in (17,31,67,127,257):
  eig=bloch_spectra(ed,v,p)
  assert len(eig)==p*80 and abs(eig[0])<1e-8 and eig[1]>1e-8
  heat=[heat_record(eig,float(t)) for t in grid]
  near1=longest_plateau(heat,.75,1.25)
  near3=longest_plateau(heat,2.75,3.25)
  spec=[heat_record(eig,t) for t in (2,5,10,20,50,100,200,400,800)]
  rec=dict(cover_degree=p,vertices=80*p,first_positive_gap=float(eig[1]),
   longest_running_dimension_near1=near1,longest_running_dimension_near3=near3,
   samples=spec)
  results.append(rec)
  print('Zdeck',p,'gap',round(float(eig[1]),6),'near1 span',round(near1['span_ratio'],2),'near3 span',round(near3['span_ratio'],2),flush=True)
 result=dict(status='PASS',
  generator='Round31 EXACT cyclic degree17 voltage data, interpreted as integer Z-valued 1-cochain then reduced modulo p for each covering degree. These are DIFFERENT covers from independent earlier degree83 cover.',
  winding_cycle_flux_gcd=gcd,first_absolute_winding_fluxes=small,
  coefficient_D_of_k_squared_band=vdiff,
  coefficient_checks_by_small_momentum=coeffs,
  exact_1D_tower_argument='The fixed connected integer-voltage cover is a graph periodic over deck group Z; finite quotients have Z_p decks. Floquet Laplacian is an 80x80 analytic 1-parameter Hermitian matrix L(k). Its bottom simple band is λ0(k)=Dk²+O(k4), D>0 by connected nontrivial winding flux, other Bloch bands remain gapped at k=0. Heat kernel per cell of the infinite cover ~const t^-1/2, so running d_s(t)->1 at long time. A finite p quotient ultimately has d_s->0, but an intermediate 1D window widens as p grows.',
  spectral_dimension_tower=results,
  relativistic_warning='For H=tL, low band energy E(k)-E(0)∼tDk², not Lorentz massless E=c|k|. Dynamic exponent z=2. The incidence W33 graph plus one deck winding coordinate cannot by itself yield isotropic three-dimensional Lorentzian massless propagation.',
  limits='Proves 1D only for the FIXED integer-voltage one-generator tower and simple unweighted Laplacian; p-dependent voltage families, nonabelian deck groups, multiple independent deck coordinates, interacting ground states and altered Hamiltonians can behave differently.')
 OUT.write_text(json.dumps(result,indent=2)+'\n')
 return result
if __name__=='__main__':run()
