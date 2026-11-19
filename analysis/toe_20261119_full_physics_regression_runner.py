"""Run every repository tests/test_toe_20261119*.py and retain machine manifest.

Use --noconftest because the root conftest imports unrelated optional
research packages in this enormous repository. Does not claim full CI.
"""
import json,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
pattern=sorted((ROOT/"tests").glob("test_toe_20261119*.py"))
args=[sys.executable,"-m","pytest","--noconftest","-q",*[str(p) for p in pattern]]
print(f"NOV19 broad physics regression: {len(pattern)} modules",flush=True)
started=time.monotonic()
r=subprocess.run(args,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
elapsed=time.monotonic()-started
lines=r.stdout.splitlines()
out={"test_modules":len(pattern),"test_module_paths":[str(x.relative_to(ROOT)) for x in pattern],
     "exit_code":r.returncode,"elapsed_seconds":round(elapsed,2),
     "pytest_last_20_lines":lines[-20:],
     "scope":"ALL tests/test_toe_20261119*.py only, no other dates, with --noconftest; full repo CI and hooks excluded"}
path=ROOT/"data/toe_20261119_all_daily_physics_regression_manifest.json"
path.write_text(json.dumps(out,indent=2)+"\n",encoding="utf8")
print("\n".join(lines[-22:]),flush=True)
print("MANIFEST",path,flush=True)
if r.returncode:raise SystemExit(r.returncode)
