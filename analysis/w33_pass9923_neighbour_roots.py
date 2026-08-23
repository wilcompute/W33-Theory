import sys, numpy as np
sys.path.insert(0,'analysis')
from w33_pass7333_leech_d4_form import load_flat, invariant_gram
from pathlib import Path
SP='C:/Users/wiljd/AppData/Local/Temp/claude/c--Repos-Theory-of-Everything/4e98df7e-146b-472d-b3f7-862c4ae1e8b0/scratchpad/'
G0,_=invariant_gram(load_flat(Path('analysis/_co0_G.txt'))); G=-G0
V=np.load(SP+'minvec.npy')
print('THE 2-NEIGHBOUR CONSTRUCTION, AND WHY TYPE DECIDES IT')
print()
print('  For c in L with c not in 2L and (c,c) = 0 mod 8, the 2-neighbour')
print('     L_c = {x in L : (x,c) even} + Z.(c/2)')
print('  is again even unimodular.')
print()
print('  A type-4 class contains vectors of norms 4, 12, 20, ... = 4 mod 8 ONLY,')
print('  so it NEVER has a representative with norm 0 mod 8: type-4 classes give NO')
print('  neighbour.  A type-8 class has norm-8 representatives, so it does.')
print()
print('  => the type-8 classes are EXACTLY the 2-neighbour directions of Leech.')
print('  => V_2, having no type-4 class, is a 12-dimensional space of 4095 neighbour')
print('     directions, closed under addition.')
print()
# build a frame and read off the neighbour's roots
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
u={}
for g in FR: u[g.tobytes()]=g
FR=list(u.values())
print('THE ROOTS OF THE NEIGHBOUR')
print('  a root of L_c is c/2 + y with |c/2+y|^2 = 2, i.e. |y|^2 + (c,y) = 0.')
print('  Then c+2y is a norm-8 vector in the class of c -- so the roots are exactly')
print('  the frame vectors HALVED.')
print()
print('  frame size:',len(FR),' -> roots of L_c:',len(FR))
Gm=np.array([[int(a@G@b) for b in FR] for a in FR])
norms=set(int(Gm[i,i])//4 for i in range(len(FR)))
print('  norm of each halved frame vector (should be 2):',norms)
offs=set()
for i in range(len(FR)):
    for j in range(len(FR)):
        if i!=j and not np.array_equal(FR[i],-FR[j]): offs.add(int(Gm[i,j])//4)
print('  inner products between non-antipodal halved frame vectors:',sorted(offs))
print()
if offs=={0} and norms=={2}:
    print('  *** 48 ROOTS, MUTUALLY ORTHOGONAL IN 24 ANTIPODAL PAIRS ***')
    print('  That is the root system A1^24 exactly. By Niemeier, the neighbour L_c IS the')
    print('  Niemeier lattice with root system A1^24 -- and ITS GLUE CODE IS THE BINARY')
    print('  GOLAY CODE.')
    print()
    print('  SO THE CODE LIVES ON THE NEIGHBOUR, NOT ON L/2L. That is exactly why a frame')
    print('  could not coordinatise L/2L at Pass9801-9824: it was the wrong target. The')
    print('  frame is the bridge from Leech to its neighbour, and the Golay code is the')
    print('  glue of the neighbour.')
