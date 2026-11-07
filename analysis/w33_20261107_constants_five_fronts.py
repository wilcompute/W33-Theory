#!/usr/bin/env python3
"""Five constants fronts: reproducible falsifiers, not a TOE proof.

F1: One-loop on-shell QED running with frozen (not graph-derived) electron loop.
F2: One common qutrit Weyl-spurion flavor operator: an explicit falsifier.
F3: Scale/Maxwell-normalization identifiability obstruction.
F4: Full-tree candidate-lineage scanner (syntactic, not a proof classifier).
F5: Multiplicity-aware rational and uniform-null sensitivity tests.

All numerical constants and limits are recorded in the source. Stdlib only.
"""
from __future__ import annotations
import argparse
import cmath
import hashlib
import json
import math
import os
import re
from fractions import Fraction
from pathlib import Path

SCHEMA = "w33.constants.five_fronts.2026-11-07.v1"
ALPHA_CODATA22 = 137.035999177
ALPHA_SIGMA = 0.000000021
WEAK_MZ_REFERENCE = 0.23122
WEAK_SIGMA_REFERENCE = 0.00003
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", ".pytest_cache",
             "__pycache__", ".tox", "build", "dist"}
SUFFIXES = {".tex", ".py", ".md", ".html", ".json", ".lean", ".g", ".sage"}
TOKENS = {
    "alpha_inverse": r"137\.0|alpha.{0,25}(?:inv|inverse|\^|\-1)|fine.struct",
    "strong_coupling": r"alpha[_\\]?s|strong coupling|\\alpha_\{s\}",
    "weak_angle": r"sin.{0,13}theta.{0,13}w|weinberg|weak mixing",
    "cabibbo_ckm": r"cabibbo|V_us|V_\{us\}|ckm",
    "pmns": r"pmns|theta[_\\]?(?:12|13|23)|neutrino mixing",
    "mass_ratio": r"m_p/m_e|m_mu/m_e|koide|mass ratio",
    "cosmology": r"Omega[_\\]|Hubble|sigma_8|cosmological constant|n_s.*=",
    "dimensionful_scale": r"Planck constant|Newton constant|speed of light|m_Pl",
}

def simpson(fun, n=4096):
    """Deterministic composite Simpson integration on [0,1]."""
    assert n > 0 and n % 2 == 0
    h = 1.0 / n
    total = fun(0.0) + fun(1.0)
    for j in range(1, n):
        total += (4 if j % 2 else 2) * fun(j * h)
    return total * h / 3.0

def on_shell_electron_shift(q_over_me):
    """QED: 1/alpha(Q)-1/alpha(0), spacelike; m_e is external input."""
    assert q_over_me >= 0
    return -(2.0 / math.pi) * simpson(
        lambda z: z * (1 - z) *
        math.log1p(q_over_me * q_over_me * z * (1-z)))

def electromagnetic():
    variants = {
        "BT53_legacy_pdg2018_target": Fraction(137) + Fraction(1, 28) + Fraction(4, 14045),
        "paper_earlier": Fraction(137) + Fraction(880, 24445),
        "operator_resolvent": Fraction(137) + Fraction(40, 1111),
        "integer_skeleton": Fraction(137),
    }
    rows = []
    for name, value in variants.items():
        rows.append({"name": name, "fraction": str(value),
                     "inverse_alpha": float(value),
                     "residual_CODATA22_sigma": (float(value)-ALPHA_CODATA22)/ALPHA_SIGMA})
    qgrid = [0.0, 1.0, 10.0, 100.0]
    shifts = [on_shell_electron_shift(q) for q in qgrid]
    assert shifts[0] == 0.0 and all(shifts[i] > shifts[i+1] for i in range(3))
    # Both hypotheses run with the SAME independent electron-loop QED function:
    # their residuals remain a constant offset at every externally frozen Q.
    selected = float(variants["BT53_legacy_pdg2018_target"])
    offsets = [(selected+s)-(ALPHA_CODATA22+s) for s in shifts]
    assert max(abs(x-(selected-ALPHA_CODATA22)) for x in offsets) < 5e-14
    return {"status": "conditional_QED_not_W33_running", "reference": "CODATA 2022",
            "alpha_inverse_reference": ALPHA_CODATA22, "reference_sigma": ALPHA_SIGMA,
            "formulas": rows, "q_over_me_fixed_grid": qgrid,
            "electron_loop_inverse_alpha_shifts": shifts,
            "max_common_running_residual_error": max(abs(x-offsets[0]) for x in offsets),
            "conclusion": "No W33-specific running is derived. QED is assumed. "
                          "The formerly precise four-term candidate is 4.40 sigma away "
                          "from CODATA22 and cannot be rescued by changing Q without "
                          "changing the observable; no prospective alpha holdout exists."}

def matrix_product(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]
def dagger(a):
    return [[a[j][i].conjugate() for j in range(len(a))] for i in range(len(a[0]))]
def max_residual(a,b):
    return max(abs(a[i][j]-b[i][j]) for i in range(len(a)) for j in range(len(a[0])))
def diagonal(items):
    return [[complex(items[i] if i==j else 0) for j in range(len(items))]
            for i in range(len(items))]

def flavor():
    """One single qutrit-alignment generator for all species: exact model test.

    X is the F3 cyclic shift, X+X†=3P-I (complete-graph adjacency K3).
    U(t)=exp(it(X+X†))=e^(2it)P+e^(-it)(I-P).
    Each H_species = U_species D_species U_species† is a named Hermitian
    Yukawa-squared operator. D values are illustrative dimensionless inputs;
    they are NOT physical masses predicted from W33.
    """
    theta = Fraction(3,13)
    t = float(theta)
    a, b = cmath.exp(2j*t), cmath.exp(-1j*t)
    U = [[(a/3+b*(2/3)) if i==j else (a-b)/3
          for j in range(3)] for i in range(3)]
    I = diagonal([1,1,1])
    assert max_residual(matrix_product(U, dagger(U)), I) < 1e-14
    # All four Yukawa-squared matrices are explicitly constructed.
    # Quark up + charged lepton are diagonal; down and neutrino rotate by U.
    spectra = {"u": [1,3,9], "d": [2,4,8], "e": [1,4,16], "nu": [1,2,3]}
    H = {}
    for sector, values in spectra.items():
        diag = diagonal(values)
        H[sector] = (matrix_product(matrix_product(U,diag),dagger(U))
                     if sector in ("d","nu") else diag)
        assert max_residual(H[sector],dagger(H[sector])) < 1e-13
    # CKM = U_u† U_d = U; PMNS = U_e† U_nu = U.
    # Thus the same |U_01| forces the identical mixing amplitude.
    Vus = abs(U[0][1])
    pmns_solar = abs(U[0][1])**2/(1-abs(U[0][2])**2)
    exact_solar_from_cabibbo = Vus**2/(1-Vus**2)
    J = (U[0][0]*U[1][1]*U[0][1].conjugate()*U[1][0].conjugate()).imag
    assert abs(pmns_solar-exact_solar_from_cabibbo) < 1e-14
    assert abs(J) > 1e-5
    return {"status": "common_spurion_exact_falsifier", "theta": str(theta),
            "operator": "K=X+X_dagger=3P-I on F3; Hs=Us Ds Us_dagger",
            "diagonal_mass_squared_fixtures_not_predictions": spectra,
            "max_unitarity_error": max_residual(matrix_product(U,dagger(U)),I),
            "Vus_common_spurion": Vus, "sin2_theta12_PMNS_common_spurion": pmns_solar,
            "Jarlskog_nonzero": J,
            "identity": "sin2(theta12_PMNS)=abs(Vus)^2/(1-abs(Vus)^2)",
            "comparison": {"Vus_observed_approx": 0.225, "solar_sin2_observed_approx": 0.307},
            "conclusion": "A single identical up/down and e/nu alignment produces "
                          "CKM=PMNS and is contradicted by the measured solar angle. "
                          "Separate left rotations, symmetry-breaking or flavor "
                          "operators are required; their coefficients remain free."}

def scale():
    energy = [0.0,2.0,4.0]
    temp, time = 1/3, 0.73
    def norm_gibbs(e,T):
        weights=[math.exp(-x/T) for x in e]; z=sum(weights)
        return [w/z for w in weights]
    probs=norm_gibbs(energy,temp)
    phases=[cmath.exp(-1j*x*time) for x in energy]
    tests=[]
    for s in (0.1,0.5,1.0,3.0,10.0):
        scaled_probs=norm_gibbs([s*x for x in energy],s*temp)
        scaled_phases=[cmath.exp(-1j*(s*x)*(time/s)) for x in energy]
        tests.append({"scale":s,
                      "max_Gibbs_error":max(abs(x-y) for x,y in zip(probs,scaled_probs)),
                      "max_phase_error":max(abs(x-y) for x,y in zip(phases,scaled_phases))})
    assert max(row["max_Gibbs_error"] for row in tests)<1e-14
    assert max(row["max_phase_error"] for row in tests)<1e-14
    # Fixed combinatorial incidence is compatible with ANY g>0 in S=(1/4g²) F².
    # The following two different couplings leave q=3 incidence untouched.
    gauge_coefficients={str(g):1/(4*g*g) for g in (1.,2.)}
    return {"status":"exact_scale_and_gauge_normalization_nonidentifiability",
            "energy_spectrum_fixture":energy, "temperature":temp,"time":time,
            "rescalings":tests, "maxwell_F2_action_coefficients":gauge_coefficients,
            "conclusion":"Dimensionless W33 incidence fixes neither absolute H/t units "
                         "nor the continuous 1/(4g²) Maxwell action coefficient. "
                         "An independent normalized action, clock or external scale "
                         "is needed. Does not rule out additional dynamics breaking the symmetry."}

def multiplicity():
    """An explicit low-denominator rational competitor family, no stochastic claims."""
    weak_candidates=[]
    frontier=[]
    for cap in (20,100,500,1000):
        n=0; best=None
        for denom in range(2,cap+1):
            middle=round(WEAK_MZ_REFERENCE*denom)
            for num in sorted({middle-1,middle,middle+1}):
                if not 0<num<denom or math.gcd(num,denom)!=1:continue
                n+=1
                delta=abs(num/denom-WEAK_MZ_REFERENCE)
                if best is None or (delta,denom,num)<(best[0],best[2],best[1]):
                    best=(delta,num,denom)
        frontier.append({"max_denominator":cap,"tested_local_reduced_rationals":n,
                         "best_fraction":f"{best[1]}/{best[2]}",
                         "absolute_residual":best[0],
                         "sigma":best[0]/WEAK_SIGMA_REFERENCE})
    pred=Fraction(3,13)+Fraction(1,2200)
    # Exact family-wise probability under the SPECIFIED independent uniform
    # baseline. Does not assume physical formulas are independent or uniform.
    delta=abs(float(pred)-WEAK_MZ_REFERENCE)
    chance=min(1.0,2*delta) # interval width 1, interior target
    sensitivity=[{"assumed_independent_uniform_formulas":M,
                  "at_least_one_match_probability":-math.expm1(M*math.log1p(-chance))}
                 for M in (1,10,1000,1000000)]
    assert frontier[-1]["absolute_residual"]<delta
    return {"status":"retrospective_multiple_testing_falsifier",
            "reference_weak":WEAK_MZ_REFERENCE,"weak_sigma":WEAK_SIGMA_REFERENCE,
            "W33_formula":str(pred), "W33_absolute_residual":delta,
            "W33_sigma":delta/WEAK_SIGMA_REFERENCE,
            "bounded_rational_search":frontier,
            "independent_uniform_null_window":[0,1],
            "uniform_null_sensitivity":sensitivity,
            "interpretation":"Uniform independent formulas are a hypothetical sensitivity null, "
                             "not the physical distribution of correlated formula searches. "
                             "Retrospectively selected W33 formulas have no valid postselection p-value. "
                             "All candidates, aliases, scales and corrections must enter the frozen family."}

def provenance(root:Path,max_bytes=1_500_000,max_files=0):
    """File/line provenance across text in the checkout; false positives retained."""
    pat={key:re.compile(expr,re.I) for key,expr in TOKENS.items()}
    occurrences={key:[] for key in TOKENS}
    variants={key:{} for key in TOKENS}
    files_scanned=0; oversized=0; file_count=0
    for dirpath,dirs,files in os.walk(root):
        dirs[:]=sorted(d for d in dirs if d not in SKIP_DIRS)
        for name in sorted(files):
            path=Path(dirpath)/name
            if path.suffix.lower() not in SUFFIXES:continue
            file_count+=1
            if max_files and file_count>max_files:break
            try:
                if path.stat().st_size>max_bytes:oversized+=1;continue
                with path.open(encoding="utf-8",errors="replace") as handle:
                    files_scanned+=1
                    for lineno,line in enumerate(handle,1):
                        if len(line)>50000:continue
                        if not re.search(r"=|≈|\\approx|\\simeq",line):continue
                        if not re.search(r"\d",line):continue
                        names=[key for key,regex in pat.items() if regex.search(line)]
                        if not names:continue
                        rel=path.relative_to(root).as_posix()
                        # Syntactic key only. Different strings need not disagree.
                        norm=re.sub(r"\s+","",line).strip()[:280]
                        digest=hashlib.sha256(norm.encode()).hexdigest()[:16]
                        for key in names:
                            d=variants[key]
                            d[digest]=d.get(digest,0)+1
                            if len(occurrences[key])<12:
                                occurrences[key].append({"path":rel,"line":lineno,
                                                         "text":line.strip()[:220],
                                                         "variant_id":digest})
            except (OSError,UnicodeError):
                continue
        if max_files and file_count>max_files:break
    return {"status":"syntactic_scan_not_algebraic_equivalence",
            "files_scanned":files_scanned,"oversized_skipped":oversized,
            "text_file_entries_seen":file_count,"root":str(root),
            "max_file_bytes":max_bytes,"limited_max_files":max_files,
            "families":{key:{"distinct_line_shapes":len(variants[key]),
                              "total_matching_lines":sum(variants[key].values()),
                              "example_provenance":occurrences[key]}
                        for key in TOKENS},
            "notes":"Counts include archival statements, retractions, source-code examples "
                    "and false positives. A variant is a line signature, not a theorem "
                    "or distinct semantic expression. Verify each origin before promotion."}

def evaluate(root=None,scan=True,max_files=0):
    output={"schema":SCHEMA,
            "basis":{"q":3,"v":40,"k":12,"lambda":2,"mu":4},
            "EM":electromagnetic(),"flavor":flavor(),
            "scale":scale(),"multiple_testing":multiplicity(),
            "provenance":provenance(Path(root),max_files=max_files) if scan and root else
                         {"status":"not_run_requires_full_checkout"},
            "scope":"Reanalysis of existing source formulas and explicit new conditional "
                    "falsifiers. No new physical TOE constant, laboratory measurement "
                    "or prospective holdout has been established."}
    return output

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--root",default=".")
    ap.add_argument("--no-scan",action="store_true")
    ap.add_argument("--max-files",type=int,default=0)
    ap.add_argument("--output",default="data/w33_20261107_constants_five_fronts.json")
    args=ap.parse_args()
    out=evaluate(args.root,scan=not args.no_scan,max_files=args.max_files)
    target=Path(args.output);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":"PASS","output":str(target),
                      "EM_2022_sigma":out["EM"]["formulas"][0]["residual_CODATA22_sigma"],
                      "shared_flavor_solar":out["flavor"]["sin2_theta12_PMNS_common_spurion"],
                      "max_provenance_files":out["provenance"].get("files_scanned",0)},indent=2))
if __name__=="__main__":
    main()
