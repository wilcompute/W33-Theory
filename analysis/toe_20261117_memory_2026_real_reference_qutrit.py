"""2026 measured-memory reference budgets for the trusted four-MUB qutrit
event-ready witness. Vendor/paper numbers are NOT qutrit certification.

Published 2026 integrated memory references:
- PRL accepted Sept 30 2026: 90.2(4)% storage AND retrieval efficiency
  for single-photon-level WEAK COHERENT pulses; 99.3(1)% time-bin
  QUBIT conditional fidelity (Pr:Y2SiO5 waveguide cavity).
- 2026 11-channel 151Eu:Y2SiO5 integrated RAQM reports 39.2(2)%
  first AFC echo storage efficiency. Different devices/protocols:
  not a like-for-like comparison.

Hypothetical qutrit source visibility .75, phase sigma .15, detector
pair efficiency .81, path throughput .95; independent trusted bases
and calibrated null p0=.51. For n memory arms,
p_gross=.81 * eta_mem**n * .95 * f_router**2 * q.
We compute required router, KL evidence scale, and QND pre-basis
herald alternative. All numbers are SCENARIO analyses.
"""
import math,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261117_2026_memory_hardware_qutrit_feasibility.json"
def q(v=.75,sigma=.15):
    return 1/3+v*(1+3*math.exp(-sigma*sigma))/6
def dkl(p,p0=.51):
    assert 0<p<1 and 0<p0<1
    return p*math.log(p/p0)+(1-p)*math.log((1-p)/(1-p0))
def scenario(eta,n,path=.95,router=.95):
    assert eta>0 and eta<=1 and n in (1,2)
    base=.81*eta**n*path*q()
    p=base*router*router
    fmin=math.sqrt(.51/base)
    KL=dkl(p) if p>.51 else 0.
    return {"memory_efficiency":eta,"number_memory_arms":n,
      "path_efficiency":path,"per_router_efficiency":router,
      "max_gross_success_per_prep_ideal_routers":base,
      "minimum_symmetric_router_efficiency":fmin,
      "feasible_even_if_router_perfect":fmin<1,
      "gross_matched_herald_probability":p,
      "violates_trusted_witness_under_model":p>.51,
      "expected_log_evalue100_information_scale_herald_trials":
        math.log(100)/KL if KL>0 else None}
def qnd_prebasis(eta,n,path=.95,router=.95):
    accepted=eta**n
    # only HERALD success on memory retrieval, before basis setting,
    # then p conditional is insensitive to pre-herald loss.
    p_cond=.81*path*router**2*q()
    fmin=math.sqrt(.51/(.81*path*q()))
    return {"memory_arms":n,"memory_efficiency":eta,
       "physical_prebasis_nondestructive_herald_REQUIRED":True,
       "herald_rate_fraction_in_ideal_independent_model":accepted,
       "conditional_p_after_prebasis_herald":p_cond,
       "minimum_symmetric_router":fmin,
       "trusted_witness_conditional_pass":p_cond>.51,
       "source_attempts_per_accepted_herald":1/accepted,
       "not_postselection":"The success flag must be before fresh secret basis choice and local, with no setting leakage. Ordinary destructive photon detection after the basis is selected does not qualify."}
def verify():
    rows=[]
    for eta,label in ((.902,"2026_PRL_weak_coherent_qubit_reference"),
                      (.392,"2026_11channel_first_echo_reference")):
        for n in (1,2):
            for f in (.95,.97,.99,.995,1.):
                rows.append({"source_label":label,**scenario(eta,n,router=f)})
    lookup=lambda eta,n,f:scenario(eta,n,router=f)
    assert .94<lookup(.902,1,.95)["minimum_symmetric_router_efficiency"]<.95
    assert .99<lookup(.902,2,.995)["minimum_symmetric_router_efficiency"]<1
    assert not lookup(.392,1,1.)["feasible_even_if_router_perfect"]
    assert lookup(.902,1,.95)["violates_trusted_witness_under_model"]
    assert not lookup(.902,2,.99)["violates_trusted_witness_under_model"]
    qnd=[qnd_prebasis(eta,n) for eta in (.902,.392) for n in (1,2)]
    assert all(row["trusted_witness_conditional_pass"] for row in qnd)
    assert math.isclose(qnd[-1]["source_attempts_per_accepted_herald"],1/.392**2)
    unc={n:[scenario(eta,n)["minimum_symmetric_router_efficiency"]
             for eta in (.898,.906)] for n in (1,2)}
    return {"status":"PASS_2026_MEASURED_MEMORY_REFERENCE_QUTRIT_WITNESS_STRESS",
      "cited_2026_measurements":[{
        "source":"Physical Review Letters accepted 30 September 2026: Efficient integrated quantum memory based on a waveguide cavity",
        "url":"https://journals.aps.org/prl/accepted/10.1103/28st-q915",
        "reported_storage_and_retrieval_percent":"90.2 +/- 0.4",
        "reported_conditional_fidelity_percent":"99.3 +/- 0.1 time-bin QUBITS",
        "scope":"single-photon-level weak coherent pulses, NOT two-qutrit entanglement or an event-ready 4-MUB POVM"},
        {"source":"Random access and high dimensional integrated quantum memory, 2026",
         "url":"https://link.springer.com/article/10.1186/s43074-026-00284-w",
         "reported_first_AFC_echo_average_storage_efficiency_percent":"39.2 +/- 0.2",
         "scope":"11-channel integrated RAQM; storage efficiency/echo measure not automatically same as the first PRL's complete storage/retrieval metric."}],
      "trusted_model":{"source_visibility":.75,"phase_sigma_rad":.15,
            "conditional_two_click_basis_match":q(),
            "detector_pair_efficiency":.81,"separable_null_with_calibration":.51,
            "default_path_efficiency":.95},
      "nominal_scenarios":rows,
      "PRL_efficiency_1sigma_router_threshold_range":{
         str(n):{"at_89p8pct":unc[n][0],"at_90p6pct":unc[n][1]} for n in (1,2)},
      "ideal_QND_prebasis_herald_scenarios":qnd,
      "information_theoretic_note":"E[log e_n]=n*D_Bernoulli(p||p0) for an oracle fixed-alternative likelihood-ratio e-process. log(100)/D is an information scale, NOT an anytime expected hitting-time theorem or guaranteed sample size.",
      "critical_caveat":"Weak-coherent-pulse QUBIT memory efficiency is not demonstrated qutrit retrieval efficiency, QND setting-independent herald, or full 4-MUB qutrit analyzer. The 39.2% result uses different protocol/efficiency definition."}
if __name__=="__main__":
    z=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(z["status"],scenario(.902,2,router=.995)["expected_log_evalue100_information_scale_herald_trials"])
