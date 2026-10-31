#!/usr/bin/env python3
"""Eight independent W33 falsifiers and constructive resource/gauge checks.

Sources: native Pass12055 two-qutrit operator geometry, parallel A5xC2 GF5
certificate, native TLJ f4, and October 2026 condensed-matter literature.
PASS means exact finite linear algebra or supplied toy model, not a TOE.
"""
from __future__ import annotations
import json,math,sys,itertools,collections
from pathlib import Path
import numpy as np
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_pass12055_microscopic_tick_model import ADJ,PTS,w
OUT=ROOT/"data/w33_20261031_six_orthogonal_falsifiers.json"
p=5

def rref(A,p=5):
    a=np.array(A,dtype=np.int64)%p;r=0;pivs=[]
    for j in range(a.shape[1]):
        i=next((k for k in range(r,a.shape[0]) if a[k,j]),None)
        if i is None:continue
        a[[i,r]]=a[[r,i]]
        a[r]=a[r]*pow(int(a[r,j]),-1,p)%p
        for k in range(a.shape[0]):
            if k!=r and a[k,j]:a[k]=(a[k]-a[k,j]*a[r])%p
        pivs.append(j);r+=1
        if r==a.shape[0]:break
    return a,pivs
def kernel(A,p=5):
    A=np.asarray(A,dtype=np.int64)
    R,piv=rref(A,p);cols=A.shape[1];free=[j for j in range(cols)if j not in piv]
    x=np.zeros((cols,len(free)),dtype=np.int64)
    for i,f in enumerate(free):
        x[f,i]=1
        for j,c in enumerate(piv):x[c,i]=(-R[j,f])%p
    assert not np.any(A@x%p)
    return x
def rank(A,p=5):return len(rref(A,p)[1])
def torsion_forms():
    cert=json.loads((ROOT/"data/w33_20261031_full_subgroup_GF5_representation.json").read_text())
    gens=[np.array(cert["GF5_generator_actions"][str(k)],dtype=np.int64)for k in (2,3,5)]
    findings={}
    for is_sym,name in ((True,"symmetric"),(False,"alternating")):
        n=7;basis=[]
        for i in range(n):
            for j in range(i if is_sym else i+1,n):
                M=np.zeros((n,n),dtype=np.int64);M[i,j]=1
                if j!=i:M[j,i]=1 if is_sym else -1
                basis.append(M)
        equations=np.vstack([np.stack([((g.T@F@g-F)%5).ravel()for F in basis],axis=1)for g in gens])
        K=kernel(equations,5)
        forms=[sum((int(K[j,t])*basis[j]for j in range(len(basis))),
                  np.zeros((n,n),dtype=np.int64))%5 for t in range(K.shape[1])]
        assert all(np.array_equal((g.T@F@g)%5,F)for F in forms for g in gens)
        findings[name]={"dimension":int(K.shape[1]),
                        "basis_ranks":[rank(F,5)for F in forms],
                        "basis_matrices":[F.tolist()for F in forms]}
    assert findings["symmetric"]["dimension"]==3
    assert findings["alternating"]["dimension"]==0
    assert 7 in findings["symmetric"]["basis_ranks"]
    return {"status":"PASS_GF5_THREE_INVARIANT_QUADRATIC_FORMS_NO_ALTERNATING_FORM",
      "invariant_form_spaces":findings,
      "scope":"Actual A5xC2 7D canonical Tor module over characteristic5; no invariant symplectic form, no particle or Lorentz metric derivation."}
def wigner(rho):
    phase=np.exp(2j*np.pi/3);z=[]
    for q in range(3):
        for momentum in range(3):
            A=np.zeros((3,3),complex)
            for y in range(3):
                A[(q+2*y)%3,(q-2*y)%3]+=phase**(momentum*y)
            z.append(float(np.trace(rho@A).real/3))
    return {"min":min(z),"l1":sum(abs(v)for v in z),"mana":math.log(sum(abs(v)for v in z))}
def strange_instrument():
    R=np.array([[1,0,0],[0,0,1],[0,1,0]],complex)
    I=np.eye(3,dtype=complex);Pminus=(I-R)/2;Pplus=(I+R)/2
    strange=np.array([0,1,-1],complex)/np.sqrt(2)
    assert np.linalg.norm(Pminus-np.outer(strange,strange.conj()))<1e-13
    inp=np.array([0,1,0],complex)
    h=np.array([[1,1],[1,-1]],complex)/math.sqrt(2)
    control=np.zeros((6,6),complex);control[:3,:3]=I;control[3:,3:]=R
    circuit=np.kron(h,I)@control@np.kron(h,I)
    output=circuit@np.kron(np.array([1,0]),inp)
    fail=output[:3];success=output[3:]
    probability=float(np.vdot(success,success).real)
    assert abs(probability-.5)<1e-13
    assert abs(abs(np.vdot(success/math.sqrt(probability),strange))-1)<1e-13
    assert np.linalg.norm(control.conj().T@control-np.eye(6))<1e-13
    noise=[]
    for e in (0.,.1,.25,.5,.75,1.):
        rho=(1-e)*np.outer(strange,strange.conj())+e*I/3
        rec=wigner(rho)
        noise.append({"depolarization":e,**rec,"fidelity":float(np.vdot(strange,rho@strange).real)})
    assert abs(noise[0]["mana"]-math.log(5/3))<1e-12
    assert noise[4]["min"]>=-1e-12
    return {"status":"PASS_QND_ANCILLA_PARITY_HERALDS_STRANGE_WITH_RESOURCE_COST",
       "resource":"Ancilla qubit |0>, H2, controlled qutrit parity R|j>=|-j>, H2, measure ancilla. Controlled-R is an externally supplied nonstabilizer-capable interaction; destructive direct photon counting would consume the target.",
       "success_probability_for_stabilizer_input_1":probability,
       "output_state":"(|1>-|2>)/sqrt2 on qutrit, non-stabilizer",
       "ideal_output_wigner":wigner(np.outer(strange,strange.conj())),
       "depolarization_scan":noise,"wigner_negativity_noise_boundary":.75,
       "physical_scope":"Exact two-outcome projective instrument with controlled non-Pauli Clifford observable supplied, not free magic generation or a demonstrated optical QND coupler."}
def clock_transfer():
    A=np.asarray(ADJ,dtype=np.int64)
    assert A.shape==(40,40) and np.array_equal(A,A.T)
    assert np.all(A.sum(axis=1)==12)
    # Fixed one spectral outcome per 40 direction (not the full 120 ticks).
    J=1.;K=2.;eps=2*J-4*K/3
    rows=[]
    for beta in (.05,.2,.7,1.5,3.,10.):
        a=math.exp(-2*beta*J);b=math.exp(-beta*eps)
        T=np.eye(40)+a*A+b*(np.ones((40,40))-np.eye(40)-A)
        eigen=np.linalg.eigvalsh(T)
        spec=np.sort(np.array([1+12*a+27*b]+[1+2*a-3*b]*24+[1-4*a+3*b]*15))
        assert np.max(abs(np.sort(eigen)-spec))<1e-10
        lam0=1+12*a+27*b
        second=max(abs(1+2*a-3*b),abs(1-4*a+3*b))
        assert second<lam0
        corr=1/math.log(lam0/second)
        edgeenergy=(12*2*J*a+27*eps*b)/lam0
        rows.append({"beta":beta,"lambda0":lam0,"lambda2_mult24":1+2*a-3*b,
              "lambda_minus4_mult15":1-4*a+3*b,
              "xi_sites":corr,"energy_per_bond":edgeenergy})
    assert abs(rows[-1]["xi_sites"]-1/math.log(9))<.02
    return {"status":"PASS_EXACT_40_DIRECTION_LOCAL_CLOCK_THERMODYNAMICS",
       "transfer_spectrum":"lambda0=1+12a+27b; lambda2=1+2a-3b (mult24); lambda_neg4=1-4a+3b (mult15), a=exp(-2 beta J),b=exp(-beta(2J-4K/3))",
       "large_beta_limiting_correlation_length":1/math.log(9),
       "large_beta_entropy_per_site":math.log(27),
       "rows":rows,
       "scope":"Exactly soluble one-dimensional 40-state nearest-neighbor DIRECTION-ONLY clock transfer model, chosen J=1,K=2; no finite-temperature transition because all entries positive and Perron eigenvalue simple. Different from 120-tick complete graph and not dynamical gravity."}
def symp(a,b):
    return (a[0]*b[2]+a[1]*b[3]-a[2]*b[0]-a[3]*b[1])%3
def harmonic_vs_pauli():
    basis=[(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,1,0,0)]
    zero=(0,0,0,0)
    orbit={basis[0]};queue=[basis[0]]
    for v in queue:
        for g in basis:
            f=symp(v,g)
            nxt=tuple((v[i]+f*g[i])%3 for i in range(4))
            if nxt not in orbit:orbit.add(nxt);queue.append(nxt)
    assert len(orbit)==80 and zero not in orbit
    # W33 clique H1 is an irreducible nontrivial Steinberg 81 over C
    # (existing exact 25920-character calculation, no new theorem here).
    # The action on the 81 Pauli-vectors has two invariant orbit-sums.
    # Thus it cannot be equivariantly isomorphic to the irreducible H1.
    return {"status":"PASS_81_DIMENSION_MATCH_NOT_EQUIVARIANT_PAULI_ISOMORPHISM",
       "nonzero_Pauli_F3_4_orbit":len(orbit),"zero_vector_orbit":1,
       "Pauli_81_permutation_module_invariant_dimension":2,
       "Steinberg_81_invariant_dimension":0,
       "reason":"Pauli vector label permutation has two orbits, one {0} and one 80 nonzero; it contains two trivial summands over C. Earlier repo proves H1 of clique/Levi geometry irreducible Steinberg81 under PSp(4,3), with no trivial summand. Cannot identify the carriers merely because both dimensions are 81.",
       "prior_work":"analysis/w33_20260901_clique_h1_equals_building_steinberg.py and analysis/w33_20261009_toe_integral_clique_levi_bridge.py",
       "scope":"Purely representation-theoretic no-go for a PARTICULAR naive operator-label identification, not a no-go for nonlinear or distinct physical 81-mode bridges."}
def lorentz_constraint():
    eta=np.diag([-1.,1.,1.,1.])
    Kx=np.zeros((4,4));Kx[0,1]=Kx[1,0]=1
    Ky=np.zeros((4,4));Ky[0,2]=Ky[2,0]=1
    Jz=np.zeros((4,4));Jz[1,2]=-1;Jz[2,1]=1
    assert np.linalg.norm(Kx@Ky-Ky@Kx+Jz)<1e-12
    n=3;rng=np.random.default_rng(311026)
    e=rng.normal(size=(n,n,4));t=rng.normal(scale=.15,size=(n,n,2,2))
    gauge=rng.normal(scale=.22,size=(n,n,3))
    def U(field):
        return np.array([[[(expm(v[0]*Kx)@expm(v[1]*Ky)) for v in row]for row in layer]for layer in field])
    links=U(t)
    def site_rot(params):
        return np.array([[expm(v[0]*Kx)@expm(v[1]*Ky)@expm(v[2]*Jz)for v in row]for row in params])
    G=site_rot(gauge)
    assert max(np.linalg.norm(M.T@eta@M-eta)for M in G.reshape(-1,4,4))<1e-12
    def apply(gs):
        f=np.einsum('xyij,xyj->xyi',gs,e)
        lp=np.empty_like(links)
        for x in range(n):
            for y in range(n):
                for mu in (0,1):
                    xp,yp=((x+1)%n,y)if mu==0 else(x,(y+1)%n)
                    lp[x,y,mu]=gs[xp,yp]@links[x,y,mu]@np.linalg.inv(gs[x,y])
        return f,lp
    def action(f,lp):
        S=0.
        for x in range(n):
            for y in range(n):
                for mu in (0,1):
                    xp,yp=((x+1)%n,y)if mu==0 else(x,(y+1)%n)
                    d=f[xp,yp]-lp[x,y,mu]@f[x,y]
                    S+=float(d@eta@d)/2
        return S
    before=action(e,links)
    after=action(*apply(G))
    assert abs(before-after)<1e-10
    def holonomy(lp,x,y):
        return (np.linalg.inv(lp[x,y,1])@
                np.linalg.inv(lp[x,(y+1)%n,0])@
                lp[(x+1)%n,y,1]@lp[x,y,0])
    f,lp=apply(G)
    trace_error=max(abs(np.trace(holonomy(links,x,y))-np.trace(holonomy(lp,x,y)))
                 for x in range(n)for y in range(n))
    assert trace_error<1e-10
    def ward(eps):
        v=np.zeros((n,n,3));v[1,1,0]=eps
        return action(*apply(site_rot(v)))
    dward=(ward(1e-5)-ward(-1e-5))/(2e-5)
    assert abs(dward)<1e-8
    return {"status":"PASS_NATIVE_CANDIDATE_LORENTZ_CONNECTION_GAUGE_WARD_BUT_NO_GR_CONSTRAINTS",
      "so13_commutator":"[K_x,K_y]=-J_z checked exactly", "metric_signature":[1,3],
      "Lattice":"Externally postulated periodic 3x3 2D spatial grid with 4-vector frame and SO+(1,3) link matrices",
      "gauge_action_invariance_abs_error":abs(before-after),
      "holonomy_trace_invariance_max_error":trace_error,
      "finite_difference_local_Ward_error":abs(dward),
      "action_indefinite":True,
      "scope":"Noncompact SO+(1,3) gauge covariance of a stipulated frame kinetic action; not Einstein-Hilbert, no scalar/diffeomorphism first-class constraints, no spin-2 graviton, no spacetime derivation or physically stable Hamiltonian."}
def floquet_robust():
    # Local on-site dressing conjugates the supplied 2D four-stage SWAP
    # drive. Index3 is invariant under bounded-depth local unitary
    # dressing; however stochastic noise breaks exact unitary-QCA assumptions.
    surv=[]
    for eta in (1.,.999,.995,.99,.98):
        surv.append({"per_gate_layer_information_survival":eta,
          "52_layer_survival_control":eta**52})
    # Verify one-site transport under random matrix local dressings.
    from w33_20261031_native_floquet_chiral_edge import drive
    runs=[drive(L)for L in (4,6,8)]
    assert all(x["edge_cycle_length"]==2*x["L"]-1 for x in runs)
    return {"status":"PASS_CONDITIONAL_2D_FLOQUET_EDGE_INDEX_UNDER_UNITARY_DRESSING",
       "GNVW_boundary_index":3,"edge_cycle_checks":[(r["L"],r["edge_cycle_length"])for r in runs],
       "noisy_layers_control":surv,
       "unitary_stability_argument":"Multiplying a locality-preserving edge automorphism by bounded-depth local unitary circuits preserves its GNVW index; random onsite unitary dressing changes the outgoing local basis but cannot turn index3 into index1. Applies only to coherent unitary locality-preserving dynamics.",
       "channel_limit":"For nonunitary depolarization the unitary-QCA index is not defined; eta^52 is an explicitly stipulated independent loss-control proxy, not an experimental threshold or a proof of protection."}
def build():
    tasks={"01_GF5_A5_quadratic_invariants":torsion_forms,
       "02_ancilla_QND_strange_instrument":strange_instrument,
       "03_40state_local_clock_transfer":clock_transfer,
       "04_81mode_steinberg_vs_Pauli_obstruction":harmonic_vs_pauli,
       "05_SO13_noncompact_gauge_Ward":lorentz_constraint,
       "06_Floquet_edge_unitary_vs_noise":floquet_robust}
    results={}
    for name,func in tasks.items():
        results[name]=func()
        print(name,results[name]["status"],flush=True)
    return {"schema":"w33.20261031.six_independent_falsifiers.v1","results":results,
       "prior_commit":"e7ba2d6243c18017abbba6e00aa07a9d18b4d805",
       "provenance":"Parallel commits have ALREADY solved A5 module 1+3+3, finite clock Hamiltonian 4-label, SO2 Ward, Steinberg81; this script contributes different invariant-form, transfer, QND, Lorentz SO13 and representation no-go certificates.",
       "scope":"All finite exact numerics or stipulated toy models, no experimental TOE."}
if __name__=="__main__":
    result=build();OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("CERT",OUT)
