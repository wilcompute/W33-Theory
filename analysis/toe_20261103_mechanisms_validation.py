"""Reproduce seven mechanism audits, tests, hashes and independent receipt."""
import concurrent.futures,datetime,hashlib,json,os,pathlib,subprocess,sys,time
ROOT=pathlib.Path(__file__).resolve().parents[1]
STEMS=['portal_protection','stationary_uplift','four_dimensional_overlap','neutrino_messengers','gravity_identifiability','holomorphic_bridge','sector_reference']
INPUTS=['data/w33_20261103_native_quantum_vacuum_displacement.json',
 'analysis/toe_uv/fading_ds_dovekie.json','data/toe_20261103_dark_radiative_stability.json',
 'data/toe_20261103_sterile_anomaly_operators.json','analysis/toe_20261103_supergravity_vacuum_completion.py']

def main():
    env=dict(os.environ,PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONIOENCODING='utf-8')
    hashes={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in INPUTS}
    source_paths=[f'analysis/toe_20261103_mechanism_{x}.py'for x in STEMS]+['tests/test_toe_20261103_mechanisms.py','analysis/toe_20261103_mechanisms_validation.py']
    sources={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in source_paths}
    receipt=ROOT/'data/toe_20261103_mechanisms_validation.json'
    old=json.loads(receipt.read_text())if receipt.exists()else None
    def run(args):
        t=time.monotonic()
        try:
            p=subprocess.run(args,cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=240)
            r=dict(command=args,exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr,seconds=round(time.monotonic()-t,3))
        except subprocess.TimeoutExpired as e:
            r=dict(command=args,exit_code=124,stdout=str(e.stdout),stderr=str(e.stderr),seconds=round(time.monotonic()-t,3))
        print(args[-1],r['exit_code'],r['stdout'][-1800:],r['stderr'][-800:],flush=True);return r
    with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:
        rows=list(pool.map(run,[[sys.executable,'-u',f'analysis/toe_20261103_mechanism_{x}.py']for x in STEMS]))
    test=run([sys.executable,'-m','pytest','-q','--noconftest','tests/test_toe_20261103_mechanisms.py'])
    node=run(['node','analysis/toe_20261103_mechanism_server_controls.js'])
    assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in hashes.items())
    assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in sources.items()),'Source changed during validation; rerun on frozen sources'
    passed=all(r['exit_code']==0 for r in rows)and test['exit_code']==node['exit_code']==0
    out=dict(status='PASS_SEVEN_MECHANISM_PRODUCERS_AND_TESTS'if passed else 'FAIL_MECHANISM_VALIDATION',
        UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),producers=rows,pytest=test,node_replay=node,
        independent_server=json.loads((ROOT/'data/toe_20261103_mechanism_server_controls.json').read_text()),
        input_raw_sha256=hashes,source_raw_sha256=sources,output_raw_sha256={f'data/toe_20261103_mechanism_{x}.json':hashlib.sha256((ROOT/f'data/toe_20261103_mechanism_{x}.json').read_bytes()).hexdigest()for x in STEMS if(ROOT/f'data/toe_20261103_mechanism_{x}.json').exists()},
        initial_failure='The first photon ray quadrature used an absolute tolerance on a7e-38rad integrand and failed its analytic relative check. Fixed by integrating a normalized dimensionless kernel with1e-12 tolerance, then restoring physical units. No failed run is counted as PASS.',
        scope='Seven explicitly declared EFT/regulator mechanisms, not full repository tests, observational validation, an interacting four-dimensional chiral gauge theory or a solved TOE.')
    history=old.get('earlier_runs',[])if old else []
    if old:history.append(dict(status=old['status'],UTC=old['UTC'],producers=[dict(command=r['command'],exit_code=r['exit_code'])for r in old['producers']],pytest_exit_code=old['pytest']['exit_code'],pytest_stdout_tail=old['pytest']['stdout'][-2600:]))
    out['earlier_runs']=history
    out['serialization_repair']='First full run20passed1failed: Sympy could not parse exported lambda*v because lambda is a Python keyword. Changed only symbolic spelling to lam, regenerated the artifact and reran all producers/tests on frozen source hashes. The earlier failed result is retained.'
    receipt.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(out['status'],flush=True);assert passed
if __name__=='__main__':main()
