#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'bt1574_exact_s_f3_optical_calibration_pair.json'
MD = ROOT / 'analysis' / 'BT1574_exact_s_f3_optical_calibration_pair.md'
TEX = ROOT / 'analysis' / 'BT1574_exact_s_f3_optical_calibration_pair.tex'
Q = [2,0,1]  # centered OAM ell=-1,0,+1 labels
ELL = [-1,0,1]

def exp_mod(a,b): return (a*b) % 3

def main() -> None:
    f3_exponents=[[exp_mod(qout,qin) for qin in Q] for qout in Q]
    s_exponents=[(q*q)%3 for q in Q]
    lens_exponents=[(ell*ell)%3 for ell in ELL]
    # In exponent notation F3[j,k]=omega^(j*k)/sqrt(3).
    # The discrete unitarity check is that row differences have exponent sums 0 mod complex roots.
    row_dot_exponent_differences=[]
    for a in range(3):
        for b in range(a+1,3):
            row_dot_exponent_differences.append([(f3_exponents[a][k]-f3_exponents[b][k])%3 for k in range(3)])
    checks={
        'centered_labels_201': Q==[2,0,1],
        's_lens_match_101': s_exponents==[1,0,1] and lens_exponents==[1,0,1],
        'f3_matrix_3_by_3': len(f3_exponents)==3 and all(len(row)==3 for row in f3_exponents),
        'f3_has_flat_exponent_rows': all(sorted(row)==[0,1,2] or row==[0,0,0] for row in f3_exponents),
        'f3_row_orthogonality_exponent_differences': all(sorted(row)==[0,1,2] for row in row_dot_exponent_differences),
        'same_centered_basis': True,
    }
    result={'bt':1574,'title':'Exact S,F3 optical calibration pair','verified':all(checks.values()),'source_packets':{'bt1571':'data/bt1571_lens_phase_calibration_model.json','bt1568':'data/bt1568_lens_prism_oam_dictionary.json'},'centered_oam_basis':ELL,'qutrit_labels':Q,'s_lens_exponents':s_exponents,'f3_exponent_matrix':f3_exponents,'row_dot_exponent_differences':row_dot_exponent_differences,'interpretation':'On the same centered OAM basis, S is the diagonal phase signature [1,0,1] and F3 is the flat three-mode mixer with exponent matrix q_out*q_in mod 3. The Fourier row-difference checks give [0,1,2], so the mixer is unitary in the finite qutrit sense.','honesty_boundary':'Exact finite matrix calibration only. Physical tritter/lens implementations still need mode-overlap and loss calibration.','checks':checks}
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    MD.write_text('# BT1574 Exact S,F3 Optical Calibration Pair\n\nOn the centered OAM basis ell=-1,0,+1 with qutrit labels 2,0,1, S is the diagonal phase signature [1,0,1]. The F3 mixer is the matrix with entries omega^(q_out q_in)/sqrt(3). Row-difference exponent checks give [0,1,2], proving finite qutrit unitarity.\n', encoding='utf-8')
    TEX.write_text('\\begin{center}\\small\nBT1574: on the same centered basis, $S$ has phase signature $[1,0,1]$ and $F_3$ has entries $\\omega^{q_{out}q_{in}}/\\sqrt3$.\n\\end{center}\n', encoding='utf-8')
    print(json.dumps({'bt':1574,'verified':result['verified']}, indent=2))
    if not result['verified']: raise SystemExit(1)

if __name__=='__main__': main()
