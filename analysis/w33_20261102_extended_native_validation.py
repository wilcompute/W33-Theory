"""Replay all nine extended-native producers and44 connected tests."""
import datetime
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import time
import importlib.util
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
STEMS=['deck_monodromy_network','clifford_native_cubic_repair','induced_cubic_common_cover',
       'quantized_native_tetrahedron','real_clifford_gate_synthesis','deck_twisted_quantum_double',
       'hypercube_switch_capacity','entanglement_metric_axiom_audit','spin6_rotation_group_audit']


def direct_tests():
    """Run the same assertion functions and unittest cases without root hooks.

    These files have no pytest fixtures. This is a collection fallback for
    the observed pytest collection timeout (SciPy import was slow), not a
    replacement for assertions or a claim that pytest integration passed.
    """
    modules=[];count=0
    for name in ['six_native_fronts','toroidal_knight_clifford_bridge','topology_interactions_geometry']:
        path=ROOT/'tests'/('test_w33_20261102_'+name+'.py')
        spec=importlib.util.spec_from_file_location('direct_'+name,path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);modules.append(module)
        for key in sorted(vars(module)):
            if key.startswith('test_') and callable(getattr(module,key)):
                print('DIRECT_TEST',name,key,flush=True);getattr(module,key)();count+=1
    suite=unittest.TestLoader().loadTestsFromModule(modules[-1])
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    assert result.wasSuccessful();count+=result.testsRun
    assert count==44,count
    print('PASS_44_DIRECT_ASSERTION_AND_UNITTEST_CASES',flush=True)


def main():
    env=dict(os.environ,PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
    inputs=['data/w33_20261102_toroidal_knight_clifford_bridge.json','data/w33_20261102_chiral_surface_development.json',
            'data/w33_20261031_signed_cubic_lift.json','data/w33_20261031_unitary_stabilizer_lift.json',
            'data/w33_20261101_common_cubic_spinor_extension.json','data/w33_20261102_common_cover_interactions.json']
    out=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        input_raw_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in inputs},
        execution='Remote Desktop Commander on TheHeavyCrown; same hardware as the workspace',jobs=[])
    jobs=[['analysis/w33_20261102_'+stem+'.py'] for stem in STEMS]+[
        ['-m','pytest','-q','tests/test_w33_20261102_six_native_fronts.py',
         'tests/test_w33_20261102_toroidal_knight_clifford_bridge.py','tests/test_w33_20261102_topology_interactions_geometry.py']]
    for args in jobs:
        print('START',args,flush=True);start=time.monotonic();command=[sys.executable,'-u']+args
        try:
            p=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=300)
            row=dict(command=command,exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr)
        except subprocess.TimeoutExpired as e:
            row=dict(command=command,exit_code=124,stdout=str(e.stdout or ''),stderr=str(e.stderr or ''),timeout_seconds=300)
        row['seconds']=round(time.monotonic()-start,3);out['jobs'].append(row)
        (ROOT/'data/w33_20261102_extended_native_validation.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
        print('RESULT',row['exit_code'],row['seconds'],row['stdout'][-1800:],row['stderr'][-800:],flush=True)
        if row['exit_code']!=0:
            if args[0:2]!=['-m','pytest'] or row['exit_code']!=124:raise SystemExit(1)
            command=[sys.executable,'-u',str(pathlib.Path(__file__).resolve()),'--direct-tests']
            start=time.monotonic()
            p=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=300)
            out['jobs'].append(dict(command=command,exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr,seconds=round(time.monotonic()-start,3)))
            out['pytest_collection_passed']=False
            assert p.returncode==0 and 'PASS_44_DIRECT_ASSERTION_AND_UNITTEST_CASES' in p.stdout
    out['status']=('PASS_NINE_PRODUCERS_AND_44_DIRECT_TEST_CASES' if out.get('pytest_collection_passed') is False
                   else 'PASS_NINE_PRODUCERS_AND_44_CONNECTED_TESTS')
    (ROOT/'data/w33_20261102_extended_native_validation.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':
    if '--direct-tests' in sys.argv:direct_tests()
    else:main()
