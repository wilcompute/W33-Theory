"""Native chiral tetrahedra, Hesse complements, and the existing Jones f4.

Classical Hesse/SIC/Strange geometry is prior art. The new calculation is the
explicit native loop-to-projector map, with scoped supplied Hamiltonians.
"""
import collections
import itertools
import json
import math
import pathlib
import sys
import numpy as np

ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261031_tick_loop_rigidity import PI, exact_trace
from w33_pass12055_microscopic_tick_model import PTS, FORM, X, Z, w
import w33_pass11177_perfect_gates_tritangent as OLD


def faces(t):
    a,b,c,d=t
    return [(a,b,c),(a,d,b),(a,c,d),(b,d,c)]


def even_permutations():
    return [p for p in itertools.permutations(range(4))
            if sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2==0]


def canonical(t):
    return min(tuple(t[i] for i in p) for p in even_permutations())


def build():
    old=json.loads((ROOT/'data/w33_20261031_tick_loop_rigidity.json').read_text())
    plus={}
    for t in old['partial_Mendelsohn_system']['cycles']:
        for i in range(3):plus[t[i],t[(i+1)%3]]=t[(i+2)%3]
    tetra=sorted({canonical((a,b,c,plus[b,a])) for (a,b),c in plus.items()})
    assert len(tetra)==810
    assert all(exact_trace(f)==(1,2) for t in tetra for f in faces(t))
    groups=collections.defaultdict(list)
    complements=[];errors=[]
    for t in tetra:
        plane=tuple(sorted({a//3 for a in t}));assert len(plane)==4
        assert all(FORM(PTS[a],PTS[b]) for a,b in itertools.combinations(plane,2))
        Q=np.eye(9)-sum(PI[a] for a in t)/2
        err=max(float(np.max(abs(Q@Q-Q))),
                max(float(np.max(abs(PI[a]@Q))) for a in t))
        assert err<1e-11
        assert np.max(abs(np.linalg.eigvalsh(Q)-np.array([0]*6+[1]*3)))<1e-11
        groups[plane].append(len(complements));complements.append(Q);errors.append(err)
    assert len(groups)==90 and set(map(len,groups.values()))=={9}
    for ids in groups.values():
        Qs=np.array([complements[i] for i in ids])
        G=np.einsum('aij,bji->ab',Qs,Qs).real
        assert np.max(abs(G-(.75*np.ones((9,9))+2.25*np.eye(9))))<1e-11
        assert np.max(abs(Qs.sum(0)-3*np.eye(9)))<1e-11
    # Distinctness is also proved by the eight nonzero Pauli support labels.
    keys={tuple(np.rint(np.r_[Q.real.ravel(),Q.imag.ravel()]*1e9).astype(int)) for Q in complements}
    assert len(keys)==810
    tetra_set={tuple(sorted(t)) for t in tetra}
    frontier=[tuple(sorted(tetra[0]))];orbit=set(frontier)
    perms=old['Clifford_generator_permutations'].values()
    while frontier:
        t=frontier.pop()
        for p in perms:
            u=tuple(sorted(p[i] for i in t));assert u in tetra_set
            if u not in orbit:orbit.add(u);frontier.append(u)
    assert len(orbit)==810
    # Actual coordinate map to the existing45 factorisations, not just counts.
    basis=np.eye(4,dtype=int)
    transport=next(p for p in itertools.permutations(range(4))
        if all(OLD.w(basis[i][list(p)],basis[j][list(p)])==FORM(basis[i],basis[j])
               for i,j in itertools.product(range(4),repeat=2)))
    pid={p:i for i,p in enumerate(OLD.PTS)}
    point_map=[pid[OLD.norm(np.array(p)[list(transport)])] for p in PTS]
    native_factors={frozenset([frozenset(P),frozenset(i for i,v in enumerate(PTS)
                           if all(FORM(v,PTS[j])==0 for j in P))]) for P in groups}
    nplanes,old_factors=OLD.factorisations()
    mapped={frozenset(frozenset(point_map[i] for i in P) for P in f) for f in native_factors}
    assert nplanes==90 and len(native_factors)==45 and mapped==set(old_factors)
    # Canonical active second qutrit, spectator first qutrit.
    strange=np.array([0.,1.,-1.])/np.sqrt(2)
    S=np.outer(strange,strange);target=np.kron(np.eye(3),S)
    labels=[i for i,P in enumerate(PI) if np.max(abs(P@target))<1e-12]
    assert len(labels)==4 and tuple(sorted(labels)) in tetra_set
    Q=np.eye(9)-sum(PI[a] for a in labels)/2
    assert np.max(abs(Q-target))<1e-12
    f2=np.eye(9)-PI[0];f3=f2-1.5*f2@PI[12]@f2
    f4=f3-2*f3@PI[6]@f3
    R=np.kron(np.diag([1.,0.,0.]),np.eye(3))
    assert np.max(abs(f4-R@Q))<1e-12
    # Four explicit qutrit rays form a qubit SIC in the Strange-orthogonal plane.
    rays=[np.array([1.,0.,0.],complex)]+[np.array([1,w**j,w**j])/np.sqrt(3) for j in range(3)]
    G=abs(np.array(rays).conj()@np.array(rays).T)**2
    assert np.max(abs(G-(np.eye(4)*2/3+np.ones((4,4))/3)))<1e-12
    assert np.max(abs(np.array(rays)@strange))<1e-12
    assert np.max(abs(sum(np.outer(v,v.conj()) for v in rays)-2*(np.eye(3)-S)))<1e-12
    parity=np.eye(3)[:,[0,2,1]]
    points=[np.linalg.matrix_power(X,q)@np.linalg.matrix_power(Z,p) for q,p in itertools.product(range(3),repeat=2)]
    phase=[D@parity@D.conj().T for D in points]
    rho=Q/3
    W=np.array([np.trace(np.kron(a,b)@rho).real/9 for a in phase for b in phase])
    assert abs(W.sum()-1)<1e-12 and abs(abs(W).sum()-5/3)<1e-12
    assert np.count_nonzero(W<-.001)==9 and abs(W.min()+1/27)<1e-12
    return dict(status='PASS_CHIRAL_TETRAHEDRON_STRANGE_BRIDGE',
        unordered_tetrahedra=810,ordered_positive_tetrahedra=9720,
        oriented_tetrahedra=tetra,all_3240_faces_integer_verified=True,
        Clifford_orbit_size=len(orbit),stabilizer_order=4199040//810,
        maximum_projector_residual=max(errors),
        local_SIC_families=[dict(plane=P,tetrahedron_indices=ids) for P,ids in sorted(groups.items())],
        native_to_old_coordinate_permutation=transport,native_to_old_point_map=point_map,
        existing_factorisations_exactly_matched=45,
        canonical_native_ticks=labels,
        complement='Q=I-(Pa+Pb+Pc+Pd)/2 is a rank3 projector. Canonical Q=I3 tensor |Strange><Strange|.',
        positive_quantum_Hamiltonian='H=(Pa+Pb+Pc+Pd)/2=I-Q: exact eigenvalues0 multiplicity3,1 multiplicity6. Supplied fixed-label Hamiltonian, not a physical vacuum selection law.',
        tetrahedron_ground_energy='For J>0,K>3J/2 and lambda!=0, E_min=6(2J-4K/3)-4|lambda|/sqrt3 on the consistently oriented tetrahedral surface, with9720 ordered ground tuples. Every bond and face bound is simultaneously saturated; not a thermodynamic phase diagram.',
        SIC='For each of90 active Pauli planes, nine Q projectors satisfy Tr(QiQj)=3/4 for i!=j and sum Qi=3I9. Qi/3 form the Hesse SIC POVM tensored with a spectator identity.',
        Jones_bridge='The prior native Jones-Wenzl f4 equals RQ, R=|0><0| tensor I3, hence f4=|0><0| tensor |Strange><Strange|. Existing f4 identity belongs to7a57f8250; the new map constructs Q from a loop-compatible tetrahedron.',
        normalized_complement_Wigner=dict(minimum=float(W.min()),negative_entries=9,L1=float(abs(W).sum()),mana=math.log(5/3)),
        orientation_boundary='Reversing tetrahedral orientation changes the loop sign but preserves its unordered set, Q and H. Magic content alone does not choose this orientation.',
        resource_boundary='The gap of the supplied quantum Hamiltonian is not a free stabilizer-state preparation protocol. Implementing cooling, coherent projector filtering, or the corresponding non-Clifford evolution supplies a physical resource.',
        prior=['Classical Hesse SIC/MUB/Strange geometry: Stacey2016 Mathematics4(2)36.',
               'Pass11177 owns90 Pauli planes and45 factorisations; an explicit coordinate map is checked here.',
               'Pass10942/10943 magic factories and the October31 native Jones-Wenzl Strange identity predate this bridge.',
               'The preceding loop packet owns3240 positive cyclic blocks and the exact triangle law.'],
        boundary='Finite native operator and supplied Hamiltonian results. No observed particle, physical chirality, UV model, 3+1D gravity, universal protected braid computation or TOE derived.')


if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261031_chiral_tetrahedron_strange_bridge.json').write_text(json.dumps(d,indent=2)+'\n')
    print(json.dumps({k:d[k] for k in ['status','unordered_tetrahedra','Clifford_orbit_size','canonical_native_ticks','maximum_projector_residual']}))
