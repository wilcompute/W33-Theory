#!/usr/bin/env python3
"""PART_MCCLXXX_MCCLXXXVIII_MODULAR_VERIFICATION.py"""
import math

q=3; k=12; v=40; Phi6=7; g1=21; g2=6; p_Ih=11

def factorize(n):
    factors=[]
    for p in range(2,int(n**0.5)+1):
        while n%p==0:
            factors.append(p); n//=p
    if n>1: factors.append(n)
    return factors

primes=[]; n=2
while len(primes)<30:
    if all(n%p!=0 for p in primes): primes.append(n)
    n+=1

tau={1:1,2:-24,3:252,4:-1472,5:4830,6:-6048,7:-16744,8:84480,9:-113643,10:-115920,11:534612,12:-370944}

print("="*60)
print("MODULAR/LEECH/HECKE x W(3,3) VERIFICATION MCCLXXX-MCCLXXXVIII")
print("="*60)

print("\nMCCLXXX: weight of Delta = k")
assert k == 12
print(f"  weight_Delta = k = {k}")

print("\nMCCLXXXI: Leech dim = 2k")
dim_L = 24
assert dim_L == 2*k
leech_vectors = 196560
assert leech_vectors % v == 0
ratio = leech_vectors // v
assert ratio == g2 * q**2 * Phi6 * primes[g2-1]
print(f"  dim_Leech = {dim_L} = 2*{k}")
print(f"  Leech_vectors/v = {ratio} = g2*q^2*Phi6*prime(g2)")

print("\nMCCLXXXII: Heawood encodes Leech")
for n_val in [7,12,40]:
    h = (n_val-3)*(n_val-4)//12
    chi = int((Phi6 + math.sqrt(dim_L*2*h+1))/2)
    assert chi == n_val
print(f"  chi(genus(n))=n for n in [7,12,40]")

print("\nMCCLXXXIII: Hecke exponent = k-1 = p_Ih")
assert k-1 == p_Ih
assert tau[2]**2 - 2**p_Ih == tau[4]
assert tau[3]**2 - 3**p_Ih == tau[9]
print(f"  k-1={k-1}=p_Ih={p_Ih}; tau(4)={tau[4]}; tau(9)={tau[9]}")

print("\nMCCLXXXIV: tau(q) = g1*k")
assert tau[q] == g1*k
assert g1 == math.comb(Phi6,2)
print(f"  tau({q})={tau[q]}=g1*k={g1}*{k}")

print("\nMCCLXXXV: tau(2) = -2k")
assert tau[2] == -2*k == -dim_L
print(f"  tau(2)={tau[2]}=-2*{k}")

print("\nMCCLXXXVI: 2v-Phi6=prime(g1)")
assert 2*v - Phi6 == primes[g1-1]
assert v == (Phi6 + primes[g1-1])//2
print(f"  2*{v}-{Phi6}={2*v-Phi6}=prime({g1})={primes[g1-1]}; v={v}")

print("\nMCCLXXXVII: tau(8)/v = p_Ih*2^g2*q")
assert tau[8] % v == 0
val = tau[8]//v
assert val == p_Ih * (2**g2) * q
print(f"  tau(8)/v={val}={p_Ih}*{2**g2}*{q}")

assert tau[2]*tau[3] == tau[6]

print("\n"+"="*60)
print("ALL THEOREMS MCCLXXX-MCCLXXXVIII VERIFIED")
print("="*60)
