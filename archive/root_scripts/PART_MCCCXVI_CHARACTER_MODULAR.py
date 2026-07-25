#!/usr/bin/env python3
"""PART MCCCXVI: Character table, Hamming distances, Frobenius verifier."""
import math
q=3; v=(q+1)*(q**2+1); k=q*(q+1); k2=v-1-k; lam=q-1; mu=q+1
l1,l2=10,16; m1,m2=24,15; g2=6
print('CHARACTER/MODULAR VERIFIER')
assert k2==q**3
ham_adj=2*k-2*lam; ham_nonadj=2*k-2*mu
print('Ham_adj=',ham_adj,'=2*l1:',ham_adj==2*l1)
print('Ham_nonadj=',ham_nonadj,'=l2:',ham_nonadj==l2)
assert ham_adj==2*l1 and ham_nonadj==l2
assert ham_adj+ham_nonadj==g2**2
assert abs(ham_adj-ham_nonadj)==mu
mod_weight=v//2; Phi3=(q**3-1)//(q-1); Phi6=7
print('mod_weight=',mod_weight,'=Phi3+Phi6:',mod_weight==Phi3+Phi6)
assert mod_weight==Phi3+Phi6
min_norm=k//2; assert min_norm==g2
print('min_norm=',min_norm,'=g2=q!:',min_norm==g2)
disc=k**2-4*k2
r1=(k-math.isqrt(disc))//2; r2=(k+math.isqrt(disc))//2
print('Frob roots:',r1,r2,'=[q,q^2]:',r1==q,r2==q**2)
assert r1==q and r2==q**2
assert r1+r2==k and r1*r2==k2
frob_gap=r2-r1; assert frob_gap==g2
print('Frob gap=',frob_gap,'=g2: 4th occurrence of g2=q!')
Sp4q=q**4*(q**4-1)*(q**2-1); W_E6=51840
print('|Sp(4,3)|=',Sp4q,'=|W(E6)|:',Sp4q==W_E6)
assert Sp4q==W_E6
print('ALL CHARACTER/MODULAR VERIFIED')
