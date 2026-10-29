"""12351b: the hypercharge of the five SUSY parents (SM_2618, 2503, 574, 2913, 1105 in search_drivers_12205/z6ii_sm_all.txt, keyed by
base to avoid the 12200 label collision) as an exact 16-vector: levelprobe (orbifolder 1.2.1) prints each field's U(1) charges (the
second entry is the SM-analyser hypercharge) and its left-moving weights; Y_vec is the exact solution of Y_vec . P = Y over all
fields (overdetermined; consistency checked)."""
import re, json, subprocess, os, sys
import sympy as sp
SHW = 'C:/Users/wiljd/AppData/Local/Temp/claude/c--Repos-Theory-of-Everything/ad42d157-70aa-40e7-80cd-3fad6695948b/scratchpad/'
SH = '/mnt/c/Users/wiljd/AppData/Local/Temp/claude/c--Repos-Theory-of-Everything/ad42d157-70aa-40e7-80cd-3fad6695948b/scratchpad/'
want = {'Z6II_06': 'SM_20260917_2618', 'Z6II_12a': 'SM_20260917_2503', 'Z6II_12b': 'SM_20260917_574', 'Z6II_23': 'SM_20260917_2913', 'Z6II_59': 'SM_20260917_1105'}
txt = open('../search_drivers_12205/z6ii_sm_all.txt').read()
base = None; models = {}
for line_blk in re.split(r'(?=BASE |begin model)', txt):
    if line_blk.startswith('BASE '):
        base = line_blk.split()[1]; continue
    if line_blk.startswith('begin model'):
        lab = re.search(r'Label:(\S+)', line_blk).group(1)
        models[(base, lab)] = line_blk.split('end model')[0] + 'end model\n'
out = {}
for key, lab in (('Z6II_06', 'SM_20260917_2618'), ('Z6II_12', 'SM_20260917_2503'), ('Z6II_12', 'SM_20260917_574'), ('Z6II_23', 'SM_20260917_2913'), ('Z6II_59', 'SM_20260917_1105')):
    blk = models.get((key, lab))
    if blk is None:
        print('missing', key, lab); continue
    fn = f'susy_{lab}.txt'; open(fn, 'w', newline='\n').write(blk)
    sh = (f'export LD_LIBRARY_PATH=/tmp/su9/lib:$HOME/orb/sysroot/usr/lib/x86_64-linux-gnu; cd ~/orb/scan; printf "" > /tmp/empty_req.txt; '
          f'timeout 900 /tmp/su9/probe/levelprobe /mnt/c/tmp/toe_wt/analysis/search_drivers_12351/{fn} /tmp/empty_req.txt > /mnt/c/tmp/toe_wt/analysis/search_drivers_12351/{fn[:-4]}.out 2>&1')
    open(SHW + 'yv.sh', 'w', newline='\n').write(sh + '\n')
    subprocess.run(['wsl', 'bash', SH + 'yv.sh'], env={**os.environ, 'MSYS_NO_PATHCONV': '1'})
    rows, rhs = [], []
    for l in open(fn[:-4] + '.out', errors='ignore'):
        if l.startswith('F '):
            p = l.split(); u = p.index('u1'); k = p.index('qsh'); w = p.index('w'); nw = int(p[p.index('nw') + 1])
            Y = sp.nsimplify(float(p[u + 2]), tolerance=1e-9, rational=True)
            ws = [float(x) for x in p[w + 1:]]
            for j in range(nw):
                P = [sp.nsimplify(x, tolerance=1e-9, rational=True) for x in ws[16 * j:16 * j + 16]]
                if len(P) == 16:
                    rows.append(P); rhs.append(Y)
    A = sp.Matrix(rows); bvec = sp.Matrix(rhs)
    sol, params = A.gauss_jordan_solve(bvec)
    yv = sol.subs({t: 0 for t in params})
    resid = max(abs(x) for x in (A * yv - bvec))
    out[lab] = dict(Yvec=[str(x) for x in yv], equations=len(rhs), free=len(params), residual=str(resid))
    print(lab, 'equations', len(rhs), 'free params', len(params), 'residual', resid, 'Y^2 =', sum(x * x for x in yv))
json.dump(out, open('yvec.json', 'w'), indent=1)
