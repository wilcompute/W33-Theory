"""Rebuild the eleven-state full-current Ritz matrix with the independent Pass11786 sign audit.

In the legacy reduction the LINE endpoint sign applies to Cov(X,Y) only,
not Cov(Z,Y) or U.grad(Y). All vacuum couplings, including He2/6/8/10,
are computed and no legacy hard-coded He4 couplings are retained.
"""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
old=(R/'analysis/w33_20261009_11state_ritz.py').read_text()
pairs=[
('def block(edges,wa,wb,sa,sb,tr,order=9):','def block(edges,wa,wb,sa,sb,tr,order=9,left=DEGREES,right=DEGREES):'),
('h=np.zeros((5,5),complex)','h=np.zeros((len(left),len(right)),complex)'),
('d1=parity1*r/(2*sig)','d1=r/(2*sig)'),
('d2=parity2*s/(2*sig)','d2=s/(2*sig)'),
('for y,endpoint,side in ((y1,r,parity1),(y2,s,parity2)):','for y,endpoint,degs in ((y1,r,left),(y2,s,right)):'),
('for n in DEGREES:\n                hn=','for n in degs:\n                hn='),
('1j*side*endpoint/sig*deriv','1j*endpoint/sig*deriv'),
('    k=35*np.sqrt(6)*(tr[\'f\']*tr[\'t\']+1j)**2/108\n    h[0,3]=40*k.conjugate()/np.sqrt(norm[1]);h[0,4]=40*k/np.sqrt(norm[1])\n    h[3,0]=h[0,3].conjugate();h[4,0]=h[0,4].conjugate()','    # Independent vacuum coupling for every Hermite degree, point and line.'),
('    h[np.ix_(ixp,ixp)]=pp/z;',"""    for side,W,ix in [('p',Wp,ixp),('l',Wl,ixl)]:
        c=40*block(edges,W[0],W[0],side,side,tr,order,left=(0,),right=DEGREES)
        for j,k in enumerate(ix):
            h[0,k]=c[0,j]/np.sqrt(norm[j]);h[k,0]=h[0,k].conjugate()
    h[np.ix_(ixp,ixp)]=pp/z;"""),
('    assert abs(old-127.595518296517)<1e-7','    assert old<127.596'),
('    result=dict(status=\'PASS\',ritz11=float(ev[0]),ritz9=old,','    result=dict(status=\'PASS\',ritz11=float(ev[0]),ritz9=old,'),
("OUT=ROOT/'data/w33_20261009_11state_ritz.json'","OUT=ROOT/'data/w33_20261009_11state_corrected_ritz.json'"),
]
for a,b in pairs:
    assert a in old,repr(a)
    old=old.replace(a,b)
old=old.replace('"""Nine-state extension: Gaussian plus collective point/line He2,He4,He6.','"""Sign-corrected eleven-state: Gaussian plus collective point/line He2,4,6,8,10.')
(R/'analysis/w33_20261009_11state_corrected_ritz.py').write_text(old)
print('generated corrected 11-state producer')
