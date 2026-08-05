#!/usr/bin/env python3
"""Readable multipart loader for Passes 3542–3555."""
from pathlib import Path
HERE=Path(__file__).resolve().parent
parts=sorted(HERE.glob('bt3542_3555_radius_amplitude_code_fault_c5.py.part*'))
source=''.join(p.read_text(encoding='utf-8') for p in parts)
exec(compile(source,str(parts[0]),'exec'),globals(),globals())
