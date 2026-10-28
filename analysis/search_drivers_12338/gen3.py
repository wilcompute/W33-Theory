"""12338: a necessary three-generation condition without a hypercharge ansatz, for the 99 tachyon-free non-SUSY Z6-II parents (12324)
and their Scherk-Schwarz brothers: for every choice of an A2 factor (SU(3)) and an A1 factor (SU(2)_L), the net chiral multiplicity of
fermions transforming as (3 or 3bar, 2) (any other factors), n_L - n_R with conjugate representations folded.  Three is necessary for
three generations, not sufficient."""
import re, json, glob, os, collections, itertools
def load(p):
    L = open(p, errors='ignore').read().split('\n')
    fac = [l.split()[2] for l in L if l.startswith('FACTOR')]
    fs = []
    for l in L:
        m = re.match(r'FIELD \d+ m=(19|20) k=\S+ mm=\S+ n=\S+ lat=\S+ dim=(\S*) ', l)
        if m:
            d = [int(re.match(r'-?\d+', x).group(0)) for x in m.group(2).split(',')] if m.group(2) else []
            fs.append((m.group(1) == '19', d))
    return fac, fs
def best(p):
    fac, fs = load(p)
    a2 = [i for i, f in enumerate(fac) if f == 'A2']; a1 = [i for i, f in enumerate(fac) if f == 'A1']
    vals = []
    for i3, i2 in itertools.product(a2, a1):
        n = 0
        for L, d in fs:
            if abs(d[i3]) == 3 and abs(d[i2]) == 2:
                n += (1 if L else -1) * (1 if d[i3] > 0 else -1)
        vals.append(abs(n) // 2)      # each Weyl fermion is listed with its CPT conjugate
    return max(vals) if vals else None, vals
tf = [os.path.basename(x.replace(chr(92), '/')) for x in json.load(open('../search_drivers_12322/tachfree_parents.json'))['tachyon_free_parents']]
tab = collections.Counter(); hits = []
for m in tf:
    D = '../search_drivers_12281/bro/' if os.path.exists(f'../search_drivers_12281/bro/{m}__ctrl.nsoq') else '../search_drivers_12302/bro/'
    for tag in ('ctrl', 'w6odd'):
        b, vals = best(D + f'{m}__{tag}.nsoq')
        tab[(tag, b)] += 1
        if b == 3:
            hits.append(f'{m}__{tag}')
for k, v in sorted(tab.items(), key=str): print(v, k)
print('three-doublet hits:', hits[:20], len(hits))
json.dump(dict(table={str(k): v for k, v in tab.items()}, hits=hits), open('gen3.json', 'w'), indent=1)
