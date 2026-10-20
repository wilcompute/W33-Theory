import re, glob, json, os
BOS, FER = {8, 9, 13, 14, 15, 16, 17, 18}, {19, 20}
def nbnf(t):
    b = f = 0
    for m in re.finditer(r'^F m=(\d+) k=\S+ m=\S+ n=\S+ dim=([^ ]*) x(\d+)', t, re.M):
        c, dims, k = int(m.group(1)), m.group(2).split(','), int(m.group(3))
        n = k
        for e in dims:
            if e:
                n *= int(re.match(r'-?(\d+)', e).group(1))
        b += n if c in BOS else 0
        f += n if c in FER else 0
    return b, f
out = {}
for fn in sorted(glob.glob(r'C:\tmp\toe_wt\analysis\search_drivers_12116\smwl\*.out') + glob.glob(r'C:\tmp\toe_round\stype\smwl3\*.out')):
    t = open(fn).read()
    if 'GAUGE' not in t:
        continue
    b, f = nbnf(t)
    out[os.path.basename(fn)[:-4]] = [b, f, b - f]
key = ['N004_F1_03_S002', 'N008_F1_03_S033', 'N008_F1_04_S037', 'N008_F1_02_S053', 'N008_F1_04_S037_T115']
print({k: out[k] for k in key})
d = [v[2] for v in out.values()]
print(len(d), 'min', min(d), 'max', max(d), 'zero', sum(x == 0 for x in d), 'positive', sum(x > 0 for x in d))
json.dump(out, open(r'C:\tmp\toe_round\stype\bf2.json', 'w'), indent=1)
