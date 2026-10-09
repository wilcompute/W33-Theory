"""Independent exact Wick He2+He4 PSp symmetry-sector Ritz enclosures.
Point/line 24+24 and separated 15+15 representations. Full 78D
current-square H, corrected line sign; all energy bounds one-sided.
"""
from pathlib import Path
from fractions import Fraction as F
import json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_certified11_wick import I,block,parameters,rayleigh
import w33_20261008_5state_ritz as Q
DEGS=(2,4,6)
def certificate():
  edges,N,A,B,wp,wl=Q.geometry();m,t,f,e=parameters()
  same={}
  for side,adj,W in [('p',A,wp),('l',B,wl)]:
    ids=[0,int(np.flatnonzero(adj[0])[0]),
         int(np.flatnonzero((adj[0]==0)&(np.arange(40)!=0))[0])]
    same[side]=[block(edges,W[0],W[j],side,side,m,t,f,left=DEGS,right=DEGS) for j in ids]
  inc=int(np.flatnonzero(N[0])[0]);non=int(np.flatnonzero(N[0]==0)[0])
  cross=[block(edges,wp[0],wl[j],'p','l',m,t,f,left=DEGS,right=DEGS) for j in (inc,non)]
  def ratio(n,lam):
    adj=F(1,3**n);far=F(1,9**n)
    return I(1+lam*adj+(-1-lam)*far)
  def comb(blocks,lam,i,j):
    return tuple(blocks[0][i][j][v]+lam*blocks[1][i][j][v]
       +(-1-lam)*blocks[2][i][j][v] for v in range(2))
  def div(z,r):
    return tuple(x/r for x in z)
  def make(lam):
    norms=[ratio(n,lam) for n in DEGS]
    size=6 if lam==2 else 3
    if lam==2:
      H=[[(I(0),I(0)) for _ in range(size)] for _ in range(size)]
      for sid,off in [('p',0),('l',3)]:
        for i in range(3):
          for j in range(3):
            H[off+i][off+j]=div(comb(same[sid],lam,i,j),(norms[i]*norms[j]).sqrt())
      for i in range(3):
        for j in range(3):
          z=div(tuple(I(6).sqrt()*(cross[0][i][j][v]-cross[1][i][j][v]) for v in range(2)),(norms[i]*norms[j]).sqrt())
          H[i][3+j]=z;H[3+j][i]=(z[0],-z[1])
      return {'24':H}
    ans={}
    for side in ('p','l'):
      H=[[(I(0),I(0)) for _ in range(3)] for _ in range(3)]
      for i in range(3):
        for j in range(3):
          H[i][j]=div(comb(same[side],lam,i,j),(norms[i]*norms[j]).sqrt())
      ans['15_'+side]=H
    return ans
  sectors={**make(2),**make(-4)}
  out={}
  for label,H in sectors.items():
    midpoint=np.array([[complex(z[0].mid(),z[1].mid()) for z in row] for row in H])
    assert np.max(np.abs(midpoint-midpoint.conj().T))<1e-14
    ev,v=np.linalg.eigh(midpoint)
    trial=[(F(f'{z.real:.13f}'),F(f'{z.imag:.13f}')) for z in v[:,0]]
    E=rayleigh(H,trial)
    assert E.hi>F('127.595506')
    out[label]=dict(midpoint_eigenvalues=list(map(float,ev)),
        rational_trial=[[str(z),str(w)] for z,w in trial],
        lower_ritz_rayleigh_interval=E.data(),
        rigorous_sector_lowest_energy_upper_endpoint=str(E.hi),
        matrix_intervals=[[[a.data(),b.data()] for a,b in row] for row in H])
  assert out['24']['midpoint_eigenvalues'][0] <= 142.7193362242186+1e-7
  assert out['15_p']['midpoint_eigenvalues'][0] <= 143.6110807402656+1e-7
  return dict(status='PASS',schema='w33.20261009.he246_rational.v1',
    sectors=out,degrees=list(DEGS),norm_formula='1+lambda/3^n+(-1-lambda)/9^n, lambda=2 or -4',
    theorem='Rational outward Wick intervals enclose all 4x4 24-sector and 2x2 15-sector Ritz blocks. Rational first-trial Rayleigh gives certified UPPER bounds on sector spectra; no lower bounds on full H or sector minima.',
    limits='He6 mixed point/line modes included. Does not establish true ground irrep/multiplicity or physical excitation gap.')
if __name__=='__main__':
  d=certificate()
  (ROOT/'data/w33_20261009_he246_symmetry_exact_wick.json').write_text(json.dumps(d,indent=2)+'\n')
  print('HE246',[(k,v['midpoint_eigenvalues']) for k,v in d['sectors'].items()])
