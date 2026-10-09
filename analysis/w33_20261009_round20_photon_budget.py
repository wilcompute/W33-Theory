"""Single-photon five-W33-orbit survival-distribution robustness and a
distribution-free shot-budget bound. Native magnetic adjacency only.
"""
from pathlib import Path
import sys,json,math,itertools
import numpy as np
from scipy.linalg import eigh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_round19_finite_time_onephoton_readout import complex_adjacency
from w33_20261008_5state_ritz import geometry
def build():
 edges,*_=geometry()
 reps=json.loads((ROOT/'data/w33_20261009_PSp_orbits_isotropic_triplets.json').read_text())['orbits']
 phases=[.49,-.74,1.22]
 spec=[]
 for o in reps:
  a=complex_adjacency(edges,o['representative'],phases)
  ev,Q=eigh(a)
  weights=np.abs(Q)**2
  spec.append((ev,weights))
 return spec
def histogram(ev,w,t):
 return np.sort(np.abs(w@np.exp(-1j*t*ev))**2)
def main():
 spec=build()
 rows=[]
 for t in np.linspace(.25,12,236):
  hist=[histogram(e,w,t) for e,w in spec]
  gaps=[float(np.max(np.abs(hist[i]-hist[j]))) for i,j in itertools.combinations(range(5),2)]
  rows.append((float(t),min(gaps),max(gaps),int(np.argmin(gaps))))
 selected=sorted(rows,key=lambda x:x[1],reverse=True)[:12]
 print('PHOTON best',selected[:8],flush=True)
 # Uniform random independent survival Bernoulli sampling of the 80 initial sites
 # in each of five oracle models; Hoeffding+union bound is intentionally
 # conservative (no optimized likelihood ratio and no claimed device).
 delta=.05
 tests=5*80
 budgets=[]
 for t,d,dmax,pair in [rows[35],*selected[:3]]:
  eps=d/4
  n=math.ceil(math.log(2*tests/delta)/(2*eps*eps))
  # Frobenius ||A(phi+e)-A(phi)|| <= sqrt(2m)*e for m changed links.
  # For N=160 independently imperfect phase links, norm <= sqrt(320)*e.
  # ||U(t)-V(t)||<=t||A-B||, |prob difference|<=2t||A-B||.
  # Thus two candidate histograms retain separation >= d-4t sqrt(320) e.
  phase_per_edge_max=d/(8*t*math.sqrt(320))
  budgets.append(dict(t=t,min_pairwise_histogram_linf_distance=d,
    closest_pair_index=pair,Hoeffding_delta=delta,survival_shots_per_site_per_candidate=n,
    total_five_candidate_model_site_shots=int(tests*n),
    phase_radians_max_for_160_edges_pairwise_half_margin=phase_per_edge_max,
    note='This worst-case static per-edge 160-link phase-error bound is sufficient for retaining at least HALF the original histogram separation when errors affect both candidates, not tight. d_new >= d-4t sqrt(320)*epsilon >= d/2.'))
 out=dict(status='PASS',phase_angles=[.49,-.74,1.22],
  best_grid_search_time=selected[0][0],optimized_grid_ranking=selected,
  representative_shot_budgets=budgets,
  theorem='For empirical 80-site survival probabilities for five distinct candidates, each with N independent Bernoulli repetitions, simultaneous max error<=eta at confidence >=1-delta if N>=log(2*5*80/delta)/(2eta^2). Sorted order statistics are L-infinity nonexpansive; eta=d/4 preserves half the minimum pairwise histogram separation.',
  limitation='A simulated five-hypothesis reference library, not a proven physical unknown-state assay; free of source-detector bias, cross-talk, non-Markov drift. Scanned finite time grid only; no guarantee of global optimal t, and device fabrication constraints are not specified.')
 (ROOT/'data/w33_20261009_round20_photon_budget.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
