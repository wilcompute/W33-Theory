import sys, numpy as np
sys.path.insert(0,'analysis')
from w33_pass7333_leech_d4_form import load_flat, invariant_gram
from pathlib import Path
SP='C:/Users/wiljd/AppData/Local/Temp/claude/c--Repos-Theory-of-Everything/4e98df7e-146b-472d-b3f7-862c4ae1e8b0/scratchpad/'
G0,_=invariant_gram(load_flat(Path('analysis/_co0_G.txt'))); G=-G0
V=np.load(SP+'minvec.npy')
v=V[0]
print('DOES A TYPE-4 CLASS CONTAIN A VECTOR OF NORM 0 mod 8?')
print('  Norms in a class are constant only MOD 4 (that is what q records), so a type-4')
print('  class could still hold a norm-8 or norm-16 vector. Checking directly.')
print()
ip=V@G@v
print('  inner products (v, lambda) over minimal lambda:',sorted(set(ip.tolist())))
print('  note +-3 does NOT occur.')
print()
print('  norm-8 in the class: |v+2lam|^2 = 4 + 4(v,lam) + 4|lam|^2 = 8 needs')
print('    (v,lam) + |lam|^2 = 1, and Cauchy-Schwarz forces |lam|^2 = 4, so (v,lam) = -3.')
print('    IMPOSSIBLE, since -3 never occurs. So no norm-8 vector in a type-4 class.')
print()
print('  norm-16 in the class: take (v,lam) = -1 with |lam|^2 = 4:')
k=int(np.flatnonzero(ip==-1)[0])
w=V[k]
g=v+2*w
print(f'    |v + 2*lam|^2 = 4 + 4*(-1) + 4*4 = {int(g@G@g)}')
print('    and 16 == 0 mod 8.')
print()
found16 = int(g@G@g)==16
print('  SO A TYPE-4 CLASS *DOES* HAVE A REPRESENTATIVE OF NORM 0 mod 8:',found16)
print()
print('  => my step "type-4 classes never give a 2-neighbour" is WRONG. They do.')
print('     What actually differs between type 4 and type 8 is the neighbour ROOT SYSTEM,')
print('     not whether a neighbour exists.')
print()
print('  roots of L_c for a type-4 class, using the norm-16 representative c:')
print('    need |c/2 + y|^2 = 2, i.e. 4 + (c,y) + |y|^2 = 2, so (c,y) + |y|^2 = -2.')
ipg=V@G@g
cnt=0
for kk in np.flatnonzero(ipg==-6):
    y=V[kk]
    if int((g+2*y)@G@(g+2*y))==8: cnt+=1
print(f'    norm-4 y with (c,y) = -6 giving a root: {cnt}')
print('    (a full count needs norm-6 and norm-8 y as well; not attempted here)')
