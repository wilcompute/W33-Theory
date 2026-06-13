# BT916 — Release CI Applies the Holonet Dictionary Row

BT916 extends the BT905/BT908 release path so the BT914 dictionary row is applied before compile/hash/release.

## Updated CI order

```text
BT903 root Holonet patch
BT914 profile dictionary row patch
BT901 profile-basis witness
BT904 constrained solver witness
BT902 cross-index witness
optional pdflatex twice
```

## Effect

Because BT908 and `make holonet-release` call

```bash
python tools/run_bt905_holonet_profile_ci.py --compile
```

they now inherit the BT914 dictionary patch automatically before the PDF is built and hashed.

## Guarded invariant

\[
\boxed{\text{No release PDF can be current unless it includes the Holonet profile dictionary row.}}
\]

## Witness

```text
tools/run_bt905_holonet_profile_ci.py
data/PART_BT916_RELEASE_CI_DICTIONARY_PATCH_results.json
```
