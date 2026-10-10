"""Round35 exact W33 alpha rational and independent CODATA 2022 holdout.

W33 SRG(40,12,2,4), all-ones eigen12, M=11((A-2I)^2+I).
Thus 1^T M^-1 1=40/1111; proposed alpha^-1=137+40/1111.
NIST/CODATA 2022 (RevModPhys 97 025002, 2025) gives
137.035999177(21), std absolute uncertainty 0.000000021.
Mathematical equality fails by ~210.6 standard uncertainties.
This does NOT refute W33 mathematical structure; it falsifies
unqualified EXACT α^-1 identification at Q²=0.
"""
from pathlib import Path
from decimal import Decimal,getcontext
from fractions import Fraction
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261010_toe35_alpha_CODATA_2022_holdout.json'
def run():
 getcontext().prec=60
 graph=dict(v=40,k=12,lam=2,mu=4)
 base=(graph['k']-1)*((graph['k']-2)**2+1)
 assert base==1111
 pred=Fraction(137)+Fraction(40,1111)
 codata=Decimal('137.035999177')
 sigma=Decimal('0.000000021')
 val=Decimal(pred.numerator)/Decimal(pred.denominator)
 diff=val-codata;nsigma=abs(diff)/sigma
 assert nsigma>200
 # any direct one-dimensional all-ones M inverse is exact and
 # needs no numerical matrix inversion.
 rec=dict(status='PASS',
  source_formula='alpha_inv_W33 = 137 + 1ᵀ M⁻¹ 1, M=(k−1)[(A−2I)²+I], W33 k=12 and A1=12*1',
  M_ones_eigenvalue=base,ones_vector_norm_squared=40,
  correction_exact_fraction='40/1111',
  alpha_inv_W33_exact_fraction=f'{pred.numerator}/{pred.denominator}',
  alpha_inv_W33_decimal=str(val),
  CODATA_2022_alpha_inv='137.035999177',
  CODATA_2022_1sigma_absolute='0.000000021',
  absolute_difference=str(abs(diff)),
  discrepancy_in_CODATA_standard_uncertainties=str(nsigma),
  authoritative_reference='CODATA recommended values of the fundamental physical constants: 2022, Reviews of Modern Physics 97 (2025) 025002, https://physics.nist.gov/cuu/pdf/RevModPhys.97.025002.pdf',
  conclusion='The graph rational is EXACT mathematics and numerically close at parts per 1e8, but differs from the CODATA 2022 empirical inverse fine structure constant by ~211 reported sigma. Treating the raw equality as an accurate/falsifiable physical prediction is scientifically untenable without independent derived radiative/scale corrections with error budget and no ex post fitting.',
  limitations='The source formula by itself does not specify physical renormalization scheme, momentum scale, radiative corrections, a gauge field or a dynamical derivation of electric charge. This failure of the naive equality does not disprove other physics that may someday arise from W33.')
 OUT.write_text(json.dumps(rec,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 print('ROUND35 alpha inverse predicted',val,'CODATA',codata,'diff',diff,'sigma',nsigma,flush=True)
 return rec
if __name__=='__main__':run()
