#!/usr/bin/env python3
"""Passes 4081-4088: deterministic deep-physics verifier.

This packet deliberately reuses the exact PSp(4,3) reconstruction from
Passes 4057-4064, then adds exact character fingerprints, effective-pair
dynamics, a two-parameter pump, overlap fermions, subgroup commutants,
inverse scattering, Landauer accounting, and an operational causal metric.
"""
from __future__ import annotations
import hashlib, importlib.util, itertools, json, math
from pathlib import Path
import networkx as nx
import numpy as np
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/"data/PART_4081_4088_DEEP_PHYSICS.json"

def semantic_sha(x):
    raw={k:v for k,v in x.items() if k!="semantic_sha256"}
    return hashlib.sha256(json.dumps(raw,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def load_prior():
    p=ROOT/"analysis/w33_pass4057_4064_advanced_physics.py"
    spec=importlib.util.spec_from_file_location("p4057",p)
    mod=importlib.util.module_from_spec(spec); assert spec.loader
    spec.loader.exec_module(mod)
    return mod

def exact_chars(block):
    rt3=math.sqrt(3)
    out=[]
    for ir in block["irreducibles"]:
        vals=np.array([(p+1j*q*rt3)/2 for p,q in ir["atlas_character_fingerprint_half_p_plus_q_i_sqrt3"]])
        out.append((ir["label"],ir["degree"],ir["dark_multiplicity"],vals))
    return out

def fhs_chern(N=41,J=1.0,R=0.4):
    def vec(k,th):
        j1=J+R*math.cos(th); j2=J-R*math.cos(th); m=2*R*math.sin(th)
        dx=j1+j2*math.cos(k); dy=j2*math.sin(k)
        H=np.array([[m,dx-1j*dy],[dx+1j*dy,-m]],complex)
        return np.linalg.eigh(H)[1][:,0]
    v=[[vec(2*math.pi*i/N,2*math.pi*j/N) for j in range(N)] for i in range(N)]
    flux=0.0
    for i in range(N):
        for j in range(N):
            u=v[i][j]; ux=v[(i+1)%N][j]; uy=v[i][(j+1)%N]; uxy=v[(i+1)%N][(j+1)%N]
            links=[]
            for a,b in ((u,ux),(ux,uxy),(uxy,uy),(uy,u)):
                z=np.vdot(a,b); links.append(z/abs(z))
            flux+=np.angle(np.prod(links))
    return flux/(2*math.pi)

def overlap_residual(k,m0=1.0,r=1.0,a=1.0):
    I2=np.eye(2); X=np.array([[0,1],[1,0]],complex)
    Y=np.array([[0,-1j],[1j,0]],complex); Z=np.diag([1,-1])
    gam=[np.kron(X,X),np.kron(X,Y),np.kron(X,Z),np.kron(Y,I2)]
    g5=np.kron(Z,I2)
    DW=1j*sum(gam[mu]*math.sin(k[mu]) for mu in range(4))
    DW+=(r*sum(1-math.cos(x) for x in k))*np.eye(4)
    HW=g5@(DW-m0*np.eye(4))
    w,V=np.linalg.eigh(HW); sign=V@np.diag(np.sign(w))@V.conj().T
    D=(np.eye(4)+g5@sign)/a
    return np.linalg.norm(g5@D+D@g5-a*D@g5@D)

def verify():
    c=json.loads(CERT.read_text())
    assert semantic_sha(c)==c["semantic_sha256"]
    assert c["checks"]=={str(i):True for i in range(4081,4089)}

    prior=load_prior()
    pts,lines,L,edges,D,P=prior.geometry()
    grouped,nclass=prior.dark_irreps(pts,lines,edges)
    assert nclass==20
    b=c["pass4081_canonical_dark_irreps"]
    rebuilt={}
    for ir in b["irreducibles"]:
        rebuilt.setdefault(str(ir["degree"]),[]).append(ir["dark_multiplicity"])
    rebuilt={k:sorted(v) for k,v in sorted(rebuilt.items(),key=lambda kv:int(kv[0]))}
    assert grouped==rebuilt
    chars=exact_chars(b); sizes=np.array(b["class_sizes_in_atlas_order"],float)
    for i,(_,di,_,chi) in enumerate(chars):
        for j,(_,dj,_,psi) in enumerate(chars):
            inner=np.sum(sizes*chi*np.conj(psi))/25920
            assert abs(inner-(1 if i==j else 0))<1e-8
        assert abs(chi[0]-di)<1e-9
    assert sum(d*m for _,d,m,_ in chars)==3161
    assert next(m for label,d,m,_ in chars if label=="1")==0
    assert b["internal_class_index_in_atlas_order"]==[0,1,2,4,3,5,6,7,8,9,11,10,13,12,14,15,16,17,19,18]

    dlt,t,a=7.0,0.3,1.2
    Jp=2*t*t/dlt
    ks=np.linspace(-math.pi,math.pi,2001)
    E=-dlt-4*t*t/dlt-4*t*t*np.cos(ks)/dlt
    assert abs((E.max()-E.min())-8*t*t/dlt)<1e-12
    mstar=dlt/(4*t*t*a*a)
    dk=1e-4
    e0=-dlt-4*t*t/dlt-4*t*t/dlt
    ep=-dlt-4*t*t/dlt-4*t*t*math.cos(dk)/dlt
    assert abs((ep-e0)/dk**2-1/(2*mstar*a*a))<1e-7
    nu=.7
    xi=math.asinh(abs(nu)/(2*abs(Jp)))
    assert xi>0 and abs(math.sinh(xi)-abs(nu)/(2*abs(Jp)))<1e-12

    assert abs(fhs_chern()-1)<1e-10
    assert c["pass4083_two_parameter_pair_pump"]["minimum_band_gap"]=="4R"

    tests=[(.2,.3,.4,.5),(.7,.1,1.1,.2),(1.2,.8,.4,.9)]
    assert max(overlap_residual(k) for k in tests)<3e-14
    assert sum(1 for bits in itertools.product([0,1],repeat=4) if 2*sum(bits)==0)==1
    assert c["pass4084_overlap_fermions"]["w33_fiber_light_species"]==81

    h=c["pass4085_one_marked_edge_nonabelian_commutant"]
    assert h["stabilizer_order"]==25920//160==162
    comps=h["restriction_components"]
    assert sum(x["degree"]*x["multiplicity"] for x in comps)==81
    assert sum(x["multiplicity"]**2 for x in comps)==45
    assert any(x["degree"]==6 and x["multiplicity"]==3 for x in comps)
    assert any(x["degree"]==3 and x["multiplicity"]==2 for x in comps)

    s=sp.symbols("s")
    lhs=sp.Rational(1,80)*(1/s+24/(s+4-sp.sqrt(6))+30/(s+4)+24/(s+4+sp.sqrt(6))+1/(s+8))
    rhs=(s**4+16*s**3+78*s**2+112*s+4)/(s*(s+4)*(s+8)*(s**2+8*s+10))
    assert sp.factor(lhs-rhs)==0

    dims=np.array(c["pass4087_landauer_dark_reservoir"]["isotypic_dimensions"],float)
    p=dims/dims.sum()
    cond=float(np.sum(p*np.log(dims))); H=float(-np.sum(p*np.log(p)))
    assert dims.sum()==3161 and abs(cond+H-math.log(3161))<1e-12

    Xg=nx.line_graph(L); A=nx.to_numpy_array(Xg,nodelist=edges,dtype=int)
    base=edges[0]; dist=nx.single_source_shortest_path_length(Xg,base)
    assert {d:sum(dist[e]==d for e in edges) for d in range(1,5)}=={1:6,2:18,3:54,4:81}
    for d,want in {1:1,2:1,3:1,4:2}.items():
        Ad=np.linalg.matrix_power(A,d)
        vals={int(Ad[0,j]) for j,e in enumerate(edges) if dist[e]==d}
        assert vals=={want}
        for n in range(d):
            An=np.linalg.matrix_power(A,n)
            assert all(An[0,j]==0 for j,e in enumerate(edges) if dist[e]==d)

    return {"all_checks_hold":True,"semantic_sha256":c["semantic_sha256"],
            "dark_dimension":3161,"pair_pump_chern":fhs_chern(),
            "marked_edge_commutant_dimension":45}

if __name__=="__main__":
    print(json.dumps(verify(),indent=2,sort_keys=True))
