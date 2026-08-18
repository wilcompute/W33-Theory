# Passes 7122–7129 — q=9 witness recovery, global-compatible LNS, blocker rigidity, and semilinear boundary

## Intake: all local-day commits reviewed

The Aug. 18 (America/New_York) commit frontier was read before extending it. The ten commits visible after local midnight were: the Pass4144 frontier-manifest reconciliation; BT1642; BT1643–1645; the Pass6144–6151 intake audit; Pass6152–6159; Pass6160–6167; the Pass7098–7105 reservation and correction packet; Pass7106–7113; and Pass7114–7121.

The durable lessons are unusually coherent. The Perplexity arithmetic was mostly correct while several physics framings were not; the targeted forced-arithmetic guard is useful while the broad guard was too noisy; a prior BT820 flag was retracted after the actual producer was read; alpha(W(3,3)) is exactly 7 and alpha(W(3,5)) exactly 18; Tallini improves the q=9 upper bound from the repo's 80 to 73; and, most importantly for this packet, the repo's q=9 lower bound 51 had no stored witness.

This packet attacks that missing-object problem first. A lower bound is a witness, not a number.

## Pass 7122 — the missing 51-point q=9 witness is now frozen

Using the exact GF(9)=F3[i]/(i^2+1) model already established by Pass7107, the producer reconstructs W(3,9) on 820 projective points, degree 90, and verifies all C(51,2)=1275 pairs of the frozen set are non-collinear.

Thus the repo now has an actual re-verifiable object for

\[
\boxed{\alpha(W(3,9))\ge 51}.
\]

The 51 coordinates are stored in `data/PART_W33_Q9_PARTIAL_OVOID_51.json`. No claim of optimality or novelty is made.

## Pass 7123 — exact blocker moments

For an outside point v define

\[
b(v)=|N(v)\cap S|.
\]

The exact blocker histogram of the frozen witness is

\[
\boxed{1^1,2^{22},3^{50},4^{102},5^{156},6^{120},7^{142},8^{107},9^{53},10^{16}}.
\]

It obeys the two SRG moment identities exactly:

\[
\sum_{v\notin S}b(v)=|S|k=51\cdot90=4590,
\]

and because every pair in S is nonadjacent and W(3,9) has mu=10,

\[
\sum_{v\notin S}\binom{b(v)}2=\binom{51}{2}\mu=1275\cdot10=12750.
\]

These are useful checksum identities for any future q=9 witness.

## Pass 7124 — maximality and the unique weak blocker

There are no zero-blockers. Therefore this particular 51-set is inclusion-maximal: no single outside point can extend it to 52.

Even more sharply, there is exactly one outside point with blocker count one. In canonical point indexing it gives the unique one-for-one move

\[
\boxed{80\longleftrightarrow40}.
\]

Swapping 80 out and 40 in produces a second valid 51-set.

## Pass 7125 — exact exchange rigidity through radius seven

An improving exchange is an independent outside set T for which the union of its blockers in S is smaller than |T|. Removing that blocker union and adding T increases the partial ovoid.

The verifier exhaustively searches this condition for |T|=1,...,8. No augmenting set exists. The search-node counts are

\[
1,1,25,116,629,3083,14892,69955.
\]

Therefore the witness admits

\[
\boxed{\text{no gain-one exchange removing at most seven incumbent points}.}
\]

This is much stronger than saying a heuristic happened to plateau at 51.

## Pass 7126 — global-compatible replacement LNS

The earlier LNS frees a region and only lets the residual solver choose replacement vertices inside that freed region. That is a legitimate but narrow move class.

The new neighborhood keeps a chosen core K subset S, then admits **every point of W(3,9)** compatible with K into the residual exact MILP. In symbols,

\[
C(K)=\{v\notin K:N(v)\cap K=\varnothing\}.
\]

The residual problem is solved exactly on C(K). This global-compatible neighborhood independently rediscovered a valid 51-set from a smaller incumbent before the witness was frozen. A further target-52 search did not find 52, but that negative search result is deliberately not promoted to an upper bound.

## Pass 7128 — the local one-swap component has exactly two vertices

The alternate witness obtained by 80<->40 has blocker histogram

\[
1^1,2^{24},3^{46},4^{102},5^{158},6^{122},7^{142},8^{103},9^{55},10^{16}.
\]

Its sole one-blocker move is the reverse swap. It is also exchange-stable through removal radius seven. Hence under one-blocker 1-for-1 moves the recovered witness sits in an isolated component of size two.

## Pass 7129 — outside-box semilinear falsifier

The nontrivial field automorphism of GF(9) is Frobenius

\[
x\mapsto x^3.
\]

Projectively it is an involutory automorphism of W(3,9). Applying it to the frozen witness gives another valid 51-point partial ovoid, but not the same one:

\[
|S\cap S^{(3)}|=4,
\qquad
|S\triangle S^{(3)}|=94.
\]

So this recovered 51-set does **not** descend setwise to the GF(3)-fixed substructure. This is a useful boundary against explaining this witness as a hidden GF(3) lift. It is only a statement about this witness, not about every possible size-51 witness.

## Literature boundary

The literature search found the modern general-construction paper of Ceria–De Beule–Pavese–Smaldore and the Tallini bounds already identified in Pass7114. It did not supply an exact classification of alpha(W(3,9)) in the searched primary literature. Accordingly this packet claims neither novelty nor optimality.

## Evidence firewall

Established: an explicit 51-point witness, pairwise verification, exact blocker histogram/moments, inclusion maximality, unique 1-swap, exchange rigidity through radius seven, the global-compatible search method, and the Frobenius-conjugacy facts.

Not established: alpha(W(3,9))=51, nonexistence of a 52-point partial ovoid, the q=9 interpolation value 52, or any physics consequence.
