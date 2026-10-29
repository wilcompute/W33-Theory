"""12363 certificate: winding-shifted constructing elements (theta^2 sub-orbifold of SM_2913_v6).  Controls: W5 = 0 -> winding changes
nothing (twisted sectors identical; 24 untwisted neutral states relabelled graviton/moduli -> gauge/scalar, a bookkeeping effect of the
translated untwisted element); W5 on, w = 2 -> identical to w = 0 (2 W5 in the lattice, W5^2 = 22 even).  Odd winding (w = -1, +-3, 5):
42 level-matched tachyons (m_R^2 = -1/6, Witten theta^2/theta^4), identical for every odd w; w = +1 trips an engine assertion
(groupTheory.cc findSimpleRoots) and is not used."""
import json, re, sys, collections
sys.path.insert(0, '../search_drivers_12359')
from cmp import states
RELABEL = {'8': '13', '9': '14', '17': '15', '18': '16'}
def relabel(c):
    out = collections.Counter()
    for k, v in c.items():
        out[(RELABEL.get(k[0], k[0]) if k[2] == '0' and k[1] == '0' else k[0],) + k[1:]] += v
    return out
tn = lambda p: int(re.search(r'T_NFIELDS (\d+)', open(p).read()).group(1)) if re.search(r'T_NFIELDS (\d+)', open(p).read()) else None
out = dict(T={f: tn(f + '.verbose') for f in ('sub2_w0', 'sub2_noW5_w0', 'sub2_w2', 'sub2_noW5_w1', 'sub2_wm1A', 'sub2_wm3A', 'sub2_w3A', 'sub2_w5A', 'sub2_w1A', 'sub2_noW5_wm1A', 'sub2_noW5_w5A')})
out['control_noW5_w1_equals_w0_up_to_relabel'] = relabel(states('sub2_noW5_w0.nsoq')) == relabel(states('sub2_noW5_w1.nsoq'))
out['control_W5_w2_equals_w0_up_to_relabel'] = relabel(states('sub2_w0.nsoq')) == relabel(states('sub2_w2.nsoq'))
odd = [open(f + '.verbose').read().split('T_NFIELDS')[0].split('\n') for f in ('sub2_wm1A', 'sub2_wm3A', 'sub2_w3A', 'sub2_w5A')]
lines = [sorted(l for l in o if l.startswith('T m')) for o in odd]
out['odd_winding_identical'] = all(x == lines[0] for x in lines); out['odd_winding_tachyons'] = lines[0]
print(json.dumps(out, indent=1)); json.dump(out, open('summary.json', 'w'), indent=1)
