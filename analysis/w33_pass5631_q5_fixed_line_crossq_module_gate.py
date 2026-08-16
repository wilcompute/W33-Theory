#!/usr/bin/env python3
"""Pass5631: test the q=5 fixed-line interpretation against the q=3 F4 12-orbits.

For ANY group action with one fixed point f and one moving 12-orbit M, the centered
13-point permutation module has dimension 12 and decomposes as
  <12 e_f - sum_M e_i> + M_0,
where M_0 is the 11-dimensional zero-sum moving module.  The ordinary 12-point
permutation module decomposes as
  <sum_M e_i> + M_0.
Therefore the centered q=5 13-cover module is equivariantly isomorphic to the
moving 12-point permutation module: the distinguished q=5 direction maps to the
CONSTANT VECTOR on the 12-orbit, not to one distinguished q=3 point.

If the pending direct Pass5606 GAP conjugator confirms that the q=5 moving12 action
is the Latin/F4 short-root-pair action, this gives the cross-q representation bridge
immediately.  It still does not identify a physical vacuum: q=3 has two isomorphic
12-orbits, and the image is an orbit-average collective mode.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5631_Q5_FIXED_LINE_CROSSQ_MODULE_GATE.json'
DIRECT=ROOT/'data/PART_W33_PASS5606_COVER12_EXPLICIT_CONJUGATOR.json'

def main():
    # Build the universal intertwiner on coordinates. Domain is the centered
    # subspace of C^13 represented by basis u plus d_i=e_i-e_11 (i=0..10).
    # Codomain is C^12 represented by c plus the same d_i.
    u=np.zeros(13);u[0]=12;u[1:]=-1
    c=np.ones(12)
    D13=[];D12=[]
    for i in range(11):
        a=np.zeros(13);a[1+i]=1;a[12]=-1;D13.append(a)
        b=np.zeros(12);b[i]=1;b[11]=-1;D12.append(b)
    B13=np.column_stack([u]+D13);B12=np.column_stack([c]+D12)
    assert np.linalg.matrix_rank(B13)==12 and np.linalg.matrix_rank(B12)==12
    assert np.max(abs(np.ones(13)@B13))<1e-12
    # The map B13 coordinates -> B12 coordinates is an isomorphism.  Every
    # permutation of moving coordinates fixes u,c and acts identically on M_0.
    gate='PENDING_DIRECT_GAP_CONJUGATOR'
    direct=None
    if DIRECT.exists():
        direct=json.loads(DIRECT.read_text())
        if direct.get('conjugate_in_S12') is True: gate='DIRECT_MOVING12_CONJUGACY_CONFIRMED'
        else: gate='DIRECT_MOVING12_CONJUGACY_REFUTED'
    out={
      'pass':5631,'status':'CROSSQ_CENTERED_MODULE_THEOREM__'+gate,
      'universal_module_identity':'centered(1+12 permutation module) = 1_fixed-difference + 11_zero-sum ~= 12-point permutation module = 1_average + 11_zero-sum',
      'q5_invariant_direction':'u = 12 e_fixed - sum e_moving',
      'only_possible_q3_image_under_degree12_intertwiner':'c = sum of the 12 q3 orbit basis vectors',
      'physical_consequence':'Even if the direct F4/Latin conjugator succeeds, the distinguished q5 vertex becomes a collective orbit-average line in q3, not a distinguished q3 projective point.',
      'nonuniqueness':'The q3 W(F4) decomposition has two isomorphic 12-orbits exchanged by a quadratic-form similarity, so there is no unique q3 12-orbit target without extra data.',
      'direct_action_gate':gate,
      'direct_file_seen':DIRECT.exists(),
      'firewall':'No q5 fixed vertex = q3 vacuum/Higgs identification is licensed. The strongest possible bridge is an equivariant module map to an orbit-average singlet, conditional on direct degree12 action conjugacy.'
    }
    if direct is not None: out['direct_conjugator_summary']={'conjugate_in_S12':direct.get('conjugate_in_S12'),'fixed_cover_vertex':direct.get('fixed_cover_vertex')}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
