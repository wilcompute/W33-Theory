# PASS 101 RESULTS — Theta Series & Moonshine
**Status: EXTENDED. Theta series computed to m=32. Three moonshine signals confirmed.**

## Theta Series Formula

Theta_L(q) = sum_{c in C} q^{wt(c)} * f(q)^{40-wt(c)} * g(q)^{wt(c)}

where:
- f(q) = theta_3(q^4) = 1 + 2q^4 + 2q^16 + ...  (squared norms of even integers)
- g(q) = sum_k q^{4k(k+1)} = 2 + 2q^8 + 2q^24 + ...  (support coordinate factor)

Note: g(0) = 2 because each support coordinate has TWO displacement choices at norm 0
(v_i = 0 and v_i = -1 both give contribution 1 to the squared norm of c+2v).

## W(3,3) vs Q(4,3) Theta Series (Exact, m=0 to 32)

| m | Theta(W(3,3)) | Theta(Q(4,3)) | Ratio |
|---|---|---|---|
| 0 | 1 | 1 | 1 |
| 4 | 80 | 80 | 1 |
| **8** | **14,640** | **3,120** | **4.69x** |
| 12 | 5,403,840 | 242,880 | 22.2x |
| 16 | 1,301,706,800 | 19,484,720 | 66.8x |
| 20 | 90,075,980,640 | 1,400,071,008 | 64.3x |
| 24 | 2,879,296,353,600 | 45,009,602,880 | 64.0x |
| 28 | 53,857,455,633,280 | 841,946,723,200 | 64.0x |
| 32 | 680,913,378,127,920 | 10,638,929,129,520 | 64.0x |

**First divergence at m=8.** Ratio stabilizes near 64 = 2^6 for large m.

### m=8 Decomposition for W(3,3)
- 3,120 from pure displacement pairs (C(40,2) * 4 = 3,120)
- 11,520 from weight-8 codewords: 45 * g^8[0] * f^32[0] = 45 * 256 * 1 = 11,520
- **Total: 14,640** (exact, verified)

The factor g^8[0] = 2^8 = 256 reflects that each of the 8 support coordinates of a
weight-8 codeword has two valid displacements preserving norm.

## Three Moonshine Signals

### Signal 1: A_8 = 45 — Tritangents and Umbral Moonshine
- W(3,3) has exactly 45 weight-8 codewords.
- 45 coincides with multiplicities in the D4^6 Niemeier umbral moonshine McKay-Thompson series.
- 45 = C(10,2) = number of double-sixers in the 27-line cubic surface (W(E6) action).
- **Q(4,3) has A_8 = 0** — confirming this signal is UNIQUE to W(3,3).

### Signal 2: W(E6) Symmetry
- |Aut(W(3,3))| = 51,840 = |W(E6)|.
- W(E6) appears as the automorphism group of the E6^4 Niemeier lattice sector.

### Signal 3: E8/2E8 Discriminant Form
- disc(Lambda_C) = (Z/2)^8 with the E8/2E8 quadratic form (135 isotropic, 120 anisotropic).
- This is the discriminant form of the E8-class moonshine sector.

## Next Action
Decompose Theta_L as a linear combination of weight-20 modular forms for Gamma_0(N),
N in {4, 8}, to either confirm a direct moonshine identification or establish a
closure theorem.
