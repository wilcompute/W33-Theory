"""Reproduce gauge-ring/Wilson-line producers and independent controls."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time
import toe_20261108_gauge_ring_quality as ring
import toe_20261108_wilson_line_mass_probe as wl

ROOT=Path(__file__).resolve().parents[1]


def main():
    start=time.monotonic();r=ring.build();w=wl.build()
    controls=[ring.matrix_control(300,psi=1.37,eps=.053*.15)]
    assert controls[0]['singular_spectrum_residual']<1e-12
    assert w['conditional_window']['window_exists']
    assert w['benchmark']['fixed_population_density_curvature_control']['curvature_over_H0_squared']>1
    env=dict(os.environ,PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
    cmd=[sys.executable,'-m','pytest','--noconftest','-q','tests/test_toe_20261108_gauge_origin.py','tests/test_toe_20261108_cyclic_vector.py']
    t=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180)
    print(t.stdout,t.stderr,flush=True)
    if t.returncode:raise RuntimeError('No PASS receipt: focused tests failed')
    files=['analysis/toe_20261108_gauge_ring_quality.py','analysis/toe_20261108_wilson_line_mass_probe.py','analysis/toe_20261108_gauge_origin_server.js','analysis/toe_20261108_gauge_origin_validation.py','tests/test_toe_20261108_gauge_origin.py','data/toe_20261108_gauge_ring_quality.json','data/toe_20261108_wilson_line_mass_probe.json','data/toe_20261108_gauge_origin_server.json','tests/test_toe_20261108_cyclic_vector.py']
    out=dict(status='PASS_DECLARED_GAUGE_ORIGIN_NORMAL_MODE_OPERATOR_AND_WORLDLINE_CONTROLS_NOT_TOE',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),seconds=time.monotonic()-start,
             tests=dict(command=cmd,exit_code=t.returncode,stdout=t.stdout,stderr=t.stderr),extra_N300_matrix=controls,
             artifact_raw_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in files},
             earlier_RDC_execution=dict(device='75dccda9-254c-47a9-9d13-ef69565dedf7',ring=dict(pid=28532,exit_code=0,seconds=7.63),one_Dirac_probe=dict(pid=27584,exit_code=0,seconds=24.70),parity_pair_probe=dict(pid=28996,exit_code=0,seconds=6.13),parity_regulator_and_first_tests=dict(pid=28828,exit_code=0,seconds=25.24,test_stdout='19passed10.44s')),
             actual_server='Independent functions.exec V8 positive worldline quadrature, full scalar-generating-function partial sums, ring cutoff and KK-coupling arithmetic. No independent population, background or radion solver.',
             scope='19new parameterized controls plus18previous vector-action/quality tests. Additional actualN300mass matrix. All operator/loop/weakgravity/species claims retain declared coefficient, cutoff, field-inventory and fixed-radius assumptions. No full vacuum, UV gravity, relic/perturbation or TOE completion.')
    (ROOT/'data/toe_20261108_gauge_origin_validation.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(out['status'],out['seconds'],flush=True)


if __name__=='__main__':main()
