# BT903 — Root Holonet Patch Runner

Target document:

```text
photonic_holonet.tex
```

BT903 makes the BT893--BT898 Holonet correction operational at the root-source level.

## What changed

Added a dedicated root patch runner:

```text
tools/apply_bt903_holonet_root_patch.py
```

It runs the idempotent BT899 integrator:

```text
tools/integrate_bt897_bt899_photonic_holonet_patch.py
```

then runs the static guard:

```text
analysis/bt899_photonic_holonet_static_guard.py
```

Optional compile path:

```bash
python tools/apply_bt903_holonet_root_patch.py --compile
```

## What it enforces

The root Holonet source must carry:

\[
Y_{g_H}[a,b]=1\Longleftrightarrow b\equiv-a-g_H\pmod3,
\]

plus the profile boundary:

\[
\boxed{\text{CKM/PMNS and mass hierarchy data live in }q^2=9\text{ within-grade profiles.}}
\]

## Honesty boundary

The connector pass adds the root-patch runner rather than silently claiming that the large root `photonic_holonet.tex` was overwritten. Running the BT903 command mutates the root source deterministically and guards the result.

## Witness

```text
tools/apply_bt903_holonet_root_patch.py
data/PART_BT903_HOLONET_ROOT_PATCH_results.json
```
