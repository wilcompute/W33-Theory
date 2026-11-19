#!/usr/bin/env python3
"""Five physical TOE consistency gates plus a new cross-sector information gate.

Research provenance 2026-11-19. These are finite, conditional falsifiers,
not a derived theory of everything, experimental predictions, or novel
standalone theorems. See companion report for scope and cited prior art.
"""
from __future__ import annotations
from itertools import combinations
from pathlib import Path
import json
import math
import numpy as np
from scipy.special import gammaln

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261119_five_physics_global_gates_and_fisher.json"

def dagger(x): return np.asarray(x).conj().T

def causal_dag_determinant_gate():
    rng=np.random.default_rng(20261119)
    rows=[]
    for n in (4,8,12,20):
        upper=np.triu((rng.random((n,n))<.43).astype(float),1)
        perm=rng.permutation(n)
        A=upper[np.ix_(perm,perm)]
        assert np.linalg.norm(np.linalg.matrix_power(A,n))<1e-10
        for m,alpha in ((.7,.3),(1.2,.65)):
            D=m*np.eye(n)-alpha*A
            inverse_from_paths=sum(
                ((alpha/m)**k)*np.linalg.matrix_power(A,k)/m
                for k in range(n))
            observed=float(np.linalg.det(D))
            expected=m**n
            assert abs(observed-expected)<1e-8*max(1,expected)
            assert np.linalg.norm(D@inverse_from_paths-np.eye(n))<1e-9
            rows.append({"events":n,"mass":m,"link_coupling":alpha,
                "directed_edges":int(upper.sum()),
                "observed_det":observed,
                "exact_graph_blind_det":expected,
                "inverse_path_sum_error":float(np.linalg.norm(D@inverse_from_paths-np.eye(n)))})
    # Two different DAGs have same determinant but generally unequal
    # retarded Green functions, so the vacuum measure is blind even
    # though propagation is NOT blind.
    B=np.zeros((4,4));C=B.copy();B[0,1]=1;C[0,2]=1
    G1=np.linalg.inv(np.eye(4)-.2*B)
    G2=np.linalg.inv(np.eye(4)-.2*C)
    assert np.linalg.norm(G1-G2)>.1
    assert abs(np.linalg.det(np.eye(4)-.2*B)-np.linalg.det(np.eye(4)-.2*C))<1e-12
    # Closing a directed circle adds a Wilson holonomy-dependent loop.
    cycles=[]
    for n in (4,5,8):
        T=np.zeros((n,n),complex)
        for i in range(n-1): T[i,i+1]=1
        angle=.67
        T[n-1,0]=np.exp(1j*angle)
        for mass in (1.2,1.7):
            alpha=.4
            det=np.linalg.det(mass*np.eye(n)-alpha*T)
            expected=mass**n-alpha**n*np.exp(1j*angle)
            assert abs(det-expected)<1e-11
            cycles.append({"n":n,"mass":mass,"theta":angle,
                           "det_real":float(det.real),"det_imag":float(det.imag)})
    return {"status":"PASS",
      "exact_theorem":"Every finite directed acyclic A is nilpotent; det(m I-alpha A)=m^N, independent of causal links.",
      "nontrivial_propagation":"(m I-alpha A)^-1 = m^-1 sum_(k=0)^(N-1)(alpha A/m)^k, which depends on causal paths.",
      "random_labelled_DAG_checks":rows,"distinct_DAG_propagator_distance":float(np.linalg.norm(G1-G2)),
      "periodically_closed_directed_cycle_checks":cycles,
      "qualifier":"No general no-go for causal fermions: bidirectional/loop, holonomy, interactions, boundary, anomalies and non-vacuum insertions can add graph dependence."}

def su2_global_chiral_matter_gate():
    # Ordinary SM left-Weyl representations and integer y=6Y.
    fields=[("Q",6,1,3,1),("u^c",3,-4,-3,0),("d^c",3,2,-3,0),
            ("L",2,-3,0,1),("e^c",1,6,0,0),("nu^c",1,0,0,0)]
    # tuple: multiplet, Weyl multiplicity, y, an arbitrary 3*color
    # spectator tag (ignored in y anomaly), weak doublet flag.
    local_yy=sum(mult*y for _,mult,y,_,_ in fields)
    local_yyy=sum(mult*y**3 for _,mult,y,_,_ in fields)
    mixed_SU2_Y=3*1+(-3)
    mixed_SU3_Y=2*1+(-4)+2
    assert (local_yy,local_yyy,mixed_SU2_Y,mixed_SU3_Y)==(0,0,0,0)
    scenarios=[]
    for description,weyl_doublets,vectorlike in [
        ("single left-handed SU2 Weyl doublet plus gauge singlet",1,False),
        ("one SU2 Dirac doublet, equivalent to two Weyl doublets",2,True),
        ("one complete SM generation, three quark colors plus one lepton",4,False),
        ("three complete SM generations",12,False),
        ("SM plus a standalone additional left Weyl doublet",13,False),
        ("SM plus a vectorlike pair of extra doublets",14,True),
    ]:
        sign=(-1)**weyl_doublets
        scenarios.append({"content":description,"left_Weyl_doublet_count":weyl_doublets,
                          "nontrivial_pi4_SU2_gauge_transformation_sign":sign,
                          "passes_ordinary_Witten_SU2_parity_gate":sign==1,
                          "vectorlike":vectorlike})
    assert [x["nontrivial_pi4_SU2_gauge_transformation_sign"] for x in scenarios]==[-1,1,1,1,-1,1]
    # SU3xSU2xU1/Z6 descent for the supplied standard multiplets.
    quotient=[("Q",1,1,1),("u^c",-1,0,-4),("d^c",-1,0,2),
              ("L",0,1,-3),("e^c",0,0,6),("nu^c",0,0,0)]
    residues={name:(2*triality+3*weak+y)%6 for name,triality,weak,y in quotient}
    assert all(v==0 for v in residues.values())
    return {"status":"PASS","SM_one_generation_local_anomaly_integer_y6Y":
            {"gravity_Y":local_yy,"Y_cubed":local_yyy,"SU2_squared_Y":mixed_SU2_Y,"SU3_squared_Y":mixed_SU3_Y},
            "Witten_global_sign_cases":scenarios,
            "standard_global_Z6_descent_residues":residues,
            "important_distinction":"A single chiral SU2 Weyl doublet is globally anomalous; a vectorlike SU2 Dirac doublet need not be. Previous positive determinant examples used vectorlike toy operators and are not refuted by the chiral sign test.",
            "qualifier":"This evaluates standard global-anomaly parity and ordinary local anomaly sums. It does not compute a five-dimensional mod-two index, classify arbitrary exotic SU2 reps, or derive the SM spectrum."}

def one_body_restricted_matrix(n,k,i,j):
    """Hard-core n-mode boson basis, k occupied 0/1 modes.
    Restricted (a_i^dagger a_j) has zero matrix element whenever
    two photons must BOTH move. This is a projected quadratic operator
    statement, not a no-go for arbitrary interferometer+binning POVMs.
    """
    basis=[v for v in range(1<<n) if v.bit_count()==k]
    lookup={v:t for t,v in enumerate(basis)}
    O=np.zeros((len(basis),len(basis)),complex)
    for col,mask in enumerate(basis):
        if (mask>>j)&1 and not ((mask>>i)&1) and i!=j:
            moved=(mask^(1<<j))|(1<<i)
            O[lookup[moved],col]=1
        elif i==j and ((mask>>i)&1):
            O[col,col]=1
    return basis,O

def photonic_one_body_gate():
    n=4;k=2
    basis=[x for x in range(1<<n) if x.bit_count()==k]
    target=np.zeros((len(basis),len(basis)))
    for a in range(0,len(basis),2):
        target[a,a+1]=target[a+1,a]=1.
    lhs=basis.index(6);rhs=basis.index(9)
    assert target[lhs,rhs]==1.
    basisops=[]
    for i in range(n):
        _,O=one_body_restricted_matrix(n,k,i,i)
        basisops.append(O.real)
    for i in range(n):
        for j in range(i+1,n):
            _,P=one_body_restricted_matrix(n,k,i,j)
            _,Q=one_body_restricted_matrix(n,k,j,i)
            basisops.append((P+Q).real)
            assert abs(P[lhs,rhs])<1e-14 and abs(Q[lhs,rhs])<1e-14
    flat=np.column_stack([B.ravel() for B in basisops])
    coeff=np.linalg.lstsq(flat,target.ravel(),rcond=None)[0]
    projection=(flat@coeff).reshape(target.shape)
    residual=float(np.linalg.norm(target-projection))
    assert residual>=math.sqrt(2)-1e-11
    assert target[lhs,rhs]==1 and projection[lhs,rhs]==0
    # Practical published passive-photon ladder vs ideal fully collective
    # number-SSR CHSH law. Do not claim passive ladder is optimal for n>2.
    compare=[]
    root=math.sqrt(2)
    for n in (2,4,6,8,10):
        k=n//2
        ideal=2+(2*root-2)*(1-2**(n.bit_count()-n))
        passive=2*root-(2*root-2)/(2**k)
        assert ideal+1e-12>=passive
        compare.append({"copies":n,"ideal_arbitrary_SSR_CHSH":ideal,
                        "published_passive_ladder_CHSH":passive,
                        "collective_minus_passive":ideal-passive})
    return {"status":"PASS","n_modes_in_witness":4,"two_photon_sector_basis_n4":basis,
        "target_local_A1_nonzero_0110_to_1001_matrix_element":float(target[lhs,rhs]),
        "any_single_body_number_preserving_hamiltonian_same_matrix_element":0.,
        "best_real_quadratic_generator_projection_residual_Frobenius":residual,
        "ideal_vs_published_passive_ladder":compare,
        "qualifier":"The specific ideal CHSH observable is NOT a single quadratic bosonic Hamiltonian/generator. This does NOT rule out passive interferometers plus number-resolved detection and nonlinear classical outcome binning, or ancilla/feedforward-based compilations."}

def gravity_fermion_entropy_gate():
    rows=[]
    q=4
    singular_lower=.5;singular_upper=2.
    for N in (8,16,32,64,128):
        M=N*N//4
        group_ln=2*gammaln(N//4+1)+gammaln(N//2+1)
        ln_orbit_lower=M*math.log(2)-group_ln
        # Conditional one "good" reference and positive per-history weights.
        # Every qN x qN bad matrix has each singular >=a, every
        # good matrix each singular <=b. Then sum_bad / weight_good
        # >= #bad_orbits*(a/b)^(qN).
        ln_ratio_lower=ln_orbit_lower+q*N*math.log(singular_lower/singular_upper)
        rows.append({"events":N,"layer_adjacent_link_bits":M,
             "log10_unlabeled_orbit_lower_bound":ln_orbit_lower/math.log(10),
             "log10_bad_to_one_good_weight_lower_bound_under_uniform_gap":ln_ratio_lower/math.log(10),
             "q_fermion_components_per_event":q})
    assert rows[-1]["log10_bad_to_one_good_weight_lower_bound_under_uniform_gap"]>700
    assert rows[3]["log10_bad_to_one_good_weight_lower_bound_under_uniform_gap"]>90
    return {"status":"PASS",
       "marked_layer_3layer_family":"N/4,N/2,N/4, independent N^2/4 adjacent relations, quotient only by S_(N/4)xS_(N/2)xS_(N/4).",
       "bound":"#orbits >=2^(N²/4)/[(N/4)!²(N/2)!]",
       "spectral_assumption":"For every bad-history qN-dimensional kinetic matrix all singular values >=a=.5, and a single good-history matrix all singular values <=b=2; bare positive weights assumed equal.",
       "conditional_weight_bound":"sum_bad |det D_bad| / |det D_good| >= #orbits*(a/b)^(qN).",
       "results":rows,
       "possible_escape":"Geometry-specific exact fermion zero modes violate the lower singular-value assumption, while oscillatory interference or other nonlocal/strongly N-dependent measures can also evade the positive-weight bound.",
       "limitation":"One stipulated good history (not the whole manifoldlike class), marked-layer incidence orbits (not all unlabeled causets), positive weights and uniform spectral gap; not a general no-go on causal quantum gravity."}

def flavor_graph_spectral_gate():
    records=[]
    for eps in (0.,1e-6,1e-4,.01,.1,1.):
        a=float(eps);b=1.
        L=np.array([[a,-a,0],[-a,a+b,-b],[0,-b,b]])
        ev=np.linalg.eigvalsh(L)
        exact=a+b-math.sqrt(a*a-a*b+b*b)
        assert abs(ev[1]-exact)<1e-9
        assert abs(ev.sum()-2*(a+b))<1e-10
        # The weakly broken family-difference combination can remain
        # light even though the graph becomes connected for any a>0.
        records.append({"weak_Yukawa_edge_weight":eps,"other_edge_weight":b,
             "graph_connected":eps>0,
             "Laplacian_rank":int(np.linalg.matrix_rank(L,tol=1e-10)),
             "exact_lambda2":exact,"numeric_lambda2":float(ev[1]),
             "approx_ratio_lambda2_over_weak_edge":exact/a if a else None})
    assert records[0]["Laplacian_rank"]==1
    assert all(x["Laplacian_rank"]==2 for x in records[1:])
    assert abs(records[1]["approx_ratio_lambda2_over_weak_edge"]-1.5)<1e-5
    return {"status":"PASS","model":"Three-family quadratic charge-mismatch penalty sum_edges w_ij (X_i-X_j)^2, with sum_i X_i=0.",
       "exact_path_graph_lambda2":"a+b-sqrt(a*a-a*b+b*b) for links a,b",
       "small_a_limit":"lambda2 ~ 3a/2 for a<<b, despite a connected interaction graph.",
       "records":records,
       "limitation":"The penalty model is imposed. Actual Yukawa couplings, physical PMNS mixing angles and charged lepton rates are not predicted by Laplacian connectivity."}

def spin_sector_probabilities(mu):
    r=math.tanh(mu/2)
    z=(1+r)*(1+r*r)
    return np.array([r**3,r,1.,r*r])/z

def spin_sector_fisher_gate():
    rows=[]
    for mu in (.05,.1,.3,1.,2.,5.,10.):
        r=math.tanh(mu/2)
        rp=(1-r*r)/2
        fisher=rp*rp*(1/(r*(1+r)**2)+4/(1+r*r)**2)
        h=min(1e-5,.01*mu)
        p=spin_sector_probabilities(mu)
        deriv=(spin_sector_probabilities(mu+h)-spin_sector_probabilities(mu-h))/(2*h)
        numerical=float(np.sum(deriv*deriv/p))
        assert abs(numerical-fisher)<3e-7*max(1,fisher)
        assert abs(float(p.sum())-1)<1e-12
        rows.append({"dimensionless_fermion_mass_times_circle_length":mu,
                     "normalized_four_sector_weights":p.tolist(),
                     "classical_Fisher_information_on_mu":fisher,
                     "finite_difference_Fisher_crosscheck":numerical})
    assert rows[-1]["classical_Fisher_information_on_mu"]<2e-8
    assert rows[0]["classical_Fisher_information_on_mu"]>10
    return {"status":"PASS",
      "prior_toy":"Wilson circle determinant with equal bare spin-center sector priors, an SU2 doublet plus neutral singlet.",
      "P_sectors":"(r³,r,1,r²)/[(1+r)(1+r²)], r=tanh(mu/2)",
      "exact_classical_Fisher":"[(1-r²)/2]² [1/(r(1+r)²)+4/(1+r²)²]",
      "large_mu_asymptotic":"I(mu)~5 exp(-2mu), so very heavy fermions make spin-sector distributions locally hard to distinguish.",
      "results":rows,
      "limitation":"Information geometry of assumed classical TOY distributions, not operational access to physical spin structures, measurement error bounds or fundamental spacetime information metric."}

def run():
    gates={
       "I_dag_fermion_determinant_blindness":causal_dag_determinant_gate(),
       "II_global_SU2_Witten_anomaly_and_SM_quotient":su2_global_chiral_matter_gate(),
       "III_photonic_quadratic_gate_complexity_witness":photonic_one_body_gate(),
       "IV_causal_history_entropy_vs_gapped_fermion_weight":gravity_fermion_entropy_gate(),
       "V_flavor_connectivity_vs_spectral_gap":flavor_graph_spectral_gate(),
       "VI_fermionic_spin_sector_information_distinguishability":spin_sector_fisher_gate()}
    assert all(g["status"]=="PASS" for g in gates.values())
    return {"date":"2026-11-19","TOE_solved":False,
      "emergent_Lorentzian_4D_Einstein_gravity":False,
      "Born_rule_derived":False,"SM_spectrum_derived":False,
      "status":"PASS conditional five-front physics gates and an information-theoretic bridge",
      "literature":[
        "https://arxiv.org/abs/2611.20084",
        "https://arxiv.org/abs/2611.19570",
        "https://arxiv.org/abs/2209.00327",
        "https://journals.aps.org/prd/abstract/10.1103/PhysRevD.103.014503",
        "https://davidtong.org/pdfs/teaching/standardmodel5.pdf",
        "https://www.scholarpedia.org/article/Lattice_gauge_theories"],
      "gates":gates}

def main():
    data=run()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(data,indent=2,allow_nan=False)+"\n",encoding="utf8")
    print(json.dumps({"status":"PASS","gates":len(data["gates"]),
      "optical_gate_frobenius_gap":data["gates"]["III_photonic_quadratic_gate_complexity_witness"]["best_real_quadratic_generator_projection_residual_Frobenius"],
      "N64_bad_to_good_log10_bound":data["gates"]["IV_causal_history_entropy_vs_gapped_fermion_weight"]["results"][3]["log10_bad_to_one_good_weight_lower_bound_under_uniform_gap"],
      "flavor_gap_eps1e-4":data["gates"]["V_flavor_connectivity_vs_spectral_gap"]["records"][2]["exact_lambda2"],
      "output":str(OUT)}))
if __name__=="__main__":main()
