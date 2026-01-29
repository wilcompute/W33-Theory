"""Lemma 2 checks: Use Sage (via WSL) to verify automorphism group properties and isomorphism to Sp(4,3).
Writes JSON summary to bundles/v23_toe_finish/v23/lemma2_check.json
"""
import json
from pathlib import Path
import subprocess
import shlex
import runpy

repo = Path(__file__).resolve().parents[2]
out = repo / 'bundles' / 'v23_toe_finish' / 'v23' / 'lemma2_check.json'

# build W33 adjacency
mod = runpy.run_path(str(repo / 'THEORY_PART_CXXV_D5_VERIFICATION.py'))
build_W33_symplectic = mod['build_W33_symplectic']
# suppress unicode-printing issues on Windows consoles by silencing stdout during build
import sys, os, io
old_stdout = sys.stdout
try:
    # open devnull with utf-8 to avoid encoding errors
    sys.stdout = io.TextIOWrapper(open(os.devnull, 'wb'), encoding='utf-8')
    verts, adj = build_W33_symplectic()
finally:
    try:
        sys.stdout.detach()
    except Exception:
        pass
    sys.stdout = old_stdout
if verts is None:
    raise SystemExit('failed to build W33')

n = len(adj)
# build a small sage script to run in WSL
sage_script = []
sage_script.append('from sage.graphs.graph import Graph')
sage_script.append('A = []')
for i,row in enumerate(adj):
    nbrs = [str(j) for j,e in enumerate(row) if e]
    sage_script.append(f"A.append(({i}, [{','.join(nbrs)}]))")
sage_script.append('G = Graph(dict(A))')
sage_script.append('Aut = G.automorphism_group()')
sage_script.append('order = Aut.order()')
sage_script.insert(0, 'from sage.groups.matrix_gps.symplectic import SymplecticGroup')
sage_script.append('Sp = SymplecticGroup(4,3)')
sage_script.append('sp_order = Sp.order()')
sage_script.append('iso = Aut.is_isomorphic(Sp)')
sage_script.append('orbits = Aut.orbits()')
sage_script.append('print(order)')
sage_script.append('print(sp_order)')
sage_script.append('print(iso)')
sage_script.append('print(orbits)')

sage_code = '\n'.join(sage_script)
# write to temporary file
tmp = repo / 'tmp_w33_lemma2.sage'
tmp.write_text(sage_code)
# map Windows path to WSL path (C: -> /mnt/c)
wsl_tmp = tmp.as_posix().replace('C:', '/mnt/c')
# write sage script into WSL /tmp via a heredoc then execute it
heredoc_cmd = "cat > /tmp/tmp_w33_lemma2.sage << 'EOF'\n" + sage_code + "\nEOF"
proc1 = subprocess.run(['wsl', 'bash', '-lc', heredoc_cmd], capture_output=True, text=True)
# now run it using sage inside WSL
cmd = "/home/wiljd/.local/share/mamba/envs/sage/bin/sage -c \"exec(open('/tmp/tmp_w33_lemma2.sage').read())\""
proc2 = subprocess.run(['wsl', 'bash', '-lc', cmd], capture_output=True, text=True)
out_text = proc1.stdout + proc1.stderr + '\n' + proc2.stdout + proc2.stderr
# parse
lines = [ln.strip() for ln in out_text.splitlines() if ln.strip()]
summary = {'raw_output': out_text, 'parsed': {}}
# attempt to parse simple ints if available
if lines:
    try:
        summary['parsed']['aut_order'] = int(lines[0])
    except Exception:
        pass
    try:
        summary['parsed']['orbits_snippet'] = lines[1:6]
    except Exception:
        pass

# supplement with dreadnaut/aut summary (if available)
w33_file = repo / 'bundles' / 'v23_toe_finish' / 'v23' / 'w33_aut_summary.json'
if w33_file.exists():
    w33 = json.load(open(w33_file))
    if 'grpsize' in w33:
        summary['parsed']['aut_order_w33'] = w33['grpsize']
        summary['parsed']['order_matches_51840'] = (w33['grpsize']==51840)

out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(summary, indent=2))
print('Wrote', out)
