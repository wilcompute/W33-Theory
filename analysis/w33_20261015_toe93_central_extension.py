"""TOE93: gauge-invariant commutator detects nontrivial PSp(4,3) multiplier.

Lift five symplectic transvections to ququart U(4) as in TOE91;
enumerate the 25920 projective words as in TOE92. Find commuting
PROJECTIVE permutations whose U(4) lifts anticommute. Their
commutator -I is unchanged by individual scalar rephasing: a true
nontrivial Schur multiplier witness (unlike a single BFS cocycle edge).
"""
from __future__ import annotations
import json
from collections import deque
import numpy as np
from analysis.w33_20261015_toe90_vlasov_ququart_design import ROOT
from analysis.w33_20261015_toe92_full_symplectic_4mode import comp
from analysis.w33_20261015_toe91_symplectic_phase_audit import transvection
from analysis.w33_20261015_toe91_symplectic_unitary_lift import lift
V=[[1,0,0,0],[0,1,0,0],[0,0,1,0],[1,1,0,0],[0,0,0,1]]
def words():
    perms=[tuple(transvection(v)) for v in V]
    Us=[]
    for p in perms:
        u,err,s=lift(p)
        u*=np.exp(-1j*np.angle(s)/3)
        assert np.max(abs(u@u@u-np.eye(4)))<1e-8
        Us.append(u)
    e=tuple(range(40))
    nodes={e:0}
    allperm=[e];allU=[np.eye(4,dtype=complex)];prev=[None]
    queue=deque([0])
    while queue:
        i=queue.popleft()
        p=allperm[i]
        for j,q in enumerate(perms):
            z=comp(q,p)
            if z not in nodes:
                nodes[z]=len(allperm)
                allperm.append(z)
                allU.append(Us[j]@allU[i])
                prev.append((i,j))
                queue.append(nodes[z])
    assert len(nodes)==25920
    return allperm,allU,prev,nodes
def word_for(i,prev):
    w=[]
    while prev[i] is not None:
        i,g=prev[i]
        w.append(g)
    return list(reversed(w))
def certificate():
    perms,Us,prev,where=words()
    # In a projective order-2 element, U^2 is scalar.
    idp=tuple(range(40))
    order2=[i for i,p in enumerate(perms) if i and comp(p,p)==idp]
    assert len(order2)>100
    witness=None
    # Prefer low-word-length representatives so the certificate is audit-friendly.
    candidates=sorted(order2,key=lambda i:(len(word_for(i,prev)),i))
    for i in candidates[:150]:
        p=perms[i];u=Us[i]
        for j in candidates[:1200]:
            if i==j:continue
            q=perms[j]
            if comp(p,q)!=comp(q,p):continue
            v=Us[j]
            # For commuting projective symmetries UV=phase VU.
            alpha=np.trace((v@u).conj().T@(u@v))/4
            if abs(alpha+1)<1e-8:
                w1,w2=word_for(i,prev),word_for(j,prev)
                assert np.max(abs(u@v+v@u))<1e-8
                assert comp(p,q)==comp(q,p)
                witness={'projective_order_two_permutation_A_word':w1,
                         'projective_order_two_permutation_B_word':w2,
                         'word_generator_vectors_F3':V,
                         'projective_permutations_commute':True,
                         'ququart_U4_lifts_anticommute':True,
                         'scalar_commutator':'-1',
                         'commutator_max_numerical_residual_rounded':round(float(np.max(abs(u@v+v@u))),12),
                         'commutator_phase_rounded':[
                            round(float(alpha.real),12),round(float(alpha.imag),12)]}
                break
        if witness:break
    assert witness is not None,'No commuting projective order-two lifts with -1 commutator found'
    print('CENTRAL-MULTIPLIER',witness,flush=True)
    return {'projective_group':'PSp(4,3)',
            'projective_40_ray_permutation_order':len(perms),
            'projective_involutions_count':len(order2),
            'gauge_invariant_nontrivial_multiplier_witness':witness,
            'result':'An honest linear representation of the 25920-element projective permutation group using these four-mode ray operators cannot exist: commuting projective group elements lift to anticommuting unitaries. The gauge-invariant -1 commutator detects a nontrivial order-two central obstruction.',
            'caveats':'This identifies an order-two obstruction and is consistent with the Sp(4,3) double cover, but does not construct an exact character table of the full unitary extension or uniquely choose global phases. Finite numerical matrices are checked with 1e-8 tolerances.'}
if __name__=='__main__':
    d=certificate()
    (ROOT/'data/w33_20261015_toe93_central_extension.json').write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
