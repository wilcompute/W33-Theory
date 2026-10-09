"""Exact n=8 site-return histogram separates five *one-photon* Peierls-
isospectral W33 selector families; no two-body nonlinearity required.
First local phase sensitivity at girth-eight; all n<=6 return multisets
equal under these native flags. Check both modular reductions and the
G8=2(A8)_xx+106848 identity on degree4 girth8 Levi.
"""
from pathlib import Path
import sys,json
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_20261009_round17_interaction_trace_certificate as OLD
from w33_20261009_round18_fixedU_resolvent_certificate import zprod,projected_returns
from w33_20261008_5state_ritz import geometry
def main():
 edges,*_=geometry()
 reps=json.loads((ROOT/'data/w33_20261009_PSp_orbits_isotropic_triplets.json').read_text())['orbits']
 out={}
 for p in (1000003,1000033):
  OLD.MOD=p;rows=[]
  for o in reps:
   A=OLD.phased_adj(edges,o['representative'])
   power=(np.eye(80,dtype=np.int64),np.zeros((80,80),dtype=np.int64))
   record={}
   for n in range(0,9):
    if n%2==0:
     record[str(n)]=sorted(map(int,np.diag(power[0])))
     assert np.all(np.diag(power[1])%p==0)
    power=zprod(power,A,p)
   G=projected_returns(A,p,9)
   # Diagonal A²,A⁴,A⁶ are independent of edge phases because girth 8:
   for n,value in [(2,4),(4,28),(6,232)]:
    assert record[str(n)]==[value]*80
   # 2*C(8,2)*(A²)_xx*(A⁶)_xx + C(8,4)*(A⁴)_xx²
   constant=(2*28*4*232+70*28**2)%p
   assert constant==106848
   # Compare site-independent sorted histograms rather than labeled sites.
   local_g8=sorted(int(z) for z in np.diag(G[8][0]))
   assert local_g8==sorted((2*x+106848)%p for x in record['8'])
   rows.append(record)
  sep={n:len(set(tuple(row[str(n)]) for row in rows)) for n in ('0','2','4','6','8')}
  assert sep=={'0':1,'2':1,'4':1,'6':1,'8':5}
  out[str(p)]=dict(distinct_relabel_invariant_site_return_histograms=sep,all_orbit_eighth_histograms=[row['8'] for row in rows])
  print('SINGLE-PARTICLE p',p,'partition',sep,'eighth unique histograms',len({tuple(z['8']) for z in rows}),flush=True)
 result=dict(status='PASS',certificate=out,
  identity='On W33 Levi degree4 girth8: (A²)_xx=4, (A⁴)_xx=28, (A⁶)_xx=232; for dGamma(A) doublon return, G8(xx)=2(A8)_xx+106848. Thus eighth-order LOCAL two-boson return requires no interaction and is equivalent to single-photon eighth local walk moment.',
  boundary='The 80-site distribution is basis-local, not the one-body spectrum. Five global spectral traces remain identical; sorted distributions are invariant to vertex relabeling, not arbitrary unitary conjugation. Formal 8th short-time coefficient may be much harder to measure than finite-time optical intensities.',
  prior='Vertex-local spectral measures distinguish some cospectral structures; not a novel general walk idea. Emms-Severini-Wilson-Hancock 2009, Pattern Recognition 42, 1988-2002.')
 (ROOT/'data/w33_20261009_round19_onephoton_local_eighth.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
