#!/usr/bin/env python3
"""Gauge-side three-qutrit Pauli firewall for the heterotic 729 carrier.

The new heterotic carrier theorem gives an exact vector-space identification
  C^27_fixed tensor C^27_E6 ~= (C^3)^tensor6.
That does NOT by itself make the E6 factor a physical 3-qutrit register.

A standard computational-basis n-qutrit Pauli representation contains a
maximal commuting shift subgroup X ~= C3^n which acts regularly on the 3^n
basis labels. For n=3 this requires a regular elementary-abelian C3^3 on the
27 E6 basis states.

Pass 370 gives a complete Sylow-3 enumeration inside the W(E6) permutation
action on the E6 27:
  * an elementary-abelian C3^3 subgroup exists,
  * it is NOT regular,
  * the regular order-27 groups are nonabelian extraspecial groups.
Thus no standard 3-qutrit Pauli group can be realized *monomially* on the E6
weight/cubic basis with its X-Lagrangian inside W(E6).

The cubic's explicit Heisenberg chart gives an independent support-level
falsifier. Plain translations of each of the three F3 chart coordinates fail
to preserve respectively 29,29,30 of the 45 Cartan-cubic support triads.
The first two coordinate phase characters do have zero total phase on all
45 supports, whereas the third does not (25/10/10 residues). This asymmetry is
consistent with the chart being a Hessian/Heisenberg incidence coordinate
system, not a three-qutrit computational basis.

Scope: this kills the natural monomial/cubic-preserving realization. It does
not rule out a nonmonomial projective H(3^3) action from the full string
vertex/Narain algebra.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_e6_gauge_three_qutrit_pauli_firewall.json'

def main(write=True):
    p370=json.loads((ROOT/'data/w33_pass370_the_two_27s_are_one_torsor.json').read_text())
    assert p370['status']=='PASS'
    c=p370['checks']
    assert c['e6_abelian_exists'] and c['e6_abelian_NOT_regular']
    assert c['e6_exp3_heisenberg_regular']
    m=json.loads((ROOT/'artifacts/e6_cubic_affine_heisenberg_model.json').read_text())
    mp={int(k):tuple(v['u'])+(int(v['z']),) for k,v in m['e6id_to_heisenberg'].items()}
    inv={v:k for k,v in mp.items()}
    tri=[]
    for rec in m['affine_u_lines']:
        tri += [tuple(sorted(map(int,t))) for t in rec['triads']]
    tri += [tuple(sorted(map(int,t))) for t in m['fiber_triads_e6id']]
    T=set(tri)
    assert len(T)==45

    trans_bad=[]
    phase_hist=[]
    for j in range(3):
        bad=0
        for t in T:
            tt=[]
            for eid in t:
                v=list(mp[eid]);v[j]=(v[j]+1)%3;tt.append(inv[tuple(v)])
            if tuple(sorted(tt)) not in T:bad+=1
        trans_bad.append(bad)
        h={0:0,1:0,2:0}
        for t in T:
            h[sum(mp[eid][j] for eid in t)%3]+=1
        phase_hist.append(h)
    assert trans_bad==[29,29,30]
    assert phase_hist[0]=={0:45,1:0,2:0}
    assert phase_hist[1]=={0:45,1:0,2:0}
    assert phase_hist[2]=={0:25,1:10,2:10}

    out={
      'schema':'w33.e6_gauge_three_qutrit_pauli_firewall.v1',
      'status':'PASS_MONOMIAL_THREE_QUTRIT_REALIZATION_NO_GO',
      'parent_carrier':'data/w33_heterotic_z3_729_matter_carrier.json',
      'theorem':{
        'necessary_condition':'a standard 3-qutrit Pauli computational basis requires a regular elementary-abelian C3^3 shift subgroup on 27 labels',
        'complete_E6_Sylow_result':'C3^3 exists in the E6 27 permutation action but is not regular; regular order-27 torsors are nonabelian',
        'conclusion':'no monomial cubic/weight-basis realization of H(3^3)=3^(1+6) with the standard shift Lagrangian inside W(E6)'},
      'independent_cubic_chart_falsifier':{
        'support_triads':45,
        'plain_coordinate_translation_bad_supports':trans_bad,
        'coordinate_phase_residue_histograms':[{str(k):v for k,v in h.items()} for h in phase_hist],
        'interpretation':'the two u-coordinate phase characters preserve every cubic support, but the z-character and all three plain shifts do not'},
      'surviving_bridge':'the 27x27=729 heterotic matter space remains an exact six-trit carrier/basis intertwiner',
      'open_loophole':'a nonmonomial or string-vertex/Narain projective action could still realize the missing gauge-side Weyl pairs; this certificate does not rule that out',
      'checks':{
        'pass370_complete_abelian_no_regular':True,
        '45_supports_loaded':True,
        'translation_failure_exact':True,
        'phase_asymmetry_exact':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out
if __name__=='__main__':main(True)
