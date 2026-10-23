"""12235: the statistics rule derived.  Projection phase of the Witten element g = (V0, s0) on a state of sector h = (w, n, m_a):
(P.V0 - R.s0) - (1/2)(V_h.V0 - v_h.s0) in Z, with R.s0 = R0, v_h.s0 = w, V_h.V0 = w V0^2 + n V1.V0 + sum m_a W_a.V0.  Hence
(P.V0 - R0) = c_h = (1/2)(w (V0^2 - 1) + n V1.V0 + sum m_a W_a.V0) mod 1, which is w/2 iff V0^2 = 2 mod 2... precisely iff
w(V0^2 - 2) + n V1.V0 + sum m_a W_a.V0 is even.  Check the inputs on every model the rule was observed in."""
import glob, json, re
from fractions import Fraction as F


def rows_of(path):
    t = open(path).read()
    rows = t.split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')
    return [[F(x.strip(',')) for x in r.replace(',', ' ').split()] for r in rows]


dot = lambda a, b: sum(x * y for x, y in zip(a, b))
out = {}
files = glob.glob(r'C:\tmp\toe_wt\analysis\search_drivers_12230\model_*.txt')
names = [p for p in glob.glob(r'C:\tmp\toe_wt\analysis\search_drivers_12230\nsoq_*.txt')]
for n in names:
    lab = n.split('nsoq_')[1][:-4]
    mp = r'C:\tmp\toe_round\stype\cand10\%s.txt' % lab
    try:
        rows = rows_of(mp)
    except OSError:
        rows = rows_of(r'C:\tmp\toe_wt\analysis\search_drivers_12230\model_Z6II_2496_v0.txt')
    V0 = rows[0]
    shifts = rows[1:]
    out[lab] = dict(V0sq=str(dot(V0, V0)), products=[str(dot(V0, s)) for s in shifts],
                    all_even=all(dot(V0, s).denominator == 1 and dot(V0, s) % 2 == 0 for s in shifts), V0sq_is_2=dot(V0, V0) == 2)
    print(lab, out[lab])
json.dump(out, open('derive.json', 'w'), indent=1)
