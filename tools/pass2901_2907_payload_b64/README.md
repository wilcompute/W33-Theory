# Passes 2901–2907 release carrier

These base64/LZMA shards are consumed by `tools/materialize_bt2901_bt2907.py`. The materializer verifies the SHA-256 digest of every emitted readable artifact and refuses to overwrite divergent files. The carrier exists only to publish the multi-file research packet atomically through the connector; canonical source files are materialized and committed by the dedicated workflow.
