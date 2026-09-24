#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import math
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_20260924_adqc_record_arrow.json"
ADQC = ROOT / "analysis/w33_20260924_single_photon_adqc_qutrit_universality.py"
KB = 1.380649e-23
TEMP_K = 300.0
TOL = 3e-12


def load_adqc():
    spec = importlib.util.spec_from_file_location("w33_adqc", ADQC)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def random_density(rng, d=3):
    A = rng.normal(size=(d,d)) + 1j*rng.normal(size=(d,d))
    rho = A @ A.conj().T
    return rho / np.trace(rho)


def entropy_nats(probs):
    return -sum(float(p)*math.log(float(p)) for p in probs if p > 0)


def main():
    adqc = load_adqc()
    _omega, F, X, _Z, _CZ, E, plus = adqc.build_operators()
    phases = [0.17, -0.91, 1.43]
    R = np.diag(np.exp(1j*np.array(phases)))
    U = F @ R

    _basis, branches = adqc.single_register_kraus(F, X, E, plus, phases)
    rng = np.random.default_rng(10943)
    trials = []
    for _ in range(32):
        rho = random_density(rng)
        probs = []
        corrected = np.zeros((3,3), dtype=complex)
        for m, K, _target in branches:
            sigma = K @ rho @ K.conj().T
            p = float(np.real(np.trace(sigma)))
            probs.append(p)
            C = np.linalg.matrix_power(X, m)
            corrected += C @ sigma @ C.conj().T

        target = U @ rho @ U.conj().T
        err = float(np.linalg.norm(corrected-target))
        trials.append({"probabilities":probs, "corrected_channel_error":err})
        assert max(abs(p-1/3) for p in probs) < TOL
        assert err < TOL

    probs = [1/3,1/3,1/3]
    Hn = entropy_nats(probs)
    Hb = Hn/math.log(2)
    landauer_per_trit = KB*TEMP_K*Hn
    assert abs(Hn-math.log(3)) < TOL
    assert abs(Hb-math.log2(3)) < TOL

    record_rows = []
    for n in [1,2,3,10,40,81]:
        record_rows.append({
            "adaptive_measurements":n,
            "possible_records":3**n,
            "record_entropy_nats":n*Hn,
            "record_entropy_bits":n*Hb,
            "symmetric_erasure_floor_J_at_300K":n*landauer_per_trit,
        })


    out = {
        "schema":"w33.20260924.adqc_record_arrow.v1",
        "status":"PASS_REVERSIBLE_LOGICAL_UPDATE_WITH_CLASSICAL_RECORD_ARROW",
        "exact_gate_fact":{
            "branch_probabilities":[1/3,1/3,1/3],
            "branch_entropy_nats":Hn,
            "branch_entropy_bits":Hb,
            "random_density_trials":trials,
            "logical_channel_after_frame_correction":
                "rho -> (F R(theta)) rho (F R(theta))^dagger",
            "logical_channel_is_unitary":True,
        },
        "record_thermodynamics":{
            "temperature_K":TEMP_K,
            "k_B_J_per_K":KB,
            "symmetric_record_reset_floor_per_measurement_J":landauer_per_trit,
            "formula":"k_B T ln(3) for erasure of one equiprobable trit",
            "records":record_rows,
            "measurement_vs_erasure_boundary":
                "The Landauer floor applies to resetting the classical record.",
        },

        "temporal_synthesis":{
            "reversible_update":
                "The corrected stationary-memory channel is unitary.",
            "record_arrow":
                "Adaptive analyzer outcomes create an ordered classical branch record.",
            "key_separation":(
                "Computation supplies change without requiring an irreversible logical "
                "channel; historical bookkeeping can live in the controller."
            ),
        },
        "holonet_consequence":(
            "A flying photonic qutrit can be the measured program head while "
            "stationary qutrit memories carry the reversible logical state."
        ),
        "literature":[
            "Proctor et al., arXiv:1510.06462",
            "Sagawa and Ueda, Phys. Rev. Lett. 102, 250602 (2009)",
            "Erker et al., Phys. Rev. X 7, 031022 (2017)",
            "Pearson et al., Phys. Rev. X 11, 021029 (2021)",
        ],
        "boundary":(
            "Exact for the ideal ADQC branch model and symmetric record reset; "
            "not a complete detector or controller thermodynamic model."
        ),
    }

    OUT.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":out["status"],
        "branch_entropy_bits":Hb,
        "reset_floor_J_300K":landauer_per_trit,
        "max_corrected_error":max(
            r["corrected_channel_error"] for r in trials
        ),
    },indent=2))


if __name__=="__main__":
    main()
