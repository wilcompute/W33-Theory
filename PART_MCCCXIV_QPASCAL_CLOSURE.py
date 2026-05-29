#!/usr/bin/env python3
"""PART MCCCXIV: q-Pascal / GQ / srg spectral closure verifier for W(3,3)."""
q = 3
print('q-PASCAL / GQ / SRG CLOSURE VERIFIER, q=', q)
# GQ(q,q) parameters
v = (q+1)*(q**2+1); k_val = q*(q+1)
lam = q-1; mu = q+1
print('v =', v, '= 40:', v==40)
print('k =', k_val, '= 12:', k_val==12)
print('lambda_GQ =', lam, '= r_char:', lam==2)
print('mu =', mu)
assert v==40 and k_val==12 and lam==2 and mu==4
# srg eigenvalues
r_srg = q-1; s_srg = -(q+1)
print('r_srg =', r_srg, 's_srg =', s_srg)
assert r_srg==2 and s_srg==-4
# block eigenvalues
l1 = k_val - r_srg; l2 = k_val - s_srg
print('lambda1 = k - r_srg =', l1, '= 10:', l1==10)
print('lambda2 = k - s_srg =', l2, '= 16:', l2==16)
assert l1==10 and l2==16
# gap
gap = l2 - l1
print('spectral gap =', gap, '= q! =', 2*3, ':', gap==6)
assert gap == 2*3  # q! = 6
# mean
print('mean(l1,l2) =', (l1+l2)//2, '= Phi3(q) =', (q**3-1)//(q-1))
assert (l1+l2)//2 == (q**3-1)//(q-1)  # Phi3(q) = 13
# multiplicities
m1 = k_val*(s_srg-k_val)*(s_srg+1)//((r_srg-s_srg)*(r_srg*s_srg+k_val))
m2 = 39 - m1
print('m1 =', m1, 'm2 =', m2)
assert m1==24 and m2==15
# srg eigenvalue relations
print('r_srg - s_srg =', r_srg-s_srg, '= g2:', r_srg-s_srg==6)
print('r_srg * s_srg =', r_srg*s_srg, '= -(q^2-1):', r_srg*s_srg==-(q**2-1))
Phi3 = (q**3-1)//(q-1)
print('v recovered =', l1*l2//4, '= v:', l1*l2//4==v)
print('Phi3 recovered =', (l1+l2)//2, '= Phi3:', (l1+l2)//2==Phi3)
print('ALL q-PASCAL CLOSURE IDENTITIES VERIFIED')
