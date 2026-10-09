"""160-link native W33 gauge-potential global stress: edge-disjoint
theta triple *rigorous lower bound* and multi-start numerical upper bound.
By fixing a spanning tree all 79 pure-gauge links are removed exactly.
"""
from pathlib import Path
import sys,json,math
import numpy as np
from scipy.sparse import csr_matrix
from scipy.optimize import minimize
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_round19_gauge_cycle_frustration import cycle_vectors,rank_f2

def spanning_tree(edges):
 adj=[[] for _ in range(80)]
 for k,(a,b) in enumerate(edges):adj[a].append((b,k));adj[b].append((a,k))
 vis={0};stack=[0];chosen=[]
 while stack:
  a=stack.pop()
  for b,k in adj[a]:
   if b not in vis:
    vis.add(b);chosen.append(k);stack.append(b)
 assert len(vis)==80 and len(chosen)==79
 return sorted(set(range(len(edges)))-set(chosen))

def theta_packing(masks,rows):
 lookup={v:k for k,v in enumerate(masks)}
 triples=[]
 for i in range(len(masks)):
  for j in range(i+1,len(masks)):
   k=lookup.get(masks[i]^masks[j])
   if k is not None and k>j:
    # 8-cycles of a theta: mod2 relation enforces integer signed linear relation
    v=(rows[i],rows[j],rows[k])
    signs=next((s for s in ((a,b,c) for a in (-1,1) for b in (-1,1) for c in (-1,1)) if all(sum(s[t]*v[t].get(e,0) for t in range(3))==0 for e in range(160))),None)
    if signs is not None:triples.append((i,j,k))
 used=set();pack=[]
 for t in triples:
  if not any(k in used for k in t):
   pack.append(t);used.update(t)
 return triples,pack

def optimize_potential(rows,keep,seed=1881):
 C=csr_matrix(([float(x) for row in rows for x in row.values()],
               ([j for j,row in enumerate(rows) for _ in row],[k for row in rows for k in row])),
              shape=(len(rows),160))[:,keep].tocsr()
 assert C.shape==(1620,81)
 def fg(theta):
  loop=C@theta
  return float(np.cos(2*loop).sum()),np.asarray(-2*C.T@np.sin(2*loop)).reshape(-1)
 rng=np.random.default_rng(seed)
 trials=[]
 for initial in [np.zeros(81)]+[rng.uniform(-math.pi,math.pi,size=81) for _ in range(8)]:
  fit=minimize(fg,initial,jac=True,method='L-BFGS-B',options={'maxiter':650,'ftol':2e-12,'gtol':1e-7})
  trials.append(dict(energy=float(fit.fun),gradient_inf=float(np.max(np.abs(fit.jac))),
                     iterations=int(fit.nit),converged=bool(fit.success),theta=fit.x))
 best=min(trials,key=lambda v:v['energy'])
 assert abs(fg(-best['theta'])[0]-best['energy'])<1e-9
 return trials,best,C

def main():
 edges,cycles,masks,rows=cycle_vectors()
 relations,packing=theta_packing(masks,rows)
 print('THETA constraints',len(relations),'disjoint greedy',len(packing),'bound',-1620+1.5*len(packing),flush=True)
 keep=spanning_tree(edges)
 assert rank_f2([masks[i] for i in range(1620)])==81
 tests,best,C=optimize_potential(rows,keep)
 print('OPTIMAL candidate',best['energy'],'grad',best['gradient_inf'],'all runs',[round(q['energy'],5) for q in tests],flush=True)
 assert len(packing)>0
 assert best['energy']>=-1620+1.5*len(packing)-1e-6
 out=dict(status='PASS',cycles=1620,links=160,vertices=80,
    gauge_degrees=79,cycle_degrees=81,tree_chords=keep,
    exact_signed_theta_relation_count=len(relations),greedy_plaquette_disjoint_theta_pack=len(packing),
    packing_indices=[list(t) for t in packing],
    rigorous_global_lower_bound_units_g=-1620+1.5*len(packing),
    best_numerical_achieved_upper_bound_units_g=float(best['energy']),
    numerical_best_gradient_inf=best['gradient_inf'],
    numerical_best_chord_angles=[float(x) for x in best['theta']],
    multistart_energies=[float(x['energy']) for x in tests],
    phase_reversal_energy_identical=True,
    proof='Each independent theta triple of 8-cycles has signed fluxes summing zero modulo 2pi; sum cos(2F)>=-3/2 for each. Disjoint sets of plaquettes permit summation with unconstrained >=-1 for all other plaquettes; an exact global lower bound. Tree gauge fix removes exactly 79 U1 vertex gradients.',
    boundary='Rigorous bound not necessarily attained. Multi-start minimizer is only a variational/numerical upper bound, not certified global optimum. External frustrated Wilson action and kinetic term still model assumptions; no spontaneous chiral phase established.')
 (ROOT/'data/w33_20261009_round20_global_plaquette.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
