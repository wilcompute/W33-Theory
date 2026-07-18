# Pass 456 — exact anatomy of the four q=5 spectral collisions

The exact Pass 447 sample was reproduced: seed 447, 400 inverse-closed sections, 396 spectra, with 392 singleton spectra and four doubletons.

The full 12,000-element affine automorphism action \(GL(2,5)\ltimes\mathbb F_5^2\) was tested on every collision pair.

- Samples \(20,159\), \(29,118\), and \(51,296\) are ordinary orbit repeats.
- Samples \(105,161\) are affine-inequivalent.

NetworkX certifies that the two 125-vertex Cayley graphs from samples 105 and 161 are nonisomorphic. Their common characteristic polynomial is

\[
(x-24)(x+1)^{24}
\bigl(x^{10}-120x^8-15x^7+4220x^6+792x^5-37925x^4
+4955x^3+96910x^2-39730x-209\bigr)^{10}.
\]

They also have exactly the same critical group:

\[
\boxed{
(\mathbb Z/5)^{16}\oplus
(\mathbb Z/25)^5\oplus
(\mathbb Z/125)^{13}\oplus
(\mathbb Z/2037033916375)^{10}.}
\]

The graphs are separated by the distribution of common-neighbor counts among nonneighbors of a vertex, so nonisomorphism has an explicit local witness in addition to the graph-isomorphism search.

**Breakthrough.** This is the first q=5 pair in the programme that is simultaneously nonisomorphic, cospectral, and Smith-identical. The critical group is therefore not a complete refinement of the section spectrum.
