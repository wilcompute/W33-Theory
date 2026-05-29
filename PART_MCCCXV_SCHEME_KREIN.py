#!/usr/bin/env python3
"""PART MCCCXV: Association scheme and Krein verifier."""
q=3; v=(q+1)*(q**2+1); k=q*(q+1); lam=q-1; mu=q+1; k2=v-1-k
r_srg=q-1; s_srg=-(q+1); m1,m2=24,15; l1,l2=10,16
print('SCHEME/KREIN VERIFIER')
assert v==40 and k==12 and lam==2 and mu==4 and k2==27
p112=k-lam-1; assert p112==q**2, f'{p112}!=q^2'
p211=mu; assert p211==q+1
p212=k-mu; assert p212==2**q
print('P-matrix row1:',[1,k,k2],'row2:',[1,q-1,-q],'row3:',[1,-(q+1),q])
assert k2==q**3
print('k2=q^3:',k2==q**3)
omega=1-k//s_srg; alpha=v*(-s_srg)//(k-s_srg)
print('omega<=',omega,'=q+1:',omega==q+1,'alpha<=',alpha,'=l1:',alpha==l1)
assert omega==q+1 and alpha==l1 and omega*alpha==v
print('omega*alpha=v: TIGHT')
assert lam+mu==6 and lam*mu==2**q and mu-lam==2
fixed=(m1*r_srg+m2*s_srg)/(m1+m2)
assert abs(fixed-(-4/13))<1e-12
print('fixed point=',-4,'/13=',fixed)
LHS=(r_srg+1)*(k+r_srg+2*r_srg*s_srg); RHS=(k+r_srg)*(s_srg+1)**2
assert LHS<=RHS; print('Krein condition verified')
print('ALL SCHEME/KREIN VERIFIED')
