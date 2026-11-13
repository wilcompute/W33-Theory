# Exact and approximate postselection for a split E6 Pauli boost

The native split-torus example doubles the IZI charge. Restrict the input to the commuting line ρ(x) = (I+xP)/8, with P = IZI and −1≤x≤1. Its target on this line has expectation 2x. It is full rank for |x|<1/2. An exact implementation on the full charge body near the maximally mixed state would in particular work on a nonempty interval of this line. [Native boost](2026-11-13_pauli_e6_positivity.md)

## Exact implementation with a fixed finite copy budget

For any trace-nonincreasing completely positive operation on n independent copies, both its success probability S(x) and its unnormalized output expectation M(x) are polynomials of degree at most n. Any quantum ancilla, joint measurement, and feed-forward with the same finite copy cap is covered by this linear map on n copies. Conditional exactness on an interval implies the polynomial identity M(x)=2xS(x). For every full-rank input, a nonzero positive success effect has strictly positive probability. At x=3/4 the identity therefore forces expectation 3/2 for a Pauli observable, an impossibility. This rules out exact bounded-copy implementation even if correctness is required only where the boosted target is strictly physical. The argument leaves variable, unbounded copy budgets open. [Watrous, The Theory of Quantum Information](https://johnwatrous.com/wp-content/uploads/TQI.pdf)

## Sharp one- and two-copy approximation on the commuting line

For the input pair x=±r, all n-copy inputs are mixtures over strings of n Pauli eigenvalue signs. The normalized states within each string sector are independent of x. Any quantum instrument followed by an output Pauli measurement therefore gives a classical conditional response to each string. The likelihood ratio of any string for +r versus −r lies between 1/A and A, where A=((1+r)/(1−r))^n. The same bounds hold for the ratio of the unnormalized probabilities of either output sign. Hence the ratio of the conditional output odds at the two endpoints is at most A², with the deterministic cases following by continuity. If the uniform absolute expectation error is ε, the conditional means at +r and −r must be at least 2r−ε and at most −(2r−ε), respectively. The odds bound yields

    ε ≥ max(0, 2r − tanh(n atanh(r))).

For one copy, measuring and repreparing the observed sign attains the bound ε=r at unit success. For two copies, accept only matching signs and prepare the normalized Pauli eigenspace with that sign. The success is (1+x²)/2 and the conditional mean is 2x/(1+x²). Its error grows with |x|, so the lower bound is attained for every radius 0<r≤1/2:

    ε₂(r) = 2r³/(1+r²).

At r=1/4 this gives exact worst-case expectation error 1/34 with success at least 1/2. Since both states are in the same Pauli line, the worst-case trace distance is 1/68 for this explicit procedure. The optimum concerns the commuting line. The full 27-coordinate boost has additional noncommuting directions. The method is related to simulating transformed coin biases in Bernoulli factories. [Huber, Nearly optimal Bernoulli factories for linear functions](https://arxiv.org/abs/1308.1562)

## Deterministic approximation for all 27 charges

Whenever the boosted target is physical, there is also a uniform deterministic approximation for the full charge map. Measure each of the 27 Paulis on its own block of m independent copies. Multiply the sample means by their native boost gains and project the resulting vector onto the convex charge-state body in Euclidean norm. Prepare the density represented by this projected vector. Projection cannot increase distance to the physical target, and the sum of the amplified variances is at most (81/2)/m. The Pauli matrices are trace orthogonal, so trace distance between encoded states is bounded by half the Euclidean charge distance. Convexity of trace distance then bounds the error of the unconditional output by 9/(2 sqrt(2m)). This bound uses 27m copies and success probability one. It gives an achievable error for the full 27-dimensional problem. Its optimal copy cost remains open.

Replay with `py -3 analysis/toe_20261113_e6_postselection.py`.
