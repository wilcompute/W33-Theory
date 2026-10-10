"""TOE37 track5: W33 electrostatic U1 gauge action normalization audit.

Exact SRG40 graph-Laplacian pseudoinverse, resistance ratio and
the unavoidable free Maxwell coupling kappa:
S=(kappa/2)phi^T L phi - rho^T phi -> relative pair-action
rho^T L+ rho/(2kappa). Mathematically ratio R_adj/R_nonadj=13/14
fixed; absolute coupling (alpha) IS NOT.
Existing w33_poisson_kemeny_green_kernel independently computed
both resistances. This work is a physics normalisation firewall,
not a novel resistance formula.
"""
import sys,json
from pathlib import Path
from fractions import Fraction as F
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe26_css_matching_family import wilson
from w33_poisson_kemeny_green_kernel import poisson_kemeny_green_kernel_packet
OUT=ROOT/'data/w33_20261010_toe37_maxwell_normalization_audit.json'
def run(write=True):
 ed,D,C=wilson()
 A=np.zeros((40,40),dtype=np.int64)
 lines=[[] for i in range(40)]
 for p,l in ed:lines[l-40].append(p)
 for points in lines:
  assert len(points)==4
  for p in points:
   for q in points:
    if q!=p:A[p,q]=1
 assert np.array_equal(A,A.T) and set(A.sum(axis=1))=={12}
 A2=A@A
 J=np.ones((40,40),dtype=np.int64)
 assert np.array_equal(A2,8*np.eye(40,dtype=np.int64)-2*A+4*J)
 L=12*np.eye(40)-A
 # Pseudoinverse from spectral projectors A=12,2,-4
 # Lplus=(7/80)I + (1/160)A - (13/3200)J
 Green=F(7,80)*np.eye(40)+F(1,160)*A-F(13,3200)*J
 Green=np.asarray(Green,dtype=float)
 identity=np.eye(40)-J/40.
 assert np.linalg.norm(L@Green-identity)<1e-12
 assert np.linalg.norm(Green@np.ones(40))<1e-12
 adj=F(13,80);nonadj=F(7,40);ratio=adj/nonadj
 assert ratio==F(13,14)
 p,q=np.argwhere(A==1)[0]
 n,k=np.argwhere((A==0)&(~np.eye(40,dtype=bool)))[0]
 def rr(i,j):return float(Green[i,i]+Green[j,j]-2*Green[i,j])
 assert abs(rr(p,q)-float(adj))<1e-12 and abs(rr(n,k)-float(nonadj))<1e-12
 old=poisson_kemeny_green_kernel_packet()
 oldr=old['commute_and_resistance']
 assert F(oldr['effective_resistance_adjacent']['fraction'])==adj
 assert F(oldr['effective_resistance_nonedge']['fraction'])==nonadj
 samples=[]
 for kap in (1.,10.,137.):
  samples.append(dict(kappa=kap,
    neutral_adjacent_pair_action=float(adj)/(2*kap),
    neutral_nonadjacent_pair_action=float(nonadj)/(2*kap),
    invariant_shell_ratio=float(ratio)))
 assert samples[0]['neutral_adjacent_pair_action']/samples[1]['neutral_adjacent_pair_action']==10
 out=dict(status='PASS',
  W33_SRG_parameters={'v':40,'k':12,'lambda':2,'mu':4},
  graph_laplacian_eigenvalues={'0':1,'10':24,'16':15},
  exact_Green='L+ = (7/80) I + (1/160) A - (13/3200) J',
  MP_pseudoinverse_residual=float(np.linalg.norm(L@Green-identity)),
  resistance_adjacent=str(adj),resistance_nonadjacent=str(nonadj),
  resistance_adjacent_over_nonadjacent=str(ratio),
  earlier_independent_prior='analysis/w33_poisson_kemeny_green_kernel.py (prior repo exact equivalent hitting/commute/resistance calculation): these resistances are NOT newly discovered here.',
  lattice_U1_electrostatic_model='For positive arbitrary κ, source rho with sum rho=0: S[phi]=(κ/2)phi^T L phi-rho^T phi. Eliminating phi gives pair energy magnitude rho^T L+ rho/(2κ); all predictions scale as κ^-1. This is a *chosen* Gaussian U(1) graph action, not derived from W33 topology.',
  sample_pair_energies=samples,
  gauge_coupling_obstruction='W33 fixes relative Green function and shell ratio 13/14 in the chosen identical-conductance graph model, but κ is arbitrary and dimensionful physical distance/charge normalizations are missing. Hence no parameter-free alpha(0), quantum electron vacuum polarization, beta function, or observed Coulomb law follows. Rescaling κ continuously changes the absolute interaction while leaving all graph counts fixed.',
  physics_boundary='An experimentally falsifiable resistor-network ratio would require 40 nodes connected according to W33 with equal measured conductance; that is a synthetic classical network, NOT a QED charge measurement. Native graph combinatorics alone cannot set physical electromagnetic alpha.')
 if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
 print('TOE37 MAXWELL resistance',adj,nonadj,'ratio',ratio,'kappa free',flush=True)
 return out
if __name__=='__main__':run()
