# Pass 10957 — mu4 phases convert the plus/minus S4 Schur cocycles

Producer: `analysis/w33_pass10957_mu4_schur_cover_converter.py`

Certificate: `data/w33_pass10957_mu4_schur_cover_converter.json`

Regression: `tests/test_w33_pass10957_mu4_schur_cover_converter.py`

## 1. Extract the clock's own central-extension cocycle

The Pass-10951 clock group is

```text
GL(2,3) -> PGL(2,3) ~= S4
```

with central kernel ({+I,-I}).

For each of the 24 projective permutations, choose the lexicographically minimal matrix in its (pm I) pair. The section defines a Z2 cocycle (c_+) by

```text
s(sigma)s(tau)=(-I)^c+(sigma,tau) s(sigma tau).
```

All (24^3=13,824) cocycle identities are checked, and the resulting 48-element extension is mapped back to the original GL(2,3) on all (48^2) products.
Its order spectrum is

```text
1^1 2^13 3^8 4^6 6^8 8^12,
```

the frozen plus-cover clock profile.

## 2. One parity cup-square toggles the Schur cover

Let (epsilon:S4->F2) be permutation parity. Define

```text
c-(sigma,tau)
 = c+(sigma,tau) + epsilon(sigma)epsilon(tau) mod 2.
```

Again all 13,824 cocycle identities close.

The resulting 48-element extension has order spectrum

```text
1^1 2^1 3^8 4^18 6^8 8^12.
```

It has exactly one involution. This is the binary-octahedral / minus-cover fingerprint already independently frozen by Pass 363 as SmallGroup(48,28), whereas GL(2,3) is SmallGroup(48,29) with 13 involutions.
## 3. The cover difference becomes a coboundary over mu4

Embed the central (mu_2={+1,-1}) into (mu_4={1,i,-1,-i}). Define either conjugate one-cochain

```text
b+(sigma)= i^epsilon(sigma),
b-(sigma)=(-i)^epsilon(sigma).
```

For every one of the (24^2=576) ordered pairs,

```text
b(sigma)b(tau)/b(sigma tau)
 = (-1)^[epsilon(sigma)epsilon(tau)].
```

Therefore

```text
c- = c+ + delta b
```

after coefficient extension to mu4.

So the plus and minus double covers remain nonisomorphic as abstract central mu2 extensions, but their complex projective cocycles differ only by a mu4 phase gauge.
## 4. The missing +i,-i clock modes are exactly the local square roots of sign

The projective image of the order-eight clock generator is a four-cycle in S4. Its powers have parity word

```text
0,1,0,1.
```

On this C4 subgroup there are exactly two conjugate mu4 characters

```text
chi+(gbar)=+i,
chi-(gbar)=-i,
```

and both satisfy

```text
chi+^2 = chi-^2 = sign restricted to C4.
```

These are exactly the phase values of the missing Pass-10954 C8 characters (k=2,6).

This sharply improves the interpretation of those modes: their phases are precisely the square roots needed to toggle the plus/minus lifting convention on the projective clock subgroup.
## 5. Why this matters for the Albert bridge

Pass 10951 established that the finite clock is the plus Schur cover. Pass 10956 found the natural Albert Spin(9) half-turn exchanging the two Spin(8) half-spin modules; that half-turn squares to the central (-1), i.e. it has the local minus-cover lifting behavior.

Pass 10957 shows that this mismatch is not arbitrary:

```text
plus clock cocycle
  + parity cup-square
= minus-style cocycle,
```

and the difference is removed projectively by the determinant phase (i^epsilon).

Thus a mu4 phase is exactly what is required to pass between the two lift conventions while preserving the same projective S4 action.

## Boundary

The result is at the level of exact finite cocycles and complex projective representations. It does not make GL(2,3) isomorphic to the binary octahedral group, and it does not yet identify the Pass-10954 missing spectral modes with the Pass-10956 Albert half-turn as matrices. The missing object is still a carrier-level intertwiner.
