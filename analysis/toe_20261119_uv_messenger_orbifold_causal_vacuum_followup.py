"""TOE physics-first: renormalizable messenger escape and five further falsifiers.

No W33 assumption. Conditional finite EFT, orbifold, topology, causal and quantum
models, NOT a derived compactification/SM/TOE.
"""
from pathlib import Path
from math import pi, sqrt, log, exp
import json
import numpy as np
import sympy as sp
from scipy.integrate import quad
from toe_20261119_balanced_source_E8_cup_gate import sector_census
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261119_uv_messenger_orbifold_causal_vacuum_followup.json"


def e8_renormalizable_messenger_completion():
    """Renormalizable F/D-flat UV messenger completion of previous five drivers."""
    sectors,_,_=sector_census()
    charge={s["label"]:np.array(s["SU4_charge"],int)
            for s in sectors if s["label"].startswith("S_")}
    names=["A","B","C","D","E","F","G1","G2"]
    Q=np.stack([charge["S_12"],-charge["S_12"],charge["S_13"],
                charge["S_14"],-charge["S_14"],charge["S_24"],
                charge["S_34"],charge["S_34"]])
    # Invariants I1=AB, I2=DE, and I3=AFE, I4=CEG1, I5=CEG2.
    n={"A":0,"B":1,"C":2,"D":3,"E":4,"F":5,"G1":6,"G2":7}
    triples=[("A","F","E"),("C","E","G1"),("C","E","G2")]
    M=10.0
    u=np.array([2,1,2,1,4,1,1,1],float)
    # For each quartic X_i P_i R_i /M introduce massive pair Y_i, Z_i,
    # q_Y=-q_P, q_Z=q_P, R_Y=0,R_Z=2. W UV includes:
    # M Y Z+ X P Y+ Z R + t X. F_Z=0 gives Y=-R/M.
    yvals=np.array([-sqrt(u[n[b]]*u[n[c]])/M for a,b,c in triples])
    for i,(a,b,c) in enumerate(triples):
        u[n[a]]+=yvals[i]**2
    fields=np.sqrt(u)
    qY=np.stack([-Q[n[a]] for a,b,c in triples])
    qZ=-qY
    assert np.array_equal(Q[n["A"]]+Q[n["B"]],np.zeros(3,int))
    assert np.array_equal(Q[n["D"]]+Q[n["E"]],np.zeros(3,int))
    for i,(p,r1,r2) in enumerate(triples):
        assert np.array_equal(qY[i]+qZ[i],np.zeros(3,int)) # M Y Z
        assert np.array_equal(Q[n[p]]+qY[i],np.zeros(3,int)) # X P Y
        assert np.array_equal(qZ[i]+Q[n[r1]]+Q[n[r2]],
                              np.zeros(3,int)) # Z R
    # W terms have R2 from X and Z; R(Y)=R(light)=0.
    q_all=np.concatenate([Q,qY],axis=0)
    vev0=np.concatenate([fields,yvals])
    D=q_all.T@(vev0**2)
    assert np.max(abs(D))<1e-12
    # 8 R-charge-zero ("charged") chiral fields, three R0 messengers;
    # 5 R2 neutral drivers and three R2 heavy partners.
    target_pairs=[fields[n["A"]]*fields[n["B"]],
                  fields[n["D"]]*fields[n["E"]]]
    target_triples=[-fields[n[a]]*yvals[i] for i,(a,b,c) in enumerate(triples)]
    # Holomorphic Hessian at X_i=Z_i=0 is [[0,J^T],[J,0]];
    # J rows = d F_(X1,..,X5,Z1,..,Z3) / d (A,..,G2,Y1,..,Y3).
    J=np.zeros((8,11))
    A,B,C,Dfield,E,F,G1,G2=fields
    J[0,n["A"]]=B;J[0,n["B"]]=A
    J[1,n["D"]]=E;J[1,n["E"]]=Dfield
    for i,(p,r1,r2) in enumerate(triples):
        J[2+i,n[p]]=yvals[i]
        J[2+i,8+i]=fields[n[p]]
        J[5+i,8+i]=M
        J[5+i,n[r1]]=fields[n[r2]]
        J[5+i,n[r2]]=fields[n[r1]]
    H=np.zeros((19,19))
    H[:11,11:]=J.T
    H[11:,:11]=J
    rankJ=int(np.linalg.matrix_rank(J,tol=1e-11))
    rankH=int(np.linalg.matrix_rank(H,tol=1e-11))
    gauge_tangent=vev0[:,None]*q_all
    assert rankJ==8 and rankH==16
    assert np.linalg.matrix_rank(gauge_tangent)==3
    gauge_norm=float(np.linalg.norm(J@gauge_tangent))
    assert gauge_norm<1e-12
    # Direct F-terms:
    # F_(X1)=AB-t1, F_(X2)=DE-t2,
    # F_(Xi)=P Yi + t_i for 3..5;
    # F_Zi=M Yi+ Ri; F_Yi=M Zi+Xi P, and F_light=0.
    FX=[A*B-target_pairs[0],Dfield*E-target_pairs[1]]
    FZ=[]
    for i,(p,r1,r2) in enumerate(triples):
        FX.append(fields[n[p]]*yvals[i]+target_triples[i])
        FZ.append(M*yvals[i]+fields[n[r1]]*fields[n[r2]])
    assert max(abs(x) for x in FX+FZ)<1e-12
    # Independently differentiate the COMPLETE superpotential symbolically
    # to certify the numerical F/Hessian/Jacobian, rather than reuse our
    # hand-derived block formula without checking its derivatives.
    syms=sp.symbols("A B C D E F G1 G2 Y0 Y1 Y2 X0 X1 X2 X3 X4 Z0 Z1 Z2")
    left,right=syms[:11],syms[11:]
    Ws=right[0]*(left[0]*left[1]-target_pairs[0])
    Ws+=right[1]*(left[3]*left[4]-target_pairs[1])
    for i,(p,r1,r2) in enumerate(triples):
        Ws+=M*left[8+i]*right[5+i]+right[2+i]*left[n[p]]*left[8+i]
        Ws+=right[5+i]*left[n[r1]]*left[n[r2]]
        Ws+=right[2+i]*target_triples[i]
    subs=dict(zip(syms,vev0.tolist()+[0.]*8))
    f_sym=np.array([float(sp.diff(Ws,v).subs(subs)) for v in syms])
    J_sym=np.array([[float(sp.diff(Ws,right[i],left[j]).subs(subs))
                      for j in range(11)] for i in range(8)])
    assert np.max(np.abs(f_sym))<1e-11
    assert np.allclose(J_sym,J,rtol=0,atol=1e-12)
    tP,tR,tX,tY,tZ,tM=sp.symbols('P R X Y Z M',nonzero=True)
    Wmess=tM*tY*tZ+tX*tP*tY+tZ*tR
    Weff=sp.simplify(Wmess.subs({tY:-tR/tM,tZ:-tX*tP/tM}))
    assert sp.simplify(Weff+tX*tP*tR/tM)==0
    # Charge-check ALL THREE formal diagonal Spin10 16_i 16_i 10_H S_i/M
    # operators with the actual source 10-sector charges. Their nonzero
    # amplitudes are *not* implied by gauge selection (original bulk cup=0).
    ten_charge={s["label"]:np.array(s["SU4_charge"],int)
                for s in sectors if s["label"].startswith("10_") and s["b1"]}
    fam_weights=[np.array([1,0,0]),np.array([0,1,0]),np.array([0,0,1])]
    assignments=[("10_34","B"),("10_34","A"),("10_24","C")]
    assert all(H in ten_charge for H,S in assignments)
    for w,(H,S) in zip(fam_weights,assignments):
        assert np.array_equal(2*w+ten_charge[H]+Q[n[S]],np.zeros(3,int))
    formal_mass=np.diag([fields[n[S]]/M for H,S in assignments])
    assert np.linalg.matrix_rank(formal_mass)==3
    # R-symmetry: each (Y,Z) fermion has R-1,+1, and qZ=-qY.
    # Mixed U1^2-R cancels per pair, gravitational-R cancels per pair,
    # ordinary U1^3 and mixed grav-U1 cancel per vectorlike pair.
    mixed=np.zeros((3,3),int)
    gravR=0
    cubic=np.zeros((3,3,3),int)
    gravU=np.zeros(3,int)
    for y,z in zip(qY,qZ):
        for q,r in ((y,0),(z,2)):
            mixed+=(r-1)*np.outer(q,q)
            gravR+=r-1
            gravU+=q
            cubic+=np.einsum("i,j,k->ijk",q,q,q)
    assert np.array_equal(mixed,np.zeros((3,3),int))
    assert gravR==0 and not cubic.any() and not gravU.any()
    return {
        "sector_source":"cb1a66717 balanced E8; zero modes and charge matrix IMPORTED",
        "charged_field_order":names,
        "field_charges":Q.tolist(),"messenger_Y_charges":qY.tolist(),
        "messenger_Z_charges":qZ.tolist(),
        "superpotential_exact":"W=X1(AB-t1)+X2(DE-t2)+sum_i[M Yi Zi + Xi Pi Yi + Zi Ri + Xi ti], with (Pi,Ri)=(A,FE),(C,EG1),(C,EG2) and ti=Pi*Ri/M",
        "all_superpotential_terms_renormalizable_in_fourD":True,
        "mass_M_input":M,
        "singlet_squared_vevs":u.tolist(),"Y_messenger_vevs":yvals.tolist(),
        "Z_messenger_vevs":[0.,0.,0.],
        "X_driver_vevs":[0.]*5,
        "two_quadratic_targets":target_pairs,
        "three_messenger_driver_targets":target_triples,
        "F_X_residual":FX,"F_Z_residual":FZ,
        "D_Abelian_residual":D.tolist(),
        "Jacobian_rank":rankJ,"full_superpotential_Hessian_rank":rankH,
        "symbolic_full_Fterm_max_error":float(np.max(np.abs(f_sym))),
        "symbolic_vs_hand_Jacobian_max_error":float(np.max(np.abs(J_sym-J))),
        "exact_integrated_out_one_pair_coefficient":"-X*P*R/M",
        "three_formal_diagonal_yukawa_spurion_selections":[{"family":i+1,"Higgs_10":h,"singlet":s} for i,(h,s) in enumerate(assignments)],
        "formal_rank3_diagonal_dimensionless_masses_with_lambda_equals_one":np.diag(formal_mass).tolist(),
        "formal_diagonal_mass_rank":int(np.linalg.matrix_rank(formal_mass)),
        "Yukawa_warning":"Full-rank DIAGONAL is only gauge/R-allowed if external overlap couplings and Higgs VEVs are nonzero; no source-space physical Yukawa or observed hierarchy follows.",
        "gauge_tangent_dimension":int(np.linalg.matrix_rank(gauge_tangent)),
        "gauge_tangent_Hessian_block_residual":gauge_norm,
        "local_physical_complex_moduli_count":19-rankH-3,
        "added_messenger_mixed_U1squared_R_anomaly":mixed.tolist(),
        "added_messenger_grav_R_anomaly":gravR,
        "added_messenger_U1cubed_anomaly":cubic.tolist(),
        "added_messenger_grav_U1_anomaly":gravU.tolist(),
        "five_R2_drivers_gravitational_Z4R_mod2_from_prior_minimal_spectrum":(-21+5+gravR)%2,
        "result":"Explicit 19-field renormalizable W with 3 heavy vectorlike gauge pairs, five neutral R2 drivers and nonzero D-flat light/messenger condensates. F=0, D=0; Hessian rank16 leaves exactly three gauge orbits; messenger pairs add zero perturbative gauge and listed R anomaly coefficients.",
        "critical_limits":"Heavy messenger Y must condense and alters the D terms; exact compensation is included. All source field content, five drivers, target t_i, heavy M, R symmetry and UV geometry are INSERTED. Full E8 higher-dimensional overlap, original anomalous U1s, gravitational/global anomalies, realistic masses, proton safety and dynamical R origin remain unsolved."
    }


def orbifold_su5_projected_fermions():
    """Two-boundary 5D orbifold SU5 generator parity decomposition."""
    P=np.diag([1,1,1,-1,-1])
    assert np.linalg.det(P)==1
    even,odd=[],[]
    # offdiagonal Hermitian pairs (symmetric and antisymmetric)
    for i in range(5):
        for j in range(i+1,5):
            parity=int(P[i,i]*P[j,j])
            for kind in ("symmetric","imaginary"):
                (even if parity==1 else odd).append((i,j,kind))
    # traceless diagonal Hermitian generators (rank 4)
    even.extend([(i,i,"Cartan") for i in range(4)])
    assert len(even)==12 and len(odd)==12
    # Boundary parity P0=I and Ppi=P, so even sector has (+,+)
    # and a zero mode, whereas odd sector has (+,-), no zero.
    # Opposite 4D chirality has (-,-) for even and (-,+) for odd;
    # no zero except first chirality's even sector.
    b3=np.array([0,0,2],float)
    b2=np.array([0,4/3,0],float)
    bx=np.array([10/3,2,4/3],float)
    assert np.allclose(b2+b3+bx,[10/3]*3)
    return {
        "P0":[1,1,1,1,1],"Ppi":[1,1,1,-1,-1],
        "Ppi_is_in_SU5":True,"SU5_generator_even_count":len(even),
        "SU5_generator_odd_count":len(odd),
        "even_subalgebra":"su3(8) + su2(3) + u1(1), total 12",
        "odd_subspace":"(3,2,-5/6) + (3bar,2,5/6), total 12",
        "boundary_pair_even":"(+,+): zero mode allowed",
        "boundary_pair_odd":"(+,-): zero mode forbidden",
        "light_Weyl_adjoint_zero_mode_betas":[(b2+b3).tolist()],
        "missing_X_dirac_pair_beta":bx.tolist(),
        "fiveD_KK_masses":"for interval length L, (+,+) n*pi/L (n>=0), (+,-) (n+1/2)*pi/L",
        "interpretation":"Boundary parity breaks SU5 to SM subgroup and protects off-block fermion/gauge X zero-mode absence without cancellation of huge signed fourD adjoint mass matrices.",
        "provenance":"Known extra-dimensional orbifold GUT mechanism (see EPJC 2025 SU5 x U1PQ article), NOT novel physics or a complete 5D theory here.",
        "limitations":"A single Z2 parity is insufficient for a 5D Dirac fermion: both boundaries' conditions and 4D chirality must be specified. Even 8+3+1 zero modes are not selectively split by P alone; mass hierarchy, KK threshold unification, brane Yukawas/anomalies, proton decay and UV/gravity completion remain open."
    }


def CP2_twisted_SpinC_chirality():
    """Dirac index under twisting a fixed spin-c line by a U1 bundle."""
    k=5
    rows=[]
    for q in range(-2,4):
        keff=k+2*q
        idx=(keff*keff-1)//8
        assert ((keff*keff-1)%8)==0
        rows.append({"line_twist_q":q,"effective_spinC_determinant_class":keff,
                     "index":idx})
    assert [r["index"] for r in rows]==[0,1,3,6,10,15]
    return {
       "M":"CP2 Euclidean compact 4-manifold, not physical Lorentzian spacetime",
       "fixed_spinC_determinant_k":k,
       "twist":"tensor spinor with complex line bundle c1=qH, gives effective determinant k+2q",
       "index_formula":"index_q=((k+2q)^2-1)/8, for k odd and integer q",
       "table":rows,
       "difference_formula":"index_(q+1)-index_q=(k+2q+1)/2",
       "nonuniversality":"The same spin-c background gives index3 at q0 but index6 for q1 and index1 for q-1. Three for one charge DOES NOT imply three for all components of a gauge multiplet after arbitrary extra twisting.",
       "physical_limit":"No dynamical flux fixing, actual G2 compactification, four-dimensional chirality, boundary/domain zero mode calculation, or SM gauge representation from this CP2 toy."
    }


def causal_density_independent_link_thinning():
    """Fixed profile f(rho V)=exp[-a rho V] cannot bound causal degree."""
    kap=pi/24
    def g(s):
        if s<=0:return 1.0
        if s>=1:return 0.0
        z=sqrt(1-s)
        return z-s*log((1+z)/sqrt(s))
    data=[]
    for alpha in (0,1,3,15):
        for rho in (160.,2560.,40960.):
            val=pi*rho*quad(lambda s:exp(-(1+alpha)*rho*kap*s*s)*g(s),
                            0,1,epsrel=1e-10,epsabs=1e-9,limit=300)[0]
            coeff=pi*sqrt(6/(1+alpha))
            data.append({"alpha":alpha,"rho":rho,"expected_retained_links":val,
                         "expected_div_sqrt_rho":val/sqrt(rho),
                         "asymptotic_div_sqrt_rho":coeff})
        these=[v for v in data if v["alpha"]==alpha]
        assert all(these[i+1]["expected_retained_links"]>these[i]["expected_retained_links"] for i in range(2))
        assert abs(these[-1]["expected_div_sqrt_rho"]/these[-1]["asymptotic_div_sqrt_rho"]-1)<.10
    return {
        "geometry":"unit coordinate-time truncated future cone in 3+1 Minkowski",
        "acceptance_rule":"given actual causal link, retain with probability exp(-alpha*rho*V_interval), alpha>=0 fixed as rho changes",
        "note":"actual links have empty intervals; rho*V_interval here is the *embedding/continuum* Alexandrov volume, not the observed number of intermediate elements. This thinning is NOT intrinsic order-only.",
        "asymptotic_exact":"E_retained ~ pi sqrt(6/(1+alpha))*sqrt(rho) for any fixed alpha>=0",
        "integral":"pi rho int_0^1 ds exp[-(1+alpha)*rho*pi*s²/24] [sqrt(1-s)-s log((1+sqrt(1-s))/sqrt(s))]",
        "data":data,
        "no_fixed_positive_alpha_makes_degree_bounded":True,
        "limits":"Positive nonvanishing density-independent link-thinning profiles still give growing null-cone link degree in this region. This does not exclude cancellation-based nonlocal kernels, density-dependent suppression or other intrinsic locality prescriptions."
    }


def quantum_pure_vacuum_energy_selection():
    """Covariant CCR and purity fix no state; supplied H_omega does."""
    J=np.array([[0.,1.],[-1.,0.]])
    table=[]
    for omega in (.5,1.,2.,4.):
        r=-.5*log(omega)
        V=np.diag([exp(2*r),exp(-2*r)])/2
        W=V+1j*J/2
        assert np.linalg.eigvalsh(W).min()>-1e-12
        assert abs(np.linalg.det(V)-.25)<1e-12
        assert np.max(abs(W-W.T-1j*J))<1e-12
        E=(V[1,1]+omega*omega*V[0,0])/2
        assert abs(E-omega/2)<1e-12
        table.append({"frequency_omega":omega,"energy_ground":E,"vacuum_squeezing_r":r,
                      "q_variance":V[0,0],"p_variance":V[1,1]})
    assert len(set(round(x["q_variance"],7) for x in table))==4
    return {
       "fixed_commutator":"[q,p]=i shared by all choices",
       "supplied_Hamiltonian":"H_omega=(p²+omega² q²)/2, omega>0",
       "minimizer_r":"-1/2 log(omega)",
       "table":table,
       "result":"Each positive omega selects a unique pure Gaussian oscillator ground state, but different supplied Hamiltonians select different physical vacua with identical CCR. A causal exchange TOE must derive the time generator/energy functional, not simply impose minimization.",
       "scope":"Elementary harmonic oscillator, not a curved-spacetime Hadamard state, a Born rule or an interacting causal quantum gravity solution."
    }


def photonic_phase_threshold():
    w=.82
    from math import log as ln
    rhs=1/(w*w)-1
    sigma_max=sqrt(-ln(rhs))
    assert abs(2*w*sqrt(1+exp(-sigma_max*sigma_max))-2)<1e-12
    samples=[]
    for sigma in (0,.4,.8,sigma_max,1,2):
        vis=exp(-sigma*sigma/2)
        S=2*w*sqrt(1+vis*vis)
        samples.append({"sigma_relative_phase":sigma,"visibility":vis,"max_CHSH":S})
    return {
       "Bell_fraction_w":w,"required_visibility_sq":rhs,
       "maximum_Gaussian_phase_sigma_for_CHSH_violation":sigma_max,
       "samples":samples,
       "ideal_two_photon_eta0p8_herald_probability":.5*.8**2,
       "if_two_independent_QND_herald_efficiencies_each_0p7":.5*.8**2*.7**2,
       "not_solved":"The model is standard QM, not an experimental TOE signature. QND herald rates and phase noise were assumed; detector loopholes, clock drift, source distinguishability and full process tomography remain."
    }


def run():
    out={
      "E8_renormalizable_messenger_vacuum":e8_renormalizable_messenger_completion(),
      "SU5_two_boundary_orbifold_alternative":orbifold_su5_projected_fermions(),
      "twisted_spinC_family_indices":CP2_twisted_SpinC_chirality(),
      "causal_link_thinning_no_go":causal_density_independent_link_thinning(),
      "CCR_energy_vacuum_selection":quantum_pure_vacuum_energy_selection(),
      "photon_phase_failure_threshold":photonic_phase_threshold()
    }
    OUT.write_text(json.dumps(out,indent=2)+"\n",encoding="utf8")
    for k in out:print("PASS",k)
    print("E8 Hessian rank",out["E8_renormalizable_messenger_vacuum"]["full_superpotential_Hessian_rank"])
    print("GUT even odd",out["SU5_two_boundary_orbifold_alternative"]["SU5_generator_even_count"],
          out["SU5_two_boundary_orbifold_alternative"]["SU5_generator_odd_count"])
    print("phase sigma threshold",out["photon_phase_failure_threshold"]["maximum_Gaussian_phase_sigma_for_CHSH_violation"])
    print(OUT)
    return out
if __name__=="__main__":run()
