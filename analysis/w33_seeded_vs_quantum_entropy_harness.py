#!/usr/bin/env python3
"""Seeded pseudorandom vs ideal-quantum-reference HoloVM entropy harness.

Two source models are kept distinct from deterministic VM transport:

1. Seeded deterministic byte generator: Y=(73*S+41) mod 256.
2. Ideal Born-uniform byte reference: all 256 outcomes equiprobable.

The seedless marginals are exactly identical, but the seeded arm has H(Y|S)=0.
Every byte is then fed to the same HoloVM two-counter guest, proving that the
VM transports source entropy/provenance rather than creating it.

An optional JSON metadata file may record an external quantum-randomness
certificate or dataset reference. This script does not independently validate
that physical certificate.
"""
from collections import Counter
from fractions import Fraction
import argparse
import json
import math
from pathlib import Path

from w33_typed_universal_microvm import (
    Capability,
    Carrier,
    TypedUniversalMicroVM,
    add_r1_into_r0_program,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "W33_SEEDED_VS_QUANTUM_ENTROPY_HARNESS.json"


def entropy(counter):
    total = sum(counter.values())
    return -sum((n/total)*math.log2(n/total) for n in counter.values() if n)


def min_entropy(counter):
    total = sum(counter.values())
    pmax = max(counter.values()) / total
    return -math.log2(pmax)


def seeded_byte(seed):
    return (73 * seed + 41) % 256


def vm_byte(value):
    program = add_r1_into_r0_program()
    cap = Capability(Carrier.CIRCUIT_ST81, 81)
    vm = TypedUniversalMicroVM(program, cap)
    vm.state.counter0 = 0
    vm.state.counter1 = int(value)
    final = vm.run(fuel=1024)
    assert final.halted
    assert final.counter0 == value
    assert final.counter1 == 0
    return {
        "input": value,
        "counter0": final.counter0,
        "counter1": final.counter1,
        "steps": final.steps,
        "trace_root": final.trace_root,
    }


def total_variation(a, b):
    keys = set(a) | set(b)
    ta, tb = sum(a.values()), sum(b.values())
    return Fraction(
        sum(abs(a.get(k, 0)*tb - b.get(k, 0)*ta) for k in keys),
        2 * ta * tb,
    )


def load_external_metadata(path):
    if path is None:
        return None
    row = json.loads(Path(path).read_text())
    required = {"source", "adversary_model", "certified_min_entropy_bits"}
    missing = sorted(required - set(row))
    if missing:
        raise ValueError(f"external metadata missing {missing}")
    if float(row["certified_min_entropy_bits"]) < 0:
        raise ValueError("negative certified min entropy")
    return row


def verify(external_metadata=None):
    prg_outputs = [seeded_byte(s) for s in range(256)]
    ideal_outputs = list(range(256))
    assert len(set(prg_outputs)) == 256

    prg = Counter(prg_outputs)
    ideal = Counter(ideal_outputs)
    assert prg == ideal
    tv = total_variation(prg, ideal)
    assert tv == 0

    h_prg = entropy(prg)
    hmin_prg = min_entropy(prg)
    h_ideal = entropy(ideal)
    hmin_ideal = min_entropy(ideal)
    assert h_prg == h_ideal == 8.0
    assert hmin_prg == hmin_ideal == 8.0

    vm_rows = [vm_byte(v) for v in ideal_outputs]
    terminal = Counter((r["counter0"], r["counter1"]) for r in vm_rows)
    assert len(terminal) == 256
    assert all(n == 1 for n in terminal.values())

    ext = load_external_metadata(external_metadata)
    external_status = (
        "PENDING_EXTERNAL_CERTIFICATE"
        if ext is None else "METADATA_ATTACHED_NOT_REVERIFIED"
    )

    return {
        "schema": "w33.seeded-vs-quantum-entropy-harness.v1",
        "status": "PASS",
        "seeded_source": {
            "map": "Y=(73*S+41) mod 256",
            "seed_space": 256,
            "output_support": 256,
            "H_output_bits": h_prg,
            "Hmin_output_bits": hmin_prg,
            "H_output_given_seed_bits": 0.0,
        },
        "ideal_quantum_reference": {
            "model": "one ideal 8-bit Born-uniform measurement outcome",
            "output_support": 256,
            "H_output_bits": h_ideal,
            "Hmin_output_bits": hmin_ideal,
            "classical_seed_variable": None,
            "physical_certification_status": external_status,
            "external_metadata": ext,
        },
        "seedless_marginal_total_variation": str(tv),
        "holovm_transport": {
            "guest": "add-r1-into-r0",
            "carrier": "circuit216/steinberg81",
            "inputs_exhaustively_checked": 256,
            "terminal_states": len(terminal),
            "max_steps": max(r["steps"] for r in vm_rows),
            "source_agnostic_distribution_result": (
                "Because the two source marginals are identical, the deterministic HoloVM "
                "terminal-state distributions are identical. Source provenance lives in side "
                "information/evidence, not in this downstream byte histogram."
            ),
        },
        "core_result": (
            "A deterministic seeded source can be exactly uniform to a seedless observer while "
            "remaining perfectly decryptable to the seed holder. Matching output statistics do "
            "not identify whether entropy is fundamental, pseudorandom, or externally certified."
        ),
        "boundary": (
            "The built-in quantum arm is an ideal distribution reference, not a laboratory "
            "randomness certificate. Device-independent or QRNG certification must enter as "
            "external evidence with an explicit adversary model."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--external-quantum-metadata")
    args = parser.parse_args()
    result = verify(args.external_quantum_metadata)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
