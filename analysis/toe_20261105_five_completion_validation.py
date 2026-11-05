"""Replay both completion producers and forty focused controls with hashes."""
import pathlib,sys,json,subprocess,time,hashlib,datetime
R=pathlib.Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
def main():
 sources=['analysis/toe_20261105_five_fronts_model_completion.py','analysis/toe_20261105_global_measure_and_lorentz_branches.py','analysis/toe_20261105_five_completion_validation.py','analysis/toe_20261105_five_completion_server.js','tests/test_toe_20261105_five_completion_fronts.py']
 inputs=['analysis/toe_20261103_mechanism_four_dimensional_overlap.py']
 out=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_raw_sha256={p:sha(p)for p in sources},input_raw_sha256={p:sha(p)for p in inputs},producers=[])
 for source in sources[:2]:
  t=time.monotonic();p=subprocess.run([sys.executable,source],cwd=R,capture_output=True,text=True,encoding='utf-8',errors='replace')
  out['producers'].append(dict(path=source,exit_code=p.returncode,seconds=time.monotonic()-t,stdout=p.stdout,stderr=p.stderr));assert p.returncode==0,p.stderr
 p=subprocess.run([sys.executable,'-m','pytest','-q','--noconftest','tests/test_toe_20261105_five_completion_fronts.py','tests/test_toe_20261105_pq_uv_controls.py','tests/test_toe_20261103_mechanisms.py'],cwd=R,capture_output=True,text=True,encoding='utf-8',errors='replace')
 out['pytest']=dict(exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr);assert p.returncode==0,p.stdout+p.stderr
 p=subprocess.run(['node','analysis/toe_20261105_five_completion_server.js'],cwd=R,capture_output=True,text=True,encoding='utf-8',errors='replace');assert p.returncode==0,p.stderr
 out['Node_server_source_replay']=json.loads(p.stdout)
 out['output_raw_sha256']={p:sha(p)for p in ['data/toe_20261105_five_fronts_model_completion.json','data/toe_20261105_global_measure_and_lorentz_branches.json']}
 for group in ['source_raw_sha256','input_raw_sha256']:
  for p,h in out[group].items():assert sha(p)==h,p
 out['initial_test_failure_history']='6PASS2FAIL: symbolic radial fluctuation incorrectly assumed positive, floating Chern integer required exact equality. Repaired test domain/tolerance; no science adjusted. Then8PASS. Refined40mesh and Schlaefli/Hessian additions checked in final replay.'
 out['EFT_scope_correction']='Initial18point flow sweep ran12rows throughMU but overlooked radial-above-fermion ordering in9rows. Final producer rejects these unsupported orderings before integration. Remaining9supported rows:5reachMU,4cut early; no absolute-stability pass inferred. Added explicit rejection control.'
 out['status']='PASS_TWO_FIVE_FRONT_PRODUCERS_AND_41_COMBINED_TESTS'
 (R/'data/toe_20261105_five_completion_validation.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
 print(out['status'],out['pytest']['stdout'],flush=True)
if __name__=='__main__':main()
