"""12357b: the mass matrices of 12357 restricted to the 6-singlet set of 12360 (only those singlets in monomials).  Entries without any
allowed monomial vanish exactly at this order.  Reports, per Higgs choice, the number of nonzero light masses (generic rank of the
light sector after the vector-like states decouple) and their log10 sizes (units of v, median over coefficient draws)."""
import sys, json
import numpy as np
sys.path.insert(0, '.')
import mono
import yukmat as Y
vac = json.load(open('vacuum.json'))['vacuum']
allowed = [s in vac for s in range(mono.NS)]
orig = mono.min_degree
Y.min_degree = lambda fixed: orig(fixed, allowed)
res = {}
for hi, phi in enumerate(Y.Hs):
    rec = {}
    for sec in ('up', 'down', 'lepton'):
        D, kind = Y.degmat(sec, phi)
        L = {str(e): [float(x) for x in Y.light(D, kind, e)] for e in (0.1, 0.2, 0.3)}
        rec[sec] = dict(D=D.tolist(), kind=kind.tolist(), light=L, n_light_nonzero=int(sum(1 for x in L['0.2'] if x > 1e-12)))
    tag = f"H{hi}_id{phi[0]['id']}_{'phi' if phi[1] > 0 else 'conj'}"; res[tag] = rec
    print(tag, {s: (rec[s]['n_light_nonzero'], [round(np.log10(max(x, 1e-300)), 1) for x in rec[s]['light']['0.2']]) for s in rec}, flush=True)
json.dump(res, open('yuk6.json', 'w'), indent=0)
