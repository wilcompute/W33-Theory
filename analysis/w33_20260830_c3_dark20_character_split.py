#!/usr/bin/env python3
"""Refine the central-C3 dark20 split from 8+12 to 8+6+6 over C.

The existing exact certificate proves that the rational/integer dark20 module
has C3-fixed dimension 8 and total dimension 20.  Because the deck generator
is represented over Q, the two nontrivial complex C3 characters omega and
omega^2 are Galois-conjugate and therefore occur with equal multiplicity.
Thus the 12-dimensional sheet-resolving sector is canonically 6*omega plus
6*omega^2 after complexification.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
IN=ROOT/'data/PART_W33_20260829_C3_COVER_DARK20_DESCENT.json'
OUT=ROOT/'data/PART_W33_20260830_C3_DARK20_CHARACTER_SPLIT.json'

def main():
    d=json.loads(IN.read_text())
    assert d['status']=='PASS'
    total=d['dark20']['fullMapRank'];fixed=d['dark20']['deckFixedDimension']
    diff=d['dark20']['deckDifferenceImageRank']
    assert (total,fixed,diff)==(20,8,12)
    assert diff%2==0
    nontrivial=diff//2
    assert fixed+2*nontrivial==total
    out={
      'schema':'w33.20260830.c3-dark20-character-split.v1','status':'PASS',
      'inputCertificate':IN.name,
      'deckGroup':'C3',
      'complexCharacterMultiplicities':{'1':fixed,'omega':nontrivial,'omega^2':nontrivial},
      'dimensions':{'deckInvariant':fixed,'omegaSector':nontrivial,'omega2Sector':nontrivial,'total':total},
      'reason':('The dark20 representation and deck action are defined over Q. Complex conjugation/Galois conjugation exchanges the omega and omega^2 eigenspaces, so they have equal dimension. The existing exact 8-dimensional fixed-space certificate leaves 12 nonfixed dimensions, forcing 6+6.'),
      'intertwinerConsequence':'Because the certified 216-to-dark20 map has full rank 20 and is C3-equivariant, its sheet-resolving image reaches both nontrivial character sectors; six complex dimensions transform by omega and six by omega^2.',
      'theorem':'After complexification the exact C3 dark20 decomposition is 8*1 + 6*omega + 6*omega^2. The previously certified 12-dimensional sheet-resolving sector is therefore a conjugate 6+6 pair, not an undifferentiated block.',
      'boundary':'Exact finite representation theory. The character labels are deck-C3 eigencharacters, not measured optical phases.'
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,sort_keys=True))

if __name__=='__main__':main()
