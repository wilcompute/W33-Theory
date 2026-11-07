"""Record actual subprocess outcomes and frozen hashes for the sterile audit."""
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys
import time

ROOT=pathlib.Path(__file__).resolve().parents[1]
SOURCES=['analysis/toe_20261106_sterile_parent_consistency.py','analysis/toe_20261106_sterile_parent_server.js','analysis/toe_20261106_published_star_axion_server.js',
         'tests/test_toe_20261106_sterile_parent_consistency.py','analysis/toe_20261106_sterile_parent_validation.py']

def sha(p):
    return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()

def main():
    rows=[]
    for args in [[sys.executable,'analysis/toe_20261106_sterile_parent_consistency.py'],
                 [sys.executable,'-m','pytest','--noconftest','-q','tests/test_toe_20261106_sterile_parent_consistency.py']]:
        start=time.monotonic()
        p=subprocess.run(args,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180)
        rows.append(dict(args=args,exit_code=p.returncode,seconds=time.monotonic()-start,stdout=p.stdout,stderr=p.stderr))
        print(p.stdout,flush=True)
        if p.returncode:
            print(p.stderr,flush=True)
            raise RuntimeError('Validation subprocess failed')
    packet=json.loads((ROOT/'data/toe_20261106_sterile_parent_consistency.json').read_text())
    assert all(sha(p)==h for p,h in packet['input_raw_sha256'].items())
    out=dict(status='PASS_PRODUCER_AND_TWELVE_TARGETED_TESTS',UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),
             runs=rows,source_raw_sha256={p:sha(p) for p in SOURCES},input_raw_sha256=packet['input_raw_sha256'],
             output_raw_sha256={p:sha(p) for p in ['data/toe_20261106_sterile_parent_consistency.json','data/toe_20261106_sterile_parent_server.json','data/toe_20261106_published_star_axion_server.json']},
             execution_scope='PC Python producer plus twelve isolated tests, including comparison against both actual server-V8 artifacts. Remote Desktop Commander attempted but device offline; local exec used. No remote process success asserted.',
             earlier_runs='Initial8 ordinary pytest tests passed175.07s; stop attempt saw already absent PID, so no process was stopped.9 isolated tests passed7.91s before final metadata cleanup. Initial symbolic test required algebraic difference simplification rather than structural equality. Earlier12test versions passed before a physical vev-normalization correction: incoming mN=y*vS/sqrt2 and Gamma=y^2*mS/(16pi) require canonical real S vev w=vS/sqrt2. Quartics double relative to the initial w=vS mapping; final tests explicitly check mN=y*w and mS^2=2lambda*w^2.',
             fixture_scope='--noconftest omits unrelated repository legacy-fixture setup. Tests use explicit local imports and stored inputs; no full-repo test success asserted.')
    (ROOT/'data/toe_20261106_sterile_parent_validation.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(out['status'],flush=True)

if __name__=='__main__':
    main()
