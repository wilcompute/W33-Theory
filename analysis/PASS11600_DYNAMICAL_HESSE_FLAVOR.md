# Pass11600: an exact dynamical Hesse flavor order parameter

Reservation: `3db837b54` (Codex track). This packet builds an explicit CP-breaking
flavor-sector EFT and proves a dimension16 lower bound in its stated inventory.
It does not derive the EFT coefficients or a physical vacuum from W33.

## What changed, and prior ownership

Since publication receipt `f914b3dee`, the reviewed remote window contains61
commits and151 changed paths through `a2f4475a8`. The intake inventory parsed all
changed Python sources and JSON certificates; its85,774,463 bytes include large
generated formula catalogues. Static parsing is not a replay of every producer.
The frozen inventory is `data/w33_pass11600_remote_intake_inventory.json`.
The scientific reports11531–11537 and11556–11599 were read against their sources
and certificates, along with the updated144-page paper's changed sections.
The expanded1588-line `Chat.txt` handoff was read as evidence, not instructions.
Its family/chirality frontier predates11590–11599. The original parallel checkout,
including local11342–11349 winding probes and dirty10956/11311/11312 work, is
preserved. The current paper still leaves measured flavor, couplings, gravity,
dynamical spacetime and the cosmological constant open.

Owners to consult before interpreting this as new geometry:

-11591: `analysis/w33_pass11591_spin10_delta54_hesse_yukawa.py` supplies the
  two-dimensional Delta54-invariant family tensor pencil.
-11597: `analysis/w33_pass11597_family_clifford_breaking.py` supplies its Clifford
  action and obstruction to keeping a cubic invariant under the whole parent.
-10972: `analysis/w33_pass10972_tetrahedral_cubic_clock_selector.py` already uses
  a cubic Landau selector on a different S4 clock carrier.10976 studies that
  clock model's first-order transition. General Landau selection is not new here.
-11550 already owns the repo's tetrahedral/Veronese/Hesse connection.
-`analysis/2026-09-23_execute_all5_plus3_physics_frontier.md` already owns an
  anti-linear hybrid E8 charge-conjugation scaffold and an H27 cubic permission
  theorem. It explicitly leaves spontaneous CP and measured mixing open. This
  packet supplies a separate dynamical tensor-field example, not spatial parity
  or a coherent nonlinear compiler. This prior report was read in full after the
  intake guard flagged the shared `hesse+pmns` wording.
-The classical Hesse group acts on its pencil through A4 with kernel of order18:
  [Artebani and Dolgachev, section4](https://arxiv.org/abs/math/0611590).

The new object is a specified field, invariant interaction, global potential,
complete vacuum-ray orbit, and exact low-degree obstruction on this carrier.
Spontaneous CP violation with Delta27/Delta54 triplet Higgs fields and its
extension to higher-order operators are established literature:
[Varzielas et al. (2012)](https://arxiv.org/abs/1204.3633) and
[Varzielas et al. (2017)](https://arxiv.org/abs/1706.07606). Those are different
field inventories; no general discovery of discrete-group CP breaking is claimed.
Our selected ray ratios are coefficient data, so they are not a claim of
parameter-independent geometrical CP violation. The bound concerns a complex
two-component tensor-pencil field, not a triplet Higgs model.

## Field and actual maps

Let B have orthonormal columns in Sym³(C³): the diagonal tensor has norm²3;
the tensor with all three indices distinct has norm²6. Introduce a canonical
complex doublet u and the tensor field Phi=B u. Under the family action Phi
transforms in Sym³(V). Contracting Phi-dagger with the symmetric matter/matter/
Higgs tensor gives an invariant interaction. With a supplied cutoff M,

    a=conjugate(u0)/(sqrt3 M), b=conjugate(u1)/(sqrt6 M),
    Y(h)=[[a h0,b h2,b h1],[b h2,a h1,b h0],[b h1,b h0,a h2]].

The normalized Fourier action is [[1,sqrt2],[sqrt2,-1]]/sqrt3; the phase action is
diag(1,omega).11597's [[1,1],[2,-1]]/sqrt3 is a different coordinate normalization:
C=diag(1,1/sqrt2) conjugates the old matrix to this one. The producer checks the
actual27-dimensional tensor action and this conversion. No old result is retracted.

Declare an exact common-phase U1 and coefficient CP (complex conjugation), plus
a polynomial scalar potential and no additional order parameters. This U1 must
extend consistently to the interaction/Higgs sector; scalar-sector invariance
alone does not establish a full quantum symmetry.

Set rho=u-dagger u and r=(2 Re(u0* u1),2 Im(u0* u1),|u0|²-|u1|²). Then r²=rho².
In tetrahedral axes (stored explicitly in the certificate), write n=(x,y,z).
Fourier acts by diag(1,-1,-1), phase cycles x,y,z, and CP swaps y,z. The projective
G216 action thus factors through A4. Adding CP gives W(D3)=S4: permutations with
an even number of sign changes. Its invariant ring is R[p2,p3,p4], where

    p2=x²+y²+z²=rho², p3=xyz, p4=x⁴+y⁴+z⁴.

The A4-invariant, CP-odd discriminant is

    W=(x²-y²)(y²-z²)(z²-x²), det d(p2,p3,p4)/d(x,y,z)=-8W.

## Why dimension16 is the minimum in this inventory

Each Bloch coordinate has canonical field degree2. On a fixed-radius sphere,
every CP-even U1-invariant potential through field degree14 has angular form

    constant + A p3+B p4+C p3²+D p3 p4.

Powers of rho only change the coefficients on that sphere. At a generic point
W!=0, (p3,p4) are local angular coordinates. The Hessian determinant is -D².
If D!=0, any stationary point is a saddle; if D=0, stationarity requires B=0
and leaves an exactly flat p4 direction. A strict isolated generic ray minimum
therefore requires at least field degree16. The potential below attains it.
This excludes neither CP-preserving W=0 extrema nor U1-breaking holomorphic
potentials, extra fields or nonpolynomial actions.

## Positive potential and its complete minima

For positive kappa, lambda3, lambda4, v and M, take

    V=kappa(rho-v²)²
      +lambda3/M⁸ [xyz-3rho³/(7sqrt14)]²
      +lambda4/M¹² [x⁴+y⁴+z⁴-rho⁴/2]².

All three terms are nonnegative. Simultaneous zeros give global energy zero and
rho=v². Their squared-coordinate ratios are exactly (1,4,9)/14, in any order,
with positive coordinate product. Indeed the elementary symmetric data of the
rescaled squares are14,49,36, so their polynomial is

    t³-14t²+49t-36=(t-1)(t-4)(t-9).

There are24 rays: six permutations times four signs. A4 splits them into two
orbits of12, exchanged by CP. At every ray W=±15rho⁶/343, so no parent generalized
CP fixes the ray. The projective stabilizer is the order18 kernel
(C3×C3):C2, the projective image of Delta54. Vector stabilizers depend on the
scalar lift and separate common phase; this is not an unqualified order54 claim.
The independent regression enumerates all216 projective qutrit Clifford elements:
18 fix a selected ray and zero composed antiunitaries fix it.

At the unscaled representative (1,2,3), the tangent Hessian of
(p3-6)²+(p4-98)² in tangent columns (2,-1,0),(3,0,-1) is
[[1314,4896],[4896,18944]], with determinant921600. The full scalar model has
positive radial and two angular directions. Each ray lifts to a U1 circle:
one phase Goldstone if global, a redundancy only if separately gauged.

## Exact angular masses, and the missing protection

For canonical Lkin=partial u-dagger partial u, the fixed-rho phase quotient has
kinetic metric v²/4 times the unit Bloch sphere metric. At m=(1,2,3)/sqrt14,
the projected gradients g3,g4 of p3(m),p4(m) have Gram matrix

    G=[[181/1372,-3sqrt14/49],[-3sqrt14/49,216/343]], detG=3600/117649.

Writing A=lambda3 v¹²/M⁸ and B=lambda4 v¹⁶/M¹² gives

    m±²=2/v² [A|g3|²+B|g4|²
          ±sqrt((A|g3|²+B|g4|²)²-4AB detG)].

For fixed positive lambdas and v/M small:

    m_heavy² ~ (181/343) lambda3 v²(v/M)⁸,
    m_light² ~ (57600/62083) lambda4 v²(v/M)¹².

These are extra tensor-field angular masses, not fermion masses. Lower-degree
p3 and p4 operators are allowed by the declared symmetries. Their absence and
the squared-potential coefficient correlations are not radiatively protected
here: quantum corrections can move the vacuum and destroy this hierarchy.
The next physical problem is a protecting mechanism or a UV completion, not
identifying these two eigenvalues with observed particles.

## An exact CP transfer witness, without a flavor fit

At one vacuum ray, remove an overall scale and take
a=1, b=-(sqrt3+i)/[2(sqrt14+2sqrt3)]. Supply two real Higgs directions
h_up=(1,2,4), h_down=(3,1,2). For H=Y Y-dagger, the exact certificate gives

    Im Tr([H_up,H_down]³)
      =1125(-40759807sqrt42-264153529)
        /[4(24532198sqrt3+11356201sqrt14)] !=0,
      approximately -1748.44523217580.

Conjugating the vacuum reverses its sign. Thus coefficient CP breaking can
transfer to a nonzero weak-basis matrix invariant with real supplied alignments.
This does not select those alignments, predict CKM/PMNS, fix measured masses,
establish a natural hierarchy, or complete chiral gauge/gravity dynamics.
The rational target ratios and the new tensor field are chosen model data.

## Reproduction and verification

Producer: `python3 analysis/w33_pass11600_dynamical_hesse_flavor.py`.
Certificate: `data/w33_pass11600_dynamical_hesse_flavor.json`, binding both prior
certificates, the clock owner and this producer by portable SHA256.
Focused regressions: `python3 -m pytest --noconftest -q
tests/test_w33_pass11600_dynamical_hesse_flavor.py` (disable auto-loaded plugins
where necessary). They independently check native tensor restriction, interaction
invariance, all216 projective actions, invariant dimensions, the exact low-order
obstruction, all24 minima, full scalar Hessian including its phase zero, CP transfer,
and canonical angular mass coefficients.

Final producer: all four sections PASS. Final focused suite: nine tests PASS
in48.13s. The distinctive mass coefficients and discriminant were searched
against the corpus before publication. The bare Hessian determinant921600 also
occurs in an unrelated historical arithmetic catalogue; no novelty is claimed
for that integer in isolation.
