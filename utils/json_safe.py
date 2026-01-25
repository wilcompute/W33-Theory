from __future__ import annotations
from pathlib import Path
import json
from typing import Any, IO

try:
    import numpy as np
except Exception:
    np = None


def _default(o: Any):
    """Default JSON serializer fallback.
    Tries to convert to int, float, list, or str. Handles numpy types if available.
    """
    # numpy types
    if np is not None:
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()

    # Generic numeric-like
    try:
        return int(o)
    except Exception:
        pass
    try:
        return float(o)
    except Exception:
        pass
    # Fall back to string
    return str(o)


def dump_json(obj: Any, fp_or_path: str | Path | IO[str], **kwargs) -> None:
    """Write JSON to a file path or file-like object with safe default serializer.

    Usage:
      dump_json(obj, 'out.json', indent=2, sort_keys=True)
      with open('out.json', 'w') as f: dump_json(obj, f, indent=2)
    """
    if isinstance(fp_or_path, (str, Path)):
        path = Path(fp_or_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w', encoding=kwargs.pop('encoding', 'utf-8')) as f:
            json.dump(obj, f, default=_default, **kwargs)
    else:
        json.dump(obj, fp_or_path, default=_default, **kwargs)


def load_json(fp_or_path: str | Path | IO[str]):
    if isinstance(fp_or_path, (str, Path)):
        with open(fp_or_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return json.load(fp_or_path)
