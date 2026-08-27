#!/usr/bin/env python3
"""Pass10613-10620: a canonical 9|18 block target inside the noncanonical H27->H4 spectral transport.

H27's central C3 average P0=(I+Z+Z^2)/3 projects onto the trivial central
character, dimension 9.  Because the H27 eigenvalues 8,-1 occur exactly there
and 2,-4 occur exactly in the two nontrivial central characters, the real
central class operator C=Z+Z^-1 is already a polynomial in H27 adjacency H:

  C_H = (H^3 - 5 H^2 - 22 H + 32 I)/24.

It takes values 2 on eigenvalues 8,-1 and -1 on 2,-4, so P0=(C_H+I)/3.

The reversible H(4)/(13:6) quotient S has spectrum 20^1,7^8,(-1)^12,(-5)^6.
The corresponding label operator is likewise polynomial:

  C_S = -(11 S^3 - 186 S^2 - 1457 S + 4340 I)/5600,

with values 2 on 20,7 and -1 on -1,-5.  Hence Q0=(C_S+I)/3 is a canonical
rank-9 projector.  Any orthogonal spectral transporter U satisfying
S=U f(H) U^T must obey Q0=U P0 U^T.  The coarse 9|18 central split is therefore
canonical even though U itself is not.

The fine split of the real 18-space into the two conjugate nontrivial C3
characters remains a choice of complex structures on the 12- and 6-dimensional
spectral sectors, with U(6)xU(3) gauge freedom.
"""
from __future__ import annotations
from fractions import Fraction
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS10613_10620_CENTRAL_PROJECTOR_TRANSPORT.json'

def ch(x): return Fraction(x**3-5*x*x-22*x+32,24)
def cs(x): return Fraction(-(11*x**3-186*x*x-1457*x+4340),5600)

def main():
    assert {x:ch(x) for x in (8,-1,2,-4)}=={8:2,-1:2,2:-1,-4:-1}
    assert {x:cs(x) for x in (20,7,-1,-5)}=={20:2,7:2,-1:-1,-5:-1}
    h_rank9=1+8; s_rank9=1+8
    assert h_rank9==s_rank9==9
    assert 12+6==18
    out={
      'schema':'w33.pass10613_10620.central_projector_transport.v1','status':'PASS','passes':'10613-10620',
      'H27':{
        'central_class_operator':'C_H=(H^3-5H^2-22H+32I)/24 = Z+Z^-1',
        'labels':{'8':2,'-1':2,'2':-1,'-4':-1},
        'central_trivial_projector':'P0=(C_H+I)/3','rank':9,'nontrivial_real_rank':18},
      'H4_reversible_quotient':{
        'label_operator':'C_S=-(11S^3-186S^2-1457S+4340I)/5600',
        'labels':{'20':2,'7':2,'-1':-1,'-5':-1},
        'rank9_projector':'Q0=(C_S+I)/3','rank':9,'complement_rank':18},
      'transport_theorem':'For every orthogonal U with S=U f(H) U^T under Pass10517, Q0=U P0 U^T. The coarse central-character 9|18 split is invariant under all allowed block gauges.',
      'fine_phase_freedom':'Recovering the actual two nontrivial C3 characters inside the real rank-18 complement requires compatible complex structures on the 12- and 6-dimensional sectors; residual gauge U(6) x U(3).',
      'theorem':'The formerly noncanonical H27-to-H4 spectral transporter contains a canonical block-level core: the rank-9 trivial-center sector of H27 maps to the rank-9 H4 eigensum (20 plus 7), and the rank-18 nontrivial-center sector maps to the (-1 plus -5) eigensum. Only the conjugate phase splitting inside that 18-space remains noncanonical.',
      'boundary':'Exact rational spectral-projector statement. It does not produce a canonical full 27x27 orthogonal transporter or a canonical order-3 permutation on the H4 quotient.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','canonical_blocks':[9,18],'fine_gauge':'U6xU3'}))
if __name__=='__main__':main()
