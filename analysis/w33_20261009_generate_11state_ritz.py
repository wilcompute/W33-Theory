"""Reproducibly extend the 9-state point/line even-Hermite Ritz tower to 11."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
src=(root/'analysis/w33_20261009_9state_ritz.py').read_text()
changes={
'DEGREES=(2,4,6,8)':'DEGREES=(2,4,6,8,10)',
'np.zeros((4,4),complex)':'np.zeros((5,5),complex)',
'np.zeros((9,9),complex)':'np.zeros((11,11),complex)',
'ixp=[1,3,5,7];ixl=[2,4,6,8]':'ixp=[1,3,5,7,9];ixl=[2,4,6,8,10]',
'h9=ritz(11);h10=ritz(12)':'h9=ritz(13);h10=ritz(14)',
'h9[:7,:7]':'h9[:9,:9]',
'127.61920315299878':'127.595518296517',
'data/w33_20261009_9state_ritz.json':'data/w33_20261009_11state_ritz.json',
'ritz9=float(ev[0]),ritz7=old':'ritz11=float(ev[0]),ritz9=old',
'quadrature11_12_error=diff':'quadrature13_14_error=diff',
}
for a,b in changes.items():
    assert a in src,a
    src=src.replace(a,b)
target=root/'analysis/w33_20261009_11state_ritz.py'
target.write_text(src)
print('generated',target)
