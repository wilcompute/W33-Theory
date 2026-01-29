"""Check transitivity of Aut(W33) as reported by dreadnaut output.
Writes JSON verdict to bundles/v23_toe_finish/v23/lemma2_transitivity.json
"""
import json
from pathlib import Path
import re

repo = Path(__file__).resolve().parents[2]
w33f = repo / 'bundles' / 'v23_toe_finish' / 'v23' / 'w33_aut_summary.json'
out = repo / 'bundles' / 'v23_toe_finish' / 'v23' / 'lemma2_transitivity.json'

report = {}
if not w33f.exists():
    report['error'] = 'w33_aut_summary.json missing'
else:
    w33 = json.load(open(w33f))
    ro = w33.get('raw_output','')
    # find level 1 line
    m = re.search(r'level\s*1:\s*([0-9]+)\s+orbit', ro, re.IGNORECASE)
    if m:
        n_orbits = int(m.group(1))
        report['level_1_orbits'] = n_orbits
        report['transitive'] = (n_orbits==1)
    else:
        # fallback: look for '1 orbit; grpsize'
        if '1 orbit; grpsize' in ro:
            report['transitive'] = True
        else:
            report['transitive'] = False
    report['raw_snippet'] = '\n'.join(ro.splitlines()[:40])

out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(report, indent=2))
print('Wrote', out)
