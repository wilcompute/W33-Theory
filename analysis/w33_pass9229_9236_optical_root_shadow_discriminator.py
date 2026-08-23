#!/usr/bin/env python3
"""Pass9229-9236: a finite optical/mode-support discriminator from root shadows.

Under the explicitly stated equal-root-coupling model, treat each W33 quotient
point as one output port and add root intensities incoherently within a port.
Two dimensionless observables distinguish all three rank-24 carriers:
  * best-line concentration among visible output intensity;
  * quotient-dark root fraction.
No claim is made that a physical device automatically realizes this coupling.
"""
from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS9229_9236_OPTICAL_ROOT_SHADOW_DISCRIMINATOR.json'

def stats(name,total,zero,visible_points,mult):
 visible=visible_points*mult;assert visible+zero==total
 p=[mult/visible]*visible_points
 H=-sum(x*math.log2(x) for x in p);pr=1/sum(x*x for x in p)
 best_line=(4*mult/visible) if visible_points==40 else 1.0
 return {'carrier':name,'total_roots':total,'dark_roots':zero,'dark_fraction':zero/total,'visible_ports':visible_points,'intensity_per_visible_port':mult,'visible_participation_ratio':pr,'visible_Shannon_bits':H,'best_W33_line_fraction_of_visible_intensity':best_line,'best_W33_line_fraction_of_total_root_weight':best_line*visible/total}

def main():
 rows=[stats('E8^3',720,0,40,18),stats('E6^4',288,72,4,54),stats('A2^12',72,0,4,18)]
 sig={(round(r['best_W33_line_fraction_of_visible_intensity'],8),round(r['dark_fraction'],8)) for r in rows};assert len(sig)==3
 assert rows[0]['best_W33_line_fraction_of_visible_intensity']==0.1
 assert rows[1]['dark_fraction']==0.25 and rows[2]['dark_fraction']==0
 out={'schema':'w33.pass9229_9236.optical_root_shadow_discriminator.v1','status':'PASS','passes':'9229-9236','model':'40 quotient points are output ports; every root has equal coupling weight; roots in the quotient kernel are dark; port intensities add incoherently','carriers':rows,
      'minimal_two_observable_signature':{'E8^3':[0.1,0.0],'E6^4':[1.0,0.25],'A2^12':[1.0,0.0],'coordinates':['best-line visible concentration','dark-root fraction']},
      'theorem':'Within the equal-root-coupling 40-port model, the rank-24 carriers are perfectly separated by two dimensionless measurements. E8^3 is delocalized (best W33 line carries 1/10 of visible intensity), E6^4 is line-localized with a 1/4 dark fraction, and A2^12 is line-localized with no dark fraction.',
      'physical_boundary':'This is a falsifiable finite readout model, not a derivation of an optical Hamiltonian or coupling law. A hardware claim requires showing that prepared modes couple approximately equally to lattice roots and that quotient-kernel roots are experimentally dark.'}
 OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','signatures':out['minimal_two_observable_signature']}))
 return 0
if __name__=='__main__':raise SystemExit(main())
