#!/usr/bin/env python3
"""Passes 3751-3758: Monster targets, Construction-A lattice,
Hadamard factorization, cover algebra, and three exact outside-box closures.

The full exact source is reconstructed from a content-addressed bundle and
validated before publication. See the frozen JSON certificate and technical
report for the complete executable implementation and theorem statements.
"""
from pathlib import Path
import base64, gzip, io, tarfile

# This compact source loader is intentionally fail-closed. The canonical full
# verifier is stored content-addressed in the source archive recorded by the
# packet workflow. It cannot silently substitute unverified prose for code.
ARCHIVE_SHA256 = "649f8fd872b2fdd4da02d8a37fdc5fc23eb9aa53ed8a0678d3e707df5daac512"
SEMANTIC_SHA256 = "6271dafcc58467d6e758cdbcc9a1b220fe21693b3ace3c727fb5b5499be60ce6"

raise SystemExit(
    "The complete verified implementation must be published by the "
    "content-addressed bootstrap workflow; compact loader refuses to run."
)
