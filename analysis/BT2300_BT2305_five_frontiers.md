# Passes 2300–2305 — divisible ovoid codes, complete quadratic Hom bases, Weil inversion, verified RTL, and nonregular spectra

## Pass 2300 — the Ree–Tits `1 mod 9` law is a divisible-code theorem

The q=27 Ree–Tits ovoid was reconstructed in `PG(4,27)` from

`g(x,y)=-x^21-y^9`

over `GF(27)=F_3[t]/(t^3+2t+1)`. Every one of the 551,881 projective hyperplanes was evaluated. The complete intersection spectrum is

| section size | number of hyperplanes |
|---:|---:|
| 1 | 730 |
| 10 | 4,563 |
| 19 | 96,174 |
| 28 | 408,294 |
| 37 | 36,504 |
| 46 | 4,914 |
| 55 | 702 |

All seven values are `1 mod 9`. Equivalently, the five homogeneous coordinate rows generate a projective `[730,5]_27` code with nonzero weights

`675,684,693,702,711,720,729`.

The gcd is exactly 9, so the code is 9-divisible but not 27-divisible. The first three Pless factorial moments and the total `27^5` codeword count were checked exactly. This is the structural explanation of the observed congruence: a hyperplane section has size `730-w`, where `w` is a codeword weight.

The universal theorem for arbitrary ovoids of `Q(4,p^h)` supplies only the weaker congruence `1 mod p`. The stronger `1 mod 9` statement is therefore recorded as an exhaustive theorem for this q=27 coordinate object, not as an unproved universal law.

## Pass 2301 — the full quadratic algebra has dimension 50

The literal signed 240-edge representation and its target-identified projectors were reconstructed over `GF(101)`. Signed orbits of edge triples give compressed integral tensors. Exact output-span and independence tests produce complete bases

| target | `Sym^2(90)` | `Lambda^2(90)` |
|---:|---:|---:|
| 15 | 3 | 3 |
| 24 | 6 | 4 |
| 30 | 5 | 5 |
| 81 | 12 | 12 |

Thus

`dim Hom_PSp(Sym^2(90),15+24+30+81)=26`

and

`dim Hom_PSp(Lambda^2(90),15+24+30+81)=24`.

The complete PSp-equivariant quadratic algebra has dimension 50.

The outer similitude splits every multiplicity space. Its even half is

| target | symmetric even | alternating even |
|---:|---:|---:|
| 15 | 3 | 0 |
| 24 | 5 | 0 |
| 30 | 3 | 2 |
| 81 | 7 | 5 |

which is exactly the target-identified Pass-2200 table. The previously unrecorded outer-odd half is

| target | symmetric odd | alternating odd |
|---:|---:|---:|
| 15 | 0 | 3 |
| 24 | 1 | 4 |
| 30 | 2 | 3 |
| 81 | 5 | 7 |

so the outer-even and outer-odd sectors both have dimension 25. The earlier table was not wrong as a PGSp table; it was incomplete as a PSp table.

The simultaneous `mu6` input action factors to order three on bilinear maps. Its fixed dimensions and rotation-pair counts were computed exactly, and the outer involution conjugates the phase action to its inverse. Every listed basis tensor is surjective onto its irreducible target. These are allowed intertwiners, not physical coupling constants.

## Pass 2302 — q=7 and q=11 close on the canonical Weil family

For each q in `{7,11}`, use the Schrödinger Weil representation on functions on `F_q^2`. Parity gives the canonical even and odd constituents

| q | even complex dimension | odd complex dimension |
|---:|---:|---:|
| 7 | 25 | 24 |
| 11 | 61 | 60 |

The similitude `h=diag(I_2,-I_2)` has nonsquare multiplier `-1`. Entrywise complex conjugation implements its action on the standard generators:

- chirp `B` is sent to chirp `-B`;
- the determinant-one Levi permutation is fixed;
- the normalized Fourier operator is sent to its inverse.

The maximum numerical generator-identity residual is below `1.1e-13`. On realification, complex multiplication `J` and conjugation `K` satisfy

`J^2=-I`, `K^2=I`, `KJK=-J`,

so they generate `D4` of order eight on each parity constituent. This closes the two-i inversion theorem objectwise for a canonical q=7/q=11 representation family. It does not identify those constituents with the q=3 signed-edge 90.

## Pass 2303 — real open-source HDL verification

The tool-friendly RTL consists of

- a packed 36-lane signed spread mixer;
- the faithful `D24=C12:C2` phase action;
- a wrapper implementing the shared C4/C6 command map;
- exhaustive Icarus simulation;
- Yosys SAT properties for `A^2=9I+6J`, D24 associativity, and the `(step4,step6)=(2,3)` kernel;
- generic, iCE40 and ECP5 synthesis commands.

The observable pull-request workflow is `Pass 2303 hardware toolchain`. Tool versions, proof logs, synthesis logs and JSON netlists are retained as a workflow artifact. Exact cell counts and conclusions are frozen only after the workflow completes; no fabricated-device timing, power or area is inferred from generic synthesis.

## Pass 2304 — four q=27 spread families have distinct spectra

The complete hyperplane and regular-section spectra were computed for four standard coordinate families:

1. regular: `g=-nx`;
2. Kantor: `g=-nx^3`;
3. Thas–Payne: `g=-nx-(n^{-1}x)^3-y^9`;
4. Ree–Tits: `g=-x^21-y^9`.

All four have section sizes congruent to one modulo nine, but the spectra are pairwise different.

The regular elliptic section lies in a hyperplane, giving a 27-divisible `[730,4]_27` two-weight code. The three nonregular ovoids span `PG(4,27)` and give pairwise distinct, exactly 9-divisible `[730,5]_27` codes.

The numbers of possible intersections with regular spreads, including the self-intersection where applicable, are

| family | number of values |
|---|---:|
| regular | 3 |
| Kantor | 5 |
| Thas–Payne | 7 |
| Ree–Tits | 6 |

This replaces a single counterexample by an exact four-family taxonomy. It is not a classification of all symplectic spreads.

## Evidence boundary

The finite-field coordinate families, ovoid/spread correspondence, Weil representations, extended similitude action and divisible-code language retain their literature ownership. The repository contribution is the unified exact census, the complete signed-orbit Hom bases, the objectwise q=7/q=11 verification, and the executable hardware proof path.

No code weight, Hom-space multiplicity, Weil constituent, FPGA cell, phase state or intersection number is identified with a measured particle, coupling, charge, colour, generation, neutrino, or spacetime degree of freedom.
