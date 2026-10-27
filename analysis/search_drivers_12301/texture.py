"""12301: minimal singlet degree of every Yukawa entry of SM_808_24 and SM_2579_27 (Z2xZ6-I, brothers; parents give the same cubic data).
Singlets: the 'n' fields (SM and hidden singlets).  Exact MILP (scipy): x_s >= 0 integers (holomorphic: no conjugates), U(1) charges
cancel exactly; R rule: sum (q_sh + osc)^a = -1 mod N_a,
N = (2, 6, 6).  The space-group rule (sector powers and translations) is NOT imposed -> degrees are lower bounds; cubic (degree 0)
entries were confirmed with the full engine rules in 12295.  Higgs choice: every bl (H_u-type) and l (H_d-type) field is tried; for
each entry the minimum over Higgs fields is reported, and the best single Higgs pair (minimal summed degrees) is also given."""
import re, sys, json, itertools
import numpy as np
from fractions import Fraction as Fr
from scipy.optimize import milp, LinearConstraint, Bounds
N = (2, 6, 6)
def fields(p):
    F = {}
    for l in open(p, errors='ignore'):
        if l.startswith('F '):
            t = l.split(); name = t[1]
            i = t.index('idx'); dd = t.index('dims'); u = t.index('u1'); k = t.index('qsh'); m = t.index('osc'); g = t.index('gam')
            F[name] = dict(idx=[int(x) for x in t[i + 1:dd]], dims=t[dd + 1:u], u1=[Fr(x).limit_denominator(36) for x in t[u + 1:k]],
                           R=[Fr(a).limit_denominator(12) + Fr(b).limit_denominator(12) for a, b in zip(t[k + 1:m], t[m + 1:g])])
    return F
def min_degree(F, names, S, cap=12):
    nu = len(F[names[0]]['u1'])
    tot_u = [sum(F[n]['u1'][j] for n in names) for j in range(nu)]
    tot_k = sum(F[n]['idx'][1] for n in names); tot_l = sum(F[n]['idx'][2] for n in names)
    tot_R = [sum(F[n]['R'][a] for n in names) for a in range(1, 4)]
    ns = len(S); den = 36
    # variables: x_s (ns), slack z_k, z_l, z_R1..3
    nv = ns + 5
    A, lo, hi = [], [], []
    for j in range(nu):
        row = [int(F[s]['u1'][j] * den) for s in S] + [0] * 5
        A.append(row); v = int(-tot_u[j] * den); lo.append(v); hi.append(v)
    # (sector rule dropped: the probe's idx is an internal sector/plane enumeration, not the (k, l) powers -- a first version used it
    #  and failed the positive control; the two slack variables stay unused)
    for a in range(3):
        rr = [F[s]['R'][a + 1] * 12 for s in S]
        A.append([int(x) for x in rr] + [0, 0] + [(-N[a] * 12 if b == a else 0) for b in range(3)])
        v = int((-1 - tot_R[a]) * 12); lo.append(v); hi.append(v)
    A.append([1] * ns + [0] * 5); lo.append(0); hi.append(cap)
    c = np.array([1] * ns + [0] * 5, dtype=float)
    res = milp(c, constraints=LinearConstraint(np.array(A, dtype=float), lo, hi), integrality=np.ones(nv),
               bounds=Bounds([0] * ns + [-1e4] * 5, [cap] * ns + [1e4] * 5))
    return int(round(res.fun)) if res.success else None
CONTROL = {'SM_20260926_808_24__odd': [('q_1','bu_1','bl_2'), ('q_2','bu_1','bl_4'), ('q_3','bu_1','bl_5')],
           'SM_20260926_2579_27__odd': [('q_1','bu_1','bl_1'), ('q_2','bu_1','bl_6'), ('q_3','bu_1','bl_7')]}
out = {}
for lab in ('SM_20260926_808_24__odd', 'SM_20260926_2579_27__odd'):
    F = fields('../search_drivers_12287/' + lab + '_p1.out')
    g = lambda pre: sorted([n for n in F if re.match(pre + r'_\d+$', n)], key=lambda x: int(x.split('_')[1]))
    q, bu, bd, l, bl, be = g('q'), g('bu'), g('bd'), g('l'), g('bl'), g('be')
    S = [n for n in g('n') if all(d in ('1', '-1') for d in F[n]['dims'])]
    res = dict(singlets=len(S), control={' '.join(c): min_degree(F, list(c), S) for c in CONTROL[lab]})
    print(lab, 'control (engine cubic couplings, must be 0):', res['control'])
    for kind, A_, B_, H in (('up', q, bu, bl), ('down', q, bd, l)):
        best = {}
        for h in H:
            M = [[min_degree(F, [a, b, h], S) for b in B_] for a in A_]
            best[h] = M
        res[kind] = best
    # leptons: l_i be_j l_k with k the H_d choice (any l not used as lepton doublet: report per Hd)
    res['lepton'] = {h: [[min_degree(F, [a, b, h], S) if a != h else None for b in be] for a in l] for h in l}
    out[lab] = res
    print(lab, 'singlets', len(S))
    for kind in ('up', 'down'):
        for h, M in res[kind].items():
            if any(x is not None and x <= 4 for row in M for x in row):
                print('  ', kind, h, M)
json.dump(out, open('texture.json', 'w'), indent=1)
