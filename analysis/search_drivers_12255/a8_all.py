"""12255: the statistics rule across every A8 SO(16) x SO(16) Standard Model of a8_sm_all.txt (Pass 11095 route): for each model, nsoq
dump, then for every field predict boson iff P.V0 - w/2 is an integer (left weights only) and compare with the engine's label."""
import json, os, re, subprocess
from fractions import Fraction as F
from collections import Counter
BOS = {8, 9, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24}; FER = {19, 20}
sh = "cat ~/orb/p1109x/a8/a8_sm_all.txt"
txt = subprocess.run(['wsl', '-e', 'bash', '-lc', sh], capture_output=True, text=True).stdout
blocks = ['begin model' + b.split('end model')[0] + 'end model\n' for b in txt.split('begin model')[1:]]
print('models', len(blocks), flush=True)
res = {}; tot = Counter()
os.makedirs(r'C:\tmp\toe_round\stype\a8all', exist_ok=True)
for i, b in enumerate(blocks):
    lab = re.search(r'Label:(\S+)', b).group(1)
    fn = r'C:\tmp\toe_round\stype\a8all\m%03d.txt' % i
    open(fn, 'w', newline='\n').write(b)
    sh = ('cd ~/orb/nsobuild && export LD_LIBRARY_PATH=/tmp/su9/lib:$HOME/orb/sysroot/usr/lib/x86_64-linux-gnu; '
          'timeout 900 ./nsoq /mnt/c/tmp/toe_round/stype/a8all/m%03d.txt' % i)
    o = subprocess.run(['wsl', '-e', 'bash', '-lc', sh], capture_output=True, text=True).stdout
    V0 = [F(x.strip(',')) for x in b.split('Shifts and Wilsonlines:')[1].strip().split('\n')[0].replace(',', ' ').split()]
    agree = mism = 0; mm = Counter(); cur = None
    def close(f):
        global agree, mism
        if not f or f['m'] not in BOS | FER or not f['W']:
            return
        eng = 'B' if f['m'] in BOS else 'F'
        pr = set()
        for W in f['W']:
            x = (sum(a * c for a, c in zip(W, V0)) - F(f['w'], 2)) % 1
            pr.add('B' if x == 0 else 'F' if x == F(1, 2) else 'other')
        p = pr.pop() if len(pr) == 1 else 'mixed'
        if p == eng:
            agree += 1
        else:
            mism += 1; mm[(f['sec'], eng, p)] += 1
    for l in o.splitlines():
        if l.startswith('FIELD'):
            close(cur)
            m = re.match(r'FIELD \d+ m=(\d+) k=(\d+) mm=(\d+) n=(\d+)', l)
            cur = dict(m=int(m.group(1)), w=int(m.group(3)), sec=(int(m.group(2)), int(m.group(3)), int(m.group(4))), W=[])
        elif l.startswith('W ') and cur:
            cur['W'].append([F(x).limit_denominator(24) for x in l[2:].split(',')])
    close(cur)
    res[lab] = dict(agree=agree, mismatch=mism, mismatches={str(k): v for k, v in mm.items()})
    tot['agree'] += agree; tot['mismatch'] += mism
    print(i, lab, agree, mism, flush=True)
    json.dump(dict(models=len(res), total=dict(tot), per_model=res), open('a8_all.json', 'w'), indent=1)
print('DONE', dict(tot))
