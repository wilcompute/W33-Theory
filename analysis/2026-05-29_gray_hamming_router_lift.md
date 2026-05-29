# Gray-Code / Extended-Hamming Router Lift Theorem

Date: 2026-05-29

This continues the Q4 hypercube-network theorem and adds the missing error-correction layer.

The important correction is:

```text
Gray code is not itself an error-correcting code.
```

Gray code gives unit-distance routing through Q4: adjacent clock states differ in exactly one information bit. That is excellent for local control and low transition cost, but it does not protect a state against bit errors.

The protected lift is:

```text
Q4 router state = 4 information bits
encode by the binary extended Hamming [8,4,4] code
```

Equivalently, this is the Reed-Muller code RM(1,3).

## Code parameters

The verifier uses a standard generator matrix for the binary extended Hamming code:

```text
[1 0 0 0 0 1 1 1]
[0 1 0 0 1 0 1 1]
[0 0 1 0 1 1 0 1]
[0 0 0 1 1 1 1 0]
```

It verifies:

```text
length = 8 = Phi6 + 1
dimension = 4
codewords = 16 = 2^4
minimum distance = 4
weight enumerator = 1 + 14 y^4 + y^8
self-dual over F2
doubly even
```

Thus the 16 Q4 router states lift to 16 protected 8-bit codewords.

## Gray clock lift

The Q4 Gray cycle gives a cyclic order on the 16 information states.

Before protection:

```text
one Gray step = one information-bit flip = Hamming distance 1 in Q4.
```

After encoding:

```text
one Gray step = distance 4 between [8,4,4] codewords.
```

The verifier checks that every adjacent state in the Gray clock lifts to a protected distance-4 transition:

```text
encoded step distances = 4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4.
```

So the clock is local in the Q4 router but protected in the encoded shell.

## Distance-4 shell

Among the 16 protected codewords, pairwise distances are only 4 or 8:

```text
distance 4 pairs = 112
distance 8 pairs = 8
```

The distance-4 graph is therefore:

```text
K16 minus the 8 complement pairs.
```

It has:

```text
16 vertices
112 edges
degree 14
diameter 2
```

So the protected shell is nearly complete: any code state can transition to 14 other code states at protected distance 4, with only its complement sitting at distance 8.

The Gray cycle is a Hamiltonian subcycle inside this distance-4 shell.

## Error-correction meaning

Since the minimum distance is 4:

```text
corrects 1 arbitrary bit error
detects up to 3 bit errors
```

The verifier also checks that all 8 single-bit error syndromes are unique and nonzero.

Thus the architecture is:

```text
Q4 Gray code = router clock
extended Hamming [8,4,4] = protected state shell
RM(1,3) = Reed-Muller / affine-function interpretation of same shell
```

## W33 bridge

The existing W(E6) minimal nonzero commutation count still factors as

```text
51840 = 40 * 16 * 81.
```

The 16 factor now has the strongest interpretation so far:

```text
16 = Q4 vertices
   = Cl4 basis blades
   = D8 Frobenius-square norm
   = number of [8,4,4] protected codewords.
```

And the code length satisfies

```text
8 = Phi6 + 1.
```

So the packet can now be read as:

```text
W33 anchor state
  -> Q4/Cl4 Gray router state
  -> [8,4,4] error-corrected codeword
  -> H1=81 signed phase-frame channel.
```

## Corrected architecture slogan

```text
Gray code supplies the clock.
Q4 supplies the interconnection network.
Cl4 supplies the 16-state algebraic basis.
The extended Hamming/RM(1,3) code supplies the error-correcting shell.
W33 supplies the ternary phase payload.
```

This is a genuine upgrade because it separates routing from protection instead of incorrectly treating Gray code itself as error correction.

## Honest boundary

This proves the finite coding/router layer. It still does not prove a physical decoder for the full W33 minimal logical surface. The next step is to test whether the [8,4,4] syndrome table can be fibered over the 40 W33 anchors and made compatible with the signed H1 phase-frame projector.
