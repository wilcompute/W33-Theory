#!/usr/bin/env python3
"""Exact rational W33 triple-voltage acoustic metric via resistance,
and local scalar wave benchmark; no emergent c or fermionic chirality."""
from pathlib import Path
from fractions import Fraction as F
import sys,math,json
import numpy as np
from scipy.linalg import eigvalsh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261102_route_216_cubic_tomography import geometry
def main():
    pts,lines,N,idx,norm,omega=geometry()
    A=N@N.T-4*np.eye(40,dtype=int)
    assert np.array_equal(A@A,8*np.eye(40,dtype=int)-2*A+4*np.ones((40,40),dtype=int))
    edges=[(a,b) for a in range(40) for b in range(a+1,40) if A[a,b]]
    chosen=[]
    for a,b in edges:
      if all(a not in e and b not in e for e in chosen):chosen.append((a,b))
      if len(chosen)==3:break
    assert chosen==[(0,1),(2,3),(4,7)]
    E=np.eye(40,dtype=int)
    dip=[E[a]-E[b] for a,b in chosen]
    R=[];D=[];cross=[]
    for i in range(3):
      rrow=[];drow=[];arow=[]
      for j in range(3):
        x=int(dip[i]@dip[j]);y=int(dip[i]@A@dip[j])
        r=F(21,20)*x+F(3,40)*y
        diff=(F(1,480) if i==j else F(0))-r/5760
        rrow.append(r);drow.append(diff);arow.append(y)
      R.append(rrow);D.append(drow);cross.append(arow)
    assert cross==[[-2,0,0],[0,-2,0],[0,0,-2]]
    assert D==[[F(67,38400) if i==j else F(0) for j in range(3)] for i in range(3)]
    def eig(k):
      H=A.astype(complex)
      for t,(a,b) in zip(k,chosen):
        H[a,b]=np.exp(1j*t);H[b,a]=np.exp(-1j*t)
      return eigvalsh(np.eye(40)-H/12,subset_by_index=[0,1],check_finite=False)
    assert abs(eig([0,0,0])[1]-5/6)<1e-12
    c0=math.sqrt(float(F(67,38400)))
    probes=[]
    for axis in ([1,0,0],[1,1,1],[1,2,-1]):
      w=np.array(axis,dtype=float);w/=np.linalg.norm(w)
      for magnitude in (.003,.01,.03):
        e=float(eig(w*magnitude)[0])
        v=math.sqrt(max(0,e))/(magnitude*c0)
        probes.append({'direction':axis,'k':magnitude,'lowest_laplacian_eigenvalue':e,'scalar_wave_speed_ratio':v})
    assert max(abs(z['scalar_wave_speed_ratio']-1) for z in probes)<.002
    out={'status':'PASS_EXACT_POSITIVE_ISOTROPIC_3DECK_METRIC',
       'voltage_edges':chosen,'point_count':40,
       'normal_laplacian_gap_at_0':'5/6',
       'pseudoinverse_zero_mean':'Lplus=(21/20)I+(3/40)A',
       'dipole_A_cross':cross,
       'effective_resistance_matrix':[[str(v) for v in row] for row in R],
       'exact_low_band_quadratic_tensor':[[str(v) for v in row] for row in D],
       'isotropic_squared_wave_speed':'67/38400',
       'isotropic_dimensionless_wave_speed':c0,
       'wave_action':'Local real scalar action: S=integral dt [sum_v (partial_t phi_v)^2/2 - sum_(v,w)edge(phi_v-phi_w)^2/24]. EL equation d_t^2 phi + (I-A_cover/12) phi=0.',
       'small_k_numeric_controls':probes,
       'analytical_obstruction':'The lowest isolated eigenvalue is even analytic in k by H(-k)=H(k).conjugate, hence no nonanalytic or linear Dirac branch in the native spinless Laplacian eigenvalue. Scalar wave omega=sqrt(lambda0) has acoustic |k| from a freely chosen second-order action.',
       'scope':'Exact rational k^2 coefficient; selected 3 deck directions, kinetic action and speed normalization are external choices. Does not derive chirality, photons, Lorentz covariance or physical c. Repo earlier TOE36 already noted square-root wave propagation; new element is the exact rational metric and dipole-resistance derivation.'}
    (ROOT/'data/w33_20261102_exact_isotropic_3deck_scalar_wave.json').write_text(json.dumps(out,indent=2)+'\n')
    print('EXACT_ISOTROPY',json.dumps({'tensor':out['exact_low_band_quadratic_tensor'],'speed':c0,'max_error':max(abs(z['scalar_wave_speed_ratio']-1) for z in probes)}),flush=True)
    return out
if __name__=='__main__':main()
