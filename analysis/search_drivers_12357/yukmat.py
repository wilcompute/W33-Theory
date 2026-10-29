"""12357: full quark and lepton mass matrices of SM_2913_v6 with the vector-like states, for each choice of the light Higgs phi (Y = +1/2
orientation; up-type couples to phi*, down and lepton to phi -- one doublet suffices in a non-SUSY model).  Entry = minimal singlet
degree d (all 80 SM-singlet scalars allowed, s or s*) of the gauge- and space-group-allowed coupling; Yukawa entries ~ v eps^d,
vector-like entries ~ M_s eps^d.  Light masses: 3 smallest singular values (median over random O(1) complex coefficients), in units of v.
Rows/cols:  up    rows Q (6) + Ubar (3), cols Qbar (3) + U (6);  Q.U phi*, Ubar.Qbar phi, Q.Qbar and Ubar.U vector-like
            down  rows Q + Dbar, cols Qbar + D;  Q.D phi, Dbar.Qbar phi*
            lepton rows L (7) + Ebar (3), cols Lbar (4) + E (6);  L.E phi, Ebar.Lbar phi*"""
import sys, json, itertools, time
import numpy as np
sys.path.insert(0, '.')
from mono import FS, min_degree, typ, smsing
F19 = [f for f in FS if f['m'] == 19 and smsing(f)]
G = {}
for f in F19:
    t, c = typ(f)
    if t: G.setdefault((t, c), []).append(f)
Hs = [f for f in FS if f['m'] == 15 and smsing(f) and abs(f['d'][1]) == 2 and abs(f['d'][0]) == 1 and abs(f['y']) == sp_half] if False else None
import sympy as sp
Hs = []
for f in FS:
    if f['m'] == 15 and smsing(f) and abs(f['d'][0]) == 1 and abs(f['d'][1]) == 2 and abs(f['y']) == sp.Rational(1, 2):
        Hs.append((f, 1 if f['y'] > 0 else -1))      # phi = f (Y = +1/2) or f* (f has Y = -1/2)
SECT = dict(up=(('Q', False), ('U', True), ('Q', True), ('U', False), -1, +1),
            down=(('Q', False), ('D', True), ('Q', True), ('D', False), +1, -1),
            lepton=(('L', False), ('E', True), ('L', True), ('E', False), +1, -1))
def degmat(sec, phi):
    r1, r2, c1, c2, s_main, s_bar = SECT[sec]
    R = G[r1] + G[r2]; C = G[c1] + G[c2]; n1, m1 = len(G[r1]), len(G[c1])
    D = np.full((len(R), len(C)), -1); kind = np.zeros((len(R), len(C)), dtype=int)
    for i, a in enumerate(R):
        for j, b in enumerate(C):
            vl = (i < n1) == (j < m1)          # Q.Qbar or Ubar.U: vector-like; Q.U and Ubar.Qbar: Yukawa
            fixed = [(a, 1), (b, 1)]
            if not vl:
                f, sg = phi
                fixed.append((f, sg * (s_main if i < n1 else s_bar)))
            r = min_degree(fixed)
            D[i, j] = -1 if r is None else r[0]; kind[i, j] = 0 if vl else 1
    return D, kind
def light(D, kind, eps, Ms_over_v=1e15, draws=200, seed=1):
    rng = np.random.default_rng(seed); out = []
    for _ in range(draws):
        c = rng.uniform(0.5, 2, D.shape) * np.exp(2j * np.pi * rng.uniform(size=D.shape))
        M = np.where(D >= 0, c * eps ** np.maximum(D, 0), 0) * np.where(kind == 0, Ms_over_v, 1.0)
        sv = np.sort(np.linalg.svd(M, compute_uv=False))
        nl = M.shape[0] - min(M.shape) + 3 if M.shape[0] == M.shape[1] else 3
        out.append(sv[:3])
    return np.median(np.array(out), axis=0)
if __name__ == '__main__':
    t0 = time.time(); res = {}
    for hi, phi in enumerate(Hs):
        rec = {}
        for sec in ('up', 'down', 'lepton'):
            D, kind = degmat(sec, phi)
            rec[sec] = dict(D=D.tolist(), kind=kind.tolist(), light={str(e): [float(x) for x in light(D, kind, e)] for e in (0.1, 0.2, 0.3)})
        res[f"H{hi}_id{phi[0]['id']}_{'phi' if phi[1] > 0 else 'conj'}"] = rec
        print(hi, phi[0]['id'], {s: [round(np.log10(max(x, 1e-300)), 1) for x in rec[s]['light']['0.2']] for s in rec}, round(time.time() - t0), 's', flush=True)
    json.dump(res, open('yukmat.json', 'w'), indent=0)
