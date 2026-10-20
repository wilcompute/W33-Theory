"""12122: Yukawa selection rules (gauge, point group, space group, H-momentum) for psi psi phi couplings in the four
three-generation models; quark-doublet x colour-antitriplet x Higgs-doublet couplings classified by sector and hypercharge."""
import re
import sys
import json
import itertools
from fractions import Fraction as Fr
from collections import Counter, defaultdict

sys.path.insert(0, r'C:\tmp\toe_round\stype')
import hyper as H
import os
EXACT = os.environ.get('EXACT') == '1'


def parse(path):
    fac, u1, fields = [], [], []
    for line in open(path).read().split('\n'):
        if line.startswith('FACTOR'):
            parts = line.split('|')
            fac.append((parts[0].split()[2], [[H.F(x) for x in p.split()] for p in parts[1:]]))
        elif line.startswith('U1 '):
            u1.append([H.F(x) for x in line.split('|')[1].split()])
        elif line.startswith('FIELD'):
            d = dict(re.findall(r'(\w+)=(\S*)', line))
            lat = [Fr(x) for x in d['lat'].split(',')]
            fields.append(dict(i=int(line.split()[1]), m=int(d['m']), mm=int(d['mm']), n=int(d['n']), lat=lat,
                               dim=d['dim'].split(','), osc=[H.F(x) for x in d['osc'].split(',')], W=[], R=[]))
        elif line.startswith('W '):
            fields[-1]['W'].append(tuple(H.F(x) for x in line[2:].split(',')))
        elif line.startswith('R '):
            fields[-1]['R'].append(tuple(H.F(x) for x in line[2:].split(',')))
    return fac, u1, fields


def rot(l, k):
    """theta^k on (a,b) per torus, theta: (a,b) -> (-b, a-b)"""
    out = list(l)
    for _ in range(k % 3):
        out = sum([[-out[2 * t + 1], out[2 * t] - out[2 * t + 1]] for t in range(3)], [])
    return out


def sg_ok(fs):
    if sum(f['n'] for f in fs) % 3 or sum(f['mm'] for f in fs) % 2:
        return False
    if any(f['n'] for f in fs):
        return all(sum(f['lat'][2 * t] + f['lat'][2 * t + 1] for f in fs) % 3 == 0 for t in range(3))
    for ks in itertools.product(range(3), repeat=len(fs)):
        s = [sum(x) for x in zip(*[rot(f['lat'], k) for f, k in zip(fs, ks)])]
        if all(x == 0 for x in s):
            return True
    return False


def hm_ok(fs, conj):
    """exists RM weights (scalar possibly conjugated) with internal sum + osc = 0 mod 3 per plane"""
    choices = []
    for f, c in zip(fs, conj):
        rs = [tuple((-x if c else x) + (-o if c else o) for x, o in zip(r, f['osc'])) for r in f['R']]
        choices.append(rs)
    for rr in itertools.product(*choices):
        s = [sum(r[i] for r in rr) for i in range(4)]
        if all((s[i] == 0) if EXACT else (s[i] % 3 == 0) for i in (1, 2, 3)):
            return True
    return False


def run(m, ygood):
    fac, u1, fields = parse(r'C:\tmp\toe_round\stype\q4\%s.q' % m)
    col = [i for i, (n, _) in enumerate(fac) if n == 'A2'][0]
    r = H.analyse(r'C:\tmp\toe_round\stype\q4\%s.q' % m)
    L = r['L']
    y = [Fr(x) for x in ygood]
    left = [f for f in fields if f['m'] == 19]
    scal = [f for f in fields if f['m'] in (15, 16)]
    hset = defaultdict(list)
    for s in scal:
        for w in s['W']:
            hset[w].append(s)
    dc = lambda f: H.dsgn(f['dim'][col])  # noqa: E731
    dl = lambda f: int(f['dim'][L])  # noqa: E731
    sect = lambda f: ('U' if f['n'] == 0 and f['mm'] == 0 else 'W' if f['n'] == 0 else 'T%d%s' % (f['n'], 'w' if f['mm'] else ''))  # noqa: E731
    # all gauge-invariant psi psi phi couplings, then the quark ones
    allowed = Counter()
    quark = []
    for a, b in itertools.combinations_with_replacement(range(len(left)), 2):
        A, B = left[a], left[b]
        seen = set()
        for wa in A['W']:
            for wb in B['W']:
                key = tuple(-(x + z) for x, z in zip(wa, wb))
                for S in hset.get(key, []):
                    if S['i'] in seen:
                        continue
                    seen.add(S['i'])
                    if not sg_ok([A, B, S]):
                        continue
                    if not hm_ok([A, B, S], [False, False, False]):
                        continue
                    allowed[(sect(A), sect(B), sect(S))] += 1
                    pair = None
                    for X, Z in ((A, B), (B, A)):
                        if abs(dc(X)) == 3 and dl(X) == 2 and abs(dc(Z)) == 3 and dl(Z) == 1 and dc(S) == 1 and dl(S) == 2:
                            pair = (X, Z)
                    if pair:
                        X, Z = pair
                        yX, yZ, yS = H.dot(y, X['W'][0]), H.dot(y, Z['W'][0]), -H.dot(y, X['W'][0]) - H.dot(y, Z['W'][0])
                        yZs = sorted(set(H.dot(y, w) for w in Z['W']))
                        quark.append(dict(Q=X['i'], Qsec=sect(X), Qy=str(yX), c=Z['i'], csec=sect(Z), cy=[str(v) for v in yZs],
                                          H=S['i'], Hsec=sect(S), Hm=S['m'], Hdim=S['dim']))
    return allowed, quark


if __name__ == '__main__':
    hy = json.load(open(r'C:\tmp\toe_round\stype\hyper3_4.json'))
    out = {}
    for m in sys.argv[1:]:
        allowed, quark = run(m, hy[m]['y_good'])
        unt = sum(v for k, v in allowed.items() if set(k) == {'U'})
        print(m, 'allowed psi psi phi:', sum(allowed.values()), 'all-untwisted', unt, 'by sector', dict(allowed.most_common(8)))
        print('  quark doublet x antitriplet x Higgs-doublet couplings:', len(quark))
        for q in quark[:20]:
            print('   ', q)
        out[m] = dict(allowed={'|'.join(k): v for k, v in allowed.items()}, quark=quark)
    json.dump(out, open(r'C:\tmp\toe_round\stype\yuk_5%s.json' % ('_exact' if EXACT else '') + '', 'w'), indent=1)
