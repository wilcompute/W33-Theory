"""Relabelling test: W_a -> W_a + 2 r (r a root with r.V0 integral) changes no Ploger datum (all products shift by even integers) and describes the same
model.  A well-defined engine output must not change.  Even order: the 40 inputs of even_gen.py.  Odd order: the first 40 lenient-only
T6/Z3 models of the 12267 census."""
import json, random, sys, os
from fractions import Fraction as F
sys.path.insert(0, '../search_drivers_12267')
from mirage import read, fmt, e8_short
R8 = [list(r) for r in e8_short(2) if sum(x * x for x in r) == 2]
Z8 = [F(0)] * 8
ROOTS = [r + Z8 for r in R8] + [Z8 + r for r in R8]
rng = random.Random(11)
os.makedirs('relabel', exist_ok=True)
lst = []
def emit(src, tag):
    head, rows = read(src)
    nzr = [k for k in range(3, 9) if any(rows[k])]
    for j in range(2):
        k = rng.choice(nzr)
        V0 = rows[0]
        r = rng.choice([q for q in ROOTS if sum(a * b for a, b in zip(q, V0)).denominator == 1])
        new = [x[:] for x in rows]
        # keep identical-WL pairs identical on Z3 geometry
        ks = [k] if 'Z2xZ2' in head else [3 + 2 * ((k - 3) // 2), 4 + 2 * ((k - 3) // 2)]
        for kk in ks:
            if any(new[kk]):
                new[kk] = [x + 2 * y for x, y in zip(new[kk], r)]
        p = f'relabel/{tag}_r{j}.txt'
        open(p, 'w', newline='\n').write(head + 'Shifts and Wilsonlines:\n' + '\n'.join(' '.join(fmt(x) for x in rr) for rr in new) + '\nend model\n')
        lst.append(p)
if 'oddctrl' in sys.argv:
    for i, n in enumerate(open('oddctrl_models.txt').read().split()):
        emit('../search_drivers_12265/' + n, f'oddc{i:03d}')
elif 'ctrl' in sys.argv:
    for i in range(40):
        emit(f'even/{i:03d}_s0.txt', f'ctrl{i:03d}')
else:
    for i in range(40):
        emit(f'even/{i:03d}_o.txt', f'even{i:03d}')
    for i in range(40):
        emit(f'../search_drivers_12267/census/{i:04d}_o.txt', f'odd{i:04d}')
open('relabel_oddctrl_list.txt' if 'oddctrl' in sys.argv else 'relabel_ctrl_list.txt' if 'ctrl' in sys.argv else 'relabel_list.txt', 'w', newline='\n').write('\n'.join('/mnt/c/tmp/toe_wt/analysis/search_drivers_12271/' + p for p in lst) + '\n')
print(len(lst))
