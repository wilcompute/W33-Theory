"""Regenerate six audits across five physical fronts; run isolated tests."""
import concurrent.futures,datetime,hashlib,json,os,pathlib,subprocess,sys,time
ROOT=pathlib.Path(__file__).resolve().parents[1]
STEMS=['supergravity_vacuum_completion','dark_radiative_stability','chiral_mirror_benchmark','sterile_anomaly_operators','gravity_entanglement_models']
EXTRA=['abelian_uv_matching']
INPUTS=['data/w33_20261103_native_quantum_vacuum_displacement.json']+[f'analysis/toe_uv/fading_ds_{name}.json'for name in ['pantheon','dovekie','desy5']]
def main():
    env=dict(os.environ,PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONIOENCODING='utf-8')
    frozen={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in INPUTS}
    def run(cmd):
        t=time.monotonic();p=subprocess.run(cmd,cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=240)
        row=dict(command=cmd,exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr,seconds=round(time.monotonic()-t,3));print(cmd[-1],p.returncode,p.stdout[-2200:],p.stderr[-700:],flush=True);return row
    with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:
        records=list(pool.map(run,[[sys.executable,'-u',f'analysis/toe_20261103_{stem}.py']for stem in STEMS]))
    # UV audit consumes the freshly regenerated sterile charge certificate.
    records +=[run([sys.executable,'-u',f'analysis/toe_20261103_{stem}.py'])for stem in EXTRA]
    test=run([sys.executable,'-m','pytest','-q','--noconftest','tests/test_toe_20261103_physical_completion.py'])
    passed=all(r['exit_code']==0 for r in records)and test['exit_code']==0
    assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in frozen.items())
    out=dict(status='PASS_SIX_PHYSICAL_COMPLETION_PRODUCERS_AND_PYTEST'if passed else 'FAIL_PHYSICAL_COMPLETION_VALIDATION',
        utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),producers=records,pytest=test,input_raw_sha256=frozen,
        output_raw_sha256={f'data/toe_20261103_{stem}.json':hashlib.sha256((ROOT/f'data/toe_20261103_{stem}.json').read_bytes()).hexdigest()for stem in STEMS+EXTRA},
        independent_server=json.loads((ROOT/'data/toe_20261103_server_physics_controls.json').read_text()),
        scope='Five declared physical-EFT/model audits, not a complete TOE or all-repository test run. Actual commands and failures are retained.',
        earlier_repairs='Initial sterile coefficient benchmark had a handwritten determinant coefficient2 instead of1; symbolic assertion caught it before output. Initial radiative producer had an unescaped derivative apostrophe in metadata; corrected before output. Charge-lattice refinement exposed a third allowed anomaly sector, preventing an unconditional two-sector claim.')
    (ROOT/'data/toe_20261103_physical_completion_validation.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(out['status'],flush=True);assert passed
if __name__=='__main__':main()
