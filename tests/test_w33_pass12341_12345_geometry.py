"""Independent finite-character and exact Laurent checks for the cover."""
from itertools import product
from pathlib import Path
import json,sys
import numpy as np
import sympy as sp
from scipy.optimize import root
from scipy.linalg import svdvals

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass12341_12345_geometry as core
import w33_20261028_three_mixed_loop_minimal_maxwell as original
import w33_20261027_native_bloch_face_module as native


def modular_rank(rows,p):
    a=np.asarray(rows,dtype=np.int64)%p;r=0
    for col in range(a.shape[1]):
        choices=np.flatnonzero(a[r:,col])
        if len(choices)==0:continue
        selected=r+int(choices[0]);a[[r,selected]]=a[[selected,r]]
        a[r]=(a[r]*pow(int(a[r,col]),-1,p))%p
        chosen=np.flatnonzero(a[r+1:,col])+r+1
        a[chosen]=(a[chosen]-a[chosen,col,None]*a[r])%p
        r+=1
        if r==a.shape[0]:break
    return r


def test_replay_global_unit_minors():
    data=core.symbol_certificate()
    assert data['short_global_unit_minor']['power']==[-12,2,18,-15]
    assert data['short_global_unit_minor']['sign']==-1
    assert data['augmented_global_unit_minor']['power']==[-14,2,20,-18]
    assert data['augmented_global_unit_minor']['sign']==1
    assert len(data['augmented_global_unit_minor']['pivot_witness'])==109
    assert data['two_by_two_minors_projective_groebner']==['1']*4
    assert data['zero_free_angle_bound']['coefficient']=='3051/7360'


def test_all_period_three_characters_against_actual_bloch_matrices():
    _,V,_,_,_=original.geometry()
    faces=json.loads((ROOT/'data/PART_20261023_NATIVE_ZERO_HOLONOMY_FACE_COMPLETION.json').read_text())['independent_face_basis']
    loops=json.loads((ROOT/'data/w33_20261027_native_bloch_face_module.json').read_text())['commutator_boundaries']
    R=np.array(core.R,dtype=int);p=109
    omega=pow(int(sp.primitive_root(p)),(p-1)//3,p)
    assert omega!=1 and pow(omega,3,p)==1
    known={tuple(v) for v in core.symbol_certificate()['third_root_nonidentity_zeros']}
    for label in product(range(3),repeat=4):
        z=[pow(omega,e,p) for e in label]
        short=np.array([original.bloch_row(f['boundary'],V,z,p) for f in faces])
        six=np.array([original.bloch_row(f,V,z,p) for f in loops])
        assert modular_rank(short,p)==105
        mixed=modular_rank(np.vstack((short,R@six%p)),p)
        full=modular_rank(np.vstack((short,six)),p)
        assert full==(105 if not any(label) else 108)
        assert mixed==(105 if not any(label) else (107 if label in known else 108))


def test_nearby_real_torus_points_have_the_predicted_rank_drop():
    data=core.symbol_certificate();W=np.array(data['period_matrix'],float)
    N=np.array(data['N'],float);inv=np.linalg.inv(W)
    _,V,edges,*_=native.geometry()
    faces=json.loads((ROOT/'data/PART_20261023_NATIVE_ZERO_HOLONOMY_FACE_COMPLETION.json').read_text())['independent_face_basis']
    six=json.loads((ROOT/'data/w33_20261027_native_bloch_face_module.json').read_text())['commutator_boundaries']
    for a,b in ((.01,0.),(-.015,.007),(.02,-.01)):
        def f(x):
            theta=np.array([x[0],x[1],a,b]);d=np.exp(1j*theta)-1
            q=d@N@d
            return [q.real,q.imag]
        sol=root(f,[2*np.pi/3,-2*np.pi/3],tol=1e-12)
        assert np.linalg.norm(f(sol.x))<1e-10
        k=inv@np.array([*sol.x,a,b]);Fs=native.curl([x['boundary'] for x in faces],V,k)
        Fl=native.curl(six,V,k)
        assert svdvals(np.vstack((Fs,np.array(core.R,float)@Fl)))[-1]<1e-11
        assert svdvals(np.vstack((Fs,Fl)))[-4]>1e-4


def test_reflection_constraints_remove_the_tested_fixed_character_mode():
    r=core.reflection_certificate()
    assert r['full_unprojected_nongauge_nullity']==1
    assert [r['parity_constraints'][str(i)]['surviving_nongauge_nullity'] for i in (1,-1)]==[0,0]
    assert r['exact_reflection_square_and_gauge_intertwining']
