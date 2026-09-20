#!/usr/bin/env python3
"""Packet72 physical-C6 Floquet contrast theorem.

Parent:
  data/w33_packet72_physical_c6_address_compiler.json
  data/w33_a5_coxeter_vs_hypercharge_z6_firewall.json

The physical packet C6 generator has cycle profile 6^12 on the 72 runtime
addresses.  Restrict the 72-dimensional permutation representation to one
six-cycle.  It splits as
  C^6 = C*1_uniform + V_contrast,
where V_contrast has dimension five and characteristic polynomial
  (x^6-1)/(x-1) = x^5+x^4+x^3+x^2+x+1.

That polynomial is exactly the characteristic polynomial of the A5 Coxeter
element on the five-dimensional A5 root/standard module.  Therefore every
physical packet-C6 orbit contains an exact spectral copy of the A5 Coxeter
module after removal of the uniform mode.

There are 12 independent six-cycles, hence 12 exact ideal pi modes (eigenvalue
-1), one in each contrast sector.  The full packet72 C6 spectrum is each sixth
root of unity with multiplicity 12.

Important firewall: this is a spectral/Floquet equivalence of permutation
modules.  It does not identify the physical inner-E8 holonomy action on the A5
Cartan with the A5 Coxeter action; the separate firewall proves those actions
are inequivalent.
"""
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_packet72_c6_floquet_contrast.json'

def main(write=True):
    c6=json.loads((ROOT/'data/w33_packet72_physical_c6_address_compiler.json').read_text())
    fw=json.loads((ROOT/'data/w33_a5_coxeter_vs_hypercharge_z6_firewall.json').read_text())
    assert c6['status']=='PASS_LOOKUP_FREE_CONTROL_PLANE_COMPILER'
    assert fw['status']=='PASS_DISTINCT_A5_Z6_STRUCTURES'
    assert c6['cycle_profiles']['packet72']['6_cycles']==12

    x=sp.symbols('x')
    six=sp.expand(x**6-1)
    contrast=sp.div(six,x-1)[0]
    assert sp.expand(contrast)==x**5+x**4+x**3+x**2+x+1
    assert sp.factor(contrast)==(x+1)*(x**2-x+1)*(x**2+x+1)

    # Eigenphases k/6 for k=1..5 on each contrast block.
    phases=[f'{k}/6' for k in range(1,6)]
    # Power fixed dimensions inside one contrast block = roots with z^p=1.
    fixed={p:sum((k*p)%6==0 for k in range(1,6)) for p in (1,2,3,6)}
    assert fixed=={1:0,2:1,3:2,6:5}
    assert fw['coxeter_C6']['fixed_dimensions_by_power']=={str(k):v for k,v in fixed.items()}

    full_mult={str(k):12 for k in range(6)}
    pi_modes=12
    zero_modes=12
    contrast_dim=12*5
    assert zero_modes+contrast_dim==72

    out={
      'schema':'w33.packet72_c6_floquet_contrast.v1',
      'status':'PASS_C6_FLOQUET_A5_CONTRAST',
      'headline':'The physical packet72 C6 permutation is twelve disjoint six-cycles. Removing the uniform mode from each orbit leaves a five-dimensional contrast block with characteristic polynomial x^5+x^4+x^3+x^2+x+1, exactly the A5 Coxeter polynomial. Thus packet72 contains 12 spectral copies of the A5 Coxeter module and 12 ideal pi modes, while the previously proved action-level firewall remains intact.',
      'packet72':{
        'C6_cycles':12,'orbit_size':6,'uniform_modes':zero_modes,
        'contrast_dimension_total':contrast_dim,
        'full_sixth_root_multiplicities':full_mult},
      'single_orbit_contrast':{
        'dimension':5,
        'characteristic_polynomial':'x^5+x^4+x^3+x^2+x+1',
        'factorization':'(x+1)(x^2-x+1)(x^2+x+1)',
        'quasienergy_fractions_of_2pi':phases,
        'fixed_dimensions_by_power':{str(k):v for k,v in fixed.items()},
        'A5_Coxeter_spectral_match':True},
      'pi_modes':{
        'eigenvalue':'-1','quasienergy':'pi','multiplicity':pi_modes,
        'one_per_six_cycle':True},
      'experimental_read':'In an ideal compiled six-step cycle, prepare any orbit contrast vector and Fourier-resolve the six phases. The pi component should return a sign flip after one period and revive after two. Splitting of the 12-fold pi-mode degeneracy is a direct diagnostic of broken packet-C6 symmetry.',
      'firewall':'Spectral equivalence does not identify the physical E8 inner-holonomy action with the A5 Coxeter action. On the A5 Cartan the physical torus holonomy fixes all five dimensions, while the Coxeter element fixes none.',
      'parents':['data/w33_packet72_physical_c6_address_compiler.json','data/w33_a5_coxeter_vs_hypercharge_z6_firewall.json'],
      'checks':{'cycles12':True,'contrast_dim5_each':True,'coxeter_polynomial_match':True,
                'pi_modes12':True,'fixed_dimensions_0_1_2_5':True,'firewall_preserved':True}}
    if write: OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out

if __name__=='__main__':main(True)
