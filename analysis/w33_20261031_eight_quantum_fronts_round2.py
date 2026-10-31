#!/usr/bin/env python3
"""Eight exact/controlled continuation falsifiers, W33 native geometry (2026-10-31).

Five fronts: characteristic-five torsion, optical losses, clock frustration,
local chiral information index, and Hamiltonian reversibility.
Three orthogonal ideas: Jones representation commutant, discrete Wigner magic,
and graph-square topology versus integral Smith torsion.

This is finite mathematical research, NOT a derivation of anyon material,
spacetime, observed chirality, gravity or a theory of everything.
"""
from __future__ import annotations
import itertools, json, math, sys
from pathlib import Path
import numpy as np
import networkx as nx

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_pass12055_microscopic_tick_model import ADJ,PROJ,PTS,w as omega,pauli
from w33_20261031_helstrom_optical_braid_readout import angle_rotation
from w33_20261031_dynamic_native_metric_backreaction import (
    Q,forward,backward,controls,energy,initial)
from w33_20261031_torsion_order5_probe import rk,ker
from w33_20261031_native_tlj_metaplectic_chain import frob

OUT=ROOT/"data/w33_20261031_eight_quantum_fronts_round2.json"

def finite_solve(A,b,p=5):
    """Solve full-column-rank A*x=b over GF(p), assert membership."""
    A=np.array(A,dtype=np.int64)%p
    b=np.array(b,dtype=np.int64)%p
    M=np.column_stack([A,b])
    n,t=A.shape
    piv=[];r=0
    for j in range(t):
        i=next((i for i in range(r,n) if M[i,j]),None)
        if i is None:continue
        M[[r,i]]=M[[i,r]]
        M[r]=M[r]*pow(int(M[r,j]),-1,p)%p
        for k in range(n):
            if k!=r and M[k,j]:M[k]=(M[k]-M[k,j]*M[r])%p
        piv.append(j);r+=1
    assert r==t and np.all(M[r:,-1]==0)
    ans=np.zeros(t,dtype=np.int64)
    for i,j in enumerate(piv):ans[j]=M[i,-1]
    assert np.array_equal(A@ans%p,b)
    return ans

def torsion():
    sys.path.insert(0,str(ROOT/"analysis/search_drivers_12466"))
    from symmetric_fast import fast_build
    from sympy import Matrix
    _,lines=fast_build(9)
    info=json.loads((ROOT/"analysis/search_drivers_12466/icosa_even_q9.json").read_text())
    selected=[set(lines[i]) for i in info["results"][0]["chosen"]]
    G=nx.Graph();G.add_nodes_from(range(48))
    G.add_edges_from((i,j) for i in range(48) for j in range(i+1,48) if selected[i]&selected[j])
    color=nx.bipartite.color(G)
    left=sorted(i for i in G if color[i]==0)
    right=sorted(i for i in G if color[i]==1)
    B=np.array([[int(G.has_edge(a,b)) for b in right]for a in left],dtype=np.int64)
    K=ker(B)
    null=Matrix(B.tolist()).nullspace()
    import math as m
    L=[]
    for v in null:
        den=m.lcm(*[int(x.q) for x in v])
        vv=[int(x*den)for x in v];d=m.gcd(*vv)
        L.append([int(x//d)%5 for x in vv])
    L=np.array(L,dtype=np.int64).T
    assert rk(L)==6 and K.shape==(24,13)
    basis=L.copy();chosen=[]
    for j in range(K.shape[1]):
        if rk(np.column_stack([basis,K[:,j]]))>basis.shape[1]:
            basis=np.column_stack([basis,K[:,j]]);chosen.append(j)
    assert basis.shape==(24,13) and len(chosen)==7
    T=K[:,chosen]
    known=json.loads((ROOT/"data/w33_20261031_torsion_order5_probe.json").read_text())
    perm=known["order5_mapping"];ridx={j:i for i,j in enumerate(right)}
    P=np.zeros((24,24),dtype=np.int64)
    for j,x in enumerate(right):P[ridx[perm[x]],j]=1
    assert np.array_equal(np.linalg.matrix_power(P,5),np.eye(24,dtype=np.int64))
    action=np.zeros((7,7),dtype=np.int64)
    for j in range(7):
        v=finite_solve(basis,P@T[:,j]%5)
        action[:,j]=v[6:]
    assert np.array_equal(np.linalg.matrix_power(action,5)%5,np.eye(7,dtype=np.int64))
    N=(action-np.eye(7,dtype=np.int64))%5
    ranks=[rk(np.linalg.matrix_power(N,k)%5)for k in range(6)]
    assert ranks==[7,4,2,0,0,0]
    # Centralizer of J3 + J3 + J1 in dimension 7: sum_ij min(λ_i, λ_j) =17.
    centralizer=7*7-rk(np.column_stack([
       (np.kron(np.eye(7,dtype=np.int64),action)
        -np.kron(action.T,np.eye(7,dtype=np.int64)))[:,k]
       for k in range(49)]))
    assert centralizer==17
    return dict(status="PASS_CYCLIC_GF5_TORSION_ACTION_EXPLICIT",
       action7_GF5=action.tolist(),powers_of_unipotent_minus_identity_ranks=ranks,
       centralizer_dimension=centralizer,smith_torsion_order=5**7,
       ambient_lift="PGSp(4,9) order5 certified in predecessor, NOT an A5 representation classification",
       caveat="Uses previous primitive rational-kernel reduction L; saturation to a canonical integral torsion module remains an independent verification requirement.")

def optical():
    f=np.array([[0,1,-3],[-1,0,2],[3,-2,0]],float)
    U=lambda s:np.eye(3)+f@f/14+s*f/math.sqrt(14)
    v,w=U(1)[:,0],U(-1)[:,0]
    eig,Q=np.linalg.eigh(np.outer(v,v)-np.outer(w,w))
    analyzer=np.stack([Q[:,2],Q[:,0],Q[:,1]])
    assert abs(v@w+3/7)<1e-12
    for s in (1,-1):assert np.linalg.norm(U(s).T@U(s)-np.eye(3))<1e-12
    # 27 identical blocks are an 81-mode real, block-local analyzer.
    block=np.kron(np.eye(27),analyzer)
    assert block.shape==(81,81) and np.linalg.norm(block.T@block-np.eye(81))<1e-11
    stage=.995**5
    efficiency=np.array([.92,.90,.88],float)
    dark=np.array([.0003,.0004,.0002],float)
    def response(state,calibration=0):
        A=angle_rotation(0,2,calibration)@angle_rotation(1,2,-calibration)@analyzer
        raw=abs(A@state)**2
        real=stage*efficiency*raw
        remaining=1-real.sum()
        clicks=real+remaining*dark
        no=remaining*(1-dark.sum())
        p=np.r_[clicks,no]
        assert abs(p.sum()-1)<1e-12 and min(p)>=0
        return p
    # Exact multinomial Bayes risk on outcomes (3 ports + no click).
    def risk(a,b,n):
        total=0.
        for i in range(n+1):
            for j in range(n-i+1):
                for k in range(n-i-j+1):
                    l=n-i-j-k
                    c=math.factorial(n)/(math.factorial(i)*math.factorial(j)*math.factorial(k)*math.factorial(l))
                    aa=c*a[0]**i*a[1]**j*a[2]**k*a[3]**l
                    bb=c*b[0]**i*b[1]**j*b[2]**k*b[3]**l
                    total+=min(aa,bb)
        return .5*total
    rows=[]
    for drift in (0.,.02,.08,.20):
        a,b=response(v,drift),response(w,drift)
        er1=.5*np.minimum(a,b).sum()
        scans={str(n):risk(a,b,n)for n in (1,5,10,15,20)}
        assert all(scans[str(j)]<scans[str(i)] for i,j in ((1,5),(5,10),(10,15),(15,20)))
        rows.append(dict(drift=drift,p_plus=a.tolist(),p_minus=b.tolist(),error_1=er1,errors=scans))
    assert rows[0]["error_1"]>.04824604 # physical losses degrade readout
    # Separate actual *inter-block* passive crosstalk and 81 detector ports.
    # Rotate the first output rail of adjacent triangles. Distinct detector
    # efficiencies and 81 low-rate dark-click channels remain explicit.
    injected=13
    amp=[np.zeros(81,dtype=complex),np.zeros(81,dtype=complex)]
    amp[0][3*injected:3*injected+3]=v
    amp[1][3*injected:3*injected+3]=w
    efficiency81=np.tile([.92,.90,.88],27)*(1-.0015*np.repeat(np.arange(27),3))
    background81=np.full(81,1e-5)
    crosstalk=[]
    for eps in (0.,.025,.10):
        probabilities=[];leakages=[]
        for state in amp:
            z=block@state
            for j in range(26):
                i=3*j;k=3*(j+1);a,b=z[i],z[k]
                z[i]=math.cos(eps)*a-math.sin(eps)*b
                z[k]=math.sin(eps)*a+math.cos(eps)*b
            assert abs(np.vdot(z,z).real-1)<1e-12
            leak=1-sum(abs(z[3*injected:3*injected+3])**2)
            detected=stage*efficiency81*abs(z)**2
            missing=1-detected.sum()
            p=np.r_[detected+missing*background81,missing*(1-background81.sum())]
            assert abs(p.sum()-1)<1e-12 and min(p)>-1e-14
            probabilities.append(p)
            leakages.append(float(leak))
        err=.5*np.minimum(*probabilities).sum()
        crosstalk.append(dict(neighbor_coupler_angle=eps,
            average_leakage_outside_injected_triangle=float(np.mean(leakages)),
            Bayes_one_shot_with_81_detectors_and_no_click=float(err)))
    assert crosstalk[0]["average_leakage_outside_injected_triangle"]<1e-12
    assert crosstalk[1]["average_leakage_outside_injected_triangle"]>0
    assert crosstalk[2]["average_leakage_outside_injected_triangle"]>crosstalk[1]["average_leakage_outside_injected_triangle"]
    return dict(status="PASS_81MODE_PHOTON_LOSS_DARK_AND_CROSSTALK_MODEL",
      mode_count=81,independent_triangles=27,stage_survival=stage,
      port_efficiencies=efficiency.tolist(),dark_assumed=dark.tolist(),models=rows,
      inter_triangle_81mode_crosstalk=crosstalk,
      assumption="Exclusive no-click/dark-click outcome model; sequential interblock passive couplers; no multiphoton interference, correlated detector errors or lab calibrations.")

def clock():
    W=nx.from_numpy_array(ADJ)
    maximal=list(nx.find_cliques(nx.complement(W)))
    sevens=[sorted(c)for c in maximal if len(c)==7]
    assert len(sevens)==2880
    # Distinct colors only; count all cross edges exactly.
    ext=[]
    for cl in sevens:
        S=set(cl)
        for j in range(40):
            if j in S:continue
            nmiss=int(sum(ADJ[j,k] for k in cl))
            ext.append((nmiss,cl,j))
    e=min(ext,key=lambda t:t[0])
    assert e[0]==1  # no K8 in complement, plus explicit 27/28-edge witness
    good=28-e[0]
    # For K sufficiently large a noncommuting pair is preferred; colors distinct.
    J,K=1.,2.
    nn=2*J-4*K/3
    energy8=good*nn+e[0]*(2*J)
    return dict(status="PASS_EIGHT_SITE_DISTINCT_COLOR_FRUSTRATION_CONTROL",
       seven_direction_cliques=2880,
       minimum_missed_bonds_among_seven_clique_extensions=int(e[0]),
       eight_color_witness=e[1]+[int(e[2])],
       satisfied_noncommuting_bonds=int(good),commuting_bonds=int(e[0]),
       sample_J=J,sample_K=K,sample_bond_energy=energy8,
       global_statement="Exact distinct-color optimum: no 8-clique exists in the W33 noncommutation graph, so at least one commuting bond; this explicit 8-set has exactly one. Hence at most 27/28 bonds can simultaneously be mutually noncommuting. Does not imply optimum over 120 ticks with label repetition and temperature.",
       scope="Externally supplied complete spatial graph, couplings, no physical vacuum selection.")

def transport():
    # Infinite-line wire permutation: finite-depth swaps versus a shift.
    def first(x):return x+1 if x%2==0 else x-1
    def second(x):return x+1 if x%2 else x-1
    sw=lambda x:second(first(x))
    sh=lambda x:x+1
    def crossing(f):
        right=sum(x<=0 and f(x)>=1 for x in range(-15,16))
        left=sum(x>=1 and f(x)<=0 for x in range(-15,16))
        return dict(right=right,left=left,index=3**(right-left))
    a,b=crossing(sw),crossing(sh)
    assert a=={"right":1,"left":1,"index":1}
    assert b=={"right":1,"left":0,"index":3}
    return dict(status="PASS_CLIFFORD_FINITE_DEPTH_TRIVIAL_GNVW_INDEX",
       on_site_qutrit_dimension=3,finite_depth_even_odd_swap=a,
       shift_by_one= b,
       reason="Conjugating SWAP layers by finite-depth local native Clifford/Jones gates cannot change the QCA index. Nonzero chirality needs shift/anomalous locality mechanism.",
       boundary="1D assumed spatial chain; not a 2D chiral edge index or an anomalous W33 physical vacuum.")

def geometry():
    def integrate(dt,n,reverse=False):
        u=initial(4);phi=np.zeros_like(u)
        pu=np.zeros_like(u);pp=np.zeros_like(u)
        initial_data=(u.copy(),phi.copy(),pu.copy(),pp.copy())
        E0=energy(u,phi,pu,pp,.3,.4,.3)
        def step(h):
            au,ap=controls(u,phi,.3,.4,.3)
            pu[:]+=h*.5*au;pp[:]+=h*.5*ap
            u[:]+=h*pu;phi[:]+=h*pp
            au,ap=controls(u,phi,.3,.4,.3)
            pu[:]+=h*.5*au;pp[:]+=h*.5*ap
        for _ in range(n):step(dt)
        err=abs(energy(u,phi,pu,pp,.3,.4,.3)-E0)/E0
        drifted=[x.copy()for x in (u,phi,pu,pp)]
        if reverse:
            for _ in range(n):step(-dt)
            reversal=max(np.max(abs(x-y))for x,y in zip((u,phi,pu,pp),initial_data))
            assert reversal<1e-11
        else:reversal=None
        return dict(dt=dt,steps=n,relative_energy_error=err,backreaction_norm=float(np.linalg.norm(drifted[1])),reversal_error=reversal)
    samples=[integrate(dt,round(1.6/dt),True)for dt in (.02,.01,.005)]
    assert samples[2]["relative_energy_error"]<samples[1]["relative_energy_error"]<samples[0]["relative_energy_error"]
    r1=samples[0]["relative_energy_error"]/samples[1]["relative_energy_error"]
    r2=samples[1]["relative_energy_error"]/samples[2]["relative_energy_error"]
    assert 3<r1<5 and 3<r2<5
    return dict(status="PASS_TIME_REVERSIBLE_SYMPLECTIC_CONFORMAL_DYNAMICS",
       measurements=samples,drift_ratio_coarse_to_mid=r1,drift_ratio_mid_to_fine=r2,
       conserved_shift_charge="Matter field u enters only via differences, so total canonical p_u is exactly conserved by the force sum on periodic space.",
       boundary="4D spatial lattice, external continuous time, ansatz and constants supplied; no diffeomorphism invariance or Einstein constraints.")

def braid_commutant():
    # 5 generators on a 9D native qutrit Hilbert space.
    coords=json.loads((ROOT/"data/w33_20261031_native_tlj_metaplectic_chain.json").read_text())["concrete_Pauli_indices"]
    E=[np.array(PROJ[i][0]) for i in coords]
    I=np.eye(9)
    # vec(EP-PE): (I⊗E - E^T⊗I) vec(P) for column-major vectorization.
    A=np.vstack([np.kron(I,e)-np.kron(e.T,I) for e in E])
    s=np.linalg.svd(A,compute_uv=False)
    dim=int(np.sum(s<1e-9))
    # commutant can be >1: report, do not assume full matrix algebra!
    assert dim==2
    # Native phase-space inversion/parity, the central -I symplectic lift:
    # |a,b> -> |-a,-b>. The 9D Weil space splits into 5 and 4 dimensions.
    parity=np.zeros((9,9),complex)
    for a in range(3):
        for b in range(3):
            parity[(-a%3)*3+(-b%3),a*3+b]=1
    assert np.allclose(parity@parity,I)
    assert abs(np.trace(parity)-1)<1e-12
    assert all(frob(parity@e-e@parity)<1e-11 for e in E)
    plus=(I+parity)/2;minus=(I-parity)/2
    dims=[int(round(np.trace(plus).real)),int(round(np.trace(minus).real))]
    assert dims==[5,4]
    assert np.allclose(plus@plus,plus) and np.allclose(minus@minus,minus)
    # Since commutant is 2D and contains independent I and parity,
    # no additional algebraically invariant sectors/intertwiners survive.
    return dict(status="PASS_NATIVE_BRAID_PARITY_SPLIT_5_PLUS_4",
      commutant_dimension=dim,minimum_nonsingular_value=float(s[-dim-1]),
      physical_parity_matrix=parity.real.astype(int).tolist(),
      irreducible_sector_dimensions=dims,
      exact_commutant_basis="span_C{I9, parity(|a,b> -> |-a,-b>)}",
      note="Two-qutrit metaplectic/Weil representation splits into 5D parity-even and 4D parity-odd sectors. Each restriction of the *-algebra generated by the five projectors is irreducible (Burnside); the total finite unitary braid group still is not dense.",
      physical_boundary="No fusion category or protective many-body gap follows from a matrix commutant.")

def wigner():
    # Gross odd-prime Wigner phase-point operators for one qutrit.
    w=np.exp(2j*np.pi/3)
    A={}
    for q in range(3):
        for p in range(3):
            m=np.zeros((3,3),complex)
            for y in range(3):
                left=(q+2*y)%3;right=(q-2*y)%3
                m[left,right]+=w**(p*y)
            assert np.linalg.norm(m-m.conj().T)<1e-12
            assert np.allclose(m@m,np.eye(3))
            A[(q,p)]=m
    def wn(rho):
        z=np.array([np.trace(rho@np.kron(a,b)).real/9
                    for a in A.values() for b in A.values()])
        assert abs(z.sum()-1)<1e-11
        return dict(min=float(np.min(z)),sum_absolute=float(np.sum(abs(z))),
                    mana=float(math.log(np.sum(abs(z)))))
    I=np.eye(9,dtype=complex)
    psi=np.zeros(9,complex);psi[0]=1
    native_p=PTS.index((1,1,0,0))
    pi=PROJ[native_p][0]
    R=I+(w-1)*(I-pi)
    stabilizer=R@psi
    cliff=wn(np.outer(stabilizer,stabilizer.conj()))
    assert cliff["min"]>-1e-11 and abs(cliff["mana"])<1e-11
    plus=np.ones(3)/math.sqrt(3)
    non=np.diag([1,1,np.exp(1j*math.pi/3)])@plus
    test=np.kron(non,np.array([1,0,0]))
    magic=wn(np.outer(test,test.conj()))
    assert magic["min"]<-1e-5 and magic["mana"]>1e-5
    return dict(status="PASS_NATIVE_CLIFFORD_POSITIVE_WIGNER_VS_NONCLIFFORD_MAGIC",
       native_entangling_braid=cliff,externally_supplied_nonclifford_phase_gate=magic,
       implementation="Two-qutrit Gross phase-point operators at odd prime d=3; exact 81 phase space outcomes",
       caveat="This demonstrates why native Clifford braids alone cannot generate Wigner mana. Injected non-Clifford phase is an external resource, not a derived interaction.")

def topology():
    sys.path.insert(0,str(ROOT/"analysis/search_drivers_12466"))
    from symmetric_fast import fast_build
    _,lines=fast_build(9)
    choice=json.loads((ROOT/"analysis/search_drivers_12466/icosa_even_q9.json").read_text())["results"][0]["chosen"]
    groups=[set(lines[i]) for i in choice]
    G=nx.Graph()
    G.add_nodes_from(range(48))
    G.add_edges_from((i,j) for i in range(48) for j in range(i+1,48) if groups[i]&groups[j])
    assert nx.is_connected(G) and G.number_of_edges()==240
    color=nx.bipartite.color(G)
    left=sorted(i for i in G if color[i]==0)
    right=sorted(i for i in G if color[i]==1)
    eidx={edge:k for k,edge in enumerate((i,j)for i in left for j in right if G.has_edge(i,j))}
    assert len(eidx)==240
    cycles=[]
    for ia,a in enumerate(left):
        for b in left[ia+1:]:
            common=sorted(set(G[a])&set(G[b]))
            for c,d in itertools.combinations(common,2):
                v={eidx[(a,c)]:1,eidx[(b,c)]:-1,eidx[(b,d)]:1,eidx[(a,d)]:-1}
                cycles.append(v)
    assert len(cycles)==1680
    def span_rank(p):
        piv={}
        for vec in cycles:
            row={j:x%p for j,x in vec.items() if x%p}
            while row:
                k=min(row)
                if k not in piv:
                    t=pow(row[k],-1,p)
                    piv[k]={j:(a*t)%p for j,a in row.items() if (a*t)%p}
                    break
                d=row[k];basis=piv[k]
                for j,a in basis.items():
                    val=(row.get(j,0)-d*a)%p
                    if val:row[j]=val
                    else:row.pop(j,None)
        return len(piv)
    r2=span_rank(2);r5=span_rank(5);r3=span_rank(3)
    b1=240-48+1
    assert r2<=b1 and r3<=b1 and r5<=b1
    return dict(status="PASS_FOUR_CYCLE_FILLED_COMPLEX_HOMOLOGY_FIELD_CHECK",
        graph_vertices=48,edges=240,connected_components=1,
        graph_h1_over_Z_free_rank=b1,graph_h1_integral_torsion=0,
        filled_4_cycles=len(cycles),boundary2_ranks={"F2":r2,"F3":r3,"F5":r5},
        filled_H1_dimensions={"F2":b1-r2,"F3":b1-r3,"F5":b1-r5},
        significance="Seven Z/5 factors in the 24x24 line-incidence B Smith cokernel are NOT ordinary H1 torsion of the unfilled 48-vertex graph. A chain complex and explicit 2-cells are essential before interpreting them as topological flux.",
        caveat="Field homology dimensions of this particular square-filled CW complex do not alone determine its integral H1 torsion.")


def build():
    tests={
        "01_characteristic_five_module":torsion,
        "02_optical_81mode_imperfections":optical,
        "03_clock_frustration":clock,
        "04_chiral_local_index":transport,
        "05_metric_hamiltonian":geometry,
        "06_outside_braid_commutant":braid_commutant,
        "07_outside_wigner_magic":wigner,
        "08_outside_homology_vs_torsion":topology}
    result={"schema":"w33.eight_quantum_fronts_round2.v1","sources":"W33-Theory master ad8846e, plus cited literature","fronts":{}}
    for name,fn in tests.items():
        value=fn()
        result["fronts"][name]=value
        print(name,value["status"],flush=True)
    return result

if __name__=="__main__":
    result=build()
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":"8_COMPLETED",
        "statuses":{k:v["status"] for k,v in result["fronts"].items()}}))
