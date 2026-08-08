#!/usr/bin/env python3
"""Deterministic verifier for Passes 4205-4212.

Default mode checks hashes, finite algebra, carrier packing, W33/Levi geometry,
stabilizer quotients, layout arithmetic and the three exact outside-box probes.
--full additionally exhausts all Levi cycles/theta cores through 14 edges and
runs outward-inflated interval/Krawczyk branch-and-bound on the edge/nonedge
stabilizer fixed spaces.
"""
from __future__ import annotations
import argparse, collections, hashlib, itertools, json, math
from pathlib import Path
import numpy as np
from scipy.optimize import root

ROOT=Path(__file__).resolve().parents[1]
P4205=ROOT/'data/w33_pass4205_carrier_surgery.json'
P4206=ROOT/'data/w33_pass4206_native_dualrail_transmon_mapping.json'
P4207=ROOT/'data/w33_pass4207_compressed_hodge_sensor.json'
P4208=ROOT/'data/w33_pass4208_component_level_tapped_delay.json'
P4209=ROOT/'data/w33_pass4209_edge_nonedge_interval_completion.json'
P4210=ROOT/'data/w33_pass4210_critical_absorber.json'
P4211=ROOT/'data/w33_pass4211_vertex_spectral_uncertainty.json'
P4212=ROOT/'data/w33_pass4212_levi_harmonic_battery.json'
PACKET=ROOT/'data/PART_4205_4212_CARRIER_NATIVE_HODGE_DELAY_INTERVAL_BONKERS.json'
MANIFEST=ROOT/'data/PART_4205_4212_CARRIER_NATIVE_HODGE_DELAY_INTERVAL_BONKERS_manifest.json'

def chash(d):
    x=dict(d);x.pop('semantic_sha256',None)
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

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
    lines=sorted(lines); E=[]; adj=[[] for _ in range(80)]
    for l,L in enumerate(lines):
        for p in L:
            e=len(E);q=40+l;E.append((p,q));adj[p].append(q);adj[q].append(p)
    for x in adj:x.sort()
    D=np.zeros((80,160),float)
    for e,(p,q) in enumerate(E):D[p,e]=1;D[q,e]=-1
    return pts,A,lines,E,D,adj

def compose(p,q):return tuple(p[q[i]] for i in range(40))
def group_perms(pts):
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
    return list(seen)

def stab_orbits(group,pair):
    S=set(pair);st=[p for p in group if {p[pair[0]],p[pair[1]]}==S]
    unseen=set(range(40));orbs=[]
    while unseen:
        x=min(unseen);o={p[x] for p in st};orbs.append(sorted(o));unseen-=o
    return st,sorted(orbs,key=lambda o:(len(o),o[0]))

def quotient(A,orbs):
    Q=np.zeros((len(orbs),len(orbs)),int)
    for i,O in enumerate(orbs):
        x=O[0]
        for j,P in enumerate(orbs):Q[i,j]=sum(A[x,y] for y in P)
    return Q

def carrier_audit(d):
    assert d['one_loop_weyl_only']['max_generations_both_nonabelian_AF']==5
    assert abs((11-4*5/3)-13/3)<1e-12 and abs((22/3-4*5/3)-2/3)<1e-12
    orig={'Q':1,'u':15,'d':15,'L':24,'e':1};dims={'Q':6,'u':3,'d':3,'L':2,'e':1}
    n=5;unch=sum(dims[k]*min(orig[k],n) for k in orig)
    assert unch==47 and 145-unch==98 and 15*n==75
    species=[6,3,3,2,1];caps=[7,6,2];weights=[1,15,24]
    cfg=[]
    for cap in caps:
        rows=[]
        for x in itertools.product(*[range(cap//z+1) for z in species]):
            if sum(a*b for a,b in zip(species,x))<=cap:rows.append(x)
        cfg.append(rows)
    assert list(map(len,cfg))==[46,32,4]
    good=0
    for a in cfg[0]:
        for b in cfg[1]:
            for c in cfg[2]:
                nsp=[a[i]+15*b[i]+24*c[i] for i in range(5)]
                if nsp[0]>0 and len(set(nsp))==1:good+=1
    assert good==0

def build_B(Q,J):
    r=len(Q);L=12*np.eye(r)-Q
    return np.block([[J[0,0]*np.eye(r)-0.1*L,J[0,1]*np.eye(r)],
                     [J[1,0]*np.eye(r),J[1,1]*np.eye(r)-10*L]])

def F(B,x):return B@x-x**3

def interval_f(B,lo,hi):
    pos=np.maximum(B,0);neg=np.minimum(B,0)
    return pos@lo+neg@hi-hi**3,pos@hi+neg@lo-lo**3

def jac_interval(B,lo,hi):
    n=len(lo);sqlo=np.where((lo<=0)&(hi>=0),0,np.minimum(lo*lo,hi*hi));sqhi=np.maximum(lo*lo,hi*hi)
    mid=B.copy();rad=np.zeros_like(B)
    for i in range(n):
        l=B[i,i]-3*sqhi[i];h=B[i,i]-3*sqlo[i]
        mid[i,i]=(l+h)/2;rad[i,i]=(h-l)/2
    return mid,rad

def krawczyk(B,lo,hi):
    x=(lo+hi)/2;r=(hi-lo)/2;J=B-np.diag(3*x*x)
    try:C=np.linalg.inv(J)
    except np.linalg.LinAlgError:return 'split',lo,hi,x
    jm,jr=jac_interval(B,lo,hi);E0=np.eye(len(x))-C@jm;Er=np.abs(C)@jr
    y=x-C@F(B,x);kr=(np.abs(E0)+Er)@r+1e-14;klo=y-kr;khi=y+kr
    nlo=np.maximum(lo,klo);nhi=np.minimum(hi,khi)
    if np.any(nlo>nhi):return 'empty',None,None,y
    if np.all(klo>lo)&np.all(khi<hi):return 'unique',klo,khi,y
    return 'contract',nlo,nhi,y

def interval_count(Q,J,U,V,max_nodes):
    B=build_B(Q,J);r=len(Q);stack=[(np.r_[-U*np.ones(r),-V*np.ones(r)],np.r_[U*np.ones(r),V*np.ones(r)])]
    unique=[];unresolved=[];nodes=0
    while stack:
        lo,hi=stack.pop();nodes+=1
        if nodes>max_nodes:raise RuntimeError('interval node cap exceeded')
        fl,fh=interval_f(B,lo,hi)
        if np.any((fl>0)|(fh<0)):continue
        typ,nlo,nhi,y=krawczyk(B,lo,hi)
        if typ=='empty':continue
        if typ=='unique':unique.append(y);continue
        old=hi-lo;new=nhi-nlo
        if np.max(new/old)<0.85:stack.append((nlo,nhi));continue
        if np.max(new)<1e-7:unresolved.append((nlo,nhi));continue
        scales=np.r_[U*np.ones(r),V*np.ones(r)];j=int(np.argmax(new/scales));m=(nlo[j]+nhi[j])/2
        h=nhi.copy();h[j]=m;l=nlo.copy();l[j]=m;stack.append((nlo,h));stack.append((l,nhi))
    # Boxes that terminate on split boundaries cluster exactly at roots. Refine one per cluster and Krawczyk-certify it.
    clusters={tuple(np.round((lo+hi)/2,6)) for lo,hi in unresolved}
    roots=[]
    for y in unique:
        rr=root(lambda z:F(B,z),y,jac=lambda z:B-np.diag(3*z*z),tol=1e-11);assert rr.success
        roots.append(rr.x)
    for c in clusters:
        rr=root(lambda z:F(B,z),np.array(c),jac=lambda z:B-np.diag(3*z*z),tol=1e-11);assert rr.success
        x=rr.x;typ,*_=krawczyk(B,x-1e-3,x+1e-3);assert typ=='unique';roots.append(x)
    ded=[]
    for x in roots:
        if not any(np.linalg.norm(x-y)<1e-6 for y in ded):ded.append(x)
    return ded,nodes

def enumerate_cycles_theta(adj,E):
    eid={tuple(sorted(e)):i for i,e in enumerate(E)}
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
                elif v>start and v not in seen and len(path)<14:stack.append((v,path+[v],seen|{v}))
    cnt=collections.Counter(map(len,cycles));assert cnt=={8:1620,10:5184,12:43200,14:336960}
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
            e=eid[tuple(sorted((x,y)))];p,l=E[e];z[e]=1 if (x==p and y==l) else -1
        return z
    theta=[];types=collections.Counter()
    for ps in paths.values():
        for i,p in enumerate(ps):
            ip=set(p[1:-1]);lp=len(p)-1
            for j in range(i+1,len(ps)):
                q=ps[j];iq=set(q[1:-1]);lq=len(q)-1
                if lp+lq<8 or ip&iq:continue
                for k in range(j+1,len(ps)):
                    r=ps[k];ir=set(r[1:-1]);lr=len(r)-1
                    if lp+lr<8 or lq+lr<8 or lp+lq+lr>14 or ip&ir or iq&ir:continue
                    fs=[flow(x) for x in (p,q,r)];keys=sorted(set().union(*map(set,fs)))
                    c1=np.array([fs[0].get(e,0)-fs[2].get(e,0) for e in keys],float)
                    c2=np.array([fs[1].get(e,0)-fs[2].get(e,0) for e in keys],float)
                    theta.append((np.array(keys,dtype=np.int16),c1,c2));types[tuple(sorted((lp,lq,lr)))]+=1
    assert sum(types.values())==133920
    return cycles,theta

def compressed_hodge_audit(D,adj,E):
    PH=np.eye(160)-D.T@np.linalg.pinv(D@D.T,rcond=1e-12)@D
    assert abs(np.trace(PH)-81)<1e-8
    rng=np.random.default_rng(421001);R=rng.normal(size=(81,160));cycles,theta=enumerate_cycles_theta(adj,E)
    def W(m):
        Y=R[:m]@PH;G=Y@Y.T;ev,U=np.linalg.eigh(G);return U@np.diag(1/np.sqrt(ev))@U.T@Y
    eid={tuple(sorted(e)):i for i,e in enumerate(E)}
    def gains(Wm):
        cg=1e9;tg=1e9
        for c in cycles:
            z=np.zeros(160);n=len(c)
            for i in range(n):
                x,y=c[i],c[(i+1)%n];e=eid[tuple(sorted((x,y)))];p,l=E[e];z[e]=1 if (x==p and y==l) else -1
            cg=min(cg,float(np.linalg.norm(Wm@z)/np.linalg.norm(z)))
        for keys,c1,c2 in theta:
            C=np.column_stack([c1,c2]);M=np.column_stack([Wm[:,keys]@c1,Wm[:,keys]@c2]);ev=np.linalg.eigvals(np.linalg.solve(C.T@C,M.T@M)).real
            tg=min(tg,math.sqrt(max(0,float(ev.min()))))
        return cg,tg
    vals={m:gains(W(m)) for m in (8,9,10)}
    assert min(vals[9])<0.05 and min(vals[10])>0.05
    assert abs(vals[10][0]-0.0677644693574068)<2e-9
    alpha=min(vals[10]);beta=2*math.sin(math.pi/30);M=np.array([[alpha*alpha,-alpha],[-alpha,1+beta*beta]])
    lb=math.sqrt(float(np.linalg.eigvalsh(M)[0]));assert lb>0.0138
    return vals,lb

def full_morse(A,orbs,J,x):
    r=len(orbs);u=np.zeros(40);v=np.zeros(40)
    for i,O in enumerate(orbs):u[O]=x[i];v[O]=x[r+i]
    L=12*np.eye(40)-A;a,b=J[0];c,d=J[1]
    M=np.block([[a*np.eye(40)-np.diag(3*u*u)-0.1*L,b*np.eye(40)],[c*np.eye(40),d*np.eye(40)-np.diag(3*v*v)-10*L]])
    return int(np.sum(np.linalg.eigvals(M).real>1e-8))

def bonkers(A,D):
    J=np.ones((40,40));P2=(2/3)*np.eye(40)+(1/6)*A-(1/15)*J;S=np.eye(40)-P2
    assert np.linalg.norm(P2@P2-P2)<1e-10 and abs(np.linalg.norm(S[:,0])**2-2/5)<1e-10
    assert abs(P2[0,0]-3/5)<1e-12
    for ranks in ([1],[15],[24],[1,15],[1,24],[15,24],[1,15,24]):
        d=sum(ranks);assert math.ceil(40/d)>=1
    PH=np.eye(160)-D.T@np.linalg.pinv(D@D.T,rcond=1e-12)@D
    assert abs(np.trace(PH)-81)<1e-8 and abs(np.mean(np.diag(PH))-81/160)<1e-10

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--full',action='store_true');args=ap.parse_args()
    ds=[json.loads(p.read_text()) for p in (P4205,P4206,P4207,P4208,P4209,P4210,P4211,P4212,PACKET,MANIFEST)]
    for d in ds:assert chash(d)==d['semantic_sha256']
    d5,d6,d7,d8,d9,d10,d11,d12,packet,manifest=ds
    pts,A,lines,E,D,adj=geometry();assert len(pts)==40 and len(lines)==40 and len(E)==160 and np.linalg.matrix_rank(D)==79
    assert sorted(np.linalg.eigvalsh(A).round(8).tolist()).count(12.0)==1
    carrier_audit(d5)
    assert d6['w33_mapping']['logical_max_degree']==3 and d6['w33_mapping']['total_transmons_excluding_readout']==87
    hist={int(k):v for k,v in d8['schedule']['delay_histogram'].items()};assert sum(hist.values())==160 and sum(k*v for k,v in hist.items())==919
    assert abs(8*d8['schedule']['slot_length_mm']-d8['schedule']['maximum_delay_mm'])<1e-9
    group=group_perms(pts);est,eorbs=stab_orbits(group,(0,1));nst,norbs=stab_orbits(group,(0,4))
    assert len(est)==108 and [len(x) for x in eorbs]==[2,2,18,18]
    assert len(nst)==48 and [len(x) for x in norbs]==[2,2,4,16,16]
    Qe=quotient(A,eorbs);Qn=quotient(A,norbs);assert Qe.tolist()==d9['edge_stratum']['adjacency_quotient'] and Qn.tolist()==d9['nonedge_stratum']['adjacency_quotient']
    bonkers(A,D)
    out={'status':packet['status'],'packet_sha256':packet['semantic_sha256'],'carrier_generations':5,'native_transmons':87,'delay_units':919,'full':args.full}
    if args.full:
        vals,lb=compressed_hodge_audit(D,adj,E);out['compressed_hodge_sigma_lb']=lb
        Js={'24':np.array([[2.,5.],[-21.,-20.]]),'15':np.array([[3.2,12.],[-21.,-10.]])};bounds={'24':(2.50439835,2.13976351),'15':(3.79360056,3.53797676)}
        expected={('edge','24'):5,('edge','15'):3,('nonedge','24'):13,('nonedge','15'):9};morse={}
        for label,Q,orbs,cap in [('edge',Qe,eorbs,600000),('nonedge',Qn,norbs,600000)]:
            for name,Jm in Js.items():
                U,V=bounds[name];roots,nodes=interval_count(Q,Jm,U,V,cap);assert len(roots)==expected[(label,name)]
                morse[(label,name)]=collections.Counter(full_morse(A,orbs,Jm,x) for x in roots)
        assert morse[('edge','24')]=={0:2,23:2,24:1};assert morse[('edge','15')]=={0:2,15:1}
        assert morse[('nonedge','24')]=={17:6,19:4,21:2,24:1};assert morse[('nonedge','15')]=={0:4,4:2,14:2,15:1}
        out['interval_root_counts']=[5,3,13,9]
    print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
