#!/usr/bin/env python3
"""The E8 Coxeter C6 fiber quotient by C3 is the signed/antipodal W33 cover.

Parent:
  data/PART_W33_PASS7163_7170_E8_HEXAGONAL_LIFT.json

Pass 7164 gives 240 E8 roots partitioned into 40 Coxeter C6 fibers over W33.
This certificate quotients each C6 fiber by its order-three subgroup <r^2>.
Each six-root fiber splits into its two alternating triples:
  even phases {0,2,4}, odd phases {1,3,5}.
Hence there are 80 quotient objects, two over each W33 point. The central
half-turn r^3 swaps those two triples.

Compute, for every unordered pair of the 80 triples, the complete multiset of
the nine E8 root inner products between their members. Exactly three relation
types occur:

  antipode:      {-8^3,+4^6}, valency 1, 40 unordered pairs;
  commuting:     {0^9},       valency 24, 960 unordered pairs;
  noncommuting:  {-4^3,0^3,+4^3}, valency 54, 2160 unordered pairs.

Moreover:
- the valency-24 relation projects exactly to the Pass-7164 W33 adjacency;
  each adjacent base pair contributes all 2x2=4 sheet pairs;
- each nonadjacent base pair contributes all four sheet pairs to the
  valency-54 relation;
- the valency-1 relation is exactly the two alternating triples in one C6 fiber.

This is precisely the fused antipodal orthogonality cover of the canonical
signed two-qutrit Pauli set F3^4\{0} -> PG(3,3):
  one antipode -v, 24 other orthogonal vectors, 54 nonorthogonal vectors.

The identification is a COVER isomorphism, not a canonical signed section:
either sheet over each of the 40 projective points may be called + or -, giving
2^40 fiber gauges.  The E8 root-inner-product relation also fuses the two
nonzero symplectic products +1 and -1 into the 54-class.  A canonical
27+27 sign refinement remains open.

This closes exactly the count-level warning in Pass 103:
the E8 six-sheet phase bundle now has a proved intermediate 80-state
antipodal cover
  240 --/C3--> 80 --/C2--> 40,
but not yet a canonical identification of its phase orientation with the
symplectic sign on Pauli vectors.
"""
from __future__ import annotations
import itertools, json
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_e8_c3_quotient_signed_pauli_cover.json'

SIMPLES=[
(1,-1,-1,-1,-1,-1,-1,1),
(2,2,0,0,0,0,0,0),
(-2,2,0,0,0,0,0,0),
(0,-2,2,0,0,0,0,0),
(0,0,-2,2,0,0,0,0),
(0,0,0,-2,2,0,0,0),
(0,0,0,0,-2,2,0,0),
(0,0,0,0,0,-2,2,0)]

def dot(a,b):return sum(x*y for x,y in zip(a,b))

def roots_e8():
    R=[]
    for i,j in itertools.combinations(range(8),2):
        for si in (1,-1):
            for sj in (1,-1):
                x=[0]*8;x[i]=2*si;x[j]=2*sj;R.append(tuple(x))
    for bits in itertools.product((1,-1),repeat=8):
        if sum(x==-1 for x in bits)%2==0:R.append(tuple(bits))
    assert len(R)==len(set(R))==240
    return R

def refl(x,r):
    q=dot(x,r);assert q%4==0;k=q//4
    return tuple(x[i]-k*r[i] for i in range(8))

def cox(x):
    y=x
    for r in SIMPLES:y=refl(y,r)
    return y

def signature(R,A,B):
    return tuple(sorted(Counter(dot(R[i],R[j]) for i in A for j in B).items()))

def symp(v,w):
    return (v[0]*w[2]+v[1]*w[3]-v[2]*w[0]-v[3]*w[1])%3

def canon(v):
    nz=next(x for x in v if x)
    return tuple((2*x)%3 for x in v) if nz==2 else tuple(v)

def main(write=True):
    R=roots_e8();I={r:i for i,r in enumerate(R)}
    cp=[I[cox(r)] for r in R]

    # d=c^5 has order six on every root.
    d=list(range(240))
    for _ in range(5):d=[cp[i] for i in d]
    seen=set();fib=[]
    for i in range(240):
        if i in seen:continue
        o=[];j=i
        while j not in o:
            o.append(j);seen.add(j);j=d[j]
        assert len(o)==6
        fib.append(tuple(o))
    assert len(fib)==40

    # Verify central half-turn = root negation.
    for F in fib:
        for k in range(6):
            assert R[F[(k+3)%6]]==tuple(-x for x in R[F[k]])

    triples=[];base_sheet=[]
    for f,F in enumerate(fib):
        triples.append(tuple(F[k] for k in (0,2,4)));base_sheet.append((f,0))
        triples.append(tuple(F[k] for k in (1,3,5)));base_sheet.append((f,1))
    assert len(triples)==80

    # Base W33 adjacency from Pass7164: no +4 E8 root-graph edges.
    badj=[set() for _ in range(40)]
    for a,b in itertools.combinations(range(40),2):
        E=sum(1 for u in fib[a] for v in fib[b] if dot(R[u],R[v])==4)
        if E==0:
            badj[a].add(b);badj[b].add(a)
        else:
            assert E==12
    assert all(len(x)==12 for x in badj)
    for a,b in itertools.combinations(range(40),2):
        assert len(badj[a]&badj[b])==(2 if b in badj[a] else 4)

    sig_counts=Counter();val=defaultdict(Counter);pairs_by_sig=defaultdict(list)
    for a,b in itertools.combinations(range(80),2):
        s=signature(R,triples[a],triples[b])
        sig_counts[s]+=1;val[a][s]+=1;val[b][s]+=1;pairs_by_sig[s].append((a,b))
    assert len(sig_counts)==3

    antip=(( -8,3),(4,6))
    commute=((0,9),)
    noncomm=((-4,3),(0,3),(4,3))
    assert sig_counts[antip]==40
    assert sig_counts[commute]==960
    assert sig_counts[noncomm]==2160
    for i in range(80):
        assert val[i][antip]==1 and val[i][commute]==24 and val[i][noncomm]==54

    # Antipode is exactly the other C3 orbit in the same C6 fiber.
    assert set(tuple(sorted((2*f,2*f+1))) for f in range(40))==set(pairs_by_sig[antip])

    # Every base adjacent pair contributes all four sheet pairs to commute;
    # every base nonedge contributes all four to noncommute.
    for a,b in itertools.combinations(range(40),2):
        S={signature(R,triples[2*a+sa],triples[2*b+sb])
           for sa in (0,1) for sb in (0,1)}
        assert len(S)==1
        only=next(iter(S))
        assert only==(commute if b in badj[a] else noncomm)

    # Canonical signed Pauli cover has the same fused relation valencies.
    V=[v for v in itertools.product(range(3),repeat=4) if any(v)]
    assert len(V)==80
    pc=Counter()
    for v in V:
        c=Counter()
        for w in V:
            if w==v:continue
            if w==tuple((-x)%3 for x in v):c['antipode']+=1
            elif symp(v,w)==0:c['commuting']+=1
            else:c['noncommuting']+=1
        pc[tuple(sorted(c.items()))]+=1
    assert pc==Counter({(('antipode',1),('commuting',24),('noncommuting',54)):80})

    # Projective signed-Pauli adjacency has the W33 parameters.
    PP=sorted({canon(v) for v in V})
    padj={p:{q for q in PP if q!=p and symp(p,q)==0} for p in PP}
    assert len(PP)==40 and all(len(x)==12 for x in padj.values())

    out={
      'schema':'w33.e8_c3_quotient_signed_pauli_cover.v1',
      'status':'PASS',
      'headline':'Quotienting each Pass-7164 E8 Coxeter C6 fiber by its C3 subgroup gives 80 alternating root triples in a 240->80->40 tower. Their exact E8 inner-product association has valencies 1,24,54: the 1-relation is the C6 half-turn antipode, the 24-relation projects exactly to W33 adjacency, and the 54-relation projects to W33 nonadjacency. This is gauge-isomorphic to the fused antipodal orthogonality cover of the 80 nonzero two-qutrit Pauli vectors.',
      'tower':{
        'E8_roots':240,'C6_fibers':40,'C3_orbits_per_fiber':2,
        'intermediate_objects':80,'base_W33_points':40,
        'quotients':'240 --/<r^2>=C3--> 80 --/<r^3>=C2--> 40'},
      'relations':{
        'antipode':{'inner_product_signature':{'-8':3,'4':6},'unordered_pairs':40,'valency':1},
        'commuting':{'inner_product_signature':{'0':9},'unordered_pairs':960,'valency':24},
        'noncommuting':{'inner_product_signature':{'-4':3,'0':3,'4':3},'unordered_pairs':2160,'valency':54}},
      'projection':{
        'base_relation':'Pass-7164 W33 adjacency = fiber pairs with zero +4 root-graph edges',
        'adjacent_base_pair':'all four sheet pairs lie in the valency-24 relation',
        'nonadjacent_base_pair':'all four sheet pairs lie in the valency-54 relation',
        'same_base_point':'the two sheets are the valency-1 antipodal pair'},
      'signed_Pauli_comparison':{
        'carrier':'F3^4 minus {0}',
        'projectivization':'F3^x=C2 -> 80 -> PG(3,3)=40',
        'per_vector_relations':{'antipode':1,'other_commuting':24,'noncommuting_fused':54},
        'cover_isomorphism':'exists fiberwise over the already-certified W33 base; 2^40 choices of sign section',
        'canonical_sign_section':False},
      'boundary':{
        'proved':'antipodal/orthogonality cover and 240->80->40 factorization',
        'open':'refine the 54 noncommuting class into the two symplectic-sign classes 27+27 equivariantly; identify an E8 phase orientation with the Pauli +/- symplectic product',
        'do_not_conflate':'the internal E8 Coxeter-fiber C6 and the heterotic/Clifford CZ-parity C6 are distinct actions unless a future equivariant theorem identifies them'},
      'parents':['data/PART_W33_PASS7163_7170_E8_HEXAGONAL_LIFT.json','w33_pass122_hopf_synthesis.py']
    }
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
    return out

if __name__=='__main__':main(True)
