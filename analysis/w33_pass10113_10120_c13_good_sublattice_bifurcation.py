#!/usr/bin/env python3
"""Pass10113-10120: sharpen the Co1 13A / canonical-V2 orbit question.

This pass consumes the exhaustive Pass10049-10056 census.  If its certificate is
not present yet, it runs that verifier first.  The exact census for one actual
Co1 class-13A representative is:

    65 invariant maximal totally singular 12-spaces,
    41 with zero Leech type-4 classes,
    24 with exactly 156 type-4 classes.

For a maximal totally singular E <= Lambda/2Lambda, the halved preimage
L_E=(1/sqrt(2))*pi^{-1}(E) is an even unimodular rank-24 lattice.  Each type-4
class in E contributes one antipodal pair of Leech minimal vectors and hence two
roots in L_E.  Therefore the two 13A-invariant types have 0 and 312 roots.
Niemeier classification identifies them as Leech and A12^2 respectively.

Crucial correction: zero type-4 classes does NOT imply one Co0 orbit.  The
literature on 'good sublattices' of the Leech lattice has 16 Aut(Lambda)=2.Co1
orbits.  Thus the 41 good generators do not close the original selector by
count/type alone; canonical V2 must be matched by a finer orbit invariant (for
example the bad-vector profile used in that classification).
"""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data/PART_W33_PASS10049_10056_CO1_C13_V2_EXHAUSTIVE.json'
OUT=ROOT/'data/PART_W33_PASS10113_10120_C13_GOOD_SUBLATTICE_BIFURCATION.json'

def ensure_source():
    if SRC.exists(): return
    subprocess.run([sys.executable, str(ROOT/'analysis/w33_pass10049_10056_co1_c13_v2_exhaustive.py')],check=True,cwd=ROOT)

def main():
    ensure_source(); src=json.loads(SRC.read_text())
    d={int(k):int(v) for k,v in src['class13A_invariant_12spaces']['type4_count_distribution'].items()}
    assert src['class13A_invariant_12spaces']['totally_singular_count']==65
    assert d=={0:41,156:24},d
    roots={c:2*c for c in d}
    assert roots=={0:0,156:312}
    # A_n has n(n+1) roots. Two A12 components have 2*12*13=312.
    assert 2*12*13==312
    out={
      'schema':'w33.pass10113_10120.c13_good_sublattice_bifurcation.v1','status':'PASS','passes':'10113-10120',
      'co1_13A_census':{'invariant_maximal_totally_singular_12spaces':65,'type4_distribution':{'0':41,'156':24},'canonical_V2_is_fixed_by_the_tested_representative':src['canonical_V2']['explicit_G2_order13_stabilizes']},
      'halved_preimage_dictionary':{'construction':'L_E=(1/sqrt(2))*pi^{-1}(E)','roots_per_type4_class':2,'root_counts':{'type4_0':0,'type4_156':312}},
      'Niemeier_identification':{'0_roots':'Leech lattice','312_roots':'A12^2','A12_root_count':156,'A12^2_root_count':312,'input':'Niemeier classification of even unimodular rank-24 lattices'},
      'orbit_correction':{'good_sublattice_definition':'maximal totally singular E whose halved preimage is similar to Leech','Aut_Leech_good_sublattice_orbits':16,'consequence':'type-4-free is not a complete Co1 orbit invariant; 41 invariant good generators need not be conjugate to canonical V2'},
      'new_selector_target':'Compute the good-sublattice profile/stabilizer of canonical V2 and of the 41 13A-fixed good generators; equality of profile is the next exact orbit test.',
      'theorem':'For a Co1 class-13A element, the 65 invariant maximal totally singular generators bifurcate exactly into 41 Leech-neighbor (rootless/good) generators and 24 A12^2-neighbor generators with 312 roots. This proves that order 13 is compatible with good Leech sublattices, but not yet with the specific canonical V2 orbit because Aut(Leech) has 16 good-sublattice orbits.',
      'boundary':'The 65/41/24 census is exact from Pass10049-10056. The Leech/A12^2 naming uses the rank-24 Niemeier classification. The 16-orbit statement is external prior art and is a warning against claiming transitivity; no canonical-V2 stabilizing C13 is claimed.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','generators':65,'Leech_good':41,'A12^2':24,'good_orbits':16}))
    return 0
if __name__=='__main__': raise SystemExit(main())
