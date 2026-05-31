#!/usr/bin/env python3
"""Compatibility wrapper for the fixed Singer hexagon affine-completion verifier.

The initial version of this file accidentally imported a non-exported helper.
The runnable implementation now lives in:

    analysis/w33_singer_hexagon_affine_completion_canonicality_fixed.py

This wrapper keeps the historical filename usable by delegating to the fixed
module.
"""
from __future__ import annotations

from analysis.w33_singer_hexagon_affine_completion_canonicality_fixed import build_payload, main


if __name__ == "__main__":
    main()
