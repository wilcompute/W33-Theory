#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1579_paper_splice_release_operator_oam.json'
MD = ROOT / 'analysis' / 'BT1579_paper_splice_release_operator_oam.md'
TEX = ROOT / 'analysis' / 'BT1579_paper_splice_release_operator_oam.tex'

INSERTS = [
    'analysis/BT1564_BT1566_holonet_insert.tex',
    'analysis/BT1567_BT1569_holonet_insert.tex',
    'analysis/BT1570_BT1572_holonet_insert.tex',
    'analysis/BT1573_BT1576_holonet_insert.tex',
]

CLAIMS = [
    {'tier':'exact finite','claim':'I,X,Z,F3,S generate 216-element internal Clifford action','support':'BT1567/BT1570'},
    {'tier':'exact finite','claim':'centered S phase equals quadratic lens signature [1,0,1]','support':'BT1571/BT1574'},
    {'tier':'exact finite','claim':'core gates have centered-basis matrices','support':'BT1578'},
    {'tier':'calibration','claim':'F3 three-mode mixer and lens row require optical calibration','support':'BT1574/BT1578'},
    {'tier':'engineering','claim':'radial leakage envelopes bound OAM/radial coupling','support':'BT1577'},
    {'tier':'protocol','claim':'passive-vs-active table separates labels from operator behavior','support':'BT1572/BT1575'},
    {'tier':'literature bridge','claim':'OAM qudit and same-photon register directions are plausible but need leakage witnesses','support':'BT1576'},
    {'tier':'blocked','claim':'all external optics can be removed from a physical implementation','support':'firewall'},
]

def main() -> None:
    checks={'four_insert_packets':len(INSERTS)==4,'all_insert_paths_exist':all((ROOT/p).exists() for p in INSERTS),'eight_claims':len(CLAIMS)==8,'has_exact_rows':sum(c['tier']=='exact finite' for c in CLAIMS)==3,'has_blocked_row':any(c['tier']=='blocked' for c in CLAIMS),'has_literature_row':any(c['tier']=='literature bridge' for c in CLAIMS)}
    result={'bt':1579,'title':'Paper splice release for operator-on-photon/OAM packet','verified':all(checks.values()),'insert_packets':INSERTS,'claim_rows':CLAIMS,'interpretation':'BT1564-BT1578 are packaged for a claim-tiered appendix/release section. Exact finite algebra and calibration rows are separated from calibration, engineering, protocol, literature-bridge, and blocked claims.','honesty_boundary':'Release packet only; no direct rewrite of photonic_holonet.tex or PDF rebuild is claimed.','checks':checks}
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    lines=['# BT1579 Paper Splice Release for Operator/OAM Packet','','Insert packets:']
    for p in INSERTS: lines.append(f'- `{p}`')
    lines += ['', 'Claim rows:']
    for c in CLAIMS: lines.append(f"- **{c['tier']}**: {c['claim']} ({c['support']})")
    MD.write_text('\n'.join(lines)+'\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1579: operator-on-photon/OAM packet is release-ready as claim-tiered appendix material; exact finite rows are separated from calibration, engineering, protocol, literature, and blocked rows.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1579,'verified':result['verified'],'claims':len(CLAIMS)}, indent=2))
    if not result['verified']: raise SystemExit(1)

if __name__=='__main__': main()
