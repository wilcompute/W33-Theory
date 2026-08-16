#!/usr/bin/env python3
"""Pass5617: turn the repo's constant AG(2,3) Z3 curvature into magnetic bands.

The existing E6/firewall connection scripts derive an AG(2,3) connection whose
plaquette holonomy is F(d1,d2)=-det(d1,d2) mod 3.  This pass packages the exact
physics consequence: magnetic translations obey the qutrit Heisenberg relation,
and the minimal Harper operator has a three-band exact spectrum.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5617_Z3_GAUGE_HARPER.json'

def det(a,b): return (a[0]*b[1]-a[1]*b[0])%3

def main():
    dirs=[(1,0),(0,1),(1,1),(1,2)]
    hist=Counter()
    for a,b in itertools.combinations(dirs,2):
        d=det(a,b);assert d!=0
        F=(-d)%3
        hist[F]+=9 # one identical-curvature plaquette at each of 9 AG(2,3) points
    assert hist==Counter({1:27,2:27})
    # Wilson convention S=sum_p (1-Re omega^F_p).
    wilson=sum(n*(1-math.cos(2*math.pi*k/3)) for k,n in hist.items())
    assert abs(wilson-81)<1e-10

    w=np.exp(2j*np.pi/3)
    X=np.array([[0,0,1],[1,0,0],[0,1,0]],complex)
    Z=np.diag([1,w,w*w])
    # With these conventions ZX=omega XZ.
    assert np.allclose(Z@X,w*(X@Z))
    H=X+X.conj().T+Z+Z.conj().T
    ev=np.linalg.eigvalsh(H)
    want=np.array([-2,1-math.sqrt(3),1+math.sqrt(3)])
    assert np.max(np.abs(ev-want))<1e-10

    out={'pass':5617,'status':'CONSTANT_Z3_GAUGE_CURVATURE_TO_QUTRIT_HARPER_BANDS',
         'source_geometry':'the existing E6/firewall quotient gives AG(2,3) and a fitted Z3 connection; toe_affine_plane_z3_holonomy.py verifies F(d1,d2)=-det(d1,d2)',
         'plaquette_curvature_histogram':{str(k):v for k,v in sorted(hist.items())},
         'all_54_oriented_direction_class_plaquettes_nonzero':True,
         'wilson_action_convention':'sum over 54 point/direction-pair plaquettes of (1-Re omega^F)',
         'wilson_action':wilson,
         'magnetic_translation_relation':'Z X = omega X Z',
         'minimal_harper_operator':'H=X+X^dagger+Z+Z^dagger',
         'harper_spectrum':[float(x) for x in ev],
         'exact_harper_spectrum':['-2','1-sqrt(3)','1+sqrt(3)'],
         'physics_firewall':'This is an exact finite Z3 lattice-gauge/Harper sector. The Wilson normalization is a declared convention; it is not yet continuum Yang-Mills, a measured gauge coupling, or a Standard-Model gauge identification.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
