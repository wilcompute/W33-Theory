"""12250: the statistics rule as a predictor -- for EVERY field of every saved nsoq dump, predict boson iff (P.V0 - w/2) is an integer
(P a left weight, w the Witten label), from the left-movers alone, and compare with the engine's multiplet label (bosons: gauge,
scalar, moduli, gravity, tachyons; fermions: 19, 20).  Mismatches are listed by sector."""
import glob, json, os, re
from fractions import Fraction as F
from collections import Counter

BOS = {8, 9, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24}
FER = {19, 20}
dumps = []
for p in glob.glob(r'C:\tmp\toe_wt\analysis\search_drivers_12230\nsoq_*.txt'):
    lab = os.path.basename(p)[5:-4]
    model = r'C:\tmp\toe_round\stype\cand10\%s.txt' % lab
    if not os.path.exists(model):
        model = r'C:\tmp\toe_wt\analysis\search_drivers_12230\model_Z6II_2496_v0.txt'
    dumps.append((lab, p, model))
for p in glob.glob(r'C:\tmp\toe_wt\analysis\search_drivers_12237\nsoq_a8_*.txt'):
    n = p.split('nsoq_a8_')[1][:-4]
    dumps.append(('A8_' + n, p, r'C:\tmp\toe_wt\analysis\search_drivers_12237\a8_%s.txt' % n))
out = {}
for lab, p, model in dumps:
    V0 = [F(x.strip(',')) for x in open(model).read().split('Shifts and Wilsonlines:')[1].strip().split('\n')[0].replace(',', ' ').split()]
    agree = Counter(); mism = Counter(); cur = None
    def close(f):
        if not f or f['m'] not in BOS | FER or not f['W']:
            return
        engine = 'B' if f['m'] in BOS else 'F'
        preds = set()
        for W in f['W']:
            x = (sum(a * b for a, b in zip(W, V0)) - F(f['w'], 2)) % 1
            preds.add('B' if x == 0 else 'F' if x == F(1, 2) else 'other')
        pred = preds.pop() if len(preds) == 1 else 'mixed'
        (agree if pred == engine else mism)[(f['sec'], engine, pred)] += 1
    for l in open(p):
        if l.startswith('FIELD'):
            close(cur)
            m = re.match(r'FIELD \d+ m=(\d+) k=(\d+) mm=(\d+) n=(\d+)', l)
            cur = dict(m=int(m.group(1)), w=int(m.group(3)), sec=(int(m.group(2)), int(m.group(3)), int(m.group(4))), W=[])
        elif l.startswith('W ') and cur:
            cur['W'].append([F(x).limit_denominator(24) for x in l[2:].split(',')])
    close(cur)
    out[lab] = dict(agree=sum(agree.values()), mismatch=sum(mism.values()), mismatches={f'{k}': v for k, v in mism.items()})
    print(lab, out[lab]['agree'], 'agree,', out[lab]['mismatch'], 'mismatch', dict(mism) if mism else '')
json.dump(out, open('predict.json', 'w'), indent=1)
