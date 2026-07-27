from __future__ import annotations
import json,math,time
from collections import deque
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass1093_dual_hesse_firewall_fiber_equivalence.json'
P=43;W=6;F=3
DIRS=[(0,0,-1),(1,1,1),(0,1,0)]

def mm(A,B,n=3,p=P):return tuple(sum(A[n*i+k]*B[n*k+j] for k in range(n))%p for i in range(n) for j in range(n))
def ident(n=3):return tuple(1 if i==j else 0 for i in range(n) for j in range(n))
def refl(v):
    den=sum(x*x for x in v)%P;c=(W-1)*pow(den,-1,P)%P
    return tuple(((1 if i==j else 0)+c*v[i]*v[j])%P for i in range(3) for j in range(3))
def inv(A,n=3):
    M=np.array(A,dtype=np.int64).reshape(n,n)%P;aug=np.concatenate([M,np.eye(n,dtype=np.int64)],axis=1);r=0
    for c in range(n):
        q=next(i for i in range(r,n) if aug[i,c]);aug[[r,q]]=aug[[q,r]];aug[r]=aug[r]*pow(int(aug[r,c]),-1,P)%P
        for i in range(n):
            if i!=r and aug[i,c]:aug[i]=(aug[i]-aug[i,c]*aug[r])%P
        r+=1
    return tuple(int(x) for x in aug[:,n:].flat)
def group(gens):
    I=ident();seen={I};q=deque([I])
    while q:
        x=q.popleft()
        for g in gens:
            y=mm(g,x)
            if y not in seen:seen.add(y);q.append(y)
    return sorted(seen)
def norm(v):
    v=tuple(int(x)%P for x in v)
    for x in v:
        if x:return tuple(y*pow(x,-1,P)%P for y in v)
    raise ValueError
def covact(h,A):
    Ai=np.array(inv(A),dtype=np.int64).reshape(3,3)
    return norm(np.array(h,dtype=np.int64)@Ai%P)
def compose(a,b):return tuple(a[b[i]] for i in range(len(a)))
def inverse(p):
    q=[0]*len(p)
    for i,j in enumerate(p):q[j]=i
    return tuple(q)
def enum_perm(gens):
    I=tuple(range(len(gens[0])));seen={I};q=deque([I])
    while q:
        x=q.popleft()
        for g in gens:
            y=compose(g,x)
            if y not in seen:seen.add(y);q.append(y)
    return sorted(seen)
def order(p):
    seen=[0]*len(p);o=1
    for i in range(len(p)):
        if not seen[i]:
            j=i;l=0
            while not seen[j]:seen[j]=1;j=p[j];l+=1
            o=math.lcm(o,l)
    return o
def classes(G,gens):
    idx={g:i for i,g in enumerate(G)};trs=[]
    for g in gens:
        gi=inverse(g);trs.append([idx[compose(gi,compose(x,g))] for x in G])
    unseen=set(range(len(G)));out=[]
    while unseen:
        s=min(unseen);unseen.remove(s);q=deque([s]);orb=[]
        while q:
            x=q.popleft();orb.append(x)
            for tr in trs:
                y=tr[x]
                if y in unseen:unseen.remove(y);q.append(y)
        out.append(orb)
    return out

def ppower(p,n):
    r=tuple(range(len(p)))
    for _ in range(n):r=compose(p,r)
    return r

def add3(a,b):return ((a[0]+b[0])%3,(a[1]+b[1])%3)
def sub3(a,b):return ((a[0]-b[0])%3,(a[1]-b[1])%3)
def det3(M):return (M[0][0]*M[1][1]-M[0][1]*M[1][0])%3

def main():
    started=time.time();roots=[1,W,W*W%P]
    extra=sorted({norm(tuple(1 if k==i else ((-z)%P if k==j else 0) for k in range(3))) for i in range(3) for j in range(i+1,3) for z in roots})
    assert len(extra)==9
    mats=group([refl(v) for v in DIRS]);assert len(mats)==648
    eidx={h:i for i,h in enumerate(extra)}
    genperms=[tuple(eidx[covact(h,refl(v))] for h in extra) for v in DIRS]
    H=enum_perm(genperms);assert len(H)==216
    cls=classes(H,genperms)
    trans_class=next(c for c in cls if len(c)==8 and order(H[c[0]])==3 and sum(i==x for i,x in enumerate(H[c[0]]))==0)
    N=[tuple(range(9))]+[H[i] for i in trans_class];Nset=set(N)
    assert len(Nset)==9 and all(compose(a,b) in Nset for a in N for b in N) and all(compose(a,b)==compose(b,a) for a in N for b in N)
    assert all(len({n[x] for n in N})==9 for x in range(9))
    nonid=sorted(trans_class,key=lambda i:H[i]);t1=H[nonid[0]];cyc1={ppower(t1,a) for a in range(3)};t2=next(H[i] for i in nonid if H[i] not in cyc1)
    base=0;point_to_coord={};coord_to_point={}
    for a in range(3):
        for b in range(3):
            p=compose(ppower(t1,a),ppower(t2,b))[base];point_to_coord[p]=(a,b);coord_to_point[(a,b)]=p
    assert len(point_to_coord)==9
    affine=[];linear_parts=set();translations=set()
    for g in H:
        b=point_to_coord[g[coord_to_point[(0,0)]]]
        y1=sub3(point_to_coord[g[coord_to_point[(1,0)]]],b);y2=sub3(point_to_coord[g[coord_to_point[(0,1)]]],b)
        A=((y1[0],y2[0]),(y1[1],y2[1]));assert det3(A)==1
        for u,p in coord_to_point.items():
            z=((A[0][0]*u[0]+A[0][1]*u[1]+b[0])%3,(A[1][0]*u[0]+A[1][1]*u[1]+b[1])%3)
            assert g[p]==coord_to_point[z]
        affine.append({'A':[list(A[0]),list(A[1])],'b':list(b)});linear_parts.add(A);translations.add(b)
    mapping=[]
    for i,h in enumerate(extra):
        eq=[int(x) for x in h]
        mapping.append({'extra_hyperplane_normal_mod43':eq,'firewall_fiber_u':list(point_to_coord[i]),'fiber_vertices':[{'u':list(point_to_coord[i]),'z':z} for z in range(3)]})
    checks={'extra_hyperplanes9':len(extra)==9,'G25_order648':len(mats)==648,'projective_Hessian_order216':len(H)==216,'unique_translation_class_size8':sum(1 for c in cls if len(c)==8 and order(H[c[0]])==3 and sum(i==x for i,x in enumerate(H[c[0]]))==0)==1,'translation_group_C3xC3_order9':len(Nset)==9,'translation_group_abelian':all(compose(a,b)==compose(b,a) for a in N for b in N),'translation_group_regular':all(len({n[x] for n in N})==9 for x in range(9)),'explicit_bijection_to_F3_squared':len(point_to_coord)==9,'all_actions_are_affine':len(affine)==216,'linear_image_is_SL2_3_order24':len(linear_parts)==24 and all(det3(A)==1 for A in linear_parts),'translation_vectors_all9':len(translations)==9,'fiber_expansion_is_9_times3':sum(len(x['fiber_vertices']) for x in mapping)==27}
    assert all(checks.values()),checks
    out={'schema':'w33.pass1093.dual_hesse.firewall_fiber_equivalence.v1','status':'PASS','headline':'The nine dual-Hesse hyperplanes and the nine E6/Heisenberg firewall fibers are the same Hessian 9-point G-set. The unique fixed-point-free conjugacy class of size 8, together with the identity, is a regular normal C3 x C3 translation subgroup; choosing two generators gives an explicit affine coordinate bijection to u in F3^2. The projective G25 action becomes exactly ASL(2,3)=3^2:SL(2,3) of order 216.','group_reading':{'projective_group':'ASL(2,3) = 3^2:SL(2,3), Hessian group','order':216,'translation_subgroup':'C3 x C3','translation_order':9,'linear_quotient':'SL(2,3)','linear_order':24},'explicit_equivariant_mapping':mapping,'generator_affine_actions':affine[:3],'fiber_definition':'For each u in F3^2, the repository firewall fiber is {(u,z): z in F3}; the nine hyperplanes map equivariantly to the nine u values.','check_count':len(checks),'checks':checks,'seconds':time.time()-started,'scope':'Exact projective G25 action reduced modulo 43 and exact affine action over F3. The affine coordinate choice is unique only up to ASL(2,3), as expected.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','checks':len(checks),'mapping':mapping,'seconds':round(time.time()-started,3)},indent=2))
if __name__=='__main__':main()
