#!/usr/bin/env python3
from fractions import Fraction
import json

chi = Fraction(24)

def split(tau):
    d = Fraction(3, 2) * tau
    return {"tau": str(tau), "diff": str(d), "plus": str((chi + d) / 2), "minus": str((chi - d) / 2)}

base = split(Fraction(-16))
rev = split(Fraction(16))
out = {
    "bt": 1149,
    "title": "K3 orientation convention",
    "choice": "use tau=-16 as the paper orientation",
    "base": base,
    "reversed": rev,
    "checks": {
        "base_plus_zero": base["plus"] == "0",
        "base_minus_24": base["minus"] == "24",
        "reverse_plus_24": rev["plus"] == "24",
        "reverse_minus_zero": rev["minus"] == "0",
    },
}
out["checks"]["all_checks_pass"] = all(out["checks"].values())
print(json.dumps(out, indent=2, sort_keys=True))
