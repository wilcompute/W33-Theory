"""Reproduce new result, nine focused controls and 41 prior mechanism controls."""
import pathlib,subprocess,sys,json,hashlib,time,datetime
R=pathlib.Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
def main():
    sources=['analysis/toe_20261105_determinant_and_fermion_quality.py',
      'analysis/toe_20261105_determinant_quality_validation.py',
      'analysis/toe_20261105_determinant_quality_server.js',
      'tests/test_toe_20261105_determinant_and_fermion_quality.py']
    out=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_raw_sha256={p:sha(p)for p in sources})
    t=time.monotonic();p=subprocess.run([sys.executable,sources[0]],cwd=R,capture_output=True,text=True,encoding='utf-8',timeout=180)
    out['producer']=dict(exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr,seconds=time.monotonic()-t)
    assert p.returncode==0,p.stdout+p.stderr
    tests=['tests/test_toe_20261105_determinant_and_fermion_quality.py','tests/test_toe_20261105_five_completion_fronts.py','tests/test_toe_20261105_pq_uv_controls.py','tests/test_toe_20261103_mechanisms.py']
    t=time.monotonic();p=subprocess.run([sys.executable,'-m','pytest','-q','--noconftest']+tests,cwd=R,capture_output=True,text=True,encoding='utf-8',timeout=180)
    out['pytest']=dict(exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr,seconds=time.monotonic()-t)
    out['initial_attempt']='Initial pytest without --noconftest completed nine tests in156.75s; an attempted stop found it had already exited. Focused replay excludes repository-wide conftest initialization.'
    out['output_raw_sha256']={p:sha(p)for p in ['data/toe_20261105_determinant_and_fermion_quality.json','data/toe_20261105_determinant_quality_server.json']}
    for path,h in out['source_raw_sha256'].items():assert sha(path)==h,path
    out['status']='PASS_NEW_PRODUCER_AND_50_COMBINED_TESTS'if p.returncode==0 and '50 passed'in p.stdout else 'FAILED'
    (R/'data/toe_20261105_determinant_quality_validation.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(out['status'],p.stdout,p.stderr,flush=True);assert out['status'].startswith('PASS'),out
if __name__=='__main__':main()
