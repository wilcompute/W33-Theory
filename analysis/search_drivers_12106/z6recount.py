import json
import re
import subprocess

scan = json.load(open(r'C:\tmp\toe_round\stype\z6scan_3.json'))
out = []
for s in scan:
    if s[2] == 'LOAD FAILED':
        continue
    lab = s[0]
    sh = ('cd $HOME/orb/bin && export LD_LIBRARY_PATH=/tmp/su9/lib:$HOME/orb/sysroot/usr/lib/x86_64-linux-gnu; '
          'printf "load orbifolds(/mnt/c/tmp/toe_round/stype/z6models/%s.txt)\\ncd %s\\ncd spectrum\\nprint summary\\nexit\\nyes\\n" | timeout 600 ./orbifolder' % (lab, lab))
    txt = subprocess.run(['wsl', '-e', 'bash', '-lc', sh], capture_output=True, text=True).stdout
    net = {}
    for m in re.finditer(r'^\s+(\d+) \(([^)]*)\)_l', txt, re.M):
        k = int(m.group(1))
        dims = [int(x) for x in m.group(2).replace(' ', '').split(',')]
        for pos, d in enumerate(dims):
            if abs(d) in (16, 27):
                w = 1
                for q, e in enumerate(dims):
                    if q != pos:
                        w *= abs(e)
                net[(pos, abs(d))] = net.get((pos, abs(d)), 0) + (k * w if d > 0 else -k * w)
    out.append((lab, s[2], {str(k): v for k, v in net.items() if v}))
    print(out[-1], flush=True)
json.dump(out, open(r'C:\tmp\toe_round\stype\z6recount_3.json', 'w'), indent=1)
