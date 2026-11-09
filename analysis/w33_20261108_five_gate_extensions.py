#!/usr/bin/env python3
"""Five physics-gate extensions plus an H27/Maxwell cross-gate test.

Exact rank/determinant claims are separated from synthetic optical controls
and from source-certificate-only cosmology reanalysis. No TOE claim.
"""
from __future__ import annotations
import argparse
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy.linalg import eigh, null_space

ROOT = Path(__file__).resolve().parents[1]

def load_native_maxwell(root=ROOT):
    sys.path.insert(0, str(root / "analysis"))
    import w33_20261108_s4_harmonic_qdual as s
    edges, faces, edge_index, b1, b2 = s.complex27()
    return np.asarray(b1, float), np.asarray(b2, float)

def gauge_weight_and_rank_budget(root=ROOT):
    b1, b2 = load_native_maxwell(root)
    assert b1.shape == (27, 108) and b2.shape == (108, 36)
    assert np.array_equal(b1 @ b2, np.zeros((27, 36)))
    assert np.allclose(b2.T @ b2, 3 * np.eye(36))
    harmonic = null_space(np.vstack((b1, b2.T)))
    assert harmonic.shape == (108, 46)
    weights = np.linspace(0.5, 1.5, 36)
    magnetic = (b2 * weights[None, :]) @ b2.T
    eigen = np.linalg.eigvalsh(magnetic)
    assert np.sum(eigen > 1e-8) == 36
    assert np.allclose(np.sort(eigen[-36:]), 3 * weights, atol=2e-12)
    assert np.max(np.abs(magnetic @ harmonic)) < 1e-10
    # This 4-column lift is an illustrative, gauge-invariant map, NOT an
    # established identification of H27's native 4-dimensional representation.
    r = harmonic[:, :4]
    extended = magnetic + 0.5 * (r @ r.T)
    eigen_extended = np.linalg.eigvalsh(extended)
    assert np.sum(eigen_extended > 1e-8) == 40
    assert np.sum(np.abs(eigen_extended) < 1e-8) == 68
    assert np.max(np.abs(extended @ b1.T)) < 1e-10
    return dict(native_complex=[27, 108, 36], gauge_gradients=26,
                harmonic_zero_modes_before=46, positive_face_weights_36=True,
                coexact_eigenvalue_formula="lambda_i=3*w_i, i=1..36",
                weighted_magnetic_rank=36, harmonic_modes_after_arbitrary_face_weight=46,
                conditional_H27_rank_cap=4, illustrative_lift_rank=40,
                harmonic_zero_modes_after_rank4_lift=42,
                warning="The native 4D H27 holonomy carrier has NOT been shown to embed into the 46D Maxwell harmonic sector; the 42 bound applies only if the added gauge-invariant stiffness has rank <=4.")

def time_dependent_null_locality_budget():
    # Given the earlier strict-null translation-invariant, SL2-covariant
    # amplitude bound 2/q^2, Duhamel handles arbitrary time-dependent E(t).
    vals = {}
    for q in (3, 5, 7, 11, 13):
        target = q ** (-1.5)
        baseline = 2 / (q * q)
        deficit = max(0.0, target - baseline)
        vals[str(q)] = dict(target_flat_amplitude=target,
                            baseline_upper_bound=baseline,
                            necessary_integrated_operator_norm=deficit)
    assert vals["3"]["necessary_integrated_operator_norm"] == 0
    assert all(vals[str(q)]["necessary_integrated_operator_norm"] > 0 for q in (5,7,11,13))
    return dict(statement="For H(t)=H0+E(t), integral_0^T ||E(t)||op dt >= q^(-3/2)-2/q^2 is necessary for a uniform amplitude on a previously bound output (q>=5).",
                derivation="Duhamel: ||U(T)-U0(T)||op <= integral ||E(t)||op dt, also valid when [E(t),H0] != 0.",
                q_values=vals, limitations="Only relative to the prior, explicitly symmetric H0 family and its 2/q^2 bound; not a no-go for general strictly local Hamiltonians.")

def native_e6_determinant(root=ROOT):
    sys.path.insert(0, str(root / "analysis"))
    import w33_pass11261_g26_cartan_coordinate_map as p
    source = p._load(root / "analysis/w33_pass11218_e8_cubic_cartan_kernel.py", "gate_ext_cubic")
    records = source.load_parent().build_records()
    assert len(records) == 1620
    rng = np.random.default_rng(14062026)
    phi = rng.normal(size=81) + 1j * rng.normal(size=81)
    m = np.zeros((81, 81), dtype=complex)
    for u, x, o, c in records:
        m[o, x] += c * phi[u]
    assert np.linalg.norm(m + m.T) < 1e-9
    assert np.linalg.matrix_rank(m, tol=1e-8) == 78
    ucols = []
    for _ in range(3):
        z = rng.normal(size=81) + 1j * rng.normal(size=81)
        z /= np.linalg.norm(z)
        ucols.append(z.conj())
    u = np.stack(ucols, axis=1)
    augmented = np.block([[m, u], [-u.T, np.zeros((3,3), complex)]])
    assert np.max(np.abs(augmented + augmented.T)) < 1e-9
    aug_sign, aug_log = np.linalg.slogdet(augmented)
    cases = []
    for ts in ((0.4,0.4,0.4), (0.3,0.9,0.2), (2.0,0.7,0.9), (0.8,1.2,0.45)):
        mass = m + (u * np.asarray(ts)[None,:]) @ u.T
        sign, logabs = np.linalg.slogdet(mass)
        logcorr = logabs - sum(math.log(t) for t in ts)
        signerr = abs(sign / aug_sign - 1)
        assert abs(logcorr-aug_log) < 1e-6, (ts, logcorr, aug_log)
        assert signerr < 1e-6, (ts, signerr)
        cases.append(dict(positive_coefficients=list(ts),
                          determinant_phase_radians=float(np.angle(sign)),
                          log_coefficient_magnitude=float(logcorr),
                          identity_log_error=float(abs(logcorr-aug_log)),
                          identity_phase_complex_error=float(signerr)))
    phase = float(np.angle(aug_sign))
    assert abs(phase) > 0.01
    return dict(native_alternating_rank=78, spurion_directions=3, completed_rank=81,
                determinant_identity="det(M+U diag(t1,t2,t3) U^T) = t1*t2*t3*det([[M,U],[-U^T,0]]) for rank(M)=n-3",
                augmented_skew_dimension=84, augmented_determinant_is_pfaffian_square=True,
                native_coefficient_phase_radians=phase, positive_vev_magnitudes_do_not_change_phase=True,
                checks=cases,
                physical_limit="This 81-state determinant is NOT theta_bar or an SM mass determinant. This algebra does not provide a vacuum, anomalies, CKM/PMNS, or loop-level CP protection; phases of U could change it.")

def correlated_photonic_noise():
    n, sigma, samples = 27, 0.30, 15000
    rng = np.random.default_rng(202611081)
    result = {}
    for rho in (0.0,0.5,0.9,1.0):
        common = rng.normal(size=(samples,1)) * sigma * math.sqrt(rho)
        independent = rng.normal(size=(samples,n)) * sigma * math.sqrt(1-rho)
        phase = common + independent
        fidelity = np.abs(np.mean(np.exp(1j*phase), axis=1))**2
        actual = float(np.mean(fidelity))
        analytic = float(1/n + (n-1)/n * math.exp(-sigma**2*(1-rho)))
        assert abs(actual-analytic) < 0.002
        result[str(rho)] = dict(analytic_conditional_fidelity=analytic,
                                simulated_conditional_fidelity=actual,
                                equal_rail_survival_eta07_unconditional_success_weighted_fidelity=0.7*analytic)
    assert abs(result["1.0"]["simulated_conditional_fidelity"]-1) < 1e-12
    return dict(synthetic=True, modes=n, sigma_radians=sigma,
                samples=samples, correlated_phase_results=result,
                general_formula="E[F] = N^-2 sum_ij exp(-(Cii+Cjj-2Cij)/2), Gaussian rail-phase covariance C",
                equicorrelated_formula="E[F] = 1/N + (1-1/N)*exp(-sigma^2*(1-rho))",
                scope="Common phase is gauge-invisible in this idealized interference fidelity. Uniform loss is an erasure/success penalty, not an improvement in physical success. No physical photon experiment.")

def cosmology_nonadditivity(root=ROOT):
    j = json.loads((root / "data/w33_20261108_S8_hybrid_shapley_audit.json").read_text(encoding="utf-8"))
    surveys = {}
    for key in ("des", "kids"):
        parts = j["surveys"][key]
        out = {}
        for name in ("all","low","high","mixed"):
            x = parts[name]
            f = x["chi2_fading_F"]; c = x["chi2_CPL_C"]
            p = x["chi2_hybrid_CPL_power_fading_geometry"]
            g = x["chi2_hybrid_fading_power_CPL_geometry"]
            delta = c-f
            interaction = c-p-g+f
            shap_power = ((p-f)+(c-g))/2
            shap_geo = ((g-f)+(c-p))/2
            assert abs(delta-x["CPL_minus_fading_total"]) < 1e-9
            assert abs(interaction-x["nonadditive_interaction"]) < 1e-9
            assert abs(shap_power-x["order_independent_shapley_power"]) < 1e-9
            assert abs(shap_geo-x["order_independent_shapley_geometry"]) < 1e-9
            assert abs((shap_power+shap_geo)-delta) < 1e-9
            out[name] = dict(delta_chi2_CPL_minus_fading=delta,
                             shapley_power=shap_power,shapley_geometry=shap_geo,
                             nonadditive_interaction=interaction)
        blocks_sum = sum(out[v]["delta_chi2_CPL_minus_fading"] for v in ("low","high","mixed"))
        out["all"]["naively_summed_block_delta"]=blocks_sum
        out["all"]["nonadditive_subblock_difference"]=out["all"]["delta_chi2_CPL_minus_fading"] - blocks_sum
        assert abs(out["all"]["nonadditive_subblock_difference"]) > 0.1
        surveys[key]=out
    return dict(exact_certificate_replay=True,surveys=surveys,
                inference_boundary="Full shear chi2 differences must not be replaced by a sum of separately evaluated blocks. Fixed-background hybrid results are not independent-likelihood replication, calibrated sigma, a Bayes factor, nor proof of temporal physics.")

def h27_exact_wilson_audit(root=ROOT):
    from fractions import Fraction
    from sympy import Matrix, ZZ
    from sympy.matrices.normalforms import smith_normal_form
    j = json.loads((root/"data/w33_20261108_h27_symmetrized_wilson_rank.json").read_text(encoding="utf-8"))
    def fmat(a):
        return np.array([[float(Fraction(x)) for x in row] for row in a])
    metric = fmat(j["electric_metric_G"])
    assert np.min(np.linalg.eigvalsh(metric))>0
    outcomes=[]
    for orbit in j["four_coordinate_orbits"]:
        charges=Matrix(orbit["unique_integer_wilson_charges"])
        snf=smith_normal_form(charges,domain=ZZ)
        invariant=[abs(int(snf[i,i])) for i in range(min(snf.shape)) if snf[i,i] != 0]
        b=fmat(orbit["mass_hessian_numerator_27"])/27
        ev=np.sort(eigh(b,metric,eigvals_only=True))
        assert len(invariant)==orbit["charge_lattice_rank"]
        assert invariant==orbit["wilson_charge_smith_normal_form"]
        assert np.sum(ev>1e-9)==orbit["symmetry_averaged_mass_hessian_rank"]
        if invariant==[1,1,1,1]:
            assert orbit["cosine_potential_minimum_modulo_2pi"]=="unique"
        outcomes.append(dict(index=orbit["selected_holonomy_index_zero_based"],
                             integer_charge_snf=invariant,
                             generalized_mass_eigenvalues=[round(float(v),12) for v in ev]))
    return dict(independent_numeric_and_integer_replay=True,orbits=outcomes,
                native_holonomy_dimension=4,
                possible_positive_mass_ranks=[2,4],
                limitation="The coupling amplitude is supplied rather than derived; the H27 holonomy basis is not identified with the separate Maxwell 46D harmonic subspace.")

def produce(root=ROOT):
    return dict(schema="w33.20261108.five_gate_extensions.v1",
                geometry=gauge_weight_and_rank_budget(root),
                quantum_walk=time_dependent_null_locality_budget(),
                e6=native_e6_determinant(root),
                photonic=correlated_photonic_noise(),
                cosmology=cosmology_nonadditivity(root),
                extra_h27=h27_exact_wilson_audit(root),
                scientific_status="Exact conditional math / synthetic optical control / source-certificate observational arithmetic; no unified physics or experimental photon established.")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",default="data/w33_20261108_five_gate_extensions.json")
    args=p.parse_args()
    result=produce()
    path=ROOT/args.output
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"output":str(path),"physics_gates":5,"extra_H27":True,
      "e6_phase":result["e6"]["native_coefficient_phase_radians"],
      "unlifted_harmonic":result["geometry"]["harmonic_zero_modes_after_rank4_lift"],
      "DES_delta":result["cosmology"]["surveys"]["des"]["all"]["delta_chi2_CPL_minus_fading"]},indent=2))
if __name__=="__main__":
    main()
