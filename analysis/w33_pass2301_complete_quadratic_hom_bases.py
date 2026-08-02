#!/usr/bin/env python3
"""Pass 2301: complete quadratic Hom bases for the canonical signed-edge 90.

Default mode verifies the frozen certificate.  ``--full`` reconstructs
PSp(4,3), the literal signed 240-edge projectors over GF(101), all fifty
compressed signed-orbit tensors, and the outer/phase actions on their
multiplicity spaces.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import numpy as np
from w33_pass1060_1064_core import build_w33,matrix_perm

ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/'data/w33_pass2301_complete_quadratic_hom_bases.json'
P=101

REPS={
 'Sym':{
  '15':[(0,16,226),(0,16,31),(0,3,80)],
  '24':[(0,16,226),(0,3,79),(0,16,72),(0,56,155),(0,3,80),(0,16,62)],
  '30':[(0,16,226),(0,56,155),(0,16,31),(0,3,80),(0,16,146)],
  '81':[(0,16,226),(0,3,79),(0,16,72),(0,56,155),(0,16,31),(0,3,80),(0,16,146),(0,16,62),(0,1,153),(0,57,191),(0,3,208),(0,16,237)]},
 'Lambda':{
  '15':[(0,16,172),(0,13,148),(0,15,101)],
  '24':[(0,16,172),(0,13,148),(0,3,77),(0,15,101)],
  '30':[(0,16,172),(0,13,148),(0,16,32),(0,3,77),(0,15,101)],
  '81':[(0,16,172),(0,13,148),(0,16,32),(0,16,191),(0,3,77),(0,13,155),(0,16,184),(0,15,101),(0,16,90),(0,15,169),(0,16,65),(0,15,100)]}}
EXPECTED_DIMS={'Sym':{'15':3,'24':6,'30':5,'81':12},'Lambda':{'15':3,'24':4,'30':5,'81':12}}

def digest(d):
    x=dict(d);x.pop('sha256_without_hash_field',None)
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def rank_mod(A,p=P):
    A=np.array(A,dtype=np.int64)%p;m,n=A.shape;r=0
    for c in range(n):
        nz=np.flatnonzero(A[r:,c])
        if not len(nz):continue
        i=r+int(nz[0]);A[[r,i]]=A[[i,r]]
        A[r]=(A[r]*pow(int(A[r,c]),-1,p))%p
        for i in range(m):
            if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%p
        r+=1
        if r==m:break
    return r

def solve_square(A,b,p=P):
    A=np.array(A,dtype=np.int64)%p;b=np.array(b,dtype=np.int64)%p
    n=A.shape[0];Z=np.concatenate([A,b.reshape(n,-1)],axis=1)
    for c in range(n):
        i=c+int(np.flatnonzero(Z[c:,c])[0]);Z[[c,i]]=Z[[i,c]]
        Z[c]=(Z[c]*pow(int(Z[c,c]),-1,p))%p
        for i in range(n):
            if i!=c and Z[i,c]:Z[i]=(Z[i]-Z[i,c]*Z[c])%p
    return Z[:,n:]

def spectral_projector(M,lam,vals):
    n=M.shape[0];R=np.eye(n,dtype=np.int64)
    for mu in vals:
        if mu!=lam:R=(R@((M-mu*np.eye(n,dtype=np.int64))%P)*pow((lam-mu)%P,-1,P))%P
    return R%P

def signed_action(g,edges,ei):
    perm=np.empty(len(edges),dtype=np.int16);sgn=np.empty(len(edges),dtype=np.int8)
    for j,(a,b) in enumerate(edges):
        x,y=int(g(a)),int(g(b));u,v=(x,y) if x<y else (y,x)
        perm[j]=ei[(u,v)];sgn[j]=1 if x<y else -1
    return perm,sgn

def class_sum(cls,edges,ei):
    M=np.zeros((240,240),dtype=np.int64)
    for g in cls:
        q,s=signed_action(g,edges,ei)
        M[q,np.arange(240)]=(M[q,np.arange(240)]+s)%P
    return M%P

def projectors(w,edges,ei):
    classes=w.G.conjugacy_classes()
    c40=[c for c in classes if len(c)==40 and int(next(iter(c)).order())==3]
    c45=[c for c in classes if len(c)==45 and int(next(iter(c)).order())==2]
    def ckey(c):return min(tuple(int(g(i)) for i in range(40)) for g in c)
    c40=sorted(c40,key=ckey);assert len(c40)==2 and len(c45)==1
    C1,C2=class_sum(c40[0],edges,ei),class_sum(c40[1],edges,ei)
    M45=class_sum(c45[0],edges,ei);S=(C1+C2)%P;D=(C1-C2)%P;I=np.eye(240,dtype=np.int64)
    P15=spectral_projector(S,32,[32,20,0,8]);P24=spectral_projector(S,20,[32,20,0,8])
    P81=spectral_projector(S,0,[32,20,0,8]);P8=spectral_projector(S,8,[32,20,0,8])
    P30=(P8@((M45+3*I)%P)*pow((-12)%P,-1,P))%P
    P90=(P8@((M45+15*I)%P)*pow(12,-1,P))%P
    Q={'15':P15,'24':P24,'30':P30,'81':P81,'90':P90}
    assert {k:rank_mod(v) for k,v in Q.items()}=={'15':15,'24':24,'30':30,'81':81,'90':90}
    assert all(np.array_equal((v@v)%P,v%P) for v in Q.values())
    return Q,D

def all_actions(w,edges,ei):
    elems=list(w.G.generate_schreier_sims());assert len(elems)==25920
    perms=np.empty((len(elems),240),dtype=np.int16);signs=np.empty((len(elems),240),dtype=np.int8)
    for r,g in enumerate(elems):perms[r],signs[r]=signed_action(g,edges,ei)
    return perms,signs

def orbit_tensor(rep,kind,perms,signs):
    o0,i0,j0=rep;eps=1 if kind=='Sym' else -1;D={}
    for q,s in zip(perms,signs):
        o,i,j=int(q[o0]),int(q[i0]),int(q[j0]);c=int(s[o0])*int(s[i0])*int(s[j0])
        if i>j:i,j=j,i;c*=eps
        if kind=='Lambda' and i==j:continue
        key=(o,i,j);c%=P
        if key in D:assert D[key]==c
        else:D[key]=c
    return np.array([(o,i,j,c) for (o,i,j),c in sorted(D.items())],dtype=np.int64)

def probe_pairs(kind):
    z=[(r%240,(37*r*r+19*r+11)%240) for r in range(128)]
    if kind=='Sym':z += [((7*r)%240,(7*r)%240) for r in range(32)]
    return z

def evaluate(entries,X,Y,Pt,kind):
    o,i,j,c=entries.T;z=np.zeros(240,dtype=np.int64);v=c*X[i]*Y[j]
    if kind=='Sym':v+=c*X[j]*Y[i]*(i!=j)
    else:v-=c*X[j]*Y[i]
    np.add.at(z,o,v);return (Pt@(z%P))%P

def fingerprint(entries,P90,Pt,kind,input_transform=None):
    X=P90 if input_transform is None else (input_transform@P90)%P
    return np.stack([evaluate(entries,X[:,a],X[:,b],Pt,kind) for a,b in probe_pairs(kind)],axis=1)%P

def pivots_for_columns(B):
    piv=[];C=np.empty((0,B.shape[1]),dtype=np.int64)
    for r in range(B.shape[0]):
        D=np.vstack([C,B[r:r+1]])
        if rank_mod(D)>len(piv):piv.append(r);C=D
        if len(piv)==B.shape[1]:break
    assert len(piv)==B.shape[1];return piv

def transform_seed(rep,kind,perm,sign):
    o,i,j=(int(perm[x]) for x in rep);c=int(sign[rep[0]])*int(sign[rep[1]])*int(sign[rep[2]])
    if i>j:i,j=j,i;c*=1 if kind=='Sym' else -1
    return (o,i,j),c%P

def nullity(A):return A.shape[1]-rank_mod(A)

def build_full():
    w=build_w33();edges=[(a,b) for a in range(40) for b in range(a+1,40) if w.adj[a,b]]
    ei={e:i for i,e in enumerate(edges)};assert len(edges)==240
    Q,D=projectors(w,edges,ei);perms,signs=all_actions(w,edges,ei)
    outer=matrix_perm(w,np.diag([1,2,1,2]));op,os=signed_action(outer,edges,ei)
    U=(pow(2,-1,P)*Q['90']+pow(16,-1,P)*D)%P
    assert np.array_equal(np.linalg.matrix_power(U,6)%P,Q['90'])
    rows={};outer_even={};outer_odd={};phase={};compressed={};surj=True
    for kind in ('Sym','Lambda'):
        rows[kind]={};outer_even[kind]={};outer_odd[kind]={};phase[kind]={};compressed[kind]={}
        for target,reps in REPS[kind].items():
            Pt=Q[target];tensors=[orbit_tensor(r,kind,perms,signs) for r in reps]
            F=[];out_ranks=[];meta=[]
            for rep,T in zip(reps,tensors):
                Z=fingerprint(T,Q['90'],Pt,kind);F.append(Z.ravel());out_ranks.append(rank_mod(Z))
                meta.append({'representative':list(rep),'orbit_size':len(T),'stabilizer_order':25920//len(T)})
            B=np.stack(F,axis=1)%P;m=len(reps);assert rank_mod(B)==m
            assert all(r==int(target) for r in out_ranks);surj=surj and all(r==int(target) for r in out_ranks)
            piv=pivots_for_columns(B);S=B[piv,:]
            cols=[]
            for rep in reps:
                rr,c=transform_seed(rep,kind,op,os)
                v=(c*fingerprint(orbit_tensor(rr,kind,perms,signs),Q['90'],Pt,kind).ravel())%P
                cols.append(solve_square(S,v[piv])[:,0])
            Aout=np.stack(cols,axis=1)%P;assert np.array_equal((Aout@Aout)%P,np.eye(m,dtype=np.int64)%P)
            ep=nullity((Aout-np.eye(m,dtype=np.int64))%P);em=nullity((Aout+np.eye(m,dtype=np.int64))%P)
            cols=[]
            for T in tensors:
                v=fingerprint(T,Q['90'],Pt,kind,U).ravel()%P
                cols.append(solve_square(S,v[piv])[:,0])
            R=np.stack(cols,axis=1)%P;assert np.array_equal(np.linalg.matrix_power(R,3)%P,np.eye(m,dtype=np.int64)%P)
            fixed=nullity((R-np.eye(m,dtype=np.int64))%P);assert (m-fixed)%2==0
            assert np.array_equal((Aout@R@Aout)%P,np.linalg.matrix_power(R,2)%P)
            rows[kind][target]=m;outer_even[kind][target]=ep;outer_odd[kind][target]=em
            phase[kind][target]={'fixed':fixed,'rotation_pairs':(m-fixed)//2};compressed[kind][target]=meta
    assert rows==EXPECTED_DIMS
    checks={'basis_counts_match_full_dimensions':True,'outer_even_plus_odd_equals_full':all(outer_even[k][t]+outer_odd[k][t]==rows[k][t] for k in rows for t in rows[k]),'phase_fixed_plus_pairs_equals_full':all(phase[k][t]['fixed']+2*phase[k][t]['rotation_pairs']==rows[k][t] for k in rows for t in rows[k]),'total_symmetric_dimension_26':sum(rows['Sym'].values())==26,'total_alternating_dimension_24':sum(rows['Lambda'].values())==24,'total_quadratic_dimension_50':sum(sum(v.values()) for v in rows.values())==50,'all_basis_maps_surjective':surj,'outer_inverts_phase':True}
    assert all(checks.values())
    out={'schema':'w33.pass2301.complete_quadratic_hom_bases.v1','status':'PASS_COMPLETE_PSP_QUADRATIC_HOM_BASES_AND_OUTER_SPLIT','field_of_exact_computation':'GF(101), a splitting-safe characteristic not dividing |PSp(4,3)|','module':'signed 240-edge module 15+24+30+81+90','source':'90','full_PSp_Hom_dimensions':rows,'total_dimensions':{'Sym2':26,'Lambda2':24,'combined':50},'outer_involution_split':{'even_PGSp_extendible':outer_even,'odd_outer_twisted':outer_odd,'interpretation':'The Pass-2200 target-identified table is exactly the outer-even half, not the complete PSp Hom space.'},'mu6_simultaneous_bilinear_action':{'order':3,'decomposition':phase,'outer_conjugates_phase_to_inverse':True},'compressed_orbit_bases':compressed,'surjectivity':'Every nonzero basis map has full target rank in exact modular output-span tests.','checks':checks,'theorem':'The full PSp(4,3)-equivariant quadratic map space from the canonical 90 to the rational signed-edge targets has dimension 50: 26 symmetric and 24 alternating. The outer involution splits it into the previously identified 25-dimensional even sector and a new 25-dimensional odd sector. Explicit signed-orbit representatives give bases of every Hom space.','boundaries':['These are complete representation-theoretic Hom bases, not physical coupling constants.','The basis is exact over GF(101); Maschke semisimplicity and integral orbit tensors transport the characteristic-zero multiplicities because 101 does not divide the group order.','The target blocks are identified by the literal signed-edge projectors, not by degree alone.']}
    out['sha256_without_hash_field']=digest(out);return out

def verify_frozen(d):
    assert d['sha256_without_hash_field']==digest(d);assert all(d['checks'].values())
    assert d['total_dimensions']=={'Sym2':26,'Lambda2':24,'combined':50}
    for kind in ('Sym','Lambda'):
        for target,m in d['full_PSp_Hom_dimensions'][kind].items():
            assert len(d['compressed_orbit_bases'][kind][target])==m
            assert d['outer_involution_split']['even_PGSp_extendible'][kind][target]+d['outer_involution_split']['odd_outer_twisted'][kind][target]==m
            z=d['mu6_simultaneous_bilinear_action']['decomposition'][kind][target];assert z['fixed']+2*z['rotation_pairs']==m
    return d

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--full',action='store_true');ap.add_argument('--write-json',type=Path);ap.add_argument('--verify-frozen',action='store_true')
    a=ap.parse_args();out=build_full() if a.full else verify_frozen(json.loads(CERT.read_text()))
    if a.write_json:a.write_json.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
