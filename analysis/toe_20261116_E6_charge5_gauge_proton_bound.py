"""Conditional p -> e+ pi0 constraint on the surviving E6 charge-five gauge boson.

Parallel E6 triplet-filter certificate gives:
charge+5 gauge block complex dimension 6,
m_X^2/(g_GUT^2 v_Y^2)=25 (reduced canonical convention),
nonzero normalized current projector coefficient -1/6
between Q†e^c and (u^c)†Q.

In a single-operator mass-eigenstate approximation:
C6 = kappa*g_GUT^2/M_X^2 = kappa/(25*v_Y^2),
where kappa=1/6 is the magnitude of THAT projector entry.
This is a necessary conditional bound if this term maps
without destructive interference to an effective p->e+pi0
decay amplitude and its low-energy coefficient is not
drastically modified. Actual rotations, thresholds and
operator normalization can alter it.

Gamma = mp/(32pi)*(1-mpi0²/mp²)² |W_pi*C6|².
Super-K limit p->e+pi0 >2.4e34 years at 90% CL.
"""
import math,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_E6_X_gauge_proton_pion_bound.json"
HBAR=6.582119569e-25
YEAR=365.25*24*3600
MP=.9382720813
MPI0=.1349768
EXPTAU=2.4e34
KAPPA=1/6
PHASE=MP/(32*math.pi)*(1-(MPI0/MP)**2)**2
def bound(W=.1,experimental_tau=EXPTAU):
    return math.sqrt(HBAR/(experimental_tau*YEAR*PHASE))/W
def model(vY,g=.7,W=.1,kappa=KAPPA,AR=1):
    if min(vY,g,W,kappa,AR)<=0:raise ValueError("positive inputs")
    mx=5*g*vY
    c6=AR*kappa*g*g/(mx*mx)
    gamma=PHASE*(c6*W)**2
    return {"VEV_Y_GeV":vY,"g_GUT":g,
       "gauge_boson_MX_GeV":mx,
       "current_projector_abs":kappa,"RG_factor":AR,
       "effective_C6_GeV_minus2":c6,
       "single_operator_partial_lifetime_years":HBAR/(YEAR*gamma),
       "passes_single_operator_bound":c6<=bound(W)}
def verify():
    b=bound()
    assert 9e-32<b<1.1e-31
    vmin=math.sqrt(KAPPA/(25*b))
    assert 2.5e14<vmin<2.7e14
    low=model(1e14)
    high=model(1e15)
    assert not low["passes_single_operator_bound"] and high["passes_single_operator_bound"]
    assert abs(model(2e14)["single_operator_partial_lifetime_years"]/model(1e14)["single_operator_partial_lifetime_years"]-16)<1e-12
    # g cancels exactly if X mass is 5*g*vY and kappa is fixed.
    assert abs(model(1e15,g=.4)["effective_C6_GeV_minus2"]/model(1e15,g=.8)["effective_C6_GeV_minus2"]-1)<1e-12
    return {"status":"PASS_E6_CHARGE5_GAUGE_D6_PROTON_EPI0_CONDITIONAL_BOUND",
       "experimental_limit_years":EXPTAU,
       "experimental_source":"Super-Kamiokande 2025 talk: p->e+pi0 >2.4e34 years at 90% CL with 450 kt yr https://www-sk.icrr.u-tokyo.ac.jp/~nakahata_s/kakenhi-kibanS/talk/Nakahata_SuperK_KMI2025_250305.pdf",
       "representative_Wpi_GeV2":.1,
       "single_operator_C6_max_GeV_minus2":b,
       "trace_metric_projector_kappa":KAPPA,
       "charge_five_gauge_boson_mass_formula":"M_X=5*g_GUT*v_Y, for canonical reduced adjoint trace metric, from parallel E6 triplet-filter gauge-current certificate",
       "coefficient_formula":"C6=AR*kappa/(25*v_Y²)",
       "VEV_Y_min_GeV_AR_1_W_0p1":vmin,
       "reference_low":low,"reference_high":high,
       "caution":"Exact current projector != physically normalized full decay amplitude. Need all gauge bosons, flavor rotations, chiral Fierz basis, matching factors, RG, wavefunction renormalization, interference, hadronic W0, and gauge-field normalization. Current bound is conditional, not a predicted proton lifetime.",
       "physics_key_point":"The Higgs-leg triplet polynomial only filters dimension-five holomorphic couplings, not this independent gauge-exchange dimension-six channel."}
if __name__=="__main__":
    x=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(x["status"],x["VEV_Y_min_GeV_AR_1_W_0p1"])
