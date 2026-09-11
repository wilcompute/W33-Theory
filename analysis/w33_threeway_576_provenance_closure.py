#!/usr/bin/env python3
from __future__ import annotations
import itertools, json, math, hashlib, time
from pathlib import Path
from collections import Counter, defaultdict, deque

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_threeway_576_provenance_closure.json'


def compose(p,q): return tuple(p[q[i]] for i in range(len(q)))
def pinv(p):
    out=[0]*len(p)
    for i,j in enumerate(p): out[j]=i
    return tuple(out)
def porder(p):
    seen=set(); z=1
    for i in range(len(p)):
        if i in seen: continue
        j=i; n=0
        while j not in seen:
            seen.add(j); n+=1; j=p[j]
        z=math.lcm(z,n)
    return z
def generated_group(gens,n):
    e=tuple(range(n)); pool=list(gens)+[pinv(g) for g in gens]
    G={e}; q=deque([e])
    while q:
        x=q.popleft()
        for g in pool:
            y=compose(g,x)
            if y not in G: G.add(y); q.append(y)
    return G
def center(G):
    L=list(G)
    return [g for g in L if all(compose(g,h)==compose(h,g) for h in L)]
def derived_subgroup(G,n):
    L=list(G); inv={g:pinv(g) for g in L}; comms=set()
    for g in L:
        gi=inv[g]
        for h in L:
            comms.add(compose(compose(compose(gi,inv[h]),g),h))
    return generated_group(comms,n)
def sha(obj): return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(',',':')).encode()).hexdigest()

# W(3,3) / PSp(4,3) minimum-vector stabilizer, reconstructed directly.
def norm3(v):
    i=next(k for k,x in enumerate(v) if x%3); s=pow(v[i]%3,-1,3)
    return tuple((s*x)%3 for x in v)
def sp3(u,v): return (u[0]*v[1]-u[1]*v[0]+u[2]*v[3]-u[3]*v[2])%3

def psp_minimum_stabilizer():
    pts=sorted({norm3(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    idx={v:i for i,v in enumerate(pts)}
    lines=set()
    for a,b in itertools.combinations(range(40),2):
        if sp3(pts[a],pts[b]): continue
        S=set()
        for s,t in itertools.product(range(3),repeat=2):
            if s==t==0: continue
            S.add(idx[norm3(tuple((s*pts[a][k]+t*pts[b][k])%3 for k in range(4)))])
        if len(S)==4: lines.add(tuple(sorted(S)))
    lines=sorted(lines); assert len(lines)==40
    N=[[0]*40 for _ in range(40)]
    for l,L in enumerate(lines):
        for p in L:N[l][p]=1
    cols=[tuple(N[l][p] for l in range(40)) for p in range(40)]
    d=defaultdict(list)
    for S in itertools.combinations(range(40),4):
        sig=tuple(sum(cols[p][l] for p in S) for l in range(40)); d[sig].append(S)
    pairs=sorted(tuple(sorted((tuple(v[0]),tuple(v[1])))) for v in d.values() if len(v)==2)
    assert len(pairs)==45 and all(not(set(a)&set(b)) for a,b in pairs)
    gens=[]
    for v in pts:
        for a in (1,2):
            perm=[]
            for x in pts:
                c=a*sp3(x,v)%3
                y=norm3(tuple((x[k]+c*v[k])%3 for k in range(4)))
                perm.append(idx[y])
            gens.append(tuple(perm))
    e=tuple(range(40)); G={e}; q=deque([e])
    while q:
        x=q.popleft()
        for g in gens:
            y=compose(g,x)
            if y not in G:G.add(y);q.append(y)
    assert len(G)==25920
    target=pairs[0]
    def aset(p,S): return tuple(sorted(p[i] for i in S))
    def apair(p,z): return tuple(sorted((aset(p,z[0]),aset(p,z[1]))))
    H={p for p in G if apair(p,target)==target}; assert len(H)==576
    return H

# W(F4) on its 48 doubled roots, with long/short reflection characters.
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def reflect(v,r):
    num=2*dot(v,r); den=dot(r,r)
    out=[]
    for i in range(4):
        n=v[i]*den-num*r[i]; assert n%den==0; out.append(n//den)
    return tuple(out)

def wf4_and_kernels():
    roots=[]
    for i in range(4):
        for s in (-1,1):
            v=[0]*4; v[i]=2*s; roots.append(tuple(v))
    roots.extend(itertools.product((-1,1),repeat=4))
    for i in range(4):
        for j in range(i+1,4):
            for a in (-1,1):
                for b in (-1,1):
                    v=[0]*4; v[i]=2*a; v[j]=2*b; roots.append(tuple(v))
    roots=sorted(set(roots)); assert len(roots)==48; ri={v:i for i,v in enumerate(roots)}
    simple=((0,2,-2,0),(0,0,2,-2),(0,0,0,2),(1,-1,-1,-1))
    gens=[tuple(ri[reflect(v,r)] for v in roots) for r in simple]
    glabel=((1,0),(1,0),(0,1),(0,1))
    e=tuple(range(48)); labels={e:(0,0)}; q=deque([e])
    while q:
        x=q.popleft(); lx=labels[x]
        for g,lg in zip(gens,glabel):
            y=compose(g,x); ly=(lx[0]^lg[0],lx[1]^lg[1])
            if y not in labels: labels[y]=ly; q.append(y)
            else: assert labels[y]==ly
    assert len(labels)==1152
    long={g for g,a in labels.items() if a[0]==0}
    short={g for g,a in labels.items() if a[1]==0}
    rot={g for g,a in labels.items() if (a[0]^a[1])==0}
    auto={e:e}; q=deque([e]); rev=list(reversed(gens))
    while q:
        x=q.popleft(); y=auto[x]
        for g,h in zip(gens,rev):
            nx=compose(g,x); ny=compose(h,y)
            if nx not in auto: auto[nx]=ny; q.append(nx)
            else: assert auto[nx]==ny
    assert len(auto)==1152 and {auto[g] for g in long}==short
    return set(labels),long,short,rot,auto

# Characteristic E=G'' coordinate model and quotient action.
def quotient_E_coords(E,n):
    E=set(E); Z=center(E); assert len(Z)==2; e=tuple(range(n)); z=next(x for x in Z if x!=e)
    cosets=[]; ci={}
    for x in sorted(E):
        if x in ci: continue
        C=tuple(sorted((x,compose(z,x))))
        k=len(cosets); cosets.append(C)
        for y in C: ci[y]=k
    reps=[C[0] for C in cosets]; idc=ci[e]
    add=[[ci[compose(a,b)] for b in reps] for a in reps]
    coord={idc:0}; basis=[]
    for c in range(16):
        if c in coord: continue
        bit=1<<len(basis); old=list(coord.items())
        for d,v in old: coord[add[d][c]]=v|bit
        basis.append(c)
        if len(coord)==16:break
    assert len(coord)==16 and len(basis)==4
    invcoord={v:c for c,v in coord.items()}
    qform={coord[c]:(0 if compose(r,r)==e else 1) for c,r in enumerate(reps)}
    return {'z':z,'cosets':cosets,'ci':ci,'reps':reps,'coord':coord,'invcoord':invcoord,'basis':basis,'q':qform}
def action_mats(G,Edata):
    mats={}
    breps=[Edata['reps'][c] for c in Edata['basis']]
    for g in G:
        gi=pinv(g); cols=[]
        for r in breps:
            y=compose(compose(g,r),gi); cols.append(Edata['coord'][Edata['ci'][y]])
        mats[g]=tuple(cols)
    return mats

def rank4(cols):
    piv={}
    for x in cols:
        y=x
        while y:
            p=y.bit_length()-1
            if p in piv:y^=piv[p]
            else:piv[p]=y;break
    return len(piv)
def mapply(A,x):
    y=0
    for i,e in enumerate((1,2,4,8)):
        if x&e:y^=A[i]
    return y
def mcomp(A,B): return tuple(mapply(A,b) for b in B)
def minv(A): return tuple(next(x for x in range(16) if mapply(A,x)==e) for e in (1,2,4,8))
def morder(A):
    I=(1,2,4,8); x=I
    for n in range(1,20):
        x=mcomp(A,x)
        if x==I:return n
    raise AssertionError
def gen_mats(gens):
    I=(1,2,4,8); pool=list(gens)+[minv(g) for g in gens]; G={I}; q=deque([I])
    while q:
        x=q.popleft()
        for g in pool:
            y=mcomp(g,x)
            if y not in G:G.add(y);q.append(y)
    return G

def find_GL4_conjugator(AH,AK,qH,qK):
    for P in itertools.permutations(range(1,16),4):
        if rank4(P)!=4: continue
        Pi=minv(P)
        if {mcomp(mcomp(P,A),Pi) for A in AH}!=AK: continue
        if all(qK[mapply(P,x)]==qH[x] for x in range(16)): return P
    raise AssertionError('no conjugator')

def normal_form(Edata,E,n):
    e=tuple(range(n)); z=Edata['z']; B=[Edata['reps'][c] for c in Edata['basis']]
    prod={}
    for v in range(16):
        x=e
        for i in range(4):
            if v&(1<<i): x=compose(x,B[i])
        prod[v]=x
    nf={}
    for v,x in prod.items(): nf[x]=(0,v); nf[compose(z,x)]=(1,v)
    assert set(nf)==set(E)
    return B,nf

def find_complement_generators(G,action,E,n):
    Aset=set(action.values())
    o2=[A for A in Aset if morder(A)==2]; o3=[A for A in Aset if morder(A)==3]
    rel=None
    for s in o2:
        for a in o3:
            if mcomp(mcomp(s,a),s)!=minv(a): continue
            if len(gen_mats((s,a)))!=6: continue
            for b in o3:
                if b in gen_mats((s,a)): continue
                if mcomp(b,s)==mcomp(s,b) and mcomp(b,a)==mcomp(a,b) and len(gen_mats((s,a,b)))==18:
                    rel=(s,a,b);break
            if rel:break
        if rel:break
    assert rel
    sM,aM,bM=rel
    choices=[]
    for M,o in ((sM,2),(aM,3),(bM,3)):
        choices.append([g for g,A in action.items() if A==M and porder(g)==o])
    for s in choices[0]:
        for a in choices[1]:
            if compose(compose(s,a),s)!=pinv(a):continue
            if len(generated_group((s,a),n))!=6:continue
            for b in choices[2]:
                if compose(b,s)!=compose(s,b) or compose(b,a)!=compose(a,b):continue
                C=generated_group((s,a,b),n)
                if len(C)==18 and len(C&set(E))==1:return rel,(s,a,b),C
    raise AssertionError('no complement')

def main():
    t=time.time()
    H=psp_minimum_stabilizer(); WF,Klong,Kshort,Krot,outer=wf4_and_kernels()
    assert Counter(porder(g) for g in H)==Counter({1:1,2:43,3:80,4:84,6:272,12:96})
    h1=derived_subgroup(H,40); h2=derived_subgroup(h1,40)
    k1=derived_subgroup(Klong,48); k2=derived_subgroup(k1,48)
    assert len(h1)==len(k1)==96 and len(h2)==len(k2)==32
    assert Counter(porder(g) for g in h2)==Counter({1:1,2:19,4:12})==Counter(porder(g) for g in k2)
    EH=quotient_E_coords(h2,40); EK=quotient_E_coords(k2,48)
    AH=action_mats(H,EH); AK=action_mats(Klong,EK)
    assert len(set(AH.values()))==len(set(AK.values()))==18
    P=find_GL4_conjugator(set(AH.values()),set(AK.values()),EH['q'],EK['q'])

    relH,hgens,HC=find_complement_generators(H,AH,h2,40)
    Pi=minv(P); targetM=tuple(mcomp(mcomp(P,A),Pi) for A in relH)
    kgopts=[]
    for M,o in zip(targetM,(2,3,3)):
        kgopts.append([g for g,A in AK.items() if A==M and porder(g)==o])
    _,Hnf=normal_form(EH,h2,40); _,_=normal_form(EK,k2,48)
    target_cosets=[EK['invcoord'][mapply(P,1<<i)] for i in range(4)]
    zK=EK['z']; eK=tuple(range(48)); eH=tuple(range(40))
    phiE=None
    for toggles in itertools.product((0,1),repeat=4):
        tb=[]
        for i,c in enumerate(target_cosets):
            base=EK['cosets'][c][0]; tb.append(compose(zK,base) if toggles[i] else base)
        tprod={}
        for v in range(16):
            x=eK
            for i in range(4):
                if v&(1<<i):x=compose(x,tb[i])
            tprod[v]=x
        phi={}
        for h,(eps,v) in Hnf.items(): phi[h]=compose(zK,tprod[v]) if eps else tprod[v]
        if len(set(phi.values()))<32:continue
        if all(phi[compose(a,b)]==compose(phi[a],phi[b]) for a in h2 for b in h2):
            phiE=phi;break
    assert phiE is not None

    def conj(g,e): return compose(compose(g,e),pinv(g))
    kchoices=[]
    for hg,opts in zip(hgens,kgopts):
        good=[kg for kg in opts if all(phiE[conj(hg,e)]==conj(kg,phiE[e]) for e in h2)]
        assert good;kchoices.append(good)
    kgens=None
    for s in kchoices[0]:
        for a in kchoices[1]:
            if compose(compose(s,a),s)!=pinv(a):continue
            for b in kchoices[2]:
                if compose(b,s)!=compose(s,b) or compose(b,a)!=compose(a,b):continue
                C=generated_group((s,a,b),48)
                if len(C)==18 and len(C&k2)==1:kgens=(s,a,b);break
            if kgens:break
        if kgens:break
    assert kgens

    cmap={eH:eK}; q=deque([eH]); gpairs=[]
    for a,b in zip(hgens,kgens):gpairs.extend(((a,b),(pinv(a),pinv(b))))
    while q:
        h=q.popleft(); k=cmap[h]
        for a,b in gpairs:
            nh=compose(a,h); nk=compose(b,k)
            if nh not in cmap:cmap[nh]=nk;q.append(nh)
            else:assert cmap[nh]==nk
    assert len(cmap)==18
    decomp={}
    for e in h2:
        for c in HC:
            x=compose(e,c); assert x not in decomp; decomp[x]=(e,c)
    assert set(decomp)==H
    phi={h:compose(phiE[e],cmap[c]) for h,(e,c) in decomp.items()}
    assert len(set(phi.values()))==576 and set(phi.values())==Klong
    assert all(phi[compose(a,b)]==compose(phi[a],phi[b]) for a in H for b in H)

    hist=lambda G:dict(sorted(Counter(porder(g) for g in G).items()))
    result={
      'schema':'w33.20260910.threeway-576-provenance-closure.v1','status':'PASS',
      'psp_minimum':{'order':len(H),'center':len(center(H)),'derived_chain':[len(H),len(h1),len(h2)],'orders':hist(H)},
      'wf4':{'order':len(WF),'index2_kernels':{
          'long_root_parity':{'order':len(Klong),'orders':hist(Klong)},
          'short_root_parity':{'order':len(Kshort),'orders':hist(Kshort)},
          'total_reflection_parity_rotations':{'order':len(Krot),'orders':hist(Krot)}},
          'diagram_reversal_maps_long_to_short':True},
      'explicit_isomorphism':{
          'target':'PSp(4,3) minimum-vector stabilizer -> W(F4) long-root-parity kernel',
          'characteristic_kernel':'second derived subgroup 2_+^{1+4} of order 32',
          'quotient_action_order':18,
          'GL4_conjugator_columns':list(P),
          'extraspecial_map_sha256':sha(sorted((str(k),str(v)) for k,v in phiE.items())),
          'full_map_sha256':sha(sorted((str(k),str(v)) for k,v in phi.items())),
          'full_576_squared_homomorphism_check':True,
          'bijection':True},
      'correction':'The W33 576 group is NOT the total-reflection-parity/rotation subgroup of W(F4): that third kernel has 144 elements of order 8 and derived order 288. It is one of the two root-length-parity kernels, which are exchanged by F4 Coxeter-diagram reversal.',
      'provenance_bridge':'Together with the existing q=5 Hoffman theorem H ~= W(D4):C3 < W(F4), this closes the abstract provenance bridge from the PSp(4,3) minimum-vector stabilizer to the same F4 root-parity subgroup class.',
      'elapsed_seconds':round(time.time()-t,3)}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({'status':result['status'],'order':result['psp_minimum']['order'],'GL4':result['explicit_isomorphism']['GL4_conjugator_columns'],'elapsed_seconds':result['elapsed_seconds']},sort_keys=True))
    return result
if __name__=='__main__': main()
