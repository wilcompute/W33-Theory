"""12373-12375 certificate: targeted Witten-shift search (15000 sampled V0 of 111108 admissible over the five SUSY parents), radius
filters, Y-independent exotics, hypercharge searches (base; all SU(3) x SU(2) pairings; relaxed -- coverage recorded at summary time)."""
import json, glob, os, collections
R = [json.loads(l) for f in glob.glob('scan_*.jsonl') for l in open(f)]
S = [r for r in R if r.get('strict') == '1']
C = [r for r in S if r.get('T') == 0 and r.get('best32') == 3]
F = [json.loads(l) for f in glob.glob('filt_*.jsonl') for l in open(f)]
cls = collections.Counter(('large-clean' if r['t3'] + r['t2'] == 0 else 'large-T', 'small-clean' if r['e5'] + r['e3a'] + r['e3b'] == 0 else 'small-T') for r in F)
v = json.load(open('vet.json')); vp = json.load(open('vet_pairs.json'))
todo = [b for b, r in v.items() if not r['y_independent_exotics']]
rel = {b: len(json.load(open(f'../search_drivers_12364/ysearch_{b}_noanom_loose.json'))['solutions']) for b in todo
       if os.path.exists(f'../search_drivers_12364/ysearch_{b}_noanom_loose.json')}
out = dict(sampled=len(R), strict=len(S), tachyon_free=sum(1 for r in S if r.get('T') == 0), three_doublet=len(C),
           three_doublet_by_parent=dict(collections.Counter(r['parent'].split('SM_20260917_')[1] for r in C)),
           radius_classes={f'{a},{b}': n for (a, b), n in cls.items()}, large_safe=len(v),
           y_independent_exotics=sum(1 for r in v.values() if r['y_independent_exotics']),
           all_radius_exotic_free=sum(1 for r in v.values() if r['all_radius'] and not r['y_independent_exotics']),
           base_hypercharge_found=sum(1 for r in v.values() if r.get('hypercharges')),
           pairings_tested=sum(len(x) for x in vp.values()), pairing_hypercharge_found=sum(1 for x in vp.values() if any(y['hypercharges'] for y in x)),
           relaxed_done=len(rel), relaxed_of=len(todo), relaxed_found=sum(1 for x in rel.values() if x))
print(json.dumps(out, indent=1)); json.dump(out, open('summary.json', 'w'), indent=1)
