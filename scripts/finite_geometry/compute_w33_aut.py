"""Compute automorphism group of W33 using nauty/dreadnaut (available in Sage env).

Outputs JSON summary to bundles/v23_toe_finish/v23/w33_aut_summary.json
"""
import json
from pathlib import Path
import subprocess
import sys

repo = Path(__file__).resolve().parents[2]
out = repo / 'bundles' / 'v23_toe_finish' / 'v23' / 'w33_aut_summary.json'

# Build W33 adjacency using existing script (import via runpy to avoid module path issues)
import runpy
mod = runpy.run_path(str(repo / 'THEORY_PART_CXXV_D5_VERIFICATION.py'))
build_W33_symplectic = mod['build_W33_symplectic']

verts, adj = build_W33_symplectic()
if verts is None:
    raise SystemExit('Failed to build W33')

n = len(adj)
# write dreadnaut input
d_in = []
d_in.append(f"n={n}")
d_in.append('g')
for i, row in enumerate(adj):
    nbrs = [str(j) for j, e in enumerate(row) if e]
    line = f"{i}: " + (" ".join(nbrs) + " ;")
    d_in.append(line)
# termination with 'x'
d_in.append('x')

d_in_text = "\n".join(d_in) + "\n"
stdin_path = repo / 'bundles' / 'v23_toe_finish' / 'v23' / 'w33_dreadnaut_input.txt'
stdin_path.write_text(d_in_text)

# determine dreadnaut path candidates
candidates = [
    '/home/wiljd/.local/share/mamba/envs/sage/bin/dreadnaut',
    '/home/wiljd/micromamba/envs/sage/bin/dreadnaut',
    '/usr/bin/dreadnaut',
    'dreadnaut'
]

# run dreadnaut via WSL using the first candidate that exists
import shlex
import os

def wsl_cmd(cmd):
    return ['wsl', 'bash', '-lc', cmd]

result_text = None
for c in candidates:
    # check existence in WSL
    check = subprocess.run(wsl_cmd(f"test -x {shlex.quote(c)} && echo exists || echo missing"), capture_output=True, text=True)
    if 'exists' in check.stdout:
        # run dreadnaut with input redirected
        cmd = f"printf {shlex.quote(d_in_text)} | {shlex.quote(c)}"
        run = subprocess.run(wsl_cmd(cmd), capture_output=True, text=True)
        result_text = run.stdout + '\n' + run.stderr
        break

if result_text is None:
    raise SystemExit('No dreadnaut found in expected locations; install nauty/dreadnaut in WSL Sage env')

# parse group size and orbits
import re
m = re.search(r'grpsize\s*=\s*([0-9]+)', result_text)
if not m:
    m = re.search(r'grpsize=\s*([0-9]+)', result_text)

size = int(m.group(1)) if m else None
orbits = []
for line in result_text.splitlines():
    if 'orbit' in line.lower() and ':' in line:
        orbits.append(line.strip())

summary = {
    'grpsize': size,
    'raw_output': result_text,
    'orbits_snippets': orbits[:20]
}

out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(summary, indent=2))
print('Wrote', out)
