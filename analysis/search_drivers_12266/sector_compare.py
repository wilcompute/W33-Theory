"""12266: sector-resolved comparison of the two N = 0 engines on the 12254 models.  v2 = orbifolder-1.2.1 with the *_n0 patches, now
rebuilt with sector output (nsdump_sec: k, l); nso = non-SUSY orbifolder (nsodump: k, m = Witten power, n = Z3 power)."""
import re, collections, json, glob
out = {}
for sec in sorted(glob.glob('v2_*.sec')):
    lab = sec[3:-4]
    v = collections.Counter(); n = collections.Counter(); v10 = collections.Counter(); n10 = collections.Counter()
    for l in open(sec):
        m = re.match(r'F m=(\d+) k=(\d+) l=(\d+) dim=(\S+) x(\d+)', l)
        if m:
            key = 'Z3^' + m.group(3)
            v[key] += int(m.group(5))
            if '10' in m.group(4).split(',')[0]: v10[key] += int(m.group(5))
    nf = f'../search_drivers_12254/nsoout_{lab}.txt'
    try:
        for l in open(nf):
            m = re.match(r'F m=(\d+) k=(\d+) m=(\d+) n=(\d+) dim=(\S+) x(\d+)', l)
            if m:
                key = ('W ' if m.group(3) == '1' else '') + 'Z3^' + m.group(4)
                if m.group(1) in ('8', '9'):
                    key += ' gravity'
                n[key] += int(m.group(6))
                if '10' in m.group(5).split(',')[0]: n10[key] += int(m.group(6))
    except OSError:
        n = None
    warn = sum('local condition' in l for l in open(sec))
    out[lab] = dict(v2=v, nso=n, v2_tens=v10, nso_tens=n10, v2_local_condition_failures=warn)
    print(lab, dict(v), dict(n) if n else None, 'tens', dict(v10), dict(n10), 'warn', warn)
json.dump(out, open('sector_compare.json', 'w'), indent=1)
