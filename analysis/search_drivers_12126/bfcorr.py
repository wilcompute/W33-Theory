import re, glob, json, os
BOS, FER = {8, 9, 13, 14, 15, 16, 17, 18}, {19, 20}
def count(t):
    b = f = 0
    for m in re.finditer(r'^F m=(\d+) k=\S+ m=\S+ n=\S+ dim=([^ ]*) x(\d+)', t, re.M):
        c, k = int(m.group(1)), int(m.group(3))
        for e in m.group(2).split(','):
            if e:
                k *= int(re.match(r'-?(\d+)', e).group(1))
        b += k if c in BOS else 0
        f += k if c in FER else 0
    nu1 = int(re.search(r'NU1 (\d+)', t).group(1))
    return b, f, nu1
out = {}
files = glob.glob(r'C:\tmp\toe_wt\analysis\search_drivers_12116\smwl\*.out') + glob.glob(r'C:\tmp\toe_wt\analysis\search_drivers_12121\smwl3\*.out') \
    + [r'C:\tmp\toe_wt\analysis\search_drivers_12111\%s_9.out' % b for b in ['N001_F1_04', 'N004_F1_03', 'N004_F1_04', 'N004_F1_05', 'N008_F1_02', 'N008_F1_03', 'N008_F1_04']] \
    + [r'C:\tmp\toe_wt\analysis\search_drivers_12111\control_z3_nsodump.out']
for fn in files:
    t = open(fn).read()
    if 'GAUGE' not in t:
        continue
    b, f, nu1 = count(t)
    out[os.path.basename(fn)[:-4]] = dict(NB=b, NF=f, NU1=nu1, old=b - f, corrected=b + 2 * nu1 - f)
v = [x['corrected'] for k, x in out.items() if not k.endswith('_9') and not k.startswith('control')]
print(len(v), min(v), max(v))
print({k: (x['old'], x['corrected']) for k, x in out.items() if k.endswith('_9') or k.startswith('control') or k in ('N004_F1_03_S002', 'N008_F1_03_S033', 'N008_F1_04_S037', 'N008_F1_02_S053', 'N008_F1_04_S037_T115')})
json.dump(out, open(r'C:\tmp\toe_round\stype\bfcorr.json', 'w'), indent=1)
