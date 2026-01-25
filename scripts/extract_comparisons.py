import json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
out = ROOT / 'NUMERIC_COMPARISONS.json'
res = []
for jf in sorted(ROOT.glob('PART_*.json')):
    try:
        data = json.load(open(jf))
    except Exception:
        continue
    # search for specific known structures
    # 1) desi_dark_energy
    kr = data.get('key_results') or {}
    if isinstance(kr, dict) and 'desi_dark_energy' in kr:
        dd = kr['desi_dark_energy']
        m = dd.get('w0_measured')
        p = dd.get('w0_w33_predicted') or dd.get('w0_w33')
        if m is not None and p is not None:
            try:
                m = float(m)
                p = float(p)
                res.append({'file': jf.name, 'name': 'DESI w0', 'measured': m, 'predicted': p, 'diff': p-m, 'pct': (abs(p-m)/abs(m))*100 if m!=0 else None})
            except Exception:
                pass
    # generic scan for measured/predicted (extended keyword matching)
    def scan(d, prefix=''):
        if not isinstance(d, dict):
            return
        # collect numeric fields in this dict
        num_fields = {k: v for k, v in d.items() if isinstance(v, (int, float)) or (isinstance(v, str) and is_number(v))}
        # classify by keyword
        for mk, mv in num_fields.items():
            kl = mk.lower()
            if any(k in kl for k in ['meas', 'observ', 'experimental', 'measured']):
                # look for predicted fields near here
                for pk, pv in num_fields.items():
                    if pk == mk:
                        continue
                    pl = pk.lower()
                    if any(k in pl for k in ['pred', 'w33', 'predicted', 'value', 'expected']) or any(k in pl for k in ['alpha', 'sin', 'w0', 'm_', 'mass', 'omega', 'h0']):
                        try:
                            m = float(mv)
                            p = float(pv)
                            res.append({'file': jf.name, 'measured_key': mk, 'predicted_key': pk, 'measured': m, 'predicted': p, 'diff': p-m, 'pct': (abs(p-m)/abs(m))*100 if m!=0 else None})
                        except Exception:
                            continue
        # recurse
        for k, v in d.items():
            if isinstance(v, dict):
                scan(v, prefix + k + '.')

    # helper to recognize numeric strings
    def is_number(s):
        try:
            float(s)
            return True
        except Exception:
            return False

    scan(data)

with open(out,'w') as f:
    json.dump(res, f, indent=2, default=int)
print('Wrote', out, 'entries:', len(res))
