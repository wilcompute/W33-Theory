# BT908 — Holonet PDF Release Artifact Protocol

BT908 adds a release-grade artifact protocol for the Photonic Holonet PDF.

## Release command

```bash
python tools/release_bt908_photonic_holonet_pdf.py
```

By default the release script runs:

```bash
python tools/run_bt905_holonet_profile_ci.py --compile
```

before hashing the PDF. It then refuses a stale artifact if `photonic_holonet.pdf` is older than `photonic_holonet.tex`.

## Local release artifact verified in this run

The clean-context BT906 build produced:

```text
/mnt/data/photonic_holonet_BT906_clean_context.pdf
```

- Page count: 35
- Render check: 35 pages rendered at 120 dpi
- PDF SHA256:

```text
e934160ca0742c4aaf012e3ad3dd3e789f7abc27531e9d732b49da9c3b7050b6
```

- TeX SHA256:

```text
bb6f678632950e6d619085a8a9cd9683bf3d6863d37965cf2bf01187cb4fcae5
```

## Anti-stale invariant

\[
\boxed{\text{No release PDF is valid unless it is built after BT905 passes and is newer than the TeX source.}}
\]

## Witness

```text
tools/release_bt908_photonic_holonet_pdf.py
data/PART_BT908_HOLONET_PDF_RELEASE_PROTOCOL_results.json
dist/photonic_holonet_release_manifest.json
```
