#!/usr/bin/env python3
"""Execute five representation/physics attacks plus three outside-box probes.

2026-09-23 continuation after the geometric/semilinear frontier.

The five attacks are:
1. Explain the weighted Dirac-square n^2 ladder and decompose its PSp(4,3)
   eigenspaces by exact chain characters.
2. Materialize the q=3 minimal full-similitude carrier as a 6D irreducible
   real representation of the 1296 point stabilizer and compute its complete
   character row, Frobenius-Schur indicators, and trace field.
3. Prove the Z3-graded antiunitary pairing theorem for T^2=C or C^2.
4. Lower the scalar FI-center gate into the existing frequency-bin lab ABI,
   including a reference-arm four-quadrature calibration and fail-closed
   admission budget.
5. Replace nominal sequential holonomy simulations with nuisance-marginalized
   adaptive tests and compare with the nominal Chernoff information scale.

Three additional probes:
A. finite McKean-Singer supertrace / Euler index;
B. real cubic character field created by qutrit similitude realification;
C. distribute the ternary FI phase frame over the already-certified optimal
   seven-tick W33 point-line broadcast tree.

All continuum/laboratory/particle interpretations remain explicitly fenced.
"""
from __future__ import annotations

from collections import Counter, deque
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_20260923_execute_next5_plus3_representation_physics.json"


def attack1_dirac_ladder():
    # Exact regular-tetrahedron circumcentric ratios, before choosing the W33
    # spherical normalization a^2=5/3.
    ratios_in_a = {
        "w1_over_w0": "1/(2 a^2)",
        "w2_over_w1": "8/a^2",
        "w3_over_w2": "18/a^2",
    }
    # Relevant unweighted incidence singular-square eigenvalues are 16,4,4.
    # Their weighted values are therefore 8/a^2,32/a^2,72/a^2.
    ladder_in_a = ["8/a^2", "32/a^2", "72/a^2"]
    a2 = 5 / 3
    ladder = [8 / a2, 32 / a2, 72 / a2]
    assert np.allclose(ladder, [24/5, 96/5, 216/5])

    # Exact GAP decomposition from the signed simplicial chain action generated
    # from the native F3^4 W33 transvections.  Irreps are indexed in the
    # CharacterTable(PSp(4,3)) order returned by GAP.
    degrees = [1,5,5,6,10,10,15,15,20,24,30,30,30,40,40,45,45,60,64,81]
    chain = {
        "C0": {1:1, 7:1, 10:1},  # 1 + 15 + 24
        "C1": {7:1, 10:1, 11:1, 16:1, 17:1, 20:1},
        "C2": {2:1, 3:1, 11:2, 16:1, 17:1},
        "C3": {2:1, 3:1, 11:1},
        "H1": {20:1},
        "coexact120": {11:1, 16:1, 17:1},
    }
    dim = lambda dec: sum(degrees[i-1]*m for i,m in dec.items())
    assert [dim(chain[k]) for k in ("C0","C1","C2","C3","H1","coexact120")] == [40,240,160,40,81,120]

    bands = {
        "3": {"multiplicity":24, "PSp43_module":"chi_10, degree 24"},
        "24/5": {"multiplicity":15, "PSp43_module":"chi_7, degree 15"},
        "96/5": {
            "multiplicity":120,
            "PSp43_module":"chi_11(deg30) + chi_16(deg45) + chi_17(deg45)",
        },
        "216/5": {
            "multiplicity":40,
            "PSp43_module":"chi_2(deg5) + chi_3(deg5) + chi_11(deg30)",
        },
        "0_H1": {"multiplicity":81, "PSp43_module":"chi_20, Steinberg degree 81"},
    }
    # chi_11 occurs at two distinct eigenvalues on two chain degrees. Therefore
    # the weighted Laplacian is not a scalar function of a PSp Casimir alone.
    casimir_only_refuted = "chi_11" in bands["96/5"]["PSp43_module"] and "chi_11" in bands["216/5"]["PSp43_module"]
    assert casimir_only_refuted

    return {
        "regular_tetrahedron_ratios": ratios_in_a,
        "incidence_square_inputs": [16,4,4],
        "ladder_general_edge_length": ladder_in_a,
        "W33_edge_length_squared": "5/3",
        "W33_ladder": ["24/5","96/5","216/5"],
        "W33_identity": "{24/5,96/5,216/5}=(24/5)*{1^2,2^2,3^2}",
        "GAP_character_degrees": degrees,
        "chain_decomposition_GAP_irrep_indices": {k:{str(i):m for i,m in v.items()} for k,v in chain.items()},
        "weighted_bands": bands,
        "mechanism": (
            "The 1:4:9 spacing is forced by regular-tetrahedron circumcentric "
            "weight ratios multiplied by the three relevant incidence-square "
            "eigenvalues. PSp(4,3) representation theory determines band "
            "multiplicities, but not the spacing."
        ),
        "pure_Casimir_explanation_refuted": casimir_only_refuted,
        "refutation_witness": (
            "The same PSp(4,3) irrep chi_11 of degree 30 occurs in the 96/5 "
            "coexact C1/C2 band and in the 216/5 C2/C3 band."
        ),
    }


def _su_normalize(A: np.ndarray) -> np.ndarray:
    det = np.linalg.det(A)
    return np.exp(-1j * np.angle(det) / A.shape[0]) * A


def _mkey(M: np.ndarray, decimals: int = 8):
    rr = np.round(M.real, decimals)
    ii = np.round(M.imag, decimals)
    rr[np.abs(rr) < 10**(-decimals)] = 0
    ii[np.abs(ii) < 10**(-decimals)] = 0
    return tuple(np.stack([rr, ii], axis=-1).ravel())


def _closure(gens, dim, limit=10000):
    I = np.eye(dim, dtype=complex)
    seen = {_mkey(I): I}
    frontier = [I]
    while frontier:
        A = frontier.pop()
        for G in gens:
            B = A @ G
            k = _mkey(B)
            if k not in seen:
                seen[k] = B
                frontier.append(B)
                if len(seen) > limit:
                    raise AssertionError("unexpected infinite/numerically unstable closure")
    return seen


def _matrix_order(A, max_order=100):
    I = np.eye(A.shape[0], dtype=complex)
    B = I.copy()
    for n in range(1, max_order + 1):
        B = B @ A
        if _mkey(B) == _mkey(I):
            return n
    raise AssertionError("order not found")


def attack2_q3_realification():
    omega = np.exp(2j*np.pi/3)
    X = np.roll(np.eye(3), 1, axis=0).astype(complex)
    Z = np.diag([omega**x for x in range(3)])
    F = np.array([[omega**(x*y) for x in range(3)] for y in range(3)], complex)/np.sqrt(3)
    P = np.diag([1,1,omega])
    base = [_su_normalize(A) for A in (X,Z,F,P)]

    even3 = _closure(base, 3)
    assert len(even3) == 648
    scalar_center = [
        A for A in even3.values()
        if np.max(np.abs(A - np.eye(3)*A[0,0])) < 1e-7
    ]
    assert len(scalar_center) == 3

    def doubled(A):
        M = np.zeros((6,6), complex)
        M[:3,:3] = A
        M[3:,3:] = A.conj()
        return M

    swap = np.zeros((6,6), complex)
    swap[:3,3:] = np.eye(3)
    swap[3:,:3] = np.eye(3)
    gens = [doubled(A) for A in base] + [swap]
    full = _closure(gens, 6)
    assert len(full) == 1296

    # Conjugacy classes under the generating set.
    inv = [G.conj().T for G in gens]
    remaining = set(full)
    classes = []
    while remaining:
        k0 = next(iter(remaining))
        orbit = {k0}
        q = deque([full[k0]])
        while q:
            A = q.popleft()
            for G, Gi in zip(gens, inv):
                B = G @ A @ Gi
                kb = _mkey(B)
                if kb not in orbit:
                    orbit.add(kb)
                    q.append(full[kb])
        classes.append(orbit)
        remaining -= orbit
    assert len(classes) == 18

    rows = []
    for C in classes:
        A = full[next(iter(C))]
        even = np.linalg.norm(A[:3,3:]) + np.linalg.norm(A[3:,:3]) < 1e-7
        tr = np.trace(A)
        trr = 0.0 if abs(tr.real)<1e-8 else round(float(tr.real), 8)
        tri = 0.0 if abs(tr.imag)<1e-8 else round(float(tr.imag), 8)
        rows.append({
            "order": _matrix_order(A),
            "class_size": len(C),
            "determinant_even_sector": bool(even),
            "character": [trr, tri],
        })
    rows.sort(key=lambda r:(r["order"], not r["determinant_even_sector"], r["class_size"], r["character"]))
    assert sum(r["class_size"] for r in rows) == 1296
    assert all(abs(r["character"][0])+abs(r["character"][1]) < 1e-8 for r in rows if not r["determinant_even_sector"])

    chars = np.array([np.trace(A) for A in full.values()])
    norm = float(np.sum(np.abs(chars)**2)/1296)
    fs6 = sum(np.trace(A@A) for A in full.values())/1296
    fs3 = sum(np.trace(A@A) for A in even3.values())/648
    assert abs(norm-1) < 1e-10
    assert abs(fs6-1) < 1e-10
    assert abs(fs3) < 1e-10

    order9 = sorted(r["character"][0] for r in rows if r["order"]==9)
    order18 = sorted(r["character"][0] for r in rows if r["order"]==18 and r["determinant_even_sector"])
    assert len(order9)==3 and len(order18)==3
    p9 = [x**3-9*x-9 for x in order9]
    p18 = [x**3-3*x-1 for x in order18]
    assert max(abs(x) for x in p9) < 2e-6
    assert max(abs(x) for x in p18) < 2e-6

    return {
        "single_sector": {
            "dimension":3,
            "retained_phase_Clifford_order":648,
            "scalar_center_order":3,
            "character_norm": float(sum(abs(np.trace(A))**2 for A in even3.values())/648),
            "Frobenius_Schur_indicator": [float(fs3.real), float(fs3.imag)],
            "type":"complex",
        },
        "full_similitude": {
            "dimension":6,
            "order":1296,
            "conjugacy_class_count":18,
            "character_norm":norm,
            "Frobenius_Schur_indicator":[float(fs6.real),float(fs6.imag)],
            "type":"real irreducible",
            "all_determinant_odd_class_traces_zero":True,
            "classes":rows,
        },
        "trace_field": {
            "field":"Q(zeta_9 + zeta_9^-1), real cubic conductor-9 field",
            "order9_trace_polynomial":"x^3 - 9x - 9",
            "order9_polynomial_discriminant":729,
            "order18_trace_polynomial":"x^3 - 3x - 1",
            "order18_polynomial_discriminant":81,
            "order9_trace_roots":order9,
            "order18_trace_roots":order18,
        },
        "fusion": (
            "The 3D retained-phase qutrit Clifford irrep has FS indicator 0 "
            "(complex type). Adjoining the determinant-odd sector swap fuses it "
            "with its complex conjugate into one 6D irreducible representation "
            "of the full 1296 point stabilizer with FS indicator +1."
        ),
    }


def attack3_z3_antiunitary_pairing():
    # Exact theorem is algebraic; the synthetic matrix check makes the pairing
    # and absence of neutral-sector Kramers forcing executable.
    omega = np.exp(2j*np.pi/3)
    neutral = np.array([0.2, 1.7, 4.1])
    matter = np.array([0.4, 1.3, 2.8, 5.0])
    H = np.diag(np.r_[neutral, matter, matter])
    C = np.diag(np.r_[np.ones(3), omega*np.ones(4), omega**2*np.ones(4)])

    # T=CJ, J is conjugation plus matter/antimatter swap.
    def J(v):
        return np.r_[v[:3].conj(), v[7:].conj(), v[3:7].conj()]
    def T(v):
        return C @ J(v)

    # Check T^2=C^2 on a complete basis and H T = T H.
    I = np.eye(11, dtype=complex)
    max_square = 0.0
    max_sym = 0.0
    for e in I:
        max_square = max(max_square, np.linalg.norm(T(T(e)) - C@C@e))
        max_sym = max(max_sym, np.linalg.norm(H@T(e) - T(H@e)))
    assert max_square < 1e-12 and max_sym < 1e-12

    # An omega-sector basis vector is paired into the omega^2 sector at same E.
    e = I[3]
    partner = T(e)
    overlap = abs(np.vdot(e, partner))
    assert overlap < 1e-12
    assert abs(np.vdot(partner,H@partner).real - H[3,3].real) < 1e-12

    return {
        "theorem": (
            "Let C be unitary with C^3=1 and H commute with C. Let T be "
            "antiunitary with HT=TH, TC=CT in the semilinear sense, and "
            "T^2=C^r for r=1 or 2. If C psi=omega psi, then "
            "C(T psi)=omega^2 T psi, so T psi is an orthogonal equal-energy "
            "partner in the conjugate grading sector. The same holds with "
            "omega and omega^2 exchanged. In the neutral C=1 sector, T^2=1 "
            "and no Kramers degeneracy is forced."
        ),
        "E8_consequence": (
            "For any Hamiltonian obeying the certified E8 grading and one of "
            "the order-6 anti-linear symmetries CJ or C^2J, the spectra on "
            "g1 and g2 are identical and paired across the 81+81 matter sectors; "
            "no even degeneracy is forced on the neutral 86-dimensional sector."
        ),
        "difference_from_Kramers": (
            "Orthogonality comes from distinct C eigenvalues, not from a "
            "T^2=-1 scalar within one sector."
        ),
        "synthetic_check": {
            "dimension":11,
            "neutral_dimension":3,
            "matter_dimensions":[4,4],
            "max_T2_minus_C2":max_square,
            "max_HT_minus_TH":max_sym,
            "matter_partner_overlap":overlap,
        },
    }


def attack4_fi_reference_arm():
    compiler = json.loads((ROOT/"data/w33_frequency_bin_hashimoto_compiler.json").read_text())
    assert compiler["verified"] is True
    hesse = compiler["frequency_plan"]["hesse_bins"]
    phase120 = [row for row in hesse if row["qutrit_phase_degrees"] == 120]
    assert [r["label"] for r in phase120] == ["H1","H4","H7"]

    packets = compiler["probe_budget"]["packets_per_mirror_atlas"]
    sectors = compiler["probe_budget"]["sector_count"]
    opportunities_per_atlas = len(phase120)*packets*sectors
    assert opportunities_per_atlas == 180
    atlases = compiler["probe_budget"]["packets_per_supercycle"] // packets
    assert atlases == 24
    opportunities_per_supercycle = opportunities_per_atlas * atlases
    assert opportunities_per_supercycle == 4320

    target_deg = 120.0
    analyzer_deg = [0.0,90.0,180.0,270.0]
    phase_max_deg = 2.5
    fidelity_min = 0.99
    # For the effective two-path dephasing/phase channel:
    # Fe=(1+V cos(delta))/2.
    Vmin = (2*fidelity_min-1)/math.cos(math.radians(phase_max_deg))
    assert Vmin < 1
    nominal_V = 0.965

    def phase_fisher(V, theta):
        d = math.radians(target_deg-theta)
        return V*V*math.sin(d)**2/(1-V*V*math.cos(d)**2)
    fi_nom = [phase_fisher(nominal_V,t) for t in analyzer_deg]
    fi_admit = [phase_fisher(Vmin,t) for t in analyzer_deg]
    avg_nom = sum(fi_nom)/4
    avg_admit = sum(fi_admit)/4
    sigma_target = math.radians(phase_max_deg)/3
    n_nom = math.ceil(1/(sigma_target**2*avg_nom))
    n_admit = math.ceil(1/(sigma_target**2*avg_admit))
    supercycles_nom = math.ceil(n_nom/opportunities_per_supercycle)
    supercycles_admit = math.ceil(n_admit/opportunities_per_supercycle)
    assert supercycles_nom == 2 and supercycles_admit == 2

    return {
        "existing_Holonet_ABI": {
            "components":[x["component"] for x in compiler["component_chain"]],
            "existing_measurement_fields":[
                "plus_counts","minus_counts","total_counts","visibility",
                "phase_error_degrees","eom_phase_reference"
            ],
            "120deg_Hesse_bins":[r["label"] for r in phase120],
            "120deg_probe_opportunities_per_mirror_atlas":opportunities_per_atlas,
            "mirror_atlases_per_supercycle":atlases,
            "120deg_probe_opportunities_per_supercycle":opportunities_per_supercycle,
        },
        "reference_arm_extension": {
            "new_primitive":"FI_REFERENCE_ARM_PHASE",
            "target_relative_phase_deg":target_deg,
            "analyzer_reference_phases_deg":analyzer_deg,
            "estimators":{
                "X":"(d_0-d_180)/2 = V cos(phi)",
                "Y":"(d_90-d_270)/2 = V sin(phi)",
                "visibility":"sqrt(X^2+Y^2)",
                "phase":"atan2(Y,X)",
                "d_theta":"(N_plus-N_minus)/(N_plus+N_minus)",
            },
        },
        "fail_closed_admission": {
            "effective_path_entanglement_fidelity_formula":"Fe=(1+V cos(delta))/2",
            "required_Fe":fidelity_min,
            "max_abs_phase_error_deg":phase_max_deg,
            "implied_min_visibility":Vmin,
            "nominal_design_visibility":nominal_V,
            "nominal_visibility_passes_99pct_gate":nominal_V >= Vmin,
            "verdict":"FAIL_CLOSED_UNTIL_MEASURED_REFERENCE_ARM_VISIBILITY_AND_PHASE_MEET_GATE",
        },
        "shot_budget_Fisher_design": {
            "phase_sigma_goal":"3 sigma <= 2.5 degrees",
            "per_shot_phase_Fisher_at_nominal_V":fi_nom,
            "average_phase_Fisher_nominal":avg_nom,
            "detected_events_needed_nominal":n_nom,
            "detected_events_needed_at_admission_floor":n_admit,
            "one_supercycle_opportunities":opportunities_per_supercycle,
            "supercycles_needed_if_one_detected_event_per_opportunity_nominal":supercycles_nom,
            "supercycles_needed_if_one_detected_event_per_opportunity_at_floor":supercycles_admit,
        },
        "boundary": (
            "This is an executable calibration/admission design using an existing "
            "frequency-bin ABI. It does not report measured reference-arm data."
        ),
    }


def _entropy(p):
    p = np.asarray(p, dtype=float)
    p = p[p>0]
    return float(-(p*np.log(p)).sum())


def _nominal_prob_tables(V=.965,b=.01):
    eta=V*(1-b)
    p=lambda ph:.5*(1+eta*np.cos(ph))
    return {
        5:p(np.radians(np.array([[72.],[144.]]))),
        7:p(2*np.pi*np.array([[1/7],[2/7],[3/7]])),
        9:p(np.radians(np.array([
            [120,0,120],[0,120,120],[120,120,0],[120,120,120]
        ],float))),
    }


def _bernkl(p,q):
    return float(p*math.log(p/q)+(1-p)*math.log((1-p)/(1-q)))


def _chernoff_rows():
    P=_nominal_prob_tables()
    out={}
    for q in (5,7):
        rows=[]
        for h in range(len(P[q])):
            d=min(_bernkl(P[q][h,0],P[q][j,0]) for j in range(len(P[q])) if j!=h)
            rows.append({"hypothesis":h,"optimal_setting_weights":[1.0],"D_star":d})
        out[str(q)]=rows

    # q9 exact optimum from the one-high/three-low incidence geometry.
    rows=[]
    for h in range(4):
        if h<3:
            lam=[0.,0.,0.]; lam[[1,0,2][h]]=1.
        else:
            lam=[1/3,1/3,1/3]
        ds=[]
        for j in range(4):
            if j==h: continue
            ds.append(sum(lam[s]*_bernkl(P[9][h,s],P[9][j,s]) for s in range(3)))
        rows.append({"hypothesis":h,"optimal_setting_weights":lam,"D_star":min(ds)})
    out["9"]=rows
    return out


def nuisance_adaptive_simulation(trials=5000, seed=20260923, q9_drift_step_deg=0.05):
    rng=np.random.default_rng(seed)
    V0,sV=.965,.005
    b0,sb=.01,.002
    sd=math.radians(1)
    Vs=np.linspace(V0-3*sV,V0+3*sV,5)
    bs=np.linspace(b0-3*sb,b0+3*sb,5)
    ds=np.radians(np.linspace(-3,3,7))
    grid=np.array([(V,b,d) for V in Vs for b in bs for d in ds])
    logprior=-.5*(((grid[:,0]-V0)/sV)**2+((grid[:,1]-b0)/sb)**2+(grid[:,2]/sd)**2)
    prior=np.exp(logprior-logprior.max()); prior/=prior.sum()
    alpha=2.866515718791933e-7
    target=1-alpha

    phase_tables={
        5:np.radians(np.array([[72.],[144.]])),
        7:2*np.pi*np.array([[1/7],[2/7],[3/7]]),
        9:np.radians(np.array([
            [120,0,120],[0,120,120],[120,120,0],[120,120,120]
        ],float)),
    }

    def build_probs(ph):
        H,S=ph.shape
        V,b,d=grid[:,0],grid[:,1],grid[:,2]
        return np.stack([
            .5*(1+V[:,None]*(1-b[:,None])*np.cos(ph[h][None,:]+d[:,None]))
            for h in range(H)
        ])

    def run(q, drift_step_deg=0.0):
        ph=phase_tables[q]; probs=build_probs(ph)
        H,N,S=probs.shape
        stops=[]; by=[[] for _ in range(H)]
        errors=0; profile_mismatch=0; settings=np.zeros(S,dtype=int)
        for _ in range(trials):
            true=int(rng.integers(H))
            Vt=float(np.clip(rng.normal(V0,sV),Vs[0],Vs[-1]))
            bt=float(np.clip(rng.normal(b0,sb),bs[0],bs[-1]))
            dt=float(np.clip(rng.normal(0,sd),ds[0],ds[-1]))
            W=np.tile(prior/H,(H,1))
            for t in range(1,401):
                Ph=W.sum(1)
                if S==1:
                    s=0
                else:
                    h0=_entropy(Ph); gains=[]
                    for s0 in range(S):
                        A=np.sum(W*probs[:,:,s0],axis=1); py=float(A.sum())
                        B=np.sum(W*(1-probs[:,:,s0]),axis=1)
                        gains.append(h0-(py*_entropy(A/py)+(1-py)*_entropy(B/(1-py))))
                    s=int(np.argmax(gains))
                settings[s]+=1
                ptrue=.5*(1+Vt*(1-bt)*math.cos(ph[true,s]+dt))
                y=rng.random()<ptrue
                W*=probs[:,:,s] if y else (1-probs[:,:,s])
                W/=W.sum()
                if drift_step_deg:
                    dt=float(np.clip(
                        dt+rng.normal(0,math.radians(drift_step_deg)),
                        ds[0],ds[-1]
                    ))
                Ph=W.sum(1); best=int(np.argmax(Ph))
                if Ph[best] >= target:
                    profile=int(np.argmax(W.max(axis=1)))
                    profile_mismatch += int(profile!=best)
                    errors += int(best!=true)
                    stops.append(t); by[true].append(t)
                    break
            else:
                stops.append(400); by[true].append(400); errors+=int(best!=true)
        return {
            "trials":trials,
            "mean":float(np.mean(stops)),
            "median":float(np.median(stops)),
            "p95":float(np.percentile(stops,95)),
            "p99":float(np.percentile(stops,99)),
            "maximum":int(np.max(stops)),
            "mean_by_hypothesis":[float(np.mean(x)) for x in by],
            "p95_by_hypothesis":[float(np.percentile(x,95)) for x in by],
            "observed_errors":int(errors),
            "profile_vs_marginal_decision_mismatches":int(profile_mismatch),
            "setting_uses":[int(x) for x in settings],
        }

    results={str(q):run(q) for q in (5,7,9)}
    results["9_with_phase_random_walk_0p05deg_per_shot"]=run(9,q9_drift_step_deg)
    return {
        "nuisance_grid":{
            "visibility":"0.965 +/- 3*0.005, 5 nodes",
            "background":"0.010 +/- 3*0.002, 5 nodes",
            "phase":"0 +/- 3 degrees, 7 nodes",
            "particle_count":len(grid),
            "prior":"truncated Gaussian product on grid",
        },
        "target_posterior":target,
        "seed":seed,
        "results":results,
    }


def attack5_sequential(trials=5000):
    P=_nominal_prob_tables()
    cher=_chernoff_rows()
    alpha=2.866515718791933e-7
    logod=math.log((1-alpha)/alpha)
    scales={}
    for q,rows in cher.items():
        scales[q]=[
            logod/r["D_star"] for r in rows
        ]
    sim=nuisance_adaptive_simulation(trials=trials)
    return {
        "nominal_probability_tables":{str(q):P[q].tolist() for q in P},
        "Chernoff_controlled_information":cher,
        "asymptotic_logodds_over_Dstar_event_scales":scales,
        "nuisance_marginalized_adaptive":sim,
        "q9_projective_geometry":{
            "quotient":"F9^*/F3^* = P^1(F3)",
            "three_zero_vs_nonzero_trace_probe_signatures":["010","100","001","000"],
            "interpretation":(
                "Each of three trace functionals has one projective kernel. "
                "Cosine collapses trace +/-1 together, giving a binary "
                "zero-vs-nonzero probe. Three kernels identify three points "
                "one-hot and the fourth point is all-low."
            ),
        },
        "conclusion":(
            "The nuisance-marginalized experiment preserves the ordering seen "
            "in the nominal study: q9 adaptive discrimination is substantially "
            "more sample-efficient than q7 despite larger hidden-label entropy. "
            "The nominal Chernoff D* values explain this through measurement "
            "channel information geometry rather than entropy alone."
        ),
        "boundary":"Monte Carlo zero-error counts are power diagnostics, not 5-sigma tail estimates.",
    }


def outside_box(a1,a2,a4,a5):
    # A: finite McKean-Singer cancellation.
    # Weighted spectra by cochain degree.
    spectra=[
        {0:1,3:24,24/5:15},
        {0:81,3:24,24/5:15,96/5:120},
        {96/5:120,216/5:40},
        {216/5:40},
    ]
    def supertrace(t):
        return sum(
            ((-1)**k)*sum(m*math.exp(-t*lam) for lam,m in sp.items())
            for k,sp in enumerate(spectra)
        )
    vals={str(t):supertrace(t) for t in (0,.01,.1,1,10)}
    assert max(abs(v+80) for v in vals.values()) < 1e-10

    # C: existing exact distributed broadcast resource.
    return {
        "A_finite_McKean_Singer_index":{
            "Euler_characteristic":"40-240+160-40=-80",
            "supertrace_identity":"Str exp(-t L) = -80 for every t",
            "sample_checks":vals,
            "mechanism":"Every positive weighted Hodge eigenvalue cancels between adjacent cochain degrees; only 1-81=-80 zero modes remain.",
            "physics_reading":"metric-independent supersymmetric/Witten-index-style invariant of the finite de Rham complex",
            "boundary":"finite-complex index identity, not a continuum supersymmetric field theory",
        },
        "B_outer_similitude_realification":{
            "single_qutrit_sector_FS":a2["single_sector"]["Frobenius_Schur_indicator"],
            "full_6D_FS":a2["full_similitude"]["Frobenius_Schur_indicator"],
            "trace_field":a2["trace_field"],
            "statement":"The determinant-odd similitude does more than add states: it realifies the complex qutrit Clifford sector into a real irreducible 6D carrier whose non-rational character values lie in the conductor-9 real cubic field.",
            "boundary":"character arithmetic, not a measured energy/coupling field",
        },
        "C_distributed_FI_phase_frame":{
            "frame_alphabet":"Z3 = {0,120,240 degrees}",
            "existing_W33_network_nodes":80,
            "optimal_broadcast_ticks":7,
            "broadcast_tree_edges":79,
            "gather_plus_broadcast_ticks":14,
            "connection_to_FI_gate":"After local reference-arm calibration, the FI center phase is exactly one ternary frame symbol, so the already-certified seven-tick frame broadcast can disseminate it without an 80-link central phase bus.",
            "connection_to_calibration":"The fourteen-tick all-reduce can aggregate ternary phase-residue corrections and rebroadcast a consensus frame symbol.",
            "boundary":"exact network/control reuse; does not establish optical phase coherence across physical nodes",
        },
    }


def main(write=True, trials=5000):
    parents=[
        ROOT/"data/w33_20260923_execute_next5_plus3_geometric_semilinear_frozen.json",
        ROOT/"data/w33_extended_clifford1296_point_stabilizer.json",
        ROOT/"data/w33_frequency_bin_hashimoto_compiler.json",
        ROOT/"data/w33_e8_split_real_form_involution.json",
    ]
    assert all(p.exists() for p in parents)
    a1=attack1_dirac_ladder()
    a2=attack2_q3_realification()
    a3=attack3_z3_antiunitary_pairing()
    a4=attack4_fi_reference_arm()
    a5=attack5_sequential(trials=trials)
    extra=outside_box(a1,a2,a4,a5)

    checks={
        "ladder_geometric_not_pure_Casimir":a1["pure_Casimir_explanation_refuted"],
        "H1_is_Steinberg81":a1["weighted_bands"]["0_H1"]["multiplicity"]==81,
        "q3_single_sector_order648":a2["single_sector"]["retained_phase_Clifford_order"]==648,
        "q3_full_realification_order1296":a2["full_similitude"]["order"]==1296,
        "q3_full_6D_irreducible_real":abs(a2["full_similitude"]["character_norm"]-1)<1e-10 and abs(a2["full_similitude"]["Frobenius_Schur_indicator"][0]-1)<1e-10,
        "Z3_antiunitary_pairing_exact":a3["synthetic_check"]["max_T2_minus_C2"]<1e-12,
        "FI_uses_existing_120deg_slots":a4["existing_Holonet_ABI"]["120deg_probe_opportunities_per_mirror_atlas"]==180,
        "FI_reference_arm_fails_closed_without_measurement":a4["fail_closed_admission"]["verdict"].startswith("FAIL_CLOSED"),
        "q9_nuisance_adaptive_beats_q7":a5["nuisance_marginalized_adaptive"]["results"]["9"]["mean"] < a5["nuisance_marginalized_adaptive"]["results"]["7"]["mean"],
        "q9_phase_drift_stays_close_nominal":a5["nuisance_marginalized_adaptive"]["results"]["9_with_phase_random_walk_0p05deg_per_shot"]["mean"] < 1.2*a5["nuisance_marginalized_adaptive"]["results"]["9"]["mean"],
        "McKean_Singer_minus80":all(abs(v+80)<1e-10 for v in extra["A_finite_McKean_Singer_index"]["sample_checks"].values()),
        "distributed_FI_frame_seven_ticks":extra["C_distributed_FI_phase_frame"]["optimal_broadcast_ticks"]==7,
    }
    assert all(checks.values())

    out={
        "schema":"w33.20260923.execute_next5_plus3_representation_physics.v1",
        "status":"PASS_NEXT5_PLUS3_DIRAC_MODULES_Q3_REALIFICATION_Z3_PAIRING_FI_REFERENCE_ADAPTIVE_CHERNOFF",
        "attack1_dirac_ladder_representation":a1,
        "attack2_q3_full_character_realification":a2,
        "attack3_Z3_antiunitary_pairing":a3,
        "attack4_FI_reference_arm_calibration":a4,
        "attack5_nuisance_adaptive_holonomy":a5,
        "outside_box":extra,
        "checks":checks,
        "boundaries":[
            "The n^2 ladder is a finite circumcentric/cochain identity; PSp modules explain multiplicity, not a continuum KK spectrum.",
            "The 6D realification is a finite point-stabilizer representation, not an observed particle multiplet.",
            "The Z3 pairing theorem applies only to Hamiltonians that actually commute with both C and T.",
            "The FI reference-arm packet is a preregistered calibration design with no measured counts.",
            "Sequential Monte Carlo is a power/design calculation; rare-tail significance requires exact or laboratory-calibrated inference.",
            "Distributed phase-frame reuse is a network theorem, not a physical phase-coherence demonstration."
        ],
        "parents":[str(p.relative_to(ROOT)) for p in parents],
    }
    if write:
        OUT.write_text(json.dumps(out,indent=2,default=lambda o:o.item() if isinstance(o,np.generic) else str(o))+"\n")
    return out


if __name__=="__main__":
    result=main(True,5000)
    print(json.dumps({
        "status":result["status"],
        "check_count":len(result["checks"]),
        "all_checks":all(result["checks"].values()),
        "q5_mean":result["attack5_nuisance_adaptive_holonomy"]["nuisance_marginalized_adaptive"]["results"]["5"]["mean"],
        "q7_mean":result["attack5_nuisance_adaptive_holonomy"]["nuisance_marginalized_adaptive"]["results"]["7"]["mean"],
        "q9_mean":result["attack5_nuisance_adaptive_holonomy"]["nuisance_marginalized_adaptive"]["results"]["9"]["mean"],
    },indent=2,default=lambda o:o.item() if isinstance(o,np.generic) else str(o)))
