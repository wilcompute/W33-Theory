#!/usr/bin/env python3
"""Equal-source-shot Fisher comparison of four W33/Q8 readout architectures.

Uses exact projective measurement frame matrices from existing *frozen*
reproducible designs. Internal component exposure/loss is a separately
stated uniform-transmission HARDWARE PROXY, not a full noncommuting-loss
POVM simulation. Per-launched-photon Fisher normalizes settings count.
"""
import hashlib,json,math,sys
from pathlib import Path
import numpy as np
from w33_20261109_q8_ten_context_tomography import select,projection_design
from w33_20261109_q8_ten_context_optimize import main as opt
from w33_20261109_shallow_cz_complete import candidate
from w33_20261109_q8_perm_fourier_phases_27 import make,invcount
from w33_20261109_q8_12setting_completion import product_mub
from w33_20261109_q8_five_extensions import horodecki_state
from w33_20261109_q8_horodecki_ccnr_exact import realign

ROOT=Path(__file__).resolve().parents[1]
def frozen(name):
    return json.loads((ROOT/"data"/(name+".json")).read_text(encoding="utf8"))

def two_cz():
    saved=frozen("w33_20261109_shallow_cz_complete")
    rng=np.random.default_rng(20261109673)
    for _ in range(20):candidate(rng,False);candidate(rng,False)
    for _ in range(950):candidate(rng,True);candidate(rng,True)
    idx=saved["best_candidate_index"]
    for k in range(idx+1):
        U=candidate(rng,True,True);V=candidate(rng,True,True)
    digest=hashlib.sha256(np.stack([U,V]).tobytes()).hexdigest()
    assert digest==saved["two_basis_complex_sha256"],(digest,saved["two_basis_complex_sha256"])
    return [U,V]

def fourier():
    saved=frozen("w33_20261109_q8_perm_fourier_phases_27")
    p,q=saved["first_permutation"],saved["second_permutation"]
    a,b=saved["programmed_diagonal_phase_masks"]
    U,V=make(np.array(a),p,0),make(np.array(b),q,1)
    digest=hashlib.sha256(np.stack([U,V]).tobytes()).hexdigest()
    assert digest==saved["matrix_digest_sha256"]
    return [U,V],[invcount(p),invcount(q)]

def designs():
    x,(bell,Ug,Vg,ops)=opt(return_components=True)
    assert len(ops)==80
    bs=[bell[:,9*j:9*(j+1)] for j in range(8)]
    UF,inv=fourier()
    UC=two_cz()
    product,_=product_mub()
    B12=[np.kron(U3,U3) for U3 in product]
    result={
       "generic_9mode":[bs+[Ug,Vg],[15,15],[0,0],[1,1]],
       "permutation_Fourier":[bs+UF,[9,9],inv,[1,1]],
       "two_CZ_local":[bs+UC,[12,12],[0,0],[2,2]],
       "matched_12_product":[bs+B12,[0,6,6,6],[0]*4,[0,1,1,1]]}
    return result,ops

def report_design(name,meta,ops,rho,dual_h,gate_t,cross_t,phase_t):
    bases,depths,crosses,phases=meta
    K=len(bases)
    rows=[];F=np.zeros((80,80))
    for j,U in enumerate(bases):
        if j<8:trans=1.
        else:
            i=j-8
            trans=(gate_t**depths[i])*(cross_t**crosses[i])*(phase_t**phases[i])
        A=projection_design(U,ops)
        p=np.real(np.diag(U.conj().T@rho@U))
        assert min(p)>1e-13,(name,min(p))
        F+=trans*(A.T/p)@A
        rows.append({"context":j,
              "nominal_photon_survival_fraction":trans,
              "per_mode_gate_exposure_proxy":0 if j<8 else depths[j-8],
              "routing_crossing_upper_proxy":0 if j<8 else crosses[j-8],
              "phase_mask_exposure":0 if j<8 else phases[j-8]})
    F/=K # equal total *source* shots, distributed over all contexts
    eig=np.linalg.eigvalsh(F)
    assert min(eig)>1e-12
    inv=np.linalg.inv(F)
    M=np.vstack([projection_design(U,ops) for U in bases])
    s=np.linalg.svd(M,compute_uv=False)
    return {"contexts":K,"ideal_frame_condition":float(s[0]/s[-1]),
            "uniform_transmission_model":"T=t_gate^max_rail_exposure * t_cross^fixed_swap_count * t_phase^phase_mask_passes, first 8 Bell contexts assumed ideal",
            "per_launched_photon_Fisher_smallest_eigenvalue":float(eig[0]),
            "per_launched_photon_inverse_Fisher_trace":float(np.trace(inv)),
            "per_launched_photon_CCNR_dual_Cramer_Rao_variance_coefficient":float(dual_h@inv@dual_h),
            "min_extra_analyzer_survival":min(t["nominal_photon_survival_fraction"] for t in rows[8:]),
            "extra_context_records":rows[8:]}

def main(path=None):
    designs_,ops=designs()
    rho=horodecki_state(.236)
    r=realign(rho)
    u,s,vh=np.linalg.svd(r)
    W=u@vh
    h=np.array([float(np.vdot(W,realign(H)).real) for H in ops])
    cases={"ideal":(1.,1.,1.),
           "moderate":(.995,.99,.999),
           "harsh":(.98,.97,.995)}
    outputs={}
    for label,(g,c,p) in cases.items():
        outputs[label]={name:report_design(name,meta,ops,rho,h,g,c,p)
            for name,meta in designs_.items()}
    # Benchmark exclusively for specific numerical scenario; it cannot
    # establish a state-independent architecture ordering.
    for label in outputs:
        assert all(x["per_launched_photon_Fisher_smallest_eigenvalue"]>0 for x in outputs[label].values())
    out={"status":"PASS_EQUAL_TOTAL_SOURCE_PULSES_4_ARCHITECTURE_FISHER_PROXY",
         "benchmark_state":"two-qutrit Horodecki a=0.236 PPT entangled",
         "scenario_rates":{"ideal":{"coupler":1.,"fixed_crossing":1.,"phase_mask":1.},
                           "moderate":{"coupler":.995,"fixed_crossing":.99,"phase_mask":.999},
                           "harsh":{"coupler":.98,"fixed_crossing":.97,"phase_mask":.995}},
         "model_outputs":outputs,
         "architecture_input_hashes":{
             "generic":frozen("w33_20261109_q8_ten_context_optimize")["refined_2bases_sha256"],
             "Fourier":frozen("w33_20261109_q8_perm_fourier_phases_27")["matrix_digest_sha256"],
             "two_CZ":frozen("w33_20261109_shallow_cz_complete")["two_basis_complex_sha256"]},
         "scope":"The optical loss is UNIFORM per context with component-exposure proxies, not a measured photonic device or true internal noncommuting-loss POVM. No detector efficiency/crosstalk/phase drift is included. Fisher bound is locally evaluated at one Horodecki state and assumes trusted ideal projective probabilities with losses, equal total source pulses split among contexts, and asymptotic unbiased estimation. Real architecture decisions need calibrated full POVMs.",
         "comparison_principle":"A lower Cramer–Rao variance coefficient is better for the chosen trace-norm polar dual in the independent idealized shot model; it does not guarantee finite-sample entanglement confidence."}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS four optics benchmarks",json.dumps({
      label:{n:round(v["per_launched_photon_CCNR_dual_Cramer_Rao_variance_coefficient"],3)
             for n,v in table.items()} for label,table in outputs.items()}))
    return out
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
