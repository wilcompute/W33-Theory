"""12295b: cubic Yukawas of the three Z2xZ6-I lineages without renormalisable QLd (SM_128_23, SM_808_24, SM_2579_27; brother and
parent).  Requests: up q bu bl (bl = Y +1/2 doublet, H_u-type), down q bd l (H_d-type), lepton l be l; engine gauge + space group,
then the R rule (validated in rcontrol.py).  Reported per model: allowed couplings, and the rank structure as (q rows reachable)."""
import sys, os, json, itertools, re, collections
sys.path.insert(0, '../search_drivers_12287')
import vet
os.chdir('../search_drivers_12287')
keep = ('SM_20260926_128_23', 'SM_20260926_808_24', 'SM_20260926_2579_27')
rep = {}
for lab, path in vet.models:
    if not lab.startswith(keep):
        continue
    F = vet.fields(lab + '_p1')
    g = lambda pre: [n for n in F if re.match(pre + r'_\d+$', n)]
    q, bu, bd, l, bl, be = g('q'), g('bu'), g('bd'), g('l'), g('bl'), g('be')
    req = [' '.join(x) for x in itertools.product(q, bu, bl)] + [' '.join(x) for x in itertools.product(q, bd, l)] + \
          [' '.join(x) for x in itertools.product(l, be, l)]
    vet.run(path, '\n'.join(req) + '\n', lab + '_yuk')
    allowed = collections.Counter(); qrows = collections.defaultdict(set); top = []
    for line in open(lab + '_yuk.out', errors='ignore'):
        if line.startswith('CHECK'):
            p = line.split(); names = p[2:]
            if int(p[1]) > 0 and all(n in F for n in names) and vet.rok(names, F):
                kind = 'up' if names[1].startswith('bu') else ('down' if names[1].startswith('bd') else 'lepton')
                allowed[kind] += 1
                if kind in ('up', 'down'):
                    qrows[kind].add(names[0])
    rep[lab] = dict(n_fields={k: len(v) for k, v in dict(q=q, bu=bu, bd=bd, l=l, bl=bl, be=be).items()}, allowed=dict(allowed),
                    q_rows={k: sorted(v) for k, v in qrows.items()})
    print(lab, rep[lab])
os.chdir('../search_drivers_12295')
json.dump(rep, open('yuk.json', 'w'), indent=1)
