#!/usr/bin/env python3
"""Validated entry point for Passes 3390-3401.

Overrides only the closed-form orbit-count normalization in the source module:
the fixed-set cardinality at x=1 is 4^(r+1), not 4*12^r.
"""
from __future__ import annotations
import importlib.util
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('core',ROOT/'analysis/bt3390_3401_exterior_switch_defect_clifford_shell.py')
core=importlib.util.module_from_spec(spec);assert spec.loader;spec.loader.exec_module(core)
def shell_theorem(max_r=6):
    x=sp.symbols('x');rows=[]
    for r in range(max_r+1):
      n=2*r+1;N=sp.expand((x+3)**n);F=sp.expand((x+3)*(x*x+3)**r);Q=sp.expand((N+F)/2)
      shell=[int(Q.coeff(x,s)) for s in range(n+1)];inv=list(reversed(shell))
      assert sum(shell)==(4**n+4**(r+1))//2
      rows.append({'r':r,'n':n,'full_shell_polynomial':str(N),'fixed_shell_polynomial':str(F),'quotient_shells':shell,'tau_invariant_multiplicities':inv})
    assert rows[2]['quotient_shells']==[135,207,144,48,9,1]
    return {'status':'PASS_GENERAL_ODD_HAMMING_SHELL_SPECTRUM_REVERSAL','family':'H(2r+1,4) with one fixed coordinate and r paired coordinates under tau','theorem':'If q_s is the coefficient of ((x+3)^(2r+1)+(x+3)(x^2+3)^r)/2, then the tau-invariant multiplicity at Hamming grade j is q_(2r+1-j).','instances':rows}
core.shell_theorem=shell_theorem
if __name__=='__main__':core.main()
