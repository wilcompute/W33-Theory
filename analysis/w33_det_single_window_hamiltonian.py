#!/usr/bin/env python3
"""Single-window analog Hamiltonian for the controlled determinant gate.

Parent identity over F3:
  det X = 2[(tr X^2)^2 + tr X^4].

Let A(X) be the reduced integer representative 0,1,2 of
  (tr X^2)^2 + tr X^4 mod3,
and let Z_L have eigenvalues r=+1,-1 on the doubled central-character rails.

Then
  H_det = -(4 pi hbar / 3T) A(X) tensor Z_L
gives
  exp(-i H_det T/hbar)|X,r>
   = exp(i 4 pi r A(X)/3)|X,r>
   = omega^(r det X)|X,r>
   = U_det|X,r>.

Because q2^2 and q4 are commuting diagonal controller observables, hardware
that couples to their sum needs one analog interaction window rather than two
sequential invariant-phase gates.

This is an exact Hamiltonian synthesis theorem.  It does not identify a
material interaction whose microscopic Hamiltonian is A(X) tensor Z_L.

A simple timing/coupling planning bound is included: the largest unreduced
phase slope occurs at A=2, so a fractional pulse-area error eps creates phase
error <= (8 pi/3)|eps|.  Requiring <=0.1 rad gives |eps|<=1.194%.
"""
from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_det_single_window_hamiltonian.json'

def main(write=True):
    parent=json.loads((ROOT/'data/w33_controlled_det_two_invariant_compiler.json').read_text())
    assert parent['status']=='PASS_TWO_PRIMITIVE_RICH_LIBRARY'
    eps=0.1*3/(8*math.pi)
    # exact table for all A in F3 and r=+-1
    table=[]
    for A in range(3):
        det=(2*A)%3
        for r in (1,-1):
            # exponents agree modulo 3: 2*r*A == r*det
            assert (2*r*A-r*det)%3==0
            table.append({'A':A,'r':r,'det_mod3':det,'phase_exponent_mod3':(r*det)%3})
    out={'schema':'w33.det_single_window_hamiltonian.v1',
      'status':'PASS_EXACT_ANALOG_SYNTHESIS__MICROSCOPIC_COUPLING_OPEN',
      'observable':'A(X)=((tr X^2)^2+tr X^4) mod3, represented by eigenvalues 0,1,2',
      'logical_operator':'Z_L eigenvalues r=+1,-1',
      'hamiltonian':'H_det=-(4*pi*hbar/(3T))*A(X) tensor Z_L',
      'evolution':'exp(-i H_det T/hbar)=U_det',
      'phase_table':table,
      'resource_comparison':{
        'native_monomial_phases':17,
        'sequential_invariant_phases':2,
        'simultaneous_analog_windows':1},
      'planning':{
        'worst_phase_slope_rad_per_fractional_area_error':'8*pi/3',
        'max_fractional_pulse_area_error_for_0.1rad':eps,
        'percent':100*eps},
      'physics_boundary':'Need a microscopic interaction or ancilla-mediated effective Hamiltonian proportional to A(X) tensor Z_L. Exact algebra alone does not supply that coupling.',
      'checks':{'parent_loaded':True,'all_A_r_phase_exponents_match':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
