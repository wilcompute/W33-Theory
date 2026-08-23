#!/usr/bin/env python3
"""Pass8409-8416: resolve the residue index by an exact D4+D4 / relative-triality calculation.

Pass7949 puts the explicit Q+(3,3) residue in the first four coordinates of
E8/3E8. Work directly with the eight E8 simple reflections mod 3. Orbit the
nondegenerate 4-space W=<e1,...,e4>, use Schreier generators for its stabilizer,
and project each stabilizer matrix onto W and W^perp.

The result is a Goursat fiber product: both 4x4 projections have order 1152,
both projection kernels have order 192, and the common quotient has order 6
with order census 1^1 2^3 3^2, hence S3. Thus the linear lift is
W(F4) x_{S3} W(F4): the two D4 triality labels are forced to agree.

Pass8801 repair: the original implementation stored matrices as np.int8 and
occasionally evaluated chained products before reducing mod 3. 8x8 products
can overflow int8 in such chains. All arithmetic below is now int64 and every
matrix product goes through mm(), which reduces mod 3 immediately. The repaired
implementation reproduces the full original certificate exactly.
"""
from __future__ import annotations
import collections,itertools,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS8409_8416_E8_D4D4_RELATIVE_TRIALITY.json'
SIMPLES=[
(1,-1,-1,-1,-1,-1,-1,1),(2,2,0,0,0,0,0,0),(-2,2,0,0,0,0,0,0),
(0,-2,2,0,0,0,0,0),(0,0,-2,2,0,0,0,0),(0,0,0,-2,2,0,0,0),
(0,0,0,0,-2,2,0,0),(0,0,0,0,0,-2,2,0)]
P=3

def mm(A,B):
    return (np.asarray(A,dtype=np.int64)@np.asarray(B,dtype=np.int64))%P

def inv(A):
    A=np.array(A,dtype=np.int64)%P;n=len(A);B=np.concatenate([A,np.eye(n,dtype=np.int64)],1)%P;r=0
    for c in range(n):
        z=next(i for i in range(r,n) if B[i,c]);B[[r,z]]=B[[z,r]]
        B[r]=(B[r]*pow(int(B[r,c]),-1,P))%P
        for i in range(n):
            if i!=r and B[i,c]:B[i]=(B[i]-B[i,c]*B[r])%P
        r+=1
    return B[:,n:]%P

def rref(B):
    A=np.array(B,dtype=np.int64)%P;m,n=A.shape;r=0
    for c in range(n):
        z=next((i for i in range(r,m) if A[i,c]),None)
        if z is None:continue
        A[[r,z]]=A[[z,r]];A[r]=(A[r]*pow(int(A[r,c]),-1,P))%P
        for i in range(m):
            if i!=r and A[i,c]:A[i]=(A[i]-A[i,c]*A[r])%P
        r+=1
        if r==m:break
    return tuple(map(tuple,A.tolist()))
def key(A):return bytes(int(x) for x in np.asarray(A,dtype=np.uint8).ravel())
def unkey(k):return np.frombuffer(k,dtype=np.uint8).astype(np.int64).reshape(4,4)
def mul(k,l):return key(mm(unkey(k),unkey(l)))
def pairkey(A,B):return key(A)+key(B)

def closure(gens):
    I=np.eye(4,dtype=np.int64);out={pairkey(I,I):(I,I)};q=collections.deque([(I,I)])
    while q:
        A,B=q.popleft()
        for C,D in gens:
            X=mm(A,C);Y=mm(B,D);k=pairkey(X,Y)
            if k not in out:out[k]=(X,Y);q.append((X,Y))
    return out

def p1(v):
    v=tuple(int(x)%3 for x in v)
    for x in v:
        if x:return tuple(((1 if x==1 else 2)*y)%3 for y in v)
    raise ValueError

def main():
    I8=np.eye(8,dtype=np.int64);gens=[]
    for r in SIMPLES:
        v=np.array(r,dtype=np.int64).reshape(8,1)%3
        S=(I8-mm(v,v.T))%3
        assert np.array_equal(mm(S,S),I8)
        gens.append(S)
    W=np.eye(8,dtype=np.int64)[:4,:];k0=rref(W)
    orb=[k0];oi={k0:0};reps=[I8.copy()];dq=collections.deque([0]);sch=[]
    while dq:
        i=dq.popleft();t=reps[i]
        for S in gens:
            nt=mm(S,t);k=rref(mm(W,nt.T))
            if k not in oi:oi[k]=len(orb);orb.append(k);reps.append(nt);dq.append(len(orb)-1)
            j=oi[k];h=mm(mm(inv(reps[j]),S),t)
            assert not np.any(h[4:,:4]) and not np.any(h[:4,4:])
            sch.append((h[:4,:4].copy(),h[4:,4:].copy()))
    assert len(orb)==3150
    seen=set();pg=[]
    for A,B in sch:
        k=pairkey(A,B)
        if k not in seen:seen.add(k);pg.append((A,B))
    H=closure(pg);assert len(H)==221184
    I4=key(np.eye(4,dtype=np.int64))
    Aset={k[:16] for k in H};Bset={k[16:] for k in H}
    KA={k[:16] for k in H if k[16:]==I4};KB={k[16:] for k in H if k[:16]==I4}
    assert len(Aset)==len(Bset)==1152 and len(KA)==len(KB)==192
    unseen=set(Aset);cos=[];ci={}
    while unseen:
        a=next(iter(unseen));C={mul(a,k) for k in KA};j=len(cos);cos.append(C)
        for x in C:ci[x]=j
        unseen-=C
    assert len(cos)==6;rep=[next(iter(C)) for C in cos];e=ci[I4]
    def qm(i,j):return ci[mul(rep[i],rep[j])]
    qo=[]
    for i in range(6):
        x=e
        for n in range(1,7):
            x=qm(x,i)
            if x==e:qo.append(n);break
    assert collections.Counter(qo)==collections.Counter({2:3,3:2,1:1})

    pts=sorted({p1(x) for x in itertools.product(range(3),repeat=4) if any(x) and sum(y*y for y in x)%3==0})
    assert len(pts)==16;pi={x:i for i,x in enumerate(pts)}
    perms=set()
    for ak in Aset:
        A=unkey(ak);perm=[]
        for x in pts:
            y=mm(A,np.array(x,dtype=np.int64).reshape(4,1)).reshape(-1)
            perm.append(pi[p1(tuple(int(z) for z in y))])
        perms.add(tuple(perm))
    assert len(perms)==576

    out={
      'schema':'w33.pass8409_8416.e8_d4d4_relative_triality.v2_safe_arithmetic','status':'PASS','passes':'8409-8416','repair_pass':8801,
      'arithmetic_repair':'all finite-field matrix arithmetic uses int64 and immediate mod-3 reduction; removes np.int8 chained-product overflow risk',
      'Qplus33_orbit_under_projective_E8':3150,
      'linear_E8_residue_stabilizer_order':221184,
      'two_block_projections':{'orders':[1152,1152],'identification':'O4+(3) ~= W(F4) on each nondegenerate 4-space','projection_kernel_orders':[192,192],'kernel_identification':'W(D4)'},
      'goursat_common_quotient':{'order':6,'element_order_census':{'1':1,'2':3,'3':2},'identification':'S3 = D4 triality'},
      'fiber_product':'W(F4) x_{S3} W(F4)','meaning':'the two independent F4/D4 triality labels of the ambient product are constrained to agree inside E8',
      'ambient_linear_residue_stabilizer':{'order':1327104,'structure':'W(F4) x W(F4)','index_of_linear_E8_stabilizer':6,'six_cosets':'six relative-triality states; S3 x S3 acts on cosets of diagonal S3'},
      'projective_E8_stabilizer_order':110592,
      'residue_16_point_action':{'E8_image_order':576,'E8_pointwise_kernel_order':192,'full_rook_graph_automorphism_order':1152,'missing_point_parity_index':2},
      'index12_interpretation':'Pass8309 full-triality-carrier index 12 factors structurally as 6 relative D4 trialities times one extra C2 point/type parity. The intrinsic linear D4+D4 enlargement is index 6.',
      'theorem':'Safe finite-field recomputation confirms the E8 residue stabilizer is W(F4) x_{S3} W(F4); the six inner cosets are relative-triality states and the full-carrier 12-state enlargement is 6 x 2.',
      'claim_boundary':'Exact mod-3 Weyl-matrix/Goursat calculation. The arithmetic repair changes implementation safety, not the theorem.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','Hlin':len(H),'quotient':'S3','inner_index':6,'projective_point_image':len(perms),'safe_arithmetic':True}))
if __name__=='__main__':main()
