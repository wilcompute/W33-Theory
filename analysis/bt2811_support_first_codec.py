#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter
from itertools import product
import hashlib
import json


def weight(mask: int) -> int:
    return mask.bit_count()


FIBER = {mask: 1 << (weight(mask) - 1) for mask in range(1, 16)}
BASE = {}
_cursor = 0
for _mask in range(1, 16):
    BASE[_mask] = _cursor
    _cursor += FIBER[_mask]
assert _cursor == 40


def support_phase_polarity(v: tuple[int, int, int, int]):
    assert all(x in (0, 1, 2) for x in v)
    mask = sum((1 << i) for i, x in enumerate(v) if x)
    if not mask:
        return 0, 0, 0
    pivot = min(i for i, x in enumerate(v) if x)
    p = v[pivot]
    polarity = 0 if p == 1 else 1
    phase = 0
    slot = 0
    for i in range(pivot + 1, 4):
        if v[i]:
            bit = 0 if v[i] == p else 1
            phase |= bit << slot
            slot += 1
    assert slot == weight(mask) - 1
    return mask, phase, polarity


def projective_address(mask: int, phase: int) -> int:
    assert 1 <= mask <= 15
    assert 0 <= phase < FIBER[mask]
    return BASE[mask] + phase


def decode_projective(addr: int) -> tuple[int, int, int, int]:
    assert 0 <= addr < 40
    mask = max(mask for mask in range(1, 16) if BASE[mask] <= addr)
    assert addr < BASE[mask] + FIBER[mask]
    phase = addr - BASE[mask]
    pivot = min(i for i in range(4) if mask & (1 << i))
    v = [0, 0, 0, 0]
    v[pivot] = 1
    slot = 0
    for i in range(pivot + 1, 4):
        if mask & (1 << i):
            v[i] = 2 if ((phase >> slot) & 1) else 1
            slot += 1
    return tuple(v)


def encode_affine(v: tuple[int, int, int, int]) -> int:
    mask, phase, polarity = support_phase_polarity(v)
    if mask == 0:
        return 0
    return 1 + 2 * projective_address(mask, phase) + polarity


def decode_affine(code: int) -> tuple[int, int, int, int]:
    assert 0 <= code <= 80
    if code == 0:
        return (0, 0, 0, 0)
    z = code - 1
    addr, polarity = divmod(z, 2)
    v = decode_projective(addr)
    if polarity:
        v = tuple(0 if x == 0 else 3 - x for x in v)
    return v


def raw8(v: tuple[int, int, int, int]) -> int:
    return sum(x << (2 * i) for i, x in enumerate(v))


def main():
    vectors = list(product(range(3), repeat=4))
    codes = [encode_affine(v) for v in vectors]
    canonical_projective = [decode_projective(i) for i in range(40)]

    affine_roundtrip = all(decode_affine(encode_affine(v)) == v for v in vectors)
    projective_roundtrip = all(
        projective_address(*support_phase_polarity(v)[:2]) == i
        for i, v in enumerate(canonical_projective)
    )
    raw_uniqueness = len({raw8(v) for v in vectors}) == 81
    code_uniqueness = len(set(codes)) == 81 and set(codes) == set(range(81))

    support_counts = Counter(support_phase_polarity(v)[0] for v in vectors if any(v))
    expected_support_counts = {mask: 2 ** weight(mask) for mask in range(1, 16)}
    proj_support_counts = Counter(support_phase_polarity(v)[0] for v in canonical_projective)

    def add(a, b):
        return (a + b) % 3

    def neg(a):
        return (-a) % 3

    def Fp(v):
        x, z, y, w = v
        return (neg(z), x, y, w)

    def CXpf(v):
        x, z, y, w = v
        return (x, add(z, neg(w)), add(y, x), w)

    def CXfp(v):
        x, z, y, w = v
        return (add(x, y), z, y, add(w, neg(z)))

    def Zp(v):
        x, z, y, w = v
        return (x, add(z, 1), y, w)

    operations = {'F_p': Fp, 'CX_pf': CXpf, 'CX_fp': CXfp, 'Z_p': Zp}
    transition_hashes = {}
    support_transition_counts = {}
    for name, op in operations.items():
        table = [encode_affine(op(decode_affine(code))) for code in range(81)]
        assert len(set(table)) == 81
        payload = bytes(table)
        transition_hashes[name] = hashlib.sha256(payload).hexdigest()
        support_transition_counts[name] = len({
            (support_phase_polarity(decode_affine(code))[0],
             support_phase_polarity(op(decode_affine(code)))[0])
            for code in range(81)
        })

    checks = {
        'affine_roundtrip_81': affine_roundtrip,
        'affine_codes_exactly_0_to_80': code_uniqueness,
        'projective_roundtrip_40': projective_roundtrip,
        'projective_addresses_exactly_0_to_39': len(set(projective_address(*support_phase_polarity(v)[:2]) for v in canonical_projective)) == 40,
        'fiber_total_40': sum(FIBER.values()) == 40,
        'affine_support_counts_2_pow_weight': dict(support_counts) == expected_support_counts,
        'projective_support_counts_2_pow_weight_minus_1': dict(proj_support_counts) == FIBER,
        'raw8_unique_81': raw_uniqueness,
        'affine_width_7_is_information_optimal': (1 << 6) < 81 <= (1 << 7),
        'projective_width_6_is_information_optimal': (1 << 5) < 40 <= (1 << 6),
        'four_micro_isa_tables_permutations': len(transition_hashes) == 4,
        'four_micro_isa_hashes_distinct': len(set(transition_hashes.values())) == 4,
    }
    assert all(checks.values()), [k for k, v in checks.items() if not v]

    out = {
        'schema': 'w33.bt2811.support_first_codec.v1',
        'status': 'COMPLETE_EXACT_RTL_PENDING_REMOTE_SYNTHESIS',
        'affine_state_count': 81,
        'affine_code_width': 7,
        'projective_state_count': 40,
        'projective_code_width': 6,
        'raw_four_trit_width': 8,
        'support_base_table': {str(k): BASE[k] for k in BASE},
        'support_fiber_table': {str(k): FIBER[k] for k in FIBER},
        'micro_isa_transition_sha256': transition_hashes,
        'micro_isa_support_transition_pair_counts': support_transition_counts,
        'checks': checks,
        'check_count': len(checks),
        'engineering_reading': (
            'The full 81-state affine Pauli frame has an exact seven-bit enumerative code. '
            'Its 40 nonzero projective classes have an exact six-bit code factored as a four-bit support shell '
            'plus a variable relative-sign phase index. This is a one-bit storage reduction from the ordinary '
            'four two-bit-trit representation and supplies a support-first lookup decomposition.'
        ),
        'boundary': (
            'The Python reference proves lossless coding and exact micro-ISA transition tables. '
            'The accompanying SystemVerilog is synthesizable by construction but area, timing, power, and '
            'fold resistance remain pending until Icarus/Yosys/nextpnr CI is observed.'
        ),
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
