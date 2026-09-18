#!/usr/bin/env python3
"""Exact W(3,3) Laplacian spectral-echo physics primitive.

For the W33 collinearity graph A with spectrum
  12^1, 2^24, (-4)^15,
the graph Laplacian L=12I-A has spectrum
  0^1, 10^24, 16^15.

If an engineered photonic/synthetic-dimension Hamiltonian is H=hbar*g*L, then
at dimensionless time gt=pi/2:
  exp(-i gt L) = +1 on lambda=0,
                   -1 on lambda=10,
                   +1 on lambda=16.
Thus the evolution is the exact reflection
  R10 = I - 2 P10
      = I - L(16I-L)/30
      = (A^2 - 8A - 18I)/30.

At gt=pi the entire 40-mode system revives exactly because gcd(10,16)=2.
This gives a clean laboratory signature of a correctly implemented W33
kinetic operator: a half-revival parity flip on exactly the 24-dimensional
restricted-eigenvalue sector, followed by full revival at pi.

This is engineered-device physics, not a claim about vacuum photon dynamics.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_laplacian_spectral_echo.json'

def phase_int(lam,numer,denom):
    # phase at t=pi*numer/denom represented by exponent lam*numer/denom mod 2
    from fractions import Fraction
    x=Fraction(lam*numer,denom)
    # e^{-i pi x}; for integer x parity determines +/-1
    return x
def main(write=True):
    spec={0:1,10:24,16:15}
    half={lam:phase_int(lam,1,2) for lam in spec}
    assert half[0].denominator==half[10].denominator==half[16].denominator==1
    signs={lam:(1 if int(x)%2==0 else -1) for lam,x in half.items()}
    assert signs=={0:1,10:-1,16:1}
    full={lam:phase_int(lam,1,1) for lam in spec}
    assert all(int(x)%2==0 for x in full.values())
    out={'schema':'w33.laplacian_spectral_echo.v1','status':'PASS_EXACT_ENGINEERED_SPECTRAL_PRIMITIVE',
      'graph':'W(3,3) collinearity SRG(40,12,2,4)',
      'adjacency_spectrum':{'12':1,'2':24,'-4':15},
      'laplacian_spectrum':{'0':1,'10':24,'16':15},
      'half_echo':{
        'dimensionless_time_gt':'pi/2',
        'sector_phases':{'lambda0':1,'lambda10':-1,'lambda16':1},
        'operator':'R10=I-2P10=I-L(16I-L)/30=(A^2-8A-18I)/30',
        'flipped_dimension':24},
      'full_revival':{'dimensionless_time_gt':'pi','operator':'I_40'},
      'experimental_signature':'prepare a lambda=10 eigenmode and a lambda=16 control mode; at gt=pi/2 their relative phase is pi, while at gt=pi both revive',
      'physics_boundary':'Requires an engineered Hamiltonian proportional to the W33 Laplacian; no vacuum-propagation claim is made.',
      'checks':{'half_echo_exact':True,'full_revival_exact':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
