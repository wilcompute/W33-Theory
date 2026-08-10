# Passes 4793–4800 — executed outcomes

## 4793 — q=7 minimum shell closes at the BLT-equivalence level

Pass 4754 gives `d(ker_F2 A_*(W(3,7)))=8`; Pass 4778 identifies equality with BLT-sets. Anton Betten's complete q=7 BLT census has exactly two full projective-orthogonal equivalence classes, Linear and Fi/K2, with stabilizer orders 5376 and 384. Since `|PΓO(5,7)|=276,595,200`, their class sizes are 51,450 and 720,300, for a complete shell count 771,750 at this equivalence level.

Boundary: the BLT classification is prior art; we transfer it to the line-kernel shell through the independently proved minimum-word=BLT theorem. We do not promote a finer PSp orbit split without an independent index-two stabilizer certificate.

## 4794 — covering radius narrows to 14 or 15

For an H10 coset, let `s` be the number of the 270 weight-4 dual checks with odd overlap. Pass 4781 proves `s<=179`. The fourth Krawtchouk moment gives

`sum_{c in H10} K4(wt(x+c)) = 1024(270-2s)`.

If an even coset had minimum at least 16, complement symmetry and OA strength three force

`A16=A24=a`, `A18=A22=1280-4a`, `A20=6a-1536`, with `256<=a<=320`.

The K4 equation then gives `a=1760-8s`, while `s<=179` forces `a>=328`, contradiction. Therefore every even coset has minimum at most 14. The explicit distance-14 witness remains, so

`14 <= rho(H10) <= 15`.

Only an odd distance-15 coset can still make rho=15. A separate exact 40-binary-variable/1024-constraint MILP producer is installed to decide that final case; no exact equality is promoted unless that solver returns feasible or infeasible decisively.

## 4795 — the 8/9 outer swap is a global orientation torsor

The 45-point quotient has 27 maximal K5 lines, three through every point. For a quotient point, the PSp stabilizer has order 576 and induces `C3` on those three lines; the full PGSp stabilizer has order 1152 and induces `S3`.

Hence a cyclic order chosen on one local three-line pencil propagates well-definedly to all 45 points under PSp. There are exactly two opposite global orientation sheets. PSp preserves each sheet; an outer element reverses it.

For ordered residue-triangle pairs on distinct K5 lines sharing exactly one quotient point, the cold orbital 1 occurs with both orientation signs, while after removing that cold sector the two signs distinguish the paired orbitals 8 and 9. Thus the outer `8<->9` action is a literal orientation reversal, with an explicit boundary: orientation is not itself the cold selector.

No H^2 claim is made.

## 4796 — the 270 carrier is intrinsic to GQ(4,2)

Starting from Q^-(5,2) alone (no W33 40-line coordinates), the 45 totally singular lines form the point graph `SRG(45,12,3,3)`. It has exactly 27 maximal K5s, every point lies on three, and every graph triangle lies in a unique K5. Therefore

`27 * C(5,3) = 270`

gives the complete carrier intrinsically. Equivalently, every triangle is the complement of a duad in its unique K5.

Inside each K5, joining two triangles when their intersection has size one gives Petersen; the 27 components produce all 405 hot edges.

The triangle hypergraph is lossless: each original quotient point is recovered as its 18-triangle star, and two recovered points are adjacent exactly when they co-occur in three carrier triangles. Thus the original 45-point SRG is reconstructed exactly from the 270 carrier.

The oriented 8/9 split needs one of the two Pass4795 orientation sheets, but no W33 coordinates.

## 4797 — explicit cube-triality -> F4/E6 crosswalk

The new 45-point source is the quotient of the 135 dependency cubes by their three-cube W(D4) triality packets. The independent target is BT167/168's index-45 F4-normalizer compiler quotient, already certified as GQ(4,2).

The new producer builds both finite graphs and uses an explicit graph isomorphism, then verifies that the displayed 45-point map carries all 27 maximal K5 lines and therefore all 270 triangles. BT169 already supplies the second explicit line-preserving leg from the F4 quotient to the older W33 center-quad/E6 quotient.

So the structural chain is now

`dependency cubes / W(D4) packets -> GQ(4,2) -> F4-normalizer quotient -> center-quad/E6 carrier`,

with explicit finite crosswalks rather than shared orders.

Boundary: the quotient forgets the central-vs-outer 51840 extension distinction. The old tomotope `192` coincidence remains firewalled by the existing tomotope-H obstruction; no tomotope=W(D4) identity is revived.

## 4798 — bonkers: characteristic-3 triangle incidence code

Let B be the 45x270 point-triangle incidence matrix of the intrinsic carrier. Each point lies in 18 triangles; adjacent quotient points lie together in 3 triangles; nonadjacent points in none. Hence

`B B^T = 18 I + 3 A45`.

Modulo 3 this vanishes. The only F3 row dependency is the global all-point sum: on any K5, requiring every 3-subset sum to zero forces all five point coefficients equal, and GQ connectedness propagates that constant globally. Therefore

`rank_F3(B)=44`, while `rank_F2(B)=rank_F5(B)=45`.

This produces a self-orthogonal length-270 qutrit code of dimension 44.

## 4799 — bonkers: exact [270,44,18]_3

On one five-point K5, exhaustive coefficient types over F3 give local triangle weights only 0, 6, or 9; weight zero is exactly a constant point pattern.

Delete the nonconstant GQ lines. The remaining constant lines connect points that must have equal coefficients. An exact finite cut census shows that deleting one or two of the 27 lines never disconnects this equality graph. The 45 minimum cuts of size three are exactly the three-line pencils through individual quotient points, with component profile `1+44`.

Therefore every nonzero global word uses at least three nonconstant lines and has weight at least `3*6=18`. A one-point perturbation attains 18 on its three incident lines. Thus

`C_triangle = [270,44,18]_3`,

with exactly 90 minimum words: 45 point choices times two nonzero F3 scalars.

## 4800 — bonkers: intrinsic qutrit [[270,182,4]]_3 CSS code

Because `B B^T=0 mod 3`, take `H_X=H_Z=B`. Both ranks are 44, so

`k = 270 - 44 - 44 = 182`.

The dual code has no word of weight 1 or 2 because the triangle columns are distinct nonzero 0/1 weight-3 vectors and no two are nonzero scalar multiples over F3. A weight-3 dependency is also impossible: three same-sign columns would have to have identical supports, while a two-versus-one sign pattern either produces an uncancellable coefficient 2 on an overlap or requires one weight-3 column to cancel six disjoint coordinates.

A weight-4 dual word exists inside every K5: choose four of its five points and sum the four triangle columns obtained by omitting one point. Every chosen point occurs three times, hence the sum is zero mod 3. Thus `d(C_triangle^perp)=4`. Since `d(C_triangle)=18`, these weight-4 words are outside the stabilizer row space.

Therefore the intrinsic triangle carrier supports

`[[270,182,4]]_3`.

Boundary: this is a finite qutrit CSS/stabilizer theorem. No hardware locality, threshold, microscopic Hamiltonian, or physical energy scale is inferred.

## Evidence boundary

Primary producers are `analysis/w33_pass4793_*.py` through `analysis/w33_pass4800_*.py`; frozen certificates live under `data/PART_W33_PASS4793...` through `PART_W33_PASS4800...`. The heavy PSp/PGSp and F4 crosswalk producers are rerun by `.github/workflows/w33_pass4793_4800_triangle_css.yml`, which preserves execution logs before enforcing success. Pass4794's exact distance-15 MILP is deliberately non-promotional until it terminates decisively.
