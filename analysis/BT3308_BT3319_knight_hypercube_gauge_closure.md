# Passes 3308–3319 — Knight-hypercube gauge closure and typed controller network

## Status

**Exact finite mathematics, executable compiler, and source-level digital architecture.** The focused verifier reports **18/18** exact checks. It reconstructs the W33 45-block/720-edge/240-face port complex, the toroidal-knight \(Q_4\) network, the nonlinear signature controller, the five-bit common envelope, and every stated group action from source.

The dedicated workflow performs Icarus simulation, Yosys synthesis, optional nextpnr placement, certificate regeneration, focused regression, and all three manuscript builds. Until that workflow is observed, source-level logic counts are not promoted to placed cell counts, timing, or FPGA performance.

The chromatic frontier remains

\[
\boxed{10\leq\chi(H)\leq11}.
\]

---

## 3308 — global \(C_3\) signature/port gauge cohomology

Passes 3286–3295 proved that the signature and natural-port alphabets are inequivalent as full \(S_3\)-sets but equivalent after restricting to the orientation subgroup \(C_3=A_3\). The local intertwiner set is a torsor under

\[
W=C_3\wr S_5,
\qquad |W|=3^5\,5!=29{,}160.
\]

The filled port complex has homotopy model

\[
X\simeq\bigvee^{436}S^1,
\qquad \pi_1(X)\cong F_{436}.
\]

If the pairing of the five three-cycles is frozen, the residual phase group is

\[
A=C_3^5.
\]

Therefore

\[
H^1(X;A)\cong A^{436}\cong\mathbb F_3^{2180}.
\]

The number of flat phase sectors is \(3^{2180}\), a 1,041-digit integer. Its decimal SHA-256 and leading/trailing digits are frozen in the certificate.

If orbit pairing is not frozen, flat \(W\)-connections modulo switching are simultaneous-conjugacy classes

\[
\operatorname{Hom}(F_{436},W)/W.
\]

Conjugacy classes of \(C_3\wr S_5\) are indexed by triples of partitions with total size five. There are exactly 108 types. Burnside gives

\[
\boxed{
N_W=
\sum_{[g]\subset W}|C_W(g)|^{435},
}
\]

a 1,943-digit exact integer, also frozen by SHA-256 and boundary digits.

A trivial flat gauge exists. The finite geometry does **not** select one canonically.

---

## 3309 — controller synthesis duel

Three architectures are compared under one evidence contract:

1. `w33_signature_s3_rom4`: four-bit nonlinear signature ROM;
2. `w33_port_s3_linear4`: four-bit linear natural-port controller;
3. `w33_signature_port_linear5`: five-bit linear shared envelope.

Exact source-level metrics remain:

| controller | exact source structure |
|---|---|
| four-bit signature | algebraic degree three; 27 ANF terms |
| four-bit port | two XORs per generator core |
| five-bit envelope | one XOR per generator core plus wire permutations |

The workflow compiles all three under the same Yosys flow and runs the same registered wrapper shape. It also runs the exhaustive signature-router testbench. Any missing simulator, synthesis, placement, timing, or artifact keeps the corresponding evidence field unobserved.

---

## 3310 — the full 22-state common-envelope algebra

The common envelope is the \(S_3\)-set

\[
\Omega_{\rm env}
\cong
1\sqcup3(S_3/C_2)\sqcup2S_3,
\qquad |\Omega_{\rm env}|=22.
\]

Its character is

\[
\chi_{\rm env}=(22,4,1),
\]

and its rational permutation module is

\[
\boxed{
\mathbb Q[\Omega_{\rm env}]
\cong
6\mathbf1\oplus2\,\mathrm{sgn}\oplus7V_{\rm std}.
}
\]

Thus

\[
\boxed{
\dim\operatorname{End}_{S_3}\mathbb Q[\Omega_{\rm env}]
=
6^2+2^2+7^2
=
89.
}
\]

Direct diagonal-orbit enumeration gives exactly 89 orbitals with size histogram

\[
\boxed{1^1\,3^{15}\,6^{73}}.
\]

The Terwilliger algebra depends sharply on the base-state orbit. Closure over two independent large prime fields gives:

\[
\boxed{
\dim T_x=
\begin{cases}
89,&x\text{ fixed},\\
222,&x\text{ in a three-state orbit},\\
484=22^2,&x\text{ in a regular six-state orbit}.
\end{cases}
}
\]

The regular signature basepoint therefore generates the full matrix algebra \(M_{22}\). At that basepoint there is no nontrivial exact algebraic compression left.

---

## 3311 — orientation-carrying chromatic compiler

The release emits a complete canonical coboundary-gauge manifest containing:

- 45 block gauges;
- 720 exact block-graph edges;
- 240 filled support triangles;
- one explicit 16-state \(C_3\)-equivariant signature-to-port bijection;
- transported five-trit edge gains;
- zero face holonomy witnesses.

Every block, edge, and face is rebuilt from the W33 frame geometry rather than copied from a count ledger.

This compiler is an exact bijective relabeling. Consequently a formula and its fully transported relabeling are syntactically isomorphic and equisatisfiable.

It does **not** reduce the current 7,800-variable ten-colour CNF. The current CNF does not expose the new signature variables as a complete quotient interface. Any future quotient must transport every local and cross-block clause and retain the independent 540-frame model checker.

---

## 3312 — anchor/orbital correspondence audit

The signature alphabet has 45 diagonal orbitals, but its intrinsic \(S_3\)-set automorphism group has order

\[
\boxed{72}.
\]

Acting on the 45 orbitals, this group produces only 13 classes, with class-size histogram

\[
\boxed{
1^5\,2^3\,4^1\,6^3\,12^1.
}
\]

Therefore the local signature structure does not canonically distinguish 45 individually labeled orbitals. The 45 anchor octets, by contrast, are a global transitive \(PSp(4,3)\)-set.

Hence the numerical equality

\[
45\text{ anchors}=45\text{ signature orbitals}
\]

does not by itself define an anchor/orbital bijection. Any such correspondence requires additional global \(PSp(4,3)\)-equivariant data.

This is a canonicity obstruction, not a proof that no correspondence can be introduced with extra structure.

---

## 3313 — bonkers construction A: optimal nonlinear controller on the toroidal knight network

The repository already proves objectwise that the \(4\times4\) toroidal knight graph is

\[
Q_4,
\]

with 16 vertices, 32 links, degree four, diameter four, and a knight-tour Hamilton cycle that becomes a four-bit Gray cycle. Its Hamming layers give the Clifford/Pascal profile

\[
1,4,6,4,1.
\]

The new question is stricter:

> How efficiently can the nonlinear four-bit signature \(S_3\)-controller be embedded into this physical \(Q_4\) network?

The signature action has seven \(S\)-transpositions. Counted in both directions, they require at least 14 physical hops.

The \(R\)-action has five three-cycles. Since \(Q_4\) is bipartite, no triangle is a one-hop subgraph. The metric perimeter of each embedded three-cycle is at least four. Therefore

\[
\text{total work}\geq14+5\cdot4=34.
\]

An exhaustive componentwise placement census achieves this lower bound. Therefore

\[
\boxed{\text{minimum total work}=34}
\]

over all 32 directed state/opcode transitions, giving uniform average work

\[
\boxed{\frac{34}{32}=\frac{17}{16}\text{ knight hops per dispatch}.}
\]

The exact minimum dilation is

\[
\boxed{2}.
\]

There are

\[
\boxed{1{,}105{,}920}
\]

minimum-work labeled embeddings, forming 2,880 orbits after fixing translation and quotienting the 24 coordinate permutations.

All minimum-work embeddings require shortest-path link congestion at least three, and congestion three is attained:

\[
\boxed{\text{minimum congestion at minimum work}=3}.
\]

A deterministic RTL router compiles all 32 state/opcode transitions into one- or two-hop paths on the physical toroidal knight board.

---

## 3314 — bonkers construction B: the symmetry bit is a second toroidal board

The five-bit affine lift acts on

\[
Q_5=Q_4\square K_2.
\]

Thus the affine symmetry overhead has a literal network realization:

\[
\boxed{
Q_5=
\text{two }4\times4\text{ toroidal-knight boards joined by a 16-edge perfect matching}.
}
\]

For both \(S_3\) generators, the binary column-weight profile is

\[
\boxed{1,1,1,1,2}.
\]

Four basis directions remain one-hop routes. Only the added fifth symmetry direction maps to a two-hop diagonal.

This refines the earlier information law

\[
4\text{ information bits}+1\text{ symmetry bit}=5\text{ affine-equivariant bits}
\]

into a physical interconnect law:

\[
\boxed{
\text{one nonlinear }Q_4\text{ board}
\longrightarrow
\text{two linear }Q_4\text{ boards plus one matching layer}.
}
\]

---

## 3315 — the sign-dark guard shell

The ten unused words in \(\mathbb F_2^5\) form the invariant guard alphabet

\[
\Omega_{\rm guard}
\cong
1\sqcup3(S_3/C_2).
\]

Its character is

\[
\chi_{\rm guard}=(10,4,1),
\]

and

\[
\boxed{
\mathbb Q[\Omega_{\rm guard}]
\cong
4\mathbf1\oplus3V_{\rm std}.
}
\]

There is no sign constituent:

\[
\boxed{m_{\rm sgn}=0}.
\]

Every sign channel of the full 32-word register lies in the 22 valid envelope states. The guard shell is therefore **sign-dark**: reflection parity cannot hide exclusively in an invalid word.

The guard coherent algebra has rank

\[
\boxed{25}
\]

and orbital histogram

\[
1^1\,3^{15}\,6^9.
\]

Its Terwilliger dimensions are 25 from the fixed guard state and 58 from a three-state guard orbit.

As a \(Q_5\) induced network, the ten guards contain seven internal edges, 36 boundary edges, and components of sizes

\[
\boxed{7,1,1,1}.
\]

The three isolated guards are immediate one-hop-invalidity sentinels rather than a connected error-correcting code. The shell is useful for detection and typing, not fault-tolerant storage.

---

## Repo reconciliation

The packet reuses and rechecks the existing exact chain:

\[
4\times4\text{ toroidal knight}
\cong Q_4
\cong\text{four-bit Gray router}
\cong\text{Cl}_4\text{ Boolean lattice},
\]

with grade profile \(1+4+6+4+1\), and the antipodal quotient theorem

\[
Q_4/\{\pm\}\cong K_{4,4},
\qquad
\text{Gray support}=K_{4,4}-M\cong Q_3.
\]

The new results do not replace those theorems. They place the nonlinear signature action and five-bit affine lift onto the already-certified network.

---

## Reproduction

```bash
python analysis/bt3308_3319_knight_hypercube_gauge_closure.py \
  --json data/PART_BT3308_BT3319_KNIGHT_HYPERCUBE_GAUGE_CLOSURE_results.json \
  --gauge-json data/PART_BT3308_BT3319_C3_GAUGE_manifest.json

python -m pytest -q tests/test_bt3308_3319_knight_hypercube_gauge_closure.py
```

Expected line:

```text
PASS 18/18 exact knight-hypercube gauge-closure checks
```

---

## Evidence boundary

The following remain open:

- a checked ten-colour model or UNSAT proof;
- a globally preferred physical \(C_3\) gauge;
- an observed synthesis/placement result until the focused workflow completes;
- a fault-tolerant interpretation of the ten-word guard shell;
- a physical identification of finite orientation data with spacetime or laboratory curvature.

## External network-theory cross-check

The new controller theorem is repository-specific, but its language matches established interconnection-network practice:

- S. Latifi and S. Q. Zheng, “Determination of Hamiltonian cycles in cube-based networks using generalized Gray Codes,” *Computers & Electrical Engineering* 21 (1995), 189–199, DOI `10.1016/0045-7906(95)00001-B`.
- C. Li, S. Lin, and S. Li, “Hamiltonian Cycle Embeddings in Faulty Hypercubes Under the Forbidden Faulty Set Model,” *International Journal of Foundations of Computer Science*, DOI `10.1142/S0129054121500039`.
- J. Cai, M. Chen, and C. K. Lin, “Dimensional edge fault-tolerant Hamiltonicity of (folded) hypercubes,” *Discrete Applied Mathematics* 384 (2026), 154–164, DOI `10.1016/j.dam.2025.12.051`.

Those works support the use of Gray/Hamilton cycles, dilation, link faults, and routed embeddings as network metrics. They do not imply the W33 signature-controller results; the values \(34\), \(17/16\), \(2\), and \(3\) are exact computations of this packet.
