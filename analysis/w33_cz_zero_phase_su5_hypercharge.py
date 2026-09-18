#!/usr/bin/env python3
"""CZ_3 zero-phase block is the canonical SU(5) GUT block.

Parents:
  data/w33_heterotic_flagship_cz_clifford_bridge.json
  Holotrade data/w33_flagship_wilson_line_cz_bridge.json

For the standard two-qutrit controlled-Z,
    CZ_3 |x,y> = omega^(x y)|x,y>,
the zero-phase basis is exactly
    (0,0),(0,1),(0,2),(1,0),(2,0),
the union of the two coordinate axes in F3^2.  It has dimension 5.
The two nonzero eigenspaces each have dimension 2.

Hence the connected centralizer in SU(9) is
    S(U(5) x U(2) x U(2)),
with semisimple part SU(5) x SU(2) x SU(2).

The independently certified flagship Wilson line is projectively SU(9)-conjugate
to CZ_3 and its neutral root subsystem is A4+A1+A1.  Therefore under any such
conjugacy its unique A4 factor is precisely the SU(5) acting on the five-
dimensional CZ zero-phase eigenspace.

Inside that five-space choose a 3+2 decomposition and define
    Y = diag(-1/3,-1/3,-1/3,+1/2,+1/2).
Then
    tr Y = 0,
    tr Y^2 = 5/6,
    k_Y = 2 tr Y^2 = 5/3.
This is the canonical SU(5) hypercharge normalization used by the flagship.

Important scope:
  * The theorem identifies the SU(5) factor and normalization at the conjugacy-
    class level.
  * It does NOT claim the repository's displayed heterotic root basis is already
    the standard |x,y> computational basis.  An SU(9) conjugation is needed.
  * It does NOT identify the five cubic top couplings or the five low-order
    Hall-defect directions with the five zero-phase basis vectors.
"""
from __future__ import annotations
import json
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_cz_zero_phase_su5_hypercharge.json'

def main(write=True):
    basis=[(x,y) for x in range(3) for y in range(3)]
    phase=[(x*y)%3 for x,y in basis]
    blocks={a:[basis[i] for i,p in enumerate(phase) if p==a] for a in range(3)}
    assert [len(blocks[a]) for a in range(3)]==[5,2,2]
    assert blocks[0]==[(0,0),(0,1),(0,2),(1,0),(2,0)]

    Y=[F(-1,3)]*3+[F(1,2)]*2
    assert sum(Y)==0
    norm=sum(y*y for y in Y)
    assert norm==F(5,6)
    kY=2*norm
    assert kY==F(5,3)

    # Centralizer dimensions in u(9) and su(9).
    mult=[5,2,2]
    u_dim=sum(m*m for m in mult)
    su_dim=u_dim-1
    assert u_dim==33 and su_dim==32
    # root counts of semisimple blocks: A4 + A1 + A1 = 20+2+2 = 24.
    root_count=sum(m*(m-1) for m in mult)
    assert root_count==24

    parent=json.loads((ROOT/'data/w33_heterotic_flagship_cz_clifford_bridge.json').read_text())
    assert parent['status']=='PASS'
    assert parent['positive_branch']['fundamental_multiplicities']==[5,2,2]
    assert parent['positive_branch']['sl9_Z3_grading']==[32,24,24]
    assert parent['positive_branch']['neutral_centralizer']=='S(U(5) x U(2) x U(2))'

    out={
      'schema':'w33.cz_zero_phase_su5_hypercharge.v1',
      'status':'PASS',
      'headline':'For qutrit CZ_3, the zero-phase eigenspace is the five-state set xy=0 in F3^2, while the two charged eigenspaces have dimension two. Therefore its SU(9) centralizer is S(U(5)xU(2)xU(2)). Since the recorded heterotic flagship Wilson line is projectively SU(9)-conjugate to CZ_3 and has neutral A4+A1+A1, its SU(5) GUT factor is exactly the unitary factor on this five-dimensional zero-phase block. Standard SU(5) hypercharge on a 3+2 split has tr(Y^2)=5/6 and kY=5/3, reproducing the flagship canonical normalization.',
      'CZ3':{
        'definition':'CZ_3 |x,y> = omega^(xy)|x,y>',
        'phase_blocks':{str(a):[list(x) for x in blocks[a]] for a in range(3)},
        'multiplicities':[5,2,2],
        'zero_phase_equation':'x*y=0 over F3',
        'zero_phase_geometry':'union of the two coordinate axes in F3^2',
      },
      'centralizer':{
        'SU9':'S(U(5) x U(2) x U(2))',
        'su9_dimension':su_dim,
        'neutral_semisimple_roots':root_count,
        'semisimple_type':'A4 + A1 + A1',
        'GUT_factor':'SU(5) on the zero-phase eigenspace'},
      'hypercharge':{
        'inside_zero_phase_SU5':['-1/3','-1/3','-1/3','1/2','1/2'],
        'trace':'0',
        'trace_Y2':str(norm),
        'level_kY':'2 tr(Y^2) = 5/3',
        'SM_subgroup':'SU(3) on the first three zero-phase states; SU(2) on the last two'},
      'heterotic_bridge':{
        'parent':'data/w33_heterotic_flagship_cz_clifford_bridge.json',
        'statement':'projective SU(9) conjugacy transports the flagship neutral A4 factor onto the CZ zero-phase U(5) block',
        'flagship_hypercharge_norm':'5/6'},
      'scope':{
        'proved':'matrix-level CZ block structure, centralizer, SU5 factor and canonical hypercharge normalization at the conjugacy-class level',
        'not_proved':'a preferred heterotic-root-to-computational-basis conjugating matrix; any identification of five top couplings or five Hall-defect modes with the five zero-phase basis states'},
      'checks':{
        'zero_phase_has_5_states':True,
        'charged_blocks_have_2_each':True,
        'centralizer_dim32':True,
        'A4_A1_A1_root_count24':True,
        'canonical_hypercharge_norm_5over6':True,
        'canonical_kY_5over3':True,
        'parent_CZ_bridge_loaded':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return out

if __name__=='__main__':main(True)
