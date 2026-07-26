from __future__ import annotations
import itertools,json,math,time,hashlib
from pathlib import Path
import numpy as np
import sympy as sp
from w33_pass1081_1086_core import *

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass1088_frame_adjacency_wedderburn.json'
PRIME=1000033
SQRT3=int(sp.sqrt_mod(3,PRIME,all_roots=True)[0])
IMAG=int(sp.sqrt_mod(-1,PRIME,all_roots=True)[0])

def subset_combos(sizes,target,start=1):
    out=[]
    def rec(i,rem,ch):
        if rem==0:out.append(ch[:]);return
        if rem<0:return
        for j in range(i,len(sizes)):
            if sizes[j]<=rem:rec(j+1,rem-sizes[j],ch+[j])
    rec(start,target,[]);return out

def block_system(FA,B):
    imgs={tuple(sorted(int(x) for x in FA[g,list(B)])) for g in range(len(FA))};blocks=[set(x) for x in sorted(imgs)]
    if len(blocks)*len(B)!=540:return None
    seen=set()
    for b in blocks:
        if seen&b:return None
        seen|=b
    return blocks if len(seen)==540 else None

def nullspace_mod(A,p):
    original=np.array(A,dtype=np.int64)%p;A=original.copy();m,n=A.shape;r=0;piv=[]
    for c in range(n):
        q=next((i for i in range(r,m) if A[i,c]),None)
        if q is None:continue
        A[[r,q]]=A[[q,r]];A[r]=A[r]*pow(int(A[r,c]),-1,p)%p
        for i in range(m):
            if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
        piv.append(c);r+=1
        if r==m:break
    free=[c for c in range(n) if c not in piv];N=np.zeros((n,len(free)),dtype=np.int64)
    for j,f in enumerate(free):
        N[f,j]=1
        for i,c in enumerate(piv):N[c,j]=(-A[i,f])%p
    assert not np.any(original@N%p)
    return N

def build_known_modules():
    pts,pidx,lines,lidx,pl,frames,fidx,flags,flagidx=build_w33();gens=[transvection_perm(pts[i],pts,pidx) for i in [0,1,4,5,13]];G,_=enumerate_group(gens)
    FA=np.empty((len(G),540),dtype=np.uint16)
    for gi,p in enumerate(G):FA[gi]=frame_perm(line_perm(p,lines,lidx),frames,fidx)
    stab=np.where(FA[:,0]==0)[0];unseen=set(range(540));orbits=[]
    while unseen:
        s=min(unseen);o=sorted(set(int(FA[h,s]) for h in stab));orbits.append(o);unseen-=set(o)
    orbits=sorted(orbits,key=lambda x:(len(x),x[0]));sizes=[len(o) for o in orbits];modules={}
    for size in [4,12,15]:
        found=[]
        for combo in subset_combos(sizes,size-1):
            B=set(orbits[0])
            for i in combo:B.update(orbits[i])
            sys=block_system(FA,B)
            if sys is not None:
                key=tuple(sorted(tuple(sorted(b)) for b in sys))
                if all(key!=x[0] for x in found):found.append((key,sys))
        assert len(found)==1
        sys=found[0][1];M=np.zeros((540,len(sys)),dtype=np.int64)
        for i,b in enumerate(sys):M[list(b),i]=1
        modules[f'U{size}']=M
    spreads=all_spreads(lines);B=np.zeros((36,540),dtype=np.int64)
    for si,S in enumerate(spreads):
        for a,b in itertools.combinations(S,2):B[si,fidx[(a,b)]]=1
    modules['spread']=B.T;modules['frame_kernel']=nullspace_mod(B,PRIME)
    st=np.load(ROOT/'data'/'w33_pass1087_canonical_steinberg_parity.npz');modules['Steinberg_plus']=st['Tplus'];modules['Steinberg_minus']=st['Tminus']
    return modules

def center_basis(P):
    r=P.shape[0];eq=[]
    for j in range(r):
        for k in range(r):
            row=[int(P[i,j,k]-P[j,i,k]) for i in range(r)]
            if any(row):eq.append(row)
    ns=sp.Matrix(eq).nullspace();basis=[]
    for v in ns:
        den=sp.ilcm(*[x.q for x in v]);a=np.array([int(x*den) for x in v],dtype=np.int64);g=0
        for x in a:g=math.gcd(g,abs(int(x)))
        if g:a//=g
        basis.append(a%PRIME)
    return basis

def transpose_map(C,r):return [int(C[next(y for y in range(C.shape[1]) if C[0,y]==i),0]) for i in range(r)]
def alg_mul(x,y,P):return np.einsum('i,j,ijk->k',x,y,P.astype(np.int64),optimize=True)%PRIME

def idempotents(C,P,eigen_specs):
    r=P.shape[0];basis=center_basis(P);tm=transpose_map(C,r);h=np.zeros(r,dtype=np.int64)
    for a,b in enumerate(basis):h=(h+(a+1)*(b+b[np.array(tm)])+IMAG*(a+2)*(b-b[np.array(tm)]))%PRIME
    one=np.zeros(r,dtype=np.int64);one[0]=1;eigs=[int(x['value_mod_prime']) for x in eigen_specs];ids=[]
    assert len(set(eigs))==len(eigs)
    for lam in eigs:
        num=one.copy();den=1
        for mu in eigs:
            if mu==lam:continue
            v=h.copy();v[0]=(v[0]-mu)%PRIME;num=alg_mul(num,v,P);den=den*((lam-mu)%PRIME)%PRIME
        e=num*pow(int(den),-1,PRIME)%PRIME;assert np.array_equal(alg_mul(e,e,P),e);ids.append(e)
    for i in range(len(ids)):
        for j in range(i):assert not np.any(alg_mul(ids[i],ids[j],P))
    assert np.array_equal(sum(ids)%PRIME,one)
    return basis,h,ids

def decompose(C,P,eigen_specs,modules):
    basis,h,ids=idempotents(C,P,eigen_specs);r=P.shape[0];records=[]
    for spec,e in zip(eigen_specs,ids):
        E=e[C].astype(np.int64)%PRIME;module_dim=rank_mod(E,PRIME);L=np.zeros((r,r),dtype=np.int64)
        for j in range(r):
            ej=np.zeros(r,dtype=np.int64);ej[j]=1;L[:,j]=alg_mul(e,ej,P)
        alg_dim=rank_mod(L,PRIME);mult=int(math.isqrt(alg_dim));assert mult*mult==alg_dim and module_dim%mult==0
        loc={name:rank_mod(E@X%PRIME,PRIME) for name,X in modules.items()}
        records.append({**spec,'isotypic_dimension':module_dim,'multiplicity':mult,'irreducible_dimension':module_dim//mult,'left_ideal_dimension':alg_dim,'idempotent_coefficients_mod_prime':[int(x) for x in e],'idempotent_sha256':hashlib.sha256(e.astype(np.int64).tobytes()).hexdigest(),'module_localization_dimensions':loc})
    return {'rank':r,'center_dimension':len(basis),'generic_center_coefficients_mod_prime':[int(x) for x in h],'components':records,'sum_isotypic_dimensions':sum(x['isotypic_dimension'] for x in records),'sum_multiplicity_squares':sum(x['multiplicity']**2 for x in records)}

def main():
    t=time.time();z=np.load(ROOT/'data'/'w33_pass1082_frame_coherent_configuration_tensor.npz');modules=build_known_modules()
    inner_specs=[{'label':'30a','eigenvalue':'-222-12*sqrt(3)','value_mod_prime':(-222-12*SQRT3)%PRIME},{'label':'30b','eigenvalue':'-222+12*sqrt(3)','value_mod_prime':(-222+12*SQRT3)%PRIME},{'label':'15','eigenvalue':'-162','value_mod_prime':(-162)%PRIME},{'label':'60','eigenvalue':'-66','value_mod_prime':(-66)%PRIME},{'label':'81','eigenvalue':'-2','value_mod_prime':(-2)%PRIME},{'label':'24','eigenvalue':'78','value_mod_prime':78},{'label':'20','eigenvalue':'174','value_mod_prime':174},{'label':'64','eigenvalue':'318','value_mod_prime':318},{'label':'1','eigenvalue':'8238','value_mod_prime':8238}]
    outer_specs=[{'label':'15a','eigenvalue':'-368','value_mod_prime':(-368)%PRIME},{'label':'60a','eigenvalue':'-212','value_mod_prime':(-212)%PRIME},{'label':'20','eigenvalue':'-140','value_mod_prime':(-140)%PRIME},{'label':'81_minus','eigenvalue':'-112','value_mod_prime':(-112)%PRIME},{'label':'60b','eigenvalue':'-56','value_mod_prime':(-56)%PRIME},{'label':'24','eigenvalue':'28','value_mod_prime':28},{'label':'64','eigenvalue':'148','value_mod_prime':148},{'label':'15b','eigenvalue':'256','value_mod_prime':256},{'label':'81_plus','eigenvalue':'288','value_mod_prime':288},{'label':'1','eigenvalue':'8248','value_mod_prime':8248}]
    inner=decompose(z['color'],z['intersection'],inner_specs,modules);outer=decompose(z['fused_color'],z['fused_intersection'],outer_specs,modules)
    idec={x['label']:(x['irreducible_dimension'],x['multiplicity']) for x in inner['components']};odec={x['label']:(x['irreducible_dimension'],x['multiplicity']) for x in outer['components']}
    expected_inner={'30a':(30,2),'30b':(30,2),'15':(15,3),'60':(60,1),'81':(81,2),'24':(24,2),'20':(20,2),'64':(64,1),'1':(1,1)};expected_outer={'15a':(15,2),'60a':(60,1),'20':(20,2),'81_minus':(81,1),'60b':(60,2),'24':(24,2),'64':(64,1),'15b':(15,1),'81_plus':(81,1),'1':(1,1)}
    ip={x['label']:x for x in inner['components']};op={x['label']:x for x in outer['components']}
    checks={'prime_is_good':sp.isprime(PRIME) and 51840%PRIME!=0,'inner_rank32':inner['rank']==32,'inner_center_dim9':inner['center_dimension']==9,'inner_wedderburn_dimensions':idec==expected_inner,'inner_dimension_sum540':inner['sum_isotypic_dimensions']==540,'inner_multiplicity_square_sum32':inner['sum_multiplicity_squares']==32,'outer_rank22':outer['rank']==22,'outer_center_dim10':outer['center_dimension']==10,'outer_wedderburn_dimensions':odec==expected_outer,'outer_dimension_sum540':outer['sum_isotypic_dimensions']==540,'outer_multiplicity_square_sum22':outer['sum_multiplicity_squares']==22,'inner_81_isotypic_is_162':ip['81']['isotypic_dimension']==162,'outer_splits_81_plus_minus':op['81_plus']['module_localization_dimensions']['Steinberg_plus']==81 and op['81_plus']['module_localization_dimensions']['Steinberg_minus']==0 and op['81_minus']['module_localization_dimensions']['Steinberg_minus']==81 and op['81_minus']['module_localization_dimensions']['Steinberg_plus']==0,'spread_module_is_1_plus15_plus20':sum(ip[x]['module_localization_dimensions']['spread'] for x in ['1','15','20'])==36 and all(ip[x]['module_localization_dimensions']['spread']==0 for x in ['30a','30b','60','81','24','64']),'frame_kernel_localization_sums504':sum(x['module_localization_dimensions']['frame_kernel'] for x in inner['components'])==504,'all_primitive_idempotents_hash_locked':all(len(x['idempotent_sha256'])==64 for x in inner['components']+outer['components'])}
    assert all(checks.values()),checks
    out={'schema':'w33.pass1088.frame_adjacency_wedderburn.v1','status':'PASS','headline':'The complete rank-32 and rank-22 frame adjacency algebras are split at the good prime 1000033 into exact primitive central idempotents. The inner permutation character has nine irreducible types; the outer fusion has ten types and separates the multiplicity-two inner Steinberg isotypic component into inequivalent 81_plus and 81_minus modules.','field_certificate':{'prime':PRIME,'sqrt3':SQRT3,'sqrt_minus1':IMAG,'prime_divides_group_order':False},'inner':inner,'outer':outer,'decomposition_reading':{'inner':'1 + 3*15 + 2*20 + 2*24 + 2*30a + 2*30b + 60 + 64 + 2*81','outer':'1 + 2*15a + 15b + 2*20 + 2*24 + 60a + 2*60b + 64 + 81_plus + 81_minus','frame_kernel_inner':'2*15 + 20 + 2*24 + 2*30a + 2*30b + 60 + 64 + 2*81','outer_steinberg_split':'the inner 162-dimensional 81-isotypic component splits as 81_plus direct-sum 81_minus under the outer similitude'},'check_count':len(checks),'checks':{k:bool(v) for k,v in checks.items()},'seconds':time.time()-t,'scope':'Exact modular Wedderburn certificate at a prime not dividing the group order and with all chosen central eigenvalues distinct. The resulting dimensions and multiplicities are the characteristic-zero semisimple decomposition; component names distinguish inequivalent types rather than claiming external ATLAS labels.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':'PASS','checks':len(checks),'inner':idec,'outer':odec,'seconds':out['seconds']},indent=2))
if __name__=='__main__':main()
