#!/usr/bin/env python3
from __future__ import annotations
import collections, hashlib, json, math
from itertools import product, combinations
from pathlib import Path
import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.linalg import eigh_tridiagonal

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_4253_4260_GIRTH16_FAULTAWARE_SU4_HYSTERESIS_CLOCK_CHANNEL_SCRAMBLING_MODULAR_CAPACITY.json'
C=json.loads(OUT.read_text())

def semantic_hash(c):
    x=dict(c); x.pop('semantic_sha256',None)
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

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
        line=frozenset(pi[norm_proj(tuple((a*x[k]+b*y[k])%3 for k in range(4)))] for a,b in product(range(3),repeat=2) if a or b)
        lines.add(line)
    lines=sorted(lines,key=lambda z:tuple(sorted(z)))
    edges=[(p,40+li) for li,line in enumerate(lines) for p in sorted(line)]
    adj=[[] for _ in range(80)]
    for u,v in edges: adj[u].append(v);adj[v].append(u)
    for a in adj:a.sort()
    return edges,adj

def simple_cycles_L(adj,L):
    cycles=[]
    for s in range(len(adj)):
        for first in adj[s]:
            if first<=s: continue
            stack=[(first,[s,first],{s,first})]
            while stack:
                u,path,seen=stack.pop()
                if len(path)==L:
                    if s in adj[u] and path[1]<path[-1]: cycles.append(tuple(path))
                    continue
                for v in adj[u]:
                    if v==s or v<=s or v in seen: continue
                    stack.append((v,path+[v],seen|{v}))
    return cycles

def check_cover():
    p=C['pass4253_girth16_levi_cover'];edges,adj=build_levi();assert len(edges)==160 and {len(a) for a in adj}=={4}
    edge_index={tuple(sorted(e)):i for i,e in enumerate(edges)};par=[-1]*80;q=collections.deque([0]);par[0]=0;tree=set()
    while q:
        u=q.popleft()
        for v in adj[u]:
            if par[v]<0: par[v]=u;tree.add(edge_index[tuple(sorted((u,v)))]);q.append(v)
    cotree=[e for e in range(160) if e not in tree];assert len(cotree)==81
    x=p['cotree_voltage_vector'];full=[0]*160
    for j,e in enumerate(cotree):full[e]=x[j]
    assert hashlib.sha256(json.dumps(x,separators=(',',':')).encode()).hexdigest()==p['cotree_voltage_vector_sha256']
    assert hashlib.sha256(json.dumps(full,separators=(',',':')).encode()).hexdigest()==p['full_voltage_vector_sha256']
    counts={};zeros={};prime=2731
    for L in (8,10,12,14):
        cs=simple_cycles_L(adj,L);counts[str(L)]=len(cs);z=0
        for cyc in cs:
            s=0
            for i in range(L):
                u,v=cyc[i],cyc[(i+1)%L];ei=edge_index[tuple(sorted((u,v)))];s=(s+(1 if u<40 else -1)*full[ei])%prime
            z+=s==0
        zeros[str(L)]=z
    assert counts==p['short_cycle_counts'] and zeros==p['zero_voltage_cycles']
    assert zeros=={'8':1,'10':0,'12':18,'14':132}
    assert p['certified_girth_lower_bound']==8 and p['status']=='RETRACTED_BY_PASS_4329'

def loop_leak(theta,r):
    h=math.sqrt(math.sin(theta)**2+(math.cos(theta)-r)**2)
    return (r*r*math.sin(theta)**2/h**2)*math.sin(math.pi*h/r)**2

def check_holonomy():
    p=C['pass4254_fault_aware_su4_holonomy'];d=p['demo_common_polar_offset_rad'];r=p['speed_ratio_omega_over_Omega'];e=math.pi*(math.cos(d)-1)
    assert abs(e-p['demo_phase_error_rad'])<1e-15
    assert abs(.3*(1-math.cos(e))-p['demo_average_gate_infidelity_from_phase_only'])<1e-15
    vals=[loop_leak(math.pi/3,r),loop_leak(2*math.pi/3,r)]
    assert max(abs(a-b) for a,b in zip(vals,p['per_loop_nonadiabatic_leakage']))<1e-15
    assert abs(sum(vals)-p['two_loop_leakage_union_bound_from_exact_values'])<1e-15

def nb(s):return 1/(math.exp(2*math.exp(-s))-1)
def flow(s,g):
    n=nb(s);return math.log(80)-4*s+g*n-.004*n*n

def fp_vals(N,g,D=.25,a=.4,b=6.3):
    xs=np.linspace(a,b,N);dx=xs[1]-xs[0];F=np.array([flow(x,g) for x in xs]);U=np.concatenate([[0.],cumulative_trapezoid(-F,xs)]);U-=U.min();du=np.diff(U)
    up=D/dx**2*np.exp(-du/(2*D));down=D/dx**2*np.exp(du/(2*D));diag=np.zeros(N);diag[:-1]+=up;diag[1:]+=down;off=-np.sqrt(up*down)
    return eigh_tridiagonal(diag,off,select='i',select_range=(0,4),eigvals_only=True)

def check_hysteresis():
    p=C['pass4255_quantum_hysteresis_spectrum'];g=p['g_coexistence']
    for N in (301,601,1201,2401):
        v=fp_vals(N,g);exp=p['finite_volume_grid_convergence'][str(N)];assert abs(v[1]-exp[0])<2e-10 and abs(v[2]-exp[1])<2e-3
    assert abs(2*p['two_state_tunnel_demo_Delta']-p['coherent_to_overdamped_exceptional_point_gamma_phi'])<1e-15

def check_clock():
    p=C['pass4256_clock_auxiliary_optimum'];pattern=list(range(8))*3
    assert len(pattern)==24 and len(set(pattern))==8
    assert p['new_auxiliary_ancillas']==13+24+8==45 and p['total_clock_plus_aux_qubits']==50 and p['max_locality']==3

RB=np.array([.00979708977002,.0203649786239,.0410938074485,.0738588749836,.0950655772517,.0738588749836,.0410938074485,.0203649786239,.00979708977002])
GB=np.array([.931739737612,.916053718604,.87648655463,.805844961224,.76,.805844961224,.87648655463,.916053718604,.931739737612])
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
def params(rv=RB,gv=GB):
    S=chain(rv,gv);tau=float(abs(S[0,0])**2);nsp=float(np.sum(abs(S[0,19:])**2));y=nsp+.5-tau/2;nbar=(2*y/(1-tau)-1)/2;eb=y>=(1+tau)/2-1e-12
    return tau,nsp,y,nbar,eb
def sigmoid(x):return 1/(1+np.exp(-x))
def logit(x):return np.log(x/(1-x))
def gfun(n):
    if n<=1e-14:return 0.
    return (n+1)*math.log(n+1)-n*math.log(n)
def seigs(V):
    m=len(V)//2;O=np.kron(np.eye(m),np.array([[0.,1.],[-1.,0.]]));return np.sort(np.abs(np.linalg.eigvals(1j*O@V)))[::2].real
def entropy(V):return sum(gfun(max(0,float(x)-.5)) for x in seigs(V))
def ic(tau,nbar,N):
    nuA=N+.5;nuE=nbar+.5;c=math.sqrt(nbar*(nbar+1));V=np.zeros((6,6));V[:2,:2]=nuA*np.eye(2);V[2:4,2:4]=nuE*np.eye(2);V[4:6,4:6]=nuE*np.eye(2);V[2:4,4:6]=np.diag([c,-c]);V[4:6,2:4]=np.diag([c,-c]);t=math.sqrt(tau);r=math.sqrt(1-tau);B=np.eye(6);B[:2,:2]=t*np.eye(2);B[:2,2:4]=r*np.eye(2);B[2:4,:2]=-r*np.eye(2);B[2:4,2:4]=t*np.eye(2);W=B@V@B.T;return entropy(W[:2,:2])-entropy(W[2:6,2:6])
def check_channel():
    p=C['pass4257_full_19mode_channel_bounds'];base=params();keys=['tau','spontaneous_output_photons','added_noise_y','effective_thermal_environment_nbar'];assert max(abs(base[i]-p['baseline'][k]) for i,k in enumerate(keys))<2e-12
    rng=np.random.default_rng(20260807);ii=np.arange(9);L=np.linalg.cholesky(np.exp(-np.abs(ii[:,None]-ii[None,:])/2));rows=[]
    for _ in range(512):
        x=L@rng.standard_normal(9);rows.append(params(RB*np.exp(.35*x),sigmoid(logit(GB)+.25*x)))
    tau=np.array([r[0] for r in rows]);nbv=np.array([r[3] for r in rows]);assert int(np.sum(tau<=.5))==510 and int(np.sum(tau>.5))==2 and sum(r[4] for r in rows)==0
    for i in np.where(tau>.5)[0]:assert max(ic(float(tau[i]),float(nbv[i]),N) for N in np.logspace(-6,6,121))<=1e-10

def check_outside_box():
    p=C['pass4258_levi_spectral_form_factor'];assert abs(p['infinite_time_average']-2054/6400)<1e-15 and abs(p['plateau_enhancement_factor']-25.675)<1e-12
    p=C['pass4259_levi_modular_spectrum'];nu4=1/math.sqrt(3);nu6=.25*math.sqrt(2+10/math.sqrt(19));assert abs(math.log((nu4+.5)/(nu4-.5))-p['entanglement_energies']['epsilon4'])<1e-14 and abs(math.log((nu6+.5)/(nu6-.5))-p['entanglement_energies']['epsilon_sqrt6'])<1e-14
    p=C['pass4260_ballistic_causal_capacity'];assert abs(p['radial_group_velocity_over_J']-2*math.sqrt(3))<1e-15 and p['conditional_tree_ball_vertices']==4373

def verify():
    assert semantic_hash(C)==C['semantic_sha256'] and not C['all_checks_hold']
    assert not C['checks']['4253'] and all(C['checks'][str(i)] for i in range(4254,4261))
    check_cover();check_holonomy();check_hysteresis();check_clock();check_channel();check_outside_box()
    print('PASS_4253_RETRACTION_4254_4260',C['semantic_sha256']);return True
if __name__=='__main__':verify()
