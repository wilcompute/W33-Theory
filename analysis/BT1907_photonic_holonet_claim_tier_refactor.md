# BT1907 — Photonic Holonet Claim-Tier Refactor

This refactor separates the full Holonet manuscript into public claim tiers.  The goal is not to reduce ambition; it is to make the exact machine harder to dismiss by keeping theorem, simulation, physical protocol, physics identification, and frontier application language distinct.

## Five claim tiers

| Tier | Meaning | Required evidence |
|---|---|---|
| E | Exact finite theorem or exhaustive computation | Witness script, proof, table, or audit row recomputes the claim from repo data. |
| S | Simulation or finite model measurement | Seeded run, model assumptions, output JSON, and error bars or pass/fail condition. |
| P | Physical demonstrator pending or completed | Apparatus protocol, raw-shot schema, estimator, pass/fail statistic, and data. |
| C | Corpus identification / postdiction / arithmetic match | Explicit statement that the value is matched or identified, not dynamically derived. |
| F | Frontier conjecture or application | Roadmap language only; no theorem wording until reduced to E/S/P/C. |

## Refactored paper stack

1. **Machine paper** (`holonet_machine.tex`, mostly E/S): processor, network, memory, CLI, audit, benchmark, contextuality fuel, and honest boundaries.
2. **Demonstrator protocol** (`holonet_demonstrator_protocol_v1.tex`, P with E prerequisites): one physical test, the contextual fraction `1/10`.
3. **Public theorem ledger** (`docs/holonet_theorem_ledger.md`): claim-to-witness map and audit contract.
4. **Grand physics paper** (`photonic_holonet.tex`, E+S+P+C+F): ambitious synthesis, but every claim tiered.
5. **Practical implications paper** (`holonet_practical_implications.tex`, mostly F with E/S inputs): infrastructure, data centers, quantum internet, DNA storage, autopoietic networks, consensus, and AI.

## Grand-paper section map

| Manuscript region | Tier | Public wording | Action |
|---|---:|---|---|
| Substrate `W(3,3)`, SRG parameters, lines/flags | E | Exact finite geometry. | Keep in machine paper and grand paper. |
| Witting rays and two-qutrit Pauli classes | E/C | Exact where witnesses construct the graphs; physical carrier identification remains architecture. | Cite witnesses and mark carrier assumptions. |
| Group distinctions `Sp(4,3)`, `PSp(4,3)`, `W(E6)` | E | Exact group-order and action statements, with double-cover warning. | Keep prominent. |
| Routing atlas, hypercube charts, Tits apartments, mirror bus | E | Verified finite incidence/routing architecture. | Keep as machine core. |
| Steinberg memory and `[[66,8,3]]_3` protection | E/S | Exact representation/code claims where witnessed; threshold behavior simulated. | Split theorem from threshold model. |
| Runnable VM, teleportation, QEC, quine, consensus | E/S | Executable software demonstrations; simulations clearly labelled. | Keep in machine paper. |
| Contextual fraction `1/10` | E/P | Exact finite budget and first physical falsifier. | Promote to demonstrator protocol. |
| Parity law: `CF=0` (even `q`) / `1/(q^2+1)` (odd `q`), scan `q=2,3,4` incl GF(4) | E | Exact: contextual iff `q` odd; `q=4` even composite proves parity, not primality. | Witness `analysis/w33_audit_qscan.py`; ledger row. |
| Explicit even-`q` ovoid (noncontextual control model) | E | Exact construction of the `W(2)` 5-ray / `W(4)` 17-ray ovoid giving `CF=0`. | Witness `analysis/w33_ovoid_construct.py`; control model for the demonstrator. |
| Two-arm contextuality discriminator | E/P | Same estimator returns `1/10` (odd) vs `0` (even); the physical control arm is pending. | `analysis/holonet_control_arm.py` runs `bt1901`/`bt1904` on both arms; `holonet_parity_control.tex`. |
| Sign vs selection contextuality on `W(2)`; realization dimension bound | E | The even fabric stays Mermin sign-contextual while selection-noncontextual; `W(2)` has no complete-basis realization in `C^3`, so `q=3` is the smallest realizable and smallest contextual order. | `analysis/w33_doily_mermin.py` (exact `F_2` obstruction, 6-line certificate); `analysis/w33_realization_dimension.py` (counting theorem, verified inputs). |
| Contextuality tax: the KS defect is one movable point-star | E | Exhaustive enumeration: exactly 40 optimal failure sets, each the star of one point, all centers realized; deficit `q+1` (odd) / 0 (even); the OS escalation budget = the `9^t` spend = one star = `1/10` of contexts. | `analysis/w33_contextuality_tax.py`; structurally underwrites the scheduler arc's `36 spreads / movable point-star defect` bridge (no assignment-to-spread bijection claimed). |
| Table-free routing scaling win | E | Routing state `~n^2 log n` diverges while the Holonet stays `0` bytes / `2` hops at every order. | `holonet bench --compare --scale`. |
| Magic robustness `R=3` and `9^t` dial | E/S | Exact robustness plus simulated small-`t` cost. | Keep as quantum-resource knob. |
| Photonic apparatus: PBS, tritter, EOM, OAM/time bins | P | Concrete experiment plan, not a completed build. | Move into demonstrator protocol. |
| Data-center, virtualization, consensus-without-mining, DNA storage | F | Applications suggested by exact substrate properties. | Keep in implications paper; avoid theorem wording. |
| `q=3` selection, cyclotomic skeleton, exceptional tower | C/E | Arithmetic ledger exact; physics identification is corpus-level. | Label every physics role as identification unless derived dynamically. |
| Standard Model descent, generations, weak angle, masses | C | Postdicted/matched integer architecture unless a dynamical derivation is present. | Put in physics tier with explicit boundaries. |
| K3, spectral action, gravity, propinquity convergence | C/F | Strong candidate bridge with named open theorems. | Keep as frontier; name T1/T2 gaps. |
| Cosmology, neutrino, dark matter, proton decay predictions | C/P/F | Dated falsifiers where numerical predictions exist; derivation status varies. | Move to physics scorecard. |

## Rewrite rules for `photonic_holonet.tex`

1. Every theorem statement must be E-tier or explicitly say which witness proves it.
2. Every Monte Carlo or model-based result must carry S-tier language: simulated, measured in model, seeded, assumptions.
3. Every physical statement must distinguish protocol, simulation, and completed experiment.
4. Every Standard-Model/cosmology match must say whether it is derived, matched, input, or open.
5. No infrastructure application may inherit theorem status merely because it is inspired by an E-tier substrate fact.
6. The first physical milestone remains the contextual-fraction demonstrator.

## Public-facing abstract template

> We present a finite, executable architecture on the symplectic generalized quadrangle `W(3,3)` in which routing, Clifford control, and memory protection are one incidence-geometric operation.  The classical layer is runnable today and self-auditing: `holonet audit` re-derives the headline constants from `q=3`, while `holonet bench` separates deterministic op counts from host-relative throughput.  The first physical falsifier is a single-photon contextuality test predicting the exact fraction `1/10`.  A broader physics program identifies the same integer ledger with exceptional structures and Standard-Model/cosmological quantities; those identifications are claim-tiered separately from the executable machine.

## Immediate integration targets

- Add a short claim-tier legend near the beginning of `photonic_holonet.tex`.
- Make every appendix/passage ending in a physics claim include one of: **derived**, **matched**, **input**, **open**.
- Keep `holonet_machine.tex` free of cosmological claims except for a pointer to the physics program.
- Use `docs/holonet_theorem_ledger.md` as the public table for reviewers.

## Bottom line

The project should lead with the machine: exact, executable, auditable, and falsifiable by a cheap contextuality experiment.  The physics program remains the grand synthesis, but its credibility improves when every claim carries its tier.
