#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1585_operator_oam_appendix_claim_ledger.json'
MD = ROOT / 'analysis' / 'BT1585_operator_oam_appendix_claim_ledger.md'
TEX = ROOT / 'analysis' / 'BT1585_operator_oam_appendix_claim_ledger.tex'

CLAIMS = [
    {'tier':'exact finite','claim':'I,X,Z,F3,S generate the 216-element internal single-qutrit projective Clifford action','support':'BT1567, BT1570','allowed_language':'finite internal register algebra'},
    {'tier':'exact finite','claim':'centered OAM basis supports exact finite matrices for I,X,Z,F3,S','support':'BT1578','allowed_language':'finite centered-basis calibration'},
    {'tier':'exact finite','claim':'S phase matches centered quadratic lens phase signature [1,0,1]','support':'BT1571, BT1574','allowed_language':'discrete phase-signature equality'},
    {'tier':'calibration-level optics','claim':'F3 tritter/mixer and S/lens rows require optical loss, aberration, and overlap calibration','support':'BT1574, BT1578','allowed_language':'calibrated optical implementation target'},
    {'tier':'engineering leakage','claim':'radial leakage must be bounded and separately tested','support':'BT1577, BT1581','allowed_language':'symbolic leakage bound and pass/fail regime'},
    {'tier':'protocol witness','claim':'passive labels and active operator-leg behavior are experimentally distinguishable by controls','support':'BT1566, BT1569, BT1572, BT1575, BT1584','allowed_language':'falsifier protocol'},
    {'tier':'literature bridge','claim':'OAM qudits and same-photon register entanglement motivate the physical direction, while radial/azimuthal coupling motivates leakage witnesses','support':'BT1576','allowed_language':'external motivation and guardrail'},
    {'tier':'blocked physical overclaim','claim':'external optics are completely unnecessary in a physical implementation','support':'BT1579 firewall','allowed_language':'do not claim'},
    {'tier':'blocked physical overclaim','claim':'symbolic leakage thresholds are measured experimental values','support':'BT1577, BT1581','allowed_language':'do not claim'},
    {'tier':'blocked physical overclaim','claim':'finite recentering correction is already a calibrated optical device','support':'BT1573, BT1580','allowed_language':'do not claim'},
]

def main() -> None:
    counts={}
    for c in CLAIMS:
        counts[c['tier']]=counts.get(c['tier'],0)+1
    checks={
        'ten_claims': len(CLAIMS)==10,
        'three_exact_finite': counts.get('exact finite',0)==3,
        'has_calibration': counts.get('calibration-level optics',0)==1,
        'has_engineering': counts.get('engineering leakage',0)==1,
        'has_protocol': counts.get('protocol witness',0)==1,
        'has_literature': counts.get('literature bridge',0)==1,
        'three_blocked': counts.get('blocked physical overclaim',0)==3,
        'all_have_support': all(c['support'] for c in CLAIMS),
        'all_have_allowed_language': all(c['allowed_language'] for c in CLAIMS),
    }
    result={'bt':1585,'title':'Operator/OAM appendix claim ledger','verified':all(checks.values()),'claim_rows':CLAIMS,'tier_counts':counts,'interpretation':'The operator/OAM appendix ledger separates exact finite algebra/calibration claims from calibration-level optics, engineering leakage, protocol witnesses, literature motivation, and blocked physical overclaims.','honesty_boundary':'Claim ledger only. It does not rewrite the paper, rebuild the PDF, or assert experimental success.','checks':checks}
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    lines=['# BT1585 Operator/OAM Appendix Claim Ledger','','| Tier | Claim | Support | Allowed language |','|---|---|---|---|']
    for c in CLAIMS:
        lines.append(f"| {c['tier']} | {c['claim']} | {c['support']} | {c['allowed_language']} |")
    MD.write_text('\n'.join(lines)+'\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1585: operator/OAM appendix ledger separates exact finite claims from calibration, engineering, protocol, literature, and blocked physical overclaims.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1585,'verified':result['verified'],'tier_counts':counts}, indent=2))
    if not result['verified']:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
