"""12430-12432 certificate: Witten-shift search over the 65 other SUSY Z6-II W(3,3) parents with W6 = 0 (240 sampled shifts each),
radius filters, Y-independent exotics, hypercharge over all SU(3) x SU(2) pairings, and the obstruction diagnosis (search_drivers_12402/
twin2.py: colour-only vs colour + hidden)."""
import json, glob, collections
R = [json.loads(l) for f in glob.glob('scan2_*.jsonl') for l in open(f)]
S = [r for r in R if r.get('strict') == '1']
C = [r for r in S if r.get('T') == 0 and r.get('best32') == 3]
F = [json.loads(l) for f in glob.glob('filt2_*.jsonl') for l in open(f)]
cls = collections.Counter(('large-clean' if r['t3'] + r['t2'] == 0 else 'large-T', 'small-clean' if r['e5'] + r['e3a'] + r['e3b'] == 0 else 'small-T') for r in F)
v = json.load(open('vet2.json')); vp = json.load(open('vet_pairs2.json')); tw = json.load(open('../search_drivers_12402/twin2.json'))
rows = [x for xs in tw.values() for x in xs]
out = dict(parents=len({r['parent'] for r in R}), sampled=len(R), strict=len(S), tachyon_free=sum(1 for r in S if r.get('T') == 0),
           three_doublet=len(C), three_doublet_parents=len({r['parent'] for r in C}),
           hidden_groups=dict(collections.Counter(r['gauge'] for r in C).most_common(8)),
           radius_classes={f'{a},{b}': n for (a, b), n in cls.items()}, large_safe=len(v),
           y_independent_exotics=sum(1 for r in v.values() if r['y_independent_exotics']),
           exotic_free=sum(1 for r in v.values() if not r['y_independent_exotics']),
           exotic_free_all_radius=sum(1 for r in v.values() if r['all_radius'] and not r['y_independent_exotics']),
           pairings=sum(len(x) for x in vp.values()), pairing_hypercharge_found=sum(1 for x in vp.values() if any(y['hypercharges'] for y in x)),
           colour_only_feasible=sum(r['colour_only_feasible'] for r in rows), twin_present=sum(1 for r in rows if r['twin_net_32'] > 0))
print(json.dumps(out, indent=1)); json.dump(out, open('newparents_summary.json', 'w'), indent=1)
