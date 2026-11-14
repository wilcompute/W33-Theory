#!/usr/bin/env python3
"""Exact stabilizer slice of CP7 -> HP3 twistor fibration.

All 1080 three-qubit stabilizer projectors are constructed over Z[i]/8.
Their 27 Pauli-charge images are 180 quaternionic rank-one planes,
with six projective states per CP1 fiber. Those six form an exact
complex-projective 2-design within their quaternionic fiber.
"""
from pathlib import Path
from itertools import combinations, product
from collections import defaultdict, Counter, deque
import sys, json, numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261114_exact_gaussian_us8_pauli_clock as E
OUT=ROOT/"data/toe_20261114_stabilizer_twistor_2design.json"

def main():
    pauli,quad,nonquad,terms=E.pauli_data()
    idx={v:i for i,v in enumerate(quad)}
    I=np.eye(8,dtype=complex)
    J=pauli[9]
    assert np.array_equal(J@J.conj(),-I)
    for v,P in pauli.items():
        assert np.array_equal(J@P.conj()@J,(1 if E.q(v)==0 else -1)*P)
    lagrangians=set()
    for a,b,c in combinations(range(1,64),3):
        if E.omega(a,b) or E.omega(a,c) or E.omega(b,c) or a^b==c:continue
        lagrangians.add(frozenset((a,b,c,a^b,a^c,b^c,a^b^c)))
    assert len(lagrangians)==135
    fibers=defaultdict(list)
    for L in sorted(lagrangians,key=lambda l:tuple(sorted(l))):
        a,b=sorted(L)[:2]
        c=next(v for v in sorted(L) if v not in (a,b,a^b))
        for signs in product((1,-1),repeat=3):
            R8=(I+signs[0]*pauli[a])@(I+signs[1]*pauli[b])@(I+signs[2]*pauli[c])
            assert np.array_equal(R8.conj().T,R8)
            assert np.array_equal(R8@R8,8*R8)
            assert np.trace(R8)==8
            R8j=J@R8.conj()@J
            assert np.array_equal(R8@R8j,np.zeros((8,8)))
            z=[]
            for v in quad:
                coeff=np.trace(R8@pauli[v])/8
                assert coeff.imag==0 and coeff.real==round(coeff.real)
                z.append(int(coeff.real))
            z=tuple(z)
            assert sum(x*x for x in z)==3
            assert sum(s*z[idx[u]]*z[idx[v]]*z[idx[w]] for (u,v,w),s in terms.items())==1
            X=sum((z[idx[v]]*pauli[v] for v in quad),np.zeros((8,8),complex))
            assert np.array_equal(R8+R8j,2*(I+X))
            fibers[z].append(R8)
    assert sum(map(len,fibers.values()))==1080
    assert len(fibers)==180 and {len(f) for f in fibers.values()}=={6}
    targets=set()
    for (u,v,w),s in terms.items():
        for a,b,c in product((-1,1),repeat=3):
            if a*b*c!=s:continue
            z=[0]*27
            z[idx[u]],z[idx[v]],z[idx[w]]=a,b,c
            targets.add(tuple(z))
    assert targets==set(fibers)
    swap=np.zeros((64,64),dtype=complex)
    for a in range(8):
        for b in range(8):swap[8*a+b,8*b+a]=1
    ov_census=Counter()
    for z,rs in fibers.items():
        Pi8=rs[0]+J@rs[0].conj()@J
        assert np.array_equal(Pi8@Pi8,8*Pi8)
        assert np.trace(Pi8)==16
        for r in rs:
            assert np.array_equal(r+J@r.conj()@J,Pi8)
            assert np.array_equal(Pi8@r,8*r)
        ov=[]
        for ra,rb in combinations(rs,2):
            n=np.trace(ra@rb).real
            assert n in (0,32)
            ov.append(n/64)
        assert sorted(ov)==[0.]*3+[.5]*12
        ov_census.update(ov)
        lhs=sum((np.kron(r,r) for r in rs),np.zeros((64,64),complex))
        rhs=np.kron(Pi8,Pi8)
        assert np.array_equal(lhs,rhs+rhs@swap)
        assert np.array_equal(sum(rs),3*Pi8)
    actions=[]
    for a in nonquad:
        mp=[]
        for v in quad:
            if not E.omega(a,v):mp.append((idx[v],1))
            else:
                w=a^v
                assert w in idx
                M=1j*pauli[a]@pauli[v]
                if np.array_equal(M,pauli[w]):s=1
                else:
                    assert np.array_equal(M,-pauli[w])
                    s=-1
                mp.append((idx[w],s))
        assert len({w for w,s in mp})==27
        actions.append(mp)
    def act(z,mp):
        r=[0]*27
        for i,(j,s) in enumerate(mp):r[j]=s*z[i]
        return tuple(r)
    unseen=set(fibers);orbits=[]
    while unseen:
        seed=min(unseen);orbit={seed};todo=deque([seed]);unseen.remove(seed)
        while todo:
            z=todo.popleft()
            for mp in actions:
                w=act(z,mp)
                assert w in fibers
                if w not in orbit:
                    orbit.add(w);todo.append(w);unseen.remove(w)
        orbits.append(len(orbit))
    assert sorted(orbits)==[180]
    rng=np.random.default_rng(20261114)
    max_residual=0.
    for _ in range(24):
        psi=rng.normal(size=8)+1j*rng.normal(size=8)
        psi/=np.linalg.norm(psi)
        eta=J@psi.conj()
        assert abs(np.vdot(psi,eta))<1e-12
        Pi=np.outer(psi,psi.conj())+np.outer(eta,eta.conj())
        z=np.array([np.vdot(psi,pauli[v]@psi).real for v in quad])
        X=sum((z[idx[v]]*pauli[v] for v in quad),np.zeros((8,8),complex))
        max_residual=max(max_residual,float(np.max(abs(4*Pi-(I+X)))))
        assert abs(z@z-3)<1e-12
        assert abs(sum(s*z[idx[u]]*z[idx[v]]*z[idx[w]] for (u,v,w),s in terms.items())-1)<1e-12
        theta=rng.uniform(0,np.pi/2);phase=rng.uniform(0,2*np.pi)
        qpsi=np.cos(theta)*psi+np.exp(1j*phase)*np.sin(theta)*eta
        qz=np.array([np.vdot(qpsi,pauli[v]@qpsi).real for v in quad])
        assert np.max(abs(qz-z))<1e-12
    assert max_residual<1e-12
    result=dict(status="PASS_EXACT_STABILIZER_TWISTOR_CP7_TO_HP3_2DESIGN",
        lagrangian_three_qubit_stabilizer_bases=135,
        complex_projective_stabilizer_states=1080,
        quaternionic_projective_integral_BPS_charge_points=180,
        fiber_cardinality=6,
        base="HP^3=Sp(4)/(Sp(1)xSp(3)), real dimension 12",
        total="CP^7=Sp(4)/(Sp(3)xU(1)), real dimension 14",
        continuous_fiber="CP^1=S^2, real dimension 2",
        each_discrete_fiber="six single-qubit stabilizer states (Pauli octahedron)",
        each_fiber_exact_projective_2design=True,
        twirl_identity="Pi_psi=|psi><psi|+|Jpsi><Jpsi|=(I+sum_{Q(v)=0} z_v P_v)/4",
        exact_first_moment="sum_{six} rho_i = 3 Pi",
        exact_second_moment="sum_{six} rho_i tensor rho_i = (Pi tensor Pi)(I+SWAP)",
        each_minimal_charge_has_cubic_N_1_and_norm2_3=True,
        number_signed_45_triads=45,
        number_signed_BPS_per_triad=4,
        packet_clifford_orbit_sizes_on_180_charges=sorted(orbits),
        exact_discrete_overlap_census={str(k):v for k,v in sorted(ov_census.items())},
        continuous_random_complex_pure_states_tested=24,
        max_complex_twirl_matrix_residual=max_residual,
        physical_scope="Known twistor fibration and qubit stabilizer 2-design, instantiated exactly for the repo signed three-qubit Pauli E6 cubic and all 1080 states; not a channel that measures or erases the fiber and not evidence of a TOE.")
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,sort_keys=True),flush=True)
    return result

if __name__=="__main__":
    main()
