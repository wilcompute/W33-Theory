#!/usr/bin/env python3
"""1458-mode photonic transducer specification for the doubled W33 carrier.

Encoding:
  internal six-qutrit basis n=(n0,...,n5) in F3^6 is flattened to
      m = sum_j n_j 3^j, 0<=m<729,
  realized as one 729-bin frequency/time-mode comb.
  The central-character logical label r=+1,-1 is a polarization/path rail.
Total optical modes: 2*729=1458.

Native generators:
  X_j: permute only ternary digit n_j -> n_j+1 mod3;
  Z_j: phase omega^(+n_j) on rail r=+1 and omega^(-n_j) on r=-1;
  center z: relative rail phase diag(omega,omega^-1);
  outer s: rail SWAP.

Planning budgets (not measurements):
  * center rail phase: average single-qubit gate fidelity >=0.99 requires
        |epsilon| <= 0.1227828 rad
    for symmetric +/-epsilon phase error;
  * qutrit digit phase: F_avg>=0.99 for diag(1,e^ie,e^-ie) requires
        |epsilon| <= 0.1417772 rad;
  * if total unwanted leakage across the other 728 internal modes must be <1%,
    an equal-leakage union bound gives <=1.3736e-5 power per wrong mode,
    i.e. about -48.62 dB relative to the addressed mode;
  * for the 17-native-primitive determinant compiler to retain >=50% optical
    transmission, each sequential primitive must transmit >=0.96005
    (<0.1771 dB insertion loss).  The two-invariant compiler relaxes the same
    target to >=0.7071 per primitive (<1.505 dB).

These are engineering targets derived from declared system requirements, not
reported performance of an existing W33 device.
"""
from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_1458_mode_photonic_transducer_spec.json'

def digits(m):
    ds=[]
    for _ in range(6):ds.append(m%3);m//=3
    return tuple(ds)
def flat(ds):return sum(ds[j]*(3**j) for j in range(6))
def xperm(j,m):
    d=list(digits(m));d[j]=(d[j]+1)%3;return flat(d)
def main(write=True):
    # Verify each X_j is a disjoint union of 243 3-cycles on 729 modes.
    cycles={}
    for j in range(6):
        seen=set();cc=[]
        for m in range(729):
            if m in seen:continue
            cyc=[];u=m
            while u not in seen:
                seen.add(u);cyc.append(u);u=xperm(j,u)
            cc.append(cyc)
        assert len(cc)==243 and all(len(c)==3 for c in cc)
        cycles[str(j)]={'three_cycles':243,'modes':729}
    eps2=math.acos(math.sqrt((0.99*6-2)/4))
    eps3=math.acos((math.sqrt(0.99*12-3)-1)/2)
    leak=0.01/728
    leak_db=10*math.log10(leak)
    eta17=0.5**(1/17);loss17=-10*math.log10(eta17)
    eta2=0.5**0.5;loss2=-10*math.log10(eta2)
    out={'schema':'w33.photonic_transducer_1458.v1','status':'PASS_MODE_COMPILER_ENGINEERING_TARGETS_NOT_MEASURED',
      'encoding':{
        'logical_rail':'r=+1,-1 -> polarization H/V or path A/B',
        'internal_index':'m=sum_j n_j 3^j, n_j in {0,1,2}',
        'internal_modes':729,'total_modes':1458,
        'recommended_physical_basis':'frequency-bin or time-bin comb for m; polarization/path for r'},
      'generator_compiler':{
        'X_j':'permutation n_j -> n_j+1 mod3; 243 disjoint three-cycles for each j',
        'Z_j':'rail-conditioned phase omega^(r n_j)',
        'center':'relative rail phase diag(omega,omega^-1)',
        'outer':'rail SWAP',
        'X_cycle_census':cycles},
      'planning_requirements':{
        'single_outer_or_center_Favg_target':0.99,
        'center_symmetric_phase_error_max_rad':eps2,
        'single_internal_qutrit_phase_Favg_target':0.99,
        'internal_phase_error_max_rad':eps3,
        'aggregate_wrong_mode_leakage_target':0.01,
        'equal_leakage_per_wrong_mode_power_max':leak,
        'equal_leakage_per_wrong_mode_db':leak_db,
        'throughput_target_after_nonlinear_stack':0.5,
        '17_native_stack_per_primitive_transmission_min':eta17,
        '17_native_stack_insertion_loss_max_db_each':loss17,
        '2_invariant_stack_per_primitive_transmission_min':eta2,
        '2_invariant_stack_insertion_loss_max_db_each':loss2},
      'repo_alignment':'Holonet blueprint already uses time-bin x frequency-bin photonic qutrits; this spec packages the six-qutrit 729-space into one high-dimensional comb rather than claiming six independent photon DOFs.',
      'physical_boundary':'Mode count and unitary normal forms are exact. Source brightness, detector efficiency, comb bandwidth, actual insertion loss, phase noise and crosstalk remain unmeasured for a W33 implementation.',
      'checks':{'all_six_X_permutations_verified':True,'1458_dimension_exact':True,'planning_budgets_derived':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
