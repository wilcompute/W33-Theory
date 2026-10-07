"""Independent tensor, invariant-ring, global-minimum and CP regressions."""
import itertools
import json
from pathlib import Path

import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parents[1]
D=json.loads((ROOT/'data/w33_pass11600_dynamical_hesse_flavor.json').read_text())


def test_bound_inputs_and_portable_source_digest():
    import hashlib
    for name,want in D['source_sha256'].items():
        p=ROOT/name
        raw=json.dumps(json.loads(p.read_text()),sort_keys=True,separators=(',',':')).encode() if p.suffix=='.json' else p.read_bytes().replace(b'\r\n',b'\n')
        assert hashlib.sha256(raw).hexdigest()==want
    raw=(ROOT/'analysis/w33_pass11600_dynamical_hesse_flavor.py').read_bytes().replace(b'\r\n',b'\n')
    assert hashlib.sha256(raw).hexdigest()==D['producer_sha256']


def native_tensor_basis():
    diagonal=np.zeros((3,3,3));off=np.zeros_like(diagonal)
    for i in range(3):diagonal[i,i,i]=1/np.sqrt(3)
    for t in itertools.permutations(range(3)):off[t]=1/np.sqrt(6)
    return np.column_stack([diagonal.ravel(),off.ravel()])


def test_native_unitary_tensor_action_and_invariant_interaction():
    B=native_tensor_basis();w=np.exp(2j*np.pi/3)
    F=np.array([[w**(i*j)/np.sqrt(3) for j in range(3)] for i in range(3)])
    R=np.array([[1,np.sqrt(2)],[np.sqrt(2),-1]])/np.sqrt(3)
    G=np.kron(np.kron(F,F),F)
    assert np.linalg.norm(G@B-B@R)<1e-12
    phi=B@np.array([1+2j,3-1j]);matter=np.arange(27)+1j*np.arange(27)[::-1]
    assert abs(np.vdot(G@phi,G@matter)-np.vdot(phi,matter))<1e-10


def test_entire_projective_parent_and_generalized_cp_stabilizers():
    B=native_tensor_basis();w=np.exp(2j*np.pi/3)
    F=np.array([[w**(i*j)/np.sqrt(3) for j in range(3)] for i in range(3)])
    generators=[np.roll(np.eye(3),1,axis=0),np.diag([1,w,w*w]),F,np.diag([1,1,w])]
    def key(g):
        a=g.ravel();v=a[np.flatnonzero(abs(a)>1e-8)[0]];a=a/(v/abs(v))
        return tuple(np.round(a.real,9))+tuple(np.round(a.imag,9))
    group={key(np.eye(3)):np.eye(3)};queue=[np.eye(3)]
    for g in queue:
        for h in generators:
            new=h@g;k=key(new)
            if k not in group:group[k]=new;queue.append(new)
        assert len(group)<=216
    assert len(group)==216
    r=np.array([-np.sqrt(6)/2,-1/np.sqrt(2),2*np.sqrt(3)])/np.sqrt(14)
    u=np.array([np.sqrt((1+r[2])/2),(r[0]+1j*r[1])/np.sqrt(2*(1+r[2]))])
    fixed=anti=0
    for g in group.values():
        R=B.conj().T@np.kron(np.kron(g,g),g)@B
        assert np.linalg.norm(R.conj().T@R-np.eye(2))<1e-12
        fixed+=abs(abs(np.vdot(u,R@u))-1)<1e-9
        anti+=abs(abs(np.vdot(u,R@u.conj()))-1)<1e-9
    assert fixed==18 and anti==0


def test_cp_even_invariant_ring_dimensions_through_seven():
    # Sign flips require three exponents all of the same parity; S3 then
    # identifies their permutations. This counts the invariant monomial orbits.
    counts=[]
    for degree in range(8):
        patterns={tuple(sorted(a)) for a in itertools.product(range(degree+1),repeat=3)
                  if sum(a)==degree and len({v%2 for v in a})==1}
        counts.append(len(patterns))
        generated=sum(2*a+3*b+4*c==degree for a,b,c in itertools.product(range(5),repeat=3))
        assert counts[-1]==generated
    assert counts==[1,0,1,1,2,1,3,2]


def test_low_order_obstruction_is_exact_not_sampled():
    i,j,a,b,c,d=s.symbols('i j a b c d',real=True)
    f=a*i+b*j+c*i*i+d*i*j
    assert s.hessian(f,[i,j]).det()==-d*d
    # d=0 removes the j dependence at any interior stationary point.
    assert s.diff(f.subs({d:0,b:0}),j)==0
    assert 'Holomorphic' in D['dynamics']['UV_boundary']


def test_all_global_minimum_rays_and_cp_orbit_pair():
    rays=[]
    for perm in itertools.permutations([1,2,3]):
        for signs in itertools.product([-1,1],repeat=3):
            if np.prod(signs)==1:rays.append(tuple(a*b for a,b in zip(perm,signs)))
    assert len(set(rays))==24
    W=lambda v:(v[0]**2-v[1]**2)*(v[1]**2-v[2]**2)*(v[2]**2-v[0]**2)
    assert sum(W(v)==120 for v in rays)==sum(W(v)==-120 for v in rays)==12
    for v in rays:
        assert sum(a*a for a in v)==14 and np.prod(v)==6 and sum(a**4 for a in v)==98
        assert W((v[0],v[2],v[1]))==-W(v)
    t=s.symbols('t')
    assert s.expand((t-1)*(t-4)*(t-9))==t**3-14*t**2+49*t-36


def test_stability_has_one_phase_zero_and_three_positive_directions():
    axes=np.array([[np.sqrt(2/3),-np.sqrt(1/6),-np.sqrt(1/6)],
                   [0,1/np.sqrt(2),-1/np.sqrt(2)],[1/np.sqrt(3)]*3])
    r=axes@np.array([1,2,3])/np.sqrt(14)
    u=np.array([np.sqrt((1+r[2])/2),(r[0]+1j*r[1])/np.sqrt(2*(1+r[2]))])
    base=np.array([u[0].real,u[0].imag,u[1].real,u[1].imag])
    def potential(v):
        a,b=v[0]+1j*v[1],v[2]+1j*v[3];rho=abs(a)**2+abs(b)**2
        bloch=np.array([2*(a.conjugate()*b).real,2*(a.conjugate()*b).imag,abs(a)**2-abs(b)**2])
        xyz=axes.T@bloch
        return (rho-1)**2+(np.prod(xyz)-3*rho**3/(7*np.sqrt(14)))**2+(sum(xyz**4)-rho**4/2)**2
    step=1e-4;eye=np.eye(4);H=np.empty((4,4))
    for i,j in itertools.product(range(4),repeat=2):
        vi,vj=step*eye[i],step*eye[j]
        H[i,j]=(potential(base+vi+vj)-potential(base+vi-vj)-potential(base-vi+vj)+potential(base-vi-vj))/(4*step**2)
    ev=np.linalg.eigvalsh(H)
    assert abs(potential(base))<1e-25 and abs(ev[0])<1e-5 and ev[1]>1e-3
    assert 'Goldstone' in D['dynamics']['phase_boundary']


def test_nonzero_physical_matrix_cp_witness_and_conjugate():
    b=-(np.sqrt(3)+1j)/(2*(np.sqrt(14)+2*np.sqrt(3)))
    Y=lambda h:np.array([[h[0],b*h[2],b*h[1]],[b*h[2],h[1],b*h[0]],[b*h[1],b*h[0],h[2]]])
    u,d=Y([1,2,4]),Y([3,1,2]);hu=u@u.conj().T;hd=d@d.conj().T;k=hu@hd-hd@hu
    cp=np.trace(k@k@k).imag
    assert abs(cp-D['CP_transfer']['numeric'])<1e-8
    k2=hu.conj()@hd.conj()-hd.conj()@hu.conj()
    assert abs(np.trace(k2@k2@k2).imag+cp)<1e-8


def test_canonical_angular_mass_hierarchy_and_its_scope():
    m=np.array([1,2,3])/np.sqrt(14);P=np.eye(3)-np.outer(m,m)
    g3=P@np.array([m[1]*m[2],m[0]*m[2],m[0]*m[1]]);g4=P@(4*m**3)
    # Divide both masses by v^2 (v/M)^8, with lambda3=lambda4=1.
    for ratio in [0.1,0.03]:
        H=4*(np.outer(g3,g3)+ratio**4*np.outer(g4,g4))
        ev=np.linalg.eigvalsh(H)
        assert abs(ev[-1]-181/343)<ratio**4*3
        assert abs(ev[1]/ratio**4-57600/62083)<ratio**4*3
    assert 'not fermion masses' in D['angular_masses']['boundary']
    assert 'not radiatively protected' in D['angular_masses']['boundary']
