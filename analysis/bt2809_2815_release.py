#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / 'analysis'
DATA = ROOT / 'data'

PACKETS = [
    (2809, 'bt2809_selector_face_pairing_intertwiner.py', 'PART_BT2809_SELECTOR_FACE_PAIRING_INTERTWINER_results.json'),
    (2810, 'bt2810_signed_support_tomotope.py', 'PART_BT2810_SIGNED_SUPPORT_TOMOTOPE_results.json'),
    (2811, 'bt2811_support_first_codec.py', 'PART_BT2811_SUPPORT_FIRST_CODEC_results.json'),
    (2812, 'bt2812_support_module_d8.py', 'PART_BT2812_SUPPORT_MODULE_D8_results.json'),
    (2813, 'bt2813_all_q_support_lift.py', 'PART_BT2813_ALL_Q_SUPPORT_LIFT_results.json'),
    (2814, 'bt2814_support_lumped_markov_clock.py', 'PART_BT2814_SUPPORT_LUMPED_MARKOV_CLOCK_results.json'),
    (2815, 'bt2815_tomotope_parity_code.py', 'PART_BT2815_TOMOTOPE_PARITY_CODE_results.json'),
]


def run_packet(script: str) -> dict:
    cp = subprocess.run(
        [sys.executable, str(ANALYSIS / script)],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return json.loads(cp.stdout)


def canonical(x: dict) -> str:
    return json.dumps(x, indent=2, sort_keys=True) + '\n'


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--verify-frozen', action='store_true')
    args = ap.parse_args()
    DATA.mkdir(exist_ok=True)

    rows = []
    for pass_number, script, output in PACKETS:
        result = run_packet(script)
        target = DATA / output
        if args.verify_frozen:
            frozen = json.loads(target.read_text())
            assert result == frozen, f'drift: {output}'
        else:
            target.write_text(canonical(result))
        rows.append({
            'pass': pass_number,
            'script': f'analysis/{script}',
            'certificate': f'data/{output}',
            'status': result['status'],
            'check_count': result['check_count'],
            'certificate_sha256': hashlib.sha256(canonical(result).encode()).hexdigest(),
        })

    checks = {
        'seven_packets': len(rows) == 7,
        'pass_range_2809_2815': [r['pass'] for r in rows] == list(range(2809, 2816)),
        'all_exact_or_bounded': all(r['status'].startswith('COMPLETE') for r in rows),
        'total_exact_checks_78': sum(r['check_count'] for r in rows) == 78,
        'selector_operator_atlas': rows[0]['check_count'] == 10,
        'tomotope_incidence_realization': rows[1]['check_count'] == 16,
        'support_codec': rows[2]['check_count'] == 12,
        'D8_module': rows[3]['check_count'] == 7,
        'all_q_theorem': rows[4]['check_count'] == 12,
        'Markov_lumping': rows[5]['check_count'] == 9,
        'parity_code': rows[6]['check_count'] == 12,
    }
    assert all(checks.values()), [k for k, v in checks.items() if not v]
    aggregate = {
        'schema': 'w33.bt2809_2815.seven_frontiers.v1',
        'status': 'COMPLETE_78_EXACT_CHECKS_RTL_REMOTE_SYNTHESIS_PENDING',
        'canonical_pass_range': '2809-2815',
        'packets': rows,
        'total_exact_checks': sum(r['check_count'] for r in rows),
        'checks': checks,
        'check_count': len(checks),
        'headline': (
            'The PG(3,2) support bridge now closes objectwise: twelve exact selector operators; '
            'an explicit signed-support tomotope; a seven-bit affine codec; a q-independent D8 module; '
            'an all-finite-field support theorem; an exact lumped Markov clock; and a [3,2,2] parity-code cell controller.'
        ),
        'boundaries': {
            'RTL': 'Icarus/Yosys/nextpnr evidence is not promoted until the dedicated workflow is observed.',
            'physics': 'The Markov and parity results are finite combinatorial theorems, not physical dynamics without an added model.',
            'group': 'The support partition is D8-frame invariant, not invariant under the full symplectic group.',
        },
    }
    aggregate_path = DATA / 'PART_BT2809_BT2815_SEVEN_FRONTIERS_results.json'
    if args.verify_frozen:
        assert aggregate == json.loads(aggregate_path.read_text()), 'aggregate drift'
    else:
        aggregate_path.write_text(canonical(aggregate))
    print(f"PASS {aggregate['total_exact_checks']}/{aggregate['total_exact_checks']}")


if __name__ == '__main__':
    main()
