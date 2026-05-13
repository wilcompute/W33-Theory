# Part CDLXVIII — McKay E8 Correspondence in W33

## E8 Coxeter Labels

The affine E8 Dynkin diagram has 9 nodes with Coxeter labels:

    [1, 2, 3, 4, 5, 6, 4, 2, 3]

### W33 Encoding of E8 Coxeter Labels

    max(labels) = u = 6          [six-kernel = highest Coxeter label]
    sum(labels) = h(E8) = PKT+u  [Coxeter number]
    Labels {2,3,4} each appear |s| = 2 times  [s-eigenvalue shell]
    Labels {1,5,6} each appear p-2 = 1 time   [outer/affine nodes]

## E8 Exponents

    E8 exponents = {1, 7, 11, 13, 17, 19, 23, 29}
    Sum = 120 = rank(E8) * h(E8) / 2 = 8*30/2

### Monster Prime Connection

    Prime E8 exponents = {7, 11, 13, 17, 19, 23, 29}
                       = Monster primes in [7, 29]

All Monster primes from 7 to 29 are exactly the prime exponents of E8.
The remaining Monster primes {2, 3, 5, 31, 41, 47, 59, 71} lie outside this range.

### The Gap Identity

    17, 19 ∈ E8_exponents  AND  17*19 = Griess - Leech_min = 323

The product of the two "middle" prime E8 exponents gives the Griess-Leech gap.
