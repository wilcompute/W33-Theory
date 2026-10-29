B = chr(92)
q = 'papers/forty_points/appA_ledger.tex'
t = open(q, encoding='utf-8', newline='').read(); nl = '\r\n' if '\r\n' in t else '\n'; row = t.split(nl)
i = next(k for k, l in enumerate(row) if l.startswith('12373--12376'))
row.insert(i + 1, "12402--12409: closure $" + B + "kappa^2=-1$ is metric for every odd $q$ (elliptic iff $q" + B + "equiv3$ mod 4; Urbantke sampling + group orders); "
           "Stab$(J)=GU(2,3)$ with derived $SL(2,3)$, a light cone leaves $Z_4$; constants as counting/transfer exchange rates (Shannon = Landauer, "
           "Smarr in bits, $" + B + "alpha=Z_0/2R_K$) & " + B + "tierC & " + B + "cert{w33" + B + "_pass12402" + B + "_to" + B + "_12409" + B
           + "_closure" + B + "_all" + B + "_q" + B + "_joint" + B + "_symmetry" + B + "_constants.py}" + B + B)
open(q, 'w', encoding='utf-8', newline='').write(nl.join(row)); print('ok')
