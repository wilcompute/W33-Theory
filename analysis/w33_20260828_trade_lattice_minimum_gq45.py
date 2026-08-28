#!/usr/bin/env python3
"""Deep structure of the W33 near-ovoid trade lattice.

The previously proved lattice is ker_Z(N), rank 15.  This pass determines its
shortest vectors and identifies them with an older exact W33 object.

Results proved here:
* minimum squared norm is 8;
* there are 90 signed minima, hence 45 antipodal minimum-vector lines;
* the 45 lines are exactly the 45 dual flat-tetrad pairs from the historical
  flat-curvature construction;
* their orthogonality graph is SRG(45,12,3,3), the GQ(4,2) carrier, while the
  nonorthogonality graph is SRG(45,32,22,24);
* PSp(4,3) is transitive on the 45 unsigned minima and on the 90 signed minima;
  stabilizers have orders 576 and 288 respectively;
* the 45 canonical minima already generate the full integral kernel, with
  discriminant group (Z/2)^5 x (Z/6)^9 x Z/24 and determinant 2^17 3^10;
* every one of the 7,200 local near-ovoid pair trades has a UNIQUE expression
  as a sum of two signed minimum vectors.  There are 720 distinct directed
  representatives in the frozen solution ordering, each occurring ten times.

The real span is the old E15 carrier: 24 P_{-4}=8I+J-4A.  This pass supplies
its intrinsic integral lattice and its minimum-vector geometry.
"""
from __future__ import annotations
import itertools,json,hashlib,math
from collections import Counter,defaultdict,deque
from pathlib import Path
from sympy import Matrix,ZZ
from sympy.matrices.normalforms import smith_normal_form,hermite_normal_form
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_20260828_TRADE_LATTICE_MINIMUM_GQ45.json'
Q=3

def norm(v):
    i=next(k for k,x in enumerate(v) if x%3);z=pow(v[i]%3,-1,3)
    return tuple((z*x)%3 for x in v)
def form(u,v):return (u[0]*v[1]-u[1]*v[0]+u[2]*v[3]-u[3]*v[2])%3

def geometry():
    pts=sorted({norm(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    idx={v:i for i,v in enumerate(pts)};lines=set()
    for a,b in itertools.combinations(range(40),2):
        if form(pts[a],pts[b]):continue
        S=set()
        for s,t in itertools.product(range(3),repeat=2):
            if s==t==0:continue
            S.add(idx[norm(tuple((s*pts[a][k]+t*pts[b][k])%3 for k in range(4)))])
        if len(S)==4:lines.add(tuple(sorted(S)))
    return pts,idx,sorted(lines)

def solve_target(lines,pls,target):
    allowed={p for p in range(40) if all(target[l]>0 for l in pls[p])}
    cand=[[p for p in L if p in allowed] for L in lines];cnt=[0]*40;chosen=[];inside=[False]*40;sol=set()
    def rec():
        if len(chosen)>10:return
        unmet=[]
        for l,t in enumerate(target):
            if cnt[l]>t:return
            need=t-cnt[l]
            if need:
                F=[p for p in cand[l] if not inside[p] and all(cnt[j]<target[j] for j in pls[p])]
                if len(F)<need:return
                unmet.append((len(F),-need,l,F))
        if not unmet:
            if len(chosen)==10:sol.add(tuple(sorted(chosen)))
            return
        _,ng,_,F=min(unmet);need=-ng
        for sub in itertools.combinations(F,need):
            d=Counter()
            for p in sub:
                for j in pls[p]:d[j]+=1
            if any(cnt[j]+z>target[j] for j,z in d.items()):continue
            for p in sub:chosen.append(p);inside[p]=True
            for j,z in d.items():cnt[j]+=z
            rec()
            for j,z in d.items():cnt[j]-=z
            for _ in sub:inside[chosen.pop()]=False
    rec();return sorted(sol)

def srg(G):
    deg={len(x) for x in G};la=set();mu=set()
    for i,j in itertools.combinations(range(len(G)),2):
        c=len(G[i]&G[j]);(la if j in G[i] else mu).add(c)
    return [len(G),sorted(deg),sorted(la),sorted(mu)]
def sha(x):return hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()
def compose(p,q):return tuple(p[q[i]] for i in range(len(q)))

def main():
    pts,idx,lines=geometry();assert len(pts)==len(lines)==40
    N=[[0]*40 for _ in range(40)];pls=[[] for _ in range(40)]
    for l,L in enumerate(lines):
        for p in L:N[l][p]=1;pls[p].append(l)
    cols=[tuple(N[l][p] for l in range(40)) for p in range(40)]

    # Norm < 8 is impossible.  Since Nx=0 implies sum(x)=0 and |x_i|<=2,
    # the only zero-sum profiles below norm 8 are k +1s versus k -1s for
    # k=1,2,3, or one +/-2 versus two -/+1s.  The required column-sum
    # equalities are excluded by the following exact signature census.
    sigs={}
    for k in (1,2,3,4):
        d=defaultdict(list)
        for S in itertools.combinations(range(40),k):
            z=tuple(sum(cols[p][l] for p in S) for l in range(40));d[z].append(S)
        sigs[k]=d
    assert all(max(map(len,sigs[k].values()))==1 for k in (1,2,3))
    assert not any(tuple(2*z for z in cols[p]) in sigs[2] for p in range(40))
    collisions=[v for v in sigs[4].values() if len(v)>1]
    assert Counter(map(len,collisions))==Counter({2:45})
    assert all(not (set(a)&set(b)) for a,b in collisions)
    pairs=sorted(tuple(sorted((tuple(a),tuple(b)))) for a,b in collisions)
    mins=[]
    for a,b in pairs:
        v=tuple(1 if i in b else -1 if i in a else 0 for i in range(40))
        assert sum(z*z for z in v)==8 and all(sum(N[l][p]*v[p] for p in range(40))==0 for l in range(40))
        mins.append(v)

    # Historical flat-curvature tetrads, reconstructed independently.
    A=[[0]*40 for _ in range(40)]
    for i,j in itertools.combinations(range(40),2):
        if any(N[l][i] and N[l][j] for l in range(40)):A[i][j]=A[j][i]=1
    centers={}
    for t in itertools.combinations(range(40),3):
        if all(not A[a][b] for a,b in itertools.combinations(t,2)):
            centers[t]=tuple(x for x in range(40) if all(A[x][a] for a in t))
    assert Counter(map(len,centers.values()))==Counter({1:2880,4:360})
    flat=[t for t,c in centers.items() if len(c)==4]
    tetrads=sorted({tuple(sorted(centers[t])) for t in flat});assert len(tetrads)==90
    invol={}
    for T in tetrads:
        images={tuple(sorted(centers[tuple(sorted(s))])) for s in itertools.combinations(T,3)}
        assert len(images)==1;invol[T]=next(iter(images))
    oldpairs=sorted({tuple(sorted((T,invol[T]))) for T in tetrads})
    assert len(oldpairs)==45 and oldpairs==pairs

    # Projective minimum-vector graph.
    Orth=[set() for _ in range(45)];dotdist=Counter()
    for i,j in itertools.combinations(range(45),2):
        dot=sum(mins[i][k]*mins[j][k] for k in range(40));dotdist[dot]+=1
        Ui=set(pairs[i][0])|set(pairs[i][1]);Uj=set(pairs[j][0])|set(pairs[j][1])
        assert (dot==0)==(not (Ui&Uj))
        if dot==0:Orth[i].add(j);Orth[j].add(i)
    assert srg(Orth)==[45,[12],[3],[3]]
    Non=[set(range(45))-{i}-Orth[i] for i in range(45)]
    assert srg(Non)==[45,[32],[22],[24]]

    # The minima themselves generate the full primitive rank-15 kernel.
    M=Matrix(mins);D=smith_normal_form(M,domain=ZZ)
    diag=[abs(int(D[i,i])) for i in range(min(D.shape)) if D[i,i]!=0]
    assert diag==[1]*15
    H=hermite_normal_form(M.T);B=H.T;G=B*B.T
    assert B.shape==(15,40)
    disc=int(G.det());assert disc==2**17*3**10
    DG=smith_normal_form(G,domain=ZZ)
    discdiag=[abs(int(DG[i,i])) for i in range(15)]
    assert Counter(discdiag)==Counter({2:5,6:9,24:1})
    basis=[[int(x) for x in B.row(i)] for i in range(15)]
    gram=[[int(G[i,j]) for j in range(15)] for i in range(15)]

    # PSp(4,3) orbits and the 576 stabilizer.
    gens=[]
    for v in pts:
        for a in (1,2):
            perm=[]
            for x in pts:
                c=a*form(x,v)%3;y=norm(tuple((x[k]+c*v[k])%3 for k in range(4)))
                perm.append(idx[y])
            gens.append(tuple(perm))
    ident=tuple(range(40));grp={ident};q=deque([ident])
    while q:
        p=q.popleft()
        for g in gens:
            h=compose(g,p)
            if h not in grp:grp.add(h);q.append(h)
    assert len(grp)==25920
    def aset(p,S):return tuple(sorted(p[i] for i in S))
    def apair(p,z):return tuple(sorted((aset(p,z[0]),aset(p,z[1]))))
    def avec(p,v):
        w=[0]*40
        for i,z in enumerate(v):w[p[i]]=z
        return tuple(w)
    uorb={apair(p,pairs[0]) for p in grp};sorb={avec(p,mins[0]) for p in grp}
    assert len(uorb)==45 and set(uorb)==set(pairs) and len(sorb)==90
    ustab=sum(apair(p,pairs[0])==pairs[0] for p in grp);sstab=sum(avec(p,mins[0])==mins[0] for p in grp)
    assert ustab==576 and sstab==288

    # Every local near-ovoid pair trade splits uniquely into two minima.
    signed=set(mins)|{tuple(-z for z in v) for v in mins}
    pairtrades=[]
    for a in range(40):
        for b in range(40):
            if a==b:continue
            Hinge=set(pls[a])&set(pls[b])
            if len(Hinge)!=1:continue
            h=next(iter(Hinge));target=[1]*40
            for l in set(pls[a])-{h}:target[l]=0
            for l in set(pls[b])-{h}:target[l]=2
            sols=solve_target(lines,pls,target);assert len(sols)==6
            for X,Y in itertools.combinations(sols,2):
                sx=set(X);sy=set(Y);d=tuple(int(i in sy)-int(i in sx) for i in range(40))
                assert sum(z*z for z in d)==12
                n=sum(tuple(d[i]-v[i] for i in range(40)) in signed for v in signed)//2
                assert n==1
                pairtrades.append(d)
    assert len(pairtrades)==7200
    mult=Counter(pairtrades);assert len(mult)==720 and set(mult.values())=={10}

    out={
      'schema':'w33.20260828.trade-lattice-minimum-gq45.v1','status':'PASS',
      'lattice':{'rank':15,'minimum_squared_norm':8,'signed_minima':90,'projective_minimum_lines':45,
                 'minimum_generators_smith':'1^15','determinant':disc,'determinant_factorization':'2^17 * 3^10',
                 'discriminant_group':'(Z/2)^5 x (Z/6)^9 x Z/24',
                 'hnf_basis_sha256':sha(basis),'gram_sha256':sha(gram)},
      'minimum_geometry':{'exact_historical_object':'45 dual flat-tetrad pairs','dot_distribution':dict(sorted(dotdist.items())),
                          'orthogonality_graph':[45,12,3,3],'nonorthogonality_graph':[45,32,22,24],
                          'unsigned_PSp_orbit':45,'unsigned_stabilizer':ustab,
                          'signed_PSp_orbit':90,'signed_stabilizer':sstab},
      'near_ovoid_trade_factorization':{'local_pair_trades':7200,'distinct_frozen_oriented_vectors':720,
                                        'multiplicity_each':10,'unique_sum_of_two_minima':True,
                                        'inner_product_of_the_two_minima':-2},
      'E15_identification':'The real span is exactly the historical E15 carrier because 24 P_{-4}=8I+J-4A; this pass supplies its primitive integral form and minimum-vector geometry.',
      'theorem':'The W33 near-ovoid trade lattice is the primitive rank-15 E_{-4} lattice of determinant 2^17 3^10 and minimum 8. Its 45 antipodal minimum-vector lines are exactly the old 45 dual flat-tetrad pairs; orthogonality is the GQ(4,2) graph. PSp(4,3) has unsigned stabilizer 576. Every local near-ovoid trade factors uniquely through an edge of the complementary 45-state graph as a sum of two minima.',
      'boundary':'The GQ(4,2) identification is an exact finite incidence/lattice statement. No physical Hilbert-space interpretation is inferred.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','min_norm':8,'minima':90,'GQ45':True,'stabilizer':576,'trades':7200,'disc':disc}))
if __name__=='__main__':main()
