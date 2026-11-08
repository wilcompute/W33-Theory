"""Reproduce focused physical checks without unrelated legacy-fixture setup."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
ARTIFACTS=[
    'analysis/toe_20261108_axion_eigenmode_audit.py',
    'analysis/toe_20261108_native_cyclic_orders.py',
    'analysis/toe_20261108_cyclic_partner_control.py',
    'analysis/toe_20261108_axion_server_control.js',
    'analysis/toe_20261108_axion_validation.py',
    'tests/test_toe_20261108_axion_and_cyclic.py',
    'data/toe_20261108_axion_eigenmode_audit.json',
    'data/toe_20261108_native_cyclic_orders.json',
    'data/toe_20261108_cyclic_partner_control.json',
    'data/toe_20261108_axion_server_control.json',
    'analysis/w33_20261108_forty_points_fivefronts.py',
    'tests/test_w33_20261108_forty_points_fivefronts.py',
]


def main():
    started=time.monotonic()
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
    command=[sys.executable,'-m','pytest','--noconftest','-q',
             'tests/test_toe_20261108_axion_and_cyclic.py',
             'tests/test_w33_20261108_forty_points_fivefronts.py']
    test=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180)
    print(test.stdout,test.stderr,flush=True)
    if test.returncode:raise RuntimeError('Focused tests failed; no PASS receipt written')
    out=dict(status='PASS_CANONICAL_EIGENMODES_CYCLIC_SPECTRUM_AND_INCOMING_FINITE_CLOCK_CONTROLS',
             UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),seconds=time.monotonic()-started,
             tests=dict(command=command,environment_overrides={k:env[k]for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','PYTEST_DISABLE_PLUGIN_AUTOLOAD']},exit_code=test.returncode,stdout=test.stdout,stderr=test.stderr),
             artifact_raw_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in ARTIFACTS},
             execution=dict(RDC_device='75dccda9-254c-47a9-9d13-ef69565dedf7',
                            group_job=dict(pid=7640,exit_code=0,runtime_seconds=6.06),
                            original_axion_job=dict(pid=26120,exit_code=1,reason='Sampling allowed a negative cosine, violating bound premise; corrected sampler before successful rerun.'),
                            corrected_axion_job=dict(pid=16092,exit_code=0,runtime_seconds=7.63),
                            cyclic_partner_job=dict(pid=30456,exit_code=0,runtime_seconds=3.19),
                            final_axion_source='Subsequent local rerun added the independently tested incoming phenomenological Fi-limit control.',
                            server='Actual functions.exec server V8 ran independent bisection/spectra/leading-envelope/population calculation and persisted its output. No independent full cosmological solve.',
                            initial_test_attempt='First command omitted --noconftest and stalled in unrelated legacy setup before test output. Its exact owned pytest PID25932 was stopped; focused tests use --noconftest. No PASS claimed for interrupted attempt.'),
             scope='Own parameterized physical controls plus incoming finite-clock/catalog controls; exact current test count in captured stdout. No cosmological likelihood rerun, physical UV completion, general axion no-go or solved TOE.')
    path=ROOT/'data/toe_20261108_axion_validation.json'
    path.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(out['status'],out['seconds'],flush=True)


if __name__=='__main__':main()
