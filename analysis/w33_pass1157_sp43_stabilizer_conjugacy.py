#!/usr/bin/env python3
"""
Pass 1157 (Step 5): Sp(4,3) 432-orbit stabilizer exact algebraic analysis.
|Sp(4,3)| = 25920, orbit = 432, so stabilizer order = 60.
Most likely isomorphism type: A5 = PSL(2,5) [GAP IdGroup 60,5].
Writes GAP script analysis/w33_sp43_stabilizer.g for local execution.
Outputs: data/SP43_STABILIZER_2026_07_27.json
"""
import json, pathlib
from datetime import datetime
SP43_ORDER = 25920
ORBIT_SIZE = 432
STABILIZER_ORDER = SP43_ORDER // ORBIT_SIZE
ORDER_60_CANDIDATES = [
    {'name': 'A5',    'gap_id': [60,5],  'simple': True,  'abelian': False, 'note': 'Most natural for Sp(4,3)'},
    {'name': 'C60',   'gap_id': [60,1],  'simple': False, 'abelian': True,  'note': 'Cyclic; unlikely'},
    {'name': 'D30',   'gap_id': [60,3],  'simple': False, 'abelian': False, 'note': 'Dihedral'},
    {'name': 'A4xC5', 'gap_id': [60,4],  'simple': False, 'abelian': False, 'note': 'Solvable'},
]
GAP_SCRIPT = '''# GAP script: w33_sp43_stabilizer.g
# Identifies the stabilizer of a 432-orbit in Sp(4,3)
# Run: gap -q analysis/w33_sp43_stabilizer.g
G := Sp(4,3);
Print("Order: ", Order(G), "\\n");
Pts := Orbit(G, [Z(3)^0,0*Z(3),0*Z(3),0*Z(3)], OnLines);
Pairs := Combinations([1..Length(Pts)],2);
orbs := Orbits(G, Pairs, function(p,g)
  return Set([Position(Pts,Pts[p[1]]^g),Position(Pts,Pts[p[2]]^g)]); end);
stabs := [];
for orb in orbs do
  if Length(orb) = 432 then
    stab := Stabilizer(G, orb[1], function(p,g)
      return Set([Position(Pts,Pts[p[1]]^g),Position(Pts,Pts[p[2]]^g)]); end);
    Print("Stabilizer order: ", Order(stab), "\\n");
    Print("IdGroup: ", IdGroup(stab), "\\n");
    Print("IsSimple: ", IsSimple(stab), "\\n");
    Print("Element orders: ", Collected(List(Elements(stab),Order)), "\\n");
    Add(stabs, stab);
  fi;
od;
if Length(stabs) >= 2 then
  for i in [1..Length(stabs)-1] do for j in [i+1..Length(stabs)] do
    x := RepresentativeAction(G, stabs[i], stabs[j], OnPoints);
    if x<>fail then Print("Stabs ",i," and ",j," ARE conjugate.\\n");
    else Print("Stabs ",i," and ",j," NOT conjugate.\\n"); fi;
  od; od;
fi;
Print("Done.\\n");
'''
def main():
    assert STABILIZER_ORDER == 60
    report = {'timestamp': datetime.utcnow().isoformat()+'Z',
        'schema': 'w33.pass1157.sp43_stabilizer_conjugacy.v1', 'status': 'PREPARED',
        'sp43_group_order': SP43_ORDER, 'orbit_size': ORBIT_SIZE,
        'stabilizer_order': STABILIZER_ORDER,
        'order_60_candidates': ORDER_60_CANDIDATES,
        'most_likely': 'A5 [60,5] -- simple, non-abelian, known to embed in Sp(4,3)',
        'next_action': 'Execute analysis/w33_sp43_stabilizer.g in GAP.',
        'typing_rule': 'Sp(4,3) carrier is typed separately from W(E6)/S5 carrier.'}
    out = pathlib.Path('data/SP43_STABILIZER_2026_07_27.json')
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=2))
    pathlib.Path('analysis/w33_sp43_stabilizer.g').write_text(GAP_SCRIPT)
    print('PASS 1157 stabilizer order:', STABILIZER_ORDER, '| GAP script written')
    return report
if __name__ == '__main__': main()
