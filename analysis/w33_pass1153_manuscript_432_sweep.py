#!/usr/bin/env python3
"""
Pass 1153 (Step 1): Repository-wide manuscript sweep.

Tags every occurrence of '432 orbit', '432 carrier', 'Steinberg bridge',
'stabilizer is S5', 'stabilizer is A5' and related untyped 432-carrier
claims in .tex and .md files. Classifies each occurrence as:
  TYPED       -- already carries acting_group + stabilizer + color tags
  NEEDS_TAG   -- missing one or more required tags
  AMBIGUOUS   -- refers to 432 but context is unclear

Outputs: data/MANUSCRIPT_432_SWEEP_2026_07_27.json
"""
import re, json, pathlib
from datetime import datetime
REPO_ROOT = pathlib.Path(__file__).parent.parent
PATTERNS = [
    (r'432.{0,30}(orbit|carrier|action|set|class)', '432_carrier_ref'),
    (r'(orbit|carrier|action|set|class).{0,20}432\b', '432_carrier_ref_alt'),
    (r'Steinberg.{0,40}bridge', 'steinberg_bridge_ref'),
    (r'bridge.{0,40}Steinberg', 'steinberg_bridge_alt'),
    (r'stabilizer.{0,30}(S_5|S5|\\mathrm\{S\}_5)', 'stabilizer_S5'),
    (r'stabilizer.{0,30}(A_5|A5|\\mathrm\{A\}_5)', 'stabilizer_A5'),
    (r'the\s+432', 'definite_432_reference'),
]
TAG_MARKERS = [r'W\(E_?6\)', r'Sp\(4,3\)', r'C_3', r'color', r'acting.group',
               r'stabilizer.label', r'uncolored', r'colored']
SUFFIXES = {'.tex', '.md'}
EXCLUDE = {'analysis/w33_pass1153_manuscript_432_sweep.py',
           'PASS1153_1157_CONTINUATION_RELEASE.md',
           'PASS1148_1152_EXACT_CROSSED_BRIDGE_RELEASE.md'}
def classify(text, s, e):
    w = text[max(0,s-300):e+300]
    t = sum(1 for m in TAG_MARKERS if re.search(m, w, re.IGNORECASE))
    return 'TYPED' if t >= 3 else ('AMBIGUOUS' if t >= 1 else 'NEEDS_TAG')
def scan():
    hits = []; scanned = 0
    for fpath in sorted(REPO_ROOT.rglob('*')):
        if not fpath.is_file() or fpath.suffix not in SUFFIXES: continue
        rel = str(fpath.relative_to(REPO_ROOT))
        if any(rel == e or rel.startswith(e) for e in EXCLUDE): continue
        if any(p.startswith('.') for p in fpath.parts): continue
        try: text = fpath.read_text(encoding='utf-8', errors='replace')
        except: continue
        scanned += 1
        for pat, label in PATTERNS:
            for m in re.finditer(pat, text, re.IGNORECASE):
                line = text[:m.start()].count('\n') + 1
                hits.append({'file': rel, 'line': line, 'pattern': label,
                    'snippet': text[max(0,m.start()-60):m.end()+60].replace('\n',' '),
                    'classification': classify(text, m.start(), m.end())})
    summary = {}
    for h in hits: summary[h['classification']] = summary.get(h['classification'], 0) + 1
    report = {'timestamp': datetime.utcnow().isoformat()+'Z', 'files_scanned': scanned,
        'total_hits': len(hits), 'summary': summary,
        'policy': 'Every 432-carrier claim must carry: acting_group, stabilizer_label_or_order, color_retained_or_forgotten.',
        'hits': hits}
    out = REPO_ROOT / 'data' / 'MANUSCRIPT_432_SWEEP_2026_07_27.json'
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=2))
    print(f'Scanned {scanned} files, {len(hits)} hits, summary: {summary}')
    return report
if __name__ == '__main__': scan()
