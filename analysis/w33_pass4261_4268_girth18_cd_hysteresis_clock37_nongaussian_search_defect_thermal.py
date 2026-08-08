#!/usr/bin/env python3
from __future__ import annotations
import collections, hashlib, itertools, json, math
from pathlib import Path
import numpy as np
from scipy.integrate import cumulative_trapezoid
from scipy.linalg import eigh, expm

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_4261_4268_GIRTH18_CD_HYSTERESIS_CLOCK37_NONGAUSSIAN_SEARCH_DEFECT_THERMAL.json'
C=json.loads(OUT.read_text())

def semantic_hash(c):
    x=dict(c);x.pop('semantic_sha256',None)
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def norm_proj(v):
    v=tuple(x%3 for x in v);f=next(x for x in v if x);q=1 if f==1 else 2
    return tuple(q*x%3 for x in v)
def symp(x,y):return (x[0]*y[1]-x[1]*y[0]+x[2]*y[3]-x[3]*y[2])%3
def levi():
    pts=sorted({norm_proj(v) for v in itertools.product(range(3),repeat=4) if any(v)});pi={p:i for i,p in enumerate(pts)};ls=set()
    for i,j in itertools.combinations(range(40),2):
        x,y=pts[i],pts[j]
        if symp(x,y):continue
        ls.add(frozenset(pi[norm_proj(tuple((a*x[k]+b*y[k])%3 for k in range(4)))] for a,b in itertools.product(range(3),repeat=2) if a or b))
    ls=sorted(ls,key=lambda z:tuple(sorted(z)));edges=[(p,40+i) for i,l in enumerate(ls) for p in sorted(l)]
    A=[[] for _ in range(80)]
    for ei,(u,v) in enumerate(edges):A[u].append((v,ei,1));A[v].append((u,ei,-1))
    return edges,A

def check_cover():
    p=C['pass4261_girth18_cover'];edges,A=levi();assert len(edges)==160
    full=[0]*160
    for e,v in zip(p['cotree_edge_indices'],p['cotree_voltage_vector']):full[e]=v
    prime=p['prime'];expected=p['radius8_tree_ball_vertices']
    for root in range(80):
        st=(root,0);dist={st:0};parent={st:None};q=collections.deque([st])
        while q:
            u,sh=q.popleft();d=dist[(u,sh)]
            if d>=8:continue
            for v,e,sgn in A[u]:
                z=(v,(sh+sgn*full[e])%prime)
                if z not in dist:dist[z]=d+1;parent[z]=(u,sh);q.append(z)
                elif parent[(u,sh)]!=z:assert d+dist[z]+1>16
        assert len(dist)==expected
    assert p['cover_vertices']==80*prime and p['cover_edges']==160*prime

def check_holonomy():
    p=C['pass4262_dynamically_corrected_holonomic_cz'];d=p['demo_common_polar_offset_rad'];pe=math.pi*(1-math.cos(d))
    assert abs(pe-p['demo_phase_error_rad'])<1e-15
    assert abs(.3*(1-math.cos(pe))-p['demo_average_gate_infidelity_phase_only'])<1e-15
    assert abs(math.cos(p['latitude_theta_rad'])-.25)<1e-15
    th=p['latitude_theta_rad'];phi=.37;n=np.array([math.sin(th)*math.cos(phi),math.sin(th)*math.sin(phi),math.cos(th)]);dn=.1*np.array([-math.sin(th)*math.sin(phi),math.sin(th)*math.cos(phi),0.]);assert abs(np.dot(n,np.cross(n,dn)))<1e-15
    assert p['four_loop_union_bound_one_percent_cd_error']<2.1e-6

def nb(s):return 1/(math.exp(2*math.exp(-s))-1)
def flow(s,g):
    n=nb(s);return math.log(80)-4*s+g*n-.004*n*n

def davies_gap(K):
    p=C['pass4263_full_coordinate_lindblad_hysteresis'];N=p['grid_points'];a,b=p['coordinate_interval'];M=p['mass_M'];T=p['temperature_T'];kap=p['davies_kappa'];g=p['coexistence_g']
    xs=np.linspace(a,b,N);dx=xs[1]-xs[0];F=np.array([flow(x,g) for x in xs]);U=np.concatenate([[0.],cumulative_trapezoid(-F,xs)]);U-=U.min()
    diag=1/(M*dx*dx)+U;off=-1/(2*M*dx*dx)*np.ones(N-1);H=np.diag(diag)+np.diag(off,1)+np.diag(off,-1);ev,V=eigh(H);ev=ev[:K];V=V[:,:K];X=V.T@(xs[:,None]*V);beta=1/T
    R=np.zeros((K,K))
    for i in range(K):
        for j in range(K):
            if i==j:continue
            w=ev[i]-ev[j]
            if w>0:n=1/(math.exp(beta*w)-1) if beta*w<700 else 0.;rate=kap*w*(n+1)*abs(X[j,i])**2
            else:w=-w;n=1/(math.exp(beta*w)-1) if beta*w<700 else 0.;rate=kap*w*n*abs(X[j,i])**2
            R[i,j]=rate
    Q=np.zeros((K,K))
    for i in range(K):
        for j in range(K):
            if i!=j:Q[j,i]=R[i,j];Q[i,i]-=R[i,j]
    z=np.linalg.eigvals(Q);z=z[np.argsort(-z.real)];return float(-z[1].real)

def check_lindblad():
    p=C['pass4263_full_coordinate_lindblad_hysteresis']
    for K in (14,16,20):assert abs(davies_gap(K)-p['population_gap_convergence_K'][str(K)])<3e-13
    assert abs(1/p['liouvillian_gap']-p['metastable_lifetime'])/p['metastable_lifetime']<1e-7

def check_clock():
    p=C['pass4264_qutrit_gray_clock37'];assert p['auxiliary_ancillas']==13+24==37 and p['separate_dynamic_flags']==0 and p['max_locality']==3
    H=np.zeros((49,49))
    for j in range(48):H[j,j+1]=H[j+1,j]=math.sqrt((j+1)*(48-j))
    assert np.max(np.abs(np.linalg.eigvalsh(H)-np.arange(-48,49,2)))<2e-10

def check_hawking_meta():
    p=C['pass4265_nongaussian_hawking_search'];assert not p['positive_coherent_information_found']
    a,b=p['high_tau_samples'];assert a['sample']==216 and b['sample']==220 and .5<a['tau']<b['tau']<.52
    assert p['tested_family_maximum'].startswith('0, attained')

def check_search_defect():
    p=C['pass4266_levi_continuous_time_quantum_search'];Q=np.zeros((5,5));off=p['shell_hamiltonian_offdiagonals']
    for i,x in enumerate(off):Q[i,i+1]=Q[i+1,i]=x
    s=np.sqrt(np.array(p['distance_shell_sizes'])/80);H=-p['found_gamma']*Q;H[0,0]-=1;psi=expm(-1j*H*p['found_time'])@s;assert abs(abs(psi[0])**2-p['success_probability'])<2e-12
    d=C['pass4267_single_defect_bound_mode'];ev,V=eigh(Q+np.diag([d['V'],0,0,0,0]));assert abs(ev[-1]-d['bound_state_energy'])<2e-12 and abs(abs(V[0,-1])**2-d['defect_probability'])<2e-12

def pair_nu(beta,sigma):
    wm=math.sqrt(5-sigma);wp=math.sqrt(5+sigma);c=lambda x:1/math.tanh(x)
    qm=c(beta*wm/2)/(2*wm);pm=wm*c(beta*wm/2)/2;qp=c(beta*wp/2)/(2*wp);pp=wp*c(beta*wp/2)/2
    V=np.zeros((4,4));V[0,0]=V[2,2]=(qm+qp)/2;V[0,2]=V[2,0]=(qm-qp)/2;V[1,1]=V[3,3]=(pm+pp)/2;V[1,3]=V[3,1]=(pm-pp)/2;P=np.diag([1,1,1,-1]);W=P@V@P;O=np.kron(np.eye(2),np.array([[0.,1.],[-1.,0.]]));z=np.sort(np.abs(np.linalg.eigvals(1j*O@W)))[::2];return float(z[0])
def check_thermal():
    p=C['pass4268_thermal_point_line_entanglement']
    for sig,T in [(4,p['sigma4_entanglement_temperature']),(math.sqrt(6),p['sigmasqrt6_entanglement_temperature'])]:assert abs(pair_nu(1/T,sig)-.5)<2e-12
    ln=max(0,-math.log(2*pair_nu(1,4)))+24*max(0,-math.log(2*pair_nu(1,math.sqrt(6))));assert abs(ln-p['logneg_at_T1_nats'])<2e-12

def verify():
    assert semantic_hash(C)==C['semantic_sha256'] and C['all_checks_hold'];check_cover();check_holonomy();check_lindblad();check_clock();check_hawking_meta();check_search_defect();check_thermal();print('PASS_4261_4268',C['semantic_sha256']);return True
if __name__=='__main__':verify()
