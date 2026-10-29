"""12402: is the twin obstruction universal?  For each of the 59 radius-safe, exotic-free candidates (12374/12375) and each SU(3) x SU(2)
pairing with three net doublets: (a) colour conditions alone (all states with |SU(3)| = 3) -- feasible?; (b) colour conditions plus
Y-neutral / vector-like hidden-charged states -- infeasible?  Mechanism = (a) feasible and (b) infeasible.  Also records whether the
other A2 x A1 pair carries net chiral (3,2)-type matter (a 'twin' sector)."""
import json, os, re, subprocess, sys, collections, itertools, math
vp = json.load(open('../search_drivers_12373/vet_pairs.json'))
def run(b, i3, i2, cond):
    env = dict(os.environ, YS_NSOQ=f'../search_drivers_12373/spec/{b}.nsoq', ONLY=cond)
    subprocess.run([sys.executable, 'ysearch.py', b, str(i3), str(i2), '1'], cwd='../search_drivers_12364', env=env, capture_output=True, text=True, timeout=3000)
    return len(json.load(open(f'../search_drivers_12364/ysearch_{b}_only.json'))['solutions']) > 0
out = {}
for b, pairs in vp.items():
    L = open(f'../search_drivers_12373/spec/{b}.nsoq', errors='ignore').read().split('\n')
    fac = [l.split()[2] for l in L if l.startswith('FACTOR')]
    c = collections.Counter()
    for l in L:
        m = re.match(r'FIELD \d+ m=19 k=\S+ mm=\S+ n=\S+ lat=\S+ dim=(\S*)', l)
        if m: c[tuple(int(re.match(r'-?\d+', x).group(0)) for x in m.group(1).split(','))] += 1
    res = []
    for pr in pairs:
        i3, i2 = pr['su3'], pr['su2']
        others3 = [j for j, f in enumerate(fac) if f == 'A2' and j != i3]; others2 = [j for j, f in enumerate(fac) if f == 'A1' and j != i2]
        twin = 0
        for j3, j2 in itertools.product(others3, others2):
            net = sum(n * (1 if d[j3] > 0 else -1) * math.prod(abs(x) for k, x in enumerate(d) if k not in (j3, j2)) for d, n in c.items() if abs(d[j3]) == 3 and abs(d[j2]) == 2)
            twin = max(twin, abs(net))
        a = run(b, i3, i2, "abs(key[0][I3])==3")
        bb = run(b, i3, i2, "abs(key[0][I3])==3 or any(abs(x)>1 for j,x in enumerate(key[0]) if j not in (I3,I2))")
        res.append(dict(su3=i3, su2=i2, colour_only_feasible=a, colour_plus_hidden_feasible=bb, twin_net_32=twin))
    out[b] = res
    print(b, res, flush=True)
json.dump(out, open('twin.json', 'w'), indent=1)
tab = collections.Counter((r['colour_only_feasible'], r['colour_plus_hidden_feasible'], r['twin_net_32']) for v in out.values() for r in v)
print('(colour-only, colour+hidden, twin net (3,2)):', dict(tab))
