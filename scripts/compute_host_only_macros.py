#!/usr/bin/env python3
r"""Compute the COMPLETE host-only macro list instead of extending one reactively.

Three Holonet build breaks came from a hand-written HOST_ONLY list being
incomplete exactly where the next insert was written. The set is finite and
computable: diff the macro/environment definitions of the two manuscript bodies.
"""
import json
import re
from pathlib import Path

ROOT = Path(r"c:\Repos\Theory of Everything")
RE_DEF = re.compile(r"\\(?:new|provide|renew)command\s*\{?\\(\w+)\}?")
RE_THM = re.compile(r"\\newtheorem\s*\{(\w+)\}")


def defs(name):
    t = (ROOT / name).read_text(encoding="utf-8", errors="ignore")
    return set(RE_DEF.findall(t)) | set(RE_THM.findall(t))


w = defs("w33_paper_body.tex")
h = defs("photonic_holonet_body.tex")
only_w = sorted(w - h)
only_h = sorted(h - w)

print(f"w33_paper_body defines   : {len(w)}")
print(f"photonic_holonet defines : {len(h)}")
print(f"shared                   : {len(w & h)}")
print(f"\nDEFINED IN w33_paper ONLY: {len(only_w)}")
print("  (an insert using any of these breaks the Holonet)")
for i in range(0, min(len(only_w), 80), 10):
    print("   ", ", ".join(only_w[i:i + 10]))
print(f"\nDEFINED IN holonet ONLY  : {len(only_h)}")
for i in range(0, min(len(only_h), 30), 10):
    print("   ", ", ".join(only_h[i:i + 10]))

out = ROOT / "data" / "w33_pass1479_host_only_macros.json"
out.write_text(json.dumps({"w33_paper_only": only_w,
                           "holonet_only": only_h,
                           "shared": sorted(w & h)}, indent=1), encoding="utf-8")
print(f"\nwrote {out.name}")
print(f"my hand-written guard list had 9 entries; the real asymmetry is "
      f"{len(only_w)} + {len(only_h)}")
