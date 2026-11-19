#!/usr/bin/env python3
"""Five falsifiable physics/code extensions plus the PGL(4,3) logical-action bridge.

See analysis/2026-11-19_TOE_five_frontiers_PGL40_decoder_experimental.md.
Arithmetic is explicit; no emergent GR or UV completion is claimed.
"""
import itertools
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sys.path.insert(0,str(HERE))
import toe_20261119_w33_40_qutrit_css as code

N=40
P=3


def gauge_beta_audit():
    """One-loop UV obstruction/comparison, not an NSVZ fixed-point result."""
    Nc=3
    table=[]
    for nf,model in ((9,"nine-pair, 19-baryon EFT"),(10,"ten-pair, cubic model")):
        b0=3*Nc-nf
        table.append({"model":model,"Nc":Nc,"Nf":nf,"one_loop_b0":b0,
                      "one_loop_classification":("boundary: b0=0" if b0==0
                        else "not asymptotically free" if b0<0
                        else "asymptotically free")})
    assert [x["one_loop_b0"] for x in table]==[0,-1]
    # For 9 identical Q+Qtilde pairs, NSVZ numerator at b0=0 is
    # (1/2)*sum_{18 chiral fields}gamma_i = 9 gamma if all equal.
    return {
        "status":"PASS",
        "gauge_group":"SU(3)",
        "one_loop_beta_coefficient_convention":"b0=3 Nc-Nf",
        "models":table,
        "nine_pair_NSVZ_numerator":"(1/2) sum_{18 fundamental/antifundamental fields} gamma_i",
        "caution":"vanishing b0 does not imply exact beta=0, especially with superpotential couplings",
        "no_claim":["E8 embedding","asymptotic safety","unique RG fixed point",
                    "realistic Standard Model matter","natural SIC couplings"]}


def charged_dirac_pulledback_flux():
    """Analytic nonzero-magnetic-flux extension of the flat Dirac gap."""
    # The sphere/two-torus product Dirac satisfies D²=D_S5²+D_T2,A²
    # for any unitary A pulled back purely from T2. Every eigenvalue
    # is >= (5/(2R))² independently of magnetic index m.
    R=1
    gap=5/(2*R)
    # For the torus with unit coordinate lengths and U(1) curvature,
    # Dirac(T2,A) has |m| zero modes of a given 2d chirality, index m.
    # For 1/3 translations in both directions, flux m divisible by 9
    # has a compatible ordinary abelian magnetic-translation lift
    # with commutator exp(2pi i m/9)=1.
    fluxes=[0,9,18,-9]
    rows=[{"cover_T2_flux":m,"T2_Dirac_index":m,
           "T2_Dirac_zero_mode_number":abs(m),
           "product_Y7_untwisted_direction_gap_lower_bound":gap}
          for m in fluxes]
    for m in fluxes:
        if m%9!=0:raise AssertionError("flux lift not integer")
    assert gap**2==6.25
    return {
        "status":"PASS conditional on smooth equivariant product-pullback connection",
        "background":"(S5(R) x T2)/H27",
        "analytic_identity":"D_product,A² = D_S5² tensor I + I tensor D_T2,A²",
        "round_S5_D_abs_lower_bound":"5/(2R)",
        "independent_of_flux":True,"tested_compatible_U1_fluxes":rows,
        "magnetic_translation_commutator":"exp(2pi i m/9) = 1 for m divisible by 9",
        "interpretation":"nonzero torus magnetic flux creates 2D chiral zero modes but no 7D product Dirac zero modes",
        "not_excluded":["sphere-dependent/non-product gauge connection",
                        "torsionful or supercovariant Dirac",
                        "singular localized charged modes","different compactification"],
        "limit":"uses an analytically known product Dirac spectrum; finite checks only certify integer flux bookkeeping"}


def qutrit_mub_witness():
    """Four-MUB entanglement witness with distribution-free shot guarantee."""
    omega=np.exp(2j*np.pi/3)
    Z=np.diag([1,omega,omega**2])
    X=np.roll(np.eye(3),1,axis=0)
    bases=[np.eye(3,dtype=complex)]
    for b in range(3):
        _,v=np.linalg.eig(X@np.linalg.matrix_power(Z,b))
        bases.append(v)
    bell=np.zeros(9,complex)
    for j in range(3):bell[3*j+j]=1/np.sqrt(3)
    projector=np.outer(bell,bell.conj())
    sum_corr=np.zeros((9,9),complex)
    for V in bases:
        assert np.allclose(V.conj().T@V,np.eye(3),atol=1e-12)
        for j in range(3):
            v=np.kron(V[:,j],V[:,j].conj())
            sum_corr+=np.outer(v,v.conj())
    assert np.allclose(sum_corr,np.eye(9)+3*projector,atol=1e-12)
    # Four complete MUBs on R and conjugate MUBs on S:
    # F=(sum_{4 bases} P_same -1)/3. For separable states F<=1/3,
    # hence sum_{4 bases}P_same<=2 and mean coincidence<=1/2.
    # For rho=(1-p)|Phi><Phi|+p I9/9, coincidence q=1-2p/3.
    alpha=0.01;beta=0.01
    p=0.5
    q=1-2*p/3
    guaranteed=None
    for total in range(4,20000,4):
        delta=np.sqrt(np.log(1/alpha)/(2*total))
        if q-0.5>delta and np.exp(-2*total*(q-0.5-delta)**2)<=beta:
            guaranteed=total;break
    assert guaranteed is not None and guaranteed%4==0
    # Two Hoeffding inequalities: type-I<=1%, power >=99%, valid
    # for independent bounded Bernoulli trials with equal basis allocation.
    # Photon loss can be treated as fair-sampled heralding only by
    # explicitly assuming loss is state/basis independent; otherwise
    # this is not device independent.
    try:
        from scipy.stats import binom
        launched=next(n for n in range(guaranteed,5000)
                      if binom.sf(guaranteed-1,n,0.7)>=0.99)
    except ImportError:
        launched=None
    return {
        "status":"PASS",
        "projector_identity":"sum_four_MUB_coincidence_projectors = I9 + 3|Phi3><Phi3|",
        "fidelity_rule":"F=(sum_{b=1..4} C_b -1)/3",
        "separable_null":"sum C_b <= 2, equivalently mean coincidence <=1/2",
        "isotropic_channel_coincidence":"q=1-2p/3",
        "quantum_entanglement_threshold":"p<3/4",
        "example_storage_depolarization":p,
        "example_coincidence":q,
        "one_sided_Hoeffding_alpha":alpha,
        "minimum_guaranteed_detection_power":1-beta,
        "shots_per_basis":guaranteed//4,
        "total_detection_shots":guaranteed,
        "launched_pulses_for_99pct_to_collect_shots_if_independent_eta0.7":launched,
        "limitations":["finite-shot guarantee assumes independent trials",
                       "lost events discarded only under explicit fair-sampling",
                       "not a loophole-free device-independent quantum-memory witness",
                       "requires isolated entangled reference and verified causal break"]}


def continuum_refinement():
    """Explicit C_m^3 refinement with W33 finite internal fiber."""
    target=4*np.pi**2
    residual=[]
    for m in (8,12,24,48):
        low=4*m*m*np.sin(np.pi/m)**2
        residual.append({"cycle_sites_per_spatial_axis":m,
                         "total_sites":40*m**3,
                         "first_nonzero_spatial_Laplacian_eigenvalue":low,
                         "continuum_target_4pi_squared":target,
                         "relative_error":abs(low-target)/target})
    assert all(residual[i+1]["relative_error"]<residual[i]["relative_error"]
               for i in range(len(residual)-1))
    # L_fiber =12I-A has eigen 0,10(24),16(15).
    return {
        "status":"PASS",
        "graph":"W33 cartesian C_m cartesian C_m cartesian C_m",
        "spatial_dimension_added_by_hand":3,
        "base_fiber_Laplacian_spectrum":{"0":1,"10":24,"16":15},
        "cycle_refinement_residuals":residual,
        "long_wavelength_dispersion":"omega²=c² |k|² for fiber-constant sector at m->infinity",
        "remaining_internal_mass_squares":"10 and 16 at constant fiber edge coupling",
        "no_claim":["spacetime emerges from W33 alone","gravitational equations",
                    "diffeomorphism constraints","physical compactification"]}


def syndrome_key(s):
    # Reduce in signed arithmetic *before* conversion, so -1 -> 2.
    return bytes((np.asarray(s,dtype=np.int64)%3).astype(np.uint8))


def build_decoder(check,max_weight):
    """Minimum-weight lookup for all support weights <= t."""
    table={syndrome_key(np.zeros(check.shape[0],dtype=int)):
           np.zeros(check.shape[1],dtype=np.int8)}
    for w in range(1,max_weight+1):
        for supports in itertools.combinations(range(check.shape[1]),w):
            for coeff in itertools.product((1,2),repeat=w):
                err=np.zeros(check.shape[1],dtype=np.int8)
                for j,k in zip(supports,coeff):err[j]=k
                key=syndrome_key((check@err)%3)
                assert key not in table, "low-weight syndrome collision"
                table[key]=err
    return table


def decoder_guaranteed_probability(p):
    """Independent uniformly distributed nonidentity qutrit Pauli errors."""
    n=40
    p0=1-p;px=p/4;pz=p/4;pb=p/2
    ans=0.
    for both in (0,1):
        for xonly in range(2-both):
            for zonly in range(3-both):
                count=n-both-xonly-zonly
                mult=math.factorial(n)//(math.factorial(both)*math.factorial(xonly)*
                          math.factorial(zonly)*math.factorial(count))
                ans+=mult*(pb**both)*(px**xonly)*(pz**zonly)*(p0**count)
    return ans


def css_decoder():
    _,_,HX,HZ=code.checks()
    Xdict=build_decoder(HZ,1)   # X errors cause Z-check syndrome
    Zdict=build_decoder(HX,2)   # Z errors cause X-check syndrome
    assert len(Xdict)==1+2*40
    assert len(Zdict)==1+2*40+4*math.comb(40,2)
    # Guaranteed correct for *every* X support <=1 and Z support <=2,
    # independently, including overlapping XZ locations.
    rng=np.random.default_rng(11919)
    for _ in range(300):
        x=rng.integers(0,3,size=40,dtype=np.int8)
        z=rng.integers(0,3,size=40,dtype=np.int8)
        a=rng.choice(40,size=1,replace=False)
        b=rng.choice(40,size=2,replace=False)
        maskx=np.zeros(40,dtype=np.int8);maskx[a]=x[a]
        maskz=np.zeros(40,dtype=np.int8);maskz[b]=z[b]
        sx=syndrome_key((HZ@maskx)%3)
        sz=syndrome_key((HX@maskz)%3)
        assert np.array_equal(Xdict[sx],maskx)
        assert np.array_equal(Zdict[sz],maskz)
    return {
        "status":"PASS",
        "code_parameters":"[[40,19,4]]_3",
        "X_distance":4,"Z_distance":6,
        "X_correctable_weight":1,"Z_correctable_weight":2,
        "lookup_syndromes_X":len(Xdict),
        "lookup_syndromes_Z":len(Zdict),
        "mixed_error_robustness":"any X-weight<=1 AND Z-weight<=2, including overlapping sites",
        "independent_depolarizing_p_to_guaranteed_success":{
           str(p):decoder_guaranteed_probability(p) for p in (0.001,0.005,0.01,0.02,0.05)},
        "uniform_T9_transversal":"fails; see extra PGL/gate proof",
        "limitations":["guaranteed-error-pattern bound, not optimal ML logical failure",
                       "perfect syndrome extraction only, no measurement noise",
                       "not a physical gate schedule or threshold"]}


def projective_permutation(M,pts):
    indices={v:i for i,v in enumerate(pts)}
    perm=[]
    for v in pts:
        w=tuple(int(z)%3 for z in (np.asarray(M,dtype=np.int64)@
                                  np.asarray(v,dtype=np.int64)))
        key=min(w,tuple((-z)%3 for z in w))
        perm.append(indices[key])
    assert sorted(perm)==list(range(len(pts)))
    return np.array(perm,dtype=int)


def nullbasis(M):
    R=code.rref_mod3(M)
    pivots=[int(np.flatnonzero(r)[0]) for r in R]
    free=[j for j in range(M.shape[1]) if j not in pivots]
    out=[]
    for j in free:
        v=np.zeros(M.shape[1],dtype=np.int64);v[j]=1
        for index,pivot in enumerate(pivots):v[pivot]=(-R[index,j])%3
        out.append(v)
    return np.array(out,dtype=np.int64)


def solve_basis(B,Vs):
    """Solve coefficient rows V=c B over F3, including all RHS at once."""
    left=B.T.astype(np.int64)%3
    r,n=left.shape
    right=np.asarray(Vs,dtype=np.int64).T%3
    arr=np.column_stack((left,right))
    row=0
    for col in range(n):
        piv=next((i for i in range(row,r) if arr[i,col]),None)
        assert piv is not None
        arr[[row,piv]]=arr[[piv,row]]
        arr[row]=arr[row]*pow(int(arr[row,col]),-1,3)%3
        for i in range(r):
            if i!=row and arr[i,col]:
                arr[i]=(arr[i]-int(arr[i,col])*arr[row])%3
        row+=1
    assert np.all(arr[n:,n:]==0)
    return arr[:n,n:].T


def pgl_code_symmetries():
    pts,A,HX,HZ=code.checks()
    rX=code.rref_mod3(HX)
    rZ=code.rref_mod3(HZ)
    gens=[]
    for i in range(4):
        for j in range(4):
            if i!=j:
                G=np.eye(4,dtype=np.int64);G[i,j]=1
                gens.append((f"E{i}{j}(1)",G))
    gens.append(("diag(-1,1,1,1)",np.diag([2,1,1,1])))
    for _,G in gens:
        perm=projective_permutation(G,pts)
        assert np.array_equal(code.rref_mod3(HX[:,perm]),rX)
        assert np.array_equal(code.rref_mod3(HZ[:,perm]),rZ)
    # GL4(F3) is generated by elementary transvections plus a non-square
    # determinant diagonal; center +/-I acts trivially on projective points.
    GL4=(3**4-1)*(3**4-3)*(3**4-9)*(3**4-27)
    PGL4=GL4//2
    assert PGL4==12130560
    kernel=nullbasis(HZ)
    assert kernel.shape==(30,40)
    rows=[r.copy() for r in rX]
    logical=[]
    current=11
    for v in kernel:
        extended=np.vstack(rows+[v])
        rk=code.rank_mod3(extended)
        if rk>current:
            rows.append(v)
            logical.append(v)
            current=rk
    assert current==30 and len(logical)==19
    full=np.array(rows,dtype=np.int64)
    u=np.eye(4,dtype=int);u[0,1]=1
    perm=projective_permutation(u,pts)
    projective_transvection_logical=solve_basis(full,np.array(logical)[:,perm])[:,11:]
    T=projective_transvection_logical%3
    assert np.array_equal(T@T@T%3,np.eye(19,dtype=np.int64))
    nil=(T-np.eye(19,dtype=int))%3
    rank_nil=code.rank_mod3(nil)
    rank_nil_squared=code.rank_mod3((nil@nil)%3)
    assert (rank_nil,rank_nil_squared)==(10,3)
    # Unipotent Jordan block multiplicities in characteristic three:
    # count(size3)=rank(N^2), count(size2)=rank(N)-2*count(size3),
    # count(size1)=19-2*count(size2)-3*count(size3).
    j3=rank_nil_squared
    j2=rank_nil-2*j3
    j1=19-2*j2-3*j3
    assert (j1,j2,j3)==(2,4,3)
    # Uniform physical T9=diag(zeta9^(j^3)) does not preserve the code:
    # its phase ratio between |0> and |h> within X-stabilizer coset is
    # zeta9^(sum_i h_i^3)=zeta9^13=zeta9^4 != 1.
    row=HX[0]
    assert set(row)=={0,1}
    weight=int(np.count_nonzero(row))
    assert weight==13 and weight%9==4
    return {
       "status":"PASS",
       "generators_tested":len(gens),
       "generators_preserve_both_CSS_check_spaces":True,
       "projective_automorphism_subgroup":"PGL(4,3)",
       "group_order":PGL4,
       "fixed_W33_point_symplectic_group_order":25920,
       "ratio_to_fixed_W33_PSp4":PGL4//25920,
       "logical_dimension":19,
       "order_three_transvection_logical_order":3,
       "transvection_rank_T_minus_identity":rank_nil,
       "transvection_rank_square_T_minus_identity":rank_nil_squared,
       "unipotent_logical_Jordan_block_multiplicities":{"size1":j1,"size2":j2,"size3":j3},
       "uniform_ninth_root_T_gate_is_transversal_logical":False,
       "physical_HX_row_weight":weight,
       "relative_T9_phase_exponent_mod9":weight%9,
       "boundary":["prior W33 classical code is PGL-invariant via 234 polarities",
                   "no full hardware gate-set or universal logical gate",
                   "non-uniform transversal gates or magic injection not excluded"]
    }


def certify():
    result={
      "study":"2026-11-19 TOE five fronts plus PGL four-dimensional projective lift",
      "gauge_SIC_UV":gauge_beta_audit(),
      "nonflat_torus_flux_Dirac":charged_dirac_pulledback_flux(),
      "four_MUB_memory_witness":qutrit_mub_witness(),
      "refinement_Lorentz_falsifier":continuum_refinement(),
      "asymmetric_CSS_decoder":css_decoder(),
      "PGL40_logical_symmetry_and_T9_nogo":pgl_code_symmetries()
    }
    assert all("PASS" in report["status"] for report in list(result.values())[1:])
    return result


def main():
    result=certify()
    target=ROOT/"data"/"toe_20261119_pgl40_five_frontiers.json"
    target.write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps({"status":"PASS","PGL4_order":result["PGL40_logical_symmetry_and_T9_nogo"]["group_order"],
       "logical_transvection_rank":result["PGL40_logical_symmetry_and_T9_nogo"]["transvection_rank_T_minus_identity"],
       "decoder_syndromes_Z":result["asymmetric_CSS_decoder"]["lookup_syndromes_Z"],
       "shots":result["four_MUB_memory_witness"]["total_detection_shots"],
       "output":str(target)}))


if __name__=="__main__":
    main()
