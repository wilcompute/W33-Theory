"""Five independent gates for a realistic TOE, deliberately not W33-dependent.

1. Compact 3D Morse/Witten index obstruction and E8 mirror-mixing Yukawa rank.
2. Asymptotically free SU4 -> SU3 vectorlike parent for a nine-qutrit SIC.
3. Parametrized-string 1+1 diffeomorphism constraint bracket discretization.
4. Single-photon logical capacity plus event-ready qutrit memory witness.
5. Measured SM gauge-coupling one-loop RGE consistency and SUSY comparator.

Theorems are conditional on explicitly stated models. Not a TOE or 11D solution.
"""
from itertools import combinations,product
from math import comb,exp,log,log10,pi,sqrt,ceil
from pathlib import Path
import json
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
np.set_printoptions(precision=9)

def independent_chirality_gate():
    # f=Re(w^4)/4-(x^2+y^2)/2+z^2-x, from the new noncompact E8/PW local profile.
    # df/dy=y(y^2-3*x^2-1).  Case 1: y=0 => x^3-x-1=0.
    # Case 2: y!=0 => y^2=3x^2+1 and -8x^3-4x-1=0.
    x0=np.roots([1,0,-1,-1])
    x1=np.roots([8,0,4,1])
    xr0=[float(z.real) for z in x0 if abs(z.imag)<1e-10]
    xr1=[float(z.real) for z in x1 if abs(z.imag)<1e-10]
    assert len(xr0)==len(xr1)==1
    q=xr1[0]
    stationary=[(xr0[0],0.,0.),(q,sqrt(3*q*q+1),0.),(q,-sqrt(3*q*q+1),0.)]
    critical=[]
    for x,y,z in stationary:
        grad=np.array([x**3-3*x*y*y-x-1,y**3-3*x*x*y-y,2*z])
        Hess=np.array([[3*x*x-3*y*y-1,-6*x*y,0],
                       [-6*x*y,3*y*y-3*x*x-1,0],
                       [0,0,2]],float)
        eigen=np.linalg.eigvalsh(Hess)
        sign=int(np.sign(np.linalg.det(Hess)))
        assert np.linalg.norm(grad)<1e-10 and min(abs(eigen))>1e-3 and sign==-1
        critical.append({"xyz":[x,y,z],"Hessian_eigenvalues":eigen.tolist(),
                         "local_gradient_index":sign})
    assert sum(c["local_gradient_index"] for c in critical)==-3
    # The boundary of a 4-simplex triangulates S^3: V,E,F,tetrahedra=5,10,10,5.
    euler_sphere3=5-10+10-5
    euler_torus3=1-3+3-1
    assert euler_sphere3==euler_torus3==0
    # E8 source spectrum: 6 chiral 16 plus 3 bar16; each allowed 16-16-10
    # bare cubic involves exactly one distinguished 16 (sheet 3).
    rng=np.random.default_rng(2026111901)
    exceptional_rank=[]
    for _ in range(64):
        u=np.zeros(6,dtype=complex);u[2]=1
        v=rng.normal(size=6)+1j*rng.normal(size=6);v[2]=0
        Y=np.outer(u,v)+np.outer(v,u)
        mirror=rng.normal(size=(3,6))+1j*rng.normal(size=(3,6))
        _,singular,Vh=np.linalg.svd(mirror,full_matrices=True)
        assert singular[-1]>1e-3
        low=Vh.conj().T[:,3:]
        assert np.linalg.norm(mirror@low)<1e-12
        lightY=low.T@Y@low
        rankY=int(np.linalg.matrix_rank(lightY,tol=1e-9))
        assert rankY<=2 and abs(np.linalg.det(lightY))<1e-10
        exceptional_rank.append(rankY)
    assert set(exceptional_rank)=={2}
    gravity=np.array([102,141,49])
    spin10=np.array([12,15,7])
    u=np.cross(gravity,spin10)
    d=int(np.gcd.reduce(abs(u)))
    primitive=(u//d).tolist()
    assert primitive==[14,-7,-9]
    return {
        "f1_local_critical_points":critical,"local_gradient_index_sum":-3,
        "closed_three_manifold_Euler_chi":"0 by Poincare duality",
        "S3_boundary_simplex_euler":euler_sphere3,"T3_euler":euler_torus3,
        "compactness_obstruction":"A globally smooth exact Cartan Witten/deRham complex on a closed 3-manifold has signed index zero. A noncompact local index -3 needs compensating +3 or changing smooth/closed/exact assumptions. This DOES NOT forbid singular/flux compactifications.",
        "Spin10_16s":6,"Spin10_bar16s":3,"net_16_chirality_index":3,
        "bare_six_family_star_Yukawa_rank_upper_bound":2,
        "random_full_rank_three_mirror_mixings_checked":len(exceptional_rank),
        "projected_three_light_family_Yukawa_ranks":sorted(set(exceptional_rank)),
        "rank_proof":"Y=e_star v.T+v e_star.T has rank<=2. For any 6x3 light-family embedding N (including generic mixing with three mirrors), Y_light=N.T Y N has rank<=2. Higgs-independent linear vectorlike decoupling cannot lift it.",
        "local_source_gravitational_U1_anomaly_vector":gravity.tolist(),
        "local_source_Spin10_U1_anomaly_vector":spin10.tolist(),
        "primitive_common_mixed_anomaly_kernel":primitive,
        "local_source_primitive_kernel_pure_cubic":49032,
        "U1_conclusion":"Using the local source anomaly values, the only line canceling both mixed anomalies has nonzero pure cubic, so no additional massless anomaly-free U1 combination of these three without spectrum changes or inflow.",
        "limits":"Local net3 and anomalies are inputs from d67b942, not independently recomputed here. Compact index theorem applies to a smooth exact Witten/deRham complex, not a general singular chiral 7D model. Yukawa obstruction applies to bare Higgs-linear star texture with Higgs-independent mirror mixing, not all higher-dimensional operators."}

def asymptotically_free_parent():
    # SU4 vectorlike Nf10 allows an intermediate SU4 -> SU3 Higgs branch.
    Nc=4;Nf=10
    b0=3*Nc-Nf
    assert b0==2
    V=12.;r=.15
    w=np.exp(2j*pi/3)
    fid=np.array([0,1,-1],complex)
    sic=np.column_stack([np.roll(fid*np.array([1,w**b,w**(2*b)]),a)
                         for a in range(3) for b in range(3)])
    assert np.allclose(sic@sic.conj().T,6*np.eye(3))
    Q=np.zeros((4,10),complex)
    Q[:3,:9]=r*sic
    Q[3,9]=V
    P=Q.conj().T
    moment=Q@Q.conj().T-P.conj().T@P
    assert np.max(np.abs(moment))<1e-14
    # At intermediate scale only Q9, P9 have VEV: stabilizer is SU3.
    # After SIC, generic 9 columns span C3 so no continuous gauge symmetry left.
    assert np.linalg.matrix_rank(Q[:3,:9])==3
    # SU4 baryon of 3 selected qutrit columns and Higgsing flavor is nonzero.
    B=np.linalg.det(Q[:,[0,1,3,9]])
    assert abs(B)>0
    # No antisymmetric tensor was included; quartic baryon constraints are not renormalizable.
    return {"UV_gauge":"N=1 SU4, Nf10 vectorlike fundamentals plus antifundamentals",
            "SU4_perturbative_one_loop_b0":b0,
            "UV_vectorlike_cubic_gauge_anomaly":Nf-Nf,
            "Higgsing_pattern":"SU4 -> SU3 with one vectorlike flavor VEV; nine pairs remain",
            "intermediate_SU3_b0_if_nine_light_flavors":3*3-9,
            "full_Dflat_moment_max_abs":float(np.max(np.abs(moment))),
            "Higgsing_vev_over_SIC_scale":V/r,
            "lifted_SIC_frame_eigenvalues":np.linalg.eigvalsh(Q[:3,:9]@Q[:3,:9].conj().T).tolist(),
            "SU4_baryon_three_SIC_plus_Higgsing_flavor_abs":float(abs(B)),
            "anomaly_free_asymptotically_free_parent_exists_for_matter_content":True,
            "critical_missing_step":"A UV-complete holomorphic gauge-invariant F-flat superpotential naturally selecting the SIC and a scale hierarchy, plus matching of heavy fields/thresholds and SM survival. A quartic SU4 baryon is nonrenormalizable without mediators."}

def center(f):
    h=2*pi/len(f)
    return (np.roll(f,-1)-np.roll(f,1))/(2*h)

def spectral(f):
    n=len(f)
    k=np.fft.fftfreq(n,d=1/n)
    return np.fft.ifft(1j*k*np.fft.fft(f)).real

def covariance_test():
    # Parametrized relativistic string/1+1 embedding constraints H[N],D[xi].
    # Their continuum first-class algebra is {H[N],H[M]}=D[N M'-M N'].
    def defect(n,modes,D):
        t=np.linspace(0,2*pi,n,endpoint=False)
        a,b,c=modes
        N=np.sin(a*t)+.2*np.cos(a*t)
        M=np.cos(b*t)+.3*np.sin(b*t)
        X=np.column_stack([np.sin(c*t),np.cos((c-1)*t)])
        P=np.column_stack([np.cos(2*t),np.sin(3*t)])
        Xp=np.column_stack([D(X[:,k]) for k in range(2)])
        lhs=np.zeros(n)
        rhs=np.zeros(n)
        for k in range(2):
            lhs+=P[:,k]*(N*D(M*Xp[:,k])-M*D(N*Xp[:,k]))
            rhs+=P[:,k]*(N*D(M)-M*D(N))*Xp[:,k]
        return float(np.linalg.norm(lhs-rhs)/max(1e-12,np.linalg.norm(rhs)))
    rows=[{"N":n,"centered_bracket_defect":defect(n,(2,3,5),center),
           "spectral_bracket_defect":defect(n,(2,3,5),spectral)}
           for n in (32,64,128,256)]
    assert max(x["spectral_bracket_defect"] for x in rows)<1e-11
    assert min(rows[i]["centered_bracket_defect"]/rows[i+1]["centered_bracket_defect"]
               for i in range(3))>3.2
    alias=defect(32,(9,10,12),spectral)
    assert alias>.1
    return {"target":"Parametrized free string in flat 1+1 target, first-class classical Hamiltonian and diffeomorphism constraints",
            "H_density":"1/2*(eta^{ab} P_a P_b + eta_ab Xprime^a Xprime^b)",
            "D_density":"P_a Xprime^a",
            "continuum_HH":"{H[N],H[M]}=D[N Mprime - M Nprime]",
            "continuum_HD":"{H[N],D[xi]}=H[N xi_prime - xi Nprime]",
            "continuum_DD":"{D[xi],D[eta]}=D[xi eta_prime - eta xi_prime]",
            "numeric_bracket_test":rows,"high_frequency_alias_defect":alias,
            "finite_local_derivation_no_go":"C^n pointwise derivations zero; even low-mode spectral exactness is not full off-shell finite-grid closure.",
            "limits":"A covariant worldsheet benchmark with fixed target Minkowski metric, not field-dependent 3+1 Einstein gravity; discrete tests assess sampled brackets, not all 3 constraints universally."}

def quantum_resource_gate():
    modes=[{"logical_qubits":n,"minimum_single_photon_orthogonal_modes":2**n,
            "nonoverlap_1ns_time_bin_duration_seconds":(2**n)*1e-9}
           for n in (4,10,20,30,40,60)]
    assert modes[0]["minimum_single_photon_orthogonal_modes"]==16
    assert (2**5)<=40<(2**6)
    # SWAP memory has reference entanglement rank 3; pure-state storage
    # requires an environment with Schmidt rank >=3, i.e. dim(E)>=3.
    p=.2
    eta_min=1/(3*(1-8*p/9))
    assert .40<eta_min<.41
    # Unencoded T9 injection with three output-dependent Clifford corrections,
    # independently of any specific quantum code (prior protocol).
    w=np.exp(2j*pi/3);zeta=np.exp(2j*pi/9)
    U=np.array([zeta**(j**3) for j in range(3)])
    rng=np.random.default_rng(11192026)
    worst=0.0
    for m in range(3):
        phi=(np.arange(3)+m)%3
        corr=U/U[phi]
        relative=corr/corr[0]
        expect=[np.ones(3),np.array([1,w,1]),np.array([1,1,w*w])][m]
        assert np.allclose(relative,expect,atol=1e-13)
        for _ in range(16):
            state=rng.normal(size=3)+1j*rng.normal(size=3)
            state/=np.linalg.norm(state)
            branch=state*U[phi]/sqrt(3)
            assert abs(np.vdot(branch,branch).real-1/3)<1e-12
            worst=max(worst,float(np.linalg.norm(corr*branch*sqrt(3)-U*state)))
    assert worst<1e-12
    return {"single_photon_mode_capacity":"An arbitrary n-qubit pure register has Hilbert dimension 2^n; a single photon restricted to M orthogonal modes has dim M. Exact faithful encoding requires M>=2^n.",
            "examples":modes,"max_qubits_in_40_single_photon_modes":5,
            "time_bin_1ns_assumption":"Duration bound applies only to sequential nonoverlapping time bins with >=1 ns separation, not general frequency/OAM multiplexing.",
            "one_photon_scalability_caveat":"Cannot claim polynomial-resource BQP on n logical qubits by relabeling 2^n single-photon modes as qubits; continuous-variable addressing may hide exponential precision/bandwidth costs. Additional photons/nonlinearities/encoding assumptions can change the model.",
            "qutrit_memory_min_environment_Schmidt_rank":3,
            "event_ready_memory_p_depolarization":p,
            "required_detection_efficiency_to_beat_entanglement_breaking_1over3":eta_min,
            "T9_one_qudit_injection_outcomes_tested":48,"T9_injection_worst_statevector_error":worst,
            "T9_boundaries":"This reproduces a known unencoded qudit Clifford feed-forward identity; it is NOT an encoded, fault-tolerant universal computation protocol."}

def gauge_running_gate():
    # Near-Z MS-bar numbers, deliberately declared as physical input.
    inv_alpha=127.930
    sin2=.23122
    alpha_s=.1177
    MZ=91.1876
    invA=[inv_alpha*(3/5)*(1-sin2), inv_alpha*sin2, 1/alpha_s]
    bSM=[41/10,-19/6,-7]
    bSUSY=[33/5,1,-3]
    def crossing(inv,b,mu):
        out={}
        for i,j in [(0,1),(0,2),(1,2)]:
            L=2*pi*(inv[i]-inv[j])/(b[i]-b[j])
            out[f"{i+1}{j+1}"]=mu*exp(L)
        L=2*pi*(inv[0]-inv[1])/(b[0]-b[1])
        ran=[inv[i]-b[i]*L/(2*pi) for i in range(3)]
        return out,ran,ran[2]-ran[0]
    crossSM,valuesSM,deltaSM=crossing(invA,bSM,MZ)
    assert 1e13<crossSM["12"]<2e13
    assert -6<deltaSM<-5
    crossToy,valuesToy,deltaToy=crossing(invA,bSUSY,MZ)
    # More useful comparison: SM up to a 1 TeV step, MSSM above.
    threshold=1000.
    L=log(threshold/MZ)
    invTeV=[invA[i]-bSM[i]*L/(2*pi) for i in range(3)]
    crossTeV,valuesTeV,deltaTeV=crossing(invTeV,bSUSY,threshold)
    assert -.8<deltaTeV<-.4
    return {
      "inputs":{"alpha_em_MSbar_inverse_MZ":inv_alpha,
                "sin_squared_MSbar_weak_angle_MZ":sin2,
                "alpha_s_MSbar_MZ":alpha_s,"MZ_GeV":MZ},
      "input_sources":["PDG 2025/2026 electroweak reviews: approximate alphaMSbar^-1 127.930 and sin²hatThetaW=.23122",
                       "PDG 2026 electroweak review external-input constraint: alpha_s(MZ)=.1177 +/- .0009"],
      "GUT_hypercharge_normalization":"alpha1=(5/3)*alphaY",
      "inverse_couplings_at_MZ":invA,
      "beta_SM":bSM,"beta_idealized_MSSM":bSUSY,
      "SM_one_loop_pairwise_crossing_GeV":crossSM,
      "SM_at_alpha1_alpha2_crossing":valuesSM,
      "SM_inverse_alpha3_mismatch":deltaSM,
      "MSSM_artificially_at_MZ_crossings":crossToy,
      "MSSM_artificially_at_MZ_inverse_alpha3_mismatch":deltaToy,
      "SM_to_1TeV_then_MSSM_crossings":crossTeV,
      "SM_to_1TeV_then_MSSM_inverse_alpha3_mismatch":deltaTeV,
      "physics_requirement":"A claimed unification must output thresholds/particle spectrum and two-loop matching, then reproduce all three measured couplings. Matching finite-group dimensions or a single alpha is insufficient.",
      "limits":"One-loop illustration with approximate electroweak inputs and abrupt idealized SUSY thresholds; not precise predictions, not evidence that MSSM is realized, not an E8 compactification."}

def main():
    out={"chirality_and_mirror_rank":independent_chirality_gate(),
         "asymptotically_free_parent":asymptotically_free_parent(),
         "worldsheet_covariance_benchmark":covariance_test(),
         "single_photon_and_qutrit_resources":quantum_resource_gate(),
         "SM_coupling_running":gauge_running_gate()}
    dst=ROOT/"data"/"toe_20261119_five_physical_gates_beyond_W33.json"
    dst.write_text(json.dumps(out,indent=2)+"\n",encoding="utf8")
    for key in out:print("PASS",key)
    print("LOCAL_INDEX",out["chirality_and_mirror_rank"]["local_gradient_index_sum"],
          "MIRROR_YUKAWA_RANK",out["chirality_and_mirror_rank"]["projected_three_light_family_Yukawa_ranks"])
    print("SU4_B0",out["asymptotically_free_parent"]["SU4_perturbative_one_loop_b0"])
    print("SM_RGE_DELTA",out["SM_coupling_running"]["SM_inverse_alpha3_mismatch"])
    print(dst)
    return out

if __name__=="__main__":
    main()
