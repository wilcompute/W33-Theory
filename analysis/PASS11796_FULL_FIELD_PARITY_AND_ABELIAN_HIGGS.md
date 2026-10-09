# Pass11796: a different full-field parity and only hypercharge in the Higgs kernel

**Constructive result:** in the actual 176-field benchmark, an alternative
order-two field-lattice character and a 13-field canonical D-flat family
preserve the candidate light matter/Higgs parity while removing every
additional Abelian Lie generator in the classical Higgs calculation.
The exact gauge mass Gram on U(1)^9 plus hidden su(2) has rank11/12;
its kernel is precisely hypercharge. Hidden SU(4) remains unbroken.
This is substantially stronger than retaining a matter sign inside a
continuous B-L direction. It is **not yet F-flatness or a physical MSSM vacuum**.

Producer: `w33_pass11796_parity_complete_abelian_higgs.py`.
Certificate: `../data/w33_pass11796_parity_complete_abelian_higgs.json`.
Independent regressions: `../tests/test_w33_pass11796_parity_complete_abelian_higgs.py`.

## What changes, and why prior certificates stay valid

Parallel3fdef4a22 owns the assignment-aware charge ledger and candidate
family constraints, avoiding the erroneous identification of every `bd`
label as a physical down antiquark. Pass11793 owns the charge lattice and
the order-four action that fixes its **particular six-singlet support**.
It proves there is no matching full-lattice order-two character **with those
six VEVs fixed**. Pass11794 constructs a hidden-center extension of that
same B-L action, but its rank-one hidden condensate retains a continuous
diagonal generator acting as B-L on visible matter.

Here **both the character and the support change**. The new parity makes
n19 and n56 odd, so it cannot use the old six-field support. This is an
escape from that fixed-support gate, not a contradiction of its certificate.
Searches checked the actual character, named fields and mass-kernel result
against the paper/index/recent analyses before framing the construction.
Published benchmark gauge congruence still does not certify complete
geometric orbifold equivalence or identical worldsheet couplings.

## Exhaust the finite character universe before choosing a vacuum

Use the exact Hermite basis of the full rational nine-U(1) lattice from
Pass11793. Let c(phi) be the integral coordinates of each of the176 fields.
Enumerate every epsilon in (Z/4)^9: **262144** characters. Require phase2
on all selected matter labels, including the declared three lepton-doublet
candidates and the four standard-charge down-antiquark labels, and phase0
on the two declared Higgs candidates (18 field constraints).

Exactly **64** characters match: **8 have full order2 and56 full order4**.
Their fixed SM/hidden-singlet sets form just four classes, with sizes
36,34,28,42 and exact charge ranks7,6,6,7. Smith normal form independently
certifies the number of solutions of the inhomogeneous congruence, while
tests enumerate epsilon=low+2*high with binary low/high as a second census.

The two rank-six classes cannot cancel FI even with signed coefficients:
each certificate gives lambda with lambda0=1 and Q_fixed^T lambda=0, so
lambda.(-e0)=-1. Both rank-seven classes have an explicit positive five-field
FI witness. No one of these64 characters admits fully Higgsing the eight
non-hypercharge Abelian directions by SM/hidden singlets alone: their full
charge-span ranks are less than8. This finite-family statement is not an
exclusion of arbitrary higher-order characters or other family assignments.

Choose the order-two character

```
epsilon2 = (0,0,1,0,1,0,0,0,0),
P(phi) = (-1)^(epsilon2.c(phi)).
```

It acts with true order2 on the full176-field carrier: **100 even and76 odd**
fields. Every selected matter field is odd and both Higgs candidates even.
This is a full field-lattice representation, not merely a Z2 image of an
order-four transformation. Global gauge/axion consistency remains separate.

## An explicit positive D-flat branch

The following are canonical squared norms, with positive arbitrary s,u,t
and FI normalized to (1,0,...,0):

| fields | squared norm of each |
|---|---:|
| n17,n47 | 9/74 |
| n50,n80,n82 | 9/37 |
| n9,n54 | s |
| n37,n38 | u |
| n35,n36,n39,n40 | t |

All thirteen fields have hypercharge zero and are **P-even**. Nine are
nonabelian singlets. The final four are (1,1,1,2), hidden SU(2) doublets.
Their actual charges satisfy

```
Q(n9)+Q(n54)=0,
Q(n37)+Q(n38)=0,
Q(n35)+Q(n36)=0,
Q(n39)=Q(n35), Q(n40)=Q(n36).
```

The first five fields give sum(norm² Q)=(-1,0,...,0) exactly.
All added pairs preserve it. Choose the doublet orientations

```
n35=sqrt(t)e1, n36=sqrt(t)e2,
n39=sqrt(t)e2, n40=sqrt(t)e1.
```

The complete hidden moment matrix is **2t I2**, so its traceless part and
all three SU(2) D terms vanish. The remaining nonabelian groups act trivially
on the entire support. Thus this is a full canonical classical D-flat family,
not an Abelian charge-balance surrogate.

## Two flavor directions remove continuous gauge locking

The nine singlet charges span rank7. Before the doublets condense their
visible residual generator has charges

```
Q,u_c,e_c: -1; d_c,L: +3; H_d: -2; H_u: +2.
```

These are the familiar SO(10)-type chi charges on this selected visible
carrier; we do not identify the full global gauge generator with a standard
SO(10) embedding solely from those numbers. The two negative-chi doublets
n35,n39 have charge -5 and their opposite partners charge +5.

With only n35,n36 nonzero, chi can be canceled by a traceless hidden
diagonal matrix: the exact gauge mass Gram has **rank10/12**. With the
second independent pair switched on, a hidden matrix canceling chi on
both n35 and n39 would have to be a nonzero scalar matrix on their full
two-dimensional color span. It cannot be traceless. The locking disappears.

At s=u=t=1/10 the producer builds the actual12x12 real gauge mass Gram
using nine Abelian generators and the three Hermitian Pauli generators.
It has rank11, and the exact kernel is

```
(0,1,0,0,0,0,0,0,0;0,0,0),  i.e. hypercharge.
```

Deleting the hypercharge row/column yields a positive principal determinant
**232296020225777740087296/1266325**. The Gram is a sum of positive weighted
squared field actions. Together these facts prove positivity on every
other gauge direction in this supplied canonical unit-coupling convention.
No physical mass eigenvalues or scale are inferred; positive gauge couplings
alter the matrix by congruence and preserve the kernel.

An independent test uses the complexified E12,E21,H generators instead of
the Pauli basis and directly solves all infinitesimal VEV-stabilizer equations.
It obtains the same one-dimensional kernel. Two separate SU(2) rotations of
the VEV frame preserve this result. Thus the absence of locking is not a
coordinate artifact. The connected unbroken algebra is the visible
su(3)+su(2)+u(1)Y plus hidden su(4).

## Selection and anomaly checks, with explicit boundaries

The actual176-field parities forbid udd,LQd,LLe,LHu and permit the three
Yukawas, mu, **QQQL and uude**. This character alone does not protect against
dimension-five proton decay. Allowed operators are not proved generated.

For the four nonabelian factors SU3,SU2_visible,SU4_hidden,SU2_hidden,
the numbers of parity-odd fundamental unit-instanton fermion zero modes are
exactly **14,18,6,10**. All are even, so the corresponding four instanton
parity phases are +1 on this massless chiral spectrum. There are144 odd
chiral components in total. These checks do not establish mixed Abelian,
global discrete, gravitational or Green-Schwarz/axion anomaly completion.

F-flatness is the immediate unsolved physical question. For example,
n35*n36 is gauge-neutral and its twist-sector sum is0 mod6; these necessary
tests neither establish nor exclude a superpotential coefficient. The
enlarged support changes the all-order F-term question from the earlier
six-support/eleven-outsider enumeration. Actual fixed points, oscillator,
R/H-momentum selection rules and coefficients/cancellations are required.
Do not call a D-flat Higgs branch a supersymmetric vacuum.

External sources checked: [Lebedev et al.](https://arxiv.org/abs/0708.2691)
for the benchmark vacuum/coupling distinctions, [Luty–Taylor](https://arxiv.org/abs/hep-th/9506098)
for the classical gauge-orbit context, and [Dreiner–Luhn–Thormeier](https://arxiv.org/abs/hep-ph/0512163)
for discrete MSSM operator selection. The13-field branch and full-lattice
census are computed on our actual ledger, not inferred from those papers.

Open: F-flatness, axion/global gauge consistency, exotic mass matrices,
physical family/Higgs identification, kinetic/Yukawa normalization,
proton-safe effective couplings, physical scales, gravity and a completed TOE.
