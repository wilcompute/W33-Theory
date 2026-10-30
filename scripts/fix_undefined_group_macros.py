"""Compile-and-fix loop for undefined GROUP-NAME macros in manuscript inserts (2026-10-30).

Remote batches wrote \\PSL_2(q), \\GL(2,3), \\AGL, \\PG(H) ... into analysis/*_insert.tex, but no manuscript preamble defines them, so
w33_paper.tex, photonic_holonet.tex and holonet_machine_blueprint.tex stopped building (tectonic halts at the FIRST undefined control
sequence, so each CI run showed one at a time).  This loop compiles a manuscript, reads the first undefined macro from the log, and if
it is an all-capital group name (2-6 letters, optionally with a leading A/P such as AGL, PSL, PSp) replaces \\NAME by \\mathrm{NAME} in
that insert only -- the rendering is identical -- then recompiles.  It stops, without editing, at any other kind of macro.

    py -3 scripts/fix_undefined_group_macros.py w33_paper.tex [more.tex ...]
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TECTONIC = Path("C:/Users/wiljd/tools/tectonic/tectonic.exe")
OUT = Path.home() / "AppData/Local/Temp/tectonic_fixloop"
B = chr(92)
# blackboard-bold field/ring macros are NOT group names: \FF means \mathbb{F} (as papers/*.tex define it), never \mathrm{FF}
SPECIAL = {"FF": B + "mathbb{F}", "ZZ": B + "mathbb{Z}", "QQ": B + "mathbb{Q}", "RR": B + "mathbb{R}", "CC": B + "mathbb{C}",
           "NN": B + "mathbb{N}"}
GROUPISH = re.compile(r"^(?:[A-Z]{1,2}[a-z]?[A-Z]{0,3}|[A-Z][a-z][A-Z]?)$")      # PSL, GL, AGL, PSp, Sp, SL, PG, AG, PGL, PSU


def first_undefined(tex):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / (Path(tex).stem + ".pdf")).unlink(missing_ok=True)
    subprocess.run([str(TECTONIC), "-X", "compile", "--keep-logs", "--outdir", str(OUT), tex], cwd=ROOT, capture_output=True, timeout=1800)
    log = (OUT / (Path(tex).stem + ".log")).read_text(encoding="utf-8", errors="replace")
    i = log.find("! Undefined control sequence.")
    if i < 0:
        # "builds" means the PDF was written -- an undefined ENVIRONMENT or any other error must not read as success
        ok = (OUT / (Path(tex).stem + ".pdf")).exists() and re.search(r"(?m)^! ", log) is None
        return None if ok else ("(other error)", None, None)
    seg = log[max(0, i - 4000):i + 600]
    files = re.findall(r"\((?:\./)?(analysis/[A-Za-z0-9_\-]+_(?:insert|INSERT))(?:\.tex)?", seg)
    m = re.search(r"\nl\.(\d+) (.*?)" + re.escape(B) + r"([A-Za-z]+)\s*\n(.*)\n", log[i:i + 600])
    if not m:
        return (None, None, None)
    tail = (B + m.group(3) + m.group(4).strip())[:40]
    hits = subprocess.run(["git", "grep", "-l", "-F", tail, "--", "analysis/*.tex"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    ins = hits[0][:-4] if len(hits) == 1 else (files[-1] if files else None)
    return (ins, int(m.group(1)), m.group(3))


def main():
    for tex in sys.argv[1:]:
        for it in range(30):
            r = first_undefined(tex)
            if r is None:
                print(f"{tex}: builds"); break
            ins, line, name = r
            if not (ins and name and (name in SPECIAL or GROUPISH.match(name))):
                print(f"{tex}: STOP at {ins}:{line} \\{name} (not a group name; fix by hand)"); break
            p = ROOT / (ins + ".tex"); s = p.read_bytes().decode("utf-8")
            n = len(re.findall(re.escape(B + name) + r"(?![A-Za-z])", s))
            if n == 0:
                print(f"{tex}: STOP -- located {ins} but it has no \\{name}; fix by hand"); break
            s = re.sub(re.escape(B + name) + r"(?![A-Za-z])", lambda _: SPECIAL.get(name, B + "mathrm{" + name + "}"), s)
            p.write_bytes(s.encode("utf-8"))
            print(f"{tex}: {ins}: {B}{name} -> {SPECIAL.get(name, B + 'mathrm{' + name + '}')} ({n} occurrences)")
        else:
            print(f"{tex}: gave up after 30 iterations")


if __name__ == "__main__":
    main()
