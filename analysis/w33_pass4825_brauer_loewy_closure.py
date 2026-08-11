#!/usr/bin/env python3
"""Pass 4825 — exact Brauer closure and fail-closed Loewy bounds for flag H1.

The workflow first runs the existing CTblLib extractor
analysis/PASS4818_U42_MOD2_BRAUER.g and then the Pass4818 parser. This pass reads
the resulting exact semisimplification together with the module-level Pass4769
head/socle data and records every Loewy consequence that genuinely follows.

A decomposition matrix does NOT determine the full indecomposable Loewy series.
Accordingly, this pass closes the composition-factor census and the trivial
extension position, and gives rigorous lower bounds on Loewy complexity, while
leaving nontrivial radical ordering open unless a future explicit 5671-module
MeatAxe computation supplies it.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4825_BRAUER_LOEWY_CLOSURE.json'

def main():
    p18=ROOT/'data/PART_W33_PASS4818_MODULAR_H1_BRAUER_LOEWY.json'
    if not p18.exists():raise RuntimeError('Pass4818 Brauer certificate not materialized; run GAP extractor and parser first')
    B=json.loads(p18.read_text());H=json.loads((ROOT/'data/PART_W33_PASS4769_MODULAR_H1_HEAD_SOCLE.json').read_text())
    assert B['ordinary_character_dimension']==5671
    soc=int(H['PGSp']['fixed_dimension_trivial_socle']);head=int(H['PGSp']['coinvariant_dimension_trivial_head']);assert (soc,head)==(4,1)
    t=int(B['trivial_composition_multiplicity']);assert t>=4
    factors=B['Brauer_composition_factors'];nontriv=sum(x['degree']*x['composition_multiplicity'] for x in factors if x['degree']!=1)
    assert nontriv+t==5671
    lower=2
    strict_internal=max(0,t-soc-head)
    out={'pass':4825,'group':'PSp(4,3) ~= U4(2)','field':'F2 splitting-field Brauer data','module_dimension':5671,
      'Brauer_simple_degrees':B['Brauer_simple_degrees'],'Brauer_composition_factors':factors,'trivial_composition_multiplicity':t,
      'module_level':{'trivial_socle_dimension':soc,'trivial_head_dimension':head,'all_fixed_lines_in_augmentation':True,'deck_line_nonsplit':True,'no_trivial_direct_summand':True},
      'Loewy_consequences':{'Loewy_length_lower_bound':lower,'trivial_factors_forced_outside_socle_and_head_at_least':strict_internal,'full_nontrivial_Loewy_ordering_known':False},
      'theorem':'CTblLib closes the exact characteristic-two composition-factor census of the 5671-dimensional flag H1. Combined with explicit module actions from Pass4769, the four-dimensional trivial socle, one-dimensional trivial head, and nonsplitting of every fixed line from a trivial direct summand are exact. These data force nonsemisimplicity and Loewy length at least two.',
      'boundary':'The exact Brauer semisimplification and trivial extension position are closed. The complete radical/socle ordering of nontrivial simple factors is not determined by a decomposition matrix and is not promoted without an explicit 5671-dimensional MeatAxe computation.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())

# Observable PR evidence trigger; no theorem content changes.
