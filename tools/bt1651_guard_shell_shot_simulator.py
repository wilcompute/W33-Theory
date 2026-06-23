#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1651_guard_shell_shot_simulator.json'
MD = ROOT / 'analysis' / 'BT1651_guard_shell_shot_simulator.md'
TEX = ROOT / 'analysis' / 'BT1651_guard_shell_shot_simulator.tex'

ACTIVE = 1600
TOTAL = 2048
GUARD = TOTAL - ACTIVE
BINS = 168
DARK_GUARDS = 168
LOSS_GUARDS = 168
PARITY_GUARDS = 112
SHOTS = 2048

FAULT_PLAN = {
    'DARK_CLICK': 56,
    'MISSED_CLICK': 84,
    'CSS_SYNDROME': 28,
}

def role_for_timebin(tb: int) -> str:
    if tb < ACTIVE:
        return 'ACTIVE_WITTING_FRAME'
    off = tb - ACTIVE
    slot = off % 64
    if slot < 24:
        return 'DARK_REFERENCE'
    if slot < 48:
        return 'LOSS_PROBE'
    return 'PARITY_OVERFLOW'

def injected_fault(tb: int) -> str | None:
    role = role_for_timebin(tb)
    if role == 'DARK_REFERENCE' and ((tb - ACTIVE) % 3 == 0) and FAULT_PLAN['DARK_CLICK'] > 0:
        return 'DARK_CLICK'
    if role == 'LOSS_PROBE' and ((tb - ACTIVE) % 2 == 0):
        return 'MISSED_CLICK'
    if role == 'PARITY_OVERFLOW' and ((tb - ACTIVE) % 4 == 0):
        return 'CSS_SYNDROME'
    return None

def stream() -> list[dict]:
    rows = []
    fault_counts = Counter()
    for tb in range(TOTAL):
        role = role_for_timebin(tb)
        f = injected_fault(tb)
        # Cap deterministic counts exactly to the planned injection budgets.
        if f is not None and fault_counts[f] >= FAULT_PLAN[f]:
            f = None
        if f is not None:
            fault_counts[f] += 1
        detector_bin = tb % BINS if role != 'PARITY_OVERFLOW' else None
        rows.append({
            'time_bin': tb,
            'word11': format(tb, '011b'),
            'role': role,
            'detector_bin': detector_bin,
            'fault': f or 'NONE',
            'recovery_action': {
                'DARK_CLICK': 'subtract_dark_reference',
                'MISSED_CLICK': 'apply_loss_probe_correction',
                'CSS_SYNDROME': 'route_to_css_retry',
                'NONE': 'none',
            }[f or 'NONE'],
        })
    return rows

def main() -> None:
    rows = stream()
    role_counts = Counter(r['role'] for r in rows)
    fault_counts = Counter(r['fault'] for r in rows if r['fault'] != 'NONE')
    recovery_counts = Counter(r['recovery_action'] for r in rows if r['recovery_action'] != 'none')
    budgets = {'DARK_CLICK': DARK_GUARDS, 'MISSED_CLICK': LOSS_GUARDS, 'CSS_SYNDROME': PARITY_GUARDS}
    checks = {
        'total_2048': len(rows) == 2048,
        'active_1600': role_counts['ACTIVE_WITTING_FRAME'] == 1600,
        'guard_448': sum(role_counts[r] for r in ['DARK_REFERENCE','LOSS_PROBE','PARITY_OVERFLOW']) == 448,
        'dark_guard_168': role_counts['DARK_REFERENCE'] == 168,
        'loss_guard_168': role_counts['LOSS_PROBE'] == 168,
        'parity_guard_112': role_counts['PARITY_OVERFLOW'] == 112,
        'faults_within_guard_budget': all(fault_counts[k] <= budgets[k] for k in budgets),
        'fault_plan_exact': dict(fault_counts) == FAULT_PLAN,
        'recovery_counts_match_faults': sum(recovery_counts.values()) == sum(fault_counts.values()),
        'no_active_fault_injection': all(r['fault'] == 'NONE' for r in rows if r['role'] == 'ACTIVE_WITTING_FRAME'),
    }
    result = {
        'bt': 1651,
        'title': 'Guard-shell shot simulator',
        'verified': all(checks.values()),
        'source_packets': {'timebin_envelope':'data/bt1649_time_bin_qudit_envelope.json','guard_closure':'data/bt1650_guard_page_calibration_closure.json','fault_abi':'BT1606F parallel fault-path ABI / BT1614 synthetic stream'},
        'shot_count': SHOTS,
        'role_counts': dict(role_counts),
        'fault_counts': dict(fault_counts),
        'guard_budgets': budgets,
        'recovery_counts': dict(recovery_counts),
        'sample_rows': rows[:16] + rows[1600:1616] + rows[-16:],
        'interpretation': 'Synthetic 2048-bin stream exercises the 448-bin guard shell. Injected dark, loss, and parity faults are recovered within BT1650 guard budgets and mapped to BT1606/BT1614-style retry actions.',
        'honesty_boundary': 'Synthetic deterministic shot stream only; no hardware count rates, detector noise model, or calibrated recovery probability is claimed.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1651 Guard-shell Shot Simulator\n\nA synthetic 2048-bin photon stream exercises the 448-bin guard shell: 168 dark-reference, 168 loss-probe, and 112 parity-overflow bins. Injected dark, loss, and parity faults remain within guard budgets and map to subtract-dark, loss-correction, and CSS-retry actions. This is deterministic simulation, not hardware data.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1651: synthetic 2048-bin guard-shell shots inject dark/loss/parity faults and recover them within BT1650 guard budgets.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt': 1651, 'verified': result['verified'], 'fault_counts': dict(fault_counts)}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__': main()
