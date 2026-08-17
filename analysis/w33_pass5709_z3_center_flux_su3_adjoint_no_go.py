#!/usr/bin/env python3
"""Pass5709 bonkers: can the old constant Z3 curvature be SU(3) center flux?

Abstractly yes: Z(SU3)={1,omega I,omega^2 I}. The AG(2,3) connection's oriented
plaquette curvature h=-det(d1,d2) mod3 is always 1 or 2 for independent direction
pairs, so it can be mapped to a nontrivial center Wilson loop.

But the new affine su3 from Pass5686 is presently realized only in the adjoint.
Every center element acts trivially by conjugation on su3. Hence a center-flux
plaquette has fundamental Wilson trace 3 omega^h but adjoint Wilson trace 8 and
identity adjoint holonomy. The old Z3 curvature therefore cannot be recovered from
or detected by the new adjoint transporter alone. A triality-nonzero/fundamental
matter representation is additional structure.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5709_Z3_CENTER_FLUX_SU3_ADJOINT_NOGO.json'
DIRS=[(1,0),(0,1),(1,1),(1,2)]

def det(a,b):return (a[0]*b[1]-a[1]*b[0])%3

def main():
    hist=Counter()
    for a,b in itertools.combinations(DIRS,2):
      d=det(a,b);assert d in (1,2)
      h=(-d)%3;assert h in (1,2)
      hist[h]+=9 # same curvature at all nine affine sites
    assert sum(hist.values())==54
    w=np.exp(2j*np.pi/3)
    center={h:(w**h)*np.eye(3) for h in (0,1,2)}
    assert all(abs(np.linalg.det(U)-1)<1e-8 for U in center.values())
    # Ad_z(X)=zXz^-1=X for any traceless matrix. Verify on a spanning set.
    E=[]
    for i in range(3):
      for j in range(3):
        if i!=j:
          X=np.zeros((3,3),complex);X[i,j]=1;E.append(X)
    E += [np.diag([1,-1,0]).astype(complex),np.diag([0,1,-1]).astype(complex)]
    residual={}
    for h,U in center.items():
      Ui=np.linalg.inv(U);res=max(np.linalg.norm(U@X@Ui-X) for X in E);residual[h]=float(res);assert res<1e-10
    ftr={h:[float((3*(w**h)).real),float((3*(w**h)).imag)] for h in (0,1,2)}
    out={
      'pass':5709,'status':'OLD_Z3_CURVATURE_CAN_BE_EMBEDDED_AS_SU3_CENTER_FLUX_BUT_IS_INVISIBLE_TO_AFFINE_ADJOINT_TRANSPORT',
      'affine_curvature':{'law':'h=-det(d1,d2) mod3','oriented_plaquettes':54,'histogram':{str(k):v for k,v in sorted(hist.items())}},
      'center_embedding':'h -> omega^h I3 in Z(SU3)',
      'fundamental_Wilson_trace_ReIm':{str(k):v for k,v in ftr.items()},
      'adjoint_action_residuals':{str(k):v for k,v in residual.items()},
      'adjoint_Wilson_trace':{'0':8,'1':8,'2':8},
      'theorem':'Center-valued flux is completely invisible in the adjoint because Ad(SU3) has kernel Z3. Thus Pass5691 adjoint-triviality of the vertical Z3 is exactly what SU3 center flux would predict, but it does not by itself identify the old connection with QCD color.',
      'missing_structure':'To observe h=1 versus h=2 one needs a representation of nonzero triality (for example a fundamental 3 or anti-3) and an explicit intertwiner tying that representation to the E6/81 matter carrier.',
      'physics_boundary':'This is an abstract center embedding and Wilson-character statement, not a derivation of color flux, quarks, confinement, or a physical gauge coupling.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
