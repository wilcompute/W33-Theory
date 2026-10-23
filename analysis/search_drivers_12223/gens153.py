"""12223: generation content of the 153 consistent twisted-10 models of 12217: net left-handed 10 and 5bar of SU(5) (code 19,
counted with all other factor dimensions), the twisted share of each, scalar 5/5bar count, tachyons."""
import json, re, subprocess
r = json.load(open('../search_drivers_12217/cand10_results.json'))
res = []
for x in r:
    if x['gauge'] == 'LOADFAIL':
        continue
    lab = f"C10_{x['base']}_{x['j']}_{x['k']}"
    sh = ('cd ~/orb/nsobuild && export LD_LIBRARY_PATH=/tmp/su9/lib:$HOME/orb/sysroot/usr/lib/x86_64-linux-gnu; '
          'timeout 900 ./nsodump /mnt/c/tmp/toe_round/stype/cand10/%s.txt 2>/dev/null' % lab)
    o = subprocess.run(['wsl', '-e', 'bash', '-lc', sh], capture_output=True, text=True).stdout
    g = re.search(r'GAUGE (.*)', o).group(1)
    facs = [f.strip() for f in g.split(' and ')[0].split(' NU1')[0].split('+')]
    i = facs.index('A4')
    n10 = n5 = n10tw = n5tw = s5 = 0
    for mm in re.finditer(r'^F m=(\d+) k=(\d+) m=(\d+) n=(\d+) dim=(\S+) x(\d+)', o, re.M):
        code, kk, w, n, dims, k = int(mm.group(1)), int(mm.group(2)), int(mm.group(3)), int(mm.group(4)), mm.group(5).split(','), int(mm.group(6))
        rest = 1
        for q, e in enumerate(dims):
            if q != i and e:
                rest *= abs(int(re.match(r'-?\d+', e).group(0)))
        d = dims[i]; tw = bool(kk or n)
        if code == 19:
            a = {'10': 1, '-10': -1}.get(d, 0) * k * rest
            b = {'-5': 1, '5': -1}.get(d, 0) * k * rest
            n10 += a; n5 += b
            if tw:
                n10tw += a; n5tw += b
        if code in (15, 16) and d.lstrip('-') == '5':
            s5 += k * rest
    rec = dict(label=lab, gauge=g, net10=n10, net5bar=n5, net10_twisted=n10tw, net5bar_twisted=n5tw, scalar5=s5,
               tachyons=int(re.search(r'T_NFIELDS (\d+)', o).group(1)), anomaly_ok=re.search(r'ANOMALY_OK (\d)', o).group(1) == '1')
    res.append(rec)
    print(rec, flush=True)
    json.dump(res, open('gens153.json', 'w'), indent=1)
print('DONE')
