#!/usr/bin/env python3
"""Deterministic verifier for Passes 4269-4276.

Quick mode:
  * reconstructs W(3,3) and PSp(4,3);
  * identifies the order-72 anchor stabilizer and its C3 x SL(2,3) structure;
  * recomputes the V15/V24/H145 branching through the class algebra;
  * verifies the species-wise H-equivariant 75-state charge partition and
    the identical-generation factorization obstruction;
  * verifies the explicit GHZ28 fusion recurrence;
  * regenerates the frozen signed-16 two-row decoder candidate;
  * checks the corrected GDS geometry arithmetic;
  * classifies three- and four-subset orbits;
  * verifies graph-state, transport-curvature, and Hodge-FDT identities.

--full additionally re-enumerates every Levi cycle/theta core through support 14,
audits the signed-16 modular pair exactly, replays the deterministic triple-root
censuses, and exhausts graph-state cuts through five qubits / weight-six stabilizers.
"""
from __future__ import annotations
import argparse, collections, hashlib, itertools, json, math
from pathlib import Path
import numpy as np
from scipy.optimize import linear_sum_assignment, root

ROOT=Path(__file__).resolve().parents[1]
NAMES={
4269:'h145_order72_branching',
4270:'explicit_ghz28_heralded_fusion',
4271:'signed16_two_row_hodge_optimization',
4272:'gds_oriented_delay_compiler',
4273:'triple_strata_and_rank4_boundary',
4274:'graph_state_five_uniformity',
4275:'ollivier_transport_curvature',
4276:'hodge_sector_fluctuation_dissipation',
}
P={n:ROOT/'data'/f'w33_pass{n}_{NAMES[n]}.json' for n in NAMES}
PACKET=ROOT/'data/PART_4269_4276_H145_FUSION_HODGE_GDS_STRATA_OUTSIDE_BOX.json'
MANIFEST=ROOT/'data/PART_4269_4276_H145_FUSION_HODGE_GDS_STRATA_OUTSIDE_BOX_manifest.json'

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
    A=np.zeros((40,40),dtype=int)
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
    lines=sorted(lines);E=[];adj=[[] for _ in range(80)]
    for l,L in enumerate(lines):
        for p in L:
            q=40+l;E.append((p,q));adj[p].append(q);adj[q].append(p)
    for x in adj:x.sort()
    D=np.zeros((80,160),dtype=int)
    for e,(p,q) in enumerate(E):D[p,e]=1;D[q,e]=-1
    return pts,A,lines,E,adj,D

def compose(p,q):return tuple(p[q[i]] for i in range(40))
def invperm(p):
    q=[0]*40
    for i,j in enumerate(p):q[j]=i
    return tuple(q)
def order(p):
    q=tuple(range(40))
    for n in range(1,100):
        q=compose(p,q)
        if q==tuple(range(40)):return n
    raise RuntimeError('order cap')
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
    return gs,sorted(seen)

def subgroup_generated(gs):
    ident=tuple(range(40));seen={ident};stack=[ident]
    gg=list(gs)+[invperm(g) for g in gs]
    while stack:
        x=stack.pop()
        for g in gg:
            y=compose(g,x)
            if y not in seen:seen.add(y);stack.append(y)
    return sorted(seen)

def order72_branching(A,G,ledger):
    S={0,1,4,5,6};H=[p for p in G if {p[x] for x in S}==S]
    assert len(H)==72
    center=[g for g in H if all(compose(g,h)==compose(h,g) for h in H)]
    assert len(center)==6 and collections.Counter(order(g) for g in center)=={1:1,2:1,3:2,6:2}
    comm=[]
    for a in H:
        ia=invperm(a)
        for b in H:
            ib=invperm(b);comm.append(compose(compose(compose(a,b),ia),ib))
    der=subgroup_generated(comm)
    assert len(der)==8 and collections.Counter(order(g) for g in der)=={1:1,2:1,4:6}
    z3=sorted(g for g in center if order(g) in (1,3))
    z=next(g for g in z3 if order(g)==3)
    t=K=None
    for g in sorted(H):
        if order(g)==3 and g not in center:
            cand=subgroup_generated(der+[g])
            if len(cand)==24 and len(set(cand)&set(z3))==1:
                t=g;K=cand;break
    assert K is not None and len({compose(a,b) for a in z3 for b in K})==72
    z2=next(g for g in center if order(g)==2)

    unseen=set(H);classes=[]
    while unseen:
        g=min(unseen)
        cl={compose(compose(h,g),invperm(h)) for h in H}
        classes.append(sorted(cl));unseen-=cl
    assert len(classes)==21
    cmap={g:i for i,cl in enumerate(classes) for g in cl}
    sizes=np.array([len(cl) for cl in classes],float)
    Ms=[]
    for Cla in classes:
        M=np.zeros((21,21),float)
        for b,Clb in enumerate(classes):
            cnt=np.zeros(21,dtype=int)
            for x in Cla:
                for y in Clb:cnt[cmap[compose(x,y)]]+=1
            for c in range(21):
                if cnt[c]:
                    assert cnt[c]%len(classes[c])==0
                    M[c,b]=cnt[c]//len(classes[c])
        Ms.append(M)
    rng=np.random.default_rng(4269)
    coeff=rng.normal(size=21)+1j*rng.normal(size=21)
    ew,V=np.linalg.eig(sum(coeff[i]*Ms[i] for i in range(21)))
    irreps=[]
    for k in range(21):
        v=V[:,k]
        lam=np.array([np.vdot(v,M@v)/np.vdot(v,v) for M in Ms])
        d=round(math.sqrt(72/sum(abs(lam[a])**2/sizes[a] for a in range(21))))
        ch=np.array([d*lam[a]/sizes[a] for a in range(21)])
        irreps.append((d,ch))
    omega=np.exp(2j*np.pi/3)
    def nexp(x):return min(range(3),key=lambda a:abs(x-omega**a))
    cz,ct,c2=cmap[z],cmap[t],cmap[z2]
    labels=[]
    for d,ch in irreps:
        a=nexp(ch[cz]/d)
        if d==1:lab=f'chi_{a}{nexp(ch[ct])}'
        elif d==2:lab=f'sigma_{a}{nexp(-ch[ct])}'
        else:lab=f'tau_{a}'
        labels.append(lab)
    assert len(set(labels))==21
    chi15=[];chi24=[]
    for cl in classes:
        g=cl[0];fix=sum(g[i]==i for i in range(40));am=sum(A[i,g[i]] for i in range(40))
        chi15.append(fix/3-am/6+5/3)
        chi24.append(2*fix/3+am/6-8/3)
    def dec(target):
        out={}
        for lab,(d,ch) in zip(labels,irreps):
            m=sum(sizes[a]*np.conj(ch[a])*target[a] for a in range(21))/72
            mm=int(round(m.real))
            assert abs(m-mm)<1e-7
            if mm:out[lab]=mm
        return out
    d15,d24=dec(chi15),dec(chi24)
    assert d15==ledger['branching']['V15'] and d24==ledger['branching']['V24']
    H145=collections.Counter({'chi_00':7})
    for k,v in d15.items():H145[k]+=6*v
    for k,v in d24.items():H145[k]+=2*v
    assert dict(H145)==ledger['branching']['H145']
    dims={lab:(1 if lab.startswith('chi') else 2 if lab.startswith('sigma') else 3) for lab in H145}
    assert sum(dims[k]*v for k,v in H145.items())==145
    used=collections.Counter()
    total=0
    for key,block in ledger['species_wise_H_equivariant_five_generation_partition'].items():
        if not key.endswith(('dim30','dim15','dim10','dim5')):continue
        d=0
        for ir,m in block.items():used[ir]+=m;d+=dims[ir]*m
        total+=d
    assert total==75 and all(used[k]<=H145[k] for k in used)
    assert max(H145.values())==23 and sum(dims[k] for k,v in H145.items() if v>=15)==1
    return H145

def ghz_audit(d):
    s=1-d['source_operating_point']['dualrail_CNOT_erasure_rate']
    F=d['source_operating_point']['dualrail_CNOT_process_fidelity']
    N=28;E=[0.0]*(N+1);gates=[0]*(N+1);split=[None]*(N+1)
    for n in range(2,N+1):
        best=((n-1)/(s**(n-1)),n-1,None)
        for a in range(1,n):
            val=(E[a]+E[n-a]+2)/(s*s);gg=gates[a]+gates[n-a]+2
            if val<best[0]-1e-12 or (abs(val-best[0])<1e-12 and gg<best[1]):best=(val,gg,(a,n-a))
        E[n],gates[n],split[n]=best
    q=d['optimized_conservative_protocol']
    assert abs(E[28]-q['expected_CNOT_attempts_with_local_rebuild'])<1e-10
    assert gates[28]==33 and split[28]==(12,16)
    assert abs(F**33-q['conditional_independent_process_factor'])<1e-12

def regen_rows(d):
    p=d['search']['prime'];rng=np.random.default_rng(d['search']['seed'])
    chosen=None
    for it in range(d['search']['selected_zero_based_candidate']+1):
        a=rng.integers(0,p,size=160,dtype=np.int64)
        b=rng.integers(0,p,size=160,dtype=np.int64)
        a=((a+p//2)%p)-p//2;b=((b+p//2)%p)-p//2
        if it==d['search']['selected_zero_based_candidate']:chosen=(a,b)
    a,b=chosen
    sha=hashlib.sha256(np.stack([a,b]).astype('<i4').tobytes()).hexdigest()
    assert sha==d['search']['row_pair_int32_sha256']
    assert max(abs(a).max(),abs(b).max())<32768
    return a,b

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
                elif v>start and v not in seen and len(path)<14:
                    stack.append((v,path+[v],seen|{v}))
    assert collections.Counter(map(len,cycles))=={8:1620,10:5184,12:43200,14:336960}
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
    return cycles,theta,eid

def hodge_full(d,adj,E,w1,w2):
    cycles,theta,eid=enumerate_cycles_theta(adj,E);p=d['search']['prime']
    minc=1e99;mint=1e99;mindet=10**100
    s1=max(abs(w1));s2=max(abs(w2))
    for c in cycles:
        z=np.zeros(160);n=len(c)
        for i in range(n):
            x,y=c[i],c[(i+1)%n];e=eid[tuple(sorted((x,y)))];pt,ln=E[e]
            z[e]=1 if (x==pt and y==ln) else -1
        a=int(round(w1@z));b=int(round(w2@z))
        assert (a%p) or (b%p)
        minc=min(minc,math.hypot(a/s1,b/s2)/np.linalg.norm(z))
    for keys,c1,c2 in theta:
        a1=float(w1[keys]@c1);a2=float(w1[keys]@c2)
        b1=float(w2[keys]@c1);b2=float(w2[keys]@c2)
        det=int(round(a1*b2-a2*b1));assert det%p
        mindet=min(mindet,abs(det))
        C=np.column_stack([c1,c2]);M=np.array([[a1/s1,a2/s1],[b1/s2,b2/s2]])
        ev=np.linalg.eigvals(np.linalg.solve(C.T@C,M.T@M)).real
        mint=min(mint,math.sqrt(max(0,float(ev.min()))))
    assert abs(minc-d['selected_pair']['minimum_cycle_gain_after_per_row_maxabs_normalization'])<2e-12
    assert abs(mint-d['selected_pair']['minimum_theta_generalized_singular_after_per_row_maxabs_normalization'])<2e-12
    assert mindet==d['selected_pair']['minimum_absolute_theta_determinant']

def mask(c):
    m=0
    for i in c:m|=1<<i
    return m
def pmask(m,p):
    out=0
    for i in range(40):
        if (m>>i)&1:out|=1<<p[i]
    return out
def subset_orbits(k,gens,A):
    universe={mask(c) for c in itertools.combinations(range(40),k)};out=[]
    while universe:
        rep=min(universe);orb={rep};stack=[rep]
        while stack:
            m=stack.pop()
            for g in gens:
                z=pmask(m,g)
                if z not in orb:orb.add(z);stack.append(z)
        universe.difference_update(orb)
        S=[i for i in range(40) if (rep>>i)&1]
        edges=int(A[np.ix_(S,S)].sum()//2);degs=sorted(A[np.ix_(S,S)].sum(1).tolist(),reverse=True)
        out.append((len(orb),25920//len(orb),edges,degs,S))
    return out
def stabilizer(G,S):
    SS=set(S);return [p for p in G if {p[x] for x in S}==SS]
def orbits(st):
    unseen=set(range(40));res=[]
    while unseen:
        x=min(unseen);o={p[x] for p in st};res.append(sorted(o));unseen-=o
    return sorted(res,key=lambda z:(len(z),z[0]))
def quotient(A,oo):
    Q=np.zeros((len(oo),len(oo)),int)
    for i,O in enumerate(oo):
        x=O[0]
        for j,P in enumerate(oo):Q[i,j]=sum(A[x,y] for y in P)
    return Q
def build_B(Q,J):
    r=len(Q);L=12*np.eye(r)-Q
    return np.block([[J[0,0]*np.eye(r)-.1*L,J[0,1]*np.eye(r)],[J[1,0]*np.eye(r),J[1,1]*np.eye(r)-10*L]])
def census(Q,J,U,V,nseed,seed):
    B=build_B(Q,J);r=len(Q);rng=np.random.default_rng(seed);roots=[]
    for _ in range(nseed):
        x0=np.r_[rng.uniform(-U,U,r),rng.uniform(-V,V,r)]
        rr=root(lambda z:B@z-z**3,x0,jac=lambda z:B-np.diag(3*z*z),method='lm',options={'maxiter':300})
        if np.linalg.norm(B@rr.x-rr.x**3)<1e-8 and not any(np.linalg.norm(rr.x-y)<1e-5 for y in roots):roots.append(rr.x)
    return roots

def graphstate(A,full):
    rows=[]
    for i in range(40):
        b=0
        for j in range(40):
            if A[i,j]&1:b|=1<<j
        rows.append(b)
    def r2(M):
        M=(np.array(M,dtype=np.uint8)&1).copy();r=0
        for c in range(M.shape[1]):
            piv=next((i for i in range(r,M.shape[0]) if M[i,c]),None)
            if piv is None:continue
            M[[r,piv]]=M[[piv,r]]
            for i in range(M.shape[0]):
                if i!=r and M[i,c]:M[i]^=M[r]
            r+=1
            if r==M.shape[0]:break
        return r
    assert r2(A)==16
    if full:
        for k in range(1,6):
            for S in itertools.combinations(range(40),k):
                T=[x for x in range(40) if x not in set(S)]
                assert r2(A[np.ix_(S,T)])==k
        cnt=0
        for S in itertools.combinations(range(40),6):
            xm=sum(1<<i for i in S);ax=0
            for i in S:ax^=rows[i]
            if (xm|ax).bit_count()==6:
                assert ax==0;cnt+=1
        assert cnt==240
    else:
        S=(0,1,2,22,27,29);ax=0
        for i in S:ax^=rows[i]
        assert ax==0

def distances(adj):
    n=len(adj);D=np.full((n,n),99,int)
    for s in range(n):
        D[s,s]=0;q=[s]
        for u in q:
            for v in adj[u]:
                if D[s,v]>D[s,u]+1:D[s,v]=D[s,u]+1;q.append(v)
    return D
def curvature(adj,D):
    out=collections.Counter()
    for x in range(len(adj)):
        for y in range(x+1,len(adj)):
            C=np.array([[D[a,b] for b in adj[y]] for a in adj[x]],int)
            rr,cc=linear_sum_assignment(C);W=int(C[rr,cc].sum())/len(adj[x]);d=D[x,y]
            out[(int(d),round(1-W/d,12),round(W,12))]+=1
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--full',action='store_true',help='exhaust cycles/thetas and graph-state cuts')
    ap.add_argument('--replay-strata',action='store_true',help='heavy deterministic 120k-start nonlinear census replay')
    args=ap.parse_args()
    data={n:json.loads(P[n].read_text()) for n in P};packet=json.loads(PACKET.read_text());manifest=json.loads(MANIFEST.read_text())
    for d in list(data.values())+[packet,manifest]:assert chash(d)==d['semantic_sha256']
    pts,A,lines,E,adj,D=geometry();assert len(lines)==40 and len(E)==160 and np.linalg.matrix_rank(D)==79
    gens,G=group_perms(pts);order72_branching(A,G,data[4269]);ghz_audit(data[4270]);w1,w2=regen_rows(data[4271])
    g=data[4272];r=g['corrected_cell']['bend_radius_mm'];v=g['corrected_cell']['vertical_straight_leg_mm'];q=g['corrected_cell']['top_straight_mm'];xp=g['corrected_cell']['x_pitch_mm']
    assert abs(xp-(4*r+q))<1e-15 and abs(2*v+(2*math.pi-4)*r-g['corrected_cell']['slot_excess_path_mm'])<1e-12
    assert g['open_drc_contract']['minimum_edge_to_edge_lane_gap_um']>31
    o3=subset_orbits(3,gens,A);o4=subset_orbits(4,gens,A)
    assert len(o3)==5 and len(o4)==16 and sum(x[0] for x in o4)==math.comb(40,4) and any(x[1]==1 for x in o4)
    graphstate(A,args.full)
    adjW=[list(np.flatnonzero(A[i])) for i in range(40)]
    DW=np.where(A,1,2);np.fill_diagonal(DW,0)
    cw=curvature(adjW,DW);cl=curvature(adj,distances(adj))
    assert cw[(1,round(1/6,12),round(5/6,12))]==240 and cw[(2,round(2/3,12),round(2/3,12))]==540
    assert cl[(1,-1.0,2.0)]==160 and cl[(4,0.5,2.0)]==1080
    fdt=data[4276];assert fdt['edge_space']['harmonic_dimension']==81 and fdt['edge_space']['gradient_dimension']==79
    assert abs(fdt['example']['integrated_response_trace']-(81+79/4))<1e-12
    if args.full:
        hodge_full(data[4271],adj,E,w1,w2)
    if args.replay_strata:
        byord={x[1]:x for x in o3};Js={'24':np.array([[2.,5.],[-21.,-20.]]),'15':np.array([[3.2,12.],[-21.,-10.]])};bounds={'24':(2.50439835,2.13976351),'15':(3.79360056,3.53797676)}
        spec=[(12,'24',20000,4269124,57),(12,'15',20000,4269115,27),(9,'24',20000,4269924,57),(9,'15',20000,4269915,27),(6,'24',20000,4269624,2376),(6,'15',20000,4269616,246)]
        for ordv,sel,nseed,seed,expected in spec:
            S=byord[ordv][4];Q=quotient(A,orbits(stabilizer(G,S)));U,V=bounds[sel]
            roots=census(Q,Js[sel],U,V,nseed,seed)
            assert len(roots)==expected
    print(json.dumps({'status':packet['status'],'packet_sha256':packet['semantic_sha256'],'manifest_sha256':manifest['semantic_sha256'],'H_order':72,'GHZ_CNOTs':33,'signed16_rows':2,'GDS_bbox_mm':data[4272]['banking']['overall_bbox_mm'],'three_subset_orbits':5,'four_subset_orbits':16,'graphstate_uniformity':5,'full':args.full,'replay_strata':args.replay_strata},sort_keys=True))
if __name__=='__main__':main()
