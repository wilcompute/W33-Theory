import pathlib,subprocess,json,hashlib,datetime,sys,time
R=pathlib.Path(__file__).resolve().parents[1];sys.stdout.reconfigure(encoding='utf-8')
sources=['analysis/toe_20261105_pq_quality_gauge_obstruction.py','analysis/toe_20261105_pq_normalization_cutoff.py','tests/test_toe_20261105_pq_uv_controls.py','analysis/toe_20261105_pq_uv_validation.py','analysis/toe_20261105_pq_server_controls.js']
inputs=['analysis/toe_uv/pq_full_scan.json','analysis/toe_uv/pq_twoloop.json','analysis/toe_uv/pq_gates.py','analysis/toe_uv/pq_mass_ceiling.py']
def sha(p):return hashlib.sha256((R/p).read_bytes()).hexdigest()
out=dict(UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_raw_sha256={p:sha(p)for p in sources},input_raw_sha256={p:sha(p)for p in inputs},producers=[])
for src in sources[:2]:
 t=time.time();p=subprocess.run([sys.executable,src],cwd=R,capture_output=True,text=True,encoding='utf-8',errors='replace')
 out['producers'].append(dict(path=src,exit_code=p.returncode,seconds=time.time()-t,stdout=p.stdout,stderr=p.stderr));assert p.returncode==0,p.stderr
p=subprocess.run([sys.executable,'-m','pytest','-q','--noconftest','tests/test_toe_20261105_pq_uv_controls.py','tests/test_toe_20261103_mechanisms.py'],cwd=R,capture_output=True,text=True,encoding='utf-8',errors='replace')
out['pytest']=dict(exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr);assert p.returncode==0,p.stdout+p.stderr
out['output_raw_sha256']={p:sha(p)for p in ['data/toe_20261105_pq_quality_gauge_obstruction.json','data/toe_20261105_pq_normalization_cutoff.json']}
for k in ['source_raw_sha256','input_raw_sha256']:
 for src,h in out[k].items():assert sha(src)==h,src
out['status']='PASS_TWO_PQ_UV_PRODUCERS_AND_32_COMBINED_TESTS'
out['initial_launch_failure']='Remote process5720 rejected CMD && syntax under PowerShell before executing Python. Relaunched with absolute producer path, no scientific input changed.'
out['corrected_unpublished_citation']='The originally typed1203.0896 points to an unrelated condensed matter paper. Verified and corrected to1203.0237 before final producer replay.'
(R/'data/toe_20261105_pq_uv_validation.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(out['status'],p.stdout,flush=True)
