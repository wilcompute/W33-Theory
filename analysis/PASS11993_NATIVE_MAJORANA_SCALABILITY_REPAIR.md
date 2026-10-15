# Pass11993: an explicit Majorana carrier and the interaction that makes blocks universal

Reservation `b49bfed2d867b7997fa82490d22bc9bb151278cf` was pushed before
computation, after integrating the simultaneous catalogue-only update.
This is an additional investigation following all five11988–11992 fronts.

## Actual native gates, not just the Spin6 name

Use11987's literal six Clifford matrices as six Majorana operators of three
fermionic modes. In this convention chirality is minus fermion parity, so the
selected positive-chirality four-space is the **odd** Fock basis001,010,100,111.
The15 Hermitian bilinears i gamma_i gamma_j restrict to a trace-orthonormal
basis of all traceless Hermitian4x4 matrices. For every one of the five actual
atlas gates, take a traceless Hermitian logarithm, expand it in those15
bilinears, exponentiate on the full eight-dimensional Fock space, and check
both the4x4 gate and its six-Majorana orthogonal cover. The JSON freezes every
coefficient. This names a fermionic Hamiltonian process for the native gate
library; it is not a claim that physical Majorana modes are present in W33.

This gives another reading of11988's local complex structure: it can define a
particle/hole polarization. SO6 transport that changes it is a Bogoliubov
transformation in this declared Fock model. It need not violate a fixed complex
quantum Hilbert space. Treating the same3 as charged particle families would
still require charge, gauge and vacuum compatibility. These are different
physical interpretations of the same exact matrix construction.

## The one-block universality result does not automatically scale

For m blocks there are6m Majoranas. Their Gaussian unitary group has dimension

```
dim Spin(6m)=18m^2-3m,
dim SU(4^m)=16^m-1.
```

The dimensions agree at m=1:15. At m=2 they are66 versus255. The difference
d(m) satisfies `d(1)=0` and `d(m+1)-16d(m)=27m(10m-3)>0`, proving the strict
deficit for every m>=2. The compact subgroup preserving the encoded space and
its continuous image cannot gain Lie dimension. Gaussian unitaries alone
therefore cannot be dense in the required multiblock unitary group. This
statement assumes a fixed fermionic carrier and unitary operations; extra
non-Gaussian measurements, ancillas or postselection are outside its scope.

The actual12-Majorana,64-Fock-state two-block construction supplies a sharper
local check: of66 quadratic generators,30 preserve each block's parity; the
other36 project to zero on the16-dimensional product code and individually
send it out of the code. Thus a generic quadratic cross-block hopping term
is not already an encoded entangler on this carrier.

The general fermionic-linear-optics boundary is established literature,
not a new general no-go:
[Bravyi–Kitaev](https://arxiv.org/abs/quant-ph/0003137),
[Bravyi–Koenig](https://arxiv.org/abs/1112.2184).
The additional application here is to11987's actual atlas gates and encoding.
Searches checked the result index, local analysis sources, Holonet TeX and
the current paper; prior non-Clifford/magic-state universality is preserved.
Quantum non-Cliffordness and fermionic non-Gaussianity are distinct resources:
the11987 gates are non-Clifford in the declared qubit tensoring but all have
the quadratic Majorana realizations constructed above.

The rediscovery guard's `deficit@10` candidate is a lexical collision with
`analysis/PASS11160_TEMPORAL_CGLMP_HIGH_D.md`,
`analysis/PASS11422_DEPTH5_EXACT.md` and
`analysis/PASS11459_DEEP_DECAY.md`, read in full: their deficits are Bell-score
or Clifford-overlap shortfalls, not the Lie dimension difference d(m).
The warning is retained in the guard receipt rather than counted as a new
general theorem or silently reported as a quiet guard.
The remaining candidate `analysis/w33_clock_magic_renewal.py` was also read:
its clock-angle/Kochen--Specker resource discussion is a distinct model, not
a premise about our fermionic Gaussian control group.

## Explicit non-Gaussian repair

Add one interaction on connected block pairs:

```
Q=(i gamma0 gamma1)(i gamma6 gamma7)
 =-gamma0 gamma1 gamma6 gamma7,
Ucross=exp(-i pi Q/4).
```

Q commutes with both block parities. On the encoded four-qubit space it is
exactly Z_virtual0 Z_virtual2. Its full64-state evolution has zero code
leakage. On a declared product input it gives squared Schmidt values
1/2,1/2,0,0 between the two4D blocks, and a four-Majorana Wick-factorization
defect of magnitude1. The quartic-off control remains a product.

One fixed angle pi/4 is sufficient. Conjugate the30 continuous local SU4
Pauli generators by Ucross, then close their commutators using exact binary
Pauli labels. The closure contains **all255 nonidentity four-qubit Paulis**,
proving the generated compact closure is SU16. This is an exact label
certificate, not a tolerance-dependent numerical Lie-rank search. Local
block universality plus this connected-pair entangler gives the usual scalable
encoded construction. The needed quartic interaction is additional input.

A concrete possible low-energy source is a heavy real boson with
`V=M^2 x^2/2+g x(nA+nB)`. Eliminating x gives
`-g^2(nA+nB)^2/(2M^2)`: since n^2=n, it includes a cross density interaction
`-g^2 nA nB/M^2`. With
`nA nB=(Q+2nA+2nB-1)/4`, this supplies the required quartic up to local phases
and a constant. It is a supplied mediator matching, not a derived native
field, an exact dynamical-bus protocol or a renormalized particle model.

## Validation and scope

The producer freezes all five bilinear Hamiltonians, exact Pauli closure,
dimension controls, parity counts and non-Gaussian entanglement witness.
Seven regressions independently test frozen logarithms/covering, symbolic induction,
the fixed-angle conjugation, code leakage, quartic-off control and the actual
mediator operator identity. A dedicated workflow checks frozen inputs,
regenerates and checks again. Actual hosted status is recorded separately.

This closes a mathematical **architecture** gap left by the single-block
SU4 library. It does not construct physical fermions, a native quartic
coupler, initialization/readout, a fault-tolerance threshold, physical scales,
an interacting chiral continuum or a TOE. The original11987 and11990 results
remain valid within their stated carrier and control assumptions.
