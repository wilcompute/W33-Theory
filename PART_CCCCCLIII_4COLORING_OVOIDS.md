# PART_CCCCCLIII — Every Proper 4-Coloring Is a Partition into Ovoids

## Theorem

The chromatic number of W(3,3) is \(\chi = q+1 = 4\), and every proper 4-coloring partitions the vertex set into 4 ovoids.

## Proof

**Lower bound:** By the Hoffman bound:
\[
\chi(G) \geq 1 - \frac{k}{s} = 1 - \frac{12}{-4} = 4.
\]

**Upper bound:** The ovoids of GQ(3,3) partition the point set. Since the GQ(q,q) is self-dual and has a partition into \(q+1 = 4\) ovoids (this follows from the existence of a spread of the dual GQ), we have \(\chi \leq 4\). Combined: \(\chi = 4\).

**Structure:** Each color class is an independent set of size \(v/4 = 10 = \alpha\). Since \(\alpha = 10\) is the Hoffman bound, the bound is **tight**, meaning every maximum independent set is an ovoid. The 4 color classes must each achieve the Hoffman bound, hence each is an ovoid.

## Ovoid Properties

- An ovoid \(O\) has \(|O| = q^2 + 1 = 10\) points.
- Every **line** of GQ(3,3) meets \(O\) in exactly 1 point.
- In W(3,3): every vertex not in \(O\) is adjacent to **exactly 1** vertex of \(O\).
- Verification: \(|O| \times (\text{lines per point}) = 10 \times 4 = 40 = b = |\text{lines}|\). Each line hit exactly once. \(\checkmark\)

## Number of Ovoids

In GQ(3,3), the number of ovoids is known to be **\(|\mathrm{PSp}(4,3)| / |\mathrm{Stab}(\text{ovoid})|\)**. The stabiliser of an ovoid in \(\mathrm{PSp}(4,3)\) is \(\mathrm{PSp}(2,9) \cong A_6\) of order 360. Hence:
\[
|\text{ovoids}| = \frac{25920}{360} = 72.
\]
