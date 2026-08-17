# Passes 5888–5895 — Ihara identity correction and physical firewall

## Executive correction

Pass5880–5887 is superseded. It conflated three distinct objects:

1. the canonical W(3,3) collinearity graph, SRG(40,12,2,4);
2. the separate 4-regular signed 40-line/Levi mesh used by Pass5706;
3. a new 33-vertex circulant surrogate with jumps ±1 and ±11.

The third object was labelled W33 without an isomorphism certificate. Direct replay shows it is 4-regular on 33 vertices with 66 edges and has a nontrivial adjacency eigenvalue of absolute value 3.682507..., exceeding 2 sqrt(3). It is therefore not even Ramanujan in the 4-regular sense.

## Pass5888 — canonical graph identity

Rebuilding W(3,3) from the symplectic form on PG(3,3) gives exactly

- v=40,
- k=12,
- lambda=2,
- mu=4,
- |E|=240.

The SRG relation gives adjacency spectrum

12^1 + 2^24 + (-4)^15.

## Pass5889–5890 — exact Hashimoto/Ihara spectrum

For the canonical collinearity graph, the nonbacktracking operator has 480 directed-edge states and outdegree 11. Ihara–Bass gives

    det(I-uB)
      =(1-u^2)^200
       (1-12u+11u^2)
       (1-2u+11u^2)^24
       (1+4u+11u^2)^15.

Thus

- 11 occurs once;
- +1 occurs 201 times;
- -1 occurs 200 times;
- 1 ± i sqrt(10) occur with multiplicity 24 each;
- -2 ± i sqrt(7) occur with multiplicity 15 each.

The salvaged equal-modulus theorem is therefore precise:

> The 78 adjacency-induced nontrivial Hashimoto modes have common modulus sqrt(11).

This statement explicitly excludes the structural ±1 modes and the Perron mode 11.

## Pass5891 — phase-equidistribution refutation

The 78 modes have only four distinct phases, with multiplicities 24,24,15,15. A finite phase multiset of four repeated values is not an equidistributed modal phase sequence. Prime-geodesic asymptotics do not imply equidistribution of the finite Hashimoto eigenphase multiset.

Therefore the Pass5880–5887 FSR-equidistribution statement is withdrawn.

## Pass5892 — surrogate audit

The Pass5880 verifier's `build_w33_adjacency()` literally constructs the circulant-like graph C_33({±1,±11}). Its exact basic census is

- 33 vertices,
- degree 4,
- 66 edges,
- largest nontrivial adjacency absolute value ≈3.682507,
- 4-regular Ramanujan bound 2 sqrt(3)≈3.464102.

So it cannot certify any theorem about canonical W(3,3).

The same verifier also obtains only two Bass roots per adjacency eigenvalue and does not add the structural ±1 spectrum of multiplicity m-n. That is why its eigenvalue count is not a full Hashimoto spectrum.

## Pass5893 — graph namespace separation

The repo must keep separate identifiers:

- `W33_collinearity`: 40 vertices, degree 12, q_nb=11;
- `signed_Levi_mesh_40`: the 4-regular signed/twisted mesh from Pass5706, q_nb=3;
- `C33_pm1_pm11`: the erroneous 33-vertex surrogate, degree 4, q_nb=3.

The Pass5706 equalized-Q statement may remain attached to its own signed 4-regular mesh certificate. It must not be transferred to the W33 collinearity graph by name alone.

## Pass5894 — physical firewall

Ihara/Hashimoto theory supplies dimensionless graph spectral data. It does not, by itself, determine:

- physical free spectral range;
- Fabry–Perot finesse;
- Shannon channel capacity;
- absolute decay/Q or uniform physical loss.

Those require a separately specified propagation/coupling model: edge lengths or delays, phase dispersion, coupler amplitudes/losses, boundary conditions, and a map from graph spectral parameter to physical frequency.

Accordingly, formulas such as `FSR=log(q)/tau_rt`, `F=pi sqrt(q)/|1-q|`, and the derived channel-capacity expression are not promoted by this packet.

## Pass5895 — verdict

Pass5880–5887 is **SUPERSEDED/QUARANTINED**.

What survives is mathematically stronger and cleaner:

- exact W33 graph identity;
- exact 480-dimensional Hashimoto factorization;
- exact 78-mode common-modulus shell sqrt(11);
- explicit separation from the q_nb=3 signed 40-line mesh;
- a fail-closed physics boundary preventing graph-valence numerology from becoming hardware claims.
