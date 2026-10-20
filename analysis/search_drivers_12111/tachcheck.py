import json
import re
import subprocess

res = json.load(open(r'C:\tmp\toe_round\stype\nswl_fam.json'))
good = [r for r in res if r['gauge'] != 'LOADFAIL']
out = []
for r in good:
    lab = r['label']
    t = open(r'C:\tmp\toe_round\stype\nswl\%s.txt' % lab).read().replace('\r', '')
    head, rest = t.split('Shifts and Wilsonlines:')
    rows = rest.split('end model')[0].strip().split('\n')
    z = ' '.join(['0/1'] * 16)
    rows9 = rows[:2] + [z] + rows[2:]
    head = head.replace('Geometry/Geometry_Z3_1_1_N0.txt', 'Geometry/Geometry_Z3_1_1.txt')
    t9 = head + 'Shifts and Wilsonlines:\n' + '\n'.join(rows9) + '\nend model\n'
    fn = r'C:\tmp\toe_round\stype\nswl\%s_9.txt' % lab
    open(fn, 'w', newline='\n').write(t9)
    sh = ('cd ~/orb/nsobuild && export LD_LIBRARY_PATH=/tmp/su9/lib:$HOME/orb/sysroot/usr/lib/x86_64-linux-gnu; '
          'timeout 900 ./nsodump /mnt/c/tmp/toe_round/stype/nswl/%s_9.txt 2>/dev/null' % lab)
    o = subprocess.run(['wsl', '-e', 'bash', '-lc', sh], capture_output=True, text=True).stdout
    open(fn.replace('_9.txt', '_9.out'), 'w', newline='\n').write(o)
    g = re.search(r'GAUGE (.*)', o)
    tn = re.search(r'T_NFIELDS (\d+)', o)
    fn_ = re.search(r'F_NFIELDS (\d+)', o)
    an = re.search(r'ANOMALY_OK (\d)', o)
    net = 0
    for m in re.finditer(r'^F m=(\d+) k=\S+ m=\S+ n=\S+ dim=([^ ]+) x(\d+)', o, re.M):
        mult, dims, k = int(m.group(1)), m.group(2).split(','), int(m.group(3))
        if mult != 2:
            continue
        for pos, d in enumerate(dims):
            if d.lstrip('-') == '16':
                w = 1
                for q, e in enumerate(dims):
                    if q != pos:
                        w *= int(re.match(r'-?(\d+)', e).group(1))
                net += (-k * w if d.startswith('-') else k * w)
    out.append(dict(label=lab, gauge=g.group(1) if g else None, net16=net, tachyonic_fields=int(tn.group(1)) if tn else None,
                    fields=int(fn_.group(1)) if fn_ else None, anomaly_ok=an.group(1) if an else None))
    print(out[-1], flush=True)
json.dump(out, open(r'C:\tmp\toe_round\stype\tachcheck.json', 'w'), indent=1)
