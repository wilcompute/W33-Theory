"""12359 certificate: geometry validation (regenerated parent = shipped parent state for state; sub-orbifold fermions vector-like;
Wilson-line-on spectra are weight-level subsets of Wilson-line-off ones; a geometry with the fixed-torus translations deleted is rejected
by the engine) and the large-radius tachyon census over the 99 tachyon-free parents."""
import json, os, re, collections, sys
sys.argv = ['x']
from cmp import states
from subset import wl
out = {}
A, B = states('m2913v6_parent.nsoq'), states('m2913v6_sub1.nsoq'); C = states('../search_drivers_12302/bro/Z6II_23_SM_20260917_2913_v6__ctrl.nsoq')
out['regenerated_parent_identical'] = A == B and A == C; out['parent_states'] = sum(A.values())
out['vectorlike'] = json.load(open('vectorlike.json'))
for t, (on, off) in dict(e5e6=('m2913v6_sub2.nsoq', 'm2913v6_sub2_noW5.nsoq'), e3e4=('m2913v6_sub3.nsoq', 'm2913v6_sub3_noW34.nsoq')).items():
    a, b = wl(on), wl(off); out[f'subset_{t}'] = dict(on=sum(a.values()), off=sum(b.values()), violations=sum((a - b).values()), shifted=sum((b - a).values()))
out['bad_geometry_fields'] = sum(1 for l in open('m2913v6_sub2bad.nsoq', errors='ignore') if l.startswith('FIELD'))
tn = lambda p: int(re.search(r'T_NFIELDS (\d+)', open(p).read()).group(1))
out['verbose_T_NFIELDS'] = {t: tn(f'm2913v6_{t}.verbose') for t in ('sub1', 'sub2', 'sub2_noW5', 'sub3', 'sub3_noW34')}
tf = [os.path.basename(x.replace(chr(92), '/')) for x in json.load(open('../search_drivers_12322/tachfree_parents.json'))['tachyon_free_parents']]
cen = {}
for m in tf:
    r = dict(t3=tn(f'c6d/{m}__t3.verbose'), t2=tn(f'c6d/{m}__t2.verbose'))
    if os.path.exists(f'c6d/{m}__t3W.verbose'): r['t3_wilson_on'] = tn(f'c6d/{m}__t3W.verbose')
    cen[m] = r
out['census'] = cen
out['census_summary'] = dict(parents=len(cen), e5e6_tachyonic=sum(1 for r in cen.values() if r['t3'] > 0),
                             e5e6_all_shifted=all(r.get('t3_wilson_on', 0) == 0 for r in cen.values()),
                             e3e4_tachyonic=sum(1 for r in cen.values() if r['t2'] > 0),
                             three_generation_models={m: cen[m]['t3'] for m in cen if m.split('SM_20260917_')[1] in ('2618_v0', '2618_v1', '2618_v2', '2618_v3', '2913_v6', '2913_v7', '2913_v8')})
print(json.dumps({k: v for k, v in out.items() if k != 'census'}, indent=1))
json.dump(out, open('summary.json', 'w'), indent=1)
