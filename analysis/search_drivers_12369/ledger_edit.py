B = chr(92)
q = 'papers/forty_points/appA_ledger.tex'
t = open(q, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in t else '\n'
row = t.split(nl)
i = next(k for k, l in enumerate(row) if l.startswith('12363--12368'))
row.insert(i + 1, "12369--12372: finite premetric closure theorem on $" + B + "Lambda^2" + B + "mathbb F_3^4$ (all 16848 solutions of $" + B
           + "kappa^2=-1$ are elliptic Hodge stars); quantum $J$ (540, hyperbolic) and light cones (elliptic) never share a metric; no duality "
           "fixes $" + B + "omega$; shared contexts 16/10 by the null invariant; Dirac-QCA checks & " + B + "tierC & " + B + "cert{w33" + B
           + "_pass12369" + B + "_to" + B + "_12372" + B + "_information" + B + "_duality.py}" + B + B)
open(q, 'w', encoding='utf-8', newline='').write(nl.join(row))
print('ok')
