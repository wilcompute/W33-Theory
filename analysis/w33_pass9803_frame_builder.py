import sys, numpy as np
sys.path.insert(0,'analysis')
from w33_pass7333_leech_d4_form import load_flat, invariant_gram
from pathlib import Path
SP='C:/Users/wiljd/AppData/Local/Temp/claude/c--Repos-Theory-of-Everything/4e98df7e-146b-472d-b3f7-862c4ae1e8b0/scratchpad/'
G0,_=invariant_gram(load_flat(Path('analysis/_co0_G.txt')))
G=-G0
V=np.load(SP+'minvec.npy')
print('BUILDING A FRAME DIRECTLY')
print('  For minimal v,w with v.w = 0:  |v+w|^2 = |v-w|^2 = 8,')
print('  (v+w)-(v-w) = 2w is in 2L so they are CONGRUENT, and (v+w).(v-w) = |v|^2-|w|^2 = 0')
print('  so they are ORTHOGONAL. Two frame vectors for free.')
print()
v=V[0]
ip=V@G@v
print('  inner-product distribution of minimal vectors against a fixed v:')
u,c=np.unique(ip,return_counts=True)
print('   ',dict(zip(u.tolist(),c.tolist())))
w=None
for k in range(len(V)):
    if ip[k]==0: w=V[k]; break
f=v+w
print()
print('  chose w orthogonal to v.  f = v+w has norm',int(f@G@f))
print()
print('COLLECTING THE WHOLE CLASS: norm-8 vectors congruent to f')
print('  f+2L has norm 8 iff (f,lam) = -|lam|^2, and |lam|^2 <= 8 by Cauchy-Schwarz,')
print('  so lam has norm 4, 6 or 8. Scanning the norm-4 vectors:')
ipf=V@G@f
cand=[f,-f]
for k in np.flatnonzero(ipf==-4):
    g=f+2*V[k]
    if int(g@G@g)==8: cand.append(g)
for k in np.flatnonzero(ipf==4):
    g=-f+2*V[k]
    if int(g@G@g)==8: cand.append(g)
uniq={}
for g in cand: uniq[g.tobytes()]=g
F=list(uniq.values())
print('  norm-8 vectors found from norm-4 lam:',len(F))
same=all(not ((g-f)%2).any() for g in F)
print('  all congruent to f mod 2:',same)
if len(F)>=2:
    Gm=np.array([[int(a@G@b) for b in F] for a in F])
    offdiag=set(int(Gm[i,j]) for i in range(len(F)) for j in range(len(F)) if i!=j)
    print('  pairwise inner products among them:',sorted(offdiag)[:8],'...' if len(offdiag)>8 else '')
    ortho=all(Gm[i,j]==0 for i in range(len(F)) for j in range(len(F)) if i!=j and not np.array_equal(F[i],-F[j]))
    print('  mutually orthogonal (except antipodal pairs):',ortho)
    print('  -> that is',len(F)//2,'antipodal pairs of the 24 a full frame needs')
