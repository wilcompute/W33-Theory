# CORRECTION NOTICE — RETRACTED k=9 portions superseded by Passes 1310–1319

**Active theorem state:** the literal carrier has 26 A5/S5 orbitals, not 9. The proposed vector `(432,4,0,1,1)` has Burnside value `43/5`. Passes 1260 and 1261 below are retracted. Passes 1258, 1259, and the independent shifted-adjacency theorem in Pass 1262 remain historical claims only to the extent supported by their own exact witnesses. Use `PASS1315_1319_EXACT_FRONTIERS.md` and `data/w33_pass1315_1319_exact_frontiers.json` for the active replacement.

---

# Passes 1258–1262: 27-Line Embedding, Species-20 Scaffold, A5 Fixed Points, Hecke Constants, Universal Shifted-Adjacency Theorem

Date: 2026-07-28

## Pass 1258 — 27-line embedding construction

The canonical 5-step embedding protocol for E: Q^27 -> Q^480 is written, with the structural prediction that the 27-line frame projects to a 20-dim PSp(4,3)-submodule inside the 201-dim P1 packet.

## Pass 1259 — species-20 AtlasRep execution scaffold

The complete GAP script and output schema for the AtlasRep-backed species-20 execution are written; all 400 matrix units can now be generated once the GAP+AtlasRep environment is live.

## Pass 1260 — A5 classwise fixed-point counts

The Burnside equation yields a contradiction when orbit count = 5, resolving to k=9 as the candidate number of A5-orbits on the 432-point carrier. The candidate fix data (fix(2A)=4, fix(3A)=0, fix(5A)=fix(5B)=1) satisfies the Burnside equation exactly.

## Pass 1261 — exact Hecke structure constants

Using the k=9 candidate orbit data, the spherical Hecke algebra has candidate dimension 9 and the full pair-orbit Hecke algebra has candidate dimension computed from the pair-Burnside sum.

## Pass 1262 — universal shifted-adjacency non-isomorphism theorem (EXACT-9)

The universal theorem is proven algebraically: for SRG(40,12,2,4), the Hashimoto packet family of A+delta*I is non-isomorphic to the original for every nonzero integer delta. The proof reduces to showing the leading eigenvalue equals 11 iff delta=0, which follows from a clean quadratic identity.
