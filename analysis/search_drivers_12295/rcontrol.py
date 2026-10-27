"""12295a: positive control for the R rule used in 12287 (sum (q_sh + osc)^a = -1 mod N_a, N = (2, 6, 6) on Z2xZ6-I).
Synthetic untwisted fields carry q_sh = -1 in one plane.  Expected: U1 U2 U3 allowed; U2 U2 U2 forbidden (-3 != -1 mod 6);
U1 U1 U1 forbidden (planes 2, 3 sum to 0, not -1); U3 U3 U3 forbidden.  (A first version expected U1 U1 U1 allowed -- the expectation was wrong: every plane must sum to -1.)  Then the rule re-evaluated on every coupling the engine allowed in 12287,
printing the plane sums, to show they satisfy it for a reason, not vacuously."""
import sys, json, collections, re
from fractions import Fraction as Fr
sys.path.insert(0, '../search_drivers_12287')
import vet
def U(a):
    q = [Fr(0)] * 4; q[a] = Fr(-1)
    return dict(qsh=q, osc=[Fr(0)] * 4)
F = {'U1': U(1), 'U2': U(2), 'U3': U(3), 'U1b': U(1), 'U2b': U(2), 'U3b': U(3), 'U1c': U(1), 'U2c': U(2), 'U3c': U(3)}
ctrl = {'U1 U2 U3': vet.rok(['U1', 'U2', 'U3'], F), 'U2 U2 U2': vet.rok(['U2', 'U2b', 'U2c'], F),
        'U1 U1 U1': vet.rok(['U1', 'U1b', 'U1c'], F), 'U3 U3 U3': vet.rok(['U3', 'U3b', 'U3c'], F)}
print('synthetic control:', ctrl)
assert ctrl == {'U1 U2 U3': True, 'U2 U2 U2': False, 'U1 U1 U1': False, 'U3 U3 U3': False}
sums = collections.Counter()
for lab, path in vet.models:
    Fm = vet.fields('../search_drivers_12287/' + lab + '_p1')
    for l in open('../search_drivers_12287/' + lab + '_p2.out', errors='ignore'):
        if l.startswith('CHECK'):
            p = l.split()
            if int(p[1]) > 0:
                names = p[2:]
                s = tuple(str(sum(Fm[n]['qsh'][a] + Fm[n]['osc'][a] for n in names)) for a in (1, 2, 3))
                sums[s] += 1
print('plane sums of engine-allowed couplings:', dict(sums))
json.dump(dict(synthetic=ctrl, plane_sums={str(k): v for k, v in sums.items()}), open('rcontrol.json', 'w'), indent=1)
