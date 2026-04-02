# Qiskit Local Workflow

This folder contains the durable local setup and experiment entrypoints for using
the Qiskit Code Assistant with a local Ollama backend from this machine.

## What Is Working

- VS Code extension: `qiskit.qiskit-vscode`
- Backend: Windows-side Ollama on `http://localhost:11434`
- Verified local model: `granite-3.3-8b-qiskit-gguf-cpu:latest`
- Linux-side Python runtime: `/home/wiljd/.venvs/qiskit-local`

## Why The Official Setup Fails Here

This machine is a WSL + Windows Ollama split setup.

- WSL `curl http://localhost:11434` does not see the Windows-side Ollama server.
- The official `setup_local.sh` model test uses `ollama run ... --verbose`, which
  is not the same path the VS Code extension uses.
- The default Qiskit `Qwen2.5-Coder 14B` model is too large for the available RAM
  on this machine and crashes the Ollama runner.

The durable path here is:

1. Use Windows Ollama.
2. Verify the actual OpenAI-compatible endpoint `/v1/completions`.
3. Use the smaller Qiskit-tuned Granite model.

## One-Time Manual VS Code Step

After running the setup script below, completely quit and reopen VS Code.

If only one local model is installed, the extension should auto-select it on
startup after the restart.

If you still want to set it manually, run:

`Qiskit Code Assistant: Select Model`

Then choose:

`granite-3.3-8b-qiskit-gguf-cpu:latest`

The extension does not currently expose a durable preseeded selected-model
setting, so this remains a one-time UI action.

If the extension still complains that your API token is invalid while you are
trying to use local Ollama, the extension is still on the IBM cloud path. This
repo now pins `qiskitCodeAssistant.url` at the workspace level and includes a
local-mode patcher for the installed extension so non-IBM URLs stay on the
OpenAI-compatible path instead of the IBM token path.

On this machine the CPU-safe Granite alias is the stable path:

`granite-3.3-8b-qiskit-gguf-cpu:latest`

## Local Auth / Token Error Fix

If model selection says your API token is invalid or unauthorized while you are
trying to use local Ollama, the extension has fallen into the IBM cloud path
instead of the local OpenAI-compatible path.

This repo now carries a local fix for that case:

```bash
python3 tools/qiskit/patch_installed_qiskit_extension_local_mode.py
```

That patch does three things:

- treats any non-IBM Qiskit URL as local OpenAI-compatible mode
- skips IBM credential startup prompts in local mode
- stops rewriting all local `401/403` responses as IBM token failures

The setup script below also runs that patch automatically.

Also note that this machine has both VS Code stable and VS Code Insiders in
use. The setup script now writes Qiskit settings to:

- Windows VS Code stable user settings
- Windows VS Code Insiders user settings
- this repo's workspace settings

## Local Setup

From the repo root:

```bash
bash tools/qiskit/local_setup_wsl_windows_ollama.sh
```

That script:

- starts Windows Ollama if needed
- installs or reuses the Qiskit Granite model
- writes the stable, Insiders, and workspace Qiskit extension settings
- patches installed Qiskit extensions so local URLs bypass IBM token flow
- verifies `/v1/models`
- verifies `/v1/completions`

## Helper Commands

These were also installed in `~/bin`:

```bash
qiskit-code-assistant-start
qiskit-code-assistant-smoke
qiskit-python -V
```

## Direct Local Delegate

If you want me to use the local Qiskit model as an auxiliary coding assistant,
the repo now includes a direct Ollama caller:

```bash
python3 tools/qiskit/qiskit_local_codegen.py \
  --prompt "Write a Qiskit 2.0 function that builds a Bell pair circuit."
```

This does not turn the model into a native Codex `spawn_agent` target, but it
does let me delegate bounded Qiskit coding subtasks to the same local model the
extension uses, inspect the result, and continue the loop inside the repo.

If only one local model is exposed from `/v1/models`, the helper auto-selects
it. Otherwise pass `--model`.

List live models:

```bash
python3 tools/qiskit/qiskit_local_codegen.py --list-models
```

On this machine, model discovery through `/v1/models` is reliable, but direct
CLI completions through `/v1/completions` can still time out under the WSL ->
Windows Ollama split. So the CLI helper is useful as a bounded auxiliary path,
but the simulator-side Qiskit workflow should not depend on it being fast on
every call.

## Permutation Search Workflow

The reusable Qiskit experiment driver is:

```bash
qiskit-python tools/qiskit/permutation_grover_search.py \
  --items A B C \
  --mark A,B,C \
  --shots 512
```

Example with two marked permutations:

```bash
qiskit-python tools/qiskit/permutation_grover_search.py \
  --items 0 1 2 3 \
  --mark 0,1,2,3 \
  --mark 3,2,1,0 \
  --shots 1024 \
  --top 8
```

The script outputs JSON with:

- encoded search size
- number of qubits
- Grover iterations used
- marked permutations
- top measured hits
- decoded valid and invalid bitstrings

## Batch Sweep

Run a sweep across multiple sizes and iteration offsets:

```bash
qiskit-python tools/qiskit/permutation_grover_batch.py \
  --min-size 3 \
  --max-size 5 \
  --mark-mode identity-reverse \
  --iteration-offsets -1 0 1 \
  --shots 512 \
  --output /tmp/qiskit_batch.json
```

Then summarize it:

```bash
qiskit-python tools/qiskit/analyze_permutation_runs.py /tmp/qiskit_batch.json
```

## Upstream Patch

I also included a concrete patch draft for the Qiskit setup flow:

`tools/qiskit/qiskit_code_assistant_wsl_windows_ollama.patch`

It fixes three things:

- WSL + Windows Ollama readiness checks
- model verification through `/v1/completions`
- smaller default model selection on low-memory machines

## Tight Loop

The intended loop is:

1. Use Qiskit Code Assistant in VS Code to edit or extend the experiment.
2. Run the script with `qiskit-python`.
3. Inspect the JSON output.
4. Revise the circuit or scoring logic.
5. Repeat.

## First TOE Search Target

The first TOE-specific Qiskit search in this repo is:

```bash
qiskit-python tools/qiskit/toe_support_hierarchy_search.py --shots 512
```

That search does not guess new physics. It encodes the exact bridge support
hierarchy already proved in the repo:

- `2E13` image channel lives on the head-compatible line
- first family-sensitive `A4` packet has minimal carrier `U1`
- transport completion lives on the full avatar
- the local `U3` and `E8_2` packets remain unconstrained in relative order

So the oracle marks exactly the support permutations whose first three slots are:

- `head_line`
- `u1_plane`
- `transport_avatar`

The next exact refinement of that same `120`-state shell is:

```bash
qiskit-python tools/qiskit/toe_support_diagnostic_search.py --shots 256 --seed 7
```

That oracle does not change the support state count. It factorizes the same
support shell exactly as:

- `10` support interleavings choosing which `3` of `5` slots carry the bridge core
- `6` orders on `(head_line, u1_plane, transport_avatar)`
- `2` free local-context orders on `(u3_local, e8_2_local)`

So the exact identity is `5! = C(5,3) * 3! * 2! = 10 * 6 * 2`, and the marked
sector keeps one support interleaving and one line/plane/avatar core order,
with the local tail order still free. A two-seed study over seeds `7,8` shows
the cleanest operating point is `6` iterations, with mean target-hit
probability `0.99609375`.

The next exact support-side refinement is:

```bash
qiskit-python tools/qiskit/toe_support_diagnostic_relaxation_search.py \
  --relaxation exact \
  --shots 256 \
  --seed 7
```

That keeps the same factorized `120`-state shell fixed and relaxes the two
support theorems one sector at a time:

- `exact`: marked count `2`
- `interleaving-relaxed`: marked count `20`
- `core-order-relaxed`: marked count `12`
- `both-relaxed`: marked count `120`

The clean operating points over seeds `7,8` are:

- `exact`: `6` iterations, mean target-hit `0.99609375`
- `interleaving-relaxed`: `1` iteration, mean target-hit `0.88671875`
- `core-order-relaxed`: `2` iterations, mean target-hit `1.0`
- `both-relaxed`: `0` iterations, mean target-hit `0.939453125`

So this is not only a count theorem. It shows where Grover amplification stops
helping once the relaxed marked sector becomes too large relative to the padded
shell.

The next exact support-side refinement is:

```bash
qiskit-python tools/qiskit/toe_support_enhancement_relaxation_search.py \
  --mode formal-completion-avatar \
  --relaxation exact \
  --shots 256 \
  --seed 7
```

This tensors that same factorized support-relaxation shell with the exact
three-state external enhancement hierarchy:

- `current_k3_zero_orbit`
- `minimal_external_enhancement`
- `formal_completion_avatar`

So the exact discrete space is `360 = 120 * 3`, padded to `9` qubits. The
marked sector factorizes exactly as

`Marked(relaxation, mode) = Marked_support(relaxation) * {enhancement(mode)}`

so the three enhancement modes are basis-conjugate to one another and the
support-side marked-count profile stays exactly:

- `exact`: `2`
- `interleaving-relaxed`: `20`
- `core-order-relaxed`: `12`
- `both-relaxed`: `120`

A representative two-seed study over seeds `7,8` on the
`formal_completion_avatar` mode gives the clean operating points:

- `exact`: `12` iterations, mean target-hit `1.0`
- `interleaving-relaxed`: `3` iterations, mean target-hit `0.970703125`
- `core-order-relaxed`: `5` iterations, mean target-hit `0.982421875`
- `both-relaxed`: `1` iteration, mean target-hit `0.994140625`

So the enhancement hierarchy does not change the support-selectivity geometry,
but the larger `360 -> 512` padded shell shifts the clean Grover windows.
Most sharply, the fully relaxed sector moves from a `0`-step optimum on the
bare-support `120`-state family to a `1`-step optimum on the enlarged shell.

The next bounded exact side result is:

```bash
qiskit-python tools/qiskit/toe_double_interleaving_shadow_search.py \
  --relaxation exact \
  --shots 256 \
  --seed 7
```

This isolates the two exact `10`-state interleaving layers already present in
the bridge:

- the support-core interleavings
- the hyperbolic-factor interleavings

Both are exact copies of `J(5,3)`, so the joint interleaving shadow has size
`100 = 10 * 10`. The current bridge is asymmetric there: the support theorem
freezes one support interleaving, while the factor copy remains free. A
two-seed study over seeds `7,8` shows the exact mode is cleanest at `2`
iterations with mean target-hit probability `0.97265625`. If the support
interleaving theorem is relaxed too, the marked count jumps to `100` and the
padded-shell optimum collapses to the uniform state at `0` iterations.

The next exact search layer is:

```bash
qiskit-python tools/qiskit/toe_bridge_product_search.py \
  --mode formal-completion \
  --shots 256 \
  --seed 7
```

That product-state oracle combines three exact theorem sectors on one search
space:

- strict support hierarchy
- five-factor packet ordering
- glue state: current zero split shadow vs unique nonzero formal completion

The next refinement is:

```bash
qiskit-python tools/qiskit/toe_bridge_line_factor_search.py \
  --mode formal-completion \
  --shots 256 \
  --seed 7
```

That line-factor oracle adds the exact `U1` line choice:

- `head_compatible_u1_line`
- `tail_biased_u1_line`

and keeps only the theorem-compatible head line in the marked sector. The
explicit product space has size `57600`, padded to `16` qubits. On the seeded
verification runs (`seed = 7`, `256` shots), both `current-shadow` and
`formal-completion` modes hit only marked states with target-hit probability
`1.0`. A two-seed study over seeds `7,8` shows the `16`-qubit oracle is
cleanest at `44` iterations rather than `45`.

The next exact filter is:

```bash
qiskit-python tools/qiskit/toe_bridge_weight_filter_search.py \
  --mode formal-completion \
  --shots 256 \
  --seed 7
```

That adds one theorem-backed concentration bit:

- `dominant_weight_filter_pass`
- `dominant_weight_filter_fail`

with `pass` meaning the exact current inequalities:

- `U3` carries more than `4/5` of the hyperbolic packet
- `E8_2` carries more than `8/9` of the exceptional packet

The explicit product space has size `115200`, padded to `17` qubits. On the
seeded verification runs (`seed = 7`, `256` shots), both `current-shadow` and
`formal-completion` modes hit only marked states with target-hit probability
`1.0`. A two-seed study over seeds `7,8` shows the `17`-qubit oracle is
cleanest at `63` iterations rather than `64`.

The next exact refinement is:

```bash
qiskit-python tools/qiskit/toe_bridge_split_weight_filter_search.py \
  --mode formal-completion \
  --shots 256 \
  --seed 7
```

That splits the concentration theorem into two independent exact factors:

- `hyperbolic_dominance_pass` / `hyperbolic_dominance_fail`
- `exceptional_dominance_pass` / `exceptional_dominance_fail`

The marked sector keeps only the exact `pass/pass` state, so Qiskit can now
distinguish "hyperbolic only" and "exceptional only" filter failures instead
of collapsing everything to one joint fail bit. The explicit product space has
size `230400`, padded to `18` qubits. On the seeded verification runs
(`seed = 7`, `256` shots), both `current-shadow` and `formal-completion` modes
hit only marked states with target-hit probability `1.0`. A local
formal-completion probe at `89`, `90`, and `91` iterations stayed on the same
`1.0` plateau for seed `7`.

The next diagnostic refinement is:

```bash
qiskit-python tools/qiskit/toe_bridge_diagnostic_order_search.py \
  --mode formal-completion \
  --shots 256 \
  --seed 7
```

That keeps the same factor-state cardinality but factorizes the five-factor
ordering exactly as:

- hyperbolic order on `U1/U2/U3`
- exceptional order on `E8_1/E8_2`
- interleaving pattern choosing the `3` hyperbolic slots among `5`

with `5! = C(5,3) * 3! * 2! = 10 * 6 * 2`. So the oracle becomes diagnostic by
theorem sector without changing the underlying `120`-state factor space. The
full product space is again `230400`, padded to `18` qubits. On the seeded
verification runs (`seed = 7`, `256` shots), both `current-shadow` and
`formal-completion` modes hit only marked states with target-hit probability
`1.0`.

For heavier bridge oracles, use the reusable study runner:

```bash
qiskit-python tools/qiskit/toe_bridge_oracle_iteration_study.py \
  --target product \
  --iterations 31 32 33 \
  --seeds 7 8 \
  --shots 256 \
  --top 6
```

The first product study shows the `15`-qubit formal-completion oracle is
cleanest at `31` iterations on seeds `7,8`.

The next exact diagnostic layer is
[toe_bridge_diagnostic_relaxation_search.py](tools/qiskit/toe_bridge_diagnostic_relaxation_search.py).
It keeps the accepted pass/pass concentration channel fixed and relaxes the two
order theorems one sector at a time, while the interleaving sector stays free
just as it already does in the diagnostic-order oracle. The corrected exact
state space is `57600` states, padded to `16` qubits, with marked counts
`20 / 40 / 120 / 240` for:

- `exact`
- `exceptional-order-relaxed`
- `hyperbolic-order-relaxed`
- `both-orders-relaxed`

On a representative two-seed study over seeds `7,8` on the
`formal-completion` mode, the clean operating points are:

- `45` iterations for `exact` with mean target-hit probability `0.998046875`
- `32` iterations for `exceptional-order-relaxed` with mean target-hit probability `0.998046875`
- `18` iterations for `hyperbolic-order-relaxed` with mean target-hit probability `1.0`
- `13` iterations for `both-orders-relaxed` with mean target-hit probability `0.99609375`

So the theorem-facing selectivity is explicit rather than buried in one
combined permutation rule: the exceptional order contributes the exact binary
factor, the hyperbolic order contributes the exact 6-fold factor, and the
interleaving sector is already free in the diagnostic-order oracle.

The next exact refinement is:

```bash
qiskit-python tools/qiskit/toe_bridge_diagnostic_enhancement_relaxation_search.py \
  --mode formal-completion-avatar \
  --relaxation exact \
  --shots 256 \
  --seed 7
```

This tensors that corrected diagnostic-relaxation shell with the exact
three-state enhancement hierarchy:

- `current_k3_zero_orbit`
- `minimal_external_enhancement`
- `formal_completion_avatar`

So the exact discrete space is `86400 = 57600 * 3`, padded to `17` qubits. The
marked sector factorizes exactly as

`Marked(relaxation, mode) = Marked_diagnostic_relaxation(relaxation) * {enhancement(mode)}`

so the three enhancement modes are basis-conjugate and the
order-relaxation marked-count profile stays exactly:

- `exact`: `20`
- `exceptional-order-relaxed`: `40`
- `hyperbolic-order-relaxed`: `120`
- `both-orders-relaxed`: `240`

A representative two-seed study over seeds `7,8` on the
`formal_completion_avatar` mode gives the clean operating points:

- `exact`: `64` iterations, mean target-hit `0.998046875`
- `exceptional-order-relaxed`: `45` iterations, mean target-hit `0.998046875`
- `hyperbolic-order-relaxed`: `26` iterations, mean target-hit `0.998046875`
- `both-orders-relaxed`: `18` iterations, mean target-hit `1.0`

So the enhancement hierarchy now sits exactly above both lower discrete
geometries: it preserves the order-selectivity profile just as it preserved the
support-selectivity profile, while shifting the padded-shell Grover windows
from `57600 -> 65536` to `86400 -> 131072`.

The next exact bridge wall is:

```bash
qiskit-python tools/qiskit/toe_bridge_enhancement_factor_search.py \
  --mode formal-completion-avatar \
  --shots 256 \
  --seed 7
```

This refines the old glue dichotomy into the exact three-state external
enhancement hierarchy:

- `current_k3_zero_orbit`
- `minimal_external_enhancement`
- `formal_completion_avatar`

So the oracle now distinguishes the current refined K3 object, the minimal
exact new datum needed for nonzero completion, and the resulting formal
completion object. The exact search space has size `345600`, padded to `19`
qubits, with marked count `20` in each mode. On seeded verification runs
(`seed = 7`, `256` shots), all three modes hit only marked states with
target-hit probability `1.0` at `127` iterations.

The sharper enhancement/slot refinement is:

```bash
qiskit-python tools/qiskit/toe_bridge_diagnostic_enhancement_slot_search.py \
  --mode formal-completion-avatar \
  --relaxation exact \
  --iterations 90 \
  --shots 256 \
  --seed 7
```

This keeps the corrected diagnostic enhancement shell and adjoins the exact
two-state cocycle-slot wall itself:

- `zero_by_splitness`
- `unique_nonzero_orbit_in_existing_slot`

The compatibility law is exact:

- `current_k3_zero_orbit -> zero_by_splitness`
- `minimal_external_enhancement -> unique_nonzero_orbit_in_existing_slot`
- `formal_completion_avatar -> unique_nonzero_orbit_in_existing_slot`

So the three-state enhancement hierarchy strictly refines the binary slot wall
rather than duplicating it. The exact shell is `172800 = 86400·2`, padded to
`18` qubits. The marked-count profile stays `20 / 40 / 120 / 240`, but the
marked pair projection becomes a singleton in each mode. Seeded exact checks at
`256` shots and `90` iterations returned `1.0` in all three exact modes:

- `current-k3-zero-orbit -> (current_k3_zero_orbit, zero_by_splitness)`
- `minimal-external-enhancement -> (minimal_external_enhancement, unique_nonzero_orbit_in_existing_slot)`
- `formal-completion-avatar -> (formal_completion_avatar, unique_nonzero_orbit_in_existing_slot)`

The stronger replacement for that free three-label axis is:

```bash
qiskit-python tools/qiskit/toe_bridge_cocycle_compatibility_search.py \
  --focus nonzero-compatible \
  --iterations 90 \
  --shots 256 \
  --seed 7
```

This resolves the wall as an exact compatibility theorem on a `6`-state factor

`wall_layer x orbit_state`

with wall layers

- `current_refined_k3_object`
- `slot_replacement_datum`
- `formal_completion_object`

and orbit states

- `zero_orbit`
- `unique_nonzero_orbit`

Only `3` wall states are admissible, and only `2` of those are nonzero:

- `current_refined_k3_object x zero_orbit`
- `slot_replacement_datum x unique_nonzero_orbit`
- `formal_completion_object x unique_nonzero_orbit`

So the wall is no longer just a relabeled three-mode family. It is a
compatibility factor with forbidden corners. Tensoring that factor with the
corrected diagnostic shell gives the exact `345600`-state `19`-qubit search.
Seeded exact checks at `256` shots now give:

- `all-compatible`: `60` marked states, `74` iterations, target-hit `1.0`
- `nonzero-compatible`: `40` marked states, `90` iterations, target-hit `1.0`

The sharper support-side projection of that same wall is:

```bash
qiskit-python tools/qiskit/toe_support_cocycle_compatibility_relaxation_search.py \
  --focus nonzero-compatible \
  --relaxation exact \
  --iterations 13 \
  --shots 256 \
  --seed 7
```

This tensors the factorized `120`-state support-relaxation shell directly with
the exact `6`-state cocycle wall, giving the exact `720`-state `10`-qubit
search. The factorization is still exact:

`Marked_support(relaxation) x Compatible_wall(focus)`.

On the live nonzero wall the marked-count profile is:

- `exact`: `4`
- `interleaving-relaxed`: `40`
- `core-order-relaxed`: `24`
- `both-relaxed`: `240`

So the live nonzero wall multiplies the old support-relaxation profile by the
precise factor `2`. Seeded nonzero-wall checks at `256` shots now give:

- `exact`: `13` iterations, target-hit `0.97265625`
- `interleaving-relaxed`: `4` iterations, target-hit `0.953125`
- `core-order-relaxed`: `5` iterations, target-hit `0.96875`
- `both-relaxed`: `1` iteration, target-hit `1.0`

The next exact lift is:

```bash
qiskit-python tools/qiskit/toe_bridge_cocycle_compatibility_relaxation_search.py \
  --focus nonzero-compatible \
  --relaxation exact \
  --iterations 90 \
  --shots 256 \
  --seed 7
```

This tensors the corrected diagnostic-relaxation shell directly with the exact
`6`-state cocycle wall, so the shell is again `345600 = 57600·6`, padded to
`19` qubits. The factorization is still exact:

`Marked_diagnostic_relaxation(relaxation) x Compatible_wall(focus)`.

On the live nonzero wall, the marked-count profile becomes:

- `exact`: `40`
- `exceptional-order-relaxed`: `80`
- `hyperbolic-order-relaxed`: `240`
- `both-orders-relaxed`: `480`

Seeded nonzero-wall checks at `256` shots now give:

- `exact`: `90` iterations, target-hit `1.0`
- `exceptional-order-relaxed`: `64` iterations, target-hit `1.0`
- `hyperbolic-order-relaxed`: `37` iterations, target-hit `1.0`
- `both-orders-relaxed`: `26` iterations, target-hit `1.0`

The next exact refinement is the enhancement-slot hierarchy:

```bash
qiskit-python tools/qiskit/toe_bridge_diagnostic_enhancement_slot_search.py \
  --mode formal-completion-avatar \
  --relaxation both-orders-relaxed \
  --iterations 26 \
  --shots 256 \
  --seed 7
```

The exact compatibility law is:

- `current_k3_zero_orbit -> zero_by_splitness`
- `minimal_external_enhancement -> unique_nonzero_orbit_in_existing_slot`
- `formal_completion_avatar -> unique_nonzero_orbit_in_existing_slot`

So the three-state enhancement hierarchy strictly refines the older two-state
slot wall. The current K3 state is separated from both completion-side states
by slot status, while the minimal and formal completion states share the same
nonzero slot but not the same support role.

The Qiskit shell for that theorem is `172800 = 86400·2`, padded to `18`
qubits. The marked-count profile stays the same as the diagnostic-enhancement
family inside each mode, but the marked pair itself is now exact. Seeded
`both-orders-relaxed` checks at `256` shots came back exact at `26`
iterations:

- `current-k3-zero-orbit`: `1.0`, marked pair `['current_k3_zero_orbit', 'zero_by_splitness']`
- `minimal-external-enhancement`: `1.0`, marked pair `['minimal_external_enhancement', 'unique_nonzero_orbit_in_existing_slot']`
- `formal-completion-avatar`: `1.0`, marked pair `['formal_completion_avatar', 'unique_nonzero_orbit_in_existing_slot']`

The next exact refinement isolates the shared nonzero-slot lift:

```bash
qiskit-python tools/qiskit/toe_bridge_completion_datum_avatar_lift_search.py \
  --mode formal-completion-object \
  --relaxation exact \
  --iterations 63 \
  --shots 256 \
  --seed 7
```

Inside the shared nonzero slot, the exact lift states are:

- `slot_replacement_datum`
- `formal_completion_object`

They already share the same nonzero orbit and the same completion normal form,
so the live distinction is role: datum-only versus minimal common external
object. The shared-nonzero-wall oracle tensors that binary lift factor with the
corrected diagnostic-relaxation shell, so the exact state count is
`115200 = 57600·2`, padded to `17` qubits. The marked-count profile stays
`20 / 40 / 120 / 240`, with exact mode relation
`Marked_diagnostic_relaxation(relaxation) x {lift_state(mode)}`. Seeded exact
checks at `256` shots came back clean in both modes, and a two-seed
`63/64/65` probe on the formal completion side is now cleanest at `63`
iterations with mean target-hit probability `1.0`:

- `slot-replacement-datum`: `1.0` at `64` on seed `7`
- `formal-completion-object`: `1.0` at `64` on seed `7`
- `formal-completion-object`: mean `1.0` at `63` on seeds `7,8`

The current promoted bridge-oracle stack is summarized in
[bridge_oracle_ledger.json](tools/qiskit/bridge_oracle_ledger.json).
For a GitHub-readable surface, use
[ORACLE_LEDGER.md](tools/qiskit/ORACLE_LEDGER.md).

## Stronger TOE Search Target

The next exact search target is the five-factor external packet hierarchy:

```bash
qiskit-python tools/qiskit/toe_bridge_permutation_search.py \
  --mode five-factor-hierarchy \
  --shots 512
```

That oracle marks exactly the permutations compatible with the current exact
bridge inequalities:

- `U3 > U1 > U2`
- `E8_2 > E8_1`

So this search is not inventing new physics. It is searching the theorem-
compatible ordering sector of the already-rigid `U1/U2/U3/E8_1/E8_2` packet.
