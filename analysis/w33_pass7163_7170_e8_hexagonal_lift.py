#!/usr/bin/env python3
"""Pass7163--7170: q9 boundary + E8 hexagonal lift + D4/center-quad dictionary.

Exact finite statements. Prior-art dependencies are named explicitly:
- Pass85: C2(W33)=[40,16,8] and 45 weight-8/tritangent words.
- Pass1021: 240 E8 roots -> 40 W33 points, six-root Eisenstein fibers.
- center-quad bridge: 90 center-quads -> 45 pairs -> 27 GQ(4,2) lines.
New here: exact cross-fiber E8 root graph law, lifted [240,16,48] code,
objectwise D4=center-quad identification, D4+D4 pair dictionary, Z12 holonomy,
and q9 rank-one boundary closure.
"""
from __future__ import annotations
import itertools, json
from collections import Counter
from pathlib import Path
from fractions import Fraction

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_W33_PASS7163_7170_E8_HEXAGONAL_LIFT.json'

# ---------------- GF(9), encoding a+bi as a+3b, i^2=2 ----------------
ADD=[[0]*9 for _ in range(9)]; MUL=[[0]*9 for _ in range(9)]
for x in range(9):
    a,b=x%3,x//3
    for y in range(9):
        c,d=y%3,y//3
        ADD[x][y]=((a+c)%3)+3*((b+d)%3)
        MUL[x][y]=((a*c+2*b*d)%3)+3*((a*d+b*c)%3)
NEG=[((-x%3)%3)+3*((-(x//3))%3) for x in range(9)]
INV={x:next(y for y in range(1,9) if MUL[x][y]==1) for x in range(1,9)}
def ga(a,b):return ADD[a][b]
def gm(a,b):return MUL[a][b]
def gn(a):return NEG[a]
def gsum(xs):
    z=0
    for x in xs:z=ga(z,x)
    return z
def norm9(v):
    z=INV[next(x for x in v if x)]
    return tuple(gm(z,x) for x in v)
def B9(u,v):
    return ga(ga(gm(u[0],v[1]),gn(gm(u[1],v[0]))),ga(gm(u[2],v[3]),gn(gm(u[3],v[2]))))
def invmat9(M):
    n=len(M); A=[list(M[i])+[1 if i==j else 0 for j in range(n)] for i in range(n)]
    for c in range(n):
        r=next(i for i in range(c,n) if A[i][c]);A[c],A[r]=A[r],A[c]
        z=INV[A[c][c]];A[c]=[gm(z,x) for x in A[c]]
        for i in range(n):
            if i!=c and A[i][c]:
                f=A[i][c];A[i]=[ga(A[i][j],gn(gm(f,A[c][j]))) for j in range(2*n)]
    return [r[n:] for r in A]
def canon3(t):
    out=[]
    def gp(a,n):
        z=1
        while n:
            if n&1:z=gm(z,a)
            a=gm(a,a);n//=2
        return z
    for perm in set(itertools.permutations(range(3))):
        u=tuple(t[i] for i in perm)
        for frob in (0,1):
            w=tuple(gp(x,3) if frob else x for x in u)
            z=INV[next(x for x in w if x)]
            out.append(tuple(gm(z,x) for x in w))
    return min(out)
def canonical_G(rep):
    x,y,z=rep
    return [[0,1,1,1],[2,0,z,gn(y)],[2,gn(z),0,x],[2,y,gn(x),0]]
def pairv(r,Gi,s):
    tmp=[gsum(gm(r[k],Gi[k][j]) for k in range(4)) for j in range(4)]
    return gn(gsum(gm(tmp[j],s[j]) for j in range(4)))
def rankstate(r):return 1 if r[3]==gm(r[1],r[2]) else 2
TYPES=[(1,1,2),(1,1,3),(1,1,4),(1,1,5),(1,2,3),(1,2,4),(1,3,4),(1,3,5)]
STATES=[(1,a,b,c) for a in range(1,9) for b in range(1,9) for c in range(1,9)]

def max_clique_bit(adj):
    n=len(adj);best=[]
    def color_sort(P):
        order=[];bounds=[];color=0;U=P
        while U:
            color+=1;Q=U
            while Q:
                bit=Q&-Q;v=bit.bit_length()-1
                order.append(v);bounds.append(color);U&=~bit;Q&=~bit;Q&=~adj[v]
        return order,bounds
    def expand(R,P):
        nonlocal best
        if not P:
            if len(R)>len(best):best=R[:]
            return
        order,bounds=color_sort(P)
        for k in range(len(order)-1,-1,-1):
            v=order[k]
            if len(R)+bounds[k]<=len(best):return
            bit=1<<v
            if not(P&bit):continue
            expand(R+[v],P&adj[v]);P&=~bit
    expand([], (1<<n)-1)
    return best

def q9_boundary():
    rank1=[i for i,r in enumerate(STATES) if rankstate(r)==1]
    assert len(rank1)==64
    rows={}
    for rep in TYPES:
        Gi=invmat9(canonical_G(rep)); deg=[0]*512; prof=[[0,0] for _ in range(512)]
        for i,j in itertools.combinations(range(512),2):
            if pairv(STATES[i],Gi,STATES[j])==0:
                deg[i]+=1;deg[j]+=1;ri=rankstate(STATES[i])-1;rj=rankstate(STATES[j])-1
                prof[i][rj]+=1;prof[j][ri]+=1
        m=len(rank1); comp=[0]*m
        for a in range(m):
            for b in range(a+1,m):
                i,j=rank1[a],rank1[b]
                if pairv(STATES[i],Gi,STATES[j])!=0:
                    comp[a]|=1<<b;comp[b]|=1<<a
        best=max_clique_bit(comp)
        joint=Counter((rankstate(STATES[i]),deg[i]) for i in range(512))
        rows[str(rep)]={
          'conflict_edges':sum(deg)//2,
          'degree_distribution':{str(k):v for k,v in sorted(Counter(deg).items())},
          'rank_degree_distribution':{f'rank{r}_deg{d}':n for (r,d),n in sorted(joint.items())},
          'rank1_independence_number_exact':len(best),
          'rank1_witness_state_indices':[rank1[x] for x in best],
        }
    expected=[21,25,22,25,23,24,21,26]
    assert [rows[str(r)]['rank1_independence_number_exact'] for r in TYPES]==expected
    S9=[22,24,78,80,88,95,141,144,149,177,182,189,190,191,200,213,214,230,234,258,271,276,288,331,336,364,368,376,397,403,449,450,478,480,539,561,570,580,588,622,651,655,658,741,750,753,756,780,784,801,814]
    P=sorted({norm9(v) for v in itertools.product(range(9),repeat=4) if any(v)})
    W=[P[i] for i in S9]; anchors=[0,1,2,5]
    Gold=[[B9(W[i],W[j]) for j in anchors] for i in anchors]
    trip=(gm(Gold[0][1],Gold[2][3]),gm(Gold[0][2],Gold[3][1]),gm(Gold[0][3],Gold[1][2]))
    assert canon3(trip)==(1,3,5)
    Gc=canonical_G((1,3,5)); solutions=[]
    for perm in itertools.permutations(range(4)):
      for d1,d2,d3 in itertools.product(range(1,9),repeat=3):
        ds=(1,d1,d2,d3)
        lhs=gm(ds[0],gm(ds[1],Gold[perm[0]][perm[1]])); c=gm(lhs,INV[Gc[0][1]])
        ok=True
        for i in range(4):
          for j in range(4):
            if gm(ds[i],gm(ds[j],Gold[perm[i]][perm[j]])) != gm(c,Gc[i][j]):ok=False;break
          if not ok:break
        if ok:solutions.append((perm,ds,c))
    assert solutions
    counts=set()
    for perm,ds,c in solutions:
        rr=[]
        for i in range(51):
            if i in anchors:continue
            old=[B9(W[i],W[a]) for a in anchors]
            new=[gm(ds[j],old[perm[j]]) for j in range(4)]
            z=INV[new[0]]; state=tuple(gm(z,x) for x in new);assert state in STATES;rr.append(rankstate(state))
        counts.add((rr.count(1),rr.count(2)))
    assert counts=={(5,42)}
    return {
      'anchor_cases':rows,
      'rank_partition':'512=64 rank-one + 448 invertible',
      'known_51_residual_anchor_type':'(1,3,5)',
      'known_47_residual_rank_split':{'rank1':5,'rank2':42},
      'global_q9_decision':'OPEN here; rank-one boundary closure does not prove residual alpha<=47.'
    }

def roots_e8():
    R=[]
    for i,j in itertools.combinations(range(8),2):
        for si in (1,-1):
          for sj in (1,-1):
            x=[0]*8;x[i]=2*si;x[j]=2*sj;R.append(tuple(x))
    for bits in itertools.product((1,-1),repeat=8):
        if sum(x==-1 for x in bits)%2==0:R.append(tuple(bits))
    assert len(R)==240 and len(set(R))==240
    return R
def dot(a,b):return sum(x*y for x,y in zip(a,b))
SIMPLES=[(1,-1,-1,-1,-1,-1,-1,1),(2,2,0,0,0,0,0,0),(-2,2,0,0,0,0,0,0),(0,-2,2,0,0,0,0,0),(0,0,-2,2,0,0,0,0),(0,0,0,-2,2,0,0,0),(0,0,0,0,-2,2,0,0),(0,0,0,0,0,-2,2,0)]
def refl(x,r):
    q=dot(x,r);assert q%4==0;k=q//4
    return tuple(x[i]-k*r[i] for i in range(8))
def cox(x):
    y=x
    for r in SIMPLES:y=refl(y,r)
    return y

def e8_fibers():
    R=roots_e8();I={r:i for i,r in enumerate(R)}
    cp=[I[cox(r)] for r in R]
    z=list(range(240))
    for _ in range(15):z=[cp[i] for i in z]
    assert all(R[z[i]]==tuple(-x for x in R[i]) for i in range(240))
    d=list(range(240))
    for _ in range(5):d=[cp[i] for i in d]
    seen=set();fib=[]
    for i in range(240):
        if i in seen:continue
        o=[];j=i
        while j not in o:o.append(j);seen.add(j);j=d[j]
        assert len(o)==6;fib.append(tuple(o))
    assert len(fib)==40
    radj=[set() for _ in R]
    for i,j in itertools.combinations(range(240),2):
        if dot(R[i],R[j])==4:radj[i].add(j);radj[j].add(i)
    assert all(len(x)==56 for x in radj)
    phase=[{v:k for k,v in enumerate(F)} for F in fib]
    zero=[];twelve=[];diffhist=Counter();cyc=Counter()
    for a,b in itertools.combinations(range(40),2):
        E=[(u,v) for u in fib[a] for v in fib[b] if v in radj[u]]
        if not E:zero.append((a,b));continue
        assert len(E)==12;twelve.append((a,b))
        da=Counter(u for u,v in E);db=Counter(v for u,v in E);assert set(da.values())=={2} and set(db.values())=={2}
        D={ (phase[b][v]-phase[a][u])%6 for u,v in E}; assert len(D)==2
        s=next(x for x in D if (x+1)%6 in D);diffhist[(s,(s+1)%6)]+=1
        V=set(fib[a])|set(fib[b]);NN={x:set() for x in V}
        for u,v in E:NN[u].add(v);NN[v].add(u)
        comps=[];un=set(V)
        while un:
            st=[un.pop()];C=set(st)
            while st:
                x=st.pop()
                for y in NN[x]:
                    if y in un:un.remove(y);C.add(y);st.append(y)
            comps.append(len(C))
        cyc[tuple(sorted(comps))]+=1
    assert len(zero)==240 and len(twelve)==540 and cyc==Counter({(12,):540})
    base_adj=[set() for _ in range(40)]
    for a,b in zero:base_adj[a].add(b);base_adj[b].add(a)
    assert all(len(x)==12 for x in base_adj)
    for a,b in itertools.combinations(range(40),2):
        common=len(base_adj[a]&base_adj[b]);assert common==(2 if b in base_adj[a] else 4)
    return R,fib,phase,radj,base_adj,zero,twelve,diffhist

def gf2_basis(rows,n=40):
    B={}
    for x in rows:
        y=x
        while y:
            k=y.bit_length()-1
            if k in B:y^=B[k]
            else:B[k]=y;break
    return [B[k] for k in sorted(B,reverse=True)]
def code_and_d4(R,fib,radj,base_adj):
    rows=[sum(1<<j for j in base_adj[i]) for i in range(40)]
    bs=gf2_basis(rows);assert len(bs)==16
    words=[];enum=Counter()
    for m in range(1<<16):
        x=0
        for i,b in enumerate(bs):
            if (m>>i)&1:x^=b
        enum[x.bit_count()]+=1
        if x.bit_count()==8:words.append(x)
    expected={0:1,8:45,12:1120,16:15570,20:32064,24:15570,28:1120,32:45,40:1};assert dict(enum)==expected
    lifted={str(6*w):a for w,a in sorted(enum.items())}
    halves=set();supports=[]
    for x in words:
        S=[i for i in range(40) if (x>>i)&1];supports.append(frozenset(S))
        H=[tuple(c) for c in itertools.combinations(S,4) if all(v not in base_adj[u] for u,v in itertools.combinations(c,2))]
        assert len(H)==2 and set(H[0])|set(H[1])==set(S);halves.update(H)
    assert len(halves)==90
    cqs=set()
    for a,b,c in itertools.combinations(range(40),3):
        if b in base_adj[a] or c in base_adj[a] or c in base_adj[b]:continue
        C=tuple(sorted(base_adj[a]&base_adj[b]&base_adj[c]))
        if len(C)==4:cqs.add(C)
    assert len(cqs)==90 and halves==cqs
    pairset=set()
    for Q in cqs:
        C=set(range(40))
        for v in Q:C &= base_adj[v]
        Rq=tuple(sorted(C));assert Rq in cqs and len(Rq)==4 and Rq!=Q
        pairset.add(tuple(sorted((Q,Rq))))
    assert len(pairset)==45
    pair_support={frozenset(set(a)|set(b)) for a,b in pairset};assert pair_support==set(supports)
    def rref(rows):
        A=[[Fraction(x) for x in row] for row in rows];m=len(A);n=8;r=0;piv=[]
        for c in range(n):
            k=next((i for i in range(r,m) if A[i][c]),None)
            if k is None:continue
            A[r],A[k]=A[k],A[r];z=A[r][c];A[r]=[x/z for x in A[r]]
            for i in range(m):
                if i!=r and A[i][c]:
                    z=A[i][c];A[i]=[A[i][j]-z*A[r][j] for j in range(n)]
            piv.append(c);r+=1
            if r==m:break
        return A[:r],piv
    for Q in sorted(cqs):
        ids=[u for f in Q for u in fib[f]];assert len(ids)==24
        rr,piv=rref([R[i] for i in ids]);assert len(piv)==4
        S=set(ids);assert all(len(radj[u]&S)==8 for u in ids)
        free=[c for c in range(8) if c not in piv];null=[]
        for f in free:
            v=[Fraction(0) for _ in range(8)];v[f]=1
            for ri,pcol in enumerate(piv):v[pcol]=-rr[ri][f]
            null.append(v)
        closure=[]
        for i,x in enumerate(R):
            if all(sum(Fraction(x[j])*v[j] for j in range(8))==0 for v in null):closure.append(i)
        assert set(closure)==S
    for A,B in pairset:
        ia=[u for f in A for u in fib[f]];ib=[u for f in B for u in fib[f]]
        assert all(dot(R[u],R[v])==0 for u in ia for v in ib)
    supp=list(sorted(pair_support,key=lambda x:tuple(sorted(x))));qline=[]
    ALL=(1<<40)-1;masks=[sum(1<<v for v in S) for S in supp]
    for ids in itertools.combinations(range(45),5):
        u=0;ok=True
        for i in ids:
            if u&masks[i]:ok=False;break
            u|=masks[i]
        if ok and u==ALL:qline.append(ids)
    assert len(qline)==27
    inc=Counter(i for L in qline for i in L);assert set(inc.values())=={3}
    return {
      'base_code':'[40,16,8]_2 (Pass85 prior art replayed)',
      'base_weight_enumerator':{str(k):v for k,v in sorted(enum.items())},
      'e8_fiber_constant_code':'[240,16,48]_2',
      'e8_weight_enumerator':lifted,
      'minimum_words':45,
      'minimum_support_induced_graph':'K4,4 for every weight-8 word',
      'd4_halves':90,'center_quads':90,'d4_equals_center_quads_objectwise':True,
      'd4_root_subsystem_certificate':'all 90 halves contain exactly the 24 E8 roots in a rank-4 span; each root has +1-degree 8',
      'orthogonal_d4_pairs':45,'minimum_support_equals_center_quad_pair_union_objectwise':True,
      'gq42_partition_lines':27,'d4pair_fivepacks_partition_240_e8_roots':True,'each_d4pair_on_partition_lines':3,
    }

def holonomy(fib,phase,radj,twelve):
    phi={}
    for a,b in twelve:
        D={(phase[b][v]-phase[a][u])%6 for u in fib[a] for v in fib[b] if v in radj[u]}
        s=next(x for x in D if (x+1)%6 in D);p=(2*s+1)%12
        phi[(a,b)]=p;phi[(b,a)]=(-p)%12
    H=Counter();tri=0
    for a,b,c in itertools.combinations(range(40),3):
        if (a,b) in phi and (b,c) in phi and (c,a) in phi:
            H[(phi[(a,b)]+phi[(b,c)]+phi[(c,a)])%12]+=1;tri+=1
    assert tri==3240 and H==Counter({1:1440,11:1440,3:180,9:180})
    return {'complement_triangles':tri,'z12_holonomy_histogram':{str(k):v for k,v in sorted(H.items())},
            'gauge_law':'fiber origin shifts change phi_xy by 2(a_y-a_x); cycle sums are invariant mod 12',
            'scope':'exact finite phase cocycle; no physical gauge-field claim'}

def symmetry_diamond():
    return {
      'common_envelope':'D12=<r,s | r^6=s^2=1, srs=r^-1>',
      'internal_cycle':'C6=<r>',
      'central_kernel':'<r^3>=C2',
      'external_controller_quotient':'D12/<r^3> = S3',
      'controller_exact_sequence':'1 -> C3 -> S3 -> C2 -> 1 with inversion action',
      'q9_hexad_note':'the q9 witness stabilizer C2 is a reflection subgroup, not the central C2',
      'boundary':'group-theoretic common envelope; not an objectwise identification of q9 witness fibers with E8 root fibers'
    }
def selected_c6_criterion():
    return {
      'conditional_theorem':'If involutions a,f act faithfully on a six-object orbit, |af|=6, and the object stabilizer in <a,f> is a reflection C2, then <a,f>=D12 and af supplies a canonical C6 on the orbit.',
      'lifting_rule':'Any larger abstract outer automorphism lifts through the ambient action only if it preserves the selected C6 (equivalently its complementary matching in the q9 K3,3 realization).',
      'scope':'field-independent group theorem; the q9 realization via Frobenius is special to fields with a nontrivial automorphism and is not asserted for every q.'
    }
def main():
    qb=q9_boundary();R,fib,phase,radj,base_adj,zero,twelve,diffhist=e8_fibers()
    cd=code_and_d4(R,fib,radj,base_adj);hol=holonomy(fib,phase,radj,twelve)
    out={
      'schema':'w33.pass7163_7170.e8_hexagonal_lift.v1','status':'PASS',
      'boundary':'Exact finite statements. Pass85 [40,16,8], Pass1021 E8->40 fibration, and the 90->45->27 center-quad quotient are prior art in this repo. New claims are the objectwise bridges and lift laws proved here. q9 residual 48-clique decision remains open unless a separate solver certificate closes it. No physics claim.',
      'pass_7163_q9_rank_boundary':qb,
      'pass_7164_e8_hexagonal_root_graph_lift':{
        'roots':240,'fibers':40,'fiber_size':6,'internal_graph':'C6 in every fiber','internal_edges_total':240,
        'base_zero_edge_pairs':240,'base_zero_edge_relation':'W33 adjacency SRG(40,12,2,4)',
        'base_nonadjacent_pairs':540,'cross_edges_per_nonadjacent_pair':12,'cross_graph':'C12 for all 540 pairs',
        'root_degree_decomposition':'56 = 2 internal + 27*2 cross','root_edges_total':'240 + 540*12 = 6720',
        'phase_difference_rule':'for every nonadjacent base pair, offsets are exactly {s,s+1} in Z6',
      },
      'pass_7165_e8_fiber_code_and_d4':cd,
      'pass_7166_sixfold_symmetry_diamond':symmetry_diamond(),
      'pass_7167_selected_c6_criterion':selected_c6_criterion(),
      'pass_7168_z12_holonomy':hol,
      'pass_7169_centerquad_d4_dictionary':{
        'dictionary':'90 W33 center-quads = 90 D4 root subsystems inside E8, objectwise under the Pass1021 fibration',
        'pairing':'center-quad involution = orthogonal-complement D4 pairing; 45 pairs are 45 D4+D4 root subsystems',
        'code':'the 45 pair-unions are exactly the 45 weight-8 words/tritangents of C2(W33)'
      },
      'pass_7170_e6_partition_dictionary':{
        'old_quotient':'90 center-quads -> 45 quotient points -> 27 GQ(4,2) lines (repo prior art)',
        'e8_translation':'90 D4 -> 45 orthogonal D4+D4 -> 27 five-packs partitioning all 240 E8 roots',
        'incidence':'each 27-line contains 5 D4+D4 supports; each of the 45 D4+D4 supports lies on 3 lines',
        'boundary':'the 27-line/cubic-surface identification is prior art; the E8 D4 translation is new here.'
      }
    }
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','q9_rank1_alpha':[qb['anchor_cases'][str(r)]['rank1_independence_number_exact'] for r in TYPES], 'e8_fibers':40,'d4':90,'d4pairs':45,'partitions':27,'holonomy':hol['z12_holonomy_histogram']},sort_keys=True))
if __name__=='__main__':main()
