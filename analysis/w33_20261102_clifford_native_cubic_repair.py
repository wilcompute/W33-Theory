"""Explicit enlarged Clifford action on the SAME signed native E6 cubic.

This is a changed embedding, not an extension of the old signed27 action.
Prior Pfaffian/E6 owners: w33_pfaffian_doily_e6_cubic_bridge.py and
w33_all36_pfaffian_double_six_sections.py. The standard SL6 model is prior
representation theory (Manivel, Configurations of lines and models of Lie algebras).
The signed common-cover obstruction is already owned by the October31/Nov1 work.
"""
import collections
import itertools
import json
import pathlib
import sys

import networkx as nx
import sympy as s

ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_pfaffian_doily_e6_cubic_bridge import DUADS,PF
from w33_20261031_signed_cubic_lift import solve2
from w33_20261102_common_cover_interactions import gaussian_product
from w33_20261102_toroidal_knight_clifford_bridge import matrices,adjoint_action,closure,compose


def cubic_terms():
    out=dict(PF)
    for k,(i,j) in enumerate(DUADS):
        out[tuple(sorted((15+i,k,21+j)))]=1
        out[tuple(sorted((15+j,k,21+i)))]=-1
    assert len(out)==45
    return out


def representation(U):
    B=s.diag(U,s.eye(2));R=s.zeros(27)
    for row,(i,j) in enumerate(DUADS):
        for col,(a,b) in enumerate(DUADS):R[row,col]=s.expand(B[i,a]*B[j,b]-B[i,b]*B[j,a])
    dual=B.inv().T
    R[15:21,15:21]=dual;R[21:27,21:27]=dual
    return R


def transform_cubic(terms,M):
    rows=[[(j,M[i,j]) for j in range(27) if M[i,j]!=0] for i in range(27)]
    out=collections.defaultdict(lambda:s.Integer(0))
    for (a,b,c),coefficient in terms.items():
        for (i,x),(j,y),(k,z) in itertools.product(rows[a],rows[b],rows[c]):
            out[tuple(sorted((i,j,k)))]+=coefficient*x*y*z
    return {key:s.simplify(value) for key,value in out.items() if s.simplify(value)!=0}


def sparse(M):
    return [[i,j,str(M[i,j])] for i in range(M.rows) for j in range(M.cols) if M[i,j]!=0]


def build():
    old=json.loads((ROOT/'data/w33_20261031_signed_cubic_lift.json').read_text())
    native={tuple(r['triple']):r['coefficient'] for r in old['coefficient_rows']}
    model=cubic_terms()
    def graph(terms):
        G=nx.Graph();G.add_nodes_from(range(27))
        G.add_edges_from(e for t in terms for e in itertools.combinations(t,2));return G
    phi=next(nx.isomorphism.GraphMatcher(graph(model),graph(native)).isomorphisms_iter())
    bits=solve2([(sum(1<<i for i in t),int(coefficient!=native[tuple(sorted(phi[i] for i in t))])) for t,coefficient in model.items()],27)
    assert bits is not None
    T=s.zeros(27)
    for i in range(27):T[phi[i],i]=(-1)**bits[i]
    assert transform_cubic(native,T)==model
    axes,blades,gens,omega=matrices();N=s.eye(4)+s.I*blades[15];U=N/s.sqrt(2);all_gens=gens+[U]
    reps=[]
    for g in all_gens:
        assert s.simplify(g.det())==1
        R=representation(g)
        assert s.simplify(R.conjugate().T*R)==s.eye(27)
        assert transform_cubic(model,R)==model
        native_R=T*R*T.T
        assert transform_cubic(native,native_R)==native
        reps.append(sparse(native_R))
    # Exhibit iI in the enlarged linear group: U^2=iP and P belongs to old1920.
    unit=json.loads((ROOT/'data/w33_20261031_unitary_stabilizer_lift.json').read_text())
    ugens=[tuple(k) for k in unit['generator_doubled_integer_keys']]
    identity=tuple(int(2*s.re(x)) for x in s.eye(4))+(0,)*16
    pkey=tuple(int(2*s.re(x)) for x in blades[15])+tuple(int(2*s.im(x)) for x in blades[15])
    words={identity:[]};queue=[identity]
    for a in queue:
        if pkey in words:break
        for j,g in enumerate(ugens):
            b=gaussian_product(g,a)
            if b not in words:words[b]=words[a]+[j];queue.append(b)
    assert pkey in words and s.simplify(U**2*blades[15])==s.I*s.eye(4)
    # A basis-invariant mismatch with the old signed27 module.
    interactions=json.loads((ROOT/'data/w33_20261102_common_cover_interactions.json').read_text())
    mismatch=None
    for row in interactions['signed_kernel_word_witnesses']:
        a=identity
        for j in row['word']:a=gaussian_product(ugens[j],a)
        if a==identity and any(row['sign_bits']):mismatch=row;break
    assert mismatch is not None
    # If unsigned actions factor through projective Clifford, unchanged support
    # extension is impossible: centralizer of its Pauli16 is that Pauli16.
    old_actions=[adjoint_action(2*g,4,blades) for g in gens]
    H=closure(old_actions,960);G=closure(old_actions+[adjoint_action(N,2,blades)],11520)
    pauli={adjoint_action(b,1,blades) for b in blades}
    assert len(pauli)==16 and pauli<=H
    centralizer={g for g in G if all(compose(g,p)==compose(p,g) for p in pauli)}
    assert centralizer==pauli and 51840%11520!=0
    # A6 component of the new27 supports a canonical scalar-spinor-spinor tensor.
    pairs=list(itertools.combinations(range(4),2));J=s.zeros(6)
    for i,a in enumerate(pairs):
        for j,b in enumerate(pairs):
            if len(set(a+b))==4:
                J[i,j]=s.LeviCivita(*(a+b))
    assert J.det()!=0 and J.T==J
    for g in all_gens:
        W=s.Matrix([[g[i,a]*g[j,b]-g[i,b]*g[j,a] for a,b in pairs] for i,j in pairs])
        assert s.simplify(W.T*J*W)==J
    return dict(status='PASS_ENLARGED_CLIFFORD_ACTION_ON_NATIVE_CUBIC',model='Pf(A)+u^T A v; A in Lambda2(C6), u,v in dual(C6)',
        model_terms=[dict(triple=t,coefficient=c) for t,c in sorted(model.items())],
        model_to_native=[dict(model_coordinate=i,native_coordinate=phi[i],sign=(-1)**bits[i]) for i in range(27)],
        native_generator_sparse_matrices=reps,native_cubic_terms_checked_per_generator=45,
        enlarged_projective_order=11520,enlarged_linear_order=46080,old_word_for_pseudoscalar=words[pkey],
        linear_order_proof='Projective image11520 is certified. Determinant-one scalar kernel has order<=4; U^2 P=iI and P is the exported old-generator word, so all4 scalars occur. Hence linear order46080.',
        unchanged_embedding_mismatch=dict(word=mismatch['word'],old_signed_trace=27-2*sum(mismatch['sign_bits']),new27_trace=27,old_sign_bits=mismatch['sign_bits'],spinor_word='I4'),
        unsigned_extension_obstruction='A normal kernel of an extension from projective Clifford to the native support-automorphism group cannot meet old960, hence cannot meet Pauli16. Its commutator with Pauli16 is trivial, forcing it into centralizer(Pauli16)=Pauli16, so the map would be injective. But11520 does not divide |Aut(GQ(2,4))|=51840. This excludes prescribed support-permutation extensions factoring through projective Clifford, not arbitrary larger common covers.',
        mixed_bilinear_repair=dict(component='Lambda2(C4), dimension6',pair_labels=pairs,
                                  symmetric_pairing=[[str(x) for x in row] for row in J.tolist()],
                                  invariant='chi^T J (psi wedge eta)',
                                  boundary='The new27 action contains the6 component; this changes the old embedding. No masses, Lorentz representation or numerical coupling is selected.'),
        boundary='Exact nonmonomial action on the same signed native cubic, with an explicit coordinate map. It does not extend the old signed27 generators unchanged: the exported identity-spinor word has incompatible traces. The standard SL6 model and Pfaffian relation are prior mathematics.')


if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261102_clifford_native_cubic_repair.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
    print(d['status'],d['enlarged_linear_order'],d['unchanged_embedding_mismatch']['old_signed_trace'],flush=True)
