"""Compatibility shim for the superseded colliding 9029–9040 filename.

Canonical implementation: analysis/w33_pass9173_9184_root_shadow_trichotomy.py
The 9013–9092 reservation landed first, so this old pass label no longer claims namespace ownership.
"""
from w33_pass9173_9184_root_shadow_trichotomy import *  # noqa: F401,F403

if __name__ == "__main__":
    raise SystemExit(main())
