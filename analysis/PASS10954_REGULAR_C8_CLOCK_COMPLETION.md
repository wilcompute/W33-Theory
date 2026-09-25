# Pass 10954 — regular C8 completion on the oriented A2^4 clock cover

Producer: `analysis/w33_pass10954_regular_c8_clock_completion.py`

Certificate: `data/w33_pass10954_regular_c8_clock_completion.json`

Regression: `tests/test_w33_pass10954_regular_c8_clock_completion.py`

## 1. The six-mode clock is exactly two Fourier modes short

Pass 10953 proved that the minimal doubled Pin clock has C8 character exponents

```text
{0,1,3,4,5,7}.
```

The only missing characters are

```text
{2,6} = {+i,-i}.
```

Adding those two one-dimensional characters gives every C8 character once. The resulting 8D representation has

```text
Tr(T^n) = 8,0,0,0,0,0,0,0
```

and admits eight mutually orthogonal clock-position states. The 6D clock has rank six on the same eight-position orbit and maximal off-diagonal overlap exactly 1/3.
## 2. The completion already exists inside the E8/A2^4 orientation geometry

The older Pass 7409 fibre starts with four A2 orientation signs,

```text
F2^4,
```

and identifies simultaneous inversion

```text
x ~ x+1111
```

to obtain the eight Eisenstein W33 leaves through one fixed A2^4 subsystem,

```text
F2^4/<1111> ~= F2^3.
```

For the exact Pass-10951 clock generator

```text
g = [[0,1],[1,1]],
```

the frozen tetracode monomial action is

```text
coordinate permutation (4,1,2,3)
with one sign flip.
```

On the sixteen oriented sign states this action has exactly two disjoint cycles of length eight.
Moreover,

```text
g^4 x = x+1111
g^8 x = x.
```

Thus four ticks are literally the global-inversion deck transformation of the oriented cover. After quotienting that deck map, the two eight-cycles become the already-certified two four-cycles on the eight-leaf fibre.

Label either oriented eight-cycle by successive clock powers. Its permutation matrix is the regular C8 shift. The producer constructs an explicit unitary intertwiner from the abstract spectral completion to this repo-native permutation carrier.

So the regular clock completion is not an arbitrary appended two-dimensional space: it is already present as either oriented lift of one projective four-cycle in the A2^4 leaf geometry.

## 3. The 6D Pin clock embeds exactly into that regular orbit

Diagonalizing the repo-native regular shift and the 6D Pin clock by C8 character gives an explicit isometry

```text
W : C^6 -> C^8
```

with

```text
T W = W D.
```

The image contains precisely the character modes

```text
k = 0,1,3,4,5,7,
```

and its orthogonal complement is exactly

```text
k = 2,6.
```

The full 8D completion intertwiner and the 6D compressed intertwiner both close numerically below 1e-8.
## 4. Four ticks separate deck parity from the missing modes

The deck involution is T^4. Its eigenspaces are

```text
deck-even: k even = {0,2,4,6}, dimension 4
deck-odd : k odd  = {1,3,5,7}, dimension 4.
```

The six-mode Pin clock contains

```text
deck-even rank 2: k={0,4}
deck-odd  rank 4: k={1,3,5,7}.
```

Therefore the missing +i and -i modes, k={2,6}, are both **deck-even**.

This is an important correction: the missing pair is not the orientation-odd/chiral sector of the A2^4 double cover. It descends to the unoriented leaf quotient. The independent temporal Weil atlas also contains phase values +/-i, but equality of phase values is not an objectwise carrier identification.
## 5. One C2 character now welds three exact layers

Exhaustion of all 48 tetracode/clock elements in GL(2,3) gives

```text
det = +1: 24/24 preserve orientation parity
det = -1: 24/24 flip orientation parity.
```

No exceptions occur.

Earlier repo results independently identify the same determinant character as:

- the unitary versus antiunitary extended-Clifford character;
- the Hesse finite spinor-norm character;
- for the order-eight clock, the even/odd complete-positivity grading.

Pass 10954 adds the E8/Fano statement:

```text
det = +1  <-> preserves the K4,4 bipartition
det = -1  <-> swaps the two bipartition classes.
```

Thus the CP/Pin grading and the oriented-A2^4/Fano grading are the same character on the shared 48-element tetracode automorphism group.
## 6. Quantum-clock interpretation

The regular C8 representation is exactly the finite-group structure used by a canonical finite quantum reference frame: the clock-position basis is permuted transitively by C8, while the Fourier basis carries all eight characters.

This also matches the standard finite Salecker-Wigner-Peres clock architecture: equally spaced Fourier/energy modes generate a cyclic shift through orthogonal time states. Here the new content is not that general construction, but that the W33/E8 orientation cover supplies an exact C8 carrier selected by the already-derived clock generator.

The 6D Pin clock is therefore a spectrally compressed finite clock. Its residual 1/3 overlap is exactly the aliasing produced by deleting the two k=2,6 Fourier modes.

## Boundary

This is a finite representation, coding, E8-orientation and quantum-reference-frame theorem. It does not prove that the oriented A2^4 cover is physical spacetime, that one abstract algebraic tick is laboratory time, that the two C8 orbits are past and future, or that the missing deck-even modes are physical particles or temporal chirality.
