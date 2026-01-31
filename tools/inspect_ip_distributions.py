#!/usr/bin/env python3
import json
import sys
from pathlib import Path

# ensure project root is on sys.path for local imports
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.e8_w33_bijection import load_explicit_bijection
from tools.e8_w33_harness import ip_distributions

ART = Path("artifacts/explicit_bijection_decomposition.json")
data = load_explicit_bijection(ART)
ip_adj, ip_non = ip_distributions(data)
print("adjacent =", json.dumps(ip_adj, sort_keys=True))
print("nonadjacent =", json.dumps(ip_non, sort_keys=True))
