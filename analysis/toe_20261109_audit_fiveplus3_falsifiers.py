#!/usr/bin/env python3
"""Five strengthened W33 gates + three creative controls, 2026-11-09.

Scientific layers:
1 global frame order selection, 2 finite magnetic 4-spatial completion,
3 optical inverse-frame echo design, 4 E6+SM flatness, 5 cosmology source
evidence, +6 higher-prime frame mixing, +7 Wilson fermion doubling,
+8 antiunitary pezzotope triality. Includes the 43-commit audit receipt.
No independent experimental physics or cosmological likelihood is claimed.
"""
from __future__ import annotations
import argparse,collections,hashlib,itertools,json,math
from fractions import Fraction
from pathlib import Path
import numpy as np
import sympy as sp
from scipy.stats import binom
ROOT=Path(__file__).resolve().parents[1]
BASE="9e2f9b9e859ee4d7b39555c0052886653a90e3be"
def read(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))
def revision_review():
    j=read("data/toe_20261109_postpr324_fullbyte_audit.json")
    assert j["base"]==BASE
    assert j["commits"]==43 and j["versioned_file_reads"]==190
    assert j["whole_final_files_read"]==112 and not j["failures"]
    assert sum(f["bytes"] for f in j["final_files"])==j["final_file_bytes"]
    names={f["path"] for f in j["final_files"]}
    required=[
      "analysis/toe_20261108_invariant_magnetic_completion.py",
      "analysis/toe_20261108_exact_signed_cubic_stabilizer.py",
      "analysis/toe_20261109_canonical_sm_flatness.py",
      "analysis/toe_20261109_real_yoshida_pezzotope_labels.py",
      "analysis/PASS12637_SIX_PARTICLES_TRIALITY.md"]
    assert all(x in names for x in required)
    return dict(status="ALL_43_FULL_COMMIT_MESSAGES_190_WHOLE_BLOBS_112_FINAL_FILES_CHECKED",
       baseline=j["base"],audited_head=j["head"],
       commits=j["commits"],revisions=j["versioned_file_reads"],
       bytes_read=j["revision_bytes_read"],final_changed_files=j["whole_final_files_read"],
       evidence_scope="Machine-read and complete-byte checksum/JSON/AST audit, plus selected complete semantic document reviews; not 43 independent proof verifications.")

def spatial_frame_phase():
    # Q3: eight sites and twelve undirected nearest-neighbor edges;
    # four-frame ferromagnetic Potts-type order variable.
    V=list(itertools.product((0,1),repeat=3))
    index={v:i for i,v in enumerate(V)}
    edges=sorted({tuple(sorted((i,index[tuple(v[:j]+(1-v[j],)+v[j+1:])])))
       for i,v in enumerate(V) for j in range(3)})
    assert len(edges)==12
    hist=collections.Counter()
    weight_sums={.7:0.,1.5:0.,2.5:0.}
    order_sums={k:0. for k in weight_sums}
    for state in itertools.product(range(4),repeat=8):
        E=sum(state[a]!=state[b] for a,b in edges)
        hist[E]+=1
        mag=max(state.count(i) for i in range(4))/8
        for beta in weight_sums:
            w=math.exp(-beta*E);weight_sums[beta]+=w
            order_sums[beta]+=mag*w
    assert sum(hist.values())==4**8
    assert hist[0]==4
    gap=min(i for i in hist if i>0)
    assert gap==3
    # exact count of single-site flipped ground configurations = 4*8*3
    assert hist[3]>=96
    return dict(status="EXACT_FOUR_FRAME_Q3_POTTS_CUBE_PARTITION_AND_DOMAIN_WALL_GAP",
        vertices=8,undirected_couplings=len(edges),
        all_configs=4**8,exact_energy_histogram={str(k):v for k,v in sorted(hist.items())},
        exactly_degenerate_zero_energy_vacua=4,
        first_nonzero_interface_energy=gap,
        single_site_flip_states=96,
        beta_energy_sweeps=[
         dict(beta_J=beta,finite_Z=weight_sums[beta],
              expectation_largest_frame_fraction=order_sums[beta]/weight_sums[beta],
              all_equal_probability=4/weight_sums[beta])
          for beta in weight_sums],
        finite_volume_symmetric_mean_occupancy_per_frame=2.,
        caveat="Only eight sites and a classical global 4-state order field. Finite volume has no spontaneous breaking; temperature-dependent domain-wall physics, thermodynamic criticality, local gauge Elitzur constraint, Lorentz bounds and a fundamental frame metric remain unresolved.")

def ratmat(x):
    return sp.Matrix([[sp.Rational(q) for q in row] for row in x])
def native_magnetic_four_spatial():
    a=read("data/toe_20261108_invariant_magnetic_completion.json")
    T=ratmat(a["target_area_tensor"])
    short=ratmat(a["exact_short_area_tensor"])
    C=ratmat(a["complement_area_tensor"])
    S=ratmat(a["commutator_area_matrix"])
    H=ratmat(a["supplied_six_flux_coupling"])
    alpha=sp.Rational(a["short_face_weight"])
    threshold=sp.Rational(a["short_weight_PSD_compensation_threshold"])
    assert (T-short*alpha)==C
    assert S.det() in (-1,1)
    assert S.T*H*S==C
    assert all(H[:i,:i].det()>0 for i in range(1,7))
    assert short.rank()==1
    # New independent rank-one matrix determinant lemma:
    # det(T-t short)=det(T)*(1-t short00*(T^-1)00).
    a0=short[0,0];tinverse=T.inv()[0,0]
    critical=1/(a0*tinverse)
    assert critical==threshold==sp.Rational(5775,29857)
    for candidate in (0,alpha,critical,2*critical,1):
        lhs=(T-candidate*short).det()
        rhs=T.det()*(1-candidate/critical)
        assert lhs==rhs
    assert (T-critical*short).det()==0
    assert (T-2*critical*short).det()<0
    return dict(status="INDEPENDENT_EXACT_RANK_ONE_COMPENSATION_AND_SPATIAL_DIMENSION_FIREWALL",
        exact_ratio_short_over_target=str(1/critical),
        critical_positive_short_weight=str(critical),
        original_unweighted_short_weight_obstructed=True,
        supplied_short_weight=str(alpha),
        commutator_area_unimodular_determinant=int(S.det()),
        positive_H_sylvester_leading_minors=[str(H[:i,:i].det()) for i in range(1,7)],
        determinant_lemma_verified_at_five_rational_alphas=True,
        source_spatial_deck_rank=4,
        source_transverse_branches_per_nonzero_momentum=3,
        observed_three_spatial_Maxwell_transverse_branches=2,
        dimensionality_gap_explicit=True,
        physically_missing="A dimensional reduction/compactification and dynamical matter normalization: four spatial directions plus external time is 4+1, not 3+1. Existing native exact proof is source-derived, not independently regenerated 1287 face FFT here.")

def optical_inverse_frame_discriminator():
    # Decide between a four-frame classical mixture (return p <=.30 after
    # calibration) and a locked reference frame (p >= .90).
    p0=.30;p1=.90;alpha=.001;target=.99
    sol=None
    for n in range(1,301):
        for threshold in range(n+1):
            fpr=float(binom.sf(threshold-1,n,p0))
            power=float(binom.sf(threshold-1,n,p1))
            if fpr<=alpha and power>=target:
                sol=(n,threshold,fpr,power)
                break
        if sol:break
    assert sol
    n,k,fpr,power=sol
    # The ideal return 1 vs 1/4 (or 1/2), but here p0=.30 and
    # p1=.90 are pessimistic illustrative conditional calibrations.
    return dict(status="EXACT_BINOMIAL_SAMPLE_SIZE_FOR_FRAME_ECHO_WITH_STATED_NUISANCE_ENVELOPE",
        ideal_reference_locked_return=1.,
        ideal_fully_random_nonzero_q0_return=.25,
        ideal_q2_duplicated_character_reference_return=.5,
        design_null_hidden_frame_p_return_upper=.30,
        design_alternative_locked_frame_p_return_lower=.90,
        nominal_familywise_single_test_alpha=alpha,
        target_power=target,
        minimum_accepted_heralded_events=n,
        accept_frame_lock_if_echo_returns_at_least=k,
        exact_false_positive_probability=fpr,
        exact_minimum_power=power,
        need_independent_loss_reference=True,
        does_not_include_multiple_hypothesis_correction=True,
        caveat="Exact finite binomial tails only, not a demonstrated heralding rate, detector efficiency, independent calibration of 0.30/0.90, coherent reference stability or real experimental samples.")

def e6_current_flatness_anomaly():
    c=read("data/toe_20261108_exact_signed_cubic_stabilizer.json")
    sm=read("data/toe_20261109_canonical_sm_flatness.json")
    anomaly=sm["perturbative_family_anomaly"]
    assert anomaly["fundamental_minus_duals"]==27
    assert anomaly["conjugate_symmetric_cube_spectator"]==-27
    assert anomaly["total"]==0 and anomaly["net_SM_families"]==3
    assert sm["repair"]["minimal_dual_count_for_exact_untwisted_SM"]==2
    assert sm["repair"]["minimum_uneaten_massless_at_fixed_vev"]==101
    assert sm["repair"]["sextic_uneaten_massless"]==89
    assert sm["repair"]["sextic_massless_character"]=="3 times restricted 27 plus 8 trivial"
    # Independent SO(10) -> SM contents of 27=16+10+1; the 16
    # contains one sterile right-handed neutrino.
    assert 89==3*(16+10+1)+8==48+30+11
    assert c["cubic_27"]["rank_over_Q"]==651
    assert c["alternating_81"]["exact_rank"]==6475
    assert 729-651==78 and 6561-6475==86
    return dict(status="FULL_NATIVE_E6_STABILIZER_SUPERSEDES_14_GENERATOR_GATE_BUT_89_MODES_SURVIVE",
       exact_e6_infinitesimal_generators=78,
       E6_plus_SL3_infinitesimal_generators=86,
       canonical_untwisted_SM_minimum_duals=2,
       signed_matter_repaired_sextic_uneaten_chiral_modes=89,
       character_certificate="3 x 27 + 8 x 1",
       decomposition_after_SO10_branch=dict(chiral_16s=3,vectorlike_10s=3,
                                                extra_1s_outside_each_16=11),
       perturbative_family_anomaly_net=anomaly["total"],
       open_gates="These results hold for the selected fixed VEV and supplied operators. 89 remaining massless fields, full vectorlike decoupling, radiative mass stability, global anomalies and phenomenological mixing remain open.",
       source_audit="The 78/86 exact source results were new in 43-commit audit; no claim of reproducing the high-cost 48870x6561 exact elimination in this lightweight test.")

def corrected_cosmo_ledger():
    s=read("analysis/toe_uv/scorecard.json")
    names=("fading_cneg","CPL","KLT")
    rows=[]
    for name in names:
        r=s[name]
        expansion=r["oos_gain_dovekie"]
        des=r["shear_heldout_elpd_rel_lcdm"]
        kids=r["shear_heldout_kids_rel_lcdm"]
        total=expansion+des+kids
        assert abs(total-r["oos_gain_dovekie_plus_des_kids_shear"])<1e-9
        rows.append(dict(name=name,linear_expansion_elpd=expansion,
                  DES_heldout_elpd=des,KiDS_heldout_elpd=kids,
                  all_heldout_elpd_total=total,
                  cosmic_shear_discrimination_magnitude=abs(des+kids)))
    f=rows[0];c=rows[1]
    assert f["all_heldout_elpd_total"]>c["all_heldout_elpd_total"]
    assert abs(f["all_heldout_elpd_total"]-c["all_heldout_elpd_total"])<.5
    S9=ROOT/"analysis/toe_uv/prereg_noshear.json"
    assert S9.is_file()
    digest=hashlib.sha256(S9.read_bytes()).hexdigest()
    assert len(digest)==64
    return dict(status="POST_HALOFIT_CORRECTED_SCORECARD_INDEPENDENT_ARITHMETIC_NO_NEW_CHAIN",
       three_models=rows,model_ordering_source_conditional=True,
       fading_minus_CPL_combined_elpd=f["all_heldout_elpd_total"]-c["all_heldout_elpd_total"],
       S9_preregistered_content_sha256=digest,
       S9_future_releases_observed_here=False,
       best_model_claim_not_significant=True,
       caveat="Exact addition of already fitted/held-out source scorecard rows. Covariance/overlap and prior-truncation, multiple comparisons and nonlinear calibration are not independently estimated; these are not recalculated likelihoods or proof of dark energy dynamics.")

def isotropic_dirs(p):
    return [(1,t,(t*t)%p) for t in range(p)]+[(0,0,1)]
def prime_frame_mixture():
    results=[]
    for p in (3,5,7):
        dirs=isotropic_dirs(p)
        mats=[]
        for fr in itertools.combinations(dirs,3):
            B=sp.Matrix.hstack(*(sp.Matrix(x) for x in fr))
            BI=np.asarray(B.inv_mod(p)).astype(int)
            mats.append((BI.T@BI)%p)
        n=len(mats)
        hist=collections.defaultdict(collections.Counter)
        witnesses={}
        for x in itertools.product(range(p),repeat=3):
            z=np.array(x,dtype=int)
            chars=collections.Counter(tuple(int(y) for y in (M@z)%p) for M in mats)
            num=sum(k*k for k in chars.values())
            q=(x[0]*x[2]-x[1]**2)%p
            hist[q][num]+=1
            if (q,num) not in witnesses:witnesses[(q,num)]=x
        assert sum(sum(v.values()) for v in hist.values())==p**3
        assert len(mats)==math.comb(p+1,3)
        fragmented={str(q):len(v) for q,v in hist.items() if len(v)>1}
        examples=[]
        for q in fragmented:
            qs=int(q)
            vals=sorted(hist[qs])
            examples.append(dict(Q=qs,first_input=list(witnesses[(qs,vals[0])]),
               second_input=list(witnesses[(qs,vals[-1])]),
               first_purity=f"{vals[0]}/{n*n}",second_purity=f"{vals[-1]}/{n*n}"))
        results.append(dict(p=p,frames=n,points=p**3,
            exact_purity_census_by_Q={str(q):{f"{u}/{n*n}":v for u,v in sorted(h.items())}
                for q,h in sorted(hist.items())},
            Q_residue_classes_with_nonuniform_purity=fragmented,
            counterexample_same_Q_different_purity=examples,
            all_frame_and_mixture_output_intensities=f"1/{p**3}"))
    assert results[0]["exact_purity_census_by_Q"]=={
      "0":{"16/16":1,"4/16":8},"1":{"4/16":6},"2":{"6/16":12}}
    return dict(status="EXACT_HIGHER_PRIME_NULL_FRAME_MIXTURE_PURITY_AND_GEOMETRIC_COVARIANCE_TEST",
       tested=results,
       normalization_warning="For p>3, projective isotropic directions have no canonical scalar representatives; the specific F_p tensor mixer uses chosen representatives. A purity-class split at fixed determinant Q exposes that the simple p=3 determinant-only census need not be a basis-free PGL2-covariant physical law.",
       phase_visibility="All intensity tables remain uniform; differences require a phase-reference or two-copy purity experiment.")

def fermion_doubling():
    I=np.eye(2, dtype=complex)
    sx=np.array([[0,1],[1,0]],complex)
    sy=np.array([[0,-1j],[1j,0]],complex)
    sz=np.diag([1,-1]).astype(complex)
    A=[np.kron(sx,s) for s in (sx,sy,sz)]
    B=np.kron(sz,I)
    gamma5=np.kron(sx,I)
    assert all(np.max(abs(a@B+B@a))<1e-12 for a in A)
    assert all(np.max(abs(a@gamma5-gamma5@a))<1e-12 for a in A)
    assert np.max(abs(B@gamma5-gamma5@B))>1
    corners=list(itertools.product((0,math.pi),repeat=3))
    counts=collections.Counter()
    gaps=[]
    for k in corners:
        nc=sum(abs(x-math.pi)<1e-9 for x in k)
        chirality=(-1)**nc
        counts[str(chirality)]+=1
        Hnaive=sum((math.sin(k[i])*A[i] for i in range(3)),np.zeros((4,4),complex))
        Hw=Hnaive+sum(1-math.cos(t) for t in k)*B
        eig=np.linalg.eigvalsh(Hw)
        assert max(abs(np.linalg.eigvalsh(Hnaive)))<1e-13
        assert np.max(abs(np.sort(eig)-[-2*nc,-2*nc,2*nc,2*nc]))<1e-11
        gaps.append(dict(pi_momentum_axes=nc,naive_Dirac_zero=True,
                chirality_orientation_sign=chirality,Wilson_absolute_energy_gap=2*nc))
    assert counts=={"+1":4,"-1":4} or counts=={"1":4,"-1":4}
    return dict(status="STANDARD_NIELSEN_NINOMIYA_FINITE_LATTICE_NEGATIVE_CONTROL",
       corner_Dirac_zeros_without_Wilson=8,
       Weyl_orientation_signs=counts,
       Wilson_gap_by_pi_axis_count={str(j):2*j for j in range(4)},
       one_Dirac_cone_remains_after_Wilson=True,
       original_chiral_symmetry_broken_by_Wilson_term=True,
       scope="Three-spatial-dimensional naive free Dirac lattice; classic species doubling, Wilson resolution, not a new SM chiral spectrum, not an anomaly-free Weyl construction. Temporal and interacting-gauge continuum unprovided.")

def antiunitary_chirality():
    # Linear U fixed on basis e0,e1 must fix their +i superposition,
    # whereas complex conjugation sends it to the orthogonal -i one.
    a=np.array([1,1j],complex)/math.sqrt(2)
    k=a.conj()
    fidelity=float(abs(np.vdot(a,k))**2)
    assert abs(fidelity)<1e-14
    t=read("data/w33_split_triality.json")
    kramers=read("data/w33_reflection_is_kramers.json")
    e7=read("data/w33_e7_facet_test.json")
    assert kramers["reflections_are_kramers"] is True
    assert kramers["stats"]=={"(True, 0, 10)":36}
    assert e7["canonical_triple_is_scalene"] is True
    assert e7["n_singular_for_all_three"]==2
    return dict(status="NO_DETERMINISTIC_UNITARY_REALIZES_THE_ODD_ANTIUNITARY_TRIALITY_ON_ALL_STATES",
       native_double_six_kramers_reflections=36,
       native_each_fixed_points=0,native_each_fixed_lines=10,
       E7_60480_candidate_canonical_scalene_triple_passes=True,
       E7_A7_singular_planes_only_two_not_three=True,
       two_basis_state_linear_extension_fidelity_to_conjugation=fidelity,
       inner_product_conjugation_contradiction=True,
       source_triality_key_inventory=sorted(t.keys()),
       cannot_infer_physical_CP_from_combinatorial_reflection=True,
       caveat="General antiunitary no-go is elementary Wigner/complex-linearity mathematics. It is not new to the W33 paper and does not rule out implementing a fixed basis-label transposition as a unitary permutation, or probabilistic state-specific operations.")

def produce():
    return dict(schema="w33.20261109.audit_5plus3_independent_falsifiers.v1",
       audit=revision_review(),frame=spatial_frame_phase(),
       magnetic=native_magnetic_four_spatial(),
       optics=optical_inverse_frame_discriminator(),
       E6=e6_current_flatness_anomaly(),
       cosmology=corrected_cosmo_ledger(),
       prime_frames=prime_frame_mixture(),
       lattice_fermions=fermion_doubling(),
       triality=antiunitary_chirality(),
       claim_boundary="Exact finite combinatorics, rational algebra and binomial statistics plus source certificate replay. No new measured data, 3+1 native continuum, anomaly-safe chiral lattice SM, complete GUT mass spectrum, experimental quantum computer or validated TOE.")
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--out",default="data/toe_20261109_audit_fiveplus3_falsifiers.json")
    args=p.parse_args()
    j=produce();path=ROOT/args.out
    path.parent.mkdir(exist_ok=True,parents=True)
    path.write_text(json.dumps(j,indent=2,sort_keys=True,allow_nan=False)+"\n",encoding="utf-8")
    print(json.dumps(dict(file=str(path),frame_gap=j["frame"]["first_nonzero_interface_energy"],
       magnetic_limit=j["magnetic"]["critical_positive_short_weight"],
       echo_accepted_events=j["optics"]["minimum_accepted_heralded_events"],
       E6_massless=j["E6"]["signed_matter_repaired_sextic_uneaten_chiral_modes"],
       S9_future=j["cosmology"]["S9_future_releases_observed_here"],
       prime_frame_fragments=[(x["p"],x["Q_residue_classes_with_nonuniform_purity"])
                            for x in j["prime_frames"]["tested"]]),indent=2))
