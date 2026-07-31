#!/usr/bin/env python3
from pathlib import Path
_SOURCE_DIR = Path(__file__).with_suffix('.src')
_SOURCE = ''.join(path.read_text() for path in sorted(_SOURCE_DIR.glob('part*.pyfrag')))
exec(compile(_SOURCE, str(Path(__file__)), 'exec'), globals(), globals())
