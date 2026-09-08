"""Exact zipper cost, dyadic timing information and reversible record erasure.

These are finite software/information-theoretic witnesses, not measured energy.
The macro counter remains unbounded; n specifies the initial input ensemble.
"""
from collections import Counter
from fractions import Fraction
import json
from pathlib import Path

import w33_counter_zipper_microcode as micro
from w33_authenticated_counter_machine import BitStore, genesis
from w33_finite_control_unbounded_guest_hypervisor import FibreProductAddress
from w33_typed_universal_microvm import Instruction, Program


def trailing_ones(x):
    k = 0
    while x & 1:
        k += 1
        x >>= 1
    return k


def trace(x, length):
    return tuple(2 * trailing_ones(x + j) + 3 for j in range(length))


def dyadic_entropy(counts, n):
    total = 1 << n
    if sum(counts) != total or any(c <= 0 or c & (c - 1) for c in counts):
        raise ValueError("distribution must have dyadic multiplicities")
    return sum((Fraction(c, total) * (n - (c.bit_length() - 1)) for c in counts), Fraction())


def observed_partition(n, m):
    if not (type(n) is int and type(m) is int and 1 <= n and 0 <= m < n):
        raise ValueError("need 1 <= n and 0 <= m < n")
    length = 1 << m
    counts = Counter()
    signature_to_trace, trace_to_signature = {}, {}
    for x in range(1 << n):
        transcript = trace(x, length)
        signature = (x % length, trailing_ones(x // length))
        # Check both directions of the claimed sufficient statistic.
        if signature in signature_to_trace and signature_to_trace[signature] != transcript:
            raise AssertionError("signature lost timing information")
        if transcript in trace_to_signature and trace_to_signature[transcript] != signature:
            raise AssertionError("transcript lost signature information")
        signature_to_trace[signature] = transcript
        trace_to_signature[transcript] = signature
        counts[transcript] += 1
    observed = dyadic_entropy(list(counts.values()), n)
    predicted = Fraction(m + 2) - Fraction(2, 1 << (n - m))
    if observed != predicted:
        raise AssertionError("timing information law failed")
    aggregate = Counter()
    for transcript, count in counts.items():
        aggregate[sum(transcript)] += count
    aggregate_entropy = dyadic_entropy(list(aggregate.values()), n)
    if aggregate_entropy != predicted - m:
        raise AssertionError("batch-only timing lost a different amount of information")
    return {"n": n, "m": m, "increments": length,
            "distinct_transcripts": len(counts),
            "information_bits": str(observed),
            "batch_only_information_bits": str(aggregate_entropy),
            "complete_input_recovery": len(counts) == 1 << n}


def backend_cost_witness(steps=256):
    program = Program((Instruction("INC", 0, 0),), name="carry-cost-law")
    memory = BitStore()
    state = genesis(program, memory, (0, 0), session="carry-cost-law")
    fibre = FibreProductAddress(7, 2, 5)
    ticks = writes = 0
    for end in range(1, steps + 1):
        control = micro.start(program, state, fibre)
        before_ticks = ticks
        while control.phase != "DONE":
            receipt = micro.prove_tick(program, control, memory)
            control, nodes = micro.verify_tick(program, control, receipt)
            for node in nodes:
                memory.put(node)
            writes += len(nodes)
            ticks += 1
        state = micro.committed(program, control)
        if ticks - before_ticks != 2 * trailing_ones(end - 1) + 3:
            raise AssertionError("backend tick law failed")
        if ticks != 5 * end - 2 * end.bit_count() or writes != 3 * end - 2 * end.bit_count():
            raise AssertionError("backend amortized law failed")
        if memory.decode(state.roots[0]) != end:
            raise AssertionError("backend value failed")
        if len(memory.nodes) != end:
            raise AssertionError("preemption introduced additional distinct bit nodes")
    return {"increments": steps, "verified_prefixes": steps,
            "microticks": ticks, "bit_writes": writes,
            "distinct_retained_bit_nodes": len(memory.nodes),
            "prior_macro_bit_constructions": 2 * steps - steps.bit_count(),
            "extra_preemption_bit_writes": steps - steps.bit_count()}


def reversible_eraser(n=5, m=2):
    """Named permutation (Y,Z)->(Y,Z xor code(trace(Y-L))) on all states."""
    if not 0 <= m < n:
        raise ValueError("need 0 <= m < n")
    size, length = 1 << n, 1 << m
    transcripts = [trace(x, length) for x in range(size)]
    codes = {t: i for i, t in enumerate(sorted(set(transcripts)))}
    width = (len(codes) - 1).bit_length()
    def oracle(y):
        return codes[trace(y - length, length)] if length <= y < size + length else 0
    def transform(y, z):
        return y, z ^ oracle(y)
    states = {(y, z) for y in range(2 * size) for z in range(1 << width)}
    images = {transform(y, z) for y, z in states}
    if images != states or any(transform(*transform(y, z)) != (y, z) for y, z in states):
        raise AssertionError("eraser is not a total reversible permutation")
    if any(transform(x + length, codes[transcripts[x]]) != (x + length, 0) for x in range(size)):
        raise AssertionError("correlated timing record was not erased")
    return {"n": n, "m": m, "record_register_bits": width,
            "permutation_states": len(states), "all_correlated_records_reset": True,
            "timing_entropy_bits": str(dyadic_entropy(list(Counter(transcripts).values()), n)),
            "timing_entropy_given_final_counter_bits": "0",
            "scope": "Logical reversible permutation; no physical heat or gate-cost claim."}


def verify():
    cost = backend_cost_witness()
    rows = [observed_partition(n, m) for n in range(1, 10) for m in range(n)]
    eraser = reversible_eraser()
    # Telescoping law also holds for arbitrary starting offsets.
    for start in range(65):
        for length in range(1, 33):
            if sum(trace(start, length)) != 5 * length + 2 * start.bit_count() - 2 * (start + length).bit_count():
                raise AssertionError("offset cost law failed")
    return {"schema": "w33.carry-timing-information.v1", "status": "PASS",
            "backend": cost, "dyadic_partitions": rows, "reversible_eraser": eraser,
            "offset_intervals_checked": 65 * 32,
            "cost_law": "T(a,L)=5L+2popcount(a)-2popcount(a+L)",
            "information_law": "I(X;timing[0:2^m])=m+2-2^(1-(n-m)), X uniform on 0..2^n-1, 0<=m<n",
            "boundary": "Ideal exact completion timing; logical entropy is not measured device dissipation."}


if __name__ == "__main__":
    result = verify()
    wire = json.dumps(result, sort_keys=True, indent=2) + "\n"
    Path(__file__).with_name("w33_carry_timing_information_certificate.json").write_text(wire)
    print(json.dumps({"status": result["status"], "backend": result["backend"],
                      "partition_cases": len(result["dyadic_partitions"]),
                      "eraser": result["reversible_eraser"]}, indent=2))
