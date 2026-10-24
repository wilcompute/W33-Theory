"""12265: cross-tabulate the Python Ploger audit against the stock (lenient) and patched (strict) non-SUSY engines."""
import collections, json, os
exec(open('audit_all.py').read().split("files = [l.strip()")[0])
eng = {}
for l in open('z3_engine_out.txt'):
    p = l.split()
    eng[p[0].split('search_drivers_12265/')[1]] = (p[1] if len(p) > 1 else '?', p[2] if len(p) > 2 else '?')
rows = [l.split('\t') for l in open('split_index.tsv').read().split('\n')]
tab = collections.Counter(); ex = collections.defaultdict(list); perdir = collections.defaultdict(collections.Counter)
for name, src, geo in rows:
    if name not in eng:
        continue
    t = open(name).read()
    try:
        rr = [[F(x) for x in r.split()] for r in t.split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n') if r.strip()]
        fl = '+'.join(check_block(rr)) or 'ok'
    except Exception:
        fl = 'parse'
    k = f'lenient={eng[name][0]} strict={eng[name][1]} audit={fl}'
    tab[k] += 1; ex[k].append(name)
    d = os.path.dirname(src).replace(chr(92), '/').split('/analysis/')[-1]
    perdir[d][f'L{eng[name][0]}S{eng[name][1]}']+= 1
for k, v in sorted(tab.items(), key=lambda x: -x[1]):
    print(v, k, ex[k][0])
print()
for d, c in sorted(perdir.items()):
    if c['L1S0']:
        print(d, dict(c))
json.dump(dict(table=tab, perdir=perdir, examples={k: v[:5] for k, v in ex.items()}), open('engine_vs_audit.json', 'w'), indent=1)
