#!/usr/bin/env python3
"""Renamespace-preserving loader for Passes 3556–3569.

The audited source bytes are stored under bootstrap/pass3556_3569 as the
superseded 3542–3555 build.  This loader applies only deterministic namespace
substitutions before execution; the mathematics is otherwise byte-for-byte the
validated packet.
"""
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]
parts=sorted((HERE/'bootstrap/pass3556_3569').glob('verifier.legacy.part*.py'))
assert len(parts)==4, f'expected four legacy source parts, found {len(parts)}'
source=''.join(p.read_text(encoding='utf-8') for p in parts)
for old,new in (
    ('3542-3555','3556-3569'),
    ('3542_3555','3556_3569'),
    ('BT3542_BT3555','BT3556_BT3569'),
    ('pass3542_3555','pass3556_3569'),
):
    source=source.replace(old,new)
exec(compile(source,str(parts[0]),'exec'),globals(),globals())
