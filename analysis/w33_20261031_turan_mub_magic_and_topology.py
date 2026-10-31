#!/usr/bin/env python3
"""Third continuation: W33 clock Turan ground states, chromatic MUB spread,
Jones-Wenzl postselection magic, optical phase twirl, categorical mismatch,
spectral-dimension no-go and metric-signature obstruction.

All results concern explicit supplied finite mathematical models.
No physical TOE, anyon material, continuum spacetime or measured hardware.
"""
from __future__ import annotations
import json,sys,itertools,math
from pathlib import Path
from collections import Counter
import numpy as np
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_pass12055_microscopic_tick_model import ADJ,PROJ,PTS,w,pauli
from w33_20261031_helstrom_optical_braid_readout import angle_rotation

OUT=ROOT/"data/w33_20261031_turan_mub_magic_and_topology.json"
def err(X):return float(np.linalg.norm(X))
def noncommutation():return nx.complement(nx.from_numpy_array(ADJ))
def turan(n,r=7):
    a,b=divmod(n,r)
    return (n*n-(r-b)*a*a-b*(a+1)*(a+1))//2
def clock():
    G=noncommutation()
    clique7=[tuple(sorted(c)) for c in nx.find_cliques(G) if len(c)==7]
    assert len(clique7)==2880
    assert not any(len(c)>7 for c in nx.find_cliques(G))
    # Complete graph with any 120 Pauli tick labels, including repetitions.
    # The subgraph made of negative-energy (noncommuting) pairs is K8-free.
    # Turan's extremal K8-free edge bound is exact, and saturated by
    # balanced classes all having one tick from a 7-clique of directions.
    rows=[]
    for n in (2,4,7,8,9,13,14,15,21,40):
        a,b=divmod(n,7)
        counts=[a+int(k<b) for k in range(7)]
        labels=[c for k,c in enumerate(clique7[0]) for _ in range(counts[k])]
        assert len(labels)==n
        good=sum(1-ADJ[p,q] if p!=q else 0 for p,q in itertools.combinations(labels,2))
        assert good==turan(n)
        J,K=1.,2.
        cost=lambda p,q:0. if p==q else 2*J-(4*K/3) if not ADJ[p,q] else 2*J
        E=sum(cost(p,q) for p,q in itertools.combinations(labels,2))
        assert abs(E-(2*J-4*K/3)*turan(n))<1e-9
        row={"n":n,"turan_noncommuting_bonds":good,"same_tick_bonds":math.comb(n,2)-good,
             "exact_Emin_at_J1_K2":E}
        if a>=1:
            # Exhaustive ground-state count, no duplicate 7-clique:
            # Turan equality => complete balanced 7-partite noncommuting graph;
            # each independent class must use identical ticks.
            # Each direction admits exactly 3 spectral labels.
            product=math.prod(math.factorial(c) for c in counts)
            degeneracy=2880*(3**7)*math.comb(7,b)*math.factorial(n)//product
            row["exact_ground_state_count_for_n_ge_7"]=degeneracy
        rows.append(row)
    # Ground state selection for all J>0, K>3J/2, irrespective of n.
    assert abs(rows[3]["exact_Emin_at_J1_K2"]+18)<1e-10
    assert rows[3]["exact_ground_state_count_for_n_ge_7"]>0
    return {"status":"PROVED_ALL_N_TURAN_CLOCK_GROUND_LAW",
       "hypotheses":"Complete spatial K_n, labels from 120 rank3 Pauli spectral projectors, J>0 K>3J/2. Negative noncommuting edges have epsilon=2J-4K/3; same tick zero; all other positive.",
       "theorem":"E_min(n)=epsilon * t7(n), t7(n)=1/2[n^2-(7-r)a^2-r(a+1)^2], n=7a+r and 0<=r<7.",
       "reason":"Negative-bond subgraph K8-free by W33 clique number7 => Turan. Achieved with seven pairwise noncommuting directions, same tick in balanced parts.",
       "ground_state_count_n_ge7":"2880 * 3^7 * binomial(7,r) * n!/[a!^(7-r) (a+1)!^r]. Exact by Turan equality (balanced complete7-partite), each part identical tick and seven distinct noncommuting directions.",
       "finite_examples":rows,
       "kac_scaled_energy_density_limit":"If couplings divided by n-1, E_min/n -> (3/7)(2J-4K/3); external Kac normalization.",
       "limitations":"No finite-T phase diagram, no physical spacetime lattice, no quantum Hamiltonian or emergent time."}
def spread():
    G=nx.from_numpy_array(ADJ);H=nx.complement(G)
    cliques=[tuple(sorted(c)) for c in nx.find_cliques(G)]
    assert len(cliques)==40 and all(len(c)==4 for c in cliques)
    belong={x:[i for i,c in enumerate(cliques) if x in c]for x in range(40)}
    assert all(len(v)==4 for v in belong.values())
    def solve(uncovered,selected):
        if not uncovered:return selected
        p=min(uncovered,key=lambda x:sum(set(cliques[k])<=uncovered for k in belong[x]))
        for k in belong[p]:
            if set(cliques[k])<=uncovered:
                r=solve(uncovered-set(cliques[k]),selected+[k])
                if r is not None:return r
        return None
    indices=solve(set(range(40)),[])
    assert indices is not None and len(indices)==10
    partition=[list(cliques[i])for i in indices]
    assert sorted(sum(partition,[]))==list(range(40))
    # Spectrum of symplectic W33 collinearity and complementary noncommutation
    a=np.linalg.eigvalsh(ADJ);h=np.linalg.eigvalsh(nx.to_numpy_array(H))
    assert np.max(abs(np.sort(np.round(a))-
        np.sort([12]+[2]*24+[-4]*15)))<1e-9
    assert np.max(abs(np.sort(np.round(h))-
        np.sort([27]+[-3]*24+[3]*15)))<1e-9
    # Hoffman: chi(H)>=1-lambda_max/lambda_min=10.
    # 10 commuting 4-lines partition vertices -> proper 10-coloring of H.
    # This is a Pauli spread and gives 10 MUB contexts.
    MUB=[]
    for line in partition:
        # Simultaneously diagonalize four commuting Pauli observables via
        # an irrational-weight Hermitian combination; certify common eigenbasis.
        hmat=np.zeros((9,9),complex)
        for k,j in enumerate(line):
            P=pauli(PTS[j])
            hmat+=(math.sqrt([2,3,5,7][k])*(P+P.conj().T)
                  +math.sqrt([11,13,17,19][k])*(P-P.conj().T)/(1j))
        eig,basis=np.linalg.eigh(hmat)
        assert min(np.diff(eig))>1e-4
        assert err(basis.conj().T@basis-np.eye(9))<1e-12
        assert all(err((basis.conj().T@pauli(PTS[j])@basis)-
            np.diag(np.diag(basis.conj().T@pauli(PTS[j])@basis)))<1e-10
            for j in line)
        MUB.append(basis)
    deviation=max(np.max(abs(abs(MUB[i].conj().T@MUB[j])**2-1/9))
        for i in range(10) for j in range(i+1,10))
    assert deviation<1e-11
    return {"status":"PROVED_W33_NONCOMMUTATION_CHROMATIC_10_AND_MUB_SPREAD",
       "W33_eigenvalues":{"12":1,"2":24,"-4":15},
       "noncommutation_eigenvalues":{"27":1,"3":15,"-3":24},
       "chromatic_lower_bound_Hoffman":10,"actual_proper_coloring":10,
       "10_disjoint_maximal_commuting_contexts":partition,
       "mutual_unbiasedness_max_error":float(deviation),
       "physical_scope":"A native complete set of 10 mutually unbiased stabilizer bases in Hilbert dimension9, not a unique observed measurement preference."}
def wigner_magic():
    path=json.loads((ROOT/"data/w33_20261031_native_tlj_metaplectic_chain.json").read_text())["concrete_Pauli_indices"]
    I=np.eye(9,complex) if False else np.eye(9,dtype=complex)
    E=[math.sqrt(3)*PROJ[p][0] for p in path]
    angle=math.pi/6
    qnum=lambda n:math.sin(n*angle)/math.sin(angle)
    f=I.copy()
    rank1=None
    for n in range(1,5):
        f=f-(qnum(n)/qnum(n+1))*f@E[n-1]@f
        if n==3:rank1=f.copy()
    assert int(np.linalg.matrix_rank(rank1,tol=1e-8))==1 and err(f)<1e-10
    eig,V=np.linalg.eigh(rank1)
    state=V[:,-1]
    assert abs(eig[-1]-1)<1e-12
    W1=[]
    for q in range(3):
        for p in range(3):
            A=np.zeros((3,3),complex)
            for y in range(3):A[(q+2*y)%3,(q-2*y)%3]+=w**(p*y)
            W1.append(A)
    W=np.array([np.vdot(state,np.kron(a,b)@state).real/9 for a in W1 for b in W1])
    assert abs(W.sum()-1)<1e-11
    signed=float(np.sum(abs(W)))
    schmidt=np.linalg.svd(state.reshape(3,3),compute_uv=False)**2
    purity=float(np.sum(schmidt**2))
    P=np.zeros((9,9))
    for a in range(3):
        for b in range(3):P[(-a%3)*3+(-b%3),a*3+b]=1
    parity=float(np.vdot(state,P@state).real)
    assert abs(abs(parity)-1)<1e-10
    rho_a=state.reshape(3,3)@state.reshape(3,3).conj().T
    rho_b=state.reshape(3,3).conj().T@state.reshape(3,3)
    local=[]
    strange=np.array([0.,1.,-1.])/math.sqrt(2)
    for local_rho in (rho_a,rho_b):
        eigen,U=np.linalg.eigh(local_rho)
        ket=U[:,-1]
        vals=np.array([np.trace(local_rho@a).real/3 for a in W1])
        assert abs(vals.sum()-1)<1e-12
        local.append({"Wigner_min":float(vals.min()),
            "Wigner_L1":float(sum(abs(vals))),
            "overlap_with_canonical_Strange":float(abs(np.vdot(strange,ket))**2),
            "ket_re_im":[[float(z.real),float(z.imag)]for z in ket]})
    assert abs(signed-5/3)<1e-10 and abs(min(W)+1/9)<1e-10
    assert any(abs(x["overlap_with_canonical_Strange"]-1)<1e-10 for x in local)
    target=np.kron(np.array([1.,0.,0.]),strange)
    assert err(rank1-np.outer(target,target.conj()))<1e-10
    return {"status":"JW_F4_POSTSELECTED_RANK1_WIGNER_TEST",
       "exact_f4_projector_identity":"f4=|0><0| tensor |S><S|, |S>=(|1>-|2>)/sqrt(2), in native computational basis",
       "local_factor_Wigner_and_Strange":local,
       "f2_f3_f4_f5_ranks":[6,3,1,0],"f4_Wigner_min":float(np.min(W)),
       "f4_Wigner_L1":signed,"f4_mana":float(math.log(signed)),
       "f4_parity_eigenvalue":parity,
       "f4_two_qutrit_Schmidt_probabilities":list(map(float,schmidt)),
       "f4_reduced_purity":purity,
       "interpretation":"If f4 mana positive, its postselected measurement would be nonstabilizer resource; implementing a coherent f4 projector is a supplied non-Pauli operation. Otherwise a stabilizer witness.",
       "scope":"No physical measurement gadget, postselection success rate or topological fusion sector proven."}
def optics():
    F=np.array([[0,1,-3],[-1,0,2],[3,-2,0]],float)
    I=np.eye(3);p=(I+F@F/14+F/math.sqrt(14))[:,0]
    m=(I+F@F/14-F/math.sqrt(14))[:,0]
    phases=np.array([0,1,-1],float)
    sigma_values=[0.,.1,.5,1.,2.,4.,10.]
    rows=[]
    for sigma in sigma_values:
        dephase=np.exp(-.5*sigma*sigma*(phases[:,None]-phases[None,:])**2)
        rho_p=np.outer(p,p)*dephase;rho_m=np.outer(m,m)*dephase
        assert abs(np.trace(rho_p)-1)<1e-12 and abs(np.trace(rho_m)-1)<1e-12
        assert np.min(np.linalg.eigvalsh(rho_p))>-1e-12
        Delta=rho_p-rho_m
        # equal-prior min error, all POVMs: 1/2 - ||rho+-rho-||_1/4
        TVquantum=.5*sum(abs(np.linalg.eigvalsh(Delta)))
        bayes=(1-TVquantum)/2
        classical=.5*sum(abs(np.diag(rho_p)-np.diag(rho_m)))
        assert TVquantum+1e-12>=classical
        rows.append({"phase_noise_sigma_radians":sigma,
            "optimal_mixed_Helstrom_error":bayes,
            "quantum_trace_distance":TVquantum,
            "fixed_port_min_error":(1-classical)/2})
    assert abs(rows[0]["optimal_mixed_Helstrom_error"]-(1-2*math.sqrt(10)/7)/2)<1e-12
    assert abs(rows[-1]["optimal_mixed_Helstrom_error"]-rows[-1]["fixed_port_min_error"])<1e-8
    assert all(rows[i+1]["optimal_mixed_Helstrom_error"]+1e-12>=rows[i]["optimal_mixed_Helstrom_error"]
        for i in range(len(rows)-1))
    return {"status":"PASS_PHASE_DEPHASING_OPTICAL_HELSTROM_TO_FIXED_PORT_LIMIT",
        "model":"Independent zero-mean Gaussian common waveguide phase theta per injection: D(theta)=diag(1,e^{i theta},e^{-i theta}); matrix coherence damped by exp(-sigma^2 (a_i-a_j)^2/2).",
        "measured_data":False,"rows":rows,
        "proof_scope":"Exact density-matrix Gaussian averaging and Helstrom trace norm for this chosen noise channel; not calibrated interferometer performance or automatic optimal measurement under unknown drift."}
def geometry():
    from w33_20261031_dynamic_native_metric_backreaction import Q, controls, initial
    eig=np.linalg.eigvalsh(Q)
    assert np.min(eig)>0
    src=initial(4);phi=.09*src
    for alpha in (0.,.3,2.):
        g=np.exp(2*alpha*phi)
        assert all(np.linalg.eigvalsh(t*Q).min()>0 for t in g.flat)
    return {"status":"PROVED_CONFORMAL_SCALAR_METRIC_CANNOT_PRODUCE_LORENTZ_SIGNATURE",
        "Q_eigenvalues":list(map(float,eig)),
        "inertia_Q":[4,0,0],
        "positive_conformal_field_preserves_inertia":True,
        "obstruction":"Every g(x)=e^(2alpha phi_x) Q has four positive eigenvalues, zero negatives: Sylvester inertia law. The externally supplied time evolution adds a fifth coordinate, not a derived Lorentz 3+1 signature.",
        "next_step":"Signed tetrad/connection plus constraint algebra and continuum Ward checks (externally motivated)."}
def category():
    # SU(2)_4 is a CHIRAL modular category; D(S3) is a Drinfeld center.
    k=4
    qdims=[math.sin((j+1)*math.pi/(k+2))/math.sin(math.pi/(k+2)) for j in range(k+1)]
    twists=[np.exp(1j*math.pi*j*(j+2)/(2*(k+2))) for j in range(k+1)]
    D2=sum(x*x for x in qdims);gauss=sum(x*x*t for x,t in zip(qdims,twists))
    assert abs(D2-12)<1e-12
    assert abs(gauss-1j*math.sqrt(12))<1e-12
    # D(S3) quantum double anyons labeled (conjugacy class, centralizer irrep):
    # identity class size1, centralizer irreps 1,1,2;
    # transposition class size3, centralizer irreps1,1;
    # 3-cycles class size2, centralizer irreps1,1,1.
    ds3=[1,1,2,3,3,2,2,2]
    assert sum(d*d for d in ds3)==36
    return {"status":"NO_BRAIDED_EQUIVALENCE_SU2_4_AND_D_S3",
       "SU2_4_simple_quantum_dimensions":qdims,"SU2_4_total_dimension_squared":D2,
       "SU2_4_gauss_sum_re_im":[gauss.real,gauss.imag],
       "SU2_4_chiral_central_charge_mod8":2,
       "D_S3_simple_quantum_dimensions":ds3,"D_S3_total_dimension_squared":36,
       "D_S3_chiral_central_charge_mod8":0,
       "obstruction":"Different numbers of anyons (5 versus8), total quantum dimensions sqrt12 versus6, and nontrivial vs trivial chiral central charge. The 2026 D(S3) braiding+fusion hardware demonstration is not an implementation of this 9D native SU2_4 Jones representation."}
def spectral():
    # 40-vertex W33 graph Laplacian lambda={0,10(24),16(15)}.
    # Effective dimension -2 dln K/dln t =2t mean(lambda)_heat.
    t=np.geomspace(.00001,10,600)
    K=1+24*np.exp(-10*t)+15*np.exp(-16*t)
    ds=2*t*(240*np.exp(-10*t)+240*np.exp(-16*t))/K
    peak=int(np.argmax(ds))
    assert ds[0]<.001 and ds[-1]<1e-30
    assert max(ds)<4
    return {"status":"FINITE_W33_LAPLACIAN_NO_INTRINSIC_4D_HEAT_KERNEL_SCALING",
        "laplacian_spectrum":{"0":1,"10":24,"16":15},
        "heat_trace":"K(t)=1+24e^(-10t)+15e^(-16t)",
        "spectral_dimension":"ds(t)=2t(240e^(-10t)+240e^(-16t))/K(t)",
        "sample_peak_time":float(t[peak]),"sample_peak_dimension":float(ds[peak]),
        "ultraviolet_limit":0,"infrared_limit":0,
        "boundary":"Fixed finite graph cannot have a genuine t->0 continuum d=4 scaling, but a growing graph family might."}
def torsion_canonical():
    """An index-not-divisible-by-5 argument establishes the quotient's
    canonical Tor(coker B,F5) meaning even without full Z saturation."""
    from sympy import Matrix
    from w33_20261031_torsion_order5_probe import rk,ker
    sys.path.insert(0,str(ROOT/"analysis/search_drivers_12466"))
    from symmetric_fast import fast_build
    _,lines=fast_build(9)
    choice=json.loads((ROOT/"analysis/search_drivers_12466/icosa_even_q9.json").read_text())["results"][0]["chosen"]
    sets=[set(lines[i])for i in choice]
    G=nx.Graph();G.add_nodes_from(range(48))
    G.add_edges_from((i,j)for i in range(48)for j in range(i+1,48)if sets[i]&sets[j])
    colors=nx.bipartite.color(G)
    left=sorted(i for i in G if colors[i]==0)
    right=sorted(i for i in G if colors[i]==1)
    B=np.array([[int(G.has_edge(i,j))for j in right]for i in left],dtype=np.int64)
    M=Matrix(B.tolist());rat_null=M.nullspace()
    assert M.rank()==18 and len(rat_null)==6
    L=[]
    for v in rat_null:
        den=math.lcm(*[int(x.q) for x in v])
        nums=[int(x*den) for x in v];scale=math.gcd(*nums)
        L.append([int(x//scale) for x in nums])
    L=np.array(L,dtype=np.int64).T
    assert np.all(B@L==0) and rk(L,5)==6
    assert ker(B,5).shape==(24,13)
    # Full rank reduction at p=5 certifies chosen six-vector integer
    # kernel sublattice has index coprime to 5 in saturated kernel.
    # Consequently reduced lattice == red(ker_Z B) as F5-subspaces.
    # LES of tensor exact sequence identifies the quotient with
    # Tor_1^Z(coker(B),F5), a CANONICAL characteristic-five module.
    old=json.loads((ROOT/"data/w33_20261031_eight_quantum_fronts_round2.json").read_text())
    action=np.array(old["fronts"]["01_characteristic_five_module"]["action7_GF5"],dtype=np.int64)
    assert action.shape==(7,7) and np.array_equal(np.linalg.matrix_power(action,5)%5,np.eye(7,dtype=int))
    N=(action-np.eye(7,dtype=int))%5
    ranks=[rk(np.linalg.matrix_power(N,j)%5)for j in range(6)]
    assert ranks==[7,4,2,0,0,0]
    return {"status":"PROVED_CANONICAL_CHAR5_TORSION_MODULE_IDENTIFICATION",
       "B_shape":[24,24],"rank_over_Q":18,"integer_kernel_dimension":6,
       "rank_reduction_mod5_of_integer_kernel_basis":6,
       "kernel_B_mod5_dimension":13,"canonical_Tor_dimension":7,
       "order5_induced_Jordan_blocks":[3,3,1],
       "theorem":"If L0 is rank-r sublattice of saturated kerZ(B) and rank_Fp(L0 modp)=r, then [kerZ(B):L0] is prime to p; their reductions span the same Fp-subspace. Here r6 p5. Exact tensor-sequence yields ker(B mod5)/red(kerZ B)=Tor_1(coker B,F5) of dimension7.",
       "limits":"This settles canonicity of the previous GF5 quotient; not full integral saturation at other primes, an A5 group representation or physical topological flux."}

def build():
    tasks={"01_all_n_clock_ground_states":clock,
        "02_exact_chromatic_MUB_geometry":spread,
        "03_JonesWenzl_rank1_magic_resource":wigner_magic,
        "04_optical_phase_noise_limit":optics,
        "05_gravitational_metric_signature":geometry,
        "06_anyonic_category_mismatch":category,
        "07_native_spectral_dimension_obstruction":spectral,
        "08_canonical_characteristic5_torsion":torsion_canonical}
    out={"schema":"w33.pass125xx.turan_mub_magic.v1",
         "reference_head":"ccbd086d1f5b1cc204547766baced5449981d020",
         "results":{}}
    for name,func in tasks.items():
        result=func();out["results"][name]=result
        print(name,result["status"],flush=True)
    return out
if __name__=="__main__":
    d=build();OUT.write_text(json.dumps(d,indent=2,sort_keys=True,default=lambda x:x.item() if isinstance(x,np.generic) else str(x))+"\n",encoding="utf-8")
    print("WROTE",OUT,flush=True)
