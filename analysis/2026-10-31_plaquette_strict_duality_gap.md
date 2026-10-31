# Exact W33 plaquette duality gap and finite-temperature ordering (2026-10-31)

**Status: exact finite calculation. No continuum or physical critical-point claim.**

## Origin and prior-work boundary

This is an independent cross-check prompted by *Forty Points*, §11.2 (the
dynamical-principle problem), and the October 31 Pass 12500 correction of the
website's unsupported self-dual Potts critical-temperature assertion.

The underlying codes are **not newly discovered here**: Pass 159/167 already
established the *address* code \([40,15,8]\) and Pass 173 the *route*
code \([40,15,10]\). Pass 12500 already proved the corresponding plaquette
models are not self-dual. This work adds the **exact factored difference,
its strict sign, and the eighth-order contact invariant**.

## The models and the algebraic statement

Let \(N\) be the 40-point by 40-line incidence matrix of \(W(3,3)\).
For an Ising spin on each point, with one 4-spin plaquette per line,

\[
H_{\mathrm{route}}(s)=-J\sum_{\ell}\prod_{p\in\ell}s_p.
\]

The high-temperature expansion of its partition function is

\[
Z_{\mathrm{route}}(K)
=2^{40}\cosh^{40}K\;W_{\mathrm{route}}(\tanh K),
\quad C_{\mathrm{route}}=\ker_{\mathbf F_2}N.
\]

Interchanging points and lines gives the dual model with
\(C_{\mathrm{address}}=\ker_{\mathbf F_2}N^\top\).
For \(t=\tanh K\), **both** have the same positive prefactor
\(2^{40}\cosh^{40}K\).

Directly enumerate all \(2^{15}\) codewords of each kernel, with independent
construction from projective \(\mathbf F_3^4\). The result is the
identity

\[
\boxed{
W_{\mathrm{address}}(t)-W_{\mathrm{route}}(t)
=9t^8(1-t^2)^8(5t^8+16t^6+38t^4+16t^2+5).
}
\]

All coefficients in the final factor are positive, so for every finite,
positive ferromagnetic coupling \(K>0\),

\[
Z_{\mathrm{address}}(K)>Z_{\mathrm{route}}(K).
\]

Thus the dual has strictly lower finite-volume free energy at fixed \(K\)
under this comparison, notwithstanding equal spin counts and coupling
counts. The partition functions are equal at \(K=0\), and their
**normalized code polynomials** agree at \(t=1\); the latter does **not**
mean the unnormalized partition functions converge to a finite common
number at \(K\to\infty\).

The gap starts at \(9\cdot5t^8=45t^8\) near \(t=0\). At \(t=1\) it vanishes
to **exact order eight**:
\[
\frac{d^j}{dt^j}(W_{\mathrm{address}}-W_{\mathrm{route}})(1)=0
\ (0\le j<8),\quad
\frac{d^8}{dt^8}(W_{\mathrm{address}}-W_{\mathrm{route}})(1)
=9\cdot 8!\cdot2^8\cdot80=7{,}431{,}782{,}400.
\]

This is stronger than the previous fact that the two binary weight
enumerators differ: their difference has a globally definite sign on the
ferromagnetic interval and an unexpectedly high order of endpoint
contact. It is useful as a finite-geometry duality diagnostic and as a
regression against future unsupported exact-self-duality claims.

## Independently checkable data

- \(40\) points, \(40\) maximal isotropic lines, four incidences each.
- Binary ranks of \(N,N^\top\): \(25\); kernel dimensions: \(15\).
- Minimum weights: route \(10\), 216 words; address \(8\), 45 words.
- Exact total words in each enumerator: \(32768\).
- The polynomial factorization is verified by integer coefficient
  multiplication rather than symbolic/numerical root fitting.
- Both enumerators are complement-symmetric.

## Boundary and falsifiers

The object is finite (40 Ising spins); **no singular critical point at
finite temperature** is implied. The inequality compares two different
finite plaquette Hamiltonians with identical coupling \(K\), not two
physically proven realizations of a proposed W33 substrate. It does not
derive Einstein dynamics, a continuum limit, particle masses or a
quantum-computational threshold. A claim of exact self-duality would
contradict the exhibited polynomial unless the model itself is changed.

Witness: \`analysis/w33_20261031_plaquette_strict_duality_gap.py\`.
Certificate: \`data/w33_20261031_plaquette_strict_duality_gap.json\`.

Background: Kim–Mellinger–Storme, *Small weight codewords in LDPC codes
defined by (dual) classical generalized quadrangles*, Designs,
Codes and Cryptography 42 (2007);
Pass 173 and Passes 12498–12500 within this repository.
