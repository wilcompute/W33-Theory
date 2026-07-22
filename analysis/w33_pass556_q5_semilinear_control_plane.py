#!/usr/bin/env python3
from __future__ import annotations
import argparse,itertools,json,math
from pathlib import Path
from w33_pass543_547_common import CycPrime,charpoly_prime

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass556_q5_semilinear_control_plane.json'
OVERLAY=ROOT/'hardware'/'w33_pass556_q5_semilinear_control_plane.json'
A=(1,1,2,2,2,3,3,2,3,2,3,2)
B=(1,1,2,2,3,3,3,3,2,3,2,2)
C=CycPrime(5)

def exact_div(a,n):
    if any(x%n for x in a):raise ArithmeticError((a,n))
    return tuple(x//n for x in a)

def e4_from_moments(ts):
    return exact_div(C.sub(C.mul(ts[1],ts[1]),C.smul(2,ts[3])),8)

def determinant_fibres():
    c={1:0,2:0,3:0,4:0}
    for a,b,c0,d in itertools.product(range(5),repeat=4):
        det=(a*d-b*c0)%5
        if det:c[det]+=1
    return c

def overlay_payload():
    modes=[]
    spec={
      1:('unitary_clifford','coherent Clifford generator sequence',False),
      2:('galois_sigma2','phase-cycled readout and software relabelling; not a complex-linear quantum gate',False),
      3:('galois_sigma3','inverse phase-cycled readout and software relabelling; not a complex-linear quantum gate',False),
      4:('antiunitary_sigma4','phase-reversed conjugate reference arm; covariance readout, not deterministic universal antiunitary dynamics',True),
    }
    for i,d in enumerate((1,2,3,4)):
        name,physical,conj=spec[d]
        modes.append({'determinant':d,'name':name,'galois_map':f'zeta5 -> zeta5^{d}','signal_bin':2038+2*i,'reference_bin':2039+2*i,'complex_conjugation':conj,'physical_contract':physical})
    return {
      'schema':'w33.hardware.pass556.q5_semilinear_control_plane.v1',
      'carrier':'2048-bin BT1653 guard-shell compiler',
      'reserved_bins':{'semilinear_modes':'2038-2045','quartic_moment_accumulator':2046,'orientation_parity_latch':2047},
      'determinant_modes':modes,
      'quartic_classifier':{'moments':['p2=tr(D^2)','p4=tr(D^4)'],'newton_formula':'e4=(p2^2-2*p4)/8','role':'Exact classifier for the Pass-540 80-word spectral fibre.'},
      'orientation_channel':{'observable':'Moore-Dickson frame product prod_v c(v) in F5^x/{squares}','role':'Distinguishes the odd global switch after quartic fibre gating.','frame_dependence':'Requires the oriented icosahedral/Fano control frame and is not a characteristic-polynomial observable.'},
      'execution_order':['apply or emulate the requested determinant-class covariance mode','measure p2 and p4 in matched signal/reference bins','reconstruct e4 exactly in the cyclotomic coefficient register','gate on the target e4 level','read the independent orientation parity latch'],
      'safety_boundary':'Determinant classes 2 and 3 are Galois-semilinear readout modes, and class 4 is an antiunitary covariance comparison. The overlay does not claim these are arbitrary deterministic quantum channels.'
    }

def payload():
    target=charpoly_prime(5,A)[0];cpB=charpoly_prime(5,B)[0];level=[];newton=True;all_count=0
    for m in range(4096):
        offs=tuple(a*(4 if (m>>i)&1 else 1)%5 for i,a in enumerate(A));cpv,ts,_=charpoly_prime(5,offs);all_count+=1
        e4=e4_from_moments(ts)
        if e4!=cpv[4]:newton=False
        if e4==target[4]:level.append(m)
    dets=determinant_fibres();prodA=math.prod(A)%5;prodB=math.prod(B)%5;ov=overlay_payload()
    OVERLAY.parent.mkdir(parents=True,exist_ok=True);OVERLAY.write_text(json.dumps(ov,sort_keys=True,separators=(',',':'))+'\n')
    checks={
      'all_4096_moment_identities':all_count==4096 and newton,
      'quartic_level_is_exact_80_fibre':len(level)==80,
      'pass540_pair_charpoly_equal':target==cpB,
      'pass540_pair_e4_equal':target[4]==cpB[4],
      'pass540_pair_orientation_opposite':prodA==(-prodB)%5,
      'quartic_does_not_observe_odd_switch':target==cpB and prodA!=prodB,
      'gl2_order480':sum(dets.values())==480,
      'four_equal_determinant_fibres120':dets=={1:120,2:120,3:120,4:120},
      'four_mode_bins_disjoint':len({x[k] for x in ov['determinant_modes'] for k in ('signal_bin','reference_bin')})==8,
      'guard_shell_bins_in_range':all(0<=x[k]<2048 for x in ov['determinant_modes'] for k in ('signal_bin','reference_bin')),
      'quartic_and_orientation_bins_reserved':ov['reserved_bins']['quartic_moment_accumulator']==2046 and ov['reserved_bins']['orientation_parity_latch']==2047,
      'galois_modes_not_misrepresented_as_gates':all('not a complex-linear quantum gate' in x['physical_contract'] for x in ov['determinant_modes'] if x['determinant'] in (2,3)),
    }
    return {
      'schema':'w33.pass556.q5_semilinear_control_plane.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'determinant_fibres':dets,'quartic_readout':{'newton_formula':'e4=(tr(D^2)^2-2 tr(D^4))/8','target_level_size':len(level),'exact_on_all_sections':newton},
      'odd_switch_test':{'A_product_mod5':prodA,'B_product_mod5':prodB,'same_characteristic_polynomial':target==cpB,'same_quartic_invariant':target[4]==cpB[4],'conclusion':'The quartic invariant gates the correct 80-word fibre but is provably blind to the odd cospectral switch. A separate oriented product latch is necessary.'},
      'hardware_overlay':str(OVERLAY.relative_to(ROOT)),'checks':checks,
      'boundary':'This is an exact compiler/control contract and finite-section certificate. It is not a claim that Galois automorphisms or antiunitary maps are available as unrestricted deterministic physical gates.'
    }

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 556 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
