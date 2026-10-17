"""Constrained theta/Barr compatibility; controls use full matrices, not PASS flags."""
import sys,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass12005_cp_real_theta_barr as p

def test_CP_real_theta_fit_and_conjugate_orientation():
    u,m,b,Ou,Od=p.bare_matrices();q,_,_,_=p.observables(u,m,b)
    assert max(abs(q[k]/p.DATA[k]-1) for k in p.DATA)<1e-7
    assert np.linalg.eigvalsh(Ou.imag)[0]>0 and np.linalg.eigvalsh(Od.imag)[0]>0
    qc=p.observables(u,m,b.conj())[0];q0=p.observables(u,m,np.zeros(3))[0]
    assert abs(qc['J']+q['J'])<1e-13 and abs(q0['J'])<1e-14
    assert abs(q0['ms_mb']/p.DATA['ms_mb']-1)>.1

def test_rank_one_defect_and_inverse_reconstruction():
    u,m,b,_,_=p.bare_matrices();q,V,sd,K=p.observables(u,m,b)
    H=m@K@m.T;C=np.eye(3)-np.linalg.solve(m,H)@np.linalg.inv(m.T)
    ev,W=np.linalg.eigh((C+C.conj().T)/2);assert max(abs(ev[:2]))<1e-8 and 0<ev[-1]<1
    c=W[:,-1]*np.sqrt(ev[-1]);br=c.conj()/np.sqrt(1-np.vdot(c,c).real)
    assert np.linalg.norm(p.observables(u,m,br)[3]-K)<1e-8
    # A target greater than bare m mT is forbidden for ANY one-row contraction.
    impossible=np.eye(3)-np.linalg.solve(m,2*m@m.T)@np.linalg.inv(m.T)
    assert max(np.linalg.eigvalsh(impossible))<-.99

def test_full_four_by_four_light_limit_and_determinant():
    u,m,b,_,_=p.bare_matrices();_,_,sd,_=p.observables(u,m,b);errors=[]
    for mu in [20.,200.]:
        M=np.zeros((4,4),complex);M[:3,:3]=m;M[3,:3]=mu*b;M[3,3]=mu
        sv=np.linalg.svd(M,compute_uv=False)[1:];errors.append(max(abs(sv/sd-1)))
        det=np.linalg.det(M);assert abs(det/(mu*np.linalg.det(m))-1)<1e-12
    assert errors[1]<errors[0]/50

def test_nonzero_upper_block_is_not_protected_by_fit():
    u,m,b,_,_=p.bare_matrices();M=np.zeros((4,4),complex);M[:3,:3]=m;M[3,:3]=b;M[3,3]=1
    direction=np.array([.2,-.3,.1]);slope=-(b@np.linalg.solve(m,direction)).imag
    M[:3,3]=1e-9*direction
    assert abs(np.angle(np.linalg.det(M))/1e-9-slope)<1e-3*max(1,abs(slope))
    assert abs(slope)>1

def test_frozen_witness_is_recomputed_not_free_real_inverse():
    d=json.loads((ROOT/'data/w33_pass12005_cp_real_theta_barr.json').read_text());u,m,b,_,_=p.bare_matrices()
    assert np.max(abs(m-np.array(d['real_bare_down'])))<1e-12
    assert d['finite_heavy_scale_controls'][-1]['max_relative_spectrum_error']<1e-7
    assert d['max_relative_comparator_error']<1e-7
