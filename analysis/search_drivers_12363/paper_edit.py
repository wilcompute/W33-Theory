B = chr(92)
p = 'papers/forty_points/sec07_realforms.tex'
s = open(p, encoding='utf-8', newline='').read()
anchor = ("the vertex rule of Pass~11097 is not imposed. " + B + "cert{w33" + B + "_pass12357" + B + "_to" + B + "_12362" + B + "_sub" + B
          + "_orbifolds" + B + "_thresholds" + B + "_vacuum" + B + "_proton.py}")
assert anchor in s, 'anchor'
add = (" Winding sectors settle the small-radius side: feeding the engine constructing elements translated by an odd winding along $e_5$ "
       "(controls: winding is invisible without the Wilson line, and even winding reproduces zero winding) gives $42$ level-matched tachyons "
       "for SM" + B + "_2913, so it is tachyonic for $R_5<" + B + "sqrt{2" + B + "alpha'/3}$ as well as for $R_5>" + B + "sqrt{3" + B + "alpha'/8}$: "
       "no radius is tachyon-free. Across the $99$ parents, $18$ are clean at every radius (twisted channels), none with three generations. "
       "The other three-generation lineages fail differently: SM" + B + "_2618 keeps $12$ fractional-charge fermions massless at every order "
       "(an exact lattice obstruction), SM" + B + "_574 admits no three-generation hypercharge (exact search, with a control that recovers "
       "SM" + B + "_2913's), and SM" + B + "_1105 carries hidden-$SU(3)$ doublets that are chiral for every hypercharge. On this sample the "
       "non-supersymmetric $" + B + "mathbb Z_6$-II route has no viable three-generation model. "
       + B + "cert{w33" + B + "_pass12363" + B + "_to" + B + "_12368" + B + "_all" + B + "_radius" + B + "_closure" + B + "_z6ii.py}")
s = s.replace(anchor, anchor + add, 1)
open(p, 'w', encoding='utf-8', newline='').write(s)
q = 'papers/forty_points/appA_ledger.tex'
t = open(q, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in t else '\n'
row = t.split(nl)
i = next(k for k, l in enumerate(row) if l.startswith('12357--12362'))
row.insert(i + 1, "12363--12368: winding sectors make SM" + B + "_2913 tachyonic at every $R_5$; all-radius census (18/99 clean, none 3-gen); "
           "SM" + B + "_2618 fractional charges massless at all orders; SM" + B + "_574 no 3-gen hypercharge; SM" + B + "_1105 Y-independent chiral "
           "exotics: route closed on this sample & " + B + "tierC & " + B + "cert{w33" + B + "_pass12363" + B + "_to" + B + "_12368" + B + "_all" + B
           + "_radius" + B + "_closure" + B + "_z6ii.py}" + B + B)
open(q, 'w', encoding='utf-8', newline='').write(nl.join(row))
print('ok')
