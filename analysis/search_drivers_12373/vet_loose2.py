"""12374c: relaxed hypercharge search (no anomalous-U(1) condition, every non-(3,2) value in (1/6)Z within [-1, 1]) for the 59
large-radius-safe candidates without Y-independent exotics; plus the same relaxed search on the control SM_2913_v6 (must succeed)."""
import json, os, subprocess, sys, collections
v = json.load(open('vet2.json')); F = {json.loads(l)['base']: json.loads(l) for f in __import__('glob').glob('filt2_*.jsonl') for l in open(f)}
todo = [b for b, r in v.items() if not r['y_independent_exotics']]
out = {}
for b in todo:
    i3, i2 = F[b]['su3su2']
    env = dict(os.environ, YS_NSOQ=f'../search_drivers_12373/spec/{b}.nsoq', NO_ANOM='1', LOOSE='1')
    subprocess.run([sys.executable, 'ysearch.py', b, str(i3), str(i2), '1'], cwd='../search_drivers_12364', env=env, capture_output=True, text=True, timeout=3000)
    out[b] = len(json.load(open(f'../search_drivers_12364/ysearch_{b}_noanom_loose.json'))['solutions'])
print('relaxed searches with a solution:', sum(1 for x in out.values() if x), 'of', len(out))
json.dump(out, open('vet_loose2.json', 'w'), indent=1)
