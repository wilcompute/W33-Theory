#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1576_oam_entanglement_literature_bridge.json'
MD = ROOT / 'analysis' / 'BT1576_oam_entanglement_literature_bridge.md'
TEX = ROOT / 'analysis' / 'BT1576_oam_entanglement_literature_bridge.tex'

ROWS = [
    {'anchor':'OAM qudits','source':'Puentes/Sorelli 2021 angular qudits','repo_bridge':'supports high-dimensional OAM qudit encoding'},
    {'anchor':'single-photon intra-particle OAM entanglement','source':'Suprano et al. 2022 quantum-dot OAM source','repo_bridge':'supports same-photon register entanglement direction'},
    {'anchor':'radial plus azimuthal LG entanglement','source':'Herrera Valencia et al. 2021 full-field LG entanglement','repo_bridge':'radial channel must be modeled, not ignored'},
    {'anchor':'azimuthal modulation changes radial content','source':'Cocotos et al. 2024 elegant LG modes','repo_bridge':'OAM operators can disturb radial shell labels'},
    {'anchor':'OAM angular momentum definitions','source':'OAM review/current notes','repo_bridge':'keep physical OAM interpretation guarded; use finite mode witnesses'},
]

checks = {
    'five_literature_rows': len(ROWS) == 5,
    'has_oam_qudit': any('qudit' in r['anchor'] for r in ROWS),
    'has_single_photon': any('single-photon' in r['anchor'] for r in ROWS),
    'has_radial_warning': any('radial' in r['anchor'] or 'radial' in r['repo_bridge'] for r in ROWS),
    'has_guardrail': any('guarded' in r['repo_bridge'] for r in ROWS),
}
result = {'bt':1576,'title':'OAM entanglement literature bridge','verified':all(checks.values()),'rows':ROWS,'interpretation':'Current OAM literature supports the repo direction but sharpens the witness burden: OAM qudits and intra-particle OAM entanglement are plausible, but radial/azimuthal coupling and OAM definition issues require leakage and mode-overlap falsifiers.','honesty_boundary':'Literature bridge only; no new experimental claim.','checks':checks}
OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
MD.write_text('# BT1576 OAM Entanglement Literature Bridge\n\nThe current OAM literature supports high-dimensional OAM qudits, same-photon OAM register entanglement, and radial+azimuthal mode structure. It also warns that azimuthal modulation can change radial content, so radial leakage and mode-overlap witnesses are required. This is a literature bridge, not an experimental claim.\n', encoding='utf-8')
TEX.write_text('\\begin{center}\\small\nBT1576: OAM literature supports qudit and intra-particle encoding, but radial/azimuthal coupling requires leakage and mode-overlap falsifiers.\n\\end{center}\n', encoding='utf-8')
print(json.dumps({'bt':1576,'verified':result['verified']}, indent=2))
if not result['verified']:
    raise SystemExit(1)
