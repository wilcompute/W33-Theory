"""12276: torsion brothers of the 128 Z6-II A8 Standard Models (search_drivers_12205/z6ii_sm_all.txt, SUSY orbifolder 1.2.1).
For an order-2 Wilson line on the SU(2)^2 torus (W5 = row 6, W6 = row 7) a lattice shift lam acts on the model only through
c(lam) = (2 X.lam mod 4 for X = V, W3, W5, W6) (every induced phase B is a function of it), so the brothers are the image subgroup
of E8 x E8 under c, built by closure from the 480 roots in exact integer arithmetic (vectors x 12).  Classes whose shifted model fails
the engine's own conditions (prefactors gcd of orders 6, 3, 2: 2 W'.V, W'.W3, 2 W'.W', 2 W'.W_other even) are not written; a sample of
them is kept as a control that the engine indeed rejects."""
import json, re, sys, random
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, '../search_drivers_12267')
from mirage import e8_short, fmt
dot = lambda a, b: sum(x * y for x, y in zip(a, b))
even = lambda x: x.denominator == 1 and x % 2 == 0
R8 = [list(r) for r in e8_short(2) if sum(x * x for x in r) == 2]
Z8 = [F(0)] * 8
ROOTS = [r + Z8 for r in R8] + [Z8 + r for r in R8]
R12 = np.array([[int(12 * x) for x in r] for r in ROOTS], dtype=np.int64)


def models(path):
    # labels are not unique across base files (SM_20260917_894 occurs in Z6II_01 and Z6II_06; the 12200 artefact):
    # a repeated label gets a suffix b, c, ... so no file is overwritten
    t = open(path).read()
    seen = {}
    for blk in t.split('begin model')[1:]:
        lab = re.search(r'Label:(\S+)', blk).group(1)
        seen[lab] = seen.get(lab, 0) + 1
        if seen[lab] > 1:
            blk = blk.replace('Label:' + lab, 'Label:' + lab + 'bcdefgh'[seen[lab] - 2], 1)
            lab = lab + 'bcdefgh'[seen[lab] - 2]
        head = 'begin model' + blk.split('Shifts and Wilsonlines:')[0]
        rows = [[F(x) for x in r.replace(',', ' ').split()] for r in blk.split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n') if r.strip()]
        yield lab, head, rows


def image(rows):
    X = np.array([[int(12 * x) for x in rows[k]] for k in (0, 4, 6, 7)], dtype=np.int64)    # 12 X
    G = (R12 @ X.T) % 288                       # 144 X.lam per root, mod 288 <=> 2 X.lam mod 4
    rep = {(0, 0, 0, 0): np.zeros(16, dtype=np.int64)}
    frontier = [(0, 0, 0, 0)]
    while frontier:
        new = []
        for g in frontier:
            for i in range(len(R12)):
                h = tuple((np.array(g) + G[i]) % 288)
                if h not in rep:
                    rep[h] = rep[g] + R12[i]; new.append(h)
        frontier = new
    return rep


def consistent(rows, line):
    W = rows[line]
    other = 7 if line == 6 else 6
    return (even(2 * dot(W, rows[0])) and even(dot(W, rows[4])) and even(2 * dot(W, W)) and even(2 * dot(W, rows[other])))


def write(path, head, lab, tag, rows):
    open(path, 'w', newline='\n').write(head.replace('Label:' + lab, 'Label:' + lab + tag) + 'Shifts and Wilsonlines:\n'
                                        + '\n'.join(' '.join(fmt(x) for x in r) for r in rows) + '\nend model\n')


if __name__ == '__main__':
    only = set(sys.argv[1:])
    rng = random.Random(3)
    out, lst, rej = [], [], []
    for lab, head, rows in models('../search_drivers_12205/z6ii_sm_all.txt'):
        assert len(rows) == 8, (lab, len(rows))
        if only and lab not in only:
            continue
        for line in (6, 7):
            if not any(rows[line]):
                continue
            rep = image(rows)
            j = 0
            for c, lam12 in sorted(rep.items()):
                lam = [F(int(x), 12) for x in lam12]
                new = [r[:] for r in rows]
                new[line] = [x + y for x, y in zip(new[line], lam)]
                tag = f'_W{line - 1}_{j:03d}'
                if consistent(new, line):
                    name = f'bro/{lab}{tag}.txt'
                    write(name, head, lab, tag, new)
                    out.append(dict(model=lab, line=line - 1, j=j, cls=list(map(int, c)), trivial=not any(lam), file=name))
                    lst.append('/mnt/c/tmp/toe_wt/analysis/search_drivers_12276/' + name)
                elif rng.random() < 0.01:
                    name = f'bro/REJ_{lab}{tag}.txt'
                    write(name, head, lab, tag, new)
                    rej.append('/mnt/c/tmp/toe_wt/analysis/search_drivers_12276/' + name)
                j += 1
    sfx = '_fix' if only else ''
    json.dump(out, open(f'brothers_index{sfx}.json', 'w'), indent=1)
    open(f'bro_list{sfx}.txt', 'w', newline='\n').write('\n'.join(lst) + '\n')
    open(f'rej_list{sfx}.txt', 'w', newline='\n').write('\n'.join(rej) + '\n')
    import collections
    print(len(out), 'consistent class representatives;', len(rej), 'rejected-class controls;',
          collections.Counter(collections.Counter(o['model'] + str(o['line']) for o in out).values()))
