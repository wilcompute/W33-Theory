"""(exit codes from the shell loop are not reliable: the verdict is read from the .sd content -- empty = load failure,
'noSM' = consistent but no Standard Model, otherwise the SM spectrum)
compare each Z2xZ6-I brother with its control (specdump: SM spectrum, field labels, sector k, multiplet, reps, charges)"""
import json, re, collections
def spec(p):
    full = collections.Counter(); inv = collections.Counter()
    for l in open(p):
        m = re.match(r'S (\S+?)_\d+ k=(\S+) susy=(\S+) dim=(\S*) q=(\S*)', l)
        if m:
            q = ','.join(f'{round(float(x), 6) + 0.0:.6f}' for x in m.group(5).split(',') if x)
            full[(m.group(1), m.group(2), m.group(3), m.group(4), q)] += 1
            inv[(m.group(1), m.group(2), m.group(3), m.group(4))] += 1
    return full, inv
def chiral(inv):
    # net count of SM quark doublets (label q minus bq) as a generation proxy
    return sum(v for k, v in inv.items() if k[0] == 'q') - sum(v for k, v in inv.items() if k[0] == 'bq')
idx = json.load(open('index.json'))
tab = collections.Counter(); rows = []
for e in idx:
    c = spec(e['files']['ctrl'][:-4] + '.sd')
    r = dict(model=e['model'], ctrl_fields=sum(c[1].values()), ctrl_netq=chiral(c[1]))
    for tag in ('even', 'odd'):
        if tag not in e['files']:
            continue
        txt = open(e['files'][tag][:-4] + '.sd').read().strip()
        if not txt:
            v = 'load failure (inconsistent)'; b = (collections.Counter(), collections.Counter())
        elif txt.startswith('noSM'):
            v = 'consistent, no Standard Model'; b = (collections.Counter(), collections.Counter())
        else:
            b = spec(e['files'][tag][:-4] + '.sd')
            v = 'identical' if b[0] == c[0] else ('SM, same reps, charges differ' if b[1] == c[1] else 'SM, different spectrum')
        r[tag] = dict(verdict=v, fields=sum(b[1].values()), netq=chiral(b[1]))
        tab[(tag, v)] += 1
    rows.append(r)
for k, v in sorted(tab.items()): print(k, v)
for r in rows[:6]: print(r)
json.dump(dict(table={str(k): v for k, v in tab.items()}, rows=rows), open('cmp.json', 'w'), indent=1)
