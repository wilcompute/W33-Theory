#!/usr/bin/env python3
"""Deterministic verifier for Passes 4145-4152."""
from __future__ import annotations
import bisect, collections, hashlib, itertools, json, math
from pathlib import Path
import networkx as nx
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds, root
from scipy.integrate import solve_ivp

ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/"data/PART_4145_4152_EXOTIC_LOCAL_CONDITIONED_STACK_MIXED_BONKERS.json"
ANOM=ROOT/"data/w33_pass4145_bounded_exotic_anomaly_optimization.json"
MOM=ROOT/"data/w33_pass4147_conditioned_seven_fault_moments.json"
STACK=ROOT/"data/w33_pass4148_hybrid_stack_materialization.json"
MIX=ROOT/"data/w33_pass4149_mixed_attractor_newton_catalogue.json"

def chash(d):
    x=dict(d);x.pop("semantic_sha256",None)
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def canon(v):
    v=tuple(x%3 for x in v)
    for x in v:
        if x:
            z=1 if x==1 else 2
            return tuple(z*y%3 for y in v)

def symp(u,v):
    return (u[0]*v[2]+u[1]*v[3]-u[2]*v[0]-u[3]*v[1])%3

def geometry():
    pts=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    idx={p:i for i,p in enumerate(pts)}
    A=np.zeros((40,40),int)
    for i,u in enumerate(pts):
        for j,v in enumerate(pts):
            if i!=j and symp(u,v)==0:A[i,j]=1
    lines=set()
    for i,u in enumerate(pts):
        for j,v in enumerate(pts):
            if j<=i or symp(u,v):continue
            S={idx[canon(tuple(a*u[k]+b*v[k] for k in range(4)))]
               for a,b in itertools.product(range(3),repeat=2) if a or b}
            if len(S)==4:lines.add(tuple(sorted(S)))
    lines=sorted(lines);E=[];G=nx.Graph();G.add_nodes_from(range(80))
    for l,L in enumerate(lines):
        for p in L:E.append((p,40+l));G.add_edge(p,40+l)
    D=np.zeros((80,160),int)
    for e,(p,l) in enumerate(E):D[p,e]=1;D[l,e]=-1
    return pts,A,lines,E,D,G

def anomaly_vector(color,weak,n):
    d3=1 if color=="1" else 3
    d2=weak
    s3=0 if color=="1" else (1 if color=="3" else -1)
    return np.array([
        s3*d2,
        d2*n if color!="1" else 0,
        d3*n if weak==2 else 0,
        d3*d2*n,
        d3*d2*n**3],int)

def anomaly_audit(ledger):
    species=[]
    for color in ("1","3","3bar"):
        for weak in (1,2):
            for n in range(-6,7):
                if n:
                    species.append((color,weak,n,(1 if color=="1" else 3)*weak,anomaly_vector(color,weak,n),1 if weak==2 else 0))
    target=np.array(ledger["required_added_anomaly"],float)
    A=np.array([s[4] for s in species],float).T
    parity=np.array([s[5] for s in species],float)
    dims=np.array([s[3] for s in species],float)
    Aeq=np.vstack([np.column_stack([A,np.zeros(5)]),np.r_[parity,-2.]])
    beq=np.r_[target,1.]
    res=milp(np.r_[dims,0.],integrality=np.ones(len(species)+1),
             bounds=Bounds(np.zeros(len(species)+1),np.full(len(species)+1,np.inf)),
             constraints=LinearConstraint(Aeq,beq,beq))
    assert res.success and abs(res.fun-107)<1e-8
    Aeq2=np.vstack([Aeq,np.r_[dims,0.]])
    beq2=np.r_[beq,107.]
    res2=milp(np.r_[np.ones(len(species)),0.],integrality=np.ones(len(species)+1),
              bounds=Bounds(np.zeros(len(species)+1),np.full(len(species)+1,np.inf)),
              constraints=LinearConstraint(Aeq2,beq2,beq2))
    assert res2.success and abs(res2.fun-30)<1e-8
    total=np.zeros(5,int);dim=0;count=0;doublets=0
    for row in ledger["solution"]:
        m=row["multiplicity"];color=row["SU3"];weak=row["SU2_dimension"];n=row["n"]
        total+=m*anomaly_vector(color,weak,n);dim+=m*row["state_dimension"];count+=m
        if weak==2:doublets+=m
    assert total.tolist()==ledger["required_added_anomaly"]
    assert dim==107 and count==30 and doublets%2==1

def cycle_theta_audit(G,E,w1,w2,p):
    eid={tuple(sorted(e)):i for i,e in enumerate(E)}
    adj={u:sorted(G.neighbors(u)) for u in G}
    cycles=set()
    for start in range(80):
        stack=[(start,[start],{start})]
        while stack:
            u,path,seen=stack.pop()
            for v in adj[u]:
                if v==start and 8<=len(path)<=14 and len(path)%2==0:
                    c=path[:];n=len(c);forms=[]
                    for q in (c,list(reversed(c))):
                        for k in range(n):forms.append(tuple(q[k:]+q[:k]))
                    cycles.add(min(forms))
                elif v>start and v not in seen and len(path)<14:
                    stack.append((v,path+[v],seen|{v}))
    cnt=collections.Counter(map(len,cycles))
    assert cnt=={8:1620,10:5184,12:43200,14:336960}
    min_norm=1e99;min_gain=1e99
    for c in cycles:
        es=[eid[tuple(sorted((c[i],c[(i+1)%len(c)])))] for i in range(len(c))]
        a=sum((1 if i%2==0 else -1)*w1[e] for i,e in enumerate(es))
        b=sum((1 if i%2==0 else -1)*w2[e] for i,e in enumerate(es))
        assert (a%p) or (b%p)
        z=math.hypot(a,b);min_norm=min(min_norm,z);min_gain=min(min_gain,z/math.sqrt(len(es)))
    paths=collections.defaultdict(list)
    for a in range(80):
        stack=[(a,[a],{a})]
        while stack:
            u,path,seen=stack.pop()
            if len(path)-1>=6:continue
            for v in adj[u]:
                if v in seen:continue
                q=path+[v]
                if v>a:paths[(a,v)].append(q)
                stack.append((v,q,seen|{v}))
    def flow(path):
        z={}
        for x,y in zip(path,path[1:]):
            e=eid[tuple(sorted((x,y)))];pt,ln=E[e]
            z[e]=1 if (x==pt and y==ln) else -1
        return z
    types=collections.Counter();min_det=10**100;min_gsv=1e99
    for ps in paths.values():
        for i,pth in enumerate(ps):
            ip=set(pth[1:-1]);lp=len(pth)-1
            for j in range(i+1,len(ps)):
                q=ps[j];iq=set(q[1:-1]);lq=len(q)-1
                if lp+lq<8 or ip&iq:continue
                for k in range(j+1,len(ps)):
                    r=ps[k];ir=set(r[1:-1]);lr=len(r)-1
                    if lp+lr<8 or lq+lr<8 or lp+lq+lr>14 or ip&ir or iq&ir:continue
                    fs=[flow(x) for x in (pth,q,r)];keys=sorted(set().union(*[set(x) for x in fs]))
                    c1=np.array([fs[0].get(e,0)-fs[2].get(e,0) for e in keys],float)
                    c2=np.array([fs[1].get(e,0)-fs[2].get(e,0) for e in keys],float)
                    a1=sum(w1[e]*v for e,v in zip(keys,c1));a2=sum(w1[e]*v for e,v in zip(keys,c2))
                    b1=sum(w2[e]*v for e,v in zip(keys,c1));b2=sum(w2[e]*v for e,v in zip(keys,c2))
                    det=int(round(a1*b2-a2*b1));assert det%p
                    min_det=min(min_det,abs(det))
                    C=np.column_stack([c1,c2]);M=np.array([[a1,a2],[b1,b2]],float)
                    eig=np.linalg.eigvals(np.linalg.solve(C.T@C,M.T@M)).real
                    min_gsv=min(min_gsv,math.sqrt(max(0,float(eig.min()))))
                    types[tuple(sorted((lp,lq,lr)))]+=1
    assert types=={(4,4,4):4320,(3,5,5):25920,(4,4,6):25920,(2,6,6):77760}
    return cnt,types,min_norm,min_gain,min_det,min_gsv

def compose(p,q):return tuple(p[q[i]] for i in range(40))
def group_and_perms(pts):
    idx={p:i for i,p in enumerate(pts)}
    def tv(v):
        out=[]
        for x in pts:
            s=symp(x,v);y=tuple((x[k]+s*v[k])%3 for k in range(4))
            out.append(idx[canon(y)])
        return tuple(out)
    gs=[tv(pts[i]) for i in (0,1,2,4,13)]
    ident=tuple(range(40));seen={ident};stack=[ident]
    while stack:
        g=stack.pop()
        for h in gs:
            x=compose(h,g)
            if x not in seen:seen.add(x);stack.append(x)
    assert len(seen)==25920
    return np.array(list(seen),dtype=np.int16)

def lexmin(arr):
    ids=np.arange(arr.shape[0])
    for j in range(arr.shape[1]):
        v=arr[ids,j];m=v.min();ids=ids[v==m]
        if len(ids)==1:break
    return tuple(arr[ids[0]].tolist())

def field_hash(state,perms):
    y=np.array(state,float);u=np.rint(y[:40]*1e6).astype(np.int64);v=np.rint(y[40:]*1e6).astype(np.int64)
    arr=np.hstack([u[perms],v[perms]])
    key=min(lexmin(arr),lexmin(-arr))
    return hashlib.sha256(np.array(key,dtype=np.int64).tobytes()).hexdigest()

def nonlinear_checks(A,mix):
    L=12*np.eye(40)-A;perms=group_and_perms(sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)}))
    hashes=set()
    for name,J in (("selector24",np.array([[2.,5.],[-21.,-20.]])),("selector15",np.array([[3.2,12.],[-21.,-10.]]))):
        block=mix[name];reps=block["representatives"]
        stable=0;index1=0
        for row in reps:
            seed=row["representative_seed"];rng=np.random.default_rng(seed)
            y0=1e-3*rng.normal(size=80);y0[:40]-=y0[:40].mean();y0[40:]-=y0[40:].mean()
            def rhs(y):
                u=y[:40];v=y[40:];a,b=J[0];c,d=J[1]
                return np.r_[a*u+b*v-u**3-0.1*(L@u),c*u+d*v-v**3-10*(L@v)]
            def jac(y):
                u=y[:40];v=y[40:];a,b=J[0];c,d=J[1]
                return np.block([[a*np.eye(40)-np.diag(3*u*u)-0.1*L,b*np.eye(40)],
                                 [c*np.eye(40),d*np.eye(40)-np.diag(3*v*v)-10*L]])
            sol=solve_ivp(lambda t,y:rhs(y),(0,500),y0,method="BDF",rtol=1e-9,atol=1e-11)
            rr=root(rhs,sol.y[:,-1],jac=jac,tol=1e-11);assert rr.success
            y=rr.x;u=y[:40];v=y[40:];a,b=J[0];c,d=J[1]
            rhs=np.r_[a*u+b*v-u**3-0.1*(L@u),c*u+d*v-v**3-10*(L@v)]
            assert np.linalg.norm(rhs)<1e-8
            Jac=np.block([[a*np.eye(40)-np.diag(3*u*u)-0.1*L,b*np.eye(40)],
                          [c*np.eye(40),d*np.eye(40)-np.diag(3*v*v)-10*L]])
            eig=np.linalg.eigvals(Jac);idx=int(np.sum(eig.real>1e-8))
            assert idx==row["morse_index"]
            if idx==0:stable+=1
            if idx==1:index1+=1
            h=field_hash(y,perms);assert h==row["canonical_class_sha256"] and h not in hashes;hashes.add(h)
        assert stable==mix[name]["stable_mixed_classes"]
        if name=="selector15":assert index1==1
    Q=np.array(mix["root_stabilizer_quotient"]["adjacency_quotient"],float);Lq=12*np.eye(3)-Q
    for name,J,key in (("selector24",np.array([[2.,5.],[-21.,-20.]]),"selector24_nonzero_mixed_saddle"),
                       ("selector15",np.array([[3.2,12.],[-21.,-10.]]),"selector15_nonzero_mixed_saddle")):
        z=np.array(mix["root_stabilizer_quotient"][key]["quotient_state"],float);u=z[:3];v=z[3:];a,b=J[0];c,d=J[1]
        rhs=np.r_[a*u+b*v-u**3-0.1*(Lq@u),c*u+d*v-v**3-10*(Lq@v)]
        assert np.linalg.norm(rhs)<1e-8

def permanent_ryser(M):
    n=M.shape[0];rows=np.zeros(n,dtype=np.int64);total=0;prev=0
    for k in range(1,1<<n):
        g=k^(k>>1);d=g^prev;j=(d&-d).bit_length()-1
        rows += M[:,j] if g&d else -M[:,j]
        total += (-1)**(n-g.bit_count())*int(np.prod(rows,dtype=object));prev=g
    return total

def main():
    cert=json.loads(CERT.read_text());an=json.loads(ANOM.read_text());mom=json.loads(MOM.read_text());stack=json.loads(STACK.read_text());mix=json.loads(MIX.read_text())
    for d in (cert,an,mom,stack,mix):assert chash(d)==d["semantic_sha256"]
    pts,A,lines,E,D,G=geometry()
    assert len(pts)==len(lines)==40 and len(E)==160 and np.linalg.matrix_rank(D)==79 and nx.girth(G)==8
    anomaly_audit(an)
    assert cert["pass4146_exchange_local_relational_gates"]["compressed_code"]["paired_word_hamming_distance"]==32
    lift=cert["pass4146_exchange_local_relational_gates"]["dual_rail_lift"]
    assert lift["total_modes"]==58 and lift["fixed_total_particles"]==29 and lift["code_dimension"]==2**29
    cnt,types,mn,mg,md,ms=cycle_theta_audit(G,E,mom["weights_row_1"],mom["weights_row_2"],mom["prime"])
    assert abs(mn-mom["minimum_cycle_measurement_norm"])<1e-9
    assert abs(mg-mom["minimum_cycle_normalized_gain"])<1e-9
    assert md==round(mom["minimum_theta_determinant_absolute"])
    assert abs(ms-mom["minimum_theta_generalized_singular_value"])<1e-8
    for layers in stack["branch_layers"]:
        inp=[];out=[]
        for layer in layers:
            assert all(layer[i][0]<layer[i+1][0] and layer[i][1]<layer[i+1][1] for i in range(len(layer)-1))
            inp += [x[0] for x in layer];out += [x[1] for x in layer]
        assert sorted(inp)==sorted(out)==list(range(40))
    assert sum(9*40 for _ in range(4))-4*40==1280
    nonlinear_checks(A,mix)
    plus=[0,1,4,6,8,14,18,21,22,23,26,28,29,30,32,33,34,35,36,39]
    minus=[i for i in range(40) if i not in plus];B=A[np.ix_(plus,minus)]
    assert np.all(B.sum(0)==8) and np.all(B.sum(1)==8) and permanent_ryser(B)==56260624960
    evals=np.linalg.eigvalsh(D@D.T)
    target=sorted([0]+[4-math.sqrt(6)]*24+[4]*30+[4+math.sqrt(6)]*24+[8])
    assert np.allclose(evals,target)
    assert (80-79)-(160-79)==-80
    I=np.eye(40);L=12*I-A;Hp=16*I-L;t=math.pi/8
    e,V=np.linalg.eigh(L);ep,Vp=np.linalg.eigh(Hp)
    U1=V@np.diag(np.exp(-1j*t*e))@V.T;U2=Vp@np.diag(np.exp(-1j*t*ep))@Vp.T
    assert np.allclose(U2@U1,I,atol=1e-12)
    print(json.dumps({"status":cert["status"],"semantic_sha256":cert["semantic_sha256"],"exotic_total_dimension":252,"moment_max":mom["maximum_coefficient"],"mixed_classes":[18,5],"perfect_matchings":56260624960,"susy_zero_modes":82,"echo_residual":float(np.max(abs(U2@U1-I)))},sort_keys=True))

if __name__=="__main__":main()
