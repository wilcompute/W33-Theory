"""An exact time-reversal firewall for the proposed W33 edge-current energy.

This tests canonical complex-conjugation time reversal on L2(W): q -> q,
p -> -p. It does not rule out a different antiunitary symmetry involving
an internal transformation, nor establish physical CP violation.
"""
from __future__ import annotations
import json
from fractions import Fraction
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass11767_global_current_algebra import actual_edges

def certificate():
    edges = actual_edges()
    assert len(edges) == 160 and len(set(edges)) == 160
    pencils = [set() for _ in range(40)]
    for pt, line in edges:
        assert 0 <= pt < 40 and 40 <= line < 80
        pencils[pt].add(line - 40)
    assert all(len(lines) == 4 for lines in pencils)
    assert all(sum(l in x for x in pencils) == 4 for l in range(40))
    checks = 0
    sample = None
    for p0 in range(40):
        for p1 in range(40):
            if p0 == p1:
                continue
            first = min(pencils[p0] - pencils[p1])
            second = min(pencils[p1] - pencils[p0])
            q = [0]*40
            r = [0]*40
            q[p0], q[p1] = 1, -1
            r[first], r[second] = 1, -1
            # In the source current J_e=(V_e.q+a)(U_e.p+a),
            # a=1/sqrt(20). Set q=a*(e_p0-e_p1),
            # p=a*(e_l0-e_l1); the P_W projections act identically
            # on these zero-sum vectors.
            h_plus = sum((1+q[i])**2 * (1+r[j-40])**2 for i,j in edges)
            h_minus = sum((1+q[i])**2 * (1-r[j-40])**2 for i,j in edges)
            assert h_plus - h_minus == 16
            assert Fraction(h_plus-h_minus,400) == Fraction(1,25)
            checks += 1
            if sample is None:
                sample = dict(points=[p0,p1], lines=[first,second],
                              H_num=h_plus, H_time_reversed_num=h_minus)
    return {
        "schema":"w33.20261008.bare_T_current_firewall.v1",
        "status":"PASS",
        "source":"analysis/w33_pass11769_quantized_current_vacuum.py",
        "parent_incidence":"analysis/w33_pass11767_global_current_algebra.py",
        "ordered_point_pairs_checked":checks,
        "incidences":len(edges),
        "point_degrees":4,
        "line_degrees":4,
        "exact_symbol_energy_difference":"H(q,p)-H(q,-p)=1/25",
        "operator_identity":"H-KHK^(-1)=4*a*sum_e (V_e.q+a)^2*(U_e.p); a=1/sqrt(20)",
        "witness_rule":"for each distinct p0,p1 choose l0 through p0 but not p1 and l1 through p1 but not p0; q=a*(e_p0-e_p1), p=a*(e_l0-e_l1)",
        "sample":sample,
        "gaussian_orientation":"E(t,f)-E(t,-f)=1280*b*m*f*t; b=1/20, m=(6*sqrt(10)+15)/40",
        "scope":"Canonical K time reversal only. A nonzero symbol difference proves the differential operator is not invariant under K; not a complete antiunitary-symmetry classification, not observed CP violation or an emergent arrow of time."
    }

if __name__ == "__main__":
    result=certificate()
    print(json.dumps(result, indent=2))
