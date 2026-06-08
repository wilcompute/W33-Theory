#!/usr/bin/env python3
import json
from pathlib import Path
import sympy as sp
s=sp.sqrt(6)
H=[sp.Rational(17205568,243),
   -sp.Rational(734384,2187)*(-244+9*s),
   sp.Rational(177720928,2187),
   sp.Rational(734384,2187)*(9*s+244),
   sp.Rational(1751954560,19683)]
m=[1,24,30,24,81]
T=[sp.simplify(H[i]*m[i]) for i in range(5)]
checks={
 'pair_ratio': sp.simplify((H[1]+H[3])/H[2])==sp.Rational(244,121),
 'pair_diff': sp.simplify(H[3]-H[1])==sp.Rational(1468768,243)*s,
 'trace_total': sp.simplify(sum(T))==sp.Integer(13651200),
 'trace_pair_ratio': sp.simplify((T[1]+T[3])/T[2])==sp.Rational(976,605)
}
r={
 'bt':562,
 'title':'Levi cubic leakage sector ratios',
 'coefficients':[str(sp.factor(x)) for x in H],
 'multiplicities':m,
 'trace_weights':[str(sp.factor(x)) for x in T],
 'pair_sum_E1_E3':str(sp.factor(H[1]+H[3])),
 'pair_diff_E3_minus_E1':str(sp.factor(H[3]-H[1])),
 'ratio_E1_plus_E3_over_E2':'244/121',
 'trace_ratio_E1_plus_E3_over_E2':'976/605',
 'total_trace':'13651200',
 'interpretation':'The conjugate 24-sector leakage pair is locked to the 30-sector by 244/121; the cubic leak is structured, not random.',
 'all_identities_hold':all(checks.values())
}
Path('data/PART_BT562_LEAKAGE_SECTOR_RATIOS_results.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
print(json.dumps(r,indent=2))
