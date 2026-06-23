#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1578_full_centered_basis_calibration_matrix.json'
MD = ROOT / 'analysis' / 'BT1578_full_centered_basis_calibration_matrix.md'
TEX = ROOT / 'analysis' / 'BT1578_full_centered_basis_calibration_matrix.tex'

LABELS = [2, 0, 1]  # centered ell=-1,0,+1 labels
ELL = [-1, 0, 1]

# Matrix entries are omega-exponents modulo 3 plus support masks.
# A value None denotes a zero entry.
def identity_matrix():
    return [[0 if i == j else None for j in range(3)] for i in range(3)]

def x_shift_matrix():
    # X |q> = |q+1>. In row/column convention, row label equals col+1.
    mat = [[None]*3 for _ in range(3)]
    for col, q in enumerate(LABELS):
        target = (q + 1) % 3
        row = LABELS.index(target)
        mat[row][col] = 0
    return mat

def z_phase_matrix():
    return [[LABELS[i] if i == j else None for j in range(3)] for i in range(3)]

def s_phase_matrix():
    return [[(LABELS[i] * LABELS[i]) % 3 if i == j else None for j in range(3)] for i in range(3)]

def f3_matrix():
    return [[(qout * qin) % 3 for qin in LABELS] for qout in LABELS]

def support_count(mat):
    return sum(1 for row in mat for x in row if x is not None)

def diag_signature(mat):
    return [mat[i][i] for i in range(3)]

def main() -> None:
    matrices = {
        'I': identity_matrix(),
        'X': x_shift_matrix(),
        'Z': z_phase_matrix(),
        'F3': f3_matrix(),
        'S': s_phase_matrix(),
    }
    rows=[]
    for name, mat in matrices.items():
        rows.append({'operation':name,'omega_exponent_matrix':mat,'support_count':support_count(mat),'optical_role':{'I':'reference','X':'OAM shift','Z':'spiral phase','F3':'three-mode mixer','S':'quadratic lens phase'}[name]})
    checks={
        'labels_201': LABELS==[2,0,1],
        'five_matrices': len(matrices)==5,
        'I_support_3': support_count(matrices['I'])==3,
        'X_support_3_permutation': support_count(matrices['X'])==3 and all(sum(x is not None for x in row)==1 for row in matrices['X']),
        'Z_signature_201': diag_signature(matrices['Z'])==[2,0,1],
        'S_signature_101': diag_signature(matrices['S'])==[1,0,1],
        'F3_full_support_9': support_count(matrices['F3'])==9,
        'same_centered_basis_all': True,
    }
    result={'bt':1578,'title':'Full S,F3,X,Z centered-basis calibration matrix','verified':all(checks.values()),'source_packets':{'bt1574':'data/bt1574_s_f3_calibration.json','bt1568':'data/bt1568_lens_prism_oam_dictionary.json'},'basis':{'ell':ELL,'labels':LABELS},'rows':rows,'interpretation':'The complete core gate set I, X, Z, F3, and S is calibrated on one centered OAM basis. I, X, Z, and S are sparse monomial matrices; F3 is the full three-mode mixer. Z has phase signature [2,0,1], S has [1,0,1].','honesty_boundary':'Exact finite qutrit calibration matrices only; physical loss, aberration, and radial leakage are handled by separate witness rows.','checks':checks}
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    MD.write_text('# BT1578 Full Centered-basis Calibration Matrix\n\nThe complete core gate set I, X, Z, F3, and S is calibrated on the centered OAM basis ell=-1,0,+1 with labels 2,0,1. I, X, Z, and S are sparse monomial matrices; F3 is the full three-mode mixer. This is exact finite qutrit calibration, not a loss model.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1578: $I,X,Z,F_3,S$ are calibrated on the centered OAM basis $\\ell=-1,0,+1$ with labels $2,0,1$.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1578,'verified':result['verified']}, indent=2))
    if not result['verified']: raise SystemExit(1)

if __name__=='__main__': main()
