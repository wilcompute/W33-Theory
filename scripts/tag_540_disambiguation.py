#!/usr/bin/env python3
"""tag_540_disambiguation.py

Automated tagger and checker for the two 540s of W(3,3).

Usage:
  # Classify all corpus files and print report:
  python scripts/tag_540_disambiguation.py

  # Check a specific file for missing tags (pre-commit mode):
  python scripts/tag_540_disambiguation.py --check-only file1.md file2.tex

  # Tag a specific file in-place (adds {540:line-nonedge} or {540:point-nonedge}):
  python scripts/tag_540_disambiguation.py --tag-inplace file1.md
"""
import re, sys, os, argparse
from pathlib import Path

# ── Classification signals ─────────────────────────────────────────────────────
LINE_NONEDGE_SIGNALS = [
    r'\bframe\b', r'\bcube\b', r'skew.pair', r'skew pair',
    r'BT773', r'540.cube', r'frame.module', r'pi_540',
    r'3A1', r'C2.*S4', r'O_h', r'frame.action', r'frame.stabiliser',
    r'frame stabilizer', r'540:line-nonedge',
    r'\bframes\b',  # plural
]
POINT_NONEDGE_SIGNALS = [
    r'noncollinear.point', r'point.pair', r'mu=4', r'\bmu\b.*4',
    r'SRG\(40,12,2,4\)', r'bt1203', r'mu_distribution',
    r'non-adjacent.point', r'540:point-nonedge',
    r'point.non.edge',
]

# ── Known explicit aliases (from corpus audit, Pass 1128) ──────────────────────
ALIAS_MAP = {
    'BT773':  'line-nonedge',   # "540 cubes, one per 3A1 involution"
    'bt1203': 'point-nonedge',  # mu_distribution {4: 540}
    'bt1205': 'line-nonedge',   # "root_triples" — sixth alias, confirmed Pass 1128
}

def score_file(path: str) -> tuple:
    """Returns (line_score, point_score, tag_present, existing_tag) for a file."""
    try:
        text = Path(path).read_text(errors='replace').lower()
    except Exception:
        return 0, 0, False, None

    # Check if already tagged
    if '540:line-nonedge' in text:
        return 99, 0, True, 'line-nonedge'
    if '540:point-nonedge' in text:
        return 0, 99, True, 'point-nonedge'

    # Check if this file is a known alias source
    basename = os.path.basename(path).lower()
    for key, tag in ALIAS_MAP.items():
        if key.lower() in basename or key.lower() in text[:200]:
            return (10, 0) if tag == 'line-nonedge' else (0, 10), True, tag

    line_score  = sum(1 for sig in LINE_NONEDGE_SIGNALS  if re.search(sig, text, re.I))
    point_score = sum(1 for sig in POINT_NONEDGE_SIGNALS if re.search(sig, text, re.I))
    return line_score, point_score, False, None

def classify(path: str) -> str:
    """Returns 'line-nonedge', 'point-nonedge', 'ambiguous', or 'no-540'."""
    try:
        text = Path(path).read_text(errors='replace')
    except Exception:
        return 'no-540'
    if '540' not in text:
        return 'no-540'
    line_score, point_score, tagged, existing = score_file(path)
    if tagged:
        return existing
    if line_score > 0 and point_score == 0:
        return 'line-nonedge'
    if point_score > 0 and line_score == 0:
        return 'point-nonedge'
    if line_score == 0 and point_score == 0:
        return 'ambiguous'  # mentions 540 but no distinguishing context
    if line_score >= 2 * point_score:
        return 'line-nonedge'  # strong majority
    if point_score >= 2 * line_score:
        return 'point-nonedge'
    return 'ambiguous'

def check_only_mode(files):
    """Pre-commit mode: warn if any file mentions 540 without a disambiguation tag."""
    untagged = []
    for f in files:
        if not os.path.isfile(f):
            continue
        try:
            text = Path(f).read_text(errors='replace')
        except Exception:
            continue
        if '540' not in text:
            continue
        if '540:line-nonedge' in text or '540:point-nonedge' in text:
            continue
        # Find line numbers mentioning 540
        lines = [(i+1, l) for i, l in enumerate(text.splitlines()) if '540' in l]
        untagged.append((f, lines))
    if untagged:
        print("WARNING: Files mention '540' without disambiguation tag:")
        for f, lns in untagged:
            print(f"  {f}:")
            for lineno, line in lns[:3]:
                print(f"    line {lineno}: {line.strip()[:80]}")
        print("  Add {{540:line-nonedge}} or {{540:point-nonedge}} near each mention.")
        print("  See BT1628_540_disambiguation.py for the canonical vocabulary.")
        # Warning only, not fatal (--check-only is advisory)
    return len(untagged)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='*', help='Files to check (pre-commit mode)')
    parser.add_argument('--check-only', action='store_true')
    parser.add_argument('--tag-inplace', action='store_true')
    parser.add_argument('--corpus-dir', default='.', help='Root directory for corpus scan')
    args = parser.parse_args()

    if args.check_only and args.files:
        n = check_only_mode(args.files)
        sys.exit(0)  # Advisory: always exit 0

    # Full corpus scan mode
    root = Path(args.corpus_dir)
    results = {'line-nonedge': [], 'point-nonedge': [], 'ambiguous': [], 'no-540': []}
    extensions = {'.md', '.tex', '.py', '.json', '.txt'}

    for p in sorted(root.rglob('*')):
        if p.suffix not in extensions:
            continue
        if any(part.startswith('.') for part in p.parts):
            continue
        cat = classify(str(p))
        results[cat].append(str(p.relative_to(root)))

    print(f"\n── 540 Disambiguation Corpus Audit ──")
    print(f"Line-nonedge {'{540:line-nonedge}'}: {len(results['line-nonedge'])} files")
    print(f"Point-nonedge {'{540:point-nonedge}'}: {len(results['point-nonedge'])} files")
    print(f"Ambiguous (need manual tag): {len(results['ambiguous'])} files")
    print(f"No 540 mention: {len(results['no-540'])} files")

    if results['ambiguous']:
        print(f"\nAmbiguous files requiring manual tagging:")
        for f in results['ambiguous'][:20]:
            print(f"  {f}")
        if len(results['ambiguous']) > 20:
            print(f"  ... and {len(results['ambiguous'])-20} more")

    total_540 = len(results['line-nonedge']) + len(results['point-nonedge']) + len(results['ambiguous'])
    if total_540 > 0:
        pct_ambiguous = 100 * len(results['ambiguous']) / total_540
        print(f"\nAmbiguity rate: {pct_ambiguous:.1f}% of files mentioning 540")
        print(f"Target: <10% (currently {'✓ GOOD' if pct_ambiguous < 10 else '✗ NEEDS WORK'})")

if __name__ == '__main__':
    main()
