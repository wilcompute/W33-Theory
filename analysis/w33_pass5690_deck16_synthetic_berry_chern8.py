#!/usr/bin/env python3
"""Pass5690 bonkers: Berry topology of the normalized deck16 multiplicity sphere.

Pass5675 identifies the equivariant K-odd cone with Herm_2. Remove the scalar part
and normalize the traceless part:

    X(n)=n_x sigma_x+n_y sigma_y+n_z sigma_z,  n in S^2.

With the projector-curvature convention used below, the negative/positive eigenlines
have Chern numbers +1/-1. The full deck16 normal form is

    H(n)=I_A tensor X(n)  direct-sum  I_Abar tensor[-conj X(n)].

Complex conjugation sends n to Rn=(n_x,-n_y,n_z), an orientation-reversing map of
S^2. The negative-energy bundle is

    E_- = A tensor L_-  +  Abar tensor R^* L_+,

with dim A=4. Hence

    c1(E_-)=4(+1)+4(deg R)(-1)=+8.

The sign depends on the orientation/Berry-curvature convention; |c1|=8 is invariant.
This is a SYNTHETIC parameter-space invariant of the family of allowed finite
Hamiltonians. It is not a momentum-space Chern number and not a particle count.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5690_DECK16_SYNTHETIC_BERRY_CHERN8.json'

def main():
    sx=np.array([[0,1],[1,0]],complex);sy=np.array([[0,-1j],[1j,0]],complex);sz=np.array([[1,0],[0,-1]],complex);I=np.eye(2)
    nt=400;theta=(np.arange(nt)+0.5)*math.pi/nt;dth=math.pi/nt
    integ=0.0
    for th in theta:
        n=np.array([math.sin(th),0,math.cos(th)])
        dn_th=np.array([math.cos(th),0,-math.sin(th)])
        dn_ph=np.array([0,math.sin(th),0])
        P=(I-(n[0]*sx+n[1]*sy+n[2]*sz))/2
        Pt=-(dn_th[0]*sx+dn_th[1]*sy+dn_th[2]*sz)/2
        Pp=-(dn_ph[0]*sx+dn_ph[1]*sy+dn_ph[2]*sz)/2
        F=float(np.real(1j*np.trace(P@(Pt@Pp-Pp@Pt))))
        integ+=F*dth*2*math.pi
    c_lower=integ/(2*math.pi)
    assert abs(c_lower-1)<2e-5
    c_upper=-c_lower
    deg_R=-1;mult=4
    total=mult*(+1)+mult*deg_R*(-1)
    assert total==8
    out={
      'pass':5690,'status':'DECK16_TRACELESS_HERM2_MODULI_SPHERE_HAS_SYNTHETIC_OCCUPIED_CHERN_MAGNITUDE8',
      'parameter_space':'normalized traceless Herm_2 = S^2 via X=n.sigma',
      'line_bundles':{'c1_L_plus':-1,'c1_L_minus':1,'numeric_c1_L_minus':c_lower,'orientation_convention':'sign flips if sphere/Berry orientation is reversed'},
      'particle_hole_conjugation':'conj X(n)=X(Rn), R(nx,ny,nz)=(nx,-ny,nz), degree(R)=-1',
      'negative_bundle':'E_-=A tensor L_- direct-sum Abar tensor R^*L_+, dim A=4',
      'first_chern_number_in_this_convention':total,'absolute_chern_number':abs(total),
      'interpretation':'The magnitude eight comes from two fourfold carrier blocks carrying the same oriented negative-band Berry charge after the conjugation reflection.',
      'boundary':'This is Berry topology over a synthetic Hamiltonian-moduli sphere. It is not a Brillouin-zone invariant, does not imply a 2D topological material phase, and is not evidence for eight particles or eight gauge bosons.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
