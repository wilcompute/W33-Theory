"""SU3 gauge invariant Welch frame potential: selects a qutrit SIC but
cannot isolate a unique H27 geometry or generate a full quadratic mass gap.
The universal Welch bound and qutrit SIC continuous family are prior art.
"""
from pathlib import Path
import json,itertools
import numpy as np
from numpy.linalg import norm
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/toe_20261119_SIC_Welch_moduli_obstruction.json'
O=np.exp(2j*np.pi/3)
X=np.roll(np.eye(3),1,axis=0)
Z=np.diag([1,O,O**2])

def orbit(t):
    fid=np.array([0.,1.,-np.exp(1j*t)],complex)/np.sqrt(2)
    return np.array([np.linalg.matrix_power(X,b)@np.linalg.matrix_power(Z,a)@fid
             for b in range(3) for a in range(3)])

def FP2(v):
    g=np.abs(v.conj()@v.T)**2
    return float(np.sum(g*g))

def A(v):
    w=np.einsum('ni,nj->nij',v,v).reshape(9,9)
    return w.conj().T@w

def tangent_basis(u):
    trial=np.eye(3,dtype=complex)
    proj=np.eye(3)-np.outer(u,u.conj())
    vv=[]
    for i in range(3):
        w=proj@trial[:,i]
        for b in vv:w-=np.vdot(b,w)*b
        if norm(w)>1e-8:vv.append(w/norm(w))
    assert len(vv)==2
    return vv

def local_chart(v):
    # Projective manifold (CP²)^9 has 9*4 =36 real coordinates.
    # First-order derivative of A=sum_i |psi_i psi_i><psi_i psi_i|
    # under tangent vectors. At a 2-design minimum FP2-13.5=||A-1.5 P_sym||²
    # so Hessian =2 J†J, and null vectors are J's nullspace.
    V=np.array([tangent_basis(u) for u in v])
    J=[]
    def DAt(i,d):
        u=v[i]
        f=np.kron(u,u)
        df=np.kron(u,d)+np.kron(d,u)
        return np.outer(df,f.conj())+np.outer(f,df.conj())
    for i in range(9):
        for k in range(2):
            J.append(DAt(i,V[i,k]));J.append(DAt(i,1j*V[i,k]))
    J=np.stack([z.reshape(81) for z in J],axis=1)
    sv=np.linalg.svd(J,compute_uv=False)
    rank=int(np.count_nonzero(sv>1e-7))
    assert rank==26 and len(sv)-rank==10
    # Eight global SU3 orbit directions are genuine Hessian zeros. Generate
    # traceless Hermitian matrices and verify J vanishes on their tangents.
    generators=[]
    for i in range(3):
        for j in range(i+1,3):
            a=np.zeros((3,3),complex);a[i,j]=a[j,i]=1
            generators.append(a)
            b=np.zeros((3,3),complex);b[i,j]=-1j;b[j,i]=1j
            generators.append(b)
    generators.append(np.diag([1.,-1.,0.]));generators.append(np.diag([1.,1.,-2.]))
    tangent=[]
    for H in generators:
        coeff=[]
        for i,u in enumerate(v):
            d=1j*H@u
            coeff.extend([z for w in V[i] for z in (np.vdot(w,d).real,np.vdot(w,d).imag)])
        tangent.append(coeff)
    T=np.array(tangent).T
    assert np.linalg.matrix_rank(T,tol=1e-8)==8
    maxg=float(np.max(np.abs(J@T)))
    assert maxg<1e-12
    # An explicit ninth independent projective zero direction is the
    # Hesse 1-parameter family. The tenth infinitesimal zero may be
    # obstructed at higher order; no 2-parameter family is claimed.
    dt=1e-6
    d=(orbit(.23+dt)-orbit(.23-dt))/(2*dt)
    coeff=[]
    for i,u in enumerate(v):
        for w in V[i]:
            c=np.vdot(w,d[i]);coeff.extend([c.real,c.imag])
    C=np.column_stack([T,np.array(coeff)])
    assert np.linalg.matrix_rank(C,tol=1e-8)==9
    familyres=float(np.linalg.norm(J@np.array(coeff)))
    assert familyres<1e-7
    return {'projective_real_tangent_dimension':36,
        'design_constraint_jacobian_rank':rank,
        'frame_potential_quadratic_zero_directions':len(sv)-rank,
        'global_SU3_zero_directions':8,
        'one_explicit_additional_Hesse_modulus':True,
        'extra_unexplained_infinitesimal_zero_direction':1,
        'smallest_nonzero_jacobian_singular_value':float(sv[rank-1]),
        'largest_null_singular_value':float(sv[rank]),
        'max_SU3_gauge_tangent_design_variation':maxg,
        'Hesse_family_tangent_design_variation':familyres}

def run():
    samples=[]
    for t in [0.,.23,.59,1.11]:
        v=orbit(t)
        eig=np.linalg.eigvalsh(A(v))
        P=v.T@v.conj()
        tr=np.vdot(v[0],v[3])*np.vdot(v[3],v[6])*np.vdot(v[6],v[0])
        assert abs(FP2(v)-13.5)<1e-11
        assert np.linalg.norm(P-3*np.eye(3))<1e-12
        assert abs(tr+np.exp(-3j*t)/8)<1e-12
        assert np.max(abs(np.sort(eig)[3:]-1.5))<1e-12
        samples.append({'t':t,'Welch_frame_potential':FP2(v),
              'bargmann_triangle_036':[float(tr.real),float(tr.imag)],
              'gauge_D_moment_map_residual':float(np.linalg.norm(P-3*np.eye(3)))})
    assert abs(samples[0]['bargmann_triangle_036'][0]-samples[1]['bargmann_triangle_036'][0])>.01
    mub=np.array([np.array([1,O**a,O**b],complex)/np.sqrt(3) for a,b in itertools.product(range(3),repeat=2)])
    assert abs(FP2(mub)-15)<1e-12
    res=local_chart(orbit(.23))
    out={'status':'PASS_WELCH_SIC_ALIGNMENT_WITH_RESIDUAL_MODULI',
      'global_bound_for_9_unit_qutrits':'FP2>=9^2/[3(3+1)/2]=13.5',
      'frame_potential_equals_tr_A_squared':True,
      'SIC_saturates_2_design_global_minimum':True,
      'SIC_samples':samples,'three_MUB_frames_potential':FP2(mub),
      'SIC_vs_three_MUB_gap':FP2(mub)-13.5,
      'Hesse_bargmann_invariant':'Tr(P0 P3 P6)=-exp(-3i t)/8 (labeled), varies while FP2 stays minimum',
      'quadratic_moduli':res,
      'physical_caveat':'A nonholomorphic higher-order gauge-invariant bosonic potential can select SIC over MUB at fixed norm, but individual species phases and a continuous Hesse family survive, so no isolated supersymmetric mass spectrum follows. Earlier repo already built explicit SU3-invariant alignment and Hesse baryon separator.',
      'related_prior_repo':'analysis/2026-11-19_SIC_SU3_Plucker_Hesse_baryon_selector.md',
      'literature':'Welch frame potential and qutrit SIC 2-design are established mathematics.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2)+'\n')
    print('SIC WELCH',13.5,'MUB',FP2(mub),'J RANK',res['design_constraint_jacobian_rank'])
    return out
if __name__=='__main__':run()
