# Pass11794: a full hidden-center D-flat branch and the surviving diagonal B-L

The benchmark has a **constructive two-parameter canonical D-flat family**
which preserves the Pass11793 matter action after multiplication by the
hidden SU(4) center. Its original B-L vector becomes massive, but a diagonal
continuous generator still acts as B-L on visible matter. The exact gauge
mass Gram has rank14 on U(1)^9 plus su(4), leaving su(3)hidden and two Abelian
directions; hidden su(2) is unchanged. This is a classical Higgs/stabilizer
result, **not an F-flat MSSM vacuum**.

## Sources, ownership and intake

- `PASS10960_MATTER_EVEN_DFLAT_CLOSURE.md` explicitly left hidden-center
  compensation outside its original singlet gate. Its amended assignment
  scope remains essential; its older blanket exclusion is not adopted.
- Parallel commit3fdef4a22 owns the assignment-aware B-L covector and the
  six-singlet FI witness for `Z6-II|Z6II_34__SM_20260917_1558`.
- `w33_pass11793_order_four_matter_action.py` owns the integral full-field
  action g=exp(i*pi*3BL), whose light image is matter parity.
- Read the new commits through d9df5bc6f and the reviewed formula catalog,
  including corrected eleven-state intervals, all-order one-outsider F gates,
  raw catalog coverage, group curvature twirls/noise, optical controls and
  the primitive triple-point quotient. Re-read source certificates and tests.
  The corrected parallel upper bound is E0<127.595507; it is not a gap.
- A prospective line/S4 spatial connection was checked **by the predicted
  result** `27/3200` against the corpus before computation. Pass11389 already
  owns the saturated FCC cover, exact S4 action, isotropic diffusion and
  fourth-order anisotropy; Pass11390-11394 owns the context clock/holonomy.
  Reservation11795 was released. The newer marked-triple quotient should be
  understood alongside that prior construction, not as a new physical space.

Producer: `analysis/w33_pass11794_hidden_center_vacuum.py`.
Certificate: `data/w33_pass11794_hidden_center_vacuum.json`.
Regressions: `tests/test_w33_pass11794_hidden_center_vacuum.py`.

## Exact classical branch

Use canonical squared VEV norms in units with FI vector (1,0,...,0):

| field | squared norm |
|---|---:|
| n17 | t |
| n19, n56 | 9/74 each |
| n50 | 9/37+t |
| n80, n82 | 9/37 each |
| n4, n5 | t each |
| n9, n54 | s each |

For every t,s>=0 the exact nine-coordinate sum is (-1,0,...,0).
At t,s>0 all ten named fields are nonzero. The last pair has opposite
charges and supplies an additional broken direction. The charged hidden
pair obeys **Q(n4)+Q(n5)=Q(n2)**, but its meson has B-L=0.

The ledger identifies n4 as (1,1,4,1) with B-L=-1 and n5 as
(1,1,conjugate4,1) with B-L=+1. Choose both VEVs along their first hidden
color with equal norm sqrt(t). Their **entire** SU(4) moment map, not just
its Cartan part, is t E11-t E11=0. They are visible SU(3)/SU(2) singlets
with hypercharge zero. All other VEVs are singlets of every nonabelian group.
Thus all nonabelian D terms vanish, and the Abelian terms cancel FI exactly.
Singlet phases are unconstrained by this D calculation; F terms can depend
on them and remain unevaluated.

The unbroken transformation is

```
g_hat = exp(i*pi*3BL) * (-I_SU4).
```

Both n4 and n5 have g phase -1, canceled by their hidden center -1.
The visible matter and Higgs are hidden singlets, so their action is exactly
the Pass11793 light matter parity. This does not supply additional protection
against the already permitted QQQL/uude operators.

## Gauge mass kernel: breaking a vector is not removing its visible action

At t=s=1/10 build the mass Gram from all ten actual field actions using
nine Abelian generators and fifteen explicit Hermitian SU(4) generators.
All gauge couplings are set to one for this diagnostic; positive nonzero
couplings change the Gram by congruence and preserve its nullity. Conventional
overall mass factors and kinetic normalizations are not physical predictions.
The exact rational 24x24 Gram is positive semidefinite and has **rank14**.
Six off-diagonal and two diagonal generators on the three unused hidden
colors give su(3)hidden. Hypercharge gives a ninth zero direction.

The tenth is

```
B_diag = BL + T,
T = diag(1,-1/3,-1/3,-1/3) in hidden su(4).
```

Its action on n4 is -e1+T e1=0 and on n5 is e1-T^T e1=0.
All neutral singlet VEVs are fixed. Bare BL has nonzero quadratic mass form
2t=1/5 at the displayed point, yet B_diag is exactly in the kernel.
Visible fields are hidden singlets, hence B_diag acts on them as BL does.
The connected surviving Lie algebra is

```
su(3)_hidden + su(2)_hidden + u(1)_Y + u(1)_B_diag.
```

Moreover exp(i*3pi*T)=-I_SU4, so **g_hat itself is contained in the
connected diagonal U(1)**. Retaining a matter-sign transformation does not
here establish a discrete remnant after removing continuous B-L.

Regressions rotate the VEVs by an independently specified complex SU(4)
matrix, transform T with them, and recheck the full moment map and the
locked generator. A unimodular change of Abelian coordinates preserves the
mass-kernel identity. These are controls against a basis artifact.

## Exhaustion of all eight center lifts of this fixed action

Enumerate g times i^(a nality4) times (-1)^(b nality2) for a=0,1,2,3
and b=0,1 on every SM-neutral elementary field in the original 176-field
ledger. Hypercharge is essential: the apparent half-BL hidden fundamentals
v2,bv2,v5,bv5 carry hypercharge +/-1/2 and cannot condense while preserving
the Standard Model gauge group.

For a=0,1,3 **every fixed SM-neutral field has BL=0**. For a=2 the only
BL-charged fixed fields are the single fundamental n4 and antifundamental
n5. Hidden SU(2) centers cannot cancel the +/-i phases of its BL-half
doublets. All 42 fully neutral BL-zero singlets have charge-span rank7;
none can remove BL or hypercharge.

For an arbitrary canonical D-flat configuration in the a=2 fixed sector,
write the two hidden VEVs as F,A. SU(4) D-flatness means the traceless part
of F Fdagger-Astar AT vanishes. This matrix has rank at most2, whereas a
nonzero scalar I4 has rank4. Therefore it is zero. Nonzero rank-one
projectors are equal, forcing equal norms and conjugate alignment. Gauge
rotate to the displayed e1 configuration: B_diag survives. If both VEVs
vanish, bare BL survives instead.

Consequently **none of these eight center lifts removes every continuous
generator acting as BL on visible matter** by classical SM-preserving
elementary D-flat VEVs in this ledger. This is not an exclusion of all
possible characters or all physical vacua.

## External checks and remaining physics

Lebedev et al., [The Heterotic Road to the MSSM with R parity](https://arxiv.org/abs/0708.2691),
is the source of the benchmark gauge-comparison program and distinguishes
actual vacuum/coupling questions from spectra. Luty and Taylor,
[Varieties of vacua in classical supersymmetric gauge theories](https://arxiv.org/abs/hep-th/9506098),
provides the classical gauge-orbit/moduli context. The displayed branch and
eight-lift classification are computed against our frozen charge ledger;
they are not imported claims of a successful published vacuum.

Open: full worldsheet selection rules and F-flatness on the enlarged support,
other Abelian characters and B-L assignments, noncentral compensation,
strong-coupling composite condensates, global gauge/axion/Stueckelberg data,
exotic mass ranks, physical Yukawas, proton protection and observed scales.
No gravity, masses or completed TOE follow from this Higgs-branch result.
