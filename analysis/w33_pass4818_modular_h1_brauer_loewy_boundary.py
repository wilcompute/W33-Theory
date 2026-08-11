#!/usr/bin/env python3
"""Pass 4818 — exact 2-Brauer semisimplification plus Loewy boundary for flag H1.

The complete ordinary PSp(4,3)=U4(2) character of the 5671-dimensional H1 was
frozen in Pass4745.  GAP/CTblLib supplies the exact characteristic-two Brauer
table and decomposition matrix.  This script combines them to obtain the exact
composition-factor multiplicities of the semisimplification.

Pass4769 independently supplies module-level information not visible to Brauer
characters: trivial socle dimension 4, trivial head dimension 1, augmentation
codimension 1, and all four fixed vectors (including the deck class) lying in
the augmentation image.  Hence the trivial factors are demonstrably involved
in nonsplit extensions.

A full radical/socle Loewy layering of all nontrivial constituents is NOT
inferred from the decomposition matrix.  This script records that boundary
explicitly rather than calling a semisimplification a Loewy series.
"""
from __future__ import annotations
import ast,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4818_MODULAR_H1_BRAUER_LOEWY.json'
TXT=ROOT/'analysis/PASS4818_U42_MOD2_BRAUER.txt'

def grab(txt,key):
    m=re.search(r'^'+re.escape(key)+r'=(.*)$',txt,re.M)
    if not m:raise RuntimeError(f'missing {key}')
    s=m.group(1).replace('true','True').replace('false','False')
    return ast.literal_eval(s)

def main():
    if not TXT.exists():raise RuntimeError('Run GAP extractor analysis/PASS4818_U42_MOD2_BRAUER.g first')
    txt=TXT.read_text(encoding='utf-8',errors='replace')
    labels=grab(txt,'ORD_LABELS');degrees=grab(txt,'ORD_DEGREES');bdeg=grab(txt,'BRAUER_DEGREES');D=grab(txt,'DECMAT');blocks=grab(txt,'BLOCKS')
    assert len(labels)==len(degrees)==len(D) and all(len(r)==len(bdeg) for r in D)
    p4745=json.loads((ROOT/'data/PART_W33_PASS4745_INVARIANT_H1_CHARACTER.json').read_text())
    p4769=json.loads((ROOT/'data/PART_W33_PASS4769_MODULAR_H1_HEAD_SOCLE.json').read_text())
    rep={x['label']:(x['degree'],x['multiplicity']) for x in p4745['ordinary_PSp']['irreducibles']}
    degree_counts={d:degrees.count(d) for d in set(degrees)}
    def mult_for(i):
        lab=str(labels[i]).lower().replace('chi','').replace('_','').replace('{','').replace('}','')
        d=degrees[i]
        # CTblLib Atlas labels are normally 1a,5a,...; accept exact repository label first.
        if lab in rep:return rep[lab][1]
        if degree_counts[d]==1:
            hit=[m for k,(dd,m) in rep.items() if dd==d]
            return hit[0] if hit else 0
        # Omitted ordinary constituents have multiplicity zero; for repeated degrees
        # match by the degree-letter suffix.
        candidates=[k for k,(dd,m) in rep.items() if dd==d]
        for k in candidates:
            if k.lower()==lab:return rep[k][1]
        return 0
    om=[mult_for(i) for i in range(len(labels))]
    assert sum(om[i]*degrees[i] for i in range(len(om)))==5671
    bm=[sum(om[i]*int(D[i][j]) for i in range(len(om))) for j in range(len(bdeg))]
    assert sum(bm[j]*bdeg[j] for j in range(len(bdeg)))==5671
    simple=[{'index':j+1,'degree':int(bdeg[j]),'composition_multiplicity':int(bm[j])} for j in range(len(bdeg)) if bm[j]]
    triv=[x for x in simple if x['degree']==1]
    assert len(triv)>=1
    soc=p4769['PGSp']['fixed_dimension_trivial_socle'];head=p4769['PGSp']['coinvariant_dimension_trivial_head']
    assert (soc,head)==(4,1) and p4769['PGSp']['deck_in_augmentation']
    trivial_comp=sum(x['composition_multiplicity'] for x in triv)
    assert trivial_comp>=soc
    out={'pass':4818,'group':'PSp(4,3) ~= U4(2)','field':'characteristic 2 over a splitting field',
      'ordinary_character_dimension':5671,'ordinary_labels':labels,'ordinary_multiplicities':om,
      'Brauer_simple_degrees':[int(x) for x in bdeg],'Brauer_composition_factors':simple,'trivial_composition_multiplicity':int(trivial_comp),
      'module_level_trivial_layers':{'trivial_socle_dimension':soc,'trivial_head_dimension':head,'all_four_fixed_vectors_in_augmentation':True,'deck_line_nonsplit':True},
      'blocks':blocks,
      'augmentation_warning':'PSp(4,3) is perfect, so the full group-algebra augmentation ideal has I/I^2=0 and hence I=I^2; its image filtration stabilizes and is not the Jacobson-radical Loewy filtration for this non-2-group.',
      'theorem':'The exact 2-Brauer semisimplification of the 5671-dimensional flag-graph H1 is obtained from the CTblLib decomposition matrix and the frozen ordinary character. Together with Pass4769, the trivial socle/head and nonsplitting position are exact module-level data.',
      'boundary':'This closes the composition-factor census but not the complete radical/socle ordering of every nontrivial simple factor. A decomposition matrix determines semisimplification, not indecomposable Loewy extensions.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
