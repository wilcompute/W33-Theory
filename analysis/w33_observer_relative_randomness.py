#!/usr/bin/env python3
"""Observer-relative randomness / decryptability separation certificate.

This is an exact finite-model companion to W33's reversible-observation work.
It deliberately separates:
  * information-theoretic uncertainty,
  * deterministic seeded generation,
  * perfect-secrecy encryption,
  * observer side information,
  * and computational/physical boundaries that entropy alone cannot settle.

No claim is made that cryptographic security, metaphysical quantum determinism,
or physical random-number generation is proved by these toy finite models.
"""
from collections import Counter
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "W33_OBSERVER_RELATIVE_RANDOMNESS.json"


def entropy(counter: Counter) -> float:
    total = sum(counter.values())
    return -sum((n / total) * math.log2(n / total) for n in counter.values() if n)


def conditional_entropy(joint: Counter, x_index: int, y_indices: tuple[int, ...]) -> float:
    xy = Counter()
    y = Counter()
    for row, n in joint.items():
        ykey = tuple(row[i] for i in y_indices)
        xy[(row[x_index],) + ykey] += n
        y[ykey] += n
    return entropy(xy) - entropy(y)


def mutual_information(joint: Counter, a_indices: tuple[int, ...], b_indices: tuple[int, ...]) -> float:
    ab, a, b = Counter(), Counter(), Counter()
    for row, n in joint.items():
        ka = tuple(row[i] for i in a_indices)
        kb = tuple(row[i] for i in b_indices)
        ab[ka + kb] += n
        a[ka] += n
        b[kb] += n
    return entropy(a) + entropy(b) - entropy(ab)


def v2(n: int) -> int:
    if n <= 0:
        return 0
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    return k


def increment_trace(x: int, length: int) -> tuple[int, ...]:
    return tuple(3 + 2 * v2(x + j + 1) for j in range(length))


def errors(seed: int, length: int, reuse: bool = False) -> tuple[int, ...]:
    out = []
    for j in range(length):
        z = (seed >> (0 if reuse else 2 * j)) & 3
        out.append(2 * ((z & 1) + (z >> 1) - 1))
    return tuple(out)


def observed(x: int, seed: int, length: int, reuse: bool = False) -> tuple[int, ...]:
    return tuple(t + e for t, e in zip(increment_trace(x, length), errors(seed, length, reuse)))


def deterministic_seed_model(seed_bits: int = 8, output_bits: int = 32) -> dict:
    assert seed_bits == 8 and output_bits == 32
    outputs = []
    for s in range(1 << seed_bits):
        y = int.from_bytes(hashlib.sha256(bytes([s])).digest()[:4], "big")
        outputs.append(y)
    # For this finite witness all 256 outputs happen to be distinct.
    assert len(set(outputs)) == 1 << seed_bits
    h_x = math.log2(len(set(outputs)))
    support_fraction = Fraction(1 << seed_bits, 1 << output_bits)
    return {
        "seed_bits": seed_bits,
        "output_bits": output_bits,
        "distinct_outputs": len(set(outputs)),
        "H_output_bits": h_x,
        "H_output_given_seed_bits": 0.0,
        "I_output_seed_bits": h_x,
        "support_fraction_of_uniform_output_space": str(support_fraction),
        "statistical_distance_lower_bound_from_uniform": str(1 - support_fraction),
        "boundary": "SHA-256 truncation is used only as a deterministic finite map; this is not a PRG security proof. Deterministic expansion cannot create information-theoretic entropy beyond the seed."
    }


def otp_model(nbits: int = 4) -> dict:
    joint = Counter()
    for m in range(1 << nbits):
        for k in range(1 << nbits):
            c = m ^ k
            joint[(m, c, k)] += 1
    h_m_given_c = conditional_entropy(joint, 0, (1,))
    h_m_given_ck = conditional_entropy(joint, 0, (1, 2))
    i_mc = mutual_information(joint, (0,), (1,))
    i_mk_given_c = h_m_given_c - h_m_given_ck
    assert abs(h_m_given_c - nbits) < 1e-12
    assert abs(h_m_given_ck) < 1e-12
    assert abs(i_mc) < 1e-12
    assert abs(i_mk_given_c - nbits) < 1e-12
    return {
        "message_bits": nbits,
        "H_message_given_ciphertext_bits": h_m_given_c,
        "H_message_given_ciphertext_and_key_bits": h_m_given_ck,
        "I_message_ciphertext_bits": i_mc,
        "side_information_resolution_bits": i_mk_given_c,
        "boundary": "Perfect secrecy is an information-theoretic statement for a uniform one-time key. Encryption is one mechanism that deliberately moves recoverability into side information; random strings need not be ciphertexts."
    }


def w33_noise_model(n: int = 3, m: int = 1) -> dict:
    N, L = 1 << n, 1 << m
    K = 4 ** L
    joint = Counter()
    for x in range(N):
        y = x + L
        for s in range(K):
            o = observed(x, s, L, reuse=False)
            joint[(o, y, s)] += 1
    h_o_given_y = conditional_entropy(joint, 0, (1,))
    h_o_given_ys = conditional_entropy(joint, 0, (1, 2))
    # Side-information identity:
    # H(O|Y)-H(O|Y,S)=I(O;S|Y).
    i_os_given_y = h_o_given_y - h_o_given_ys
    h_s_given_yo = conditional_entropy(joint, 2, (1, 0))
    assert abs(h_o_given_y - 1.5 * L) < 1e-12
    assert abs(h_o_given_ys) < 1e-12
    assert abs(h_s_given_yo - 1.0) < 1e-12
    return {
        "n": n,
        "m": m,
        "timings": L,
        "seed_register_bits": 2 * L,
        "H_observed_record_given_final_counter_bits": h_o_given_y,
        "H_observed_record_given_final_counter_and_seed_bits": h_o_given_ys,
        "I_record_seed_given_final_counter_bits": i_os_given_y,
        "H_seed_given_final_counter_and_record_bits": h_s_given_yo,
        "interpretation": "All apparent record entropy is resolved by the retained seed, while one bit of seed degeneracy remains invisible in the record."
    }


def shared_seed_privacy_model(n: int = 3) -> dict:
    rows = []
    for m in range(3):
        N, L = 1 << n, 1 << m
        for reuse in (False, True):
            K = 4 if reuse else 4 ** L
            marginal = Counter()
            h_local = []
            diff = Counter()
            for x in range(N):
                local = Counter(observed(x, s, L, reuse) for s in range(K))
                h_local.append(entropy(local))
                marginal.update(local)
                if reuse:
                    variants = {tuple(v - z[0] for v in z) for z in local}
                    assert len(variants) == 1
                    diff[next(iter(variants))] += 1
            h_o = entropy(marginal)
            h_o_x = sum(h_local) / N
            input_info = h_o - h_o_x
            rows.append({
                "m": m,
                "timings": L,
                "seed_reused": reuse,
                "input_information_bits": input_info,
                "timing_difference_information_bits": entropy(diff) if reuse else None,
            })
    r = {(row["m"], row["seed_reused"]): row for row in rows}
    assert abs(r[(1, True)]["input_information_bits"] - 2.5) < 1e-12
    assert abs(r[(2, True)]["input_information_bits"] - 3.0) < 1e-12
    assert abs(r[(1, True)]["timing_difference_information_bits"] - 2.5) < 1e-12
    assert abs(r[(2, True)]["timing_difference_information_bits"] - 3.0) < 1e-12
    return {
        "rows": rows,
        "interpretation": "A hidden common cause can reduce seed storage yet increase observer leakage because correlations let the observer cancel the common offset. Randomness/privacy depend on the observer's algebra, not only marginal noise entropy."
    }


def verify() -> dict:
    seed = deterministic_seed_model()
    otp = otp_model()
    w33 = w33_noise_model()
    shared = shared_seed_privacy_model()
    assert seed["H_output_given_seed_bits"] == 0.0
    assert otp["H_message_given_ciphertext_and_key_bits"] == 0.0
    assert w33["H_observed_record_given_final_counter_and_seed_bits"] == 0.0
    return {
        "schema": "w33.observer-relative-randomness.v1",
        "status": "PASS",
        "observer_key_identity": "H(X|O)-H(X|O,K)=I(X;K|O)",
        "finite_witnesses": {
            "deterministic_hidden_seed": seed,
            "one_time_pad": otp,
            "w33_reversible_noise_seed": w33,
            "shared_seed_privacy_failure": shared,
        },
        "classification": {
            "epistemic": "Outcome is determined by hidden state/seed; uncertainty can vanish with sufficient side information.",
            "cryptographic": "Recoverability is deliberately gated by a secret and/or bounded-computation assumption.",
            "computational": "Conditional entropy may be zero while prediction/inversion remains too expensive or undecidable in a universal model.",
            "quantum_operational": "Randomness certification lower-bounds unpredictability against an allowed adversary/side-information model; it does not by itself settle metaphysical interpretations of quantum mechanics.",
        },
        "universal_computation_boundary": "Deterministic transition laws do not imply a universal predictor: if a physical model can faithfully embed a universal counter machine, an oracle deciding whether every encoded execution ever reaches HALT would decide the halting problem under ordinary Turing-computability assumptions.",
        "core_conclusion": "Randomness is better modeled as a relation among outcome, observer side information, computational resources and physical access. Encryption is a special engineered case of observer-relative unresolved information, not a definition of randomness itself."
    }


if __name__ == "__main__":
    row = verify()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(row, indent=2, sort_keys=True) + "\n")
    print(json.dumps(row, indent=2, sort_keys=True))
