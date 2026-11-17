"""Proton-decay conditional dressing and experimental constraint.

Rate normalization Gamma[p->K nu] = mp/(32pi)*(1-mK²/mp²)^2 *
 |W_K*C6|² (one coherent effective operator/chirality).
W_K in GeV², C6 in GeV^-2, Gamma in GeV.
This assumes the standard spinor/form-factor convention; interference,
flavor and chirality channels must be included in real fits.

Dominant wino-like toy dressing:
C6 = A_RG * g2²/(16pi²) * (m_wino/m_sq²) * floop *
 (y_u*y_d)/Mtriplet .
This is a controlled dimensional estimate, NOT a complete SUSY
operator-running or superpartner-dressing calculation.
"""
import math,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_proton_Knu_conditional_bound.json"
HBAR=6.582119569e-25
YEAR=365.25*24*3600
MP=.9382720813
MK=.493677
LIMIT=8.2e33
PHASE=MP/(32*math.pi)*(1-(MK/MP)**2)**2
def limit_c6(lifetime=LIMIT,W=.1):
    return math.sqrt(HBAR/(lifetime*YEAR*PHASE))/abs(W)
def rate(C6,W=.1):
    gamma=PHASE*(W*C6)**2
    return math.inf if gamma==0 else HBAR/(YEAR*gamma)
def model(Mtriplet=5e16,ymul=1e-6,mw=1e3,ms=1e4,
          g2=.65,ARG=2.,loop=1.,W=.1):
    if min(Mtriplet,mw,ms,g2,ARG,loop,W)<=0 or ymul<0:
        raise ValueError("all masses and strengths positive")
    dress=ARG*g2*g2/(16*math.pi*math.pi)*mw/(ms*ms)*loop
    c6=dress*ymul/Mtriplet
    return {"M_triplet_GeV":Mtriplet,"yukawa_product":ymul,
      "wino_GeV":mw,"sfermion_GeV":ms,"RG_factor":ARG,
      "loop_shape_factor":loop,
      "dressing_factor_inverse_GeV":dress,
      "coefficient_C6_GeV_minus2":c6,
      "lifetime_years":rate(c6,W),
      "required_triplet_GeV_for_this_yukawa_product":dress*ymul/limit_c6(W=W),
      "passes_single_operator_bound":c6<=limit_c6(W=W)}
def verify():
    bound=limit_c6()
    assert 2e-31<bound<2.5e-31
    assert abs(rate(bound)/LIMIT-1)<1e-12
    weak=model(ymul=1e-8)
    strong=model(ymul=1e-6)
    assert weak["passes_single_operator_bound"]
    assert not strong["passes_single_operator_bound"]
    assert abs(strong["coefficient_C6_GeV_minus2"]/weak["coefficient_C6_GeV_minus2"]-100)<1e-12
    assert abs(strong["lifetime_years"]/weak["lifetime_years"]-1e-4)<1e-10
    rows=[model(ymul=y,ms=ms) for y in (1e-8,1e-7,1e-6)
                            for ms in (5e3,1e4,3e4)]
    return {"status":"PASS_CONDITIONAL_PROTON_KNU_D5_D6_BOUNDS",
       "source_experiment":"Super-Kamiokande FY2025 results talk from January 29 2026: tau(p->anti_nu K+) > 8.2e33 years, 90% confidence, 365 kt years. URL https://www-sk.icrr.u-tokyo.ac.jp/~nakahata_s/kakenhi-kibanS/talk/Nakahata_SuperK_KMI2025_250305.pdf",
       "lattice_hadronic_W0_reference_GeV2":.1,
       "lattice_W0_example_source":"PACS lattice 2024 proceedings https://pos.sissa.it/466/435/pdf; reference .1 GeV² is an illustrative channel-dependent scale, NOT a universal matrix element",
       "phase_space_GeV":PHASE,
       "single_operator_C6_upper_GeV_minus2":bound,
       "effective_cutoff_for_C6_coefficient_one_GeV":1/math.sqrt(bound),
       "reference_dressing":{"g2":.65,"m_wino_GeV":1000,"m_sfermion_GeV":10000,"A_RG":2,"loop_factor":1},
       "weak_reference":weak,"strong_reference":strong,"scan":rows,
       "required_further_physics":"Full flavor matrices, CKM/PMNS rotations, LLLL/RRRR dressing, sfermion spectra, threshold running, all interfering hadronic W0 channels, SUSY spectrum and experiment-specific acceptance.",
       "physics_claim_level":"Conditional single-amplitude experimental constraint, not a prediction or exclusion of the E6 vacuum."}
if __name__=="__main__":
    r=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(r["status"],r["single_operator_C6_upper_GeV_minus2"],r["strong_reference"]["lifetime_years"])
