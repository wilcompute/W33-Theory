#!/usr/bin/env python3
from __future__ import annotations
import collections, hashlib, itertools, json, math
from itertools import combinations, product
from pathlib import Path
import numpy as np
from scipy.optimize import brentq, root, milp, LinearConstraint, Bounds
from scipy.integrate import quad

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/PART_4213_4220_SMALL_COVER_SU4_QUANTUM_HYSTERESIS_CLOCK_HAWKING_PELL_VACUUM_VELOCITY.json"

def semantic_hash(c):
    x=dict(c);x.pop("semantic_sha256",None)
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def norm_proj(v):
    v=tuple(x%3 for x in v); first=next(x for x in v if x); inv=1 if first==1 else 2
    return tuple((inv*x)%3 for x in v)
def symp(x,y): return (x[0]*y[1]-x[1]*y[0]+x[2]*y[3]-x[3]*y[2])%3
def build_levi():
    pts=sorted({norm_proj(v) for v in product(range(3),repeat=4) if any(v)})
    pi={p:i for i,p in enumerate(pts)}; lines=set()
    for i,j in combinations(range(40),2):
        x,y=pts[i],pts[j]
        if symp(x,y): continue
        lines.add(frozenset(pi[norm_proj(tuple((a*x[k]+b*y[k])%3 for k in range(4)))] for a,b in product(range(3),repeat=2) if a or b))
    lines=sorted(lines,key=lambda z:tuple(sorted(z))); edges=[]
    for li,line in enumerate(lines):
        for p in line: edges.append((p,40+li))
    adj=[set() for _ in range(80)]
    for u,v in edges: adj[u].add(v);adj[v].add(u)
    return pts,lines,edges,adj

def cycles_len(adj,L):
    C=[]
    for s in range(len(adj)):
        path=[s]; vis={s}
        def dfs(u):
            if len(path)==L:
                if s in adj[u] and path[1]<path[-1]: C.append(tuple(path))
                return
            for v in adj[u]:
                if v<=s or v in vis: continue
                vis.add(v);path.append(v);dfs(v);path.pop();vis.remove(v)
        for v in sorted(adj[s]):
            if v<=s: continue
            vis.add(v);path.append(v);dfs(v);path.pop();vis.remove(v)
    return C

def cover_check(C):
    pts,lines,edges,adj=build_levi(); assert len(pts)==40 and len(lines)==40 and len(edges)==160 and {len(x) for x in adj}=={4}
    ei={tuple(sorted(e)):i for i,e in enumerate(edges)}
    parent=[-1]*80;parent[0]=0;q=collections.deque([0]);tree=set()
    while q:
        u=q.popleft()
        for v in sorted(adj[u]):
            if parent[v]<0: parent[v]=u;tree.add(ei[tuple(sorted((u,v)))]);q.append(v)
    cotree=[i for i in range(160) if i not in tree]; assert len(cotree)==81
    x=np.array(C["pass4213_small_high_girth_cover"]["cotree_voltage_vector"],dtype=int);cv={e:j for j,e in enumerate(cotree)};p=359
    counts={}
    for L in (8,10,12):
        cycles=cycles_len(adj,L);counts[str(L)]=len(cycles)
        for cyc in cycles:
            s=0
            for k in range(L):
                u,v=cyc[k],cyc[(k+1)%L];e=ei[tuple(sorted((u,v)))]
                if e in cv:s+=(1 if (u<40 and v>=40) else -1)*int(x[cv[e]])
            assert s%p!=0
    assert counts=={"8":1620,"10":5184,"12":43200}
    full=[0]*160
    for e,j in cv.items():full[e]=int(x[j])
    h=hashlib.sha256((",".join(map(str,full))).encode()).hexdigest();assert h==C["pass4213_small_high_girth_cover"]["full_voltage_vector_sha256"]

I2=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex)
def herm_basis(ms,tol=1e-10):
    out=[]
    for M in ms:
        V=np.stack([np.r_[A.real.ravel(),A.imag.ravel()] for A in out+[M]])
        if np.linalg.matrix_rank(V,tol)>len(out):out.append(M)
    return out
def su4_check(C):
    CZ=np.diag([1,1,1,-1]).astype(complex);local=[np.kron(P,I2) for P in (X,Y,Z)]+[np.kron(I2,P) for P in (X,Y,Z)]
    B=herm_basis(local+[CZ@G@CZ for G in local])
    while len(B)<15:
        old=list(B);changed=False
        for A in old:
            for D in old:
                K=(A@D-D@A)/(2j)
                if np.linalg.norm(K)<1e-12:continue
                NB=herm_basis(B+[K])
                if len(NB)>len(B):B=NB;changed=True
                if len(B)==15:break
            if len(B)==15:break
        assert changed
    plus=np.array([1,1],complex)/math.sqrt(2);a,b,c,d=CZ@np.kron(plus,plus);conc=2*abs(a*d-b*c);assert len(B)==15 and abs(conc-1)<1e-12

LN80=math.log(80);H=.004
def nb(s):return 1/(math.exp(2*math.exp(-s))-1)
def F(s,g):
    n=nb(s);return LN80-4*s+g*n-H*n*n
def roots(g):
    xs=np.linspace(.2,8,6000);vals=[F(float(s),g) for s in xs];rr=[]
    for i in range(len(xs)-1):
        if vals[i]*vals[i+1]<0:rr.append(brentq(lambda z:F(z,g),xs[i],xs[i+1]))
    return rr
def Udiff(a,b,g):return -quad(lambda s:F(s,g),a,b,epsabs=1e-11,limit=200)[0]
def hyst_check(C):
    def eq(g):
        r=roots(g);assert len(r)==3;return Udiff(r[0],r[2],g)
    gc=brentq(eq,.5,.6);r=roots(gc);a,b,c=r;barrier=Udiff(a,b,gc);S=quad(lambda s:math.sqrt(max(0,2*Udiff(a,s,gc))),a,c,epsabs=1e-9,limit=300)[0]
    p=C["pass4215_quantized_hysteresis_memory"];assert abs(gc-p["classical_coexistence_g"])<2e-10
    assert max(abs(r[i]-[p["stationary_points"]["left"],p["stationary_points"]["barrier"],p["stationary_points"]["right"]][i]) for i in range(3))<2e-9
    assert abs(barrier-p["equal_barrier_height"])<2e-9 and abs(S-p["semiclassical_zero_energy_instanton_action_for_M1"])<2e-8

def clock_problem():
    codes=[t^(t>>1) for t in range(25)];conds=[]
    for t in range(24):
        a,b=codes[t],codes[t+1];flip=(a^b).bit_length()-1;conds.append(tuple((bit,(a>>bit)&1) for bit in range(5) if bit!=flip))
    def options(L):
        a,b,c,d=L;return [((a,b),(c,d)),((a,c),(b,d)),((a,d),(b,c))]
    O=[options(c) for c in conds];pairs=sorted({tuple(sorted(pair)) for oo in O for op in oo for pair in op});pi={p:i for i,p in enumerate(pairs)};ny=len(pairs);n=ny+72
    obj=np.zeros(n);obj[:ny]=1;A=[];lo=[];hi=[]
    for t in range(24):
        row=np.zeros(n);row[ny+3*t:ny+3*t+3]=1;A.append(row);lo.append(1);hi.append(1)
    for t in range(24):
        for o,op in enumerate(O[t]):
            for pair in op:
                row=np.zeros(n);row[ny+3*t+o]=1;row[pi[tuple(sorted(pair))]]=-1;A.append(row);lo.append(-np.inf);hi.append(0)
    R=milp(obj,integrality=np.ones(n),bounds=Bounds(np.zeros(n),np.ones(n)),constraints=LinearConstraint(np.array(A),np.array(lo),np.array(hi)));return conds,pairs,R
def clock_check(C):
    conds,pairs,R=clock_problem();assert R.success and abs(R.fun-13)<1e-9;p=C["pass4216_compressed_exact_3local_clock"];assert p["optimal_shared_pair_ancillas"]==13 and p["new_auxiliary_ancillas"]==61 and len(set(conds))==24

RB=np.array([.00979708977002,.0203649786239,.0410938074485,.0738588749836,.0950655772517,.0738588749836,.0410938074485,.0203649786239,.00979708977002]);GB=np.array([.931739737612,.916053718604,.87648655463,.805844961224,.76,.805844961224,.87648655463,.916053718604,.931739737612])
def squeezer(n,i,j,r):
    S=np.eye(2*n,dtype=complex);c=math.cosh(r);s=math.sinh(r)
    for row in (i,j,n+i,n+j):S[row,:]=0
    S[i,i]=c;S[i,n+j]=s;S[j,j]=c;S[j,n+i]=s;S[n+i,n+i]=c;S[n+i,j]=s;S[n+j,n+j]=c;S[n+j,i]=s;return S
def beamsplitter(n,i,j,g):
    S=np.eye(2*n,dtype=complex);t=math.sqrt(g);q=math.sqrt(1-g)
    for row in (i,j,n+i,n+j):S[row,:]=0
    S[i,i]=t;S[i,j]=q;S[j,i]=-q;S[j,j]=t;S[n+i,n+i]=t;S[n+i,n+j]=q;S[n+j,n+i]=-q;S[n+j,n+j]=t;return S
def chain(rv=RB,gv=GB):
    S=np.eye(38,dtype=complex)
    for j,(r,g) in enumerate(zip(rv,gv)):S=beamsplitter(19,0,10+j,g)@squeezer(19,0,1+j,r)@S
    return S
def qsymp(S):
    K=np.zeros((38,38),complex)
    for i in range(19):K[i,2*i]=K[19+i,2*i]=1/math.sqrt(2);K[i,2*i+1]=1j/math.sqrt(2);K[19+i,2*i+1]=-1j/math.sqrt(2)
    return np.real_if_close(np.linalg.inv(K)@S@K,tol=1e5).real
def cov(S,n=.0):Q=qsymp(S);return (n+.5)*Q@Q.T
def seigs(V):
    m=len(V)//2;O=np.kron(np.eye(m),np.array([[0.,1.],[-1.,0.]]));return np.sort(np.abs(np.linalg.eigvals(1j*O@V)))[::2].real
def red(V,modes):
    ii=[x for m in modes for x in (2*m,2*m+1)];return V[np.ix_(ii,ii)]
def steer(V,A,B):
    ia=[x for m in A for x in (2*m,2*m+1)];ib=[x for m in B for x in (2*m,2*m+1)];AA=V[np.ix_(ia,ia)];BB=V[np.ix_(ib,ib)];CC=V[np.ix_(ia,ib)];nu=seigs(BB-CC.T@np.linalg.inv(AA)@CC);return sum(max(0,-math.log(2*x)) for x in nu),nu
def entropy(V):
    s=0
    for nu in seigs(V):
        nu=max(.5,float(nu));a=nu+.5;b=nu-.5;s+=a*math.log(a)-(b*math.log(b) if b>1e-14 else 0)
    return s
def hawk_metrics(n=.0,rv=RB,gv=GB):
    V=cov(chain(rv,gv),n);A=[0];B=list(range(1,10));W=red(V,A+B);PT=np.eye(20);PT[1,1]=-1;nupt=seigs(PT@W@PT);LN=sum(max(0,-math.log(2*x)) for x in nupt);ga,nua=steer(V,A,B);gb,nub=steer(V,B,A);SA,SB,SAB=entropy(red(V,A)),entropy(red(V,B)),entropy(W);return LN,ga,gb,SB-SAB,SA-SAB,float(nupt[0]),float(nua.min()),float(nub.min())
def sigmoid(x):return 1/(1+np.exp(-x))
def logit(x):return np.log(x/(1-x))
def hawking_check(C):
    p=C["pass4217_full_19mode_hawking_channel"];m=hawk_metrics(0);vals=[p["baseline"]["logarithmic_negativity"],p["baseline"]["steering_outside_to_partners"],p["baseline"]["steering_partners_to_outside"],p["baseline"]["coherent_information_outside_to_partners_nats"],p["baseline"]["coherent_information_partners_to_outside_nats"]];assert max(abs(m[i]-vals[i]) for i in range(5))<2e-10
    rootspec=[brentq(lambda n:hawk_metrics(n)[6]-.5,.002,.006),brentq(lambda n:hawk_metrics(n)[3],.005,.01),brentq(lambda n:hawk_metrics(n)[7]-.5,.01,.02),brentq(lambda n:hawk_metrics(n)[5]-.5,.1,.13)];exp=[p["uniform_thermal_thresholds"]["outside_to_partners_steering"],p["uniform_thermal_thresholds"]["outside_to_partners_coherent_information"],p["uniform_thermal_thresholds"]["partners_to_outside_steering"],p["uniform_thermal_thresholds"]["entanglement_PPT"]];assert max(abs(a-b) for a,b in zip(rootspec,exp))<2e-9
    rng=np.random.default_rng(20260807);ii=np.arange(9);C0=np.exp(-np.abs(ii[:,None]-ii[None,:])/2);L=np.linalg.cholesky(C0);counts=np.zeros(4,int)
    for _ in range(512):
        x=L@rng.standard_normal(9);rv=RB*np.exp(.35*x);gv=sigmoid(logit(GB)+.25*x);z=hawk_metrics(.005,rv,gv);counts+=np.array([z[0]>1e-12,z[1]>1e-12,z[2]>1e-12,z[3]>1e-12])
    assert counts.tolist()==[512,228,482,415]

def pell_check(C):
    p=C["pass4218_pell_echo"];m=p["example_m"];x=p["example_x"];assert x*x-6*m*m==-6;delta=math.pi/2*(m*math.sqrt(6)-x);err=2*abs(math.sin(delta/2));assert abs(err-p["operator_norm_recurrence_error"])<1e-14
def vac_check(C):
    def nu(sig):return .25*math.sqrt(2+10/math.sqrt(25-sig*sig))
    def g(v):
        a=v+.5;b=v-.5;return a*math.log(a)-(b*math.log(b) if b>1e-14 else 0)
    n4,n6=nu(4),nu(math.sqrt(6));S=g(n4)+24*g(n6);LN=math.acosh(2*n4)+24*math.acosh(2*n6);p=C["pass4219_levi_vacuum_entanglement"];assert abs(S-p["point_line_von_neumann_entropy_nats"])<1e-12 and abs(LN-p["point_line_logarithmic_negativity_nats"])<1e-12
def velocity_check(C):
    p=C["pass4220_high_girth_information_velocity"];assert abs(p["maximum_radial_group_velocity_over_J"]-2*math.sqrt(3))<1e-15 and abs(p["earliest_ball_boundary_time_over_invJ"]-math.sqrt(3))<1e-15

def verify():
    C=json.loads(OUT.read_text());assert semantic_hash(C)==C["semantic_sha256"] and C["all_checks_hold"];cover_check(C);su4_check(C);hyst_check(C);clock_check(C);hawking_check(C);pell_check(C);vac_check(C);velocity_check(C);print("PASS_4213_4220",C["semantic_sha256"]);return True
if __name__=="__main__":verify()
