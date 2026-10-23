"""12259: the full Ploger-Ramos-Sanchez-Ratz-Vaudrevange consistency conditions (hep-th/0702176, eqs. (7a)-(7f), derived in their
appendix A from Phi_vac(g, h)^gcd(n, s) = 1, i.e. well-defined projection phases) for Z_2^W x Z_3 models with Wilson lines:
  M (V_i^2 - v_i^2) = 0 mod 2,  N_a (A_a . V_i) = 0 mod 2,  N_a A_a^2 = 0 mod 2,  gcd(N_a, N_b) (A_a . A_b) = 0 mod 2 (a != b),
shifts V0 (order 2, twist s0 with s0^2 = 3 for (0,1,1,1)... the mixed condition (7c) M(V1.V2 - v1.v2) with the Witten element is checked as
V0.V1 = 0 mod 1 on the gauge side), Wilson lines of order 3 on the three tori (W_{2a-1} = W_{2a} counted once per torus pair).
Reports, per model, which conditions fail."""
import glob, json, os, re, itertools
from fractions import Fraction as F
dot = lambda a, b: sum(x * y for x, y in zip(a, b))


def rows(t):
    return [[F(x.strip(',')) for x in r.replace(',', ' ').split()] for r in t.split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')]


def check(rs, wl=range(3, 9), shifts=(0, 1)):
    fails = []
    W = [(i, rs[i]) for i in wl if any(rs[i])]
    for i, a in W:
        if (3 * dot(a, a)) % 2:
            fails.append(f'7e W{i}')
        for s in shifts:
            v = 3 * dot(a, rs[s])
            if v.denominator != 1 or v % 2:
                fails.append(f'7d W{i}.V{s}')
    for (i, a), (j, b) in itertools.combinations(W, 2):
        if (i - 3) // 2 == (j - 3) // 2:
            continue
        v = 3 * dot(a, b)
        if v.denominator != 1 or v % 2:
            fails.append(f'7f W{i}.W{j}')
    return sorted(set(f.split()[0] for f in fails)), fails


sets = {
    'twisted10_C10_loaded': [r'C:\tmp\toe_round\stype\cand10\C10_%s_%d_%d.txt' % (x['base'], x['j'], x['k'])
                             for x in json.load(open('../search_drivers_12217/cand10_results.json')) if x['gauge'] != 'LOADFAIL'],
    'A8_SMs': sorted(glob.glob(r'C:\tmp\toe_round\stype\a8all\m*.txt')),
    'three_generation_bases_12111': sorted(glob.glob(r'C:\tmp\toe_wt\analysis\search_drivers_12111\*_9.txt')),
    'flipscan2_SU5_models': sorted(p for p in glob.glob(r'C:\tmp\toe_round\stype\flipscan2\*.txt')
                                   if os.path.exists(p[:-4] + '.out') and 'A4' in (re.search(r'GAUGE (.*)', open(p[:-4] + '.out').read()) or [None, ''])[1]),
}
out = {}
for name, files in sets.items():
    res = {}
    for f in files:
        kinds, det = check(rows(open(f).read()))
        res[os.path.basename(f)] = kinds
    from collections import Counter
    c = Counter(tuple(v) for v in res.values())
    out[name] = dict(models=len(res), fully_consistent=sum(1 for v in res.values() if not v), failure_patterns={str(k): n for k, n in c.items()})
    print(name, out[name])
json.dump(out, open('ploger.json', 'w'), indent=1)
json.dump({n: {os.path.basename(f): check(rows(open(f).read()))[0] for f in fs} for n, fs in sets.items()}, open('ploger_per_model.json', 'w'), indent=1)
