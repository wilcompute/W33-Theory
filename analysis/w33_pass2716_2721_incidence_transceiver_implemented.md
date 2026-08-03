# Passes 2716–2721 — the incidence transceiver is now an exact digital datapath

The newest parallel frontier was reconciled before continuation.  Parallel Passes
2682–2689 built the nine-cell Kraft router and independently verified the manuscript
theorem

\[
T=N-\frac1{10}J,\qquad \operatorname{rank}T=24,\qquad
T^{\mathsf T}T=6E_{24},
\]

but explicitly left transceiver RTL open.  Parallel Passes 2690–2715 then occupied the
next namespace while still listing the transceiver as unbuilt.  This packet closes that
specific digital implementation boundary in the collision-free namespace 2716–2721.

---

## Pass 2716 — integer digital form

Use the exact integral scale

\[
\boxed{S=10T=10N-J.}
\]

Each output row contains four coefficients `+9` and thirty-six coefficients `-1`, so

\[
\boxed{
 y_i=10\sum_{j\sim i}x_j-\sum_{j=0}^{39}x_j
 = (\operatorname{local4}_i\ll3)+(\operatorname{local4}_i\ll1)-\operatorname{global40}.
}
\]

Therefore the digital transceiver needs **no general multipliers** and no internal
fractional coefficients.  A conservative signed width is `OW=W+7`, since every row has
\(\ell_1\)-norm \(4\cdot9+36=72\).

The self-contained verifier reconstructs `W(3,3)` from projective points over
\(\mathbb F_3^4\), enumerates the forty isotropic lines, and freezes forty forward and
forty reverse four-tap masks.

Exact results:

\[
\boxed{\operatorname{rank}_{\mathbb Q}S=24,}
\]

\[
\boxed{S^{\mathsf T}S=600E_{24}^{P},\qquad SS^{\mathsf T}=600E_{24}^{L},}
\]

and hence

\[
\boxed{(S^{\mathsf T}S)^2=600S^{\mathsf T}S,\qquad
(SS^{\mathsf T})^2=600SS^{\mathsf T}.}
\]

The all-ones mode is killed on both sides.  On the shared rank-24 image, exact digital
decoding is the gain-normalized composition

\[
\boxed{x=\frac1{600}S^{\mathsf T}Sx.}
\]

The frozen certificate SHA-256 is

```text
ceedf1972f11c6a0f8309558ea0d93d907943cbfe5da352bd373c9bec288c2dd
```

---

## Pass 2717 — bidirectional RTL and placeable serial wrapper

`rtl/w33_pass2717_incidence_transceiver.sv` contains:

1. `w33_pass2717_incidence_core`, parameterized by signed input width and direction;
2. `REVERSE=0` for point-to-line transport and `REVERSE=1` for line-to-point transport;
3. frozen 40-bit incidence masks in both directions;
4. a shift-add implementation of multiplication by ten;
5. `w33_pass2717_incidence_serial`, which loads forty lanes and drains forty lanes so the
   matrix remains internal instead of becoming hundreds of package pins.

This applies the placement lesson from Pass 2612: a correct flat matrix core is not yet a
usable device interface.

---

## Pass 2718 — basis, kernel, and streaming testbench

The SystemVerilog testbench checks:

- a forward basis point produces `+9` on its four incident lines and `-1` elsewhere;
- a reverse basis line produces `+9` on its four incident points and `-1` elsewhere;
- constant vectors are annihilated in both directions;
- the serial wrapper preserves lane ordering and returns to its loading state.

---

## Passes 2719–2721 — frozen certificate, focused tests, and CI

The committed JSON records all exact masks, projector identities, and the evidence
boundary.  The Python regression reconstructs the geometry independently, verifies the
certificate digest, and checks that the RTL mask multiset is literally the reconstructed
incidence matrix and its transpose.

The focused workflow recomputes the certificate, requires a clean JSON diff, runs the
Python tests, compiles the SystemVerilog with Icarus, and executes the RTL testbench.
Remote Actions status is not assumed until GitHub reports it.

---

## Namespace reconciliation

An initial draft used Passes 2690–2695.  A wider parallel-commit scan then showed that the
parallel track had already occupied 2690–2715.  The packet was byte-preservingly relabelled
to 2716–2721, its certificate digest was recomputed for the corrected metadata, and all
superseded 2690–2695 filenames were removed.  The parallel track's legitimate files were
not touched.

---

## Evidence boundary

This closes an exact **digital** implementation of `10T` and its streamed interface.
It does **not** provide:

- the optical amplitude normalization \(T/\sqrt6\);
- an insertion-loss or noise budget;
- detector transfer functions;
- a calibration procedure;
- proof that integer division by `600` should be implemented inside the datapath.

The natural hardware boundary is to keep the reversible integer gain through the digital
pipeline and normalize only at a specified interface.  Any optical claim remains open.

---

## Ledger

| claim | status |
|---|---|
| exact integer transceiver exists | **proved: `S=10N-J`** |
| general multipliers are required | **refuted: shift-add plus sums suffice** |
| forward and reverse maps are supported | **implemented with frozen transpose masks** |
| flat 40-lane package interface is required | **refuted: streamed wrapper supplied** |
| rank-24 lossless sector survives integer scaling | **proved, gain `600`** |
| optical `1/sqrt(6)` transceiver is implemented | **not claimed** |
| remote CI passed | **pending GitHub status** |

## Prior art

- `photonic_holonet_body.tex`, incidence-transceiver subsection — owns the rank-24 theorem
  and optical evidence firewall.
- `analysis/w33_pass173_incidence_transceiver_route_dark_lattice.py` — owns the exact
  lattice and selector theorem.
- parallel Passes 2682–2689 — own the Kraft-router RTL and the independent numerical
  transceiver verification.

## Still open

- Synthesis/place-and-route census for the streamed transceiver.
- A power-of-two or residue-domain normalization strategy for gain `600`.
- Optical amplitude, loss, detector, and calibration models.
- Five remaining ISA instructions, beginning with the first two-register `CX` frame
  update.
- The long-standing mathematical fronts: `chi(H) in {10,11}`, commutative-fusion ranks
  10–14, complete `U6`, and the unrepaired certificate producers.
