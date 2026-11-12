# Independent matter and the radial family connection of the W33 monopole

The radial solution improves when the sourced family connection and the previously paired matter amplitude both vary. At unit couplings the converged energy is 574.21984905. The paired calculation with the family connection frozen gave 574.24156726. The enlarged ansatz still has a transverse matter equation with nonzero residual. [Previous radial solution](2026-11-11_monopole_radial_solution.md)

## Eliminate the radial gauge connection

Write the e0 tensor f2 entries of X[0] and Z[0] as u−v/sqrt(2) and u+v/sqrt(2). Use U = sqrt(2)u so U and v both have unit kinetic coefficient before gauge elimination. The other matter entries and four diagonal adjoint singlets are defined as in the previous solve.

On this real ansatz the only sourced family generator is the real rotation T from f0 toward f2, normalized by T f0 = f2 and T f2 = −f0. Both the fundamental and its dual transform by the same real rotation. The scalar current for T is 2u' and the quadratic norm of its action is M = 6+U²+v². The family radial connection a T has zero field strength. Its equation is algebraic and gives a = −sqrt(2)U'/M. Substitution changes the radial kinetic term U'^2+v'^2 to G U'^2+v'^2 with G = 1−2/M. A radial gauge transformation can remove the connection while rotating the matter profiles. Freezing it in the original matter chart changes the variational equations.

## D energy and the enlarged radial solution

With the gauge kinetic convention Tr(F²)/(2g²), elimination of the auxiliary D field gives g²/4 times the squared trace norm of the projected moment. The internal trace uses the 27 and the family trace uses the 3. The diagonal projector entry on e0 is exactly 2/9. The internal moment is proportional to −2sqrt(2)uv times the e0 projector. The family moment has an off-diagonal 02 entry −sqrt(2)v and a traceless diagonal term proportional to −2sqrt(2)uv. At unit internal and family couplings this gives

    V_D = v² (1 + 16u²/9).

The adjoint stays Hermitian, so it adds no D moment. The replay reconstructs the mixed and centered-meson F derivatives before restricting the fields. At v = 0 the F potential and its retained derivatives agree with the previous implementation. Its derivative along v agrees with the previously measured transverse force. The calculation uses the canonical charged Yukawa action and omits the optional independent neutrino deformation. [Supersymmetric auxiliary-field conventions](https://arxiv.org/abs/hep-ph/9709356)

| Radial problem | Energy |
| --- | ---: |
| Paired matter with family connection frozen | 574.24156726 |
| Paired matter with family connection eliminated | 574.21992270 |
| Independent matter with family connection eliminated | 574.21984905 |

The final three meshes use outer radii 3, 4 and 5. Their energies agree within 2.2e−7. The finest collocation residual is below 1e−7, and the Derrick energy residual is about −2.6e−9. The integrated D energy is about 3.56e−7. The classical electric phase inertia of this profile is 9.23335466 at unit internal coupling.

## Another matter equation remains sourced

Vary the e1 tensor f2 entries of X[2] and Z[1] together. This preserves their cancellation in the D moment. The F contribution is the derivative of the original invariants along this variation. The radial kinetic contribution, after solving the family gauge equation, is 4a² in the equation residual for a unit increment of both entries. The replay evaluates their sum and finds a nonzero residual. The remaining neutral fields must vary to obtain a stationary core of the full action.

Run python analysis/toe_20261111_monopole_independent_matter.py from the repository root. [Frozen profiles and residuals](../data/toe_20261111_monopole_independent_matter.json)
