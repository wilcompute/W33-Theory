#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1606_mass_gap_fault_bridge_firewall.json'
MD = ROOT / 'analysis' / 'BT1606_mass_gap_fault_bridge_firewall.md'
TEX = ROOT / 'analysis' / 'BT1606_mass_gap_fault_bridge_firewall.tex'

ROWS = [
    {'tier':'finite exact source','claim':'BT679 gives a finite K33 spectral-gap lower-bound model Delta >= 1/6','support':'BREAKTHROUGH_BT679_YANG_MILLS_MASS_GAP.md'},
    {'tier':'finite exact ABI','claim':'BT1603 gives a finite Witting/Hesse/CSS photonic computation ABI with 1600 frames and 72 CSS rows','support':'data/bt1603_universal_computation_proof_closure.json'},
    {'tier':'candidate bridge','claim':'minimum logical-error energy in the ABI may be comparable to the finite mass-gap normalization','support':'requires new decoder/fault simulation'},
    {'tier':'required test','claim':'compute minimum undetectable CSS error chain and convert through a stated W33 unit map','support':'not yet built'},
    {'tier':'blocked overclaim','claim':'the W33 photonic ABI proves the continuum Yang-Mills Millennium theorem','support':'explicitly blocked'},
    {'tier':'blocked overclaim','claim':'symbolic logical-error weight is a measured mass gap','support':'explicitly blocked'},
]

def main() -> None:
    counts = {}
    for r in ROWS:
        counts[r['tier']] = counts.get(r['tier'], 0) + 1
    checks = {
        'six_rows': len(ROWS) == 6,
        'has_finite_source': counts.get('finite exact source', 0) == 1,
        'has_finite_abi': counts.get('finite exact ABI', 0) == 1,
        'has_candidate_bridge': counts.get('candidate bridge', 0) == 1,
        'has_required_test': counts.get('required test', 0) == 1,
        'two_blocked_overclaims': counts.get('blocked overclaim', 0) == 2,
        'all_have_support': all(r['support'] for r in ROWS),
    }
    result = {
        'bt': 1606,
        'title': 'Mass-gap / fault-tolerance bridge firewall',
        'verified': all(checks.values()),
        'source_packets': {
            'yang_mills_gap': 'BREAKTHROUGH_BT679_YANG_MILLS_MASS_GAP.md',
            'universal_abi': 'data/bt1603_universal_computation_proof_closure.json',
        },
        'claim_rows': ROWS,
        'tier_counts': counts,
        'interpretation': 'The mass-gap/fault-tolerance bridge is a meaningful candidate because both sides are finite spectral/energy-gap objects. The next required object is a decoder/fault simulation computing the minimum undetectable CSS error chain and a unit conversion. Continuum Yang-Mills claims remain blocked.',
        'honesty_boundary': 'This firewall does not prove the continuum Yang-Mills mass gap and does not report measured fault-tolerance data.',
        'checks': checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    MD.write_text('# BT1606 Mass-gap / Fault-tolerance Bridge Firewall\n\nBT679 gives a finite K33 spectral-gap lower-bound model. BT1603 gives a finite Witting/Hesse/CSS photonic computation ABI. The possible bridge is the minimum undetectable CSS logical-error energy, but that requires a decoder/fault simulation and a stated unit map. Continuum Yang-Mills and measured hardware claims remain blocked.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1606: mass-gap/fault-tolerance bridge is a candidate finite-gap comparison; continuum Yang--Mills and measured-hardware claims remain blocked.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1606,'verified':result['verified'],'tiers':counts}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
