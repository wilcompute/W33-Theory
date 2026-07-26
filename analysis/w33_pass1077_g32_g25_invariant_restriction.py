from __future__ import annotations
import itertools,json,time
from collections import deque,Counter
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass1077_g32_g25_invariant_restriction.json'
P=43;OMEGA=6
DIRS=[(0,0,-1,0),(1,1,1,0),(0,1,0,0),(1,-1,0,-1)]
def mm(A,B,n,p=P):return tuple(sum(A[n*i+k]*B[n*k+j] for k in range(n))%p for i in range(n) for j in range(n))
def ident(n):return tuple(1 if i==j else 0 for i in range(n) for j in range(n))
def reflection(v):
    n=len(v);den=sum(x*x for x in v)%P;c=(OMEGA-1)*pow(den,-1,P)%P
    return tuple(((1 if i==j else 0)+c*v[i]*v[j])%P for i in range(n) for j in range(n))
def group(gens,n):
    I=ident(n);seen={I};q=deque([I])
    while q:
        x=q.popleft()
        for g in gens:
            y=mm(g,x,n)
            if y not in seen:seen.add(y);q.append(y)
    return sorted(seen)
def rank_mod(M,p=P):
    A=np.array(M,dtype=np.int64)%p;r=0
    for c in range(A.shape[1]):
        q=next((i for i in range(r,A.shape[0]) if A[i,c]),None)
        if q is None:continue
        A[[r,q]]=A[[q,r]];A[r]=A[r]*pow(int(A[r,c]),-1,p)%p
        for i in range(A.shape[0]):
            if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
        r+=1
    return r
def solve_mod(A,b,p=P):
    A=np.array(A,dtype=np.int64)%p;b=np.array(b,dtype=np.int64).reshape(-1,1)%p;M=np.concatenate([A,b],axis=1);r=0;piv=[]
    for c in range(A.shape[1]):
        q=next((i for i in range(r,M.shape[0]) if M[i,c]),None)
        if q is None:continue
        M[[r,q]]=M[[q,r]];M[r]=M[r]*pow(int(M[r,c]),-1,p)%p
        for i in range(M.shape[0]):
            if i!=r and M[i,c]:M[i]=(M[i]-M[i,c]*M[r])%p
        piv.append(c);r+=1
    if any(not M[i,:A.shape[1]].any() and M[i,-1] for i in range(r,M.shape[0])):raise ValueError('inconsistent')
    x=np.zeros(A.shape[1],dtype=np.int64)
    for i,c in enumerate(piv):x[c]=M[i,-1]
    return x
def normalize_vec(v,p=P):
    v=tuple(int(x)%p for x in v)
    for x in v:
        if x:return tuple(y*pow(x,-1,p)%p for y in v)
    return v
def powmod_scalar_table(degrees):return {d:np.array([pow(x,d,P) for x in range(P)],dtype=np.int64) for d in degrees}
def candidate_evals(arr,candidates,X,degrees):
    tables=powmod_scalar_table(degrees);out=[]
    for a in candidates:
        rows=np.einsum('i,nij->nj',np.array(a,dtype=np.int64),arr,optimize=True)%P;vals=rows@X.T%P
        counts=np.stack([np.bincount(vals[:,j],minlength=P) for j in range(vals.shape[1])]);out.append({d:(counts@tables[d])%P for d in degrees})
    return out
def choose_independent(evals,degree,span,needed=1):
    out=[];inds=[]
    for i,E in enumerate(evals):
        v=E[degree]
        if not np.any(v):continue
        if rank_mod(np.stack(span+out+[v],axis=1))>len(span)+len(out):out.append(v);inds.append(i)
        if len(out)==needed:break
    return out,inds
def powvec(x,n):
    if n==0:return np.ones_like(x)
    out=np.ones_like(x);base=x.copy();k=n
    while k:
        if k&1:out=out*base%P
        base=base*base%P;k//=2
    return out
def monomials_eval(u,v,w,degree):
    cols=[];labels=[]
    for a in range(degree//6+1):
      for b in range(degree//9+1):
       for c in range(degree//12+1):
        if 6*a+9*b+12*c==degree:cols.append(powvec(u,a)*powvec(v,b)%P*powvec(w,c)%P);labels.append(f'u6^{a}*v9^{b}*w12^{c}')
    return np.stack(cols,axis=1),labels
def inv_matrix(A,n):
    M=np.array(A,dtype=np.int64).reshape(n,n)%P;aug=np.concatenate([M,np.eye(n,dtype=np.int64)],axis=1);r=0
    for c in range(n):
        q=next(i for i in range(r,n) if aug[i,c]);aug[[r,q]]=aug[[q,r]];aug[r]=aug[r]*pow(int(aug[r,c]),-1,P)%P
        for i in range(n):
            if i!=r and aug[i,c]:aug[i]=(aug[i]-aug[i,c]*aug[r])%P
        r+=1
    return tuple(int(x) for x in aug[:,n:].flat)
def projective_orbit(seed,gens,n):
    def norm(v):
        v=tuple(int(x)%P for x in v)
        for x in v:
            if x:return tuple(y*pow(x,-1,P)%P for y in v)
        raise ValueError
    invT=[np.array(inv_matrix(g,n),dtype=np.int64).reshape(n,n).T%P for g in gens];s=norm(seed);seen={s};q=deque([s])
    while q:
        v=q.popleft();vv=np.array(v,dtype=np.int64)
        for T in invT:
            w=norm(T@vv%P)
            if w not in seen:seen.add(w);q.append(w)
    return sorted(seen)
def main():
    started=time.time();R4=[reflection(v) for v in DIRS];R3=[tuple(R4[k][4*i+j] for i in range(3) for j in range(3)) for k in range(3)];G25=group(R3,3);G32=group(R4,4);assert len(G25)==648 and len(G32)==155520
    A25=np.array(G25,dtype=np.int16).reshape(-1,3,3);A32=np.array(G32,dtype=np.int16).reshape(-1,4,4);rng=np.random.default_rng(1077)
    X3=rng.integers(0,P,size=(36,3),dtype=np.int64);X3[:8]=np.array([[1,0,0],[0,1,0],[0,0,1],[1,1,0],[1,0,1],[0,1,1],[1,1,1],[2,3,5]]);X4=np.c_[X3,np.zeros(36,dtype=np.int64)]
    cand3=[(1,0,0),(0,1,0),(0,0,1),(1,1,0),(1,0,1),(0,1,1),(1,1,1),(1,2,3),(2,3,5),(1,4,7)]
    cand4=[(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,1,0,0),(1,0,1,0),(1,0,0,1),(0,1,1,0),(0,1,0,1),(0,0,1,1),(1,1,1,0),(1,1,0,1),(1,0,1,1),(0,1,1,1),(1,1,1,1),(1,2,3,4)]
    E25=candidate_evals(A25,cand3,X3,[6,9,12]);u6,ui=choose_independent(E25,6,[],1);v9,vi=choose_independent(E25,9,[],1);u6=u6[0];v9=v9[0];w12,wi=choose_independent(E25,12,[powvec(u6,2)],1);w12=w12[0]
    dims25={};bases25={}
    for d in [12,18,24,30]:M,labs=monomials_eval(u6,v9,w12,d);dims25[str(d)]=rank_mod(M);bases25[d]=(M,labs)
    assert dims25=={'12':2,'18':3,'24':4,'30':5}
    E32=candidate_evals(A32,cand4,X4,[12,18,24,30]);F12,i12=choose_independent(E32,12,[],1);F12=F12[0];F18,i18=choose_independent(E32,18,[],1);F18=F18[0];F24,i24=choose_independent(E32,24,[powvec(F12,2)],1);F24=F24[0];F30,i30=choose_independent(E32,30,[F12*F18%P],1);F30=F30[0]
    restricted={'F12':F12,'F18':F18,'F24':F24,'F30':F30};degrees={'F12':12,'F18':18,'F24':24,'F30':30};idxs={'F12':i12[0],'F18':i18[0],'F24':i24[0],'F30':i30[0]};formulas={}
    for name,vec in restricted.items():M,labs=bases25[degrees[name]];coef=solve_mod(M,vec);assert np.all(M@coef%P==vec);formulas[name]={'degree':degrees[name],'basis':labs,'coefficients_mod43':[int(x) for x in coef]}
    Y3=rng.integers(0,P,size=(16,3),dtype=np.int64);Y4=np.c_[Y3,np.zeros(16,dtype=np.int64)];EY25=candidate_evals(A25,cand3,Y3,[6,9,12]);Yu=EY25[ui[0]][6];Yv=EY25[vi[0]][9];Yw=EY25[wi[0]][12];EY32=candidate_evals(A32,cand4,Y4,[12,18,24,30]);validation={}
    for name in restricted:M,_=monomials_eval(Yu,Yv,Yw,degrees[name]);validation[name]=bool(np.array_equal(M@np.array(formulas[name]['coefficients_mod43'])%P,EY32[idxs[name]][degrees[name]]))
    H25=projective_orbit(DIRS[0][:3],R3,3);H32=projective_orbit(DIRS[0],R4,4);restricted_h=[];zero=0
    for h in H32:
        r=normalize_vec(h[:3]);zero+=not any(r)
        if any(r):restricted_h.append(r)
    mult=Counter(restricted_h);h25set=set(H25);in_parabolic=sum(m for h,m in mult.items() if h in h25set);outside=sum(m for h,m in mult.items() if h not in h25set)
    checks={'orders_648_and_155520':len(G25)==648 and len(G32)==155520,'g25_invariant_dimensions_2_3_4_5':dims25=={'12':2,'18':3,'24':4,'30':5},'all_four_restrictions_fit_G25_monomial_bases':all(validation.values()),'degree9_generator_never_occurs_oddly':all(all(int(lbl.split('v9^')[1].split('*')[0])%2==0 for lbl,c in zip(formulas[n]['basis'],formulas[n]['coefficients_mod43']) if c) for n in formulas),'g25_has_12_reflecting_hyperplanes':len(H25)==12,'g32_has_40_reflecting_hyperplanes':len(H32)==40,'slice_is_itself_one_G32_reflecting_hyperplane':zero==1,'all_g25_hyperplanes_occur_in_restriction':h25set.issubset(set(mult))};checks={k:bool(v) for k,v in checks.items()};assert all(checks.values()),checks
    out={'schema':'w33.pass1077.g32_g25.invariant_restriction.v1','status':'PASS','headline':'The parabolic slice x4=0 was computed over the good prime 43. Exact Reynolds-orbit invariants for G32 restrict into the G25 invariant ring, but only through the subring even in the degree-9 generator.','field_certificate':{'prime':43,'omega_residue':6,'G25_order':648,'G32_order':155520},'G25_generators':{'degrees':[6,9,12],'names':['u6','v9','w12']},'G25_evaluation_dimensions':dims25,'G32_basic_restrictions_mod43':formulas,'validation_on_independent_points':validation,'structural_decision':{'restriction_surjective':False,'reason':'The degree-9 generator v9 occurs only through v9^2.','image_subring':'contained in F43[u6,w12,v9^2]'},'reflection_arrangement_restriction':{'G25_hyperplanes':len(H25),'G32_hyperplanes':len(H32),'slice_hyperplane_factor_count':zero,'distinct_restricted_hyperplanes':len(mult),'multiplicity_profile':dict(sorted(Counter(mult.values()).items())),'total_factors_on_G25_hyperplanes':in_parabolic,'total_extra_restricted_factors':outside,'factor_multiplicities_after_dividing_slice_factor':{'/'.join(map(str,h)):m for h,m in sorted(mult.items())},'transverse_discriminant_reading':'After dividing the slice factor, the remaining 39 hyperplanes restrict as the 12 G25 hyperplanes once plus 9 additional hyperplanes with multiplicity three.'},'check_count':len(checks),'checks':checks,'scope':'Exact finite-field invariant and reflection-arrangement computation at a good prime; no characteristic-zero canonical normalization is claimed.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','formulas':formulas,'seconds':round(time.time()-started,3)},indent=2))
if __name__=='__main__':main()
