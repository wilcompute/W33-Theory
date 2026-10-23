#!/usr/bin/env python3
"""The full S4 physical 4-rail permutation group acts on the 3D Walsh qutrit.

Normal Klein V4 XOR bus -> diagonal sign gates.
Order-3 rail permutation (1->2->3->1, 0 fixed) -> exact qutrit X3.
F3 X3 F3^dagger -> qutrit Z3, with the selected Fourier convention.
The three-cycle is NOT available on the existing XOR-only 4-MZI controller:
it requires an additional rail permutation / network, not a relabel-only lie.
"""
from __future__ import annotations
import hashlib,itertools,json,math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_walsh_qutrit_metaplectic_noise_20261023 import code_basis
from w33_fractal_linebus_switch_matrix_20261023 import permutation_matrix

def four_rail_perm(sigma):
    if tuple(sorted(sigma))!=(0,1,2,3):raise ValueError("must permute 0..3")
    P=np.zeros((4,4),float)
    for initial,final in enumerate(sigma):
        P[final,initial]=1
    return P

def result():
    V,aux=code_basis()
    reps=[]
    images=set()
    for sigma in itertools.permutations(range(4)):
        P=four_rail_perm(sigma)
        L=V.conj().T@P@V
        err=float(np.linalg.norm(P@V-V@L))
        assert err<1e-12
        assert np.linalg.norm(L.conj().T@L-np.eye(3))<1e-12
        assert np.linalg.norm(P@aux-aux)<1e-12
        # These signed permutation matrices form the 3D octahedral
        # representation of S4 in the nontrivial Walsh character basis.
        assert np.linalg.norm(np.abs(L).sum(axis=0)-1)<1e-12
        assert np.linalg.norm(np.abs(L).sum(axis=1)-1)<1e-12
        A=np.rint(L.real).astype(int)
        images.add(tuple(int(x) for x in A.flatten()))
        reps.append({'physical_permutation':list(sigma),
                     'logical_signed_permutation':A.tolist(),
                     'code_leakage_residual':err,
                     'determinant':int(round(np.linalg.det(P)))})
    assert len(reps)==len(images)==24
    # This is a 3-cycle of nonzero physical rail labels, fixing port 0.
    three_cycle=[0,2,3,1]
    G=four_rail_perm(three_cycle)
    X=V.conj().T@G@V
    shift=np.zeros((3,3))
    for initial,final in enumerate((2,0,1)):
        shift[final,initial]=1
    assert np.linalg.norm(X-shift)<1e-12
    assert np.linalg.norm(X@X@X-np.eye(3))<1e-12
    assert all(np.linalg.norm(X-permutation_matrix(k)[:3,:3])>1 for k in (1,2,3))
    w=np.exp(2j*math.pi/3)
    F=np.array([[w**(i*j) for j in range(3)] for i in range(3)],complex)/math.sqrt(3)
    Z=F@X@F.conj().T
    assert np.linalg.norm(Z-np.diag([1,w*w,w]))<1e-12
    out={'schema':'w33.walsh.qutrit.s4_physical_rail_bridge.v1',
       'carrier':'one four-rail Walsh qutrit, coherent 4-mode single-photon Hilbert space',
       'physical_rail_permutation_count':len(reps),
       'logical_sign_permutation_count':len(images),
       'all_permutations_preserve_qutrit':True,
       'three_cycle_rail_permutation':three_cycle,
       'three_cycle_logical_X3':np.rint(X.real).astype(int).tolist(),
       'three_cycle_order':3,
       'Z3_F3_conjugate_real':Z.real.tolist(),
       'Z3_F3_conjugate_imag':Z.imag.tolist(),
       'nonzero_induced_logical_generators':{
           'XOR_V4':'diagonal signed metaplectic-reflection class',
           'rail_3cycle':'qutrit cyclic shift X3',
           'Fourier_3':'needed to construct Z3 by conjugating X3'},
       'group_theory':'S4 on 4 physical rails has a 3D standard real representation on the nontrivial Walsh characters. V4 normal; 3-cycle extends V4 to A4.',
       'engineering_boundary':['existing XOR four-state bus cannot execute rail 3-cycle',
         '3-cycle requires at least two ordinary transpositions in a 4-rail permutation-only realization',
         'routing waveguides and state preparation must be coherent and synchronized',
         'Clifford+R is prior-art; no novel quantum gate species, dense-gate proof or two-qutrit entangler implied'],
       'permutation_table':reps}
    obj=json.dumps(out,sort_keys=True,separators=(',',':'))
    out['sha256']=hashlib.sha256(obj.encode()).hexdigest()
    return out
if __name__=='__main__':
    o=result()
    path=ROOT/'data/w33_walsh_qutrit_s4_affine_bridge_20261023.json'
    path.write_text(json.dumps(o,sort_keys=True,indent=2)+'\n')
    print('PASS',o['physical_rail_permutation_count'],o['three_cycle_logical_X3'],o['sha256'])
