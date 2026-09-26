# Pass 10976 — The native clock cubic makes the minimal transition first order

Producer: `analysis/w33_pass10976_first_order_clock_selection.py`
Certificate: `data/w33_pass10976_first_order_clock_selection.json`
Regression: `tests/test_w33_pass10976_first_order_clock_selection.py`

## Result

Pass 10972 found the four tetrahedral extrema of the unique cubic invariant
on the three-dimensional clock augmentation module. Pass 10975 then showed
that the actual signed (E_6) cubic has a nonzero Reynolds component on that
module:
[
mathcal R(D)|_A=-rac23 p_3.
]

This immediately changes the minimal Landau dynamics.
Take
[
F(x)=alpha p_2(x)+eta p_2(x)^2-gamma p_3(x),
qquad eta>0, gamma>0.
]
At fixed radius (p_2=r^2), Pass 10972 gives
[
max p_3=rac{r^3}{sqrt3},
]
attained on exactly four (S_4/S_3) tetrahedral clock rays. The full
three-dimensional minimization therefore reduces exactly to
[
f(r)=alpha r^2-rac{gamma}{sqrt3}r^3+eta r^4,
qquad rge0.
]

Put (kappa=gamma/sqrt3).
The nonzero stationary radii solve
[
4eta r^2-3kappa r+2alpha=0.
]
They first appear when the discriminant vanishes:
[
oxed{alpha_{
m sp}^{
m ord}=rac{3gamma^2}{32eta}}.
]

The ordered and symmetric vacua coexist when
[
f(r_*)=f'(r_*)=0.
]
The exact solution is
[
oxed{
r_*=rac{gamma}{2sqrt3,eta},
qquad
alpha_*=rac{gamma^2}{12eta}.
}
]
Because (alpha_*>0), the ordered vacuum becomes globally competitive
**before** the quadratic coefficient changes sign. The order parameter jumps
from (0) to (r_*): this is a first-order transition in the minimal
homogeneous mean-field model.

The disordered extremum remains locally stable down to
[
alpha_{
m sp}^{
m dis}=0.
]
Hence the metastability interval is
[
0<alpha<rac{3gamma^2}{32eta},
]
with coexistence strictly inside it:
[
alpha_{
m sp}^{
m ord}-alpha_*
=rac{gamma^2}{96eta}.
]
## Exact barrier

At coexistence the unstable radial stationary point sits at
[
r_b=rac{gamma}{4sqrt3,eta}.
]
Its free-energy height above either degenerate minimum is
[
oxed{
Delta F_b=rac{gamma^4}{2304,eta^3}.
}
]

The ordered radial curvature at coexistence is
[
f''(r_*)=rac{gamma^2}{6eta}>0.
]

The four ordered vacua form one (S_4/S_3) orbit. Since the broken symmetry is
finite, there are no Goldstone modes in this minimal order-parameter theory.
Changing the sign of (gamma) selects the opposite tetrahedron.
## Inherit the native E6 normalization

If an effective coefficient (g_{E6}>0) multiplies the Reynolds-projected
native cubic from Pass 10975, then
[
g_{E6}mathcal R(D)|_A=-rac{2g_{E6}}3 p_3,
]
so
[
gamma_{
m eff}=rac{2g_{E6}}3.
]

The phase scales become
[
oxed{
r_*=rac{g_{E6}}{3sqrt3,eta},
qquad
alpha_*=rac{g_{E6}^2}{27eta},
}
]
[
oxed{
alpha_{
m sp}^{
m ord}=rac{g_{E6}^2}{24eta},
qquad
Delta F_b=rac{g_{E6}^4}{11664,eta^3}.
}
]
These are relative normalization statements only. The repository still does
not derive (g_{E6}), (eta), or an energy scale.

## If alpha is temperature-like

If one later has
[
alpha=a(T-T_0),qquad a>0,
]
then the same mean-field algebra gives
[
T_*-T_0=rac{gamma^2}{12aeta},
]
and the latent heat is
[
L=T_*,a,r_*^2
=rac{T_*agamma^2}{12eta^2}.
]

This line is conditional: no identification of (alpha) with physical
temperature has been derived from (W(3,3)).
## Literature boundary

The mean-field conclusion is standard Landau theory: an allowed cubic invariant
generically produces a discontinuous transition because it creates a competing
minimum while the quadratic coefficient is still positive. Classical examples
include the Landau treatment of structural transitions with cubic invariants.

The repository increment is not that general fact. It is the chain that makes
the cubic unavoidable in this particular finite construction:

[
	ext{clock }S_4
longrightarrow
V_3
longrightarrow
p_3
longleftarrow
mathcal R(D_{E6}),
]
followed by the exact phase diagram above.

## Boundary

This is an exact **homogeneous mean-field** statement for the minimal analytic
Landau polynomial. It is not a microscopic Hamiltonian, fluctuation theorem,
finite-temperature universe, cosmological phase transition, nucleation-rate
calculation, domain-wall prediction, or continuum dynamics derivation.

Extra fields, nonlocal terms, higher invariants, fluctuations, or a different
dynamical realization can change the transition. The result says what the
minimal model forced by the already-certified cubic does—not that nature must
realize that minimal model.
