"""Unrestricted exterior-arc equality is a binary conic-code question.

Coordinates below accept odd primes only. The counting/equality theorem in
the result is valid over every odd prime-power field. Code families are prior
art (Droms et al.; Sin--Wu--Xiang); no new dimension formula is asserted.
"""
import pathlib,json,itertools,hashlib
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[1]

def geometry(q):
    if q<3 or q%2==0 or any(q%d==0 for d in range(3,int(q**.5)+1,2)):raise ValueError('Odd primes only in this coordinate implementation')
    squares={a*a%q for a in range(1,q)}
    points=[(1,a,b)for a,b in itertools.product(range(q),repeat=2)]+[(0,1,a)for a in range(q)]+[(0,0,1)]
    exterior=[p for p in points if(p[1]*p[1]-p[0]*p[2])%q in squares]
    passants=[l for l in points if(l[1]*l[1]-4*l[0]*l[2])%q not in squares|{0}]
    H=(np.array(passants)@np.array(exterior).T)%q==0;n=(q+1)//2
    assert H.shape==(q*(n-1),q*n)and np.all(H.sum(0)==n-1)and np.all(H.sum(1)==n)
    return exterior,passants,H

def binary_kernel(H):
    basis={};n=H.shape[1]
    for row in H:
        a=sum(1<<int(i)for i in np.flatnonzero(row))
        while a:
            j=a.bit_length()-1
            if j not in basis:basis[j]=a;break
            a^=basis[j]
    vectors=[]
    for j in range(n):
        if j in basis:continue
        v=1<<j
        for i,row in sorted(basis.items()):
            if (row&v).bit_count()%2:v^=1<<i
        assert all((row&v).bit_count()%2==0 for row in basis.values());vectors.append(v)
    return len(basis),vectors

def verify_arc(q,points):
    squares={a*a%q for a in range(1,q)}
    for a,b in itertools.combinations(points,2):
        l=np.cross(a,b)%q;assert (int(l[1])**2-4*int(l[0])*int(l[2]))%q not in squares|{0}
    for a,b,c in itertools.combinations(points,3):assert int(np.dot(np.cross(a,b),c))%q
    return True

def build():
    known=json.loads((ROOT/'data/w33_20261031_exterior_search.json').read_text());rows=[]
    for q in (3,5,7,11,19,23,31):
        E,L,H=geometry(q);rank,kernel=binary_kernel(H);n=(q+1)//2
        row=dict(q=q,length=len(E),checks=len(L),binary_rank=rank,dimension=len(kernel),distance_lower_bound=n,
            incidence_sha256=hashlib.sha256(np.packbits(H,bitorder='little').tobytes()).hexdigest())
        if len(kernel)<=13:
            words=[0]
            for v in kernel:words.extend(w^v for w in list(words))
            weights=[w.bit_count()for w in words];distance=min(w for w in weights if w)
            row.update(exact_distance=distance,minimum_word_count=weights.count(distance),weight_enumerator={str(k):weights.count(k)for k in sorted(set(weights))})
            if distance==n:
                for w in words:
                    if w.bit_count()==n:verify_arc(q,[p for i,p in enumerate(E)if w>>i&1])
        hit=next((r for r in known if r['q']==q and r['status']=='found'),None)
        if hit:
            def norm(p):
                iv=pow(next(int(a)for a in p if a%q),-1,q);return tuple(int(a)*iv%q for a in p)
            poles=[]
            for a,b in hit['matching']:
                if a=='inf':a,b=b,a
                P=(2*a%q,1,0)if b=='inf'else(a*b%q,(a+b)*pow(2,-1,q)%q,1);poles.append(norm(P))
            indices=[E.index(p)for p in poles];word=np.zeros(len(E),dtype=int);word[indices]=1
            assert not np.any(H@word%2);verify_arc(q,poles)
            row.update(exact_distance=n,bound_equality_points=poles,bound_equality_indices=indices)
        rows.append(row)
    return dict(status='PROVED_ALL_FIELD_UNRESTRICTED_CODE_EQUIVALENCE',rows=rows,
        code='C_ext(q)=ker_F2 H, H=incidence(passant lines,external points) of a nondegenerate conic.',
        universal_bound='For every odd prime power q, any nonzero codeword has weight at least(q+1)/2.',
        bound_proof='An exterior point lies on(q-1)/2 passants. If selected in an even codeword, each of these lines needs another selected point. No other point can lie on two such lines, so there are at least(q-1)/2 other selected points.',
        equality_theorem='A weight(q+1)/2 codeword is exactly a complete exterior arc: equality gives precisely one other selected point on each passant through every selected point, so all joining lines are distinct passants and no three selected points are collinear. Conversely an exterior arc of that size exhausts all passants through each point, so every passant meets it in0 or2 points. The two conic tangents at each exterior point partition all q+1 conic tangent contacts, recovering the good matching.',
        significance='This equivalence places arbitrary matchings, without rational-degree restrictions, in a single binary linear code. An all-q arc exclusion is equivalent to strictness of this code-distance bound outside q=3,7,11.',
        prior='Conic incidence binary codes were constructed by Droms et al. and their dimensions studied by Sin--Wu--Xiang and others. The displayed finite ranks are exact computed controls, not a new general rank theorem. The lower bound is the standard no4-cycle parity-check counting bound; the explicit link to the present exterior-arc target is the purpose here.',
        literature=['https://arxiv.org/abs/0911.2018','https://doi.org/10.1016/j.jcta.2010.11.010','https://arxiv.org/abs/1104.0324'],
        boundary='Does not prove strictness of the distance bound for all larger q. Separate CP-SAT probes at19,23,31 timed out and are archived as UNKNOWN, not as exclusions. Prime-power coordinate extensions are not simulated using integer residues.')

if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261031_exterior_arc_code.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print(d['status'],[(r['q'],r.get('exact_distance'))for r in d['rows']])
