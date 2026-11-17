# The same R charge controls proton protection and the mixed flux anomaly

The [mixed anomaly calculation](2026-11-17_E6_fixed_point_R_anomaly.md) finds an obstruction to universal $E_6$ Green–Schwarz inflow in the [explicit two-frame vacuum](2026-11-17_E6_two_corner_vacuum.md). The obstruction extends to cyclic rephasings of any order with the same conjugate-pair frame and Yukawa couplings. An explicit pair of orthogonal $E_6$ coroot fluxes gives the necessary integer witness. There is also a spin-quantized local inflow option, whose axion has a definite selection rule for the proton-decay contact.

## The charge identity

Write $t$ for the charge of the superspace coordinate, so the superpotential has charge $2t$ in $\mathbb Z_N$. The brane norm terms force the charges of $A,\bar A$ and $B,\bar B$ to be opposite. The $K^c$ and $\bar K^c$ mass terms imply $r_K=r_A=a$ and $r_{\bar K}=-a$. The direct weak mass pairs and second triplet mass term imply $r_L=a$ and $2(r_B-a)=0$. The two localized singlets have charge zero. These equations use the fixed nonzero couplings as neutral constants.

The required $XXA$ cubic and $XX\,d^*(\bar K,\bar A)$ down coupling, for a common matter charge $x$, impose

$$
2x+a=2t,\qquad 2x-2a=2t .
$$

The explicit boundary contact is $X^4\bar A$ with the tensor contraction described in the [proton-decay calculation](2026-11-17_E6_orbifold_proton_boundary.md). Its excess charge above the superpotential charge is $4x-a-2t=2t$. The coefficient mismatch that forbids the contact is therefore exactly $2t$. For the standard $Z_4^R$ normalization $t=1$, the diagonal solutions have $a=0$, $r_B=0$ or $2$, and $x=1$ or $3$. A pure rephasing trivially preserving the nonzero $B$ VEV requires $r_B=0$. Allowing the other assignment for the purpose of the anomaly test gives the same mixed phase.

## A single flux pair tests all cyclic orders

The verifier constructs the coroots of $E_6$ by raising each of the 72 roots with the integral Cartan bilinear $J$. It finds two orthogonal coroots of squared length two. With one flux on each sphere of spin $S^2\times S^2$, their $E_6$ instanton number is zero and their *integer* mixed exponent for $t=1$ is $+2$. The fixed-point exponents in the displayed regulator are $(0,0,0,2)$ on this background. The two 27-component flux vectors are in the certificate.

For arbitrary cyclic diagonal rephasings the integrated phase on this background is $\exp(2\pi i\,2t/N)$. At a projected hypermultiplet zero mode, the fermion charges of the two conjugate reps add to $-2t$ for $H,\bar H$ or $+2t$ for $H^c,\bar H^c$. This follows from their opposite superfield charges and the bulk mass charge $2t$. The pair has identical real parities, so the quadratic gauge indices in the conjugate reps agree. The bulk gaugino and chiral adjoint contributions scale by $t$. A localized complete matter $27$ can change the anomaly only by a multiple of the universal Cartan trace, which vanishes on this flux. Localized gauge singlets carry no mixed gauge index. These integrated statements use actual zero modes and hold modulo $N$, independently of the placement of local counterterms.

Consequently inherited inflow depending only on the bulk $E_6$ instanton class and the tangent Pontryagin number requires $2t=0\bmod N$ on this background. That is precisely the condition under which the given contact is allowed by the rephasing. A larger cyclic R group or composition with diagonal field rephasings cannot evade this test within the stated matter and brane ansatz. Added nonuniversal inflow, a changed matter sector, and different couplings can change it.

## A geometric check on the torus

The holonomies $U_x,U_y,U_xU_y$ have fixed Lie-algebra dimensions $46,38,46$. A torus lattice automorphism must preserve the unique mod-two direction of dimension 38. In $\mathrm{GL}(2,\mathbb F_2)$ this leaves the identity and one transvection. For the charged hypers, the multiplicities of the intrinsic translation characters $(+,-)$ and $(-,+)$ are six and two. The transvection sends $(+,-)$ to $(-,-)$, which is absent. A compensating common $E_6$ bundle rotation cannot absorb a minus sign by an $E_6$ center element, since the center has order three and the holonomies are involutions. Thus only the identity action modulo two survives these tests. A crystallographic quarter turn has a nontrivial mod-two action in any integral lattice basis, and a hexagonal order-three rotation acts with a three-cycle. Also, every nontrivial half translation permutes the unique dimension-46 corner with a dimension-38 corner. The minimal flat data lack these geometric generators. Intrinsic R rotations and ultraviolet degrees of freedom remain possible. [Nilles et al. on geometric R symmetries with Wilson lines](https://arxiv.org/abs/1308.3435)

In particular, a quarter-turn matrix $M$ satisfies $M^2=-I$. If $M=I+2D$ for integral $D$, then $M^2=I\bmod 4$, a contradiction. For an order-three rotation the integral trace is $-1$, so its mod-two reduction differs from the identity, of trace zero.

## Quantized spin inflow and the first allowed axion harmonic

The three $SU(6)\times SU(2)$ corners have the class $C_f=4I_2$ of the adjoint $SO(3)$ factor. On a closed spin four-manifold its integral is even. Indeed the first Pontryagin class reduces modulo two to $w_2^2$, whose evaluation vanishes by the Wu formula. Thus $C_f/2$ is an integer on such backgrounds. At the Spin(10) corner the class $C_{01}=\tfrac12\int c_1(L_4)^2$ is already integral. Dividing the four mixed exponents by two gives the integer spin-background expressions

| Fixed point | Half the mixed gauge exponent |
| --- | --- |
| $00$ | $-C_{00}/2$ |
| $10$ | $J-3C_{10}/2$ |
| $01$ | $2J-5C_{01}$ |
| $11$ | $-C_{11}/2$ |

A $2\pi$-periodic axion with $Z_4^R$ shift $\pi$ and these couplings, with overall sign chosen to cancel the fermion phase, is sufficient on the tested spin gauge backgrounds. This verifies the coefficient arithmetic and quantization of the evaluated classes. It does not produce the axion from the 6D theory, extend the action to general R backgrounds, or cancel the full gravitational and global anomaly.

An axion shifting by $\pi$ gives its unit holomorphic harmonic R charge two. One harmonic can therefore dress the contact. If the axion shifts by $\pi/2$, with the undivided integral couplings, the first allowed positive harmonic is the second. These are selection rules. An actual instanton and its fermion zero modes are required to generate either term. [Lee et al. on nonperturbative dimension-five terms in $Z_4^R$](https://arxiv.org/abs/1009.0905)

Reproduce with `python analysis/toe_20261117_E6_cyclic_R_robustness.py`. The output is `data/toe_20261117_E6_cyclic_R_robustness.json`.
