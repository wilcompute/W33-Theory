# BT909 — Human-facing Holonet Release Wrapper

BT909 makes the Photonic Holonet release path obvious for humans.

## Commands

```bash
make holonet-ci
```

runs the guarded Holonet profile CI with compile.

```bash
make holonet-release
```

runs the full BT908 release protocol through a small wrapper:

```text
tools/release_holonet.py
```

## Release chain

```text
make holonet-release
  -> tools/release_holonet.py
  -> tools/release_bt908_photonic_holonet_pdf.py
  -> tools/run_bt905_holonet_profile_ci.py --compile
```

## Guarded invariant

The release command does not just run `pdflatex`. It first runs the Holonet profile guard stack, then hashes the TeX/PDF outputs and rejects stale PDFs.

## Witness

```text
Makefile
tools/release_holonet.py
data/PART_BT909_HOLONET_RELEASE_WRAPPER_results.json
```
