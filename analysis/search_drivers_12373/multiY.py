"""12444b: is the unliftable (1,2,0) pair hypercharge-dependent?  For a model, enumerate up to NSOL distinct relaxed hypercharges (no-good
cuts in ysearch.py), keep the anomaly-free ones, and run the exact lifting test with each.  Usage: py -3 multiY.py MODEL NSOL"""
import json, os, subprocess, sys
D = os.path.dirname(os.path.abspath(__file__))
b, nsol = sys.argv[1], sys.argv[2]
F = {json.loads(l)['base']: json.loads(l) for f in __import__('glob').glob(os.path.join(D, 'filt3_*.jsonl')) for l in open(f)}
su3, su2 = F[b]['su3su2']
env = dict(os.environ, YS_NSOQ=os.path.join(D, 'spec', f'{b}.nsoq'), LOOSE='1', NO_ANOM='1')
subprocess.run([sys.executable, 'ysearch.py', b, str(su3), str(su2), nsol], cwd=os.path.join(D, '..', 'search_drivers_12364'), env=env, capture_output=True, text=True, timeout=7200)
sols = json.load(open(os.path.join(D, '..', 'search_drivers_12364', f'ysearch_{b}_noanom_loose.json')))['solutions']
out = []
for k, s in enumerate(sols):
    env2 = dict(os.environ, MONO_MODEL=b, MONO_PATH=os.path.join(D, 'spec', f'{b}.nsoq'), MONO_Y=json.dumps(s['t']), MONO_I3=str(su3), MONO_I2=str(su2))
    subprocess.run([sys.executable, 'lift_exact.py'], cwd=os.path.join(D, '..', 'search_drivers_12357'), env=env2, capture_output=True, text=True, timeout=3000)
    le = json.load(open(os.path.join(D, '..', 'search_drivers_12357', f'lift_exact_{b}.json')))
    out.append(dict(kY=s['kY'], t=s['t'], fractional=le['fractional'], liftable=le['liftable_all_orders_upper'], unmatched=le['unmatched_types']))
    print(k, out[-1]['kY'], out[-1]['fractional'], out[-1]['liftable'], out[-1]['unmatched'], flush=True)
json.dump(out, open(os.path.join(D, f'multiY_{b}.json'), 'w'), indent=1)
