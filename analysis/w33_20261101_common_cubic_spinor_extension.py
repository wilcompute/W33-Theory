"""Smallest common extension for the prescribed cubic and spinor quotient maps.

Finite fibre products are standard. Minimality here is checked for these
actual maps using all Cayley edges and a six-variable sign-lift certificate.
"""
import pathlib,sys,json,itertools,hashlib
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1]

def signed_mul(g,x):
    p,a=g;q,b=x
    return tuple(p[q[i]] for i in range(27)),tuple(b[i]^a[q[i]] for i in range(27))

def gaussian(rows,n=6):
    basis={}
    for k,(a,b) in enumerate(rows):
        witness=1<<k
        while a:
            j=a.bit_length()-1
            if j not in basis:basis[j]=(a,b,witness);break
            c,d,w=basis[j];a^=c;b^=d;witness^=w
        else:
            if b:return None,[i for i in range(len(rows)) if witness>>i&1]
    solution=0
    for j,(a,b,w) in sorted(basis.items()):
        if ((solution&a).bit_count()&1)!=b:solution|=1<<j
    return solution,None

def evaluate(word,gens,mats):
    s=(tuple(range(27)),(0,)*27);A=np.eye(4,dtype=np.int16);parity=0
    for j in word:s=signed_mul(gens[j],s);A=mats[j]@A%5;parity^=1<<j
    return s,A,parity

def verify_witness(rows,gens,mats):
    total=rhs=0
    for row in rows:
        s,A,p=evaluate(row['left_word'],gens,mats);t,B,q=evaluate(row['right_word'],gens,mats)
        assert s==t and p^q==row['coefficient_mask']
        bit=0 if np.array_equal(A,B) else 1
        assert np.array_equal(A,(-1)**bit*B%5) and bit==row['rhs']
        total^=p^q;rhs^=bit
    assert total==0 and rhs==1
    return True

def build():
    cubic=json.loads((ROOT/'data/w33_20261031_signed_cubic_lift.json').read_text())
    geom=json.loads((ROOT/'data/w33_20261031_petersen_stabilizer.json').read_text())
    unitary=json.loads((ROOT/'data/w33_20261031_unitary_stabilizer_lift.json').read_text())
    gens=[(tuple(x['permutation']),tuple(x['sign_bits'])) for x in cubic['signed_generators']]
    mats=[np.array(A,dtype=np.int16) for A in geom['symplectic_matrix_generators']]
    coefficients={tuple(r['triple']):r['coefficient'] for r in cubic['coefficient_rows']}
    for p,b in gens:
        assert all(coefficients[t]*(-1)**sum(b[i] for i in t)==coefficients[tuple(sorted(p[i] for i in t))] for t in coefficients)
    identity=(tuple(range(27)),(0,)*27);I=np.eye(4,dtype=np.int16)
    # Each signed element gets one tree-word spinor lift and word parity.
    keys={identity:0};queue=[identity];lifts=[I];words=[[]];parities=[0]
    constraints={};edges=0;opposite_edge=None
    for ix,x in enumerate(queue):
        for j,g in enumerate(gens):
            y=signed_mul(g,x);A=mats[j]@lifts[ix]%5
            parity=parities[ix]^(1<<j);left=words[ix]+[j]
            if y not in keys:
                keys[y]=len(queue);queue.append(y);lifts.append(A);words.append(left);parities.append(parity)
            iy=keys[y];B=lifts[iy]
            bit=0 if np.array_equal(A,B) else 1
            assert np.array_equal(A,(-1)**bit*B%5)
            row=(parity^parities[iy],bit)
            constraints.setdefault(row,dict(coefficient_mask=row[0],rhs=bit,left_word=left,right_word=words[iy]))
            if bit and opposite_edge is None:opposite_edge=constraints[row]
            edges+=1
    assert len(queue)==30720 and edges==184320
    rowkeys=list(constraints);solution,bad=gaussian(rowkeys)
    witness=[] if bad is None else [constraints[rowkeys[i]] for i in bad]
    if bad is not None:verify_witness(witness,gens,mats)
    # All choices of generator central signs, independently of elimination.
    choices=[x for x in range(64) if all(((a&x).bit_count()&1)==b for a,b in rowkeys)]
    assert bool(choices)==(solution is not None)
    image_sizes=[]
    for x in choices:
        image_sizes.append(len({tuple(map(int,(((-1)**((parities[i]&x).bit_count()&1))*A%5).flat)) for i,A in enumerate(lifts)}))
    admits=any(n==1920 for n in image_sizes)
    minimum=30720 if admits else 61440
    # The fibre product itself is explicit: both +/- lifts over each signed
    # element. Every one of the184320 edges above verifies closure for both.
    assert opposite_edge is not None
    kernel=[b for p,b in queue if p==identity[0]];assert len(kernel)==32
    pgroup={p for p,b in queue}
    pcenter=[p for p in pgroup if all(tuple(p[g[i]] for i in range(27))==tuple(g[p[i]] for i in range(27)) for g,b in gens)]
    assert pcenter==[identity[0]]
    central=[b for b in kernel if all(tuple(b[p[i]] for i in range(27))==b for p,a in gens)]
    # Rebuild the1920 dyadic unitary lift alongside its actual F5 matrices.
    Ugens=[tuple(x) for x in unitary['generator_doubled_integer_keys']]
    U0=tuple(map(int,(2*I).flat))+(0,)*16
    ukeys={tuple(map(int,I.flat)):U0};uq=[I];pkeys={tuple(map(int,I.flat)):identity[0]}
    def umul(g,h):
        A=np.array(g[:16],dtype=int).reshape(4,4);B=np.array(g[16:],dtype=int).reshape(4,4)
        C=np.array(h[:16],dtype=int).reshape(4,4);D=np.array(h[16:],dtype=int).reshape(4,4)
        R=A@C-B@D;S=A@D+B@C
        assert not np.any(R%2) and not np.any(S%2)
        return tuple(map(int,(R//2).flat))+tuple(map(int,(S//2).flat))
    for A in uq:
        akey=tuple(map(int,A.flat));U=ukeys[akey];perm=pkeys[akey]
        for j,(G,V) in enumerate(zip(mats,Ugens)):
            B=G@A%5;k=tuple(map(int,B.flat));W=umul(V,U)
            image=tuple(gens[j][0][perm[i]] for i in range(27))
            if k not in ukeys:ukeys[k]=W;pkeys[k]=image;uq.append(B)
            else:assert ukeys[k]==W and pkeys[k]==image
    assert len(ukeys)==1920
    assert len(set(ukeys.values()))==1920 and len(set(pkeys.values()))==960
    minus=tuple(map(int,(-I%5).flat))
    assert ukeys[minus]==tuple(-x for x in U0) and pkeys[minus]==identity[0]
    assert {tuple(map(int,(s*A%5).flat)) for A in lifts for s in (1,-1)}==set(ukeys)
    assert sorted(sum(b) for b in central)==[0,16]
    for U in ukeys.values():
        A=np.array(U[:16]).reshape(4,4);B=np.array(U[16:]).reshape(4,4)
        assert np.array_equal(A.T@A+B.T@B,4*np.eye(4,dtype=int)) and not np.any(A.T@B-B.T@A)
    return dict(status='PASS_MINIMAL_COMMON_CUBIC_SPINOR_EXTENSION',
        signed_group_order=30720,unitary_group_order=1920,common_quotient_order=960,
        fibre_product_order=61440,minimum_common_extension_order=minimum,
        prescribed_quotient_maps=True,all_signed_Cayley_edges_checked=edges,
        central_generator_sign_choices_allowed=choices,allowed_lift_image_sizes=image_sizes,
        no_lift_integer_GF2_certificate=witness,central_kernel_generator_word_pair=opposite_edge,
        fibre_kernel_order=64,fibre_kernel_structure='C2^6',
        signed_central_kernel_elements=central,fibre_center_order=2*len(central),fibre_center_structure='C2 x C2',
        paired_signed_generators=cubic['signed_generators'],paired_GF5_generators=geom['symplectic_matrix_generators'],
        paired_unitary_dyadic_generators=Ugens,
        exact_unitary1920_sha256=hashlib.sha256(json.dumps(sorted(ukeys.values()),separators=(',',':')).encode()).hexdigest(),
        construction='H={(l,g): signed cubic element l and actual spinor element g have the same prescribed960 permutation image}. Enumerated30720 signed elements, with two actual unitary lifts each. Combined27+4 representation is faithful; the individual kernels are different.',
        minimality='Any compatible common cover maps into this fibre product. A subdirect image has order30720 or61440. The former exists exactly when the prescribed30720-to960 map lifts onto1920. All six generator signs and all Cayley relations are checked; the exported GF2 certificate independently excludes every choice when inconsistent.',
        boundary='Minimality is for these fixed quotient maps and these actual representations. No classification of arbitrary E6/nonmonomial embeddings, physical matter assignment, coupling, or TOE.')

if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261101_common_cubic_spinor_extension.json').write_text(json.dumps(d,indent=2)+'\n')
    print(d['status'],d['minimum_common_extension_order'],d['fibre_center_order'],flush=True)
