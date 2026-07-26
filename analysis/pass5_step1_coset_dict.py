#!/usr/bin/env python3
"""
Pass5 Step 1: 540 Coset -> Amplitude Dictionary
Co-Authored-By: Perplexity AI (Sonnet 4.6) <noreply@perplexity.ai>
"""
from math import comb, factorial
from itertools import product

q, v, k, mu = 3, 40, 12, 4
PSp43 = 25920
n_gluon = 14

print('540 Coset -> Amplitude Dictionary')
print('='*50)

assert PSp43 // 48 == 540
print(f'540 = |PSp(4,3)| / |S4| = {PSp43} / 48 = {PSp43//48}')
print(f'540 = 27 * 20 = dim(E6) * (v/2) = {27*20}')

# MHV frames: stabiliser = S3 x S1 of order 6
stab_MHV = factorial(3)
n_MHV = 540 // stab_MHV
print(f'\nMHV frames: 540 / {stab_MHV} = {n_MHV}')
print(f'C(14,2) - 1 = {comb(14,2)} - 1 = {comb(14,2)-1}')
assert n_MHV == comb(14,2) - 1, f'{n_MHV} != {comb(14,2)-1}'
print('90 = C(14,2) - 1: VERIFIED')

# Total BCFW = 2^11
total = sum(comb(11, j) for j in range(2, 10))
print(f'\nTotal BCFW = sum C(11,j) j=2..9 = {total} = 2^11 = {2**11}')
assert total == 2**11
print('2048 = 2^11: VERIFIED')
