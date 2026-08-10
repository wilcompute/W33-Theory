import json
import subprocess
from pathlib import Path

def test_golay_clifford_mapping(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    res = subprocess.run([".venv\\Scripts\\python.exe", str(repo / "tools" / "golay_clifford.py")], cwd=repo)
    assert res.returncode == 0
    jsonf = repo / "artifacts" / "golay_clifford_mapping.json"
    csvf = repo / "artifacts" / "golay_clifford_mapping.csv"
    assert jsonf.exists() and csvf.exists()
    mapping = json.loads(jsonf.read_text(encoding="utf-8"))
    assert len(mapping) == 1 << 12
    # keys should be stringified integers, values tuples of ints
    for k, v in mapping.items():
        assert k.isdigit()
        assert isinstance(v, list) or isinstance(v, tuple)
        for idx in v:
            assert isinstance(idx, int) and 0 <= idx < 24
    # verify all monomials correspond to even-weight codewords
    for k, v in mapping.items():
        w = int(k)
        assert bin(w).count("1") % 2 == 0
    # closure sampling: multiply a few random pairs and ensure result appears
    import random
    monos = [tuple(v) for v in mapping.values()]
    mono_set = set(monos)
    def mult(a,b):
        sign = 1
        prod = list(a)
        for x in b:
            if x in prod:
                idx = prod.index(x)
                sign *= (-1) ** (len(prod) - idx - 1)
                prod.pop(idx)
            else:
                larger = sum(1 for y in prod if y > x)
                sign *= (-1) ** larger
                pos = 0
                while pos < len(prod) and prod[pos] < x:
                    pos += 1
                prod.insert(pos, x)
        return tuple(prod)
    for _ in range(100):
        a = random.choice(monos)
        b = random.choice(monos)
        assert mult(a,b) in mono_set
