#!/usr/bin/env python3
import json
from pathlib import Path
import sympy as sp

x=sp.symbols('x')
r6=sp.sqrt(6)
ev=[6,2+r6,2,2-r6,-2]
labels=['E0_uniform','E1_24_plus','E2_30','E3_24_minus','E4_H1_81']
mult=[1,24,30,24,81]

def interp(vals):
    return sp.factor(sp.interpolate([(ev[i], vals[i]) for i in range(5)], x))

projectors={labels[i]: str(interp([1 if j==i else 0 for j in range(5)])) for i in range(5)}
E4=interp([0,0,0,0,1])
companion=interp([0,1,1,1,0])
leak_kill_keep_uniform=interp([1,0,0,0,1])
annihilate_E4=interp([1,1,1,1,0])
all_but_uniform=interp([0,1,1,1,1])

# Spectral filters are arbitrary functions on the five eigenvalues.
# Preserving E4 as an invariant subspace is automatic for any Bose-Mesner filter;
# isolating E4 imposes f(ev_i)=0 for i<4.  Annihilating leakage companion imposes
# f(ev_1)=f(ev_2)=f(ev_3)=0.
checks={
    'E4_values': [sp.simplify(E4.subs(x,e)) for e in ev] == [0,0,0,0,1],
    'companion_values': [sp.simplify(companion.subs(x,e)) for e in ev] == [0,1,1,1,0],
    'leak_kill_keep_uniform_values': [sp.simplify(leak_kill_keep_uniform.subs(x,e)) for e in ev] == [1,0,0,0,1],
    'annihilate_E4_values': [sp.simplify(annihilate_E4.subs(x,e)) for e in ev] == [1,1,1,1,0],
    'all_but_uniform_values': [sp.simplify(all_but_uniform.subs(x,e)) for e in ev] == [0,1,1,1,1]
}
result={
    'bt':566,
    'title':'Allowed evolution algebra',
    'eigenvalues':[str(e) for e in ev],
    'sectors':labels,
    'multiplicities':mult,
    'primitive_projector_polynomials':projectors,
    'protected_E4_projector':str(E4),
    'companion_24_30_24_projector':str(companion),
    'leakage_killer_keep_uniform_and_E4':str(leak_kill_keep_uniform),
    'E4_annihilator_keep_companion_and_uniform':str(annihilate_E4),
    'uniform_annihilator_keep_all_nonuniform':str(all_but_uniform),
    'classification':'Bose-Mesner filters are all degree <=4 polynomials in A. Any such filter preserves E4 as an invariant eigenspace. Exact E4 isolation is the protected_E4_projector. Exact cubic-leakage removal while retaining uniform+E4 is leakage_killer_keep_uniform_and_E4.',
    'physical_rule':'Allowed linear evolution is spectral/Bose-Mesner diagonal. Forbidden pointwise nonlinear evolution is governed separately by the five-shell selection rule from BT560/BT563.',
    'all_identities':{k:bool(v) for k,v in checks.items()},
    'all_identities_hold':all(bool(v) for v in checks.values())
}
Path('data/PART_BT566_ALLOWED_EVOLUTION_ALGEBRA_results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
