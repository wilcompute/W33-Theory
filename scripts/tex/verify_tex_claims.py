"""Verify numeric claims parsed from TeX against computed invariants (W33 etc.).
Writes JSON report to bundles/v23_toe_finish/v23/tex_claims_verification.json
"""
import json
from pathlib import Path

repo = Path(__file__).resolve().parents[2]
parsed = repo / 'bundles' / 'v23_toe_finish' / 'v23' / 'tex_claims_summary.json'
out = repo / 'bundles' / 'v23_toe_finish' / 'v23' / 'tex_claims_verification.json'

claims = json.load(open(parsed)) if parsed.exists() else []
report = []

# load computed invariants
w33 = {}
w33f = repo / 'bundles' / 'v23_toe_finish' / 'v23' / 'w33_aut_summary.json'
if w33f.exists():
    w33 = json.load(open(w33f))
# also lemma1/2 summaries
l1 = repo / 'bundles' / 'v23_toe_finish' / 'v23' / 'lemma1_check.json'
lem1 = json.load(open(l1)) if l1.exists() else {}
lem2 = repo / 'bundles' / 'v23_toe_finish' / 'v23' / 'lemma2_check.json'
lem2j = json.load(open(lem2)) if lem2.exists() else {}

for c in claims:
    file = c.get('file')
    env = c.get('env')
    nums = c.get('numbers', [])
    matches = []
    # check for aut claim
    if any('51840' in n.replace(',','') or '51,840' in n for n in nums):
        ok = (w33.get('grpsize') == 51840 if w33 else False) or (lem2j.get('parsed',{}).get('aut_order_w33')==51840)
        matches.append({'claim': 'Aut(W33)=51840', 'verified': ok, 'computed': w33.get('grpsize')})
    # check for edges=240
    if any('240' in n.replace(',','') for n in nums):
        # use lemma1_check for edge count implicitly by n_edges from producing 240 earlier
        # We can check degree distribution: edges = sum(deg)/2
        degs = lem1.get('degree_distribution', {}).get('deg_list') if lem1 else None
        edges = None
        if degs:
            edges = sum(degs)//2
            matches.append({'claim': 'edges=240', 'verified': edges==240, 'computed': edges})
    # check for 27 non-neighbors
    if any('27' == n or '27' in n for n in nums):
        nn_ok = lem1.get('non_neighbor_count_ok') if lem1 else None
        matches.append({'claim': '27 non-neighbors', 'verified': nn_ok, 'computed': lem1.get('non_neighbor_counts_example') if lem1 else None})
    if matches:
        report.append({'file': file, 'env': env, 'matches': matches, 'excerpt': c.get('excerpt')})

out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(report, indent=2))
print('Wrote', out)
