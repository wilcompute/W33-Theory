#!/usr/bin/env python3
"""
Pass 1154 (Step 2): Colored-vs-uncolored bridge rank checker.

Enforces: uncolored target rank cap = 81, colored (C3) cap = 243.
Severities: OK | UNCOLORED_OVERCLAIM | FATAL_OVERCLAIM | OVERCLAIM

Outputs: data/COLORED_BRIDGE_CHECKER_2026_07_27.json
"""
import json, pathlib
from datetime import datetime
PACKET_DIM = 243
STEINBERG_DIM = 81
FOURIER_MODES = 3
FOURIER_DECOMPOSITION = [
    {'mode': 0, 'label': 'trivial (1)',  'dim': 81, 'visible_in_uncolored': True},
    {'mode': 1, 'label': 'omega',        'dim': 81, 'visible_in_uncolored': False},
    {'mode': 2, 'label': 'omega^2',      'dim': 81, 'visible_in_uncolored': False},
]
def check_bridge(claimed_rank: int, target_is_colored: bool) -> dict:
    cap = PACKET_DIM if target_is_colored else STEINBERG_DIM
    if target_is_colored:
        sev = 'OVERCLAIM' if claimed_rank > cap else 'OK'
    else:
        sev = 'FATAL_OVERCLAIM' if claimed_rank > PACKET_DIM else \
              ('UNCOLORED_OVERCLAIM' if claimed_rank > cap else 'OK')
    return {'claimed_rank': claimed_rank, 'target_colored': target_is_colored,
            'rank_cap': cap, 'violation': sev != 'OK', 'severity': sev}
def main():
    cases = [(81,False,'OK'),(82,False,'UNCOLORED_OVERCLAIM'),
             (243,False,'FATAL_OVERCLAIM'),(243,True,'OK'),(244,True,'OVERCLAIM')]
    results = []
    for claimed, colored, expected in cases:
        r = check_bridge(claimed, colored)
        assert r['severity'] == expected, f'{r}'
        results.append(r)
    report = {'timestamp': datetime.utcnow().isoformat()+'Z',
        'schema': 'w33.pass1154.colored_bridge_checker.v1', 'status': 'PASS',
        'packet_total_dim': PACKET_DIM, 'steinberg_mode_dim': STEINBERG_DIM,
        'fourier_decomposition': FOURIER_DECOMPOSITION,
        'uncolored_rank_cap': STEINBERG_DIM, 'colored_rank_cap': PACKET_DIM,
        'test_cases': results,
        'policy': 'Uncolored target rank > 81 is UNCOLORED_OVERCLAIM; rank > 243 is FATAL.'}
    out = pathlib.Path('data/COLORED_BRIDGE_CHECKER_2026_07_27.json')
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=2))
    print('PASS 1154 colored bridge checker all assertions hold')
    return report
if __name__ == '__main__': main()
