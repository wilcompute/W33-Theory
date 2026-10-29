"""12451b: re-run the exact all-orders lifting for all 52 SM_2541 models WITH Majorana self-pairing of real-representation, Y = 0 fermions."""
import json, os, subprocess, sys, collections
D = os.path.dirname(os.path.abspath(__file__))
F = {json.loads(l)['base']: json.loads(l) for f in __import__('glob').glob(os.path.join(D, 'filt3_*.jsonl')) for l in open(f)}
vs = json.load(open(os.path.join(D, 'vet_sm2541.json')))
out = {}
for b in sorted(vs):
    t = json.load(open(os.path.join(D, '..', 'search_drivers_12364', f'ysearch_{b}_noanom_loose.json')))['solutions'][0]['t']
    su3, su2 = F[b]['su3su2']
    env = dict(os.environ, MONO_MODEL=b, MONO_PATH=os.path.join(D, 'spec', f'{b}.nsoq'), MONO_Y=json.dumps(t), MONO_I3=str(su3), MONO_I2=str(su2), LIFT_MAJORANA='1')
    subprocess.run([sys.executable, 'lift_exact.py'], cwd=os.path.join(D, '..', 'search_drivers_12357'), env=env, capture_output=True, text=True, timeout=3000)
    le = json.load(open(os.path.join(D, '..', 'search_drivers_12357', f'lift_exact_{b}_maj.json')))
    out[b] = dict(kY=vs[b]['kY'], fractional=le['fractional'], dirac=le['liftable_all_orders_upper'], with_majorana=le['liftable_with_majorana'])
    print(b, out[b], flush=True)
json.dump(out, open(os.path.join(D, 'vet_maj.json'), 'w'), indent=1)
print('all fractional liftable with Majorana:', sum(1 for r in out.values() if r['with_majorana'] == r['fractional']), 'of', len(out))
