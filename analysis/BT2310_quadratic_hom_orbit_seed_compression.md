# Pass 2310 — twenty-four orbit seeds generate all fifty quadratic maps

The complete Pass-2301 basis contains 50 surjective equivariant quadratic maps,
but only 24 distinct signed-orbit tensors. Five seeds survive projection to all
four rational targets \(15,24,30,81\).

Caching each orbit tensor once changes the literal stored orbit-entry count from

\[
1,213,920\quad\text{to}\quad583,200,
\]

an exact compression factor

\[
\boxed{281/135\approx2.08148}.
\]

Only two seeds have nontrivial stabilizer: the symmetric seed
`(0,56,155)` has stabilizer order 6 and the symmetric seed `(0,57,191)`
has stabilizer order 3. The other 22 are regular PSp orbits.

The full per-map orbit tensors occupy about \(2248/19309\approx11.64\%\) of
the corresponding dense target-coordinate array. This is a useful compiler and
memory result, but it is **not** a proof of physical locality or low CP tensor
rank. It says that the exact representation-theoretic maps admit a compact
orbit-program description.
