#!/usr/bin/env python3
"""Five physical falsifiers + three independent outside-box finite geometry controls.

The sources are existing W33 Pauli projectors and actual Schlaefli/W33 data.
Every spatial substrate, hopping strength, gauge group or quantum phase not
derived from W33 is explicitly identified as an extra model input.
"""
from __future__ import annotations
import itertools, json, math, sys
from pathlib import Path
import networkx as nx
import numpy as np
from scipy.sparse import diags, eye, kron
from scipy.sparse.linalg import eigsh

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_pass12055_microscopic_tick_model import PTS,ADJ,PROJ,pauli,w
from w33_20261031_helstrom_optical_braid_readout import angle_rotation
OUT=ROOT/"data/w33_20261031_quantum_geometry_eight_new_falsifiers.json"
def N(x):return float(np.linalg.norm(x))
def peak_bernstein(p,q):return float(p@q)
def optical_gauge():
    F=np.array([[0.,1.,-3.],[-1.,0.,2.],[3.,-2.,0.]])
    wilson=lambda m:float((m[0,1]*m[1,2]*m[2,0]).real)
    assert wilson(F)==6 and wilson(-F)==-6
    rng=np.random.default_rng(73111)
    errors=[]
    for _ in range(200):
        theta=rng.uniform(-math.pi,math.pi,3)
        D=np.diag(np.exp(1j*theta))
        Fp=D@F@D.conj().T
        Fm=-Fp
        loops=Fp[0,1]*Fp[1,2]*Fp[2,0]
        minus=Fm[0,1]*Fm[1,2]*Fm[2,0]
        errors.append(max(abs(loops-6),abs(minus+6)))
    assert max(errors)<1e-13
    v=(np.eye(3)+F@F/14+F/math.sqrt(14))[:,0]
    u=(np.eye(3)+F@F/14-F/math.sqrt(14))[:,0]
    assert abs(v@u+3/7)<1e-14
    e=np.linalg.eigh(np.outer(v,v)-np.outer(u,u))[1]
    Q=np.stack([e[:,2],e[:,0],e[:,1]])
    results=[]
    for shift in (0.,.03,.10,.20):
        # Phase drift that is common to both hypotheses (not random refits).
        D=np.diag(np.exp(1j*np.array([shift,-shift/2,shift/3])))
        pa=np.abs(Q@D@v)**2;pb=np.abs(Q@D@u)**2
        err=.5*np.sum(np.minimum(pa,pb))
        results.append({"phase_drift":shift,"optimal_reshaped_classical_error":float(err)})
    assert abs(results[0]["optimal_reshaped_classical_error"]-(1-2*math.sqrt(10)/7)/2)<1e-13
    # Unknown *hypothesis-dependent* port gains can counterfeit either
    # probability vector. They are not allowed in a calibrated fixed model.
    raw_plus=np.abs(v)**2;raw_minus=np.abs(u)**2
    spoof=raw_minus/raw_plus
    assert np.max(abs(raw_plus*spoof/(raw_plus@spoof)-raw_minus))<1e-13
    return {"status":"PASS_Z2_TRIANGLE_WILSON_SIGN_GAUGE_OBSTRUCTION",
       "signed_triangle_Wilson_products":[wilson(F),wilson(-F)],
       "random_U1_local_rephasings_verified":200,"maximum_invariance_error":max(errors),
       "port_calibration_spoof_gains":spoof.tolist(),
       "drift_control":results,
       "scope":"A directed, labelled three-mode real-skew coupler has a gauge-invariant odd-loop sign under diagonal U(1) rephasings; arbitrary hypothesis-dependent detector gains erase identifiability. Phase reference and relative rail calibration are external inputs."}

def clock_quantum():
    # Four directions deliberately contain both commuting and noncommuting pairs.
    indices=None
    for group in itertools.combinations(range(40),4):
        a=[int(ADJ[i,j])for i,j in itertools.combinations(group,2)]
        if 1<=sum(a)<=4:
            indices=group;break
    assert indices
    q=4;J=1.;K=2.
    costs=np.array([[0. if a==b else
                      (2. if ADJ[indices[a],indices[b]] else 2-4*K/3)
                      for b in range(q)]for a in range(q)])
    outcomes=[]
    for spatial_edges in ([(0,1),(1,2)],[(0,1),(1,2),(2,0)],
                          [(0,1),(1,2),(2,3),(3,0)]):
        sites=max(max(a,b)for a,b in spatial_edges)+1
        dim=q**sites
        labels=np.array(list(itertools.product(range(q),repeat=sites)),dtype=int)
        diagE=np.array([sum(costs[s[a],s[b]]for a,b in spatial_edges)for s in labels])
        # Local transverse projector -h|+><+| including constant diagonal;
        # Perron-Frobenius ensures unique ground for h>0 on connected color graph.
        V=None
        P=np.ones((q,q))/q
        for n in range(sites):
            left=eye(q**n,format="csr")
            right=eye(q**(sites-n-1),format="csr")
            h=kron(kron(left,P),right,format="csr")
            V=h if V is None else V+h
        assert V is not None
        rows=[]
        for field in (0.,.1,.4,1.):
            H=diags(diagE,format="csr")-field*V
            if field==0:
                ev=np.sort(diagE)
                e0=float(ev[0]);e1=float(next((x for x in ev if x>e0+1e-10),e0))
                gdeg=int(sum(abs(ev-e0)<1e-9))
                gap=0.
            else:
                ev=np.linalg.eigvalsh(H.toarray()) if dim<=64 else eigsh(H,k=2,which="SA",return_eigenvectors=False,tol=1e-10)
                ev=np.sort(ev)
                e0=float(ev[0]);e1=float(ev[1]);gdeg=1;gap=e1-e0
                assert gap>1e-9
            rows.append({"transverse_field":field,"ground_energy":e0,"gap":gap,"ground_degeneracy":gdeg})
        outcomes.append({"sites":sites,"edges":spatial_edges,"hilbert_dimension":dim,
                         "classical_min":float(diagE.min()),"spectral_samples":rows})
    return {"status":"PASS_FINITE_QUANTUM_CLOCK_NONTRANSITION_CONTROL",
      "Pauli_direction_indices":indices,"pair_energy":costs.tolist(),"models":outcomes,
      "boundary":"120 genuine tick labels are reduced to 4 directions with one fixed outcome. Local Hilbert factors, transverse field and spatial graph are supplied. A positive finite-size gap for h>0 is not a thermodynamic phase classification."}

def chiral_pure_gauge():
    # Native rank-three projectors supply globally periodic momentum rotations:
    # a smooth periodic conjugation of a fixed rank-3 projector is a trivial bundle.
    P0=np.asarray(PROJ[0][0]);P1=np.asarray(PROJ[4][0]);P2=np.asarray(PROJ[13][0])
    assert N(P0@P0-P0)<1e-12
    vec=np.linalg.eigh(P0)[1][:,6:] # 3 eigenvectors with eigenvalue 1
    assert N(vec.conj().T@vec-np.eye(3))<1e-12
    def U(theta,P):return np.eye(9)+(np.exp(1j*theta)-1)*P
    samples=[]
    for m in (7,11,17):
        frames=[]
        for i in range(m):
            layer=[]
            for j in range(m):
                kx=2*math.pi*i/m;ky=2*math.pi*j/m
                layer.append(U(kx,P1)@U(ky,P2)@vec)
            frames.append(layer)
        flux=0.
        curvature_abs=0.
        for i in range(m):
            for j in range(m):
                q=frames[i][j]
                f=lambda a,b:np.linalg.det(a.conj().T@b)
                u=f(q,frames[(i+1)%m][j]);v=f(q,frames[i][(j+1)%m])
                v2=f(frames[(i+1)%m][j],frames[(i+1)%m][(j+1)%m])
                u2=f(frames[i][(j+1)%m],frames[(i+1)%m][(j+1)%m])
                assert min(abs(x)for x in (u,v,u2,v2))>.2
                z=(u/abs(u))*(v2/abs(v2))/((u2/abs(u2))*(v/abs(v)))
                fxy=np.angle(z)
                flux+=fxy;curvature_abs+=abs(fxy)
        ch=flux/(2*math.pi)
        assert abs(ch)<1e-10
        samples.append({"grid":m,"chern_number":ch,
                        "integrated_absolute_discrete_curvature":curvature_abs})
    return {"status":"PASS_NATIVE_GLOBAL_BLOCH_FRAME_CHERN_ZERO",
        "rank":3,"grid_tests":samples,
        "proof":"P(k)=U(k)P0 U(k)^dagger, U=exp(i kx P1) exp(i ky P2) is globally smooth and periodic. This supplies a global frame U(k)|u_a>, hence the rank-3 Bloch bundle is trivial and c1=0 exactly.",
        "boundary":"A Bloch torus and hopping wavevector are supplied. Nonzero local Berry curvature may occur while total Chern is zero. Nontrivial Chern requires patching obstructions, not globally conjugating a constant W33 projector."}

def gauge_geometry():
    # Dynamical two-component frames e(x) with U(1) edge connection; exact
    # finite-lattice gauge invariance and Noether/Ward zero mode.
    n=3;rng=np.random.default_rng(31031)
    e=rng.normal(size=(n,n,2)); a=rng.normal(size=(n,n,2))
    theta=rng.normal(size=(n,n))
    def rot(x,v):return np.array([np.cos(x)*v[0]-np.sin(x)*v[1],np.sin(x)*v[0]+np.cos(x)*v[1]])
    def act(e,a,beta=.7):
        energy=0.
        for x in range(n):
            for y in range(n):
                for mu in range(2):
                    nxt=((x+1)%n,y)if mu==0 else(x,(y+1)%n)
                    d=e[nxt]-rot(a[x,y,mu],e[x,y])
                    energy+=.5*float(d@d)
                xx=(x+1)%n;yy=(y+1)%n
                curl=a[x,y,0]+a[xx,y,1]-a[x,yy,0]-a[x,y,1]
                energy+=beta*(1-np.cos(curl))
        return energy
    gaugea=a.copy();gaugee=e.copy()
    for x in range(n):
        for y in range(n):
            gaugee[x,y]=rot(theta[x,y],e[x,y])
            gaugea[x,y,0]+=theta[(x+1)%n,y]-theta[x,y]
            gaugea[x,y,1]+=theta[x,(y+1)%n]-theta[x,y]
    E0=act(e,a);Eg=act(gaugee,gaugea)
    assert abs(E0-Eg)<1e-11
    # infinitesimal Ward identity dS/dtheta_v == 0 around arbitrarily
    # distorted configurations; independent finite difference check.
    eps=1e-6
    def transformed(t):
        aa=a.copy();ee=e.copy();x=y=0
        ee[x,y]=rot(t,e[x,y])
        aa[x,y,0]-=t;aa[x,y,1]-=t
        aa[(x-1)%n,y,0]+=t;aa[x,(y-1)%n,1]+=t
        return act(ee,aa)
    deriv=(transformed(eps)-transformed(-eps))/(2*eps)
    assert abs(deriv)<1e-8
    return {"status":"PASS_LOCAL_LATTICE_FRAME_CONNECTION_WARD_IDENTITY",
            "lattice":[n,n],"gauge_group":"SO(2) = U(1)",
            "energy_before":E0,"energy_after_local_transform":Eg,
            "gauge_invariance_error":abs(E0-Eg),
            "infinitesimal_Ward_residual":abs(deriv),
            "Hamiltonian":"E=1/2 sum_edges ||e(y)-R(a_xy)e(x)||^2 + beta sum_plaquettes(1-cos curl a)",
            "boundary":"Actual exact local frame/connection gauge symmetry on an externally chosen 2D periodic lattice, not tetrad Einstein-Cartan gravity, not local Lorentz SO(1,3), and no quantum spin-2 modes."}

def quantum_double_S3():
    # S3 = semidirect product Z3 rtimes Z2: (a,b)(c,d)=(a+(-1)^b c,b+d).
    g=list(itertools.product(range(3),range(2)));idx={z:i for i,z in enumerate(g)}
    mul=lambda x,y:((x[0]+(-1)**x[1]*y[0])%3,(x[1]+y[1])%2)
    for x,y,z in itertools.product(g,repeat=3):
        assert mul(mul(x,y),z)==mul(x,mul(y,z))
    inv=lambda x:next(y for y in g if mul(x,y)==(0,0)and mul(y,x)==(0,0))
    classes=[];unseen=set(g)
    while unseen:
        x=next(iter(unseen))
        C={mul(mul(y,x),inv(y))for y in g}
        unseen-=C;classes.append(C)
    assert sorted(map(len,classes))==[1,2,3]
    # Electron/flux (class, centralizer-irrep) quantum dimensions
    dims=[]
    types=[]
    for C in classes:
        c=next(iter(C));central=[y for y in g if mul(y,c)==mul(c,y)]
        irreps=([1,1,2] if len(central)==6 else [1]*len(central))
        for ir in irreps:
            dims.append(len(C)*ir);types.append([len(C),len(central),ir,len(C)*ir])
    assert sorted(dims)==[1,1,2,2,2,2,3,3]
    assert sum(x*x for x in dims)==36 and len(dims)==8
    su4=[1,math.sqrt(3),2,math.sqrt(3),1]
    assert abs(sum(x*x for x in su4)-12)<1e-12
    assert len(su4)!=len(dims)
    return {"status":"PASS_QUANTUM_DOUBLE_ANYON_CATEGORY_NONIDENTITY",
      "S3_anyon_quantum_dimensions":sorted(dims),"S3_sector_table":types,
      "S3_rank":8,"S3_total_quantum_dimension_squared":36,
      "SU2_level4_quantum_dimensions":su4,"SU2_level4_rank":5,
      "SU2_level4_total_quantum_dimension_squared":12,
      "group_S3_order":6,
      "obstruction":"D(S3) and SU(2)_4 cannot be equivalent braided fusion categories: ranks 8 versus 5, total D² 36 versus 12.",
      "scope":"S3 quantum-double Hilbert space uses a physical six-level edge with a 2D gauge lattice; native two-qutrit Jones operators are not automatically this anyon model. Established quantum-double category theory, new explicit contrast in this repo packet."}

def MUB_spread():
    G=nx.from_numpy_array(ADJ)
    lines=sorted(tuple(sorted(c)) for c in nx.find_cliques(G)if len(c)==4)
    assert len(lines)==40
    bypoint={p:[l for l in lines if p in l]for p in range(40)}
    def exactcover(unused,found):
        if not unused:return found
        p=min(unused,key=lambda x:sum(set(l)<=unused for l in bypoint[x]))
        for ln in bypoint[p]:
            if set(ln)<=unused:
                result=exactcover(unused-set(ln),found+[ln])
                if result is not None:return result
        return None
    spread=exactcover(set(range(40)),[])
    assert spread is not None and len(spread)==10
    bases=[]
    I=np.eye(9)
    for line in spread:
        p,q=line[:2]
        projs=[np.array(PROJ[p][i]@PROJ[q][j])for i in range(3)for j in range(3)]
        assert all(abs(np.trace(A)-1)<1e-12 and N(A@A-A)<1e-12 for A in projs)
        assert N(sum(projs)-I)<1e-11
        bases.append(projs)
    err=max(abs(float(np.trace(A@B).real)-1/9) for i in range(10) for j in range(i+1,10)
            for A in bases[i] for B in bases[j])
    assert err<1e-12
    return {"status":"PASS_TEN_MUTUALLY_UNBIASED_QUTRIT_CONTEXT_BASES",
       "40_direction_spread":[list(l)for l in spread],
       "number_bases":10,"Hilbert_dimension":9,
       "rank_one_projectors_per_basis":9,
       "max_unbiased_probability_error":err,
       "operational_entropy_bound_nats":"For any two distinct bases, Maassen-Uffink H(B_i)+H(B_j)>=log 9, since maximal basis overlap squared is 1/9.",
       "prior_art":"Complete 10 MUB sets in prime-power dimension 9 and W33 symplectic spreads are classical mathematics and have earlier repository studies.",
       "scope":"Exact Pauli MUB/context construction; not a new physical Born-rule derivation or Bell-nonlocality experiment."}

def finite_spectral_dimension():
    # Graph spectrum from W33 strongly regular (40,12,2,4): A=12,2,-4
    A=np.array(ADJ,dtype=float)
    spec=np.linalg.eigvalsh(A)
    assert np.max(abs(np.sort(spec)-np.sort(np.array([12.]+[2.]*24+[-4.]*15))))<1e-10
    def Z(t):return 1+24*math.exp(-10*t)+15*math.exp(-16*t)
    def ds(t):
        return 2*t*(24*10*math.exp(-10*t)+15*16*math.exp(-16*t))/Z(t)
    grid=np.geomspace(1e-4,4,1000)
    vals=np.array([ds(float(t))for t in grid])
    j=int(np.argmax(vals))
    assert ds(1e-6)<1e-3 and ds(5)<1e-15
    return {"status":"PASS_FINITE_SPECTRAL_DIMENSION_PRODUCT_ARTIFACT",
      "laplacian_spectrum":{"0":1,"10":24,"16":15},
      "heat_trace_formula":"1+24 exp(-10t)+15 exp(-16t)",
      "spectral_dimension_formula":"2t(240 exp(-10t)+240 exp(-16t))/Z(t)",
      "sampled_peak":{"time":float(grid[j]),"dimension":float(vals[j])},
      "single_graph_samples":[{"t":t,"ds":ds(t)}for t in (.001,.01,.05,.1,.2,.5,1.)],
      "Cartesian_square_peak_dimension":float(2*vals[j]),
      "exact_obstruction":"For G Cartesian-square, graph Laplacian is L tensor I + I tensor L, heat trace Z2=Z1² and ds2=2 ds1 exactly. The finite spectral dimension can be multiplied by arbitrary Cartesian powers without emerging physical spatial dimensions.",
      "boundary":"Finite graph heat-trace effective dimension vanishes in both UV and IR; no continuum 4D plateau or Planck scale inferred."}

def build():
    parts={
      "optical_U1_Wilson_gauge":optical_gauge(),
      "finite_quantum_clock":clock_quantum(),
      "native_Chern_trivial_frame":chiral_pure_gauge(),
      "local_connection_Ward":gauge_geometry(),
      "quantum_double_S3_vs_Jones":quantum_double_S3(),
      "ten_W33_MUB_contexts":MUB_spread(),
      "spectral_dimension_artifact":finite_spectral_dimension()}
    assert all(d["status"].startswith("PASS_")for d in parts.values())
    return {"status":"PASS_SEVEN_NEW_QUANTUM_GEOMETRY_CONTROLS",
       "note":"The same-subgroup 2/3/5 F9 stabilizer computation is in a separate companion script.",
       "parts":parts}
if __name__=="__main__":
    d=build();OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":d["status"],"summary":{
      k:{x:d["parts"][k][x]for x in
         (["status"] if k!="finite_quantum_clock" else ["status","Pauli_direction_indices"])}
      for k in d["parts"]}},sort_keys=True))
