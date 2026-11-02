"""Replay the knight bridge and independent connected tests with actual logs."""
import datetime
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT/'data/w33_20261102_knight_bridge_validation.json'


def main():
    env = dict(os.environ, PYTEST_DISABLE_PLUGIN_AUTOLOAD='1', OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1')
    jobs = [
        ['analysis/w33_20261102_toroidal_knight_clifford_bridge.py'],
        ['-m','pytest','-q','tests/test_w33_20261102_toroidal_knight_clifford_bridge.py',
         'tests/test_w33_20261102_topology_interactions_geometry.py'],
    ]
    out = dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
               execution='Remote Desktop Commander on TheHeavyCrown; same hardware as local workspace',
               input_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in [
                   'data/w33_20261031_unitary_stabilizer_lift.json',
                   'data/w33_20261102_chiral_surface_development.json']},jobs=[])
    for args in jobs:
        command = [sys.executable,'-u']+args
        print('START',args,flush=True)
        start = time.monotonic()
        try:
            p = subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=600)
            row = dict(command=command,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr)
        except subprocess.TimeoutExpired as e:
            row = dict(command=command,returncode=None,timeout_seconds=600,
                       stdout=str(e.stdout or ''),stderr=str(e.stderr or ''))
        row['seconds'] = round(time.monotonic()-start,3)
        out['jobs'].append(row)
        OUT.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
        print('RESULT',row['returncode'],row['seconds'],row['stdout'][-3000:],row['stderr'][-1000:],flush=True)
        if row['returncode'] != 0:
            raise SystemExit(1)
    out['status']='PASS_PRODUCER_AND_21_CONNECTED_TESTS'
    OUT.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')


if __name__ == '__main__':
    main()
