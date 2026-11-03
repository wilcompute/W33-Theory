"""Native rank3 measurement holonomies realize a logical qutrit Clifford.

Discrete degenerate-projection holonomies are prior (Oi2014). The actual
120 projectors and Bargmann tensor are owned by the October tick work.
"""
import collections
import itertools
import json
import pathlib
import sys

import numpy as np
import sympy as s

ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261031_tick_loop_rigidity import PI

PAIRS=list(itertools.product(range(3),repeat=2));IDENTITY=tuple(range(9))+(0,)*9


def compose(a,b):return tuple(a[b[j]] for j in range(9))+tuple((b[9+j]+a[9+b[j]])%3 for j in range(9))


def closure(gens):
    words={IDENTITY:[]};queue=[IDENTITY]
    for a in queue:
        for j,g in enumerate(gens):
            b=compose(g,a)
            if b not in words:words[b]=words[a]+[j];queue.append(b)
        assert len(words)<=216
    return words


def build():
    C=np.array(json.loads((ROOT/'data/w33_20261102_chiral_surface_development.json').read_text())['completion_table'])
    A=np.rint(6*PI.real).astype(np.int64);B=np.rint(6*PI.imag/np.sqrt(3)).astype(np.int64)
    error=float(np.max(abs(PI-(A+1j*np.sqrt(3)*B)/6)));assert error<2e-14
    support=np.flatnonzero(np.diag(PI[0]).real>.5);assert support.tolist()==[0,3,6]
    assert np.max(abs(PI[0]-np.diag(np.diag(PI[0]))))<1e-14
    for a in range(120):
        neighbors=np.flatnonzero(C[a]>=0)
        R=A[a]@A[neighbors]-3*B[a]@B[neighbors]
        I=A[a]@B[neighbors]+B[a]@A[neighbors]
        assert np.array_equal(R@A[a]-3*I@B[a],np.broadcast_to(12*A[a],R.shape))
        assert np.array_equal(R@B[a]+I@A[a],np.broadcast_to(12*B[a],R.shape))
    unique={};counts=collections.Counter();triangle_count=0
    for b,c in itertools.combinations(np.flatnonzero(C[0]>=0),2):
        if C[b,c]<0:continue
        R=(A[b]@A[c]-3*B[b]@B[c])[np.ix_(support,support)]
        I=(A[b]@B[c]+B[b]@A[c])[np.ix_(support,support)]
        key=tuple(map(int,R.ravel()))+tuple(map(int,I.ravel()))
        unique.setdefault(key,[int(b),int(c)]);counts[key]+=1;triangle_count+=1
    assert triangle_count==2187 and len(unique)==28
    omega=(-1+s.I*s.sqrt(3))/2
    X=s.Matrix([[0,0,1],[1,0,0],[0,1,0]]);Z=s.diag(1,omega,omega**2)
    D=[s.simplify(X**a*Z**b) for a,b in PAIRS];Dn=np.array([np.array(x,dtype=complex) for x in D]);w=complex(omega)
    def action(M):
        p=[];phase=[]
        for O in Dn:
            image=M@O@M.conj().T
            matches=[(np.max(abs(image-w**k*Q)),i,k) for i,Q in enumerate(Dn) for k in range(3)]
            residual,i,k=min(matches);assert residual<2e-12;p.append(i);phase.append(k)
        assert sorted(p)==list(range(9));return tuple(p+phase)
    symbolic=[];actions=[];rows=[]
    for key,pair in unique.items():
        R=s.Matrix(3,3,key[:9]);I=s.Matrix(3,3,key[9:]);H=(s.sqrt(3)*R+3*s.I*I)/12
        assert R*R.T+3*I*I.T==48*s.eye(3) and I*R.T==R*I.T
        act=action(np.array(H,dtype=complex))
        # Exact images of X and Z prove Pauli-normalizer membership.
        for j in [3,1]:assert s.simplify(H*D[j]*H.conjugate().T-omega**act[9+j]*D[act[j]])==s.zeros(3)
        det=s.simplify(H.det());assert s.simplify(det**12)==1
        symbolic.append(H);actions.append(act)
        rows.append(dict(pair=pair,real_sqrt3_numerator=list(key[:9]),imaginary_times3_numerator=list(key[9:]),denominator=12,multiplicity=counts[key],action=list(act),determinant=str(det)))
    selected=[];group={IDENTITY:[]}
    for j,a in enumerate(actions):
        if a not in group:selected.append(j);group=closure([actions[k] for k in selected])
    assert len(group)==216 and len(selected)==3 and all(a in group for a in actions)
    ax=action(np.array(X,dtype=complex));az=action(np.array(Z,dtype=complex));assert ax in group and az in group
    def matrix_word(word):
        out=s.eye(3)
        for j in word:out=s.simplify(symbolic[selected[j]]*out)
        return out
    WX=matrix_word(group[ax]);WZ=matrix_word(group[az])
    comm=s.simplify(WX*WZ*WX.conjugate().T*WZ.conjugate().T)
    assert s.simplify(comm-omega**2*s.eye(3))==s.zeros(3)
    assert any(H==s.I*s.eye(3) for H in symbolic)
    maximal=0
    for row,H in zip(rows,symbolic):
        b,c=row['pair']
        if C[0,b]==c:
            assert H==s.I*s.eye(3);maximal+=row['multiplicity']
        if C[0,c]==b:assert H==-s.I*s.eye(3)
    return dict(status='PASS_NATIVE_POSTSELECTED_HOLONOMIC_QUTRIT_CLIFFORD',reference_projector=0,reference_support=support.tolist(),
        projector_entry_reconstruction_error=error,exact_isoclinic_ordered_pairs=9720,
        based_unordered_triangles=triangle_count,distinct_oriented_holonomy_matrices=28,holonomies=rows,
        selected_holonomy_indices=selected,projective_Clifford_order=216,linear_holonomy_group_order=2592,
        logical_X_word=group[ax],logical_Z_word=group[az],central_commutator='omega^2 I3',central_quartet_loop='i I3',
        order_proof='Exact X/Z conjugation places all generators in the qutrit Pauli normalizer. Their finite adjoint action has order216. Determinants are12th roots, so any scalar kernel element has order dividing36. All entries lie in Q(sqrt3,i)=Q(zeta12), whose roots of unity are mu12, giving kernel at most12. Explicit iI and omega^2 I generate all12, so group order2592.',
        transport='For a noncommuting pair Pa Pb Pa=Pa/3. Based loop H=3sqrt3*(P0 Pb Pc P0)|support is unitary. Physical projector application order is Pc, then Pb, then P0.',
        success_probability='1/27 for this three-projection branch, independent of encoded logical state. Failed outcomes are not repaired by this producer.',
        chiral_boundary='Every positively maximal triangle at this base gives iI3: chirality alone is a scalar logical phase. Non-Abelian logical gates require other triangles outside the frozen quartet.',
        ownership='October31 tick-loop rigidity owns the120 native projectors and scalar Bargmann phase; Pass12521 owns a648 braid image on a different carrier. Oi2014 owns the general degenerate-projection holonomy method. The explicit native3x3 gates and all2187 based triangles are audited here.',
        reference='https://arxiv.org/abs/1402.1104',
        boundary='Postselected ideal Clifford control, not a deterministic receiver, a non-Clifford universal set, a laboratory result or a spacetime connection.')


if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261103_native_projector_holonomic_qutrit.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
    print(d['status'],d['selected_holonomy_indices'],d['linear_holonomy_group_order'],flush=True)
