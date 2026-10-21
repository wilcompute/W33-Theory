import os, sys, json
os.environ['QUINTIC'] = '1'; os.environ['EXACT'] = '1'
import numpy as np
from collections import Counter
from scipy.sparse.csgraph import maximum_bipartite_matching
from scipy.sparse import csr_matrix
src = open('exomass5.py').read().replace("        M5t = M3 + 0.1 * M4 + 0.01 * M5", "        M5t = M3 + 0.1 * M4 + 0.01 * M5\n        if key[1] == 2:\n            DBG.append((key, A, B, M5t))").split("if __name__ == '__main__':")[0]
DBG = []
exec(src)
hy = json.load(open('hyper3_4.json'))
run('N008_F1_04_S037_T115', hy['N008_F1_04_S037_T115']['y_good'])
key, A, B, M = DBG[0]
pat = (np.abs(M) > 0)
nA, nB = pat.shape
# matching columns -> rows
mc = maximum_bipartite_matching(csr_matrix(pat.T.astype(int)), perm_type='column')   # for each column (B index) the matched row
unc = [j for j in range(nB) if mc[j] < 0]
rowmatch = {mc[j]: j for j in range(nB) if mc[j] >= 0}
ZC, ZR, st = set(unc), set(), list(unc)
while st:
    j = st.pop()
    for i in np.nonzero(pat[:, j])[0]:
        if i not in ZR:
            ZR.add(int(i))
            if i in rowmatch and rowmatch[i] not in ZC:
                ZC.add(rowmatch[i]); st.append(rowmatch[i])
lab = lambda u: dict(field=u['f']['i'], sector=(u['f']['n'], u['f']['mm']), fp=[int((u['f']['lat'][2*t] + u['f']['lat'][2*t+1]) % 3) for t in range(3)], dim=u['f']['dim'])
out = dict(deficient_columns=[lab(B[j]) for j in sorted(ZC)], their_rows=[lab(A[i]) for i in sorted(ZR)],
           other_rows=[lab(A[i]) for i in range(nA) if i not in ZR], other_cols=[lab(B[j]) for j in range(nB) if j not in ZC])
print('|Z_C| =', len(ZC), ' |N(Z_C)| =', len(ZR))
for k, v in out.items():
    print(k, [(d['field'], d['sector'], d['fp']) for d in v])
json.dump(out, open('block.json', 'w'), indent=1, default=str)
