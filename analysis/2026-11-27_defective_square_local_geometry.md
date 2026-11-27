# Square-lattice neighborhoods survive finite plaquette defects

The square-gluing threshold distinguishes exact global flatness from a disordered graph. It does not mark the point at which every local square-grid neighborhood disappears. In the connected permutation model with one supplied horizontal cycle, a uniformly chosen vertex typically has an exact edge-colored square-grid neighborhood on a growing radius, even conditional on a fixed nonzero number of bad plaquettes. This also holds on the nonflat branch of the critical window \(\beta=\log n+c\) for every fixed \(c>0\).

## A quadratic bound on defect neighborhoods

Set \(a(x)=x+1\), and let \(b\) be the vertical permutation. Let \(D\) be the set of vertices where one of the four signed commutations \(a^{\pm1}b^{\pm1}=b^{\pm1}a^{\pm1}\) fails. A failed equation for each of the inverse-sign combinations corresponds by a bijective change of base point to an original failure of \(ab=ba\), so \(|D|\le4k\) for \(k\) original defects.

Suppose a root is at distance \(j\) from \(D\). Reorder a shortest word to \(D\) by adjacent horizontal-vertical swaps. Every prefix shorter than \(j\) is outside \(D\), regardless of the ordering, so the swaps preserve the endpoint. The reordered word is a horizontal run followed by a vertical run; inverse steps can be canceled. Therefore the roots within distance \(R\) of \(D\) lie among the preimages of \(D\) under at most \(1+2R(R+1)\) canonical words. This bounds the excluded roots by \(4k[1+2R(R+1)]\), without using the exponential ball bound of a general degree-four graph. The result complements known Hamming stability of almost commuting permutations, which has a different conclusion about replacing the generators. [Arzhantseva and Păunescu](https://arxiv.org/abs/1410.2626)

## Short wraparound loops require a separate estimate

Even away from \(D\), a ball can be a thin quotient of the square lattice. To control that possibility, condition on any orbit \(b_s=a^s b_0\) under a global output translation. The conditional shift \(s\) is uniform because the plaquette-defect count is preserved. The displacement \(b_0(x)-x\pmod n\) is constant on each of at most \(K=\max(1,k)\) runs. Denote the offsets by \(d_i\). For a canonical return with horizontal net displacement \(u\) and \(v>0\) vertical steps,

\[
u+vs+\sum_i c_i d_i=0\bmod n,\qquad \sum_i c_i=v,
\]

where the nonnegative integers \(c_i\) count the vertical visits to each run. For fixed \(v\le R\) there are at most \((R+1)^{K-1}\) possible count vectors. For each vector, the number of shifts that can solve the congruence for some \(|u|\le R\) is at most \(2R+\gcd(v,n)\le3R\): eligible values of \(u\) lie in one residue class modulo \(\gcd(v,n)\), and each gives that many solutions. This bound does not require the itinerary to be independent of the shift. The union bound over \(v\) is \(3R^2(R+1)^{K-1}/n\). A loop with negative vertical net displacement can be reversed and reordered, and a purely horizontal nonzero return is impossible for \(R<n\).

To compare the induced ball of radius \(r\) with the square grid, take \(R=2r+1\), avoid \(D\) within that radius, and exclude all nonzero canonical returns of length at most \(R\). Every path in the ball can then be put in canonical order. Two charts colliding would produce a nonzero return of length at most \(2r\), and an extra edge produces one of length at most \(2r+1\). The bad-ball probability for a uniform root and shift is therefore

\[
O_k\!\left((r+1)^{\max(2,k+1)}/n\right).
\]

For fixed \(k\), this proves growing balls whenever \(r=o(n^{1/\max(2,k+1)})\). It is uniform in the original run lengths. It does not require the prescribed horizontal cycle to emerge dynamically.

## A growing diffusion window on the nonflat branch

In the previous square-gluing calculation, the \(c>0\) critical-window distribution has a uniform exponential tail in \(k\), bounded by \(\sum_{j>K}e^{-cj}/j\). Split at \(K\) proportional to \(\sqrt{\log n}\), with the proportionality chosen small enough, and take \(r=\lfloor\exp(A\sqrt{\log n})\rfloor\) for any fixed \(A>0\). The short-loop bound and the tail both vanish. The limiting nonflat probability is strictly positive at every finite \(c>0\), so conditioning on nonflatness preserves the conclusion.

On a good ball, the continuous-time return probability at its center differs from the square-grid return probability by at most \(\Pr[\operatorname{Pois}(4t)>r]\). Couple the walks at each jump until more than \(r\) steps have occurred. At the two times \(t=r/32\) and \(2t=r/16\), this tail decreases exponentially in \(r\), whereas the grid return probability behaves as \(1/(4\pi t)\). Thus the ratio of the return probabilities tends to two, giving two-dimensional return decay on a growing time scale for random roots on the nonflat branch. This is an intrinsic graph diffusion statement. It does not identify a Lorentzian light cone or a four-dimensional continuum.

The verifier checks signed defect counts, the defect-neighborhood bound, and full colored-ball isomorphism on shifted three- and five-defect examples through 65,537 sites. The finite controls use specified run sizes. The probability proof covers all run sizes in the stated shift ensemble. Run `python analysis/toe_20261127_defective_square_local_geometry.py`.
