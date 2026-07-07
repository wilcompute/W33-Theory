# BT1835 — Raw Uploaded Artifact Import

`analysis/bt1835_raw_artifact_importer.py` imports the uploaded JSON artifacts into this directory when run in an environment where the upload directory is mounted.

Default command:

```bash
python analysis/bt1835_raw_artifact_importer.py --src /mnt/data --dst data/imported_runtime_artifacts/raw
```

By default the nine JSON artifacts are copied. The large `w33_defect_walk_trace.jsonl` trace is represented by SHA-256 and line count in `data/imported_runtime_artifacts/BT1833_uploaded_artifact_manifest.json`; pass `--include-trace` to copy it too.

Honest boundary: this README and importer are committed now. The byte-for-byte raw payloads are materialized by running the importer in the repo environment that has the upload files.
