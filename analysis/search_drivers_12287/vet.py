"""12287: vet the 12 new Z2xZ6-I three-generation SUSY SM brothers (12282) against their 12 parents.
Pass 1 (levelprobe, orbifolder 1.2.1): left-chiral fields with labels, U(1) charges (2nd entry = hypercharge), q_sh, oscillators.
Pass 2: every renormalisable QLd (q l bd) and udd (bu bd bd) trilinear checked by the engine (gauge + space group) and then by the
R rule  sum_i (q_sh + osc)^a = -1 mod N_a,  N = (2, 6, 6) for Z2xZ6-I (twists (0,1/2,0,-1/2), (0,0,1/6,-1/6)).
usage: py -3 vet.py pass1 | pass2 | report"""
import json, sys, os, subprocess, itertools, re, collections
from fractions import Fraction as Fr
B = '/mnt/c/tmp/toe_wt/analysis/search_drivers_12282/'
SHW = 'C:/Users/wiljd/AppData/Local/Temp/claude/c--Repos-Theory-of-Everything/ad42d157-70aa-40e7-80cd-3fad6695948b/scratchpad/'
SH = '/mnt/c/Users/wiljd/AppData/Local/Temp/claude/c--Repos-Theory-of-Everything/ad42d157-70aa-40e7-80cd-3fad6695948b/scratchpad/'
new = json.load(open('../search_drivers_12282/new_sm.json'))
idx = {e['model']: e for e in json.load(open('../search_drivers_12282/index.json'))}
models = []
for n in new:
    models.append((n['model'] + '__odd', B + idx[n['model']]['files']['odd']))
    models.append((n['model'] + '__ctrl', B + idx[n['model']]['files']['ctrl']))
N = (2, 6, 6)


def run(model, req, out):
    open('req_' + out + '.txt', 'w', newline='\n').write(req)
    sh = (f'export LD_LIBRARY_PATH=/tmp/su9/lib:$HOME/orb/sysroot/usr/lib/x86_64-linux-gnu; cd ~/orb/scan; '
          f'timeout 3000 /tmp/su9/probe/levelprobe {model} /mnt/c/tmp/toe_wt/analysis/search_drivers_12287/req_{out}.txt '
          f'> /mnt/c/tmp/toe_wt/analysis/search_drivers_12287/{out}.out 2>&1')
    open(SHW + 'vetrun.sh', 'w', newline='\n').write(sh + '\n')
    subprocess.run(['wsl', 'bash', SH + 'vetrun.sh'], env={**os.environ, 'MSYS_NO_PATHCONV': '1'})


def fields(out):
    F = {}
    for l in open(out + '.out', errors='ignore'):
        if l.startswith('F '):
            p = l.split()
            name = p[1]
            i = p.index('dims'); j = p.index('u1'); k = p.index('qsh'); m = p.index('osc'); g = p.index('gam')
            F[name] = dict(dims=p[i + 1:j], u1=[float(x) for x in p[j + 1:k]], qsh=[Fr(x).limit_denominator(12) for x in p[k + 1:m]],
                           osc=[Fr(x).limit_denominator(12) for x in p[m + 1:g]])
    return F


def rok(names, F):
    for a in range(1, 4):
        s = sum(F[n]['qsh'][a] + F[n]['osc'][a] for n in names)
        if (s + 1) % N[a - 1] != 0:
            return False
    return True


if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'pass1':
        for lab, path in models:
            run(path, '', lab + '_p1')
            print(lab, len(fields(lab + '_p1')))
    elif mode == 'pass2':
        for lab, path in models:
            F = fields(lab + '_p1')
            q = [n for n in F if re.match(r'q_\d', n)]; l = [n for n in F if re.match(r'l_\d', n)]
            bd = [n for n in F if re.match(r'bd_\d', n)]; bu = [n for n in F if re.match(r'bu_\d', n)]
            req = [' '.join(c) for c in itertools.product(q, l, bd)] + [' '.join((u,) + c) for u in bu for c in itertools.combinations_with_replacement(bd, 2)]
            run(path, '\n'.join(req) + '\n', lab + '_p2')
            print(lab, len(req), 'requests')
    else:
        rep = {}
        for lab, path in models:
            F = fields(lab + '_p1')
            cnt = collections.Counter(re.match(r'([a-zA-Z]+)_', n).group(1) for n in F)
            allowed = collections.Counter()
            for l in open(lab + '_p2.out', errors='ignore'):
                if l.startswith('CHECK'):
                    p = l.split(); c = int(p[1]); names = p[2:]
                    if c > 0 and all(n in F for n in names):
                        kind = 'QLd' if names[0].startswith('q') else 'udd'
                        allowed[kind + ' gauge+SG'] += 1
                        if rok(names, F):
                            allowed[kind + ' gauge+SG+R'] += 1
            rep[lab] = dict(fields=dict(cnt), allowed=dict(allowed))
            print(lab, dict(cnt), dict(allowed))
        json.dump(rep, open('vet.json', 'w'), indent=1)
