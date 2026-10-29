"""12366: combine large-R5 (12359b: 6D tachyons, Wilson lines off) with small-R5 (odd e5 winding) per parent."""
import json, os, re, collections
tn = lambda p: int(re.search(r'T_NFIELDS (\d+)', open(p).read()).group(1))
tf = [os.path.basename(x.replace(chr(92), '/')) for x in json.load(open('../search_drivers_12322/tachfree_parents.json'))['tachyon_free_parents']]
rows = {m: dict(large_e5e6=tn(f'../search_drivers_12359/c6d/{m}__t3.verbose'), small_e5=tn(f'ca/{m}__e5.verbose'),
                large_e3e4=tn(f'../search_drivers_12359/c6d/{m}__t2.verbose'), small_e3a=tn(f'ca/{m}__e3a.verbose'), small_e3b=tn(f'ca/{m}__e3b.verbose')) for m in tf}
tab = collections.Counter((r['large_e5e6'] > 0, r['small_e5'] > 0) for r in rows.values())
allr = [m for m, r in rows.items() if not any(r.values())]
print('(large tachyonic, small tachyonic):', dict(tab)); print('clean at all radii (necessary level):', len(allr), allr)
json.dump(dict(rows=rows, table={str(k): v for k, v in tab.items()}, all_radius_clean=allr), open('combine.json', 'w'), indent=1)
