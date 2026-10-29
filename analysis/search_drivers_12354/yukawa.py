"""12354: renormalisable (degree-0) Yukawa couplings of SM_2913_v6 (non-SUSY: fermion-fermion-scalar).  Fields: left-handed Weyl fermions
(m = 19) of SM type under the chosen SU(3) x SU(2) and Y (SUSY parent's exact vector), all other factors singlet; Higgs scalars (1,2)_{+-1/2}
(scalars m = 15/16; a scalar or its conjugate may enter).  A coupling chi_a chi_b phi is allowed iff the three exact U(1) charge vectors
(basis = complement of the non-abelian roots, applied to each field's first weight) sum to zero (phi or phi*), SU(3) x SU(2) contraction
exists by representation (Q u^c H, Q d^c H~, L e^c H~ types), and the space-group rule holds: sum of Z6 powers = 0 mod 6, sum of
Witten labels = 0 mod 2, sum of fixed-point translations in sum_k (1 - theta^k) Lambda over the sectors present.  Output: for up, down,
lepton, the coupling count and the rank of the coupling pattern (max over Higgs choices) -- structural rank, an upper bound."""
import re, json, os, itertools, collections
import numpy as np
import sympy as sp
yv = json.load(open('../search_drivers_12351/yvec.json')); ch = json.load(open('../search_drivers_12351/chiral.json'))
th = np.zeros((6, 6), dtype=np.int64)
th[0:2, 0:2] = [[1, -1], [1, 0]]; th[2:4, 2:4] = [[0, -1], [1, -1]]; th[4:6, 4:6] = -np.eye(2, dtype=np.int64)
D6 = {k: sp.Matrix(np.eye(6, dtype=np.int64) - np.linalg.matrix_power(th, k)) for k in range(1, 6)}
def in_translation_lattice(vec, sectors):
    gens = [D6[k][:, j] for k in sectors for j in range(6)] if sectors else []
    if not gens:
        return all(x == 0 for x in vec)
    from sympy.matrices.normalforms import hermite_normal_form
    M = sp.Matrix.hstack(*gens)
    H = hermite_normal_form(M); H = sp.Matrix.hstack(*[H[:, j] for j in range(H.shape[1]) if any(H[:, j])])
    try:
        x, prm = H.gauss_jordan_solve(sp.Matrix(vec))
    except ValueError:
        return False
    return all(e.is_integer for e in x.subs({t: 0 for t in prm}))
def load(m):
    lab = re.search(r'(SM_20260917_\d+)', m).group(1); Y = [sp.Rational(x) for x in yv[lab]['Yvec']]
    D = '../search_drivers_12302/bro/' if os.path.exists(f'../search_drivers_12302/bro/{m}__ctrl.nsoq') else '../search_drivers_12281/bro/'
    p = D + f'{m}__ctrl.nsoq'
    roots = []
    for l in open(p, errors='ignore'):
        if l.startswith('FACTOR'):
            for r in l.split('|')[1:]:
                roots.append([sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in r.split()])
    Ub = sp.Matrix(roots).nullspace()
    out = []; cur = None
    for l in open(p, errors='ignore'):
        if l.startswith('FIELD'):
            mm = re.match(r'FIELD \d+ m=(\S+) k=\S+ mm=(\S+) n=(\S+) lat=(\S+) dim=(\S*) q=', l)
            cur = dict(m=int(mm.group(1)), w=int(mm.group(2)), n=int(mm.group(3)), lat=[int(sp.Rational(x)) for x in mm.group(4).split(',')],
                       d=tuple(int(re.match(r'-?\d+', x).group(0)) for x in mm.group(5).split(',')) if mm.group(5) else (), P=None)
            out.append(cur)
        elif l.startswith('W ') and cur is not None and cur['P'] is None:
            cur['P'] = sp.Matrix([sp.nsimplify(float(x), tolerance=1e-9, rational=True) for x in l[2:].split(',')])
    for f in out:
        f['y'] = sum(a * b for a, b in zip(Y, f['P'])) if f['P'] is not None else None
        f['q'] = [(u.T * f['P'])[0] for u in Ub] if f['P'] is not None else None
    return out
m = 'Z6II_23_SM_20260917_2913_v6'
fs = load(m); i3, i2 = ch[m]['SU3'], ch[m]['SU2']
def sm_singlet_elsewhere(f):
    return all(abs(f['d'][j]) == 1 for j in range(len(f['d'])) if j not in (i3, i2))
F = [f for f in fs if f['m'] == 19 and sm_singlet_elsewhere(f)]
H = [f for f in fs if f['m'] in (15, 16) and sm_singlet_elsewhere(f) and abs(f['d'][i3]) == 1 and abs(f['d'][i2]) == 2 and abs(f['y']) == sp.Rational(1, 2)]
def typ(f):
    a, b, y = f['d'][i3], abs(f['d'][i2]), f['y']
    s = 1 if a > 0 else -1
    if abs(a) == 3 and b == 2: return ('Q', s * y)
    if abs(a) == 3 and b == 1: return ('T', s * y)
    if abs(a) == 1 and b == 2: return ('L', y)
    if abs(a) == 1 and b == 1: return ('S', y)
    return ('X', y)
groups = collections.defaultdict(list)
for f in F:
    groups[typ(f)].append(f)
print('fermion groups:', {f'{k[0]},{k[1]}': len(v) for k, v in groups.items() if k[0] != 'S'})
def coupling_ok(a, b, h):
    for sh in (1, -1):    # phi or phi*
        if all(x + y + sh * z == 0 for x, y, z in zip(a['q'], b['q'], h['q'])) and (a['y'] + b['y'] + sh * h['y'] == 0):
            nsum = a['n'] + b['n'] + sh * h['n']; wsum = a['w'] + b['w'] + sh * h['w']
            if nsum % 6 or wsum % 2:
                continue
            lat = [a['lat'][i] + b['lat'][i] + sh * h['lat'][i] for i in range(6)]
            sectors = sorted({k % 6 for k in (a['n'], b['n'], h['n']) if k % 6} | {(6 - k) % 6 for k in (a['n'], b['n'], h['n']) if k % 6})
            if in_translation_lattice(lat, sectors):
                return True
    return False
# Y sign: the SUSY parent's vector gives quark doublets Y = -1/6 in this orientation (12351); define types relative to that
qd = [k for k in groups if k[0] == 'Q']
print('quark-doublet hypercharges present:', qd)
# The fitted Y vector carries the opposite overall sign (quark doublets at -1/6), so in this orientation: up-type Q x T(-2/3),
# down-type Q x T(+1/3), lepton L(+1/2) x S(-1).  (A first version did not split by type; corrected here.)
import networkx as nx
out = {}
for name, ka, kb in (('up', ('Q', sp.Rational(-1, 6)), ('T', sp.Rational(-2, 3))), ('down', ('Q', sp.Rational(-1, 6)), ('T', sp.Rational(1, 3))),
                     ('lepton', ('L', sp.Rational(1, 2)), ('S', -1))):
    fa, fb = groups.get(ka, []), groups.get(kb, [])
    pairs = [(a, b, h) for a in fa for b in fb for h in H if coupling_ok(a, b, h)]
    best = 0
    for h in H:
        G = nx.Graph(); [G.add_edge(('a', id(a)), ('b', id(b))) for (a, b, hh) in pairs if hh is h]
        best = max(best, len(nx.max_weight_matching(G, maxcardinality=True)) if G.number_of_edges() else 0)
    out[name] = dict(left=len(fa), right=len(fb), higgs=len(H), couplings=len(pairs), structural_rank_max_over_higgs=best)
    print(name, out[name])
json.dump(out, open('yukawa.json', 'w'), indent=1)
