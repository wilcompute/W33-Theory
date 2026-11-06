"""Replay native model and18 new plus17 related PQ/determinant controls."""
import pathlib,sys,subprocess,json,hashlib,time,datetime,os
R=pathlib.Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
def main():
    source=['analysis/toe_20261105_native_boundary_axion.py','analysis/toe_20261105_native_boundary_axion_server.js',
      'analysis/toe_20261105_native_boundary_axion_validation.py','tests/test_toe_20261105_native_boundary_axion.py']
    inputs=['analysis/w33_levi_kirchhoff_cycle_projector.py','data/PART_BT547_W33_LEVI_KIRCHHOFF_CYCLE_PROJECTOR_results.json',
      'data/PART_W33_PASS5396_5401_ALLQ_APARTMENT_TIGHT_FRAME.json','analysis/toe_20261105_determinant_and_fermion_quality.py',
      'analysis/toe_20261105_pq_quality_gauge_obstruction.py','analysis/toe_20261105_pq_normalization_cutoff.py']
    out=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_raw_sha256={p:sha(p)for p in source},input_raw_sha256={p:sha(p)for p in inputs})
    env=os.environ.copy();env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
    t=time.monotonic();p=subprocess.run([sys.executable,source[0]],cwd=R,capture_output=True,text=True,encoding='utf-8',timeout=180,env=env)
    out['producer']=dict(exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr,seconds=time.monotonic()-t)
    assert p.returncode==0,p.stdout+p.stderr
    tests=['tests/test_toe_20261105_native_boundary_axion.py','tests/test_toe_20261105_determinant_and_fermion_quality.py','tests/test_toe_20261105_pq_uv_controls.py']
    t=time.monotonic();p=subprocess.run([sys.executable,'-m','pytest','-q','--noconftest']+tests,cwd=R,capture_output=True,text=True,encoding='utf-8',timeout=180,env=env)
    out['pytest']=dict(exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr,seconds=time.monotonic()-t)
    out['initial_validation_history']='Before the extra phase/telescoping/scalar-mediator controls,14 new cases passed32.09s. Server direct powers overflowed the s6 Planck denominator; switched to logs, retained history and tested all six nonzero amplitudes againstPC.'
    out['output_raw_sha256']={p:sha(p)for p in ['data/toe_20261105_native_boundary_axion.json','data/toe_20261105_native_boundary_axion_server.json']}
    for group in ['source_raw_sha256','input_raw_sha256']:
        for path,h in out[group].items():assert sha(path)==h,path
    out['status']='PASS_NATIVE_PRODUCER_AND_35_RELEVANT_TESTS'if p.returncode==0 and '35 passed'in p.stdout else 'FAILED'
    (R/'data/toe_20261105_native_boundary_axion_validation.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(out['status'],p.stdout,p.stderr,flush=True);assert out['status'].startswith('PASS'),out
if __name__=='__main__':main()
