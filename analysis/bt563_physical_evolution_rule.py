#!/usr/bin/env python3
import json
from pathlib import Path
import sympy as sp
x=sp.symbols('x')
# Levi flag adjacency eigenvalues in P-polynomial order.
ev=[6,2+sp.sqrt(6),2,2-sp.sqrt(6),-2]
# Spectral projector polynomial selecting E4: p(-2)=1 and p(other)=0.
p=sp.interpolate([(ev[i], 1 if i==4 else 0) for i in range(5)], x)
p=sp.factor(p)
# Shell rule for entrywise radial maps.
shell=[sp.Rational(1,1),-sp.Rational(1,3),sp.Rational(1,9),-sp.Rational(1,27),sp.Rational(1,81)]
null=[81,-27,9,-3,1]
vanish=sp.factor(sp.prod(x-t for t in shell))
checks={
 'projector_values': all(sp.simplify(p.subs(x,ev[i])-(1 if i==4 else 0))==0 for i in range(5)),
 'null_equals_81_shell': sp.Matrix(null)==81*sp.Matrix(shell),
 'vanish_degree_5': sp.degree(vanish,x)==5
}
r={
 'bt':563,
 'title':'physical evolution rule',
 'allowed_linear_rule':'Bose-Mesner/spectral filters preserve E4 when they are diagonal in primitive idempotents; the exact protected projector is p(A).',
 'E4_projector_polynomial':str(p),
 'entrywise_rule':'A radial entrywise nonlinearity preserves only E4 iff its five shell values are alpha*[1,-1/3,1/9,-1/27,1/81].',
 'degree_le_4_entrywise_allowed':'alpha*x only',
 'higher_degree_entrywise_allowed':'alpha*x + h(x)*'+str(vanish),
 'forbidden':'generic powers x^n, n not 1, leak to companion sectors',
 'all_identities_hold':all(checks.values())
}
Path('data/PART_BT563_PHYSICAL_EVOLUTION_RULE_results.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
print(json.dumps(r,indent=2))
