"""Compile native period cycles and put a unitary history on the selected clock.

The reversible update law and coin are supplied. Lorentz principal dispersion
follows from conditional unitarity, not from negating a diffusion eigenvalue.
"""
import json,itertools
from pathlib import Path
import numpy as np
import sympy as s
from scipy.linalg import expm
from w33_pass11991_native_four_period_cover import native_geometry,gamma4
ROOT=Path(__file__).resolve().parents[1]


def native_paths():
    old=json.loads((ROOT/'data/w33_pass11991_native_four_period_cover.json').read_text());V=np.array(old['primitive_integer_edge_voltages'],int)
    H,edges,*_=native_geometry();paths={0:[]};queue=[0];tree=[]
    for a in queue:
        for e,(u,v) in enumerate(edges):
            if V[e].any():continue
            if u==a and v not in paths:paths[v]=paths[a]+[(e,1)];queue.append(v);tree.append(e)
            if v==a and u not in paths:paths[u]=paths[a]+[(e,-1)];queue.append(u);tree.append(e)
    assert len(paths)==27 and len(tree)==26
    reverse=lambda p:[(e,-sign) for e,sign in reversed(p)]
    cycles=[]
    for j in range(4):
        e=next(e for e,v in enumerate(V) if np.array_equal(v,np.eye(4,dtype=int)[j]));a,b=edges[e]
        word=paths[a]+[(e,1)]+reverse(paths[b]);assert np.array_equal(sum((sign*V[e] for e,sign in word),np.zeros(4,int)),np.eye(4,dtype=int)[j]);cycles.append(word)
    # The first column advances the actual ordered clock by exactly1.
    clock=np.array([3,0,2,1]);T=s.Matrix([[0,1,0,0],[0,0,1,0],[0,0,0,1],[1,-3,0,-2]])
    assert abs(T.det())==1 and s.Matrix([list(clock)])*T==s.Matrix([[1,0,0,0]])
    def compile_period(period):
        out=[]
        for j,n in enumerate(period):
            for _ in range(abs(int(n))):out+=cycles[j] if n>0 else reverse(cycles[j])
        return out
    words=[compile_period(T[:,j]) for j in range(4)]
    for j,word in enumerate(words):
        a=0;vol=np.zeros(4,int)
        for e,sign in word:
            x,y=edges[e];assert a==(x if sign>0 else y);a=y if sign>0 else x;vol+=sign*V[e]
        assert a==0 and np.array_equal(vol,np.array(T[:,j],int).ravel())
    return edges,V,paths,tree,T,words


def update(k,mass=0.):
    gamma,_=gamma4();U=expm(-1j*mass*gamma[3])
    for j in range(3):U=U@expm(-1j*k[j]*gamma[j])
    assert np.max(abs(U.conj().T@U-np.eye(4)))<1e-12
    return U


def payload():
    edges,V,paths,tree,T,words=native_paths();gamma,_=gamma4();rows=[]
    direction=np.array([.2,-.3,.4]);mass=.35;target=np.sqrt(mass**2+np.dot(direction,direction))
    for a in [.04,.02,.01,.005]:
        U=update(a*direction,a*mass);energy=np.sort(abs(np.angle(np.linalg.eigvals(U))))/a
        rows.append(dict(spacing=a,positive_quasienergy_magnitudes=energy.tolist(),continuum_target=float(target),maximum_error=float(max(abs(energy-target)))))
    assert rows[-1]['maximum_error']<rows[0]['maximum_error']/3
    # Exact Clifford identity proves the Lorentz principal polynomial.
    X=s.Matrix([[0,1],[1,0]]);Y=s.Matrix([[0,-s.I],[s.I,0]]);Z=s.diag(1,-1)
    alpha=[s.kronecker_product(X,X),s.kronecker_product(X,Y),s.kronecker_product(X,Z)];beta=s.kronecker_product(Z,s.eye(2))
    k=s.symbols('k0:3',real=True);m,omega=s.symbols('m omega',real=True)
    h=m*beta+sum((q*a for q,a in zip(k,alpha)),s.zeros(4));assert s.expand(h*h-(m*m+sum(q*q for q in k))*s.eye(4))==s.zeros(4)
    det=s.factor((omega*s.eye(4)-h).det());assert s.expand(det-(omega*omega-m*m-sum(q*q for q in k))**2)==0
    corners=[]
    for bits in itertools.product([0,1],repeat=3):
        U=update(np.pi*np.array(bits));zero=np.linalg.norm(U-np.eye(4))<1e-10
        corners.append(dict(bits=list(bits),zero_quasienergy_node=bool(zero)))
    assert sum(r['zero_quasienergy_node'] for r in corners)==4
    return dict(status='PASS',clock_covector_primitive=[3,0,2,1],unimodular_period_matrix=T.tolist(),zero_voltage_tree_edges=tree,
        root_to_vertex_paths={str(a):p for a,p in paths.items()},native_period_closed_paths=words,
        maximal_period_word_length=max(map(len,words)),
        exact_principal_determinant=str(det),continuum_refinement=rows,Brillouin_corner_nodes=corners,
        microscopic_process='Fourcoin amplitudes per nativeaddress and spatialdeckcell. Each conditional shift is e^-ik_j alpha_j, realizable by diagonalizingalpha_j and traversing a compilednativeperiod path or itsreverse. Onsite coin e^-im beta. ClockperiodT0 is an actual integraldeckcycle; impose psi(t+1)=U psi(t).',
        positive_history_operator='C=S_clock-U; H_history=C^dag C>=0. Fourier zero modes obey e^iomega psi=U(k)psi. The leading differential equation has det(omega-H_D)=(omega²-|k|²-m²)²; the negative spatial/time relative sign follows from the supplied reversible unitary clock law.',
        boundary='Actualnativecycles and a supplied causal/coined history process. No selection of thisupdate fromtheW33action, exactfinite-spacingLorentzsymmetry, gravity, uniquevelocity orphysicaltime. Fourzero-quasienergycornernodes demonstrate doubling; no chiralSMor threefamilies is inferred.',
        prior=['11991 primitive connectednativefourperiodcover','11994 nativeclockorder','11995 clockmetricalignment','11610 nativeCliffordmass and JackiwRebbi repair','priorHolonet history/VM constructions'],
        primary=['https://arxiv.org/abs/1307.3524'])

if __name__=='__main__':
    d=payload();(ROOT/'data/w33_pass12000_native_unitary_clock.json').write_text(json.dumps(d,indent=2,default=int)+'\n');print(d['status'],d['maximal_period_word_length'])
