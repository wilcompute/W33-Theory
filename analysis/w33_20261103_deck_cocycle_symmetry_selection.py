"""Tetrahedral symmetry constrains, but does not select, native deck twists.

H3(C2^3,U1)=C2^7 and twisted-double formulas are standard. We apply them
to the actual meridians1,2,4,7; the prior ordered typeIII choice is audited.
"""
import collections
import itertools
import json
import pathlib

import numpy as np

ROOT=pathlib.Path(__file__).resolve().parents[1]
BRANCH=[1,2,4,7]


def exponent(code,a,b,c):
    out=0
    for i in range(3):out^=((code>>i)&1)*((a>>i)&1)*((b>>i)&1)*((c>>i)&1)
    for k,(i,j) in enumerate([(0,1),(0,2),(1,2)],3):out^=((code>>k)&1)*((a>>j)&1)*((b>>i)&1)*((c>>i)&1)
    return out^(((code>>6)&1)*(a&1)*((b>>1)&1)*((c>>2)&1))


def signature(code):return tuple(exponent(code,g,g,g) for g in range(1,8))


def sectors(code):
    count=0;dimensions=collections.Counter();spins=collections.Counter()
    for g in range(8):
        def alpha(x,y):return exponent(code,g,x,y)^exponent(code,x,y,g)^exponent(code,x,g,y)
        radical=[x for x in range(8) if all(alpha(x,y)==alpha(y,x) for y in range(8))]
        dim=round((8/len(radical))**.5);assert dim*dim*len(radical)==8
        dimensions[dim]+=len(radical);count+=len(radical)
        if not g:spins['1']+=8
        else:
            labels=['i','-i'] if exponent(code,g,g,g) else ['1','-1']
            for label in labels:spins[label]+=len(radical)//2
    assert sum(dim*dim*n for dim,n in dimensions.items())==64
    return dict(anyons=count,dimensions={str(k):v for k,v in dimensions.items()},spins=dict(spins))


def build():
    native=json.loads((ROOT/'data/w33_20261102_deck_monodromy_network.json').read_text())
    assert native['status'].startswith('PASS')
    actions=[]
    for p in itertools.permutations(range(4)):
        parity=sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))%2
        columns=[BRANCH[p[i]] for i in range(3)]
        action=[0]*8
        for x in range(8):
            for j in range(3):
                if x>>j&1:action[x]^=columns[j]
        assert sorted(action)==list(range(8)) and [action[x] for x in BRANCH]==[BRANCH[j] for j in p]
        if not parity:actions.append(action)
    assert len(actions)==12
    sig={code:signature(code) for code in range(128)};assert len(set(sig.values()))==128
    invariant=[code for code,q in sig.items() if all(tuple(exponent(code,p[g],p[g],p[g]) for g in range(1,8))==q for p in actions)]
    assert len(invariant)==4
    a,b,c,d=np.indices((8,8,8,8));checked=0
    for code in range(128):
        tensor=np.array([exponent(code,x,y,z) for x,y,z in itertools.product(range(8),repeat=3)],dtype=np.int8).reshape(8,8,8)
        delta=tensor[b,c,d]^tensor[a,b^c,d]^tensor[a,b,c]^tensor[a^b,c,d]^tensor[a,b,c^d]
        assert not delta.any();checked+=delta.size
    # The tempting fully alternating volume phase is an explicit coboundary.
    def beta(a,b):return ((a&1)*((a>>1)&1)*((b>>2)&1))^((a&1)*((a>>2)&1)*((b>>1)&1))^(((a>>1)&1)*((a>>2)&1)*(b&1))
    for a,b,c in itertools.product(range(8),repeat=3):
        determinant=0
        for p in itertools.permutations(range(3)):determinant^=((a>>p[0])&1)*((b>>p[1])&1)*((c>>p[2])&1)
        assert determinant==beta(b,c)^beta(a,b^c)^beta(a^b,c)^beta(a,b)
    ordered_orbit={tuple(exponent(64,p[g],p[g],p[g]) for g in range(1,8)) for p in actions}
    assert len(ordered_orbit)==4 and 64 not in invariant
    data=[]
    for code in invariant:
        row=dict(code=code,diagonal_negative_fluxes=[g for g in range(1,8) if exponent(code,g,g,g)],typeIII=bool(code&64),**sectors(code))
        if code&64:assert row['anyons']==22
        data.append(row)
    assert sorted(len(r['diagonal_negative_fluxes']) for r in data)==[0,3,4,7]
    return dict(status='PASS_NATIVE_BRANCH_SYMMETRY_COCYCLE_AUDIT',branch_addresses=BRANCH,
        oriented_tetrahedron_A4_actions=actions,standard_U1_classes=128,cocycle_equations_checked=checked,
        signature_complete_on_standard_classes='q(g)=omega(g,g,g) on7 nonzero elements uniquely distinguishes these128 standard representatives. A normalized U1 coboundary leaves q unchanged.',
        invariant_classes=data,ordered_typeIII_A4_orbit_size=4,
        prior_typeIII_boundary='The previously supplied omega=(-1)^(a0 b1 c2) distinguishes branch111. Its class is not invariant under native oriented tetrahedral A4; it breaks this symmetry unless extra fields transform the twist choice.',
        alternating_volume_phase='(-1)^det(a,b,c)=delta beta, beta=(-1)^(a0*a1*b2+a0*a2*b1+a1*a2*b0); thus the fully alternating candidate is cohomologically trivial.',
        nonabelian_invariant_choices=2,nonabelian_genus2_Hilbert_dimension=736,
        native_selection_obstruction='Deck maps fix every native projector label. Their canonical permutation operators compose strictly, so their native associator is1. The covering and its symmetry constrain possible extra gauge actions but do not select either nontrivial invariant typeIII class.',
        boundary='Exact finite cohomological/symmetry audit. No native SPT action, cocycle Hamiltonian, realized topological phase or braid universality is derived.',
        reference='https://link.aps.org/accepted/10.1103/PhysRevB.91.035134')


if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261103_deck_cocycle_symmetry_selection.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
    print(d['status'],[(r['code'],r['anyons'],r['spins']) for r in d['invariant_classes']],flush=True)
