"""Reproduce coupled classical transport, sensitivity checks and focused tests."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1';os.environ['OMP_NUM_THREADS']='1'
import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]


def main():
    start=time.monotonic()
    spec=importlib.util.spec_from_file_location('moments',ROOT/'analysis/toe_20261107_coupled_scalar_moments.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    baseline=m.run();rates=m.ThermalRates();experiments=[]
    def compare(label,mass,**kwargs):
        result=m.solve(mass,rates,**kwargs)
        base=next(x for x in baseline['rows']if x['M_keV']==mass)
        residual={key:result[key]/base[key]-1 for key in ['omega_h2','mean_q','rms_q']}
        experiments.append(dict(label=label,relative_changes=residual,row=result))
        print('CHECK',label,mass,residual,flush=True)
        return residual
    for mass in [16.,30.,100.]:
        residual=compare('72momentum32transfer_nodes',mass,nq=72,nangle=32)
        assert max(abs(x) for x in residual.values())<.003
    residual=compare('independent_Radau_ODE',30.,method='Radau')
    assert max(abs(x) for x in residual.values())<2e-4
    for scale in [.5,2.]:compare('chemical_rate_scale_'+str(scale),30.,chemical_scale=scale)
    for r0 in [.01,.1]:compare('reheating_cutoff_'+str(r0),16.,r0=r0)
    compare('reheating_cutoff_point1',30.,r0=.1)
    residual=compare('source_seed_refinement',16.,seed_interval=1e-6)
    assert max(abs(x) for x in residual.values())<2e-4
    compare('omit_leading_portal_selfexchange',30.,portal_exchange=False)
    coarse=m.ThermalRates(json.loads((ROOT/'data/toe_20261107_coupled_scalar_rate_table_coarse.json').read_text()))
    result=m.solve(30.,coarse);base=baseline['rows'][1]
    experiments.append(dict(label='coarse_MC_rate_table',relative_changes={key:result[key]/base[key]-1 for key in ['omega_h2','mean_q','rms_q']},row=result))
    command=[sys.executable,'-m','pytest','--noconftest','-q','tests/test_toe_20261107_coupled_scalar_moments.py','tests/test_w33_20261107_constants_five_fronts.py']
    test=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
    if test.returncode:raise RuntimeError(test.stdout+test.stderr)
    files=['analysis/toe_20261107_coupled_scalar_moments.py','analysis/toe_20261107_scalar_self_reactions.py',
           'analysis/toe_20261107_coupled_scalar_rate_server.js','analysis/toe_20261107_scalar_self_server.js',
           'analysis/toe_20261107_coupled_scalar_validation.py','tests/test_toe_20261107_coupled_scalar_moments.py',
           'data/toe_20261107_coupled_scalar_rate_table.json','data/toe_20261107_coupled_scalar_rate_table_coarse.json',
           'data/toe_20261107_coupled_scalar_moments.json','data/toe_20261107_coupled_scalar_rate_server.json']
    receipt=dict(status='PASS_COUPLED_CLASSICAL_MOMENTS_AND_NUMERICAL_CONTROLS_NOT_UV_COMPLETION',
                 UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),seconds=time.monotonic()-start,
                 experiments=experiments,tests=dict(command=command,exit_code=test.returncode,stdout=test.stdout,stderr=test.stderr),
                 artifact_raw_sha256={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()for f in files},
                 scope='Eight coupled physics checks plus seven incoming constants tests. Two stiff ODE methods; resolution, seed, chemical-rate, reheating and leading-portal controls. Server validates chemical rate coefficients only. No independent server coupled ODE. Frozen broken-phase/MB assumptions have material flagged violations.')
    (ROOT/'data/toe_20261107_coupled_scalar_validation.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(receipt['status'],test.stdout,'seconds',receipt['seconds'],flush=True)


if __name__=='__main__':main()
