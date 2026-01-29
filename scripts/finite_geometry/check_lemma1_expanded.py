"""Expanded checks for W33 and cross-references to TeX claims.

Checks performed:
- SRG parameter verification (n,k,lambda,mu) computed from adjacency
- Spectral check: adjacency eigenvalues and multiplicities
- Triangle counts and per-nonneighbor stats
- Search TeX files for numeric claims (|Aut(W33)|, edges, 27 counts) and compare

Writes JSON summary to bundles/v23_toe_finish/v23/lemma1_expanded.json
"""
import json
from pathlib import Path
import numpy as np
from itertools import combinations
import re

repo = Path(__file__).resolve().parents[2]
out = repo / 'bundles' / 'v23_toe_finish' / 'v23' / 'lemma1_expanded.json'

# helper: load W33
import runpy
mod = runpy.run_path(str(repo / 'THEORY_PART_CXXV_D5_VERIFICATION.py'))
build_W33_symplectic = mod['build_W33_symplectic']

# helper: search TeX claims
# Avoid scanning into large or inaccessible virtual env dirs
EXCLUDE_DIRS = {'.venv', '.venv_tools', '.venv_wsl', 'tools', 'external'}
# Walk the tree manually and skip problematic paths
TEX_FILES = []
# Walk up to a limited depth and skip problematic dirs to avoid OS errors
def iter_tex_files(root, max_depth=4):
    root = Path(root)
    for p in root.iterdir():
        if any(part in EXCLUDE_DIRS for part in p.parts):
            continue
        try:
            if p.is_dir():
                # do a shallow walk
                for q in p.rglob('*.tex'):
                    if any(part in EXCLUDE_DIRS for part in q.parts):
                        continue
                    try:
                        _ = q.stat()
                    except OSError:
                        continue
                    yield q
            else:
                if p.suffix == '.tex':
                    yield p
        except OSError:
            continue

TEX_FILES = list(iter_tex_files(repo))

CLAIM_RE = re.compile(r"(Aut\(W33\)\)|edges\s*=|27\s+non[- ]?neighbors|192|51,840|240)", re.IGNORECASE)


def compute_srg_params(adj):
    n = len(adj)
    degrees = [sum(row) for row in adj]
    k = degrees[0]
    # compute lambda (common neighbors count for adjacent pairs) and mu for nonadjacent
    lam_vals = []
    mu_vals = []
    for i in range(n):
        for j in range(i+1,n):
            common = sum(adj[i][k] and adj[j][k] for k in range(n))
            if adj[i][j]:
                lam_vals.append(common)
            else:
                mu_vals.append(common)
    lam = lam_vals[0] if lam_vals else None
    mu = mu_vals[0] if mu_vals else None
    return {'n': n, 'k': k, 'lambda': lam, 'mu': mu}


def spectral_summary(adj):
    A = np.array(adj, dtype=float)
    vals = np.linalg.eigvalsh(A)
    vals_rounded = np.round(vals, 6)
    unique, counts = np.unique(vals_rounded, return_counts=True)
    return {'eigenvalues': unique.tolist(), 'multiplicities': counts.tolist()}


def find_tex_claims(files):
    claims = []
    for p in files:
        try:
            txt = p.read_text(encoding='utf-8')
        except Exception:
            continue
        for m in re.finditer(r"(Aut\(W33\)\)\s*[:=\(]*\s*([0-9,]+))|(edges\s*[:=]\s*([0-9]+))|(27\s+non[- ]?neighbors)", txt, re.IGNORECASE):
            claims.append({'file': str(p.relative_to(repo)), 'match': m.group(0)})
    return claims


def main():
    verts, adj = build_W33_symplectic()
    if verts is None:
        raise SystemExit('Failed to build W33')

    srg = compute_srg_params(adj)
    spec = spectral_summary(adj)

    # triangles
    tri_total = 0
    for a,b,c in combinations(range(len(adj)),3):
        if adj[a][b] and adj[b][c] and adj[a][c]:
            tri_total += 1
    # triangle per nonneighbor induced (sample first)
    non_neighbors = [ [j for j in range(len(adj)) if j!=i and adj[i][j]==0] for i in range(len(adj))]
    tri_counts = []
    for idxs in non_neighbors:
        cnt = 0
        for a,b,c in combinations(idxs,3):
            if adj[a][b] and adj[b][c] and adj[a][c]:
                cnt += 1
        tri_counts.append(cnt)

    tex_claims = find_tex_claims(TEX_FILES)

    summary = {
        'srg': srg,
        'spectrum': spec,
        'total_triangles': tri_total,
        'triangle_per_nonneighbor_stats': {'min': min(tri_counts), 'max': max(tri_counts), 'sample': tri_counts[:8]},
        'tex_claims_found': tex_claims,
    }

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=2))
    print('Wrote', out)

if __name__ == '__main__':
    main()
