# Ramified Hesse compiler to Cartan-cubic holonomy

The exact full-Clifford Hesse compiler has a second arithmetic life at the
prime above three.  Over `Q(omega)` it is an invertible `36 x 36` matrix made
from twelve three-point Fourier transforms and satisfies `T* T = 3 I`.  Under

```text
Z[omega] -> Z[omega]/(1-omega) = F3,   omega -> 1,
```

each Fourier block becomes the all-ones `3 x 3` matrix.  The reduced compiler
therefore has rank 12, right and left nullity 24, and zero Gram matrix.  Its
twelve distinct column supports partition the ordinary 36 Hesse tritangents
into triples, with three triples in each of the four noncentral Hesse
directions.

That 24-dimensional compiler nullity is **not** the 24-dimensional
Cartan-cubic line kernel.  The former uses safe-plane compiler coordinates;
the latter uses 45 tritangent coordinates.  The executable bridge only uses
the reduced rank-12 image.  In the fixed Clifford gauge this image lies in the
ordinary-36 projection of the cubic line kernel.  The incidence map on the
nine distinguished center-coset tritangents has full column rank nine, so
each Fourier support has a unique fiber correction.

The corrected vectors have weight six: three ordinary and three distinguished
tritangents.  They are independent and generate an explicit ternary code

```text
R12 <= ker_F3(Cartan point-tritangent incidence),
R12 is [45,12,6]_3.
```

Exhaustion of all `3^12 = 531441` codewords proves that the 24 minimum words
are exactly the two nonzero scalar multiples of the twelve generator hexads.
Across the basis, every ordinary coordinate occurs once and every
distinguished coordinate occurs four times.  The generator Gram matrix has
rank three.  Grouping generators by the four Hesse directions gives

```text
Gram = (J4-I4) tensor J3,
```

so the modular residue retains the affine Hesse parallel-class organization
even though the three complex characters in each Fourier fiber have merged.

There is a complete structural form behind these counts.  The nine
distinguished center cosets are the quotient points
`H27/Z(H27) = AG(2,3)`, and the twelve fiber-correction supports are exactly
all twelve affine lines.  Every correction coefficient is 2.  The ordinary
parts are twelve disjoint private triples.  After a coordinate permutation the
generator matrix is therefore

```text
G = [2 A_AG(2,3) | I12 tensor (1,1,1)],
wt(cG) = 3 wt(c) + wt(c A_AG(2,3)).
```

The second formula independently reproduces the complete weight enumerator.
It also explains the Gram law: parallel affine lines have intersection zero
modulo three, while lines in different directions meet once.

An external result check found that Saif and Alhomaidhi published a different
ternary `[45,12,6]` Gray-image construction in June 2026
(`doi:10.3390/math14112019`).  The parameters are therefore prior art.  No code
equivalence has been checked.  The increment here is the Cartan-kernel
embedding, ramified Clifford origin, exact minimum shell and enumerator, and
the affine-plane systematic form.

This is an arithmetic compiler/incidence theorem in the repository's fixed
gauge.  It does not identify the two dimension-24 kernels, claim that the
subcode is `W(E6)` invariant, interpret modular reduction as physical noise,
or assign particle data to the hexads.

Executable evidence:

- `analysis/w33_ramified_hesse_cubic_holonomy_bridge.py`
- `data/w33_ramified_hesse_cubic_holonomy_bridge.json`
- `tests/test_w33_ramified_hesse_cubic_holonomy_bridge.py`
