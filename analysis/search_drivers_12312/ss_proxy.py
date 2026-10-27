"""12312: Scherk-Schwarz potential proxy for the left-right candidate.  At large radius a Scherk-Schwarz compactification has
V(R) ~ xi (n_F - n_B) / R^4 (xi > 0; Itoyama-Taylor form), n_F/n_B = massless fermionic/bosonic degrees of freedom of the
Scherk-Schwarz model (component counts as in 12280, same convention for every model).  n_F > n_B: V > 0 falling with R, the radius
runs outwards (away from the tachyonic region R < 1.63 sqrt(alpha')); n_F < n_B: inwards.  A proxy only: the potential is not computed."""
import sys, json
sys.path.insert(0, '../search_drivers_12277')
from bf_count import count
out = {}
for v in ('v9', 'v4'):
    for tag in ('w6odd', 'ctrl'):
        c = count(f'../search_drivers_12281/bro/Z6II_60_SM_20260917_810_{v}__{tag}.nsoq')
        bos = c['gauge'] + c['scalar'] + c['moduli'] + c['gravity']
        out[f'{v}_{tag}'] = dict(components=dict(c), n_F=c['fermion'], n_B=bos, nF_minus_nB=c['fermion'] - bos)
        print(v, tag, out[f'{v}_{tag}'])
json.dump(out, open('ss_proxy.json', 'w'), indent=1)
