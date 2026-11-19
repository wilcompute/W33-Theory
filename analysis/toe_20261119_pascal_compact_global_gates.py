"""Six independent Pascal-H27 compactness, flavor and causal/optical gates.

Mathematically tested finite models only; not a derived G2/TOE, complete
SM spectrum, gravity or fault-tolerant photonic implementation.
"""
from pathlib import Path
from math import pi,sqrt,exp,log,ceil
from fractions import Fraction as Q
import json
import numpy as np
import sympy as s
from scipy.integrate import solve_ivp,simpson

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261119_pascal_compact_global_gates.json"
PHI=(1+sqrt(5))/2

def pascal_gram():
    A=np.array([[1.,0],[1.,1.]])
    P=np.kron(A,A);K=P.T@P
    ev=np.linalg.eigvalsh(K)
    assert np.allclose(ev,[PHI**-4,1.,1.,PHI**4])
    return P,K,ev

def compact():
    P,K,ev=pascal_gram();m0=2.;t=np.linspace(0,2*pi,8192,endpoint=False)
    data=[]
    for lam in ev:
        m=m0-4.5*lam*(1+np.tanh(8*np.sin(t)))
        crosses=int(np.sum(np.signbit(m)!=np.roll(np.signbit(m),1)))
        integral=2*pi*(m0-4.5*lam)
        assert crosses in (0,2)
        assert abs(float(2*pi*m.mean())-integral)<1e-11
        data.append({"lambda":float(lam),"integral_mass":float(integral),
                     "mass_sign_changes":crosses,"left_wall_candidates":crosses//2,
                     "right_antiwall_candidates":crosses//2,
                     "exact_periodic_zero_mode":bool(abs(integral)<1e-10)})
    assert [r["left_wall_candidates"] for r in data]==[0,1,1,1]
    assert sum(r["right_antiwall_candidates"] for r in data)==3
    assert not any(r["exact_periodic_zero_mode"] for r in data)
    return {"noncompact_three_chiral_index":3,"periodic_S1_Fredholm_index":0,
       "circle_at_m0_2_exact_zero_modes":0,
       "left_wall_candidates":3,"right_antiwall_candidates":3,
       "periodic_criterion":"real scalar channel: exp(integral m dz)=1 iff integral m=0; then one D+ and one D+adjoint zero",
       "mass_profiles":"m_lambda(theta)=2−(9lambda/2)[1+tanh(8sin(theta))]",
       "channels":data,
       "qualification":"Noncompact or physical boundary/orbifold/flux defects could evade this specific smooth periodic-circle compactness objection. Sign flips represent candidate localized bound states, not necessarily exact zero modes."}

def overlap():
    P,K,ev=pascal_gram()
    epert=np.linalg.eigvalsh(K+np.diag([0.,.05,0.,0.]))
    L=ev[ev>2/9];LP=epert[epert>2/9]
    assert len(L)==len(LP)==3
    f=lambda z,y:[3*y[0]**2*(1-y[0]**3)]
    neg=solve_ivp(f,(0,-24),[.5],t_eval=np.linspace(0,-24,2501),rtol=2e-11,atol=1e-13)
    pos=solve_ivp(f,(0,8),[.5],t_eval=np.linspace(0,8,1501),rtol=2e-11,atol=1e-13)
    assert neg.success and pos.success
    z=np.r_[neg.t[::-1][:-1],pos.t]
    x=np.r_[neg.y[0][::-1][:-1],pos.y[0]]
    x=np.clip(x,1e-14,1-1e-14)
    force=3*x*x*(1-x**3)
    assert min(force)>0
    def profiles(lams):
        cols=[]
        for lam in lams:
            y=np.exp(np.clip(2*z+lam*np.log(force),-700,500))
            norm=sqrt(float(simpson(y*y,x=z)))
            cols.append(y/norm)
        return np.stack(cols,axis=1)
    A=profiles(L);B=profiles(LP)
    gram=lambda F:simpson(F[:,:,None]*F[:,None,:],x=z,axis=0)
    g0=np.linalg.eigvalsh(gram(A));g1=np.linalg.eigvalsh(gram(B))
    assert g0[0]<1e-10 and min(g1)>0
    sites=[-2.,0.,1.]
    V=np.array([[np.interp(site,z,B[:,j]) for site in sites] for j in range(3)])
    rows=[]
    for i in (1,2,3):
        y=V[:,:i]@V[:,:i].T
        vals=np.linalg.svd(y,compute_uv=False)
        rank=int(np.linalg.matrix_rank(y,tol=1e-10))
        assert rank==i
        rows.append({"contact_count":i,"Y_rank_at_tol_1e_minus10":rank,"Y_singular_values":vals.tolist()})
    return {"mass_offset":2.,"unperturbed_selected_lambdas":L.tolist(),
      "rank_one_split_selected_lambdas":LP.tolist(),
      "unperturbed_profile_Gram_eigenvalues":g0.tolist(),
      "perturbed_profile_Gram_eigenvalues":g1.tolist(),
      "unperturbed_profile_rank":2,"perturbed_profile_rank":3,
      "defect_sites":sites,"defect_rank_census":rows,
      "exact_contact_rank_bound":"rank(sum of r point-contact outer products) <= r",
      "qualification":"Coupling positions, 5D scalar profile, gauge representations and Higgs amplitudes inserted; no observed quark/lepton masses, physical G2 source or compact chiral fermion spectrum."}

def h27_and_anomalies():
    P,K,ev=pascal_gram()
    omega=np.exp(2j*pi/3)
    X=np.roll(np.eye(3),1,axis=1)
    Z=np.diag([1.,omega,omega**2])
    U=np.eye(4,dtype=complex);V=np.eye(4,dtype=complex)
    U[1:,1:]=X;V[1:,1:]=Z
    dx=float(np.linalg.norm(K@U-U@K))
    dz=float(np.linalg.norm(K@V-V@K))
    assert dx>2 and dz>5
    species=[("Q",6,Q(1,6)),("uc",3,Q(-2,3)),("dc",3,Q(1,3)),
             ("L",2,Q(-1,2)),("ec",1,Q(1)),("nc",1,Q(0))]
    u1=sum(dim*y for _,dim,y in species)
    u3=sum(dim*y**3 for _,dim,y in species)
    su2=3*Q(1,2)*Q(1,6)+Q(1,2)*Q(-1,2)
    su3=2*Q(1,2)*Q(1,6)+Q(1,2)*Q(-2,3)+Q(1,2)*Q(1,3)
    assert u1==u3==su2==su3==0
    assert 2*3-3-3==0 and 3*(3+1)%2==0
    return {"4_channel_PascalK2_H27_shift_commutator_norm":dx,
       "4_channel_PascalK2_H27_clock_commutator_norm":dz,
       "unbroken_1_plus_irrep3_H27_equivariant_mass_eigenvalue_pattern":"a,b,b,b (Schur lemma); actual phi^-4,1,1,phi^4",
       "local_SM_anomalies_for_complete_Spin10_16":["U1^3=0","SU2^2U1=0","SU3^2U1=0","gravity^2U1=0","SU3^3=0"],
       "Witten_doublets_three_complete_16":12,
       "qualification":"Only if physical 4-channel representation is H27 1⊕3. A broken-symmetry background may generate noninvariant K2 but requires sourced covariant couplings. Complete 16 anomaly ledger is not proof of 5D inflow or actual chiral matter."}

def pascal_graph():
    rows=[]
    for L in range(1,8):
        N=2**L
        P=np.array([[int((j & ~i)==0) for j in range(N)] for i in range(N)])
        A=np.logical_or(P,P.T).astype(int)
        np.fill_diagonal(A,0)
        degrees=A.sum(0)
        expected=np.array([2**i.bit_count()+2**(L-i.bit_count())-2 for i in range(N)])
        assert np.array_equal(degrees,expected)
        assert int(A.sum()//2)==3**L-2**L
        assert degrees[0]==degrees[-1]==N-1
        if L>=2:
            assert A[1,2]==0
            assert np.all(A@A+A+np.eye(N)>0)
        lap=np.diag(degrees)-A
        second=float(np.linalg.eigvalsh(lap)[1])
        assert second>.99
        rows.append({"L":L,"N":N,"edges":int(A.sum()//2),
                     "diameter":1 if L==1 else 2,"max_degree":int(max(degrees)),
                     "laplacian_lambda2":second})
    return {"graph":"Boolean lattice B_L comparability graph of Pascal parity support",
       "degree_formula":"2^popcount(v)+2^(L-popcount(v))-2",
       "edge_formula":"3^L-2^L",
       "diameter_L_at_least_2":2,
       "levels":rows,
       "qualification":"Raw parity graph has universal vertices and cannot by itself give local 3+1 continuum adjacency. A Sierpinski gasket nearest-neighbor Laplacian or an ordered causal Hasse cover is a different graph."}

def photon_cost():
    rows=[]
    for x in (0.,.5,1.,2.):
        S=1+sqrt(1+exp(-2*x*x))
        for eta in (.9,.99):
            upper=2+eta*eta*(S-2)
            gap=upper-2
            N=ceil(32*log(1/.05)/(gap*gap))
            rows.append({"relative_energy_phase_jitter_x":x,"survival_eta":eta,
               "ideal_SSR_CHSH":S,"optimistic_unconditional_CHSH_upper_bound":upper,
               "Hoeffding_alpha_0p05_trials_targeting_upper_bound_gap":N})
    assert rows[-2]["Hoeffding_alpha_0p05_trials_targeting_upper_bound_gap"]>1e9
    return {"theoretical_model":"Two copies under strict local number SSR; independent energy-phase jitter and independent whole-photon loss",
       "bound":"Sall <=2+eta²(1+sqrt(1+exp(-2x²))-2)",
       "statistical_concentration":"For Z=4(-1)^(ij) AB in [-4,4], one-sided P(S_hat-E[S_hat]>=gap)<=exp(-N gap²/32)",
       "cases":rows,
       "qualification":"Upper-bound-target counts have neither guaranteed attainable optical measurements nor specified statistical power. No detector loophole closure or departure from ordinary QM."}

def deformed_wall():
    x,y,z,g=s.symbols("x y z g",real=True)
    W=sum(v**3-v**6/s.Integer(2) for v in (x,y,z))+g*x*y*z*(x**3+y**3+z**3-2)
    gradients=[s.diff(W,v) for v in (x,y,z)]
    along=[s.factor(v.subs({y:1,z:1})) for v in gradients]
    assert s.simplify(along[1]-g*x*(x**3+3))==0
    assert s.simplify(along[2]-g*x*(x**3+3))==0
    assert s.simplify(along[0]-(3*x*x-3*x**5+4*g*x**3))==0
    val=along[1].subs({x:s.Rational(1,2),g:s.Rational(1,4)})
    assert val==s.Rational(25,64)
    assert [a.subs({x:1,g:s.Rational(1,4)}) for a in along]==[1,1,1]
    t=s.Rational(5,3)
    Wnew=3*(t-t*t/s.Integer(2))+s.Rational(1,4)*t*(3*t-2)
    assert Wnew==s.Rational(25,12)
    T=2*(Wnew-1)
    assert T==s.Rational(13,6)
    return {"parallel_baseline":"37ba627 H27 sextic mass-lift Wg",
      "transverse_gradient_along_old_x_only_wall":"g*x*(x^3+3)",
      "transverse_force_x_half_g_quarter":str(val),
      "gradient_at_old_111_endpoint_g_quarter":[1,1,1],
      "new_equal_coordinate_MUB_r_cubed":"5/3",
      "new_MUB_critical_W":"25/12",
      "conditional_BPS_tension_if_wall_exists":str(T),
      "old_undeformed_wall_tension":"1",
      "failure":"Old straight-line y=z=1 path is NOT a gradient BPS solution for g!=0; full coupled three-scalar heteroclinic unknown."}

def hypercube_log_mass():
    from scipy.linalg import expm
    X=np.array([[0.,1.],[1.,0.]])
    Z=np.diag([1.,-1.])
    B=np.array([[2.,1.],[1.,1.]])
    H=(2*X+Z)/sqrt(5)
    t=2*log(PHI)
    assert np.linalg.norm(B-expm(t*H))<1e-13
    # One local rotation maps H=(2X+Z)/sqrt5 to X.
    # The Pascal K_L=(A^T A)^{tensor L}=exp(2ln(phi)*sum_i H_i).
    # That sum is unitarily equivalent to Q_L hypercube adjacency sum X_i.
    data=[]
    for L in range(1,6):
        K=np.array([[1.]])
        Hsum=np.zeros((2**L,2**L))
        Q=np.zeros_like(Hsum)
        for i in range(L):
            K=np.kron(K,B)
            for out,local in ((Hsum,H),(Q,X)):
                ops=[np.eye(2) for _ in range(L)]
                ops[i]=local
                kron=ops[0]
                for op in ops[1:]:kron=np.kron(kron,op)
                out+=kron
        err=float(np.max(abs(K-expm(t*Hsum))))
        ev=np.linalg.eigvalsh(Hsum)
        evQ=np.linalg.eigvalsh(Q)
        expected=sorted([L-2*j for j in range(L+1)
                         for _ in range(s.binomial(L,j))])
        assert np.max(abs(ev-expected))<1e-10
        assert np.max(abs(evQ-expected))<1e-10
        assert err<2e-10
        assert len(Q)==2**L
        assert np.all(Q.sum(0)==L)
        # The order-theoretic transitive reduction is hypercube Q_L.
        data.append({"L":L,"vertices":2**L,
          "cover_graph_edges":L*2**(L-1),
          "cover_graph_degree":L,"cover_graph_diameter":L,
          "max_operator_K_minus_expm_error":err,
          "hypercube_adjacency_eigenvalues_with_multiplicity":
             [int(z) for z in expected]})
    return {"exact_single_digit_identity":
        "A=[[1,0],[1,1]], B=A^T A=[[2,1],[1,1]]=exp(2log(phi)*(2sigma_x+sigma_z)/sqrt5)",
       "exact_tensor_identity":
        "K_L=P_L^T P_L=exp(2log(phi)*sum_i(2X_i+Z_i)/sqrt5)",
       "unitary_equivalence":
        "sum_i(2X_i+Z_i)/sqrt5 is related by independent local SU2 rotations to hypercube adjacency A(Q_L)=sum_i X_i",
       "mass_squared_spectrum":
        "lambda_j(K_L)=exp[2log(phi)*(L-2j)]=phi^(2L-4j), multiplicity C(L,j), j=0..L",
       "hypercube_cover_graph":
        "The Hasse-cover graph of Boolean subset inclusion is L-dimensional hypercube Q_L with 2^L vertices, degree L, diameter L",
       "tests":data,
       "obstruction":
        "The adjacency becomes local on a hypercube only at the price of increasing its graph dimension L with resolution; for fixed L=4 only 16 vertices. The exponent spectrum is a free tensor-product spin field, not a sourced 3+1 Einstein/Yukawa Hamiltonian."}

def run():
    R={"compact_index":compact(),"localized_masses":overlap(),
       "H27_GUT_anomalies":h27_and_anomalies(),"pascal_graph":pascal_graph(),
       "photon":photon_cost(),"new_H27_deformed_wall":deformed_wall(),
       "Pascal_hypercube_log_mass_equivalence":hypercube_log_mass(),
       "limitations":"Finite toy mechanisms tested; true G2/E8 chiral index, observed masses, GUT anomaly inflow, causal quantum Einstein gravity and optical fault-tolerant hardware all remain unsolved."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(R,indent=2)+"\n",encoding="utf8")
    print("PASS six physical compatibility gates; 3 noncompact -> 3 compact mirror candidates; 3 defect contacts -> rank3")
    print("GRAPH Pascal graph diameter",R["pascal_graph"]["diameter_L_at_least_2"])
    print("H27 deformed old-wall transverse force",R["new_H27_deformed_wall"]["transverse_force_x_half_g_quarter"])
    print("OUTPUT",OUT)
    return R

if __name__=="__main__":run()
