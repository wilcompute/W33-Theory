# An exact logarithmic threshold for square-cell gluing

The higher-valence entropy bound leaves open whether a concrete local action can supply the required \(n\log n\) contrast. Here a plaquette penalty does so at a sharp logarithmic coupling. It selects connected square-lattice covers with a growing two-dimensional neighborhood on the exactly flat branch. The construction supplies one cyclic coordinate and a size-dependent coupling, so it leaves the physical origin of both inputs open.

## Gluing and its exact defect census

Use \(n\) labeled squares with two oriented neighbor permutations. After naming the vertices, fix the horizontal permutation \(a(i)=i+1\pmod n\), and sum over all vertical permutations \(b\). The horizontal cycle makes every sample connected. At a site a plaquette closes iff \(ab(i)=ba(i)\). The number \(k\) of failed plaquettes is the number of cyclic adjacencies in the word \(b(0),\ldots,b(n-1)\) that fail to advance by one. Assign weight \(e^{-\beta k}\). All statements concern this permutation gluing ensemble, which can have coincident or reverse links away from the generic flat branch.

For \(k=0\), there are exactly \(n\) slopes, \(b(i)=i+s\). For \(k>0\), mark the \(k\) broken successor edges of the natural cycle on the image values. Cutting those edges produces \(k\) runs. The image word is a cyclic ordering of the runs with every prescribed successor adjacency forbidden, followed by a choice of which of the \(n\) positions in that cyclic word is the first site. Thus the exact count is

\[
N_{n,k}=n\binom nk D_k,\qquad
D_k=\sum_{j=0}^{k-1}(-1)^j\binom kj(k-j-1)!+(-1)^k .
\]

Inclusion-exclusion gives \(D_k\): imposing any \(j<k\) successor edges contracts \(j\) links and leaves \((k-j-1)!\) cyclic orders, while imposing all of them gives one cycle. In particular there are no one- or two-defect configurations. Flat configurations are a special class of torus covers by commuting permutations. [Commuting permutations and torus covers](https://pmc.ncbi.nlm.nih.gov/articles/PMC11449981/)

## Critical window

Set \(\beta=\log n+c\), \(x=e^{-c}\). The inverse flat probability is

\[
1+\sum_{k=1}^n \frac{(n)_k}{n^k}\frac{D_k}{k!} x^k.
\]

For \(c>0\), dominated convergence applies since \(D_k\le(k-1)!\). Interchanging the nonconstant terms of the inclusion-exclusion generating series yields

\[
1+\sum_{k\ge1}D_k x^k/k!=e^{-x}[1-\log(1-x)].
\]

The limiting flat probability is \(e^x/[1-\log(1-x)]\). It is about 0.949 at \(c=0.5\). For \(c\le0\) the limit is zero: \(D_k/(k-1)!\to e^{-1}\) by the Bonferroni bounds for the forbidden successor edges, whose fixed-order inclusion-exclusion terms tend to \(1/j!\). At \(c=0\), the falling-factorial term cuts the harmonic sum off near \(\sqrt n\). Its difference from one below \(\sqrt n\) is at most \(k(k-1)/(2n)\), and above \(\sqrt n\) it is bounded by \(\exp[-k(k-1)/(2n)]\). The resulting flat probability is asymptotic to \(2e/\log n\), which approaches zero slowly. If \(\beta-\log n\to+\infty\), the flat probability tends to one. If \(\beta-\log n\to-\infty\), monotonicity and the result at \(c=0\) give zero.

## Defect density below the threshold

Just below the threshold, at fixed \(c<0\), the defects have a nonzero limiting density. For \(k/n\to y\in(0,1)\), Stirling's formula and \(D_k/k!\sim 1/(ek)\) give the log of its relative weight divided by \(n\) as \(f_c(y)=-y-(1-y)\log(1-y)-cy\). Its unique maximum is at \(y=1-e^c\), with value \(e^c-1-c>0\). The same Stirling bound is uniform up to the endpoints with \(0\log0=0\), since the \(D_k/k!\) factor is subexponential for \(k\ge3\). Summing at most \(n+1\) terms preserves the maximal exponential rate. Thus \(k/n\) concentrates at \(1-e^c\) and the flat probability decays as \(\exp[-n(e^c-1-c)+o(n)]\). For \(c>0\), the convergent count generating function makes the number of defects tight.

## Local geometry on the flat branch

A uniform flat slope \(s\) gives the graph on \(\mathbb Z_n\) with steps \(\pm1,\pm s\). It is the quotient of the square grid by the relation lattice \(u+sv=0\bmod n\). For a fixed \(0<|v|\le R\), put \(g=\gcd(v,n)\). Only \(u\) divisible by \(g\) can contribute, and each such \(u\) gives \(g\) slopes. Summing over \(|u|\le R\) gives at most \(2R+g\le3R\) slopes counted with multiplicity. Union over both signs of \(v\) bounds the fraction of slopes with a nonzero relation of length at most \(R<n\) by \(6R^2/n\). Hence with probability tending to one the flat quotient has exact square-grid balls up to radii \(r\) with \(2r+1\le n^{1/2-\delta}\) for any fixed \(0<\delta<1/2\). The extra one ensures that even edges within the induced ball agree. This demonstrates a growing two-dimensional metric neighborhood on the flat branch, without deriving a Lorentzian spacetime or claiming that the nonflat samples share that neighborhood.

The verifier counts all vertical permutations through \(n=8\), tests the critical formula and a separate direct partition calculation, and evaluates short relations and a representative graph Laplacian gap at three larger sizes. Run `python analysis/toe_20261127_square_gluing_flatness.py`.
