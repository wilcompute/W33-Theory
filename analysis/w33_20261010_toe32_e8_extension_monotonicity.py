"""TOE32: exact group-commutant monotonicity obstruction.

Read independent parallel Pass11843 report certificate; certify an
extension by translations of its SAME embedded finite Lorentz group
cannot *enlarge* the gauge centralizer to SU3xSU2xU1. An extension may
shrink it. Distinguish finite-kinematic algebra from physical gauge.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'data/w33_pass11843_e8_tits_lorentz_commutant.json'
OUT=ROOT/'data/w33_20261010_toe32_e8_extension_monotonicity.json'
def run():
 data=json.loads(SRC.read_text(encoding='utf-8'))
 print('PARALLEL_CERT topkeys',list(data.keys())[:20],flush=True)
 assert data['e8']['dim']==248 and data['e8']['jacobi_max']<1e-10
 c=data['commutants']
 assert c["lorentz_W(A5)'_even_tits_words"]['dim']==11
 assert c["lorentz_W(A5)'_even_tits_words"]['derived_dim']==11
 assert c["lorentz_W(A5)'_even_tits_words"]['centre_dim']==0
 assert c['contains_su3_A2'] and c['contains_su2_alpha']
 assert c["control_W(E6)'_even_words"]['dim']==8
 # The parallel commit's frozen pass is a separate, independently tested input:
 # E8 centralizer of finite Lorentz Tits embedding is su3+su2, dimension 11,
 # rank3 and centre0; Weil embedding centralizer u1 but is not SAME embedding.
 sample=dict(
   status='PASS',
   parallel_certificate_filename=SRC.relative_to(ROOT).as_posix(),
   parallel_certificate_top_level_keys=list(data.keys())[:25],
   lorentz_tits_centralizer='su(3)⊕su(2)',dimension=11,
   algebraic_centre_dimension=0,
   statement='For any H with L⊂H⊂Aut(e8), c_e8(H)⊂c_e8(L)=su3⊕su2. Therefore any extension by finite translations cannot add a commuting independent hypercharge u1 while retaining the full su3 and su2 as the commutant: the centralizer of su3⊕su2 inside itself is zero. Any subalgebra containing the full su3⊕su2 and extra line within the same c_e8(L) is impossible by dimension11.',
   converse_limit='A subalgebra of su3+su2 can have a nontrivial centre after symmetry reduction, but that centre cannot coexist with the FULL original su3+su2 (dimension11). Translation extension may preserve 11 or reduce it, not reach the Standard Model total dimension12.',
   comparison='Weil E8 route has commutant u1 but is a distinct representation, and direct sums of commutants from inequivalent actions are not a single E8 representation. To obtain SM gauge commutant SU3xSU2xU1 with same finite Lorentz target, must change embedding, enlarge Lie algebra, or abandon commutant identification.',
   novelty_boundary='The dimension11 and centre0 and Weil u1 are prior parallel Pass11837 and 11843 results; the subgroup-extension monotonicity deduction and hypercharge obstruction for all containing groups in the FIXED Tits embedding are new here. No actual 248-dimensional subgroup action for translations constructed.',
   source='analysis/PASS11839_11843_CROSSCAP_HOLOGRAPHY_FREE_FIELDS_E8_COMMUTANT.md')
 OUT.write_text(json.dumps(sample,indent=2)+'\n',encoding='utf-8')
 return sample
if __name__=='__main__':run()
