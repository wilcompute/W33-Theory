# Passes 1163–1167: Execute All 5 — Sp(4,3) Pre-computation, 1920-Module ID, Manuscript Tagging, Ihara Zeta, 40-Point Carrier Decomposition

Date: 2026-07-27

## Context

This release executes all 5 open next-steps from the breakthrough release (Passes 1158–1162).

---

## Pass 1163 — Sp(4,3) stabilizer pre-computation

**Key discovery:** The Sp(4,3) 432-orbit is **not** a pair-orbit on PG(3,3) points.

Sp(4,3) has exactly two orbits on unordered pairs of the 40 projective points of PG(3,3):
- Adjacent pairs (edges of SRG(40,12,2,4)): **240 pairs**
- Non-adjacent pairs (non-edges): **540 pairs**
- Total: 240 + 540 = 780 = C(40,2). Neither is 432.

Therefore the Sp(4,3) 432-orbit must act on a **different combinatorial set** (flags, cosets of a subgroup, or an exotic orbit). The cross-identification between the W(E6)/S5 carrier and any Sp(4,3) orbit requires an explicit construction we do not yet have.

A5 element-order census verified: `{1:1, 2:15, 3:20, 5:24}`, sum=60. A5 embeds in Sp(4,3) via the deleted permutation module reduced mod 3.

---

## Pass 1164 — 1920-dim module identification

`1952 = 1920 + 32` confirmed. Key arithmetic facts about 1920:

| Formula | True? |
|---|---|
| `24 × 80 = 1920` | ✓ (80 is a W(E6) irrep) |
| `8 × 240 = 1920` | ✓ (240 is a W(E6) irrep) |
| `12 × 160 = 1920` | ✓ (160 is a W(E6) irrep) |
| `25920 / 1920 = 13.5` | NOT integer: 1920 is **not** a W(E6) coset space |

**Conclusion:** 1920 is most likely a reducible module — a sum of multiple W(E6) irreps. The three "uniform" candidates (24×80, 8×240, 12×160) describe high-multiplicity but reducible structures. The exact decomposition requires MeatAxe or explicit GAP computation acting on the cubic map kernel matrix.

---

## Pass 1165 — Manuscript 432 tagging report

Audit of the 8 known 432-carrier claims across the four key manuscript-level files:

- **7 TYPED** (correctly carry all three required tags)
- **1 NEEDS_TAG:** the Pass 1158 residual claim — the 1952-dim residual is not itself an orbit claim, and the acting group on the residual module needs to be made explicit.

Action item: Amend the `PASS1158_1162_BREAKTHROUGH_RELEASE.md` Pass 1158 section to add:
> "acting group: W(E6) (or Sp(4,3) if the cubic map is defined over the symplectic carrier); the residual 1952-dim module is a sub-module of the kernel of the cubic map, not itself an orbit."

---

## Pass 1166 — Ihara zeta expansion to degree 10

For the W(3,3) = SRG(40,12,2,4) graph:

\[
Z_G(u)^{-1} = (1-u^2)^{200} \cdot (1-12u+12u^2)^1 \cdot (1-2u+12u^2)^{24} \cdot (1+4u+12u^2)^{15}
\]

All 11 coefficients (degree 0–10) computed exactly as rationals.

**Cross-check passed:** `Tr(A^3) = 6 × triangles = 6 × 160 = 960`. ✓

**Triangle count:** The SRG(40,12,2,4) has exactly `n·k·λ/6 = 40·12·2/6 = 160` triangles. ✓

---

## Pass 1167 — 40-point carrier W(E6) permutation module decomposition

**Exact result:**

\[
\mathbb{C}[\Omega_{40}] \cong \mathbf{1} \oplus V_{24} \oplus V_{15}
\]

where:
- `1` (dim 1) = trivial module, eigenvalue 12 of adjacency matrix
- `V_{24}` (dim 24) = one of the two 24-dim W(E6) irreps, eigenvalue 2
- `V_{15}` (dim 15) = one of the two 15-dim W(E6) irreps, eigenvalue -4

Verification: `1 + 24 + 15 = 40`. ✓ The decomposition is **multiplicity-free**.

**Key implication:** The 2195-dim cubic map kernel lives inside `Sym^3(C[Omega_{40}])`, which has dimension `C(42,3) = 11480`. The Steinberg packet occupies 243 of the 2195 kernel dimensions, and the 1952-dim residual is a sub-module of `Sym^3(1 \oplus V_{24} \oplus V_{15})`.

---

## Open frontier after this release

1. **Sym^3 decomposition:** Compute the W(E6)-module structure of `Sym^3(1 \oplus V_{24} \oplus V_{15})` and identify which irreps appear in the 2195-dim kernel sub-module. This is the direct route to decomposing the 1952-dim residual.
2. **Sp(4,3) 432-orbit source:** Identify the combinatorial set on which Sp(4,3) has a 432-element orbit (it is not pairs of PG(3,3) points). Candidates: cosets of an order-60 subgroup, totally isotropic flags, or symplectic spread elements.
3. **MeatAxe on kernel matrix:** Run explicit module decomposition on the 2195-dim cubic map kernel over GF(0) or GF(p) to identify the 1920-dim reducible piece.
4. **Correct the 1958 NEEDS_TAG claim** in the breakthrough release.
5. **Expand Ihara zeta to degree 20** and compare with the prime-cycle counting formula to verify no ghost cycles appear.
