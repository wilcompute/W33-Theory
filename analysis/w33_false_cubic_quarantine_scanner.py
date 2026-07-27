#!/usr/bin/env python3
"""
Step 1: Repository-wide dependency scanner for the false historical cubic.

Scans every .py, .tex, .md, .json file in the repository for occurrences of
the false eigenvalue set {-7, -1, 5} (as a triple), the 32-dimensional
multiplicity packet, the old generating function Z(x) Taylor coefficients
(8, -248, ...), and any reference to the old polynomial roots or the
32-dimensional packet.

Classification for each hit:
  COPY    — verbatim reproduction, no independent derivation visible
  DERIVED — file contains its own derivation chain (manual review flag)
  INVALIDATED — file depends on the false spectrum as an axiom

Outputs:
  data/QUARANTINE_2026_07_27_false_cubic_scan.json

Usage:
  python analysis/w33_false_cubic_quarantine_scanner.py
"""
import re
import json
import os
import pathlib
from datetime import datetime

REPO_ROOT = pathlib.Path(__file__).parent.parent

# Patterns that indicate the false cubic or its direct descendants
FALSE_PATTERNS = [
    # Old eigenvalue triple (any ordering)
    (r'(?<!\w)-7(?!\w).*(?<!\w)-1(?!\w).*(?<!\w)5(?!\w)', 'old_eigenvalue_triple_ordered'),
    (r'\{\s*-7\s*,\s*-1\s*,\s*5\s*\}', 'old_eigenvalue_set'),
    (r'\{\s*5\s*,\s*-1\s*,\s*-7\s*\}', 'old_eigenvalue_set_alt'),
    # Old multiplicities (16, 10, 6) — sum 32
    (r'multiplicit\w+.*\b16\b.*\b10\b.*\b6\b', 'old_multiplicities_1610_6'),
    (r'\b16\b.*\b10\b.*\b6\b.*multiplicit', 'old_multiplicities_6_10_16'),
    # 32-dimensional packet
    (r'32.{0,20}(dimen|packet|eigenspace|mode)', 'dim_32_packet'),
    (r'(dimen|packet|eigenspace|mode).{0,20}32\b', 'dim_32_packet_alt'),
    # Old Z(x) claim
    (r'Z\(-1\)\s*=\s*0', 'Zx_at_minus1_zero'),
    # Old Taylor coefficients
    (r'8\s*,\s*-248', 'old_taylor_coeff_8_248'),
    # Old minimal polynomial factors
    (r'\(t\+1\)\s*\(\s*\(t\+1\)\^?2\s*-\s*36\s*\)', 'old_minimal_poly_factored'),
    (r't\^3\s*[+-]\s*3t\^2\s*-\s*33t\s*-\s*35', 'old_min_poly_expanded'),
    # Old root -7 appearing with spectral context
    (r'eigenval\w*.*-7', 'eigenvalue_neg7'),
    (r'-7.*eigenval', 'eigenvalue_neg7_alt'),
]

EXCLUDE_PATHS = {
    'analysis/2026-07-27_shifted_adjacency_spectral_erratum.md',
    'analysis/w33_shifted_adjacency_spectral_audit.py',
    'tests/test_w33_shifted_adjacency_spectral_audit.py',
    'data/PART_2026_07_27_W33_SHIFTED_ADJACENCY_SPECTRAL_AUDIT.json',
    'analysis/w33_false_cubic_quarantine_scanner.py',
    'analysis/2026-07-27_false_cubic_quarantine_report.md',
}

SUFFIXES = {'.py', '.tex', '.md', '.json', '.txt'}
PRUNED_DIRS = {
    '.git',
    '.mypy_cache',
    '.pytest_cache',
    '.ruff_cache',
    '.tox',
    '.venv',
    '__pycache__',
    'node_modules',
}
ACTIVE_CORPUS_DIRS = {
    'analysis',
    'code',
    'data',
    'docs',
    'exploration',
    'formal',
    'hardware',
    'lean',
    'lib',
    'manuscripts',
    'notebooks',
    'paper',
    'papers',
    'passes',
    'proofs',
    'reports',
    'scripts',
    'src',
    'submission',
    'tests',
    'tex',
    'theorems',
    'theory',
    'tools',
    'w33',
}


def classify_hit(content: str, path_str: str) -> str:
    """Heuristic classification of a match in a file."""
    # If it's in the erratum or audit files, skip (handled above)
    if 'erratum' in path_str or 'audit' in path_str:
        return 'SUPERSEDED_BY_ERRATUM'
    # If the file also contains the corrected eigenvalues 11, 24, 15, flag as possibly aware
    if re.search(r'\b11\b.*\b24\b.*\b15\b', content) or re.search(r'spec.*11.*24.*15', content):
        return 'POSSIBLY_AWARE_NEEDS_REVIEW'
    # If the file has a proof or derivation keyword, flag for manual review
    if re.search(r'(proof|derive|construct|compute|verif)', content, re.IGNORECASE):
        return 'DERIVED_MANUAL_REVIEW'
    return 'COPY_INVALIDATED'


def scan_file(fpath: pathlib.Path) -> list:
    hits = []
    try:
        text = fpath.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        return [{'file': str(fpath.relative_to(REPO_ROOT)), 'error': str(e)}]
    for pattern, label in FALSE_PATTERNS:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            line_no = text[:m.start()].count('\n') + 1
            classification = classify_hit(text, str(fpath))
            hits.append({
                'file': str(fpath.relative_to(REPO_ROOT)),
                'pattern': label,
                'line': line_no,
                'snippet': text[max(0, m.start()-40):m.end()+40].replace('\n', ' '),
                'classification': classification,
            })
    return hits


def iter_source_files():
    """Yield corpus files without traversing Git objects or tool caches."""
    paths = [
        path
        for path in REPO_ROOT.iterdir()
        if path.is_file() and path.suffix.lower() in SUFFIXES
    ]
    scan_roots = [
        REPO_ROOT / name
        for name in sorted(ACTIVE_CORPUS_DIRS)
        if (REPO_ROOT / name).is_dir()
    ]
    for scan_root in scan_roots:
        for dirpath, dirnames, filenames in os.walk(scan_root):
            dirnames[:] = sorted(
                name
                for name in dirnames
                if name not in PRUNED_DIRS and not name.startswith('.')
            )
            base = pathlib.Path(dirpath)
            paths.extend(
                base / name
                for name in filenames
                if pathlib.Path(name).suffix.lower() in SUFFIXES
            )
    yield from sorted(paths)


def main():
    all_hits = []
    scanned = 0
    for fpath in iter_source_files():
        rel = str(fpath.relative_to(REPO_ROOT))
        if any(rel.startswith(e) or rel == e for e in EXCLUDE_PATHS):
            continue
        # Skip hidden dirs and .git
        parts = fpath.parts
        if any(p.startswith('.') for p in parts):
            continue
        hits = scan_file(fpath)
        all_hits.extend(hits)
        scanned += 1

    # Summarise
    by_class = {}
    for h in all_hits:
        c = h.get('classification', 'UNKNOWN')
        by_class.setdefault(c, []).append(h['file'])

    report = {
        'timestamp': datetime.utcnow().isoformat() + 'Z',
        'files_scanned': scanned,
        'total_hits': len(all_hits),
        'summary_by_classification': {k: len(v) for k, v in by_class.items()},
        'hits': all_hits,
    }

    out = REPO_ROOT / 'data' / 'QUARANTINE_2026_07_27_false_cubic_scan.json'
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=2))
    print(f'Scanned {scanned} files, found {len(all_hits)} hits.')
    print(f'Classifications: {report["summary_by_classification"]}')
    print(f'Report written to {out}')


if __name__ == '__main__':
    main()
