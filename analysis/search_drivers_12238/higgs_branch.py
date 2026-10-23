"""12244: SM_2496 -- is the shift-broken class (v9: hidden A2 + A1) the stabiliser of a scalar-10 vev of the unbroken class (v0: hidden
A4 with scalar 10s)?  Hidden A4 roots of v0 (E8 x E8 roots integral on every shift and Wilson line, the 20-root component); the
scalar-10 left weights from the v0 nsoq dump; for each, the A4 roots orthogonal to its A4 projection; compare with the v9 roots
that lie in the span of the v0 A4."""
import json, re, sys
import numpy as np
from fractions import Fraction as F
sys.path.insert(0, r'C:\tmp\toe_wt\analysis')
from w33_pass12087_standard_model_sectors import Gradings
g = Gradings(); R8 = g.R
R = np.vstack([np.hstack([R8, np.zeros_like(R8)]), np.hstack([np.zeros_like(R8), R8])])
integ = lambda a: np.abs(a - np.round(a)) < 1e-9


def rows(path):
    t = open(path).read()
    return [np.array([float(F(x.strip(','))) for x in r.replace(',', ' ').split()]) for r in t.split('Shifts and Wilsonlines:')[1].split('end model')[0].strip().split('\n')]


def unbroken(path):
    m = np.ones(len(R), bool)
    for s in rows(path):
        m &= integ(R @ s)
    return np.nonzero(m)[0]


def comps(idx):
    Rm = R[idx]; G = np.abs(Rm @ Rm.T) > 1e-9; seen = set(); out = []
    for s in range(len(idx)):
        if s in seen: continue
        st = [s]; c = []; seen.add(s)
        while st:
            a = st.pop(); c.append(idx[a])
            for b in np.nonzero(G[a])[0]:
                if b not in seen: seen.add(b); st.append(b)
        out.append(sorted(c))
    return out


u0 = unbroken('model_2496_v0.txt'); u9 = unbroken('model_2496_v9.txt')
A4 = [c for c in comps(u0) if len(c) == 20]
assert len(A4) == 1, [len(c) for c in comps(u0)]
A4 = A4[0]
B = np.linalg.svd(R[A4])[2][:4]
in_span = [i for i in u9 if np.linalg.norm(R[i] - (R[i] @ B.T) @ B) < 1e-9]
# scalar 10 weights of v0
ws = []; cur = None
for l in open('../search_drivers_12230/nsoq_Z6II_2496_v0.txt'):
    if l.startswith('FIELD'):
        m = re.match(r'FIELD \d+ m=(\d+) .*dim=(\S+)', l)
        cur = (int(m.group(1)), m.group(2))
    elif l.startswith('W ') and cur and cur[0] in (15, 16) and any(d.lstrip('-') == '10' for d in cur[1].split(',')):
        ws.append(np.array([float(x) for x in l[2:].split(',')]))
stabs = set()
for w in ws:
    p = (w @ B.T) @ B
    if abs(p @ p - 6 / 5) > 1e-6:
        continue
    st = tuple(sorted(i for i in A4 if abs(R[i] @ p) < 1e-9))
    stabs.add(st)
out = dict(v0_A4_roots=len(A4), v9_roots_in_A4_span=len(in_span), scalar10_weights=len(ws), distinct_stabilisers=len(stabs),
           stabiliser_sizes=sorted(len(s) for s in stabs), v9_equals_a_stabiliser=tuple(sorted(in_span)) in stabs,
           v9_component_sizes=sorted(len(c) for c in comps(np.array(in_span))) if in_span else [])
print(out)
json.dump(out, open('higgs_branch.json', 'w'), indent=1)
