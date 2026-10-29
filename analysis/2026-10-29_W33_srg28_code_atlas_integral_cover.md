# Spectral twins, binary CSS distances, integral E8 cover and phase-referenced test

**Date:** October 29, 2026. **Status:** exact computer-assisted finite-geometry and circuit certificates, no experimentally verified new physics.

## A complete control population: all 28 SRG(40,12,2,4)

E. Spence classified all **28** nonisomorphic strongly regular graphs of parameters (40,12,2,4) [EJC 7 (2000) R22](https://doi.org/10.37236/1500). We retrieved [the graph6 catalog compiled by Brendan McKay](https://users.cecs.anu.edu.au/~bdm/data/sr401224.g6), checked all 28 adjacency matrices satisfy their SRG common-neighbor counts and froze SHA256 `b899979459e6304bfff848d112d0ac8d738c837e5e21dc6e9d310a386aee8be6`.

Their **identical real adjacency spectrum** is 12 (multiplicity 1), 2 (24), and -4 (15). The SRG equation is `A^2 = 8I - 2A + 4J`, hence `A^2=0` over GF(2), so every graph defines an honest symmetric CSS stabilizer `im A` on 40 physical qubits. The logical space has dimension `40 - 2 rank_2(A)`.

Computed binary ranks occur with multiplicities 10:1, 12:2, 14:8, 16:17. Exhaustive, *full* 40-bit-syndrome meet-in-the-middle search of words of weight 1–6, explicitly excluding stabilizers, yields **exact** quantum code families:

| Number of graphs | CSS parameters |
|---:|---|
| 1 | [[40,20,4]] |
| 2 | [[40,16,4]] |
| 8 | [[40,12,4]] |
| 17 | [[40,8,6]] |

For every graph a minimum logical word of weight 4 or 6 was exhibited, and all smaller logical words were excluded. The method enumerates every support of size at most three and all disjoint pairs whose syndromes agree. Each weight up to six admits such a balanced partition. The full output includes one explicit logical support per graph.

**Distinctive W33 fingerprint:** the catalog has exactly two graphs with 40 four-cliques: index 26 has `rank_2(A)=10` and is the orthogonal GQ(3,3) dual; index 27 has `rank_2(A)=16` and is the symplectic W(3,3) point graph. Every other catalog graph has fewer than 40 K4. Thus the ordered pair **(rank_2(A), number of 4-cliques) = (16,40)** singles out W33 within the complete 28-graph control group. The dual has [[40,20,4]], while W33 has [[40,8,6]]. Sixteen non-W33 cospectral graphs also have [[40,8,6]], so W33's CSS parameters **alone** are not identifying.

This is not a first study of binary codes of these graphs; compare Crnković, Maksimović, Rodrigues and Rukavina, *Self-orthogonal codes from the strongly regular graphs on up to 40 vertices*, Advances in Mathematics of Communications **10** (2016), 555–582, [DOI](https://doi.org/10.3934/amc.2016026). The contribution is a completely reproduced *adjacency CSS logical-distance* atlas, its W33/dual code contrast and a catalog-wide control experiment. The source catalog is fetched separately, not redistributed.

## Integral E8 central extension and optical reference witness

The executable `analysis/w33_20261029_e8_cover_photonic_sign.py` constructs all **240 integral E8 roots** in the simple-root basis and groups them in 120 mod-two antipodal pairs. Each of the seven previously verified PSp4(3) binary generators is lifted constructively to an **integer** matrix preserving the E8 Cartan Gram form, using the tree of simple roots to fix signs. Choosing signs so each lift has order 3, the lifts generate the exact pullback of the order-25,920 PSp4(3) subgroup under `W(E8)->O8+(2)`. Because the explicit word of generator indices `(0,1,5,4)` squares to `-I8`, the integral subgroup has order exactly **51,840**. This proves the extension is **nonsplit**; the 270 rank-four involutions lift to order four and the 45 rank-two involutions to order two.

The matrix M of that order-four witness satisfies `M^T G M = G` but is not orthogonal under ordinary Euclidean mode amplitudes. Diagonalize and whiten the **positive-definite** Gram G: `O = G^(1/2) M G^(-1/2)`. Then `O^T O=I` and `O^2=-I`. An ordinary real 8-mode optical scatterer implementing O is decomposed into **28 adjacent-mode SU(2) elements**. With one coherent untouched reference mode (nine modes total), two passes cause an observable relative pi phase. In the ideal lossless, phase-locked interferometer, the reference **minus** output is 1 and **plus** output is 0. Without the reference, -I is global and cannot be measured.

This is a **standard quantum-optics reference interferometer**, not a discovery of E8 as a fundamental symmetry or a prediction beyond quantum mechanics. Loss/noise and calibration are experimental constraints not addressed by the ideal calculation.

## Reproduce

```powershell
# Download catalog as a separate research input, then check its SHA256
Invoke-WebRequest https://users.cecs.anu.edu.au/~bdm/data/sr401224.g6 -OutFile "$env:TEMP\sr401224.g6"
python analysis/w33_20261029_srg28_css_population.py "$env:TEMP\sr401224.g6"
python analysis/w33_20261029_e8_cover_photonic_sign.py
python -m unittest discover -s tests -p test_w33_20261029_srg28_cover.py -v
```

Prior repo dependencies: `data/w33_20261029_explicit_mod2_E8_isometry.json`; requires NumPy for the E8 interferometer. Finite graph catalog uses only the standard library. Evidence is exact finite computation against an external catalog; there is no full TOE claim.

## Best five independent future falsifiers

1. Complete the `W(3,7)` weight-10/12 exclusion and prove or disprove exact [[400,48,14]].
2. Compare the W33 versus all 27 cospectral controls under realistic waveguide disorder and full multiport tomography; the 4-clique invariant is an identifying *classical* control, not automatically a quantum advantage.
3. Specify a calibrated optical and/or matter-photonic encoding for the integral-cover witness, including a reference rail, measured phases, loss and control errors.
4. Search for an independently justified, local and energy-calibrated Hamiltonian—not an arbitrarily chosen polynomial in A.
5. Require one parameter-free observable that actually departs from standard quantum mechanics or established field theory before claiming a physical TOE breakthrough.


## Important same-order group distinction: two different 51,840s

The **integral lift** constructed here is a *non-split central extension* `2.PSp(4,3)` with center `{+I,-I}`, of order **51,840**. By the standard Schur-cover identification this is `Sp(4,3) ~= 2.U4(2)` (see [GAP Atlas character table](https://www.math.rwth-aachen.de/~Thomas.Breuer/ctbllib/ctbltoc/data/2.U4%282%29.html) and [LMFDB 51840.a](https://www.lmfdb.org/Groups/Abstract/51840.a)). Its 270 quotient involutions of the rank-four class lift to order four.

There is **another, non-isomorphic** group with the same order appearing elsewhere in this repository: `PGSp(4,3) ~= Aut(PSp(4,3)) ~= W(E6)`, the outer automorphism extension `PSp(4,3):2`. Its center is trivial. It must **not** be conflated with the central double cover `2.PSp(4,3)`: equality of cardinality 51,840 is *not* an identification. The distinction is physically relevant because the central minus sign is detectable only interferometrically relative to a reference, whereas a projective outer automorphism acts differently on the finite geometry. See also the [repository's stated group vocabulary](https://wilcompute.github.io/W33-Theory/) and [the standard E6 Weyl identification](https://oa.tib.eu/renate/bitstreams/6fb7e7a9-d01b-4f4c-85ac-5813e67933d8/download).

