import re
from collections import Counter

D = r'C:\tmp\toe_wt\analysis\search_drivers_12111'
BOS = {8, 9, 13, 14, 15, 16, 17, 18}
FER = {19, 20}


def dimprod(dims):
    w = 1
    for e in dims:
        w *= int(re.match(r'-?(\d+)', e).group(1))
    return w


def count(text):
    b = f = 0
    codes = Counter()
    for m in re.finditer(r'^F m=(\d+) k=\S+ m=\S+ n=\S+ dim=([^ ]+) x(\d+)', text, re.M):
        c, dims, k = int(m.group(1)), m.group(2).split(','), int(m.group(3))
        n = k * dimprod(dims)
        codes[c] += n
        if c in BOS:
            b += n
        elif c in FER:
            f += n
    return b, f, dict(codes)


for lab in ['control_z3_nsodump'] + ['N001_F1_04', 'N004_F1_03', 'N004_F1_04', 'N004_F1_05', 'N008_F1_02', 'N008_F1_03', 'N008_F1_04']:
    fn = D + '\\' + (lab + '.out' if lab.startswith('control') else lab + '_9.out')
    b, f, codes = count(open(fn).read())
    print(lab, 'N_B', b, 'N_F', f, 'N_B - N_F', b - f, codes)
