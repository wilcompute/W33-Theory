import os, re
patterns = ["Heegner", "Ramanujan tau", "CF alphabet", "12-regular", "840 identities", "D4 triality", "28 graphs", "Klein quartic", "PSL(2,7)", "Yukawa", "Y21", "Y32", "Spectral action", "Bose-Mesner", "Trace tower"]
compiled = {p: re.compile(p, re.IGNORECASE) for p in patterns}
results = {p: [] for p in patterns}
for root, dirs, files in os.walk("c:/Repos/Theory of Everything"):
    if ".venv" in root or ".claude" in root or "__pycache__" in root: continue
    for f in files:
        if not f.endswith((".py", ".md", ".tex")): continue
        path = os.path.join(root, f)
        try:
            with open(path, "r", encoding="utf-8") as fp:
                for i, line in enumerate(fp):
                    for p, regex in compiled.items():
                        if regex.search(line) and len(results[p]) < 5:
                            results[p].append(f"{path}:{i+1}")
        except: pass
for p in patterns:
    print(f"\n--- {p} ---")
    for r in results[p]: print(r)

