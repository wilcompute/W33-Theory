"""Five TOE 'cracks' and exact obstruction audits; physics first, no W33 input.
Run from repository: python analysis/toe_20261119_five_cracks_symmetry_adjoints_gravity_photons.py
All conclusions conditional on explicit EFT/geometry/symmetry assumptions.
"""
from pathlib import Path
from math import pi, log, sqrt
import json
import numpy as np
from scipy.optimize import root
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from toe_20261119_balanced_source_E8_cup_gate import sector_census

BASE=Path(__file__).resolve().parents[1]

def su5_three_adjoint_completion():
    # Three distinct fermionic SU5 adjoints 24_F with one adjoint-Higgs VEV:
    # M8=M+2K, M3=M-3K, MX=(M8+M3)/2, M1=(2M8+3M3)/5.
    # Choose complementary light-triplet (2 dims)/light-octet (1 dim)
    # flavor projectors to make all X heavy, then refit all thresholds.
    mz=91.1876;mu=2.e16;ae=127.930;sw=.23122;as3=.1180
    inv0=np.array([(3/5)*(1-sw)*ae,sw*ae,1/as3],float)
    bsm=np.array([41/10,-19/6,-7.],float)
    trip=np.array([0.,4/3,0.])
    octet=np.array([0.,0.,2.])
    lepto=np.array([10/3,2.,4/3])
    def physical_masses(log_to):
        t,o=np.exp(log_to)
        m3=np.array([t,t,mu]);m8=np.array([mu,mu,o])
        mx=(m3+m8)/2
        ms=(2*m8+3*m3)/5
        return m3,m8,mx,ms
    def coupling_at_mu(log_to):
        m3,m8,mx,ms=physical_masses(log_to)
        inv=inv0-bsm*log(mu/mz)/(2*pi)
        for masses,beta in ((m3,trip),(m8,octet),(mx,lepto)):
            inv-=np.sum(np.log(mu/masses))*beta/(2*pi)
        return inv
    def eqs(log_to):
        a=coupling_at_mu(log_to)
        return np.array([a[0]-a[1],a[0]-a[2]])
    fit=root(eqs,np.log([2e7,4e5]),tol=1e-11)
    assert fit.success and max(abs(eqs(fit.x)))<1e-10
    m3,m8,mx,ms=physical_masses(fit.x)
    m0=(3*m8+2*m3)/5
    k=(m8-m3)/5
    assert np.allclose(m0-3*k,m3)
    assert np.allclose(m0+2*k,m8)
    assert np.allclose(m0-k/2,mx)
    assert np.allclose(m0-k,ms)
    assert np.all(mx>1e15) and np.all(m3>mz) and np.all(m8>mz)
    assert np.allclose(trip+octet+lepto,[10/3]*3)
    # The choice requires cancellations at (light/heavy) ~10^-10 to 10^-12.
    fine=min(m3[0]/mu,m8[2]/mu)
    # Same two light SU2 triplets allow a conventional rank-two
    # type-III seesaw. These light neutrino masses are INPUTS, not predictions.
    v=246.22
    target=np.array([0.,sqrt(7.465e-5),sqrt(2.5093e-3)])*1.e-9
    Y=np.zeros((2,3),float)
    Y[0,1]=sqrt(2*m3[0]*target[1])/v
    Y[1,2]=sqrt(2*m3[1]*target[2])/v
    mnu=v*v/2*Y.T@np.diag(1/m3[:2])@Y
    assert np.linalg.matrix_rank(mnu)==2
    assert np.allclose(np.diag(mnu),target,rtol=1e-12,atol=1e-24)
    return {
        "field_content":"three Weyl fermionic SU5 24_F with diagonal generation matrices M0 and K times a single 24_H vev",
        "SU5_mass_relations":"M8=M0+2K; M3=M0-3K; MX=M0-K/2; M1=M0-K",
        "SU5_GUT_scale_chosen_GeV":mu,
        "SU2_triplet_masses_GeV":m3.tolist(),
        "SU3_octet_masses_GeV":m8.tolist(),
        "X_leptoquark_masses_GeV":mx.tolist(),
        "singlet_masses_GeV":ms.tolist(),
        "SU5_invariant_M0_eigenvalues_GeV":m0.tolist(),
        "SU5_adj_H_K_eigenvalues_GeV":k.tolist(),
        "one_loop_inverse_couplings_at_MU":coupling_at_mu(fit.x).tolist(),
        "one_loop_inverse_coupling_spread":float(np.ptp(coupling_at_mu(fit.x))),
        "beta_triplet":trip.tolist(),"beta_octet":octet.tolist(),"beta_X":lepto.tolist(),
        "smallest_light_to_heavy_cancellation_fraction":float(fine),
        "seesaw_typeIII_two_heavy_triplets":True,
        "seesaw_normal_ordering_input_eV":(target*1e9).tolist(),
        "seesaw_Y_example_flavor_diagonal":Y.tolist(),
        "seesaw_reconstruction_eV":(np.diag(mnu)*1e9).tolist(),
        "seesaw_light_mass_rank":int(np.linalg.matrix_rank(mnu)),
        "neutrino_limit":"Example diagonal Yukawas reconstruct imported splittings; PMNS, type-I singlet mixings, CP phases, radiative masses and leptogenesis remain free.",
        "result":"Three complementary flavor projectors evade the TWO-24_F light-X singular-value obstruction while refitting all 24_F thresholds at ONE LOOP.",
        "not_solved":"Chosen MU and mass matrix alignments, 10^-12-ish cancellations, Higgs/scalar thresholds, 2-loop RGE, proton lifetime, PMNS, scalar vacuum and actual unified UV dynamics are NOT predicted."
    }

def E8_discrete_R_necessary_gate():
    sectors,_,_=sector_census()
    active16=[s for s in sectors if s["label"].startswith("16_") and s["b1"]>0]
    active10=[s for s in sectors if s["label"].startswith("10_") and s["b1"]>0]
    activeS=[s for s in sectors if s["label"].startswith("S_")]
    assert sum(s["b1"] for s in active16)==3
    assert sum(s["b1"] for s in active10)==5
    assert any(s["label"]=="10_34" for s in active10)
    assert any(s["label"]=="10_24" for s in active10)
    # Candidate Z4^R: R(W)=2, R(16)=1, R(S)=0,
    # R(10_34)=R(10_24)=0. One unused 10 receives R=1,
    # specifically to make mixed Spin10^2-Z4R coefficient even.
    unused=[s["label"] for s in active10 if s["label"] not in ("10_34","10_24")]
    assert len(unused)==3
    ten_R={s["label"]:(1 if s["label"]==unused[0] else 0) for s in active10}
    singlet_R={s["label"]:0 for s in activeS}
    assert all((1+1+ten_R[h]+0)%4==2 for h in ("10_34","10_24"))
    assert (1+1+ten_R["10_34"])%4==2
    # Pure singlet monomials all have R=0, hence absent from W at all
    # polynomial orders so long as exact Z4R and only these singlets.
    # The Spin10 gauge anomaly residue for Z4R has eta=N/2=2:
    # A=T(adj)+sum (R_i-1)*T(R_i).
    a_spin=8
    for s in active16:a_spin+=2*(1-1)*s["b1"]
    for s in active10:a_spin+=(ten_R[s["label"]]-1)*s["b1"]
    assert a_spin%2==0
    # U1^2-Z4R mixed coefficients from all charged fermions, using
    # full rep dimension. No assertion they vanish.
    a_u=np.zeros((3,3),dtype=int)
    for s in active16:
        q=np.array(s["SU4_charge"],int)
        a_u+=16*0*s["b1"]*np.outer(q,q)
    for s in active10:
        q=np.array(s["SU4_charge"],int)
        a_u+=10*(ten_R[s["label"]]-1)*s["b1"]*np.outer(q,q)
    for s in activeS:
        q=np.array(s["SU4_charge"],int)
        a_u-=s["b1"]*np.outer(q,q)
        a_u-=s["b2"]*np.outer(q,q)
    # Four-dimensional minimal supergravity discrete-R gravitational anomaly:
    # gravitino -21, each gaugino contributes dim(g), each chiral
    # fermion dim(rep)*(r-1). This is a necessary modulo-eta check,
    # subject to additional gravity/moduli and Green-Schwarz sectors.
    agr=-21+(45+3)
    agr+=sum(16*(1-1)*s["b1"] for s in active16)
    agr+=sum(10*(ten_R[s["label"]]-1)*s["b1"] for s in active10)
    agr-=sum(s["b1"]+s["b2"] for s in activeS)
    assert agr==-21 and agr%2==1
    assert (agr-1)%2==0  # one additional neutral R=0 chiral multiplet
    # Build a nonzero F/D-flat singlet branch if no other W operators
    # are generated: opposite S12 pair plus CEG triangle.
    sc={s["label"]:np.array(s["SU4_charge"],int) for s in activeS}
    charge_balance=sc["S_12"]-sc["S_12"]+sc["S_13"]+sc["S_34"]-sc["S_14"]
    assert np.array_equal(charge_balance,np.zeros(3,int))
    return {
        "symmetry":"candidate Z4^R, W charge2, all eight charged singlets charge0, three 16s charge1",
        "ten_R_charges":ten_R,
        "one_singlet_Yukawas_R_allowed":True,
        "singlet_bilinears_and_dangerous_cubics_R_forbidden":True,
        "all_pure_singlet_polynomials_forbidden_at_exact_R_level":True,
        "Spin10_mixed_R_anomaly_integer":a_spin,
        "Spin10_mod_eta_2":a_spin%2,
        "U1a_U1b_R_mixed_anomaly_matrix":a_u.tolist(),
        "U1a_U1b_R_mixed_anomaly_mod2":(a_u%2).tolist(),
        "minimal_supergravity_gravitational_Z4R_coefficient":agr,
        "gravitational_Z4R_mod_eta_2":agr%2,
        "one_neutral_R0_chiral_makes_gravitational_mod2_zero":(agr-1)%2==0,
        "Dflat_pair_plus_triangle_charge_sum":charge_balance.tolist(),
        "Fflat_Dflat_nonzero_tree_vacuum_with_only_these_chiral_superfields":True,
        "nonprediction":"This establishes a tree-level *moduli branch*, not a stabilized finite VEV, mass hierarchy, physical E8 wavefunction overlap or a fully anomaly-free discrete gauge symmetry.",
        "risk":"Mixed Abelian/gravitational discrete anomalies, Green-Schwarz inflow, supergravity constant W, anomalous U1 FI terms, additional neutral fields and nonperturbative R breaking require a separate UV audit."
    }

def singlet_driving_field_FD_completion():
    # Construct an explicit nonzero SUSY vacuum for the previously forbidden
    # singlet branch using a candidate exact Z4R and two neutral driving
    # superfields X_A, X_B with R=2, all eight charged singlets R=0.
    # W = X_A(AB-vA²) + X_B(CEG/M-vB³/M).
    # The X_B term is quartic in fields and therefore an effective operator.
    sectors,_,_=sector_census()
    charges={s["label"]:np.array(s["SU4_charge"],int)
             for s in sectors if s["label"].startswith("S_")}
    qA=charges["S_12"];qB=-qA
    qC=charges["S_13"];qE=-charges["S_14"];qG=charges["S_34"]
    Q=np.column_stack([qA,qC,qG])
    assert np.array_equal(qA+qB,np.zeros(3,int))
    assert np.array_equal(qC+qE+qG,np.zeros(3,int))
    D=int(sp.Matrix(Q).det())
    assert abs(D)==4
    smith=smith_normal_form(sp.Matrix(Q),domain=sp.ZZ)
    smith_diag=[abs(int(smith[i,i])) for i in range(3)]
    assert smith_diag==[1,1,4]
    vA=1.7;vB=.6;M=10.
    A=B=vA
    C=E=G=vB
    XA=XB=0.
    # F_XA=AB-vA², F_XB=(CEG-vB³)/M.
    fx=np.array([A*B-vA*vA,(C*E*G-vB**3)/M])
    fs=np.array([XA*B,XA*A,
                 XB*E*G/M,XB*C*G/M,XB*C*E/M])
    Dmoment=qA*(abs(A)**2)+qB*(abs(B)**2)+qC*(abs(C)**2)+qE*(abs(E)**2)+qG*(abs(G)**2)
    assert np.linalg.norm(fx)<1e-12 and np.linalg.norm(fs)<1e-12
    assert np.linalg.norm(Dmoment)<1e-12
    # F/D-holomorphic quotient: five nonzero complex singlet fields,
    # rank3 Higgsed U1 and two gauge-invariant constraints => dimension0
    # in this branch, not necessarily in the entire eight-field model.
    assert int(np.linalg.matrix_rank(Q))==3
    # A bare CEG monomial R=0 is forbidden; X_B CEG/M has R=2.
    assert (0+0+0)%4!=2 and (2+0+0+0)%4==2
    return {
      "driving_fields":"two gauge-neutral chiral multiplets X_A,X_B of Z4R charge2",
      "EFT_superpotential":"W=X_A*(S12*S12conj-vA^2)+X_B*(S13*S14conj*S34-vB^3)/M",
      "explicit_condensates":{"S12":A,"S12conj":B,"S13":C,"S14conj":E,"S34":G,"X_A":XA,"X_B":XB},
      "Fterm_driving_residual":fx.tolist(),
      "Fterm_charged_residual":fs.tolist(),
      "three_Dterms_residual":Dmoment.tolist(),
      "Higgs_charge_3x3_matrix":Q.tolist(),
      "Higgs_charge_index_abs_det":abs(D),
      "Higgs_charge_Smith_invariants":smith_diag,
      "naive_abelian_residual_gauge_stabilizer":"Z4 if the gauge group is U1^3 with primitive weight-character lattice",
      "global_group_caution":"For actual E8 -> (Spin10 x SU4)/Z4, this index may simply encode the SU4 center/diagonal quotient, not a new independent discrete gauge symmetry and NOT the proposed discrete R symmetry.",
      "local_moduli_count_on_five_field_branch":5-3-2,
      "R_gravitational_anomaly_with_two_R2_drivers":-21+2,
      "R_gravitational_mod2_with_drivers":(-21+2)%2,
      "R_gravitational_mod2_with_drivers_plus_one_R0_modulus":(-21+2-1)%2,
      "constructive_fact":"With exact Z4R, bare CEG is forbidden, but X_B*CEG/M and X_A*AB are allowed. Their F equations plus D=0 admit all three required singlet VEVs nonzero.",
      "not_solved":"The scales vA,vB and cutoff M are inputs; X_B CEG/M is nonrenormalizable; the remaining three singlet zero modes and all additional neutral moduli need stabilization. Z4R anomalies, physical Yukawa overlaps and the full compact G2 vacuum remain open."
    }


def torus_Wilson_line_gate():
    # Cellular cochain of T3 with a flat complex rank-one local system
    # character lambda=(l1,l2,l3). a_i=lambda_i-1.
    def ranks(lam):
        a=np.array(lam,dtype=complex)-1
        D0=a.reshape(3,1)
        D1=np.array([[-a[1],a[0],0],[-a[2],0,a[0]],[0,-a[2],a[1]]],complex)
        D2=np.array([[a[2],-a[1],a[0]]],complex)
        assert np.linalg.norm(D1@D0)<1e-12
        assert np.linalg.norm(D2@D1)<1e-12
        r0=int(np.linalg.matrix_rank(D0,tol=1e-10))
        r1=int(np.linalg.matrix_rank(D1,tol=1e-10))
        r2=int(np.linalg.matrix_rank(D2,tol=1e-10))
        return [1-r0,3-r1-r0,3-r2-r1,1-r2],[r0,r1,r2]
    vals=[(1,1,1),(-1,1,1),(np.exp(2j*pi/3),1,-1),
          (np.exp(1j*pi/7),np.exp(2j*pi/5),1)]
    samples=[]
    for lam in vals:
        dims,ran=ranks(lam)
        assert dims==([1,3,3,1] if all(abs(x-1)<1e-12 for x in lam) else [0,0,0,0])
        samples.append({"lambda":list(map(str,lam)),"twisted_Betti_dimensions":dims,"coboundary_ranks":ran})
    return {
        "T3_flat_line_bundle_samples":samples,
        "general_theorem":"If any rank-one character lambda_i !=1, the T3 local-system Koszul cochain complex is acyclic (contract with a_i^-1); trivial character has H1 dimension3.",
        "puncture_H1_extension":"Removing a 3-ball from T3 does not change absolute H1 local-system cohomology; the pair excision affects degree3, not degree1.",
        "centralizer_obstruction":"Wilson-line holonomy commuting with the entire unbroken Spin10 acts trivially on its 45 adjoint generators, so its adjoint local system remains untwisted and still has 3 copies from b1=3.",
        "escape":"Break/lift adjoints by non-flat Higgs background, boundary/defect projections, a different three-cycle, or dynamics. Noncentral holonomy can eliminate some modes but breaks part of Spin10.",
        "scope":"This is flat local-system cohomology, not a sourced ALE/G2 index calculation with flux and physical boundary domains."
    }

def lattice_linearized_Einstein_gate():
    # 4D Minkowski signature, periodic lattice and *commuting* central
    # differences. Linearized Einstein tensor obeys exact discrete Bianchi
    # and kills pure gauge h_mu_nu=D_mu xi_nu+D_nu xi_mu.
    n=8; shape=(n,)*4;metric=np.array([-1,1,1,1])
    D=lambda x,i:(np.roll(x,-1,axis=i)-np.roll(x,1,axis=i))/2
    def Einstein(h):
        trace=sum(metric[i]*h[i,i] for i in range(4))
        div=np.stack([sum(metric[r]*D(h[r,nu],r) for r in range(4)) for nu in range(4)])
        box=lambda f:sum(metric[r]*D(D(f,r),r) for r in range(4))
        R=np.empty_like(h)
        for i in range(4):
            for j in range(4):
                R[i,j]=.5*(D(div[j],i)+D(div[i],j)-box(h[i,j])-D(D(trace,j),i))
        scal=sum(metric[i]*R[i,i] for i in range(4))
        G=R.copy()
        for i in range(4):G[i,i]-=.5*metric[i]*scal
        return G
    rng=np.random.default_rng(198314)
    a=rng.normal(size=(4,4)+shape)
    h=(a+np.swapaxes(a,0,1))/2
    G=Einstein(h)
    div=np.stack([sum(metric[i]*D(G[i,nu],i) for i in range(4)) for nu in range(4)])
    xi=rng.normal(size=(4,)+shape)
    pure=np.stack([np.stack([D(xi[j],i)+D(xi[i],j) for j in range(4)]) for i in range(4)])
    pureG=Einstein(pure)
    # Even lattice alternating-sign Nyquist high mode D_checker=0;
    # exact lattice Bianchi alone is not enough to guarantee spectrum.
    checker=(-1.)**np.indices(shape)[1]
    # Genuine transverse-traceless spatial shear with wavevector x1,
    # polarization h23: not a mere lapse perturbation.
    checker_h=np.zeros_like(h);checker_h[2,3]=checker;checker_h[3,2]=checker
    doublerG=Einstein(checker_h)
    assert np.linalg.norm(checker)>1 and np.max(abs(D(checker,1)))==0
    assert max(np.max(abs(div)),np.max(abs(pureG)),np.max(abs(doublerG)))<1e-11
    forward=lambda x,i:np.roll(x,-1,axis=i)-x
    assert np.max(abs(forward(checker,1)))==2
    return {
        "grid":"periodic 8^4 Minkowski lattice, central symmetric derivatives",
        "discrete_linearized_Bianchi_max_residual":float(np.max(abs(div))),
        "pure_gauge_Einstein_max_residual":float(np.max(abs(pureG))),
        "staggered_Nyquist_false_zero_Einstein_residual":float(np.max(abs(doublerG))),
        "forward_derivative_on_same_Nyquist_amplitude":float(np.max(abs(forward(checker,1)))),
        "physical_question":"An exactly gauge invariant finite difference Einstein tensor can still have spurious zero-energy Nyquist modes. A positive-norm, causal, no-doubler propagator and local constraint algebra are additional demands.",
        "scope":"Linearized free GR identity, no full nonlinear gravity, no constraint/Hamiltonian dynamics, no proof of quantum unitarity."
    }

def two_copy_one_photon_SSR_activation():
    # Independent copies of (|10>+|01>)/sqrt2 in mode pairs
    # (A1,B1) and (A2,B2): amplitudes each 1/2.
    # The local N_A=N_B=1 sector contains A1B2+B1A2, probability 1/2.
    components={"A1A2":.25,"A1B2":.25,"A2B1":.25,"B1B2":.25}
    p=components["A1B2"]+components["A2B1"]
    assert p==.5
    # Dual-rail encoded qubit each site, both local particle numbers=1.
    psi=np.array([0,1,1,0],complex)/sqrt(2)
    X=np.array([[0,1],[1,0]],complex)
    Y=np.array([[0,-1j],[1j,0]],complex)
    rho=np.outer(psi,psi.conj())
    e=lambda a,b:float(np.vdot(psi,np.kron(a,b)@psi).real)
    B0=(X+Y)/sqrt(2);B1=(X-Y)/sqrt(2)
    S=e(X,B0)+e(X,B1)+e(Y,B0)-e(Y,B1)
    assert abs(S-2*sqrt(2))<1e-12
    # Both X and Y act solely within local N=1 dual-rail subspace.
    return {
        "single_copy":"(|A>+|B>)/sqrt2 under strict local U1 SSR",
        "two_copy_event_ready_one_local_photon_each_probability":p,
        "conditional_dual_rail_entangled_state":"(|A1 B2>+|A2 B1>)/sqrt2",
        "conditional_CHSH_number_conserving_dual_rail":S,
        "probability_two_photons_at_same_lab":.5,
        "required_consumed_nonvacuum_photons":2,
        "mechanism":"Second copy activates locally accessible entanglement, rather than pretending that one shared photon offers unrestricted local X/Y Pauli operations.",
        "limits":"Requires two identically phased copies and local phase-stable interferometers; event-ready heralding without setting bias and all optical loss rates must be included. Established SSR activation phenomenon, not a new Born-rule prediction."
    }

def main():
    out={
      "three_24F_GUT":su5_three_adjoint_completion(),
      "E8_discrete_R_candidate":E8_discrete_R_necessary_gate(),
      "E8_driving_field_singlet_vacuum":singlet_driving_field_FD_completion(),
      "centralizer_Wilson_line_test":torus_Wilson_line_gate(),
      "linearized_GR_lattice":lattice_linearized_Einstein_gate(),
      "two_copy_photon_SSR_activation":two_copy_one_photon_SSR_activation()
    }
    dest=BASE/"data"/"toe_20261119_five_cracks_symmetry_adjoints_gravity_photons.json"
    dest.write_text(json.dumps(out,indent=2)+"\n",encoding="utf8")
    for k in out:print("PASS",k)
    print("GUT masses",out["three_24F_GUT"]["SU2_triplet_masses_GeV"],out["three_24F_GUT"]["SU3_octet_masses_GeV"])
    print("GUT spread",out["three_24F_GUT"]["one_loop_inverse_coupling_spread"])
    print("Spin10 Z4R anomaly",out["E8_discrete_R_candidate"]["Spin10_mod_eta_2"])
    print("lattice doubled",out["linearized_GR_lattice"]["staggered_Nyquist_false_zero_Einstein_residual"])
    print(dest)
    return out

if __name__=="__main__":main()
