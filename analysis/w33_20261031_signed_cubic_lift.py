"""Transport the actual q=5 action to the repository's signed E6 cubic.

Construct a signed monomial lift, and test a section over signs +/-1 using
all Cayley-edge relations. A failed sign section says nothing about arbitrary
complex torus phases or arbitrary nonmonomial representations.
"""
import itertools,json,pathlib,collections,hashlib,sys
import numpy as np
import networkx as nx
ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261031_continuum_chirality import internal_e6_support

def solve2(rows,n):
    basis={}
    for a,b in rows:
        while a:
            i=a.bit_length()-1
            if i not in basis:basis[i]=(a,b);break
            u,v=basis[i];a^=u;b^=v
        else:
            if b:return None
    x=0
    for i,(a,b)in sorted(basis.items()):
        if ((a&x).bit_count()&1)!=b:x|=1<<i
    return [(x>>i)&1 for i in range(n)]

def mul(g,h):
    p,a=g;q,b=h
    return tuple(p[q[i]]for i in range(27)),tuple(b[i]^a[q[i]]for i in range(27))

def section_test(generators,triples,coefficients,matrices=None,central_bits=None):
    """Unknowns are six generator sign vectors (162 bits).

    A spanning-tree word determines every group element's signs linearly.
    Every remaining Cayley edge must give the same signs. Thus consistency
    is necessary and sufficient for a signed monomial homomorphic section.
    """
    n=27*len(generators);basis={};inputs=[];bad=None
    def add(a,b,description):
        nonlocal bad
        index=len(inputs);inputs.append((a,b,description));w=1<<index
        while a:
            k=a.bit_length()-1
            if k not in basis:basis[k]=(a,b,w);return
            c,d,v=basis[k];a^=c;b^=d;w^=v
        if b and bad is None:bad=w
    for j,p in enumerate(generators):
        for t in triples:
            a=sum(1<<(27*j+i)for i in t)
            b=int(coefficients[t]!=coefficients[tuple(sorted(p[i]for i in t))])
            add(a,b,dict(kind='cubic',generator=j,triple=t))
    identity=tuple(range(27));matrix_key=lambda A:tuple(map(int,A.flat))
    I=np.eye(4,dtype=int);key0=identity if matrices is None else matrix_key(I)
    words={key0:([0]*27,identity,[],I)};queue=[key0]
    for key in queue:
        L,p,path,A=words[key]
        for j,g in enumerate(generators):
            q=tuple(g[p[i]]for i in range(27));nextL=[L[i]^(1<<(27*j+p[i]))for i in range(27)]
            B=A if matrices is None else np.array(matrices[j])@A%5
            target=q if matrices is None else matrix_key(B)
            if target not in words:
                words[target]=(nextL,q,path+[j],B);queue.append(target)
                if matrices is not None and target==matrix_key(-I%5):
                    for i in range(27):add(nextL[i],central_bits[i],dict(kind='central',word=path+[j],coordinate=i))
            else:
                for i in range(27):add(nextL[i]^words[target][0][i],0,dict(kind='Cayley-edge',left_word=path+[j],right_word=words[target][2],coordinate=i))
                if bad is not None:break
            if bad is not None:break
        if bad is not None:break
    if bad is not None:
        witness=[dict(coefficients_hex=hex(a),rhs=b,description=d)for i,(a,b,d)in enumerate(inputs)if bad>>i&1]
        a=b=0
        for row in witness:a^=int(row['coefficients_hex'],16);b^=row['rhs']
        assert a==0 and b==1
        return dict(splits_over_real_signs=False,unknown_sign_bits=n,contradiction_rows=witness,
            conclusion=('No signed-monomial representation of the actual unitary1920 double cover with central -I acting as minus on16 and plus on1+10.' if matrices is not None else 'No homomorphic signed-monomial section of this unsigned960 action preserves this cubic.')+' XOR of the frozen equations is0=1. This excludes +/-1 phases only.')
    assert len(words)==(960 if matrices is None else 1920)
    solution=solve2([(a,b)for a,b,d in inputs],n);assert solution is not None
    return dict(splits_over_real_signs=True,unknown_sign_bits=n,solution=solution,
        conclusion='A signed-monomial section exists; the initial larger generated group is a choice-of-lifts artifact.')

def verify_section_witness(section,generators,coefficients,matrices=None,central_bits=None):
    def word(w):
        p=tuple(range(27));L=[0]*27;A=np.eye(4,dtype=int)
        for j in w:
            L=[L[i]^(1<<(27*j+p[i]))for i in range(27)];p=tuple(generators[j][p[i]]for i in range(27))
            if matrices is not None:A=np.array(matrices[j])@A%5
        return p,L,A
    total_a=total_b=0
    for row in section['contradiction_rows']:
        desc=row['description'];kind=desc['kind']
        if kind=='cubic':
            j=desc['generator'];t=tuple(desc['triple']);p=generators[j]
            a=sum(1<<(27*j+i)for i in t);b=int(coefficients[t]!=coefficients[tuple(sorted(p[i]for i in t))])
        elif kind=='Cayley-edge':
            p,L,A=word(desc['left_word']);q,K,B=word(desc['right_word']);assert p==q
            if matrices is not None:assert np.array_equal(A,B)
            a=L[desc['coordinate']]^K[desc['coordinate']];b=0
        else:
            assert kind=='central'and matrices is not None
            p,L,A=word(desc['word']);assert p==tuple(range(27))and np.array_equal(A,-np.eye(4,dtype=int)%5)
            a=L[desc['coordinate']];b=central_bits[desc['coordinate']]
        assert a==int(row['coefficients_hex'],16)and b==row['rhs']
        total_a^=a;total_b^=b
    assert total_a==0 and total_b==1
    return True

def build():
    old=json.loads((ROOT/'data/w33_20261031_petersen_stabilizer.json').read_text())
    support=internal_e6_support(old['signed_five_dimensional_generators'])
    triples=[tuple(t)for t in support['cubic_support']]
    raw=(ROOT/'artifacts/canonical_su3_gauge_and_cubic.json').read_bytes()
    native={tuple(sorted(t['triple'])):int(t['sign'])for t in json.loads(raw)['solution']['d_triples']}
    def graph(ts,anchor):
        G=nx.Graph();G.add_nodes_from(range(27));G.add_edges_from((a,b)for t in ts for a,b in itertools.combinations(t,2))
        nx.set_node_attributes(G,{i:0 if i==anchor else 1 if G.has_edge(i,anchor)else 2 for i in G},'sector');return G
    W,N=graph(triples,0),graph(native,0)
    match=next(nx.isomorphism.GraphMatcher(W,N,node_match=lambda a,b:a['sector']==b['sector']).isomorphisms_iter())
    coefficients={t:native[tuple(sorted(match[i]for i in t))]for t in triples}
    assert {tuple(sorted(match[i]for i in t))for t in triples}==set(native)
    generators=[]
    for perm in support['generator_permutations']:
        rows=[(sum(1<<i for i in t),int(coefficients[t]!=coefficients[tuple(sorted(perm[i]for i in t))]))for t in triples]+[(1,0)]
        bits=solve2(rows,27);assert bits is not None
        assert all(coefficients[t]*(-1)**sum(bits[i]for i in t)==coefficients[tuple(sorted(perm[i]for i in t))]for t in triples)
        generators.append((tuple(perm),tuple(bits)))
    identity=(tuple(range(27)),(0,)*27);seen={identity};queue=[identity]
    for x in queue:
        for g in generators:
            y=mul(g,x)
            if y not in seen:seen.add(y);queue.append(y)
        assert len(seen)<=61440
    projected={p for p,b in seen};kernel=[b for p,b in seen if p==identity[0]]
    assert len(seen)==30720 and len(projected)==960 and len(kernel)==32
    section=section_test([p for p,b in generators],triples,coefficients)
    perms=[p for p,b in generators];central=[int(c==1)for c in support['charges']]
    cover=section_test(perms,triples,coefficients,old['symplectic_matrix_generators'],central)
    assert not section['splits_over_real_signs']and not cover['splits_over_real_signs']
    verify_section_witness(section,perms,coefficients)
    verify_section_witness(cover,perms,coefficients,old['symplectic_matrix_generators'],central)
    return dict(status='PASS_NATIVE_SIGNED_CUBIC_LIFT',signed_group_order=len(seen),unsigned_image_order=len(projected),diagonal_kernel_order=len(kernel),
        diagonal_kernel_sign_bits=sorted(kernel),weight_to_native=[match[i]for i in range(27)],
        native_cubic_sha256=hashlib.sha256(raw).hexdigest(),
        coefficient_rows=[dict(triple=t,coefficient=coefficients[t])for t in triples],
        signed_generators=[dict(permutation=p,sign_bits=b)for p,b in generators],
        signed_group_sha256=hashlib.sha256(json.dumps(sorted(seen),separators=(',',':')).encode()).hexdigest(),
        real_sign_section=section,unitary_double_cover_sign_lift=cover,
        prior='Pass11185 owns sector counts; w33_20261031_continuum_chirality.py owns the unsigned q5 transport. The 45 signs here are read from artifacts/canonical_su3_gauge_and_cubic.json, also used by TOE41.',
        boundary='A finite signed E6-cubic symmetry lift. Its kernel is a diagonal sign group, not the central +/-I kernel of the distinct 1920-element SU4 lift. No physical Yukawa values, complex-phase section classification, E8 coupling or vacuum derived.')

if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261031_signed_cubic_lift.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print(d['status'],d['signed_group_order'],d['real_sign_section']['conclusion'])
