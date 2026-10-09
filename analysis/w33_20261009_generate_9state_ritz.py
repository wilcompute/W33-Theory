"""Generate nine-dimensional collective Hermite Ritz variant from frozen seven-state producer."""
from pathlib import Path
r=Path(__file__).resolve().parents[1]
source=(r/'analysis/w33_20261008_7state_ritz.py').read_text()
changes={
    'DEGREES=(2,4,6)':'DEGREES=(2,4,6,8)',
    'h=np.zeros((3,3),complex)':'h=np.zeros((4,4),complex)',
    'h=np.zeros((7,7),complex)':'h=np.zeros((9,9),complex)',
    'ixp=[1,3,5];ixl=[2,4,6]':'ixp=[1,3,5,7];ixl=[2,4,6,8]',
    'h9=ritz(9);h10=ritz(10)':'h9=ritz(11);h10=ritz(12)',
    'h9[:5,:5]':'h9[:7,:7]',
    '127.61937784333912':'127.61920315299878',
    'data/w33_20261008_7state_ritz.json':'data/w33_20261009_9state_ritz.json',
    'ritz7=float(ev[0]),ritz5=old':'ritz9=float(ev[0]),ritz7=old',
    'quadrature9_10_error=diff':'quadrature11_12_error=diff',
    'Seven-state':'Nine-state',
}
for old,new in changes.items():
    assert old in source,old
    source=source.replace(old,new)
target=r/'analysis/w33_20261009_9state_ritz.py'
target.write_text(source)
print('generated',target)
