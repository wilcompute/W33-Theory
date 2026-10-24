"""12267: mirage-torsion lattice shifts.  For a T6/Z3 non-SUSY model (rows V0, V1, 0, W1..W6 with W1=W2, W3=W4, W5=W6) failing only
Ploger (7f), search lattice vectors D (E8xE8, norm <= 4) added to one torus' pair of Wilson lines so that (7d) [D.V0 even, 3 D.V1 even]
stay and every 3 W_a.W_b becomes even.  Writes the shifted model.  usage: py -3 mirage.py IN OUT"""
import sys, itertools
from fractions import Fraction as F
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
even = lambda x: x.denominator == 1 and x % 2 == 0


def e8_short(maxnorm=4):
    vs = set()
    for idx in itertools.combinations(range(8), 2):          # integer roots
        for s in itertools.product((1, -1), repeat=2):
            v = [0] * 8
            v[idx[0]], v[idx[1]] = s
            vs.add(tuple(F(x) for x in v))
    for s in itertools.product((1, -1), repeat=8):             # spinor roots
        if s.count(-1) % 2 == 0:
            vs.add(tuple(F(x, 2) for x in s))
    out = {tuple([F(0)] * 8)}
    if maxnorm >= 4:
        roots = list(vs)
        for a in roots:
            for b in roots:
                c = tuple(x + y for x, y in zip(a, b))
                if dot(c, c) in (2, 4):
                    out.add(c)
    return list(vs | out)


def read(path):
    t = open(path).read()
    head, body = t.split('Shifts and Wilsonlines:')
    rows = [[F(x) for x in r.replace(',', ' ').split()] for r in body.split('end model')[0].strip().split('\n') if r.strip()]
    return head, rows


def fails(rows):
    V0, V1, W = rows[0], rows[1], rows[3:]
    bad = []
    for a in range(6):
        if not any(W[a]):
            continue
        if not even(dot(W[a], V0)) or not even(3 * dot(W[a], V1)) or not even(3 * dot(W[a], W[a])):
            bad.append(('d/e', a))
        for b in range(a + 1, 6):
            if any(W[b]) and not even(3 * dot(W[a], W[b])):
                bad.append(('f', a, b))
    return bad


def search(rows, short):
    zero = [F(0)] * 8
    lat = [list(a) + zero for a in short] + [zero + list(a) for a in short]
    for torus in range(3):
        for D in lat:
            if not any(D):
                continue
            new = [r[:] for r in rows]
            for k in (3 + 2 * torus, 4 + 2 * torus):
                if any(new[k]):
                    new[k] = [x + y for x, y in zip(new[k], D)]
            if not fails(new):
                return torus, D, new
    return None


def fmt(x):
    return f'{x.numerator}/{x.denominator}'


if __name__ == '__main__':
    head, rows = read(sys.argv[1])
    print('fails', fails(rows))
    r = search(rows, e8_short())
    if r is None:
        print('NO SHIFT FOUND'); sys.exit(1)
    torus, D, new = r
    print('torus', torus + 1, 'D', [str(x) for x in D])
    open(sys.argv[2], 'w', newline='\n').write(head + 'Shifts and Wilsonlines:\n' + '\n'.join(' '.join(fmt(x) for x in row) for row in new) + '\nend model\n')
