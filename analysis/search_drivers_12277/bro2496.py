"""12277: torsion brothers of the non-SUSY Z6-II model SM_2496 (v0): one-line shifts of its order-2 Wilson line W5 (row 7), all classes
of c(lam) = 2 X.lam mod 4 for X = V0, V1, W3, W5 (closure from the roots, integer arithmetic).  The strict non-SUSY engine decides
consistency; nsoq_strict spectra are compared with the unshifted control.  In the non-SUSY model the order-2 Witten element commutes
with the translation e5, so torsion is possible (unlike the SUSY Z6-II models of 12276)."""
import sys, json
from fractions import Fraction as F
import numpy as np
sys.path.insert(0, '../search_drivers_12267'); sys.path.insert(0, '../search_drivers_12276')
from mirage import read, fmt
from brothers_z6 import R12
head, rows = read('SM2496_v0.txt')
X = np.array([[int(12 * x) for x in rows[k]] for k in (0, 1, 5, 7)], dtype=np.int64)
G = (R12 @ X.T) % 288
rep = {(0, 0, 0, 0): np.zeros(16, dtype=np.int64)}
fr = [(0, 0, 0, 0)]
while fr:
    new = []
    for g in fr:
        for i in range(len(R12)):
            h = tuple((np.array(g) + G[i]) % 288)
            if h not in rep:
                rep[h] = rep[g] + R12[i]; new.append(h)
    fr = new
lst = []
for j, (c, l12) in enumerate(sorted(rep.items())):
    new = [r[:] for r in rows]
    new[7] = [x + F(int(y), 12) for x, y in zip(new[7], l12)]
    p = f'b2496/c{j:03d}.txt'
    open(p, 'w', newline='\n').write(head + 'Shifts and Wilsonlines:\n' + '\n'.join(' '.join(fmt(x) for x in r) for r in new) + '\nend model\n')
    lst.append('/mnt/c/tmp/toe_wt/analysis/search_drivers_12277/' + p)
json.dump({f'c{j:03d}': list(map(int, c)) for j, c in enumerate(sorted(rep))}, open('b2496_classes.json', 'w'))
open('b2496_list.txt', 'w', newline='\n').write('\n'.join(lst) + '\n')
print(len(rep), 'classes')
