"""A finite enlarged common cover preserving the old27 action on one block.

Induction, Schreier transversals and abelian-kernel relation calculations are
standard. This uses the actual signed27 lifts and the actual Clifford11520.
It supplies a324-coordinate alternative to changing the native27 embedding.
No minimality among all enlarged common covers is claimed.
"""
import collections
import json
import pathlib
import sys

import numpy as np
import sympy as s

ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261102_toroidal_knight_clifford_bridge import compose,closure,IDENTITY,matrices,adjoint_action
from w33_20261101_common_cubic_spinor_extension import signed_mul


def inverse(a):
    p=[0]*16;q=[0]*16
    for i,j in enumerate(a[:16]):p[j]=i;q[j]=-a[16+i]%4
    return tuple(p+q)


def rank_add(basis,value):
    while value:
        k=value.bit_length()-1
        if k not in basis:basis[k]=value;return True
        value^=basis[k]
    return False


def build():
    bridge=json.loads((ROOT/'data/w33_20261102_toroidal_knight_clifford_bridge.json').read_text())
    cubic=json.loads((ROOT/'data/w33_20261031_signed_cubic_lift.json').read_text())
    old_actions=[tuple(a) for a in bridge['old_signed_generator_actions']];extra=tuple(bridge['signed_switch_action']);gens=old_actions+[extra]
    signed=[(tuple(a['permutation']),tuple(a['sign_bits'])) for a in cubic['signed_generators']]
    identity27=(tuple(range(27)),(0,)*27)
    # A nonhomomorphic section old960 -> signed30720, retaining original generators.
    section={IDENTITY:identity27};todo=[IDENTITY]
    for a in todo:
        for g,lift in zip(old_actions,signed):
            b=compose(g,a)
            if b not in section:section[b]=signed_mul(lift,section[a]);todo.append(b)
    assert len(section)==960 and all(section[g]==lift for g,lift in zip(old_actions,signed))
    G=closure(gens,11520)
    unseen=set(G);transversal=[IDENTITY];coset={}
    def add_coset(t,index):
        for h in section:
            a=compose(t,h);assert a not in coset;coset[a]=index;unseen.remove(a)
    add_coset(IDENTITY,0)
    while unseen:
        t=min(unseen);transversal.append(t);add_coset(t,len(transversal)-1)
    assert len(transversal)==12
    inv=[inverse(t) for t in transversal];newgens=[]
    coefficients={tuple(row['triple']):row['coefficient'] for row in cubic['coefficient_rows']}
    for j,g in enumerate(gens):
        p=[0]*324;b=[0]*324
        for block,t in enumerate(transversal):
            gt=compose(g,t);target=coset[gt];h=compose(inv[target],gt);q,signs=section[h]
            for i in range(27):p[27*block+i]=27*target+q[i];b[27*block+i]=signs[i]
            assert all(coefficients[tri]*(-1)**sum(signs[i] for i in tri)==coefficients[tuple(sorted(q[i] for i in tri))] for tri in coefficients)
        assert sorted(p)==list(range(324))
        if j<6:assert p[:27]==list(signed[j][0]) and b[:27]==list(signed[j][1])
        newgens.append((tuple(p),sum(x<<i for i,x in enumerate(b))))
    # Exact scalar phases of Clifford relations via a characteristic1009 image.
    # Same exact projective Pauli action implies ratios are scalars. det=1
    # restricts them to mu4, whose reduction is injective, so this is exact.
    _,blades,Uold,_=matrices();Uextra=(s.eye(4)+s.I*blades[15])/s.sqrt(2)
    pmod=1009;iroot=next(i for i in range(pmod) if i*i%pmod==pmod-1);rroot=next(i for i in range(pmod) if i*i%pmod==2)
    def modular(z):
        z=s.expand(z)
        # Algebraic-number coefficients in Q(sqrt2,i), evaluated by a ring map.
        value=s.expand(z).subs(s.sqrt(2),s.Integer(rroot)).subs(s.I,s.Integer(iroot))
        num,den=s.fraction(value);return int(num)*pow(int(den),-1,pmod)%pmod
    ugens=[np.array([[modular(z) for z in row] for row in U.tolist()],dtype=np.int64) for U in Uold+[Uextra]]
    phases=[pow(iroot,k,pmod) for k in range(4)]
    chosen={IDENTITY:(tuple(range(324)),0,np.eye(4,dtype=np.int64),[])};queue=[IDENTITY]
    signed_basis={};mixed_basis={};odd_phase=False;pure_basis={};relation_count=0;witnesses=[]
    for a in queue:
        perm,bits,U,word=chosen[a]
        for j,(g,(q,signs),V) in enumerate(zip(gens,newgens,ugens)):
            target=compose(g,a)
            newperm=tuple(q[perm[i]] for i in range(324))
            newbits=bits^sum(((signs>>perm[i])&1)<<i for i in range(324))
            newU=V@U%pmod
            if target not in chosen:
                chosen[target]=(newperm,newbits,newU,word+[j]);queue.append(target)
                continue
            oldperm,oldbits,oldU,oldword=chosen[target];assert oldperm==newperm
            # B^-1 A has domain sign vector bits(A) xor bits(B).
            delta=newbits^oldbits
            exponent=next(k for k,z in enumerate(phases) if np.array_equal(newU,z*oldU%pmod))
            fresh=rank_add(signed_basis,delta)
            mixed_fresh=rank_add(mixed_basis,delta|((exponent%2)<<324))
            pure_fresh=rank_add(pure_basis,delta|(((exponent//2)%2)<<324))
            odd_phase|=exponent%2==1;relation_count+=1
            if fresh or mixed_fresh or pure_fresh:witnesses.append(dict(left_word=word+[j],right_word=oldword,sign_delta_hex=hex(delta),spinor_scalar_i_exponent=exponent))
    assert len(chosen)==11520
    assert len({row[0] for row in chosen.values()})==11520
    # Kernel is a subgroup of C2^324 x C4. If an odd phase occurs, doubling
    # gives(0,2); otherwise the phase/2 supplies an ordinary extra F2 bit.
    kernel_exponent=len(mixed_basis)+1 if odd_phase else len(pure_basis)
    paired_order=11520*(1<<kernel_exponent)
    signed_order=11520*(1<<len(signed_basis))
    assert paired_order%46080==0 and len(signed_basis)<=60
    return dict(status='PASS_INDUCED_NATIVE_CUBIC_COMMON_COVER',blocks=12,block_dimension=27,total_scalar_dimension=324,
        signed_generator_permutations=[list(p) for p,b in newgens],signed_generator_bits_hex=[hex(b) for p,b in newgens],
        unsigned_projective_order=11520,signed_kernel_F2_dimension=len(signed_basis),signed_group_order=signed_order,
        paired_kernel_over_projective_order=1<<kernel_exponent,paired_common_cover_order=paired_order,
        kernel_over_linear_spinor_order=paired_order//46080,linear_spinor_quotient_order=46080,
        paired_kernel_exponent=kernel_exponent,paired_kernel_has_order4=odd_phase,
        Schreier_non_tree_relations_checked=relation_count,kernel_relation_witnesses=witnesses,
        cubic='Sum over12 coset blocks of the identical signed native27 cubic. Every generator permutes blocks and acts inside each by a certified old signed-cubic symmetry.',
        old_action_preservation='Each of the six original generators preserves reference block0 and restricts exactly to the original signed27 generator there, paired with the original spinor matrix. Thus the old coupled action is recovered on the reference block of its stabilizer; the globally enlarged carrier has dimension324, not27.',
        order_proof='Choose one signed/linear spinor lift for each of11520 exact projective Pauli actions. Every non-tree Cayley relation is a diagonal sign vector plus a mu4 scalar; these commute. Schreier generators span the complete kernel. Binary elimination computes the sign rank and the C2^324 x C4 kernel size. The same-projective-action ratios are exact scalar fourth roots; reduction modulo1009 distinguishes them injectively.',
        phase_modulus=pmod,phase_i_root=iroot,phase_sqrt2_root=rroot,
        boundary='An explicit finite common cover and enlarged324-coordinate cubic carrier, not a minimal extension, unchanged global27 module, physical matter spectrum or coupling theory. Its12 algebraic cosets are distinct from the8 sheets of the native surface covering.')


if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261102_induced_cubic_common_cover.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
    print(d['status'],d['signed_kernel_F2_dimension'],d['paired_common_cover_order'],flush=True)
