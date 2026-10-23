"""12229: the 58 three-generation twisted-10 models: every scalar SU(5) representation they carry (any sector).  SU(5) can be broken
to the Standard Model in field theory only by a scalar in the 10 (flipped) or the 24 / larger representations; 5s and singlets
cannot do it."""
import json, re, subprocess
from collections import Counter
g = [x for x in json.load(open('../search_drivers_12223/gens153.json')) if abs(x['net10']) == 3 and abs(x['net5bar']) == 3]
res = []
allreps = Counter()
for x in g:
    sh = ('cd ~/orb/nsobuild && export LD_LIBRARY_PATH=/tmp/su9/lib:$HOME/orb/sysroot/usr/lib/x86_64-linux-gnu; '
          'timeout 900 ./nsodump /mnt/c/tmp/toe_round/stype/cand10/%s.txt 2>/dev/null' % x['label'])
    o = subprocess.run(['wsl', '-e', 'bash', '-lc', sh], capture_output=True, text=True).stdout
    facs = [f.strip() for f in re.search(r'GAUGE (.*)', o).group(1).split(' and ')[0].split(' NU1')[0].split('+')]
    i = facs.index('A4')
    reps = Counter()
    for mm in re.finditer(r'^F m=(\d+) k=\S+ m=\S+ n=\S+ dim=(\S+) x(\d+)', o, re.M):
        if int(mm.group(1)) in (15, 16, 17, 18):
            reps[mm.group(2).split(',')[i].lstrip('-')] += int(mm.group(3))
    res.append(dict(label=x['label'], scalar_su5_reps=dict(reps)))
    allreps.update(reps)
    print(x['label'], dict(reps), flush=True)
json.dump(dict(models=len(res), union=dict(allreps), per_model=res), open('vet58.json', 'w'), indent=1)
print('UNION', dict(allreps))
