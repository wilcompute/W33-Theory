# Passes 2937–2945 — global protected readout, Landauer compiler, OAM audit, and two outside-box closures

## Evidence ladder

- **Exact:** finite-field enumeration, closed integer programs, exhaustive code/group checks, symbolic algebra.
- **Modelled:** independent detector-bit calibration and an adversarial accepted-fault envelope.
- **Source-complete:** syndrome decoder RTL and exhaustive one-bit testbench.
- **Open:** physical OAM crosstalk, circuit-specific M36 malignant sets, FPGA timing, and laboratory calibration.

## 2937 — global affine-support distance four

Every affine-Clifford binary support probe is

\[
f_{a,b}(x)=\mathbf1[a\cdot x+b\ne0]=(a\cdot x+b)^2,
\qquad x\in\mathbf F_3^4.
\]

Modulo simultaneous sign there are exactly 120 nonconstant probes. An exact integer program on `AG(3,3)` proves that every restricted distance-four multiset needs at least 12 probes, and exhibits 12. There are 120 affine three-flats in `AG(4,3)`; each global probe is nonconstant on 117. Double counting gives

\[
117n\ge120\cdot12,
\qquad n\ge13.
\]

An explicit 16-probe witness has 81 distinct words and binary minimum distance four:

\[
\boxed{13\le n_{\rm affine-support,d=4}\le16.}
\]

This beats the previous 24-sample construction globally. It does not prove 16 optimal.

## 2938 and 2941 — the hidden ternary code

The sixteen probes are two affine offsets on each of eight directions. Their underlying ternary values form an exact `[8,4,4]_3` code with weight enumerator

\[
1+22z^4+24z^5+20z^6+8z^7+6z^8.
\]

An explicit signed coordinate permutation maps the code to its dual, while `G^T G` is nonzero. Hence it is **isodual and formally self-dual, but not self-dual**. The eleven weight-four supports have coordinate automorphism group `S4` of order 24; including signs gives `C2 x S4` of order 48.

All sixteen nonzero one-symbol syndromes are distinct. The decoder therefore becomes

```text
16 support bits -> eight ternary symbols/erasures
 -> four-trit syndrome -> 16-entry correction table
 -> recover four frame trits.
```

This replaces an 81-codeword binary nearest-neighbour scan.

### Bonkers result 1 — measurement/check reciprocity

Isoduality means the generator and parity-check networks are the same ternary mixer after a signed coordinate relabeling. One physical mixer topology can therefore serve encode and diagnose roles. This is an exact wiring equivalence, not a claim of thermodynamic time reversal.

## 2939 — circuit-independent M36 fault envelope

The exact accepted-output saddle-node budget is

\[
g_c=\frac{7-3\sqrt5}{4}\approx0.072949016875.
\]

The repo contains an exact stabilizer projector but not one canonical gate decomposition, so this packet does not invent a circuit threshold. If a compiled accepted branch has `L` independent locations with per-location fault probability `q`, then a pessimistic accepted-fault envelope is

\[
f\le1-(1-q)^L,
\qquad p_{\rm out}\le f+(1-f)R(p).
\]

A sufficient condition is

\[
q<1-(1-g_c)^{1/L}.
\]

For `L=8,12,16,24,32`, this gives `0.942%`, `0.629%`, `0.472%`, `0.315%`, and `0.236%`. These are adversarial budgets, not compiled-circuit thresholds.

## 2940 — calibrated active diagnosis

For the explicit independent channel

```text
false positive = 0.002
false negative = 0.03
prior support-one probability = 2/3,
```

Bayes-optimal repeated-bit decisions plus a union bound over at most sixteen observed bits give:

| total failure target | repetitions/bit | certified bound |
|---:|---:|---:|
| `1e-3` | 5 | `2.546e-4` |
| `1e-6` | 9 | `6.148e-7` |
| `1e-9` | 13 | `3.513e-10` |
| `1e-12` | 18 | `1.102e-13` |

This is model-calibrated logic, not detector data.

## 2942 — Landauer audit and thermodynamic compiler

The existing paper correctly separates reversible frame computation from irreversible observation and destructive routing. The new theorem concerns complete diagnosis. For a uniform 81-state frame, any deterministic exact terminal transcript is in bijection with the initial state, so

\[
\boxed{H(T)=H(X)=\log_2 81=6.33985000288\text{ bits}.}
\]

Adaptivity changes latency and raw storage but not the optimally compressed Landauer information floor.

- Static observer: 8 raw bits; redundancy `1.66015` bits.
- Protected observer: 16 raw bits; redundancy `9.66015` bits.
- Four-mask adaptive policy: expected uncompressed storage `4(94/27)=13.9259` bits.

For an at-most-one-error block with total error probability `p` and sixteen equiprobable locations, reversible syndrome extraction followed by record erasure exports

\[
H(E)=h_2(p)+4p
\]

bits rather than blindly erasing sixteen. Finite-time reset adds positive protocol-dependent dissipation above the quasistatic floor; an absolute number requires a physical reset model.

### Bonkers result 2 — compile for information gain per erased bit

A diagnostic compiler should optimize latency and raw transcript entropy separately. No exact compiler can beat `log2(81)` compressed bits. Its thermodynamic opportunity is to approach that floor while buying the needed error distance, rather than assuming a shorter decision tree changes the fundamental information erased.

## 2943 — does the Holonet use OAM?

**Abstractly, OAM is optional.** Any two independent qutrit-capable photon degrees of freedom suffice.

**In a major concrete hardware profile, OAM is explicit.** The repo contains an `ell in {-1,0,+1}` qutrit, operator/OAM dictionary, nine-sector recenter ABI, 24-word centered kernel, three-shell Laguerre–Gaussian surrogate, 77,760-tick witness replay, and proposed OAM/GKP mode banks. The radial leakage figures are correctly labelled symbolic rather than measured.

A new full-group audit enumerates all 51,840 projective symplectic-similitude actions on the forty W33 points. There are sixteen cycle types; the largest single cycle has length 12 and no 40-cycle exists:

\[
\boxed{\text{one cyclic OAM shift cannot be the complete W33 address bus}.}
\]

A geometry-preserving implementation needs a multi-cycle sorter/interferometer, multiple mode registers, or a hybrid OAM-times-time/frequency address. This does not forbid arbitrary non-symmetry permutations.

## Reproduction

```bash
python analysis/bt2937_2945_global_code_landauer_oam.py
python analysis/bt2937_2945_global_code_landauer_oam.py --verify-frozen
pytest -q tests/test_bt2937_2945_global_code_landauer_oam.py
```
