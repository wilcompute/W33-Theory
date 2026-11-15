# A mass-weighted KK sum-rule obstruction for positive graph Laplacians

The recent D9 Einstein-Maxwell calculation gives the linear spin-two tower on the smooth product of two spheres. A separate test asks whether a finite graph with positive edge couplings and pointwise multiplication can reproduce the mass-weighted overlap identity used in continuum KK graviton scattering. The obstruction below applies even with a complete graph eigenbasis. [Continuum sum rule, Eq. 29](https://arxiv.org/abs/1910.06159)

Let the inner product use positive vertex measures and let the graph Laplacian be self-adjoint with nonnegative conductances w on undirected edges. Take a real eigenmode f with eigenvalue lambda>0. Expand its pointwise square in the complete orthonormal eigenbasis. The cubic overlaps are its expansion coefficients, so their unweighted sum of squares is the quartic overlap by Parseval. The mass-weighted sum E is the graph Dirichlet energy of f squared.

The continuum requirement is 4 lambda times the quartic overlap minus 3 E equal to zero. On the graph the tested difference is instead exactly

    4 lambda <f^2,f^2> - 3 <f^2,L(f^2)> = sum_edges w (f_i-f_j)^4.

The eigen-equation replaces the first term by 4<f^3,Lf>. The identity then follows on each edge by expanding the two differences. A positive eigenvalue forces a nonzero difference on an edge of positive weight. The defect is therefore strictly positive. The ordinary overlap identity and the presence of a massless constant mode are compatible with this failure. It is an interaction constraint on this regulator ansatz. A full amplitude claim would require a specified nonlinear graph action and its own vertices.

## Controls and scaling

The verifier independently constructs the 4x4 toroidal knight graph and the W(3,3) point graph. The knight parity character alternates sign on every edge, so its square is constant. It gives zero mass-weighted exchange and a defect equal to the entire continuum contact contribution in this test. For the smooth sphere the normalized mode sqrt(3) cos(theta) gives quartic overlap 9/5. Its square contains only degree zero and degree two, and the weighted exchange is 24/5 in inverse sphere-radius-squared units. The continuum difference is zero.

For the N-cycle with N>=5, uniform vertex measure and jump rate k per neighbor, the first normalized real Fourier mode has quartic moment 3/2 and eigenvalue lambda=4k sin(pi/N)^2. Its forward differences form another sinusoid of amplitude sqrt(lambda/k) times the original amplitude. Summing the fourth powers gives defect (3/2) lambda^2/k. Relative to the contact contribution 4 lambda times the quartic moment, the defect is sin(pi/N)^2. A refinement can therefore converge to the smooth sum rule while every finite positive graph still fails it.

Replay with py -3 analysis/toe_20261114_kk_graph_sum_rule.py.

The native W(3,3) control has eigenvalue 16 and a normalized defect of 4/7. The knight graph and its hypercube identification are documented in [the earlier toroidal-knight construction](BT738_toroidal_knight_quotient_cube.md).
