"""Reproduce the frozen-history self-collision refinement and focused tests.

Run producer with --power17 first to reproduce the stored17-to18 comparison;
otherwise the receipt truthfully labels whichever existing reference it reads.
The independent server output must already exist; this script never fabricates
it by executing JavaScript on the PC and calling that server execution.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
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
    spec=importlib.util.spec_from_file_location('self_rates',ROOT/'analysis/toe_20261107_scalar_self_reactions.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    target=ROOT/'data/toe_20261107_scalar_self_reactions.json'
    reference=json.loads(target.read_text())
    result=module.evaluate(18)
    target.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    comparisons=[]
    for old,new in zip(reference['rows'],result['rows']):
        assert (old['M_keV'],old['r'])==(new['M_keV'],new['r'])
        comparisons.append(dict(M_keV=new['M_keV'],r=new['r'],relative_changes={
            key:abs(old[key]/new[key]-1) for key in [
                'gamma32_over_nS_H','gamma23_over_nS_H','elastic_entropy_production_over_nS_H']}))
    test=subprocess.run([sys.executable,'-m','pytest','--noconftest','-q','tests/test_toe_20261107_scalar_self_reactions.py'],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
    if test.returncode:raise RuntimeError(test.stdout+test.stderr)
    files=['analysis/toe_20261107_scalar_self_reactions.py','analysis/toe_20261107_scalar_self_server.js',
           'analysis/toe_20261107_scalar_self_validation.py','tests/test_toe_20261107_scalar_self_reactions.py',
           'data/toe_20261107_scalar_self_reactions.json','data/toe_20261107_scalar_self_server_input.json',
           'data/toe_20261107_scalar_self_server.json']
    receipt=dict(status='PASS9_TESTS_AND_INDEPENDENT_MC_FROZEN_HISTORY_DIAGNOSTIC',
                 UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),seconds=time.monotonic()-start,
                 tests=dict(exit_code=test.returncode,stdout=test.stdout,stderr=test.stderr),
                 power_refinement=dict(from_power=reference['power'],to_power=result['power'],comparisons=comparisons),
                 artifact_raw_sha256={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files},
                 limits='Four scrambled Sobol replicates estimate sampling uncertainty, not a rigorous integration bound. No corrected parent history or sterile spectrum computed.')
    (ROOT/'data/toe_20261107_scalar_self_validation.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(receipt['status'],test.stdout,flush=True)


if __name__=='__main__':main()
