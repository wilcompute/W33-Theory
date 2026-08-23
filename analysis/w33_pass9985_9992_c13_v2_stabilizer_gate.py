#!/usr/bin/env python3
"""Pass9985-9992: exact gate for an actual C13 inside the canonical V2/Co0 stabilizer.

This pass does NOT assume the abstract GL(12,2) C13 from Pass9973-9980 comes
from Co0.  It proves sharp necessary conditions from the actual canonical V2
construction and standard subgroup orders already present in the repository.

Facts used:
* V2 comes from the unique pure order-8 Co0 class M; |C_Co0(M)| = 48384.
* Every nonzero V2 class is type 8, hence a Leech frame direction.
* A frame/type-4-vector stabilizer in Co1 is 2^11:M24, and 13 does not divide
  its order.
* N(<M>)/C(M) embeds in Aut(C8), of order 4.

Consequences for any C13 <= Stab_Co0(V2):
* it is fixed-point-free on V2\{0}, hence has exactly 315 thirteen-cycles;
* it cannot normalize <M>, hence must move M through an orbit of size 13;
* any maximal Co1 overgroup containing such a C13 and the stabilizer must have
  a factor 13.  From the ATLAS maximal-subgroup list used by the project, the
  surviving candidates are 3.Suz:2 and (A4 x G2(4)):2.

The existence question is therefore reduced to two explicit maximal-overgroup
branches.  This is a gate theorem, not an existence theorem.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/PART_W33_PASS9985_9992_C13_V2_STABILIZER_GATE.json'

M24 = 244_823_040
FRAME_STAB = (2**11) * M24
CENTRALIZER_M = 48_384
AUT_C8 = 4
V2_NONZERO = 4095


def factors(n: int):
    out = {}
    p = 2
    while p*p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def main() -> int:
    assert V2_NONZERO % 13 == 0 and V2_NONZERO // 13 == 315
    assert CENTRALIZER_M % 13 != 0
    assert AUT_C8 % 13 != 0
    assert FRAME_STAB % 13 != 0
    assert factors(CENTRALIZER_M) == {2: 8, 3: 3, 7: 1}
    assert factors(M24).get(13, 0) == 0

    out = {
        'schema': 'w33.pass9985_9992.c13_v2_stabilizer_gate.v1',
        'status': 'PASS',
        'passes': '9985-9992',
        'canonical_V2': {
            'pure_order8_class_unique': True,
            'centralizer_order': CENTRALIZER_M,
            'centralizer_factorization': factors(CENTRALIZER_M),
            'nonzero_vectors': V2_NONZERO,
            'all_nonzero_are_type8_frame_directions': True,
        },
        'fixed_point_gate': {
            'frame_stabilizer': '2^11:M24 in Co1',
            'frame_stabilizer_order': FRAME_STAB,
            'divisible_by_13': False,
            'consequence': 'Any C13 in Stab(V2) fixes no nonzero V2 vector/frame direction.',
            'forced_cycle_count': 315,
        },
        'normalizer_gate': {
            'C_Co0(M)_order': CENTRALIZER_M,
            'Aut_C8_order': AUT_C8,
            'reason': 'N(<M>)/C(M) embeds in Aut(C8), so an element of order 13 normalizing <M> would centralize M.',
            'consequence': 'No C13 in Stab(V2) can normalize <M>; it must move M through an orbit whose size is divisible by 13.',
        },
        'maximal_overgroup_gate': {
            'Co1_maximal_overgroups_with_factor13_relevant_here': ['3.Suz:2', '(A4 x G2(4)):2'],
            'consequence': 'An actual Co0/Co1 realization of the abstract V2 C13 must be found through one of these 13-bearing branches (or an explicitly verified subgroup thereof).',
        },
        'theorem': ('If C13 <= Stab_Co0(V2), then it is semiregular on V2\\{0} with 315 cycles, '
                    'it cannot normalize the unique pure-order-8 generator M, and the search for it reduces to '
                    'the 13-bearing maximal-overgroup branches 3.Suz:2 and (A4 x G2(4)):2.'),
        'existence_status': 'OPEN after this pass: the exact gates are proved, but no explicit Co0 word of order 13 stabilizing V2 is certified.',
        'boundary': ('Uses exact repository centralizer/frame data plus standard subgroup/normalizer facts. '
                     'It deliberately does not identify the abstract GL(12,2) companion C13 with a Co0 element.'),
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status':'PASS','cycles':315,'centralizer_has_13':False,'existence':'OPEN'}))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
