#!/usr/bin/env python3
"""Pass8409-8416: resolve the residue index by an exact D4+D4 / relative-triality calculation.

Pass7949 puts the explicit Q+(3,3) residue in the first four coordinates of
E8/3E8.  Work directly with the eight E8 simple reflections mod 3.  Orbit the
nondegenerate 4-space W=<e1,...,e4>, use Schreier generators for its stabilizer,
and project each stabilizer matrix onto W and W^perp.

The result is a Goursat fiber product: both 4x4 projections have order 1152,
both projection kernels have order 192, and the common quotient has order 6
with order census 1^1 2^3 3^2, hence S3.  Thus the linear lift is
W(F4) x_{S3} W(F4): the two D4 triality labels are forced to agree.
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

def inv(A):
    A=np.array(A,dtype=np.int8)%P;n=len(A);B=np.concatenate([A,np.eye(n,dtype=np.int8)],1)%P;r=0
    for c in range(n):
        z=next(i for i in range(r,n) if B[i,c]);B[[r,z]]=B[[z,r]]
        B[r]=(B[r]*pow(int(B[r,c]),-1,P))%P
        for i in range(n):
            if i!=r and B[i,c]:B[i]=(B[i]-B[i,c]*B[r])%P
        r+=1
    return B[:,n:]%P

def rref(B):
    A=np.array(B,dtype=np.int8)%P;m,n=A.shape;r=0
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
def unkey(k):return np.frombuffer(k,dtype=np.uint8).astype(np.int8).reshape(4,4)
def mul(k,l):return key((unkey(k)@unkey(l))%P)
def pairkey(A,B):return key(A)+key(B)

def closure(gens):
    I=np.eye(4,dtype=np.int8);out={pairkey(I,I):(I,I)};q=collections.deque([(I,I)])
    while q:
        A,B=q.popleft()
        for C,D in gens:
            X=(A@C)%P;Y=(B@D)%P;k=pairkey(X,Y)
            if k not in out:out[k]=(X,Y);q.append((X,Y))
    return out

def p1(v):
    v=tuple(int(x)%3 for x in v)
    for x in v:
        if x:return tuple(((1 if x==1 else 2)*y)%3 for y in v)
    raise ValueError

def det2(x):return (x[0]*x[3]-x[1]*x[2])%3

def main():
    I8=np.eye(8,dtype=np.int8);gens=[]
    for r in SIMPLES:
        v=np.array(r,dtype=np.int8).reshape(8,1)%3
        S=(I8-v@v.T)%3       # root norm is 8, so 1/4 = 1 mod 3
        assert np.array_equal((S@S)%3,I8)
        gens.append(S)
    W=np.eye(8,dtype=np.int8)[:4,:];k0=rref(W)
    orb=[k0];oi={k0:0};reps=[I8.copy()];dq=collections.deque([0]);sch=[]
    while dq:
        i=dq.popleft();t=reps[i]
        for S in gens:
            nt=(S@t)%3;k=rref(W@nt.T)
            if k not in oi:oi[k]=len(orb);orb.append(k);reps.append(nt);dq.append(len(orb)-1)
            j=oi[k];h=(inv(reps[j])@S@t)%3
            assert not np.any(h[4:,:4]) and not np.any(h[:4,4:])
            sch.append((h[:4,:4].copy(),h[4:,4:].copy()))
    assert len(orb)==3150
    # Only a small set of distinct block pairs is needed.
    seen=set();pg=[]
    for A,B in sch:
        k=pairkey(A,B)
        if k not in seen:seen.add(k);pg.append((A,B))
    H=closure(pg);assert len(H)==221184
    I4=key(np.eye(4,dtype=np.int8))
    Aset={k[:16] for k in H};Bset={k[16:] for k in H}
    KA={k[:16] for k in H if k[16:]==I4};KB={k[16:] for k in H if k[:16]==I4}
    assert len(Aset)==len(Bset)==1152 and len(KA)==len(KB)==192
    # Quotient A/KA: six cosets and S3 order census.
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

    # Projective action on the 16 singular points of W.  The linear 1152 group
    # has scalar kernel {+I,-I}, so its image has order 576.
    pts=sorted({p1(x) for x in itertools.product(range(3),repeat=4) if any(x) and sum(y*y for y in x)%3==0})
    assert len(pts)==16;pi={x:i for i,x in enumerate(pts)}
    perms=set()
    for ak in Aset:
        A=unkey(ak);perms.add(tuple(pi[p1(tuple(int(z) for z in (A@np.array(x,dtype=np.int8))%3))] for x in pts))
    assert len(perms)==576

    out={
      'schema':'w33.pass8409_8416.e8_d4d4_relative_triality.v1','status':'PASS','passes':'8409-8416',
      'Qplus33_orbit_under_projective_E8':3150,
      'linear_E8_residue_stabilizer_order':221184,
      'two_block_projections':{'orders':[1152,1152],'identification':'O4+(3) ~= W(F4) on each nondegenerate 4-space','projection_kernel_orders':[192,192],'kernel_identification':'W(D4)'},
      'goursat_common_quotient':{'order':6,'element_order_census':{'1':1,'2':3,'3':2},'identification':'S3 = D4 triality'},
      'fiber_product':'W(F4) x_{S3} W(F4)','meaning':'the two independent F4/D4 triality labels of the ambient product are constrained to agree inside E8',
      'ambient_linear_residue_stabilizer':{'order':1327104,'structure':'W(F4) x W(F4)','index_of_linear_E8_stabilizer':6,'six_cosets':'six relative-triality states; S3 x S3 acts on cosets of diagonal S3'},
      'projective_E8_stabilizer_order':110592,
      'residue_16_point_action':{'E8_image_order':576,'E8_pointwise_kernel_order':192,'full_rook_graph_automorphism_order':1152,'missing_point_parity_index':2},
      'index12_interpretation':'Pass8309 full-triality-carrier index 12 factors structurally as 6 relative D4 trialities times one extra C2 point/type parity. The intrinsic linear D4+D4 enlargement is index 6.',
      'theorem':'The E8 stabilizer of the explicit D4+D4 / Q+(3,3) residue is a triality fiber product, not an arbitrary subgroup: its linear lift is W(F4) x_{S3} W(F4). The six inner cosets are relative triality states; the 12-state full carrier enlargement is 6 x 2 after the outer parity/type extension.',
      'claim_boundary':'Exact mod-3 Weyl-matrix/Goursat calculation. The 6x2 factorization is a finite-group carrier statement, not a generation or particle claim.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','Hlin':len(H),'quotient':'S3','inner_index':6,'projective_point_image':len(perms)}))
if __name__=='__main__':main()
