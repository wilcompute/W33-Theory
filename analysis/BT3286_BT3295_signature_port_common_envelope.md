# Passes 3286–3295 — Signature/port obstruction and the minimal common controller

## Status

**Exact finite theorem and source-level controller equivalence.** The local verifier passed 13/13 checks, the frozen pytest passed, and the shared TeX insert compiled twice in a standalone document. FPGA synthesis, placement, full-manuscript PDF observation, optical calibration, and the final chromatic decision remain fail-closed.

## 3286 — the requested signature-to-port intertwiner does not exist under full symmetry

The exact-cover signature alphabet has orbit profile

\[
\Omega_{\rm sig}:1+3+6+6
\]

under cell permutations. The natural port alphabet of the local \(V_4\) orthogonal array,

\[
\Omega_{\rm port}=\{(a,b,c)\in V_4^3:a+b+c=0\},
\]

has profile

\[
\Omega_{\rm port}:1+3+3+3+6.
\]

Their characters are respectively

\[
\chi_{\rm sig}=(16,2,1),\qquad \chi_{\rm port}=(16,4,1).
\]

Therefore

\[
\boxed{\operatorname{Bij}_{S_3}(\Omega_{\rm sig},\Omega_{\rm port})=\varnothing.}
\]

This closes the prior “find the direct intertwiner” target by exact obstruction rather than failed search.

## 3287 — orientation-preserving transport breaks through

On the rotation subgroup \(C_3=A_3\), both alphabets restrict to

\[
1+3+3+3+3+3.
\]

Hence there are exactly

\[
\boxed{5!\,3^5=29{,}160}
\]

\(C_3\)-equivariant bijections. A canonical representative is frozen in the JSON certificate. The reflection subgroup still distinguishes the alphabets:

\[
\Omega_{\rm sig}|_{C_2}:1^2 2^7,
\qquad
\Omega_{\rm port}|_{C_2}:1^4 2^6.
\]

The mismatch is therefore precisely chirality/reflection-sensitive.

## 3288 — representation-ring defect

The rational permutation modules are

\[
\mathbb Q[\Omega_{\rm sig}]
\cong4\mathbf1\oplus2\,\mathrm{sgn}\oplus5V_{\rm std},
\]

\[
\mathbb Q[\Omega_{\rm port}]
\cong5\mathbf1\oplus\mathrm{sgn}\oplus5V_{\rm std}.
\]

Thus

\[
\boxed{[\Omega_{\rm port}]-[\Omega_{\rm sig}]=[\mathbf1]-[\mathrm{sgn}]}
\]

and stably

\[
\boxed{\mathbb Q[\Omega_{\rm sig}]\oplus\mathbf1
\cong\mathbb Q[\Omega_{\rm port}]\oplus\mathrm{sgn}.}
\]

The defect vanishes upon restriction to \(C_3\), where sign becomes trivial.

## 3289 — rank-45 global audit

The signature commutant has dimension 45 and orbital histogram

\[
1^1 3^3 6^{41}.
\]

The natural port commutant has dimension 51 and histogram

\[
1^1 3^{15}6^{35}.
\]

Therefore the existing equality between 45 anchor octets and 45 signature orbitals cannot be lifted through the unmodified port action. The six-direction rank defect is structural, not a missing coordinate convention.

## 3290 — minimal common envelope

At the set level, the orbit multiplicities are

\[
\Omega_{\rm sig}:1^1 3^1 6^2,
\qquad
\Omega_{\rm port}:1^1 3^3 6^1.
\]

The componentwise maximum gives the minimal common \(S_3\)-envelope

\[
1^1 3^3 6^2,
\qquad
\boxed{|\Omega_{\rm env}|=22}.
\]

The maximum equivariant overlap is

\[
\boxed{10},
\qquad 16+16-10=22.
\]

Both alphabets are embedded explicitly into one linear \(S_3\)-action on \(\mathbb F_2^5\). The 32 ambient words split into 22 valid envelope states and 10 guard words.

## 3291 — controller comparison

Three source-level controllers are supplied:

1. a four-bit nonlinear signature ROM, algebraic degree three with 27 ANF terms;
2. a four-bit linear natural-port controller, using two XORs per generator core;
3. a shared five-bit linear envelope controller, using one XOR per generator core plus wire permutations before opcode multiplexing.

The supplied testbench checks \(R^3=S^2=I\), \(SRS=R^{-1}\), all signature and port state transitions, the 22-state valid envelope, and the ten guard words. Observed Icarus/Yosys numbers require the guarded CI lane and are not inferred from source structure.

## 3292 — chromatic proof firewall

A ten-colour proof or solver quotient may not identify local signatures with natural ports under full \(S_3\); that quotient is mathematically false. A \(C_3\)-only orientation-preserving quotient is locally compatible, but it still has 29,160 local gauge choices before global consistency. No ten-colouring and no checked UNSAT proof was produced. The exact boundary remains

\[
\boxed{10\leq\chi(H)\leq11.}
\]

## Two outside-box constructions

### Orientation defect line

The entire signature/port mismatch is the virtual line \(\mathbf1-\mathrm{sgn}\). This is an exact finite representation statement, not a claim of a physical anomaly.

### Twenty-two-state universal controller

The two 16-state alphabets are not forced into a false identity. They become overlapping codebooks in one 22-state invariant language, with ten shared words and ten ambient guard words. This turns the obstruction into a concrete typed-controller architecture.

## Reproduction

The merged bootstrap packet reconstructs the full verifier, frozen JSON, RTL, testbench, workflow, and front-door updates byte-for-byte. Expected verifier line:

```text
PASS 13/13 exact signature-port common-envelope checks
```

## Evidence boundary

The results above are exact finite calculations and source-level logic identities. They do not establish FPGA area/timing, physical loss/fidelity, a canonical global \(C_3\) gauge, or the value of \(\chi(H)\).
