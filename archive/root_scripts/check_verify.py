import math
from math import sqrt
q=3
qfact=math.factorial(q)
twoq=2**q
D=qfact**2-4*twoq
roots=((qfact+sqrt(D))/2,(qfact-sqrt(D))/2)
lam,mu=sorted(roots)
# ensure lam=2 mu=4
k=2**q+q+1
v_calc=(k*(k-1)-mu*(mu-1))/(lam-mu+k)
E=v_calc*k/2
T=v_calc*k*lam/6
Theta=q*q+1
Phithree=q*q+q+1
Phisix=q*q-q+1
z=(k-1)+mu*1j
M_vac=(k-1)*((k-lam)**2+1)
Delta_M=q/(lam*(k-1))
M_eff=M_vac+Delta_M
alpha_inv=abs(z)**2 + v_calc/M_eff
alpha_inv_alt=137 + 880/24445
alpha_s=lam*Theta/Phithree**2
mH1=(mu+1)**q
mH2=q**4+v_calc+mu
mH3=v_calc*q+mu+1
vEW=E+qfact
mp_me=v_calc*(v_calc+lam+mu)-mu
V_us=(lam+Phisix)/v_calc
V_cb=mu/Theta**2
V_ub=lam/(v_calc*Phithree)
print('q=',q,'q! =',qfact,'2^q=',twoq)
print('Discriminant D=',D,'roots=',roots,'lam,mu=',lam,mu)
print('k=',k,'v=',v_calc,'E=',E,'T=',T)
print('Theta=',Theta,'Phi3=',Phithree,'Phi6=',Phisix)
print('alpha_inv=',alpha_inv)
print('alpha_inv_alt=',alpha_inv_alt)
print('alpha_s=',alpha_s)
print('mH checks:',mH1,mH2,mH3)
print('vEW=',vEW)
print('mp/me=',mp_me)
print('CKM:',V_us,V_cb,V_ub)
print('Weinberg sin^2=',q/Phithree)
print('Koide K target=',lam/q)
print('Proton-electron exact?',mp_me==1836)
print('alpha_inv_close?',abs(alpha_inv-137.035999177)<1e-6)
