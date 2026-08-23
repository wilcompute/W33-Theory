import sys, numpy as np
sys.path.insert(0,'analysis')
from w33_pass7333_leech_d4_form import load_flat, invariant_gram
from pathlib import Path
SP='C:/Users/wiljd/AppData/Local/Temp/claude/c--Repos-Theory-of-Everything/4e98df7e-146b-472d-b3f7-862c4ae1e8b0/scratchpad/'
G0,_=invariant_gram(load_flat(Path('analysis/_co0_G.txt'))); G=-G0
V=np.load(SP+'minvec.npy')
v=V[0]; ip=V@G@v
f=v+V[np.flatnonzero(ip==0)[0]]
ipf=V@G@f
FR=[f,-f]
for k in np.flatnonzero(ipf==-4):
    g=f+2*V[k]
    if int(g@G@g)==8: FR.append(g)
for k in np.flatnonzero(ipf==4):
    g=-f+2*V[k]
    if int(g@G@g)==8: FR.append(g)
uu={}
for g in FR: uu[g.tobytes()]=g
reps=[]
for g in uu.values():
    if not any(np.array_equal(g,-h) for h in reps): reps.append(g)
R=np.array(reps,dtype=np.int64)
print('FRAME VALIDATION: do Leech vectors have all-equal-parity coordinates?')
print('  (that is a defining feature of the Conway-Sloane frame coordinates)')
C=(V@G@R.T)                      # coordinates of every minimal vector
par=(C%2)
same=np.all(par==par[:,[0]],axis=1)
print('  minimal vectors with all coordinates the same parity:',int(same.sum()),'of',len(V))
print()
shapes={}
for row in C:
    a=np.abs(row); key=tuple(sorted(np.unique(a,return_counts=True)[0].tolist()))
    cnt=tuple(sorted(zip(*[x.tolist() for x in np.unique(a,return_counts=True)])))
    shapes[cnt]=shapes.get(cnt,0)+1
print('  coordinate SHAPES of the 196560 minimal vectors:')
for k,n in sorted(shapes.items(),key=lambda t:-t[1]):
    print('   ',k,'->',n)
print()
print('  Conway-Sloane predicts exactly: (2^8,0^16) x 97152, (+-3,1^23) x 98304, (4^2,0^22) x 1104')
print()
print('WHY THE mod-2 COORDINATE MAP CANNOT WORK -- structural, not a bug:')
print('  all 48 frame vectors lie in ONE class mod 2L, so f_i - f_j is in 2L and')
print('    (x, f_i) - (x, f_j) = (x, 2*lambda) = 2(x,lambda) == 0 mod 2')
print('  for every x. All 24 functionals coincide mod 2, so the map has rank 1.')
print('  The Golay code in these coordinates lives in the mod-4 layer, and mod-4 data is')
print('  NOT a function of the class mod 2L: replacing x by x+2*lambda shifts x_i by')
print('  2*lambda_i, which changes the mod-4 pattern whenever lambda_i is odd.')
