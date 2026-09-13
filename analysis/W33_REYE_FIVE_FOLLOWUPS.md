# Five Reye computation followups executed

All five requested directions now have executable implementations or experiments.
The register, compiler and noise results are in `w33_reye_control_extensions.py`
and its adjacent JSON; the explicit kernel is in
`w33_schur_cross_kernel_matrices.py` and JSON. Holotrade owns the exact dual-witness
transaction implementation. Each extends previously published objects rather than
claiming to discover the underlying geometry or general control theorems.

## 1. A connected family of computational registers

Each tile has three qubits and the fifteen independently switchable Pauli
Hamiltonians established in `w33_reye_sector_control.py`. Add one controllable
`Z(first) tensor Z(first)` interaction between each neighbouring pair of tiles.
Inside each tile choose its first qubit as a routing hub. This makes a connected
qubit interaction graph for every positive number of tiles.

`network_compile(registers,control,target)` emits a chronological adjacent-CNOT
program: move the control along a path using SWAPs, execute the final adjacent
CNOT, and reverse those SWAPs. Each SWAP is three CNOTs. Every spectator is
restored. Exact basis-permutation comparisons check all 108 ordered qubit pairs
across one, two and three tiles, including all spectator states. The routing
argument applies to every finite chain; enumeration alone is not its proof.

The port lowering is explicit, with `R_P(theta)=exp(-i theta P)`:

    CZ = exp(-i*pi/4) R_Za(-pi/4) R_Zb(-pi/4) R_ZaZb(pi/4)
    CNOT(a,b) = H_b CZ H_b
    H = i R_Y(pi/4) R_Z(pi/2).

`lower_network` returns product-order Pauli pulses and the global phase. It uses
the existing native tile pulse compiler for all local operations and the declared
ZZ port for cross-tile interactions. The two-tile CNOT from qubit 2 to qubit 5
lowers to 247 pulses. Its full 64-by-64 matrix agrees with CNOT to approximately
`1.01e-14`, including coherent phase. A port Bell-state check gives reduced purity
one half.

Arbitrary one-qubit rotations and these routed CNOTs provide the standard circuit
universality construction; see [Bremner et al.](https://arxiv.org/abs/quant-ph/0207072).
The contribution here is the concrete tile interface, router and pulse lowering.
This is a logically scalable architecture under explicit control and coupling
assumptions, not evidence of physical scalability, error correction, unbounded
storage, or an operational photonic machine.

## 2. Certified pulse reduction

Use the 63 nonidentity Pauli directions as vertices. Conjugation by an available
native pi/4 pulse joins anticommuting words `B` and `A XOR B`. Multisource BFS from
the fifteen native directions produces a shortest native-conjugation template.
A target at distance d requires `2d+1` pulses in that template.

The compiler reduces the aggregate for all 63 rotations from **369 to 337**
pulses; the worst case drops from **21 to 15**. No individual word regresses.
All full coherent matrices are checked. The certificate records the per-word
counts and distances. It also checks, for every anticommuting pair, the lower-bound
potential inequality `cost(C) <= 2 cost(A)+cost(B)`. Native costs are one and the
constructed witnesses attain their costs. Induction proves minimality within
this recursive conjugation grammar. Arbitrary identities, cross-instruction
cancellation, time scheduling and device-weighted costs are outside that claim.

## 3. Synthetic error experiments that separate leakage from coherence

The channel simulator uses unit nominal Rabi rate and pulse time `abs(angle)`.
Its coherent Hamiltonian has a fractional amplitude error on the driven Pauli,
static Z2 detuning, and static X2 crosstalk. Independent Markov Z2 dephasing is
applied after each pulse with probability `(1-exp(-2 gamma time))/2`. These are
explicit uncalibrated model parameters, not measurements from a device. Nine
parameter settings are checked on all twelve sector-addressed rotations.

Each channel passes trace-preservation checks. The reported average gate fidelity
is computed from the Kraus operators against the ideal complete eight-dimensional
unitary, rather than from a favourable input state. Worst-case sector leakage is
the largest eigenvalue of `Q sum K^dagger(I-Q)K Q`.

| Model setting | Minimum average gate fidelity | Maximum sector leakage |
|---|---:|---:|
| Ideal | 1 within numerical precision | 0 within numerical precision |
| Amplitude error 0.01 | 0.99998629 | 0 within numerical precision |
| X2 crosstalk 0.01 | 0.99994733 | 0.00005839 |
| X2 crosstalk 0.05 | 0.99868393 | 0.00145902 |
| Z2 dephasing rate 0.01 | 0.99307323 | 0 within numerical precision |

The last row is the useful architectural warning: sector population checks can
pass while inter-sector coherence is damaged. A register admission test needs a
coherent channel test as well as a leakage test. No fault-tolerance threshold,
calibrated operating point or hardware performance is inferred.

## 4. Holotrade verifies mathematics before signing delivery

Holotrade's `js/w33-dual-witness.js` verifies actual 40-coordinate integer vectors
and exact BigInt rationals. The opt-in policy mode `dual-one-step-v1` pins the
incidence geometry and permitted circuit-move digests before execution.

The existing transaction path now checks input/fibre/output identities, the
actual vector transition, both line images, dual feasibility and a zero l1
duality gap. Four-regular incidence fixes the sum of preimage coordinates, so
this l1 optimum also certifies minimum negative mass in the complete integer
fibre. The actual endpoint cost must match the policy's exact depth. The signed
delivery carries the verified-witness digest through the existing result and
policy identities.

Six transaction tests pass, preserving the three legacy tests and adding both
existing exact escape witnesses, eleven malformed/substituted proof cases, an
exact rational perturbation below floating precision, policy downgrade rejection,
permitted-move binding and equivalent rational encodings. The fixture is checked
against its existing Python geometry and original dual certificates without site
packages. Test attestation verdicts are simulated; this is not real hardware
attestation. Legacy policies retain their original summary-check semantics. The
new proof mode currently accepts one strictly descending permitted circuit step;
it does not yet verify arbitrary multi-step histories or independently regenerate
the complete allowed circuit library.

## 5. The cross-fibre kernel is explicitly a Pauli frame group

For `omega=(-1+i sqrt(3))/2`, define

    A = [[-1,1],[2,1]] / sqrt(3)
    B = [[-1,omega],[2 conjugate(omega),1]] / sqrt(3).

Then `A^2=B^2=I` and `AB=-BA`. All sixteen matrices `i^p A^a B^b` preserve the
actual binary quartic `u(u^3-v^3)` and its companion Hessian polynomial. They
therefore realize the order-16 kernel already identified by the prior
`w33_schur176_sixteen_line_fibre_structure.py` certificate. The geometric source
is [Nurowski's Schur/Reye construction](https://arxiv.org/abs/2609.10751).

The exact multiplication rule is

    (p,a,b)*(q,c,d) = (p+q+2bc mod4, a XOR c, b XOR d).

The script checks all 256 products, exports the sixteen matrices and multiplication
table, and checks an independent regular permutation realization. Its center has
order four; the element-order counts are one identity, seven involutions and eight
order-four elements.

Choose `v=(1,1+sqrt(3))^T` and `S=[v,Bv]`. The exported exact conjugator satisfies
`S^-1 A S=Z` and `S^-1 B S=X`. The original-coordinate positive Hermitian form is
`G=diag(2,1)`, and `S^dagger G S` is a positive scalar identity. Thus this is the
one-qubit Pauli group including central phases, with the metric and change of
basis displayed explicitly. Its projective V4 quotient is a finite two-bit frame;
the additional phase register is essential to multiplication. The finite group
alone is not a universal gate set. No canonical physical metric or common global
action on all eleven Schur blocks is claimed.

## Reproduction and boundaries

    OPENBLAS_NUM_THREADS=1 python3 analysis/w33_reye_control_extensions.py
    python3 analysis/w33_schur_cross_kernel_matrices.py

Use `--write` to regenerate the adjacent W33 certificates. In Holotrade:

    python3 -S analysis/export_octet_dual_transaction_fixture.py --check
    node --test tests/w33-certified-decoder-transaction.test.js

Focused CI workflows were added in both repositories. Local checks pass; full
repository CI, remote workflow outcomes and full manuscript builds were not
verified in this execution. Existing unrelated dirty files are preserved.
The historical full-reading backlog remains open. Searches covered existing
result strings, the result index, both repositories, and primary literature;
this report asserts concrete extensions, not worldwide novelty.
