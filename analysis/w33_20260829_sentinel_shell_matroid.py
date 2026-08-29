#!/usr/bin/env python3
"""The minimum-word shell of the W33 sentinel is a 45-point binary matroid.

This independently rebuilds the 45 Hermitian/trade supports B and certifies:
- Hamming distance 16 between two minimum words is exactly GQ(4,2)
  collinearity (disjoint eight-supports); distance 12 is noncollinearity.
- the 720 noncollinear pairs have 720 distinct XORs and exhaust the complete
  weight-12 shell of the [40,15,8] sentinel code.
- the 45 columns have no binary dependency of size < 5 and exactly 216
  dependencies of size 5; these are therefore the 5-circuits of the column
  matroid.
- all 216 circuits are five-cocliques in GQ(4,2), form one PSp(4,3) orbit, and
  have stabilizer S5 of order 120.

The numerical equality 216 = |projective one-qutrit Clifford| is recorded only
as a comparison: this script proves a PSp(4,3)/S5 coset orbit, not an
identification with a Clifford group.
"""
from __future__ import annotations
import itertools, json
from collections import Counter, defaultdict, deque
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260829_SENTINEL_SHELL_MATROID.json'

def norm(v):
    i=next(k for k,x in enumerate(v) if x%3); z=pow(v[i]%3,-1,3)
    return tuple((z*x)%3 for x in v)

def form(u,v):
    return (u[0]*v[1]-u[1]*v[0]+u[2]*v[3]-u[3]*v[2])%3

def compose(p,q):
    return tuple(p[q[i]] for i in range(len(q)))

def geometry():
    pts=sorted({norm(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    idx={v:i for i,v in enumerate(pts)}; lines=set()
    for a,b in itertools.combinations(range(40),2):
        if form(pts[a],pts[b]): continue
        S=set()
        for s,t in itertools.product(range(3),repeat=2):
            if s==t==0: continue
            S.add(idx[norm(tuple((s*pts[a][k]+t*pts[b][k])%3 for k in range(4)))])
        if len(S)==4: lines.add(tuple(sorted(S)))
    lines=sorted(lines); assert len(pts)==len(lines)==40
    N=[[0]*40 for _ in range(40)]
    for li,L in enumerate(lines):
        for p in L:N[li][p]=1
    return pts,idx,N

def supports_from_N(N):
    cols=[tuple(N[l][p] for l in range(40)) for p in range(40)]
    sig=defaultdict(list)
    for S in itertools.combinations(range(40),4):
        z=tuple(sum(cols[p][l] for p in S) for l in range(40)); sig[z].append(S)
    pairs=sorted(tuple(sorted((tuple(v[0]),tuple(v[1])))) for v in sig.values() if len(v)==2)
    assert len(pairs)==45
    supports=[frozenset(set(a)|set(b)) for a,b in pairs]
    assert len(set(supports))==45 and {len(S) for S in supports}=={8}
    masks=[sum(1<<i for i in S) for S in supports]
    return supports,masks

def gf2_basis(vectors):
    piv={}
    for x in vectors:
        y=x
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    return list(piv.values())

def closure(gens,n):
    e=tuple(range(n)); G={e};Q=deque([e])
    while Q:
        a=Q.popleft()
        for g in gens:
            h=compose(g,a)
            if h not in G:G.add(h);Q.append(h)
    return G

def main():
    pts,idx,N=geometry(); supports,masks=supports_from_N(N)
    basis=gf2_basis(masks); assert len(basis)==15

    code=set()
    for c in range(1<<15):
        w=0
        for i,b in enumerate(basis):
            if (c>>i)&1:w^=b
        code.add(w)
    weight12={w for w in code if w.bit_count()==12}
    assert len(weight12)==720

    pair_sums={}; relation=Counter()
    for i,j in itertools.combinations(range(45),2):
        inter=len(supports[i]&supports[j]); assert inter in (0,2)
        d=(masks[i]^masks[j]).bit_count()
        assert d==(16 if inter==0 else 12)
        w=masks[i]^masks[j]
        assert w not in pair_sums
        pair_sums[w]=(i,j)
        relation['GQ_collinear_distance16' if inter==0 else 'GQ_noncollinear_distance12']+=1
    assert relation==Counter({'GQ_noncollinear_distance12':720,'GQ_collinear_distance16':270})
    pair12={w for w in pair_sums if w.bit_count()==12}
    assert pair12==weight12

    # Pair sums are unique, so there are no 4-circuits. Pair sums have weights
    # 12/16 rather than 8, so there are no 3-circuits either. Distinct nonzero
    # columns exclude 1/2-circuits. Enumerate the first possible shell.
    circuits=[]
    for C in itertools.combinations(range(45),5):
        w=0
        for i in C:w^=masks[i]
        if w==0:circuits.append(C)
    assert len(circuits)==216
    circuit_set=set(circuits)
    assert all(all(supports[i]&supports[j] for i,j in itertools.combinations(C,2)) for C in circuits)

    pair_circuit_degree=Counter()
    for C in circuits:
        for i,j in itertools.combinations(C,2):
            assert (masks[i]^masks[j]).bit_count()==12
            pair_circuit_degree[tuple(sorted((i,j)))]+=1
    nonedges={tuple(sorted((i,j))) for i,j in itertools.combinations(range(45),2)
              if (masks[i]^masks[j]).bit_count()==12}
    assert set(pair_circuit_degree)==nonedges
    assert set(pair_circuit_degree.values())=={3}

    # Exact PSp(4,3) action on the 45 supports. Four deterministic
    # transvections generate the full 25,920-element group in this ordering.
    gens40=[]
    for v in pts:
        for alpha in (1,2):
            p=[]
            for x in pts:
                z=alpha*form(x,v)%3
                y=norm(tuple((x[k]+z*v[k])%3 for k in range(4)))
                p.append(idx[y])
            gens40.append(tuple(p))
    si={S:i for i,S in enumerate(supports)}
    gens45=[]
    for p in gens40:
        q=tuple(si[frozenset(p[x] for x in S)] for S in supports)
        gens45.append(q)
    selected=[gens45[i] for i in (18,62,77,10)]
    G=closure(selected,45); assert len(G)==25920

    seed=circuits[0]
    def act(C,g): return tuple(sorted(g[i] for i in C))
    orbit={act(seed,g) for g in G}
    assert orbit==circuit_set
    stab=[g for g in G if act(seed,g)==seed]
    assert len(stab)==120
    pos={x:i for i,x in enumerate(seed)}
    induced={tuple(pos[g[x]] for x in seed) for g in stab}
    assert len(induced)==120

    out={
      'schema':'w33.20260829.sentinel-shell-matroid.v1','status':'PASS',
      'minimumWordGeometry':{
        'points':45,'wordWeight':8,
        'GQ42Adjacency':'distance 16 / disjoint supports',
        'GQ42Nonadjacency':'distance 12 / intersection size 2',
        'pairCounts':{'distance12':720,'distance16':270}},
      'weight12Shell':{
        'words':720,
        'theorem':'every weight-12 word is the XOR of a unique GQ-noncollinear pair of minimum words',
        'circuitsThroughPair':3},
      'binaryMatroid':{
        'rank':15,'girth':5,'fiveCircuits':216,
        'circuitGeometry':'every 5-circuit is a five-coclique in GQ(4,2)'},
      'groupAction':{
        'group':'PSp(4,3)','groupOrder':25920,
        'circuitOrbitSize':216,'stabilizerOrder':120,'stabilizerAction':'S5 faithfully on the five circuit elements',
        'cosetReading':'the 216 circuits realize the transitive PSp(4,3)/S5 action'},
      'boundary':'The 216-circuit orbit is not identified with the order-216 projective qutrit Clifford group; only the cardinality coincidence is noted. All asserted identifications are finite code/matroid/group-action statements.'
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','weight12':720,'girth':5,'circuits':216,'stabilizer':'S5'}))

if __name__=='__main__':main()
