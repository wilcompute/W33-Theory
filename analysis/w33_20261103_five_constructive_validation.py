"""Regenerate six producers across five fronts; retain actual pytest output."""
import concurrent.futures,datetime,hashlib,json,os,pathlib,subprocess,sys,time
ROOT=pathlib.Path(__file__).resolve().parents[1]
STEMS=['changed_embedding_matter_completion','native_singlet_stabilization','native_qutrit_feedforward','kagome_tunneling_bounds','deck_twist_interfaces','native_quantum_vacuum_displacement']
INPUTS=['data/w33_20261102_clifford_native_cubic_repair.json','data/w33_20261103_native_projector_holonomic_qutrit.json','data/w33_20261103_all_quartet_tunneling.json','data/w33_20261102_chiral_surface_development.json','data/w33_20261102_deck_monodromy_network.json','data/w33_20261103_deck_cocycle_symmetry_selection.json','data/w33_20261103_vacuum_effective_quantum_audit.json']
def main():
    env=dict(os.environ,PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONIOENCODING='utf-8')
    def run(args):
        t=time.monotonic();p=subprocess.run(args,cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=240)
        row=dict(command=args,exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr,seconds=round(time.monotonic()-t,3));print(args[-1],p.returncode,p.stdout[-1200:],p.stderr[-800:],flush=True);return row
    before={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()for p in INPUTS}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:
        rows=list(pool.map(run,[[sys.executable,'-u',f'analysis/w33_20261103_{stem}.py']for stem in STEMS]))
    test=run([sys.executable,'-m','pytest','-q','--noconftest','tests/test_w33_20261103_five_constructive_fronts.py'])
    assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in before.items())
    passed=all(r['exit_code']==0 for r in rows) and test['exit_code']==0
    out=dict(status='PASS_SIX_REGENERATED_PRODUCERS_AND_INDEPENDENT_PYTEST'if passed else 'FAIL_FIVE_CONSTRUCTIVE_VALIDATION',utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        producers=rows,pytest=test,input_raw_sha256=before,
        earlier_run='Initial replay: all5 producers passed,25 tests passed and one wording-only test failed because it searched for a word absent from a metadata sentence. That check was replaced with a symbolic scaling-gradient calculation before this replay. No scientific certificate changed for that test repair.',
        independent_server=json.loads((ROOT/'data/w33_20261103_kagome_server_crosscheck.json').read_text()),
        generated_raw_sha256={f'data/w33_20261103_{stem}.json':hashlib.sha256((ROOT/f'data/w33_20261103_{stem}.json').read_bytes()).hexdigest()for stem in STEMS},
        scope='Five declared-model investigations with exact arithmetic and independent checks. Global repository conftest intentionally excluded; no all-repository test or completed TOE claim.')
    (ROOT/'data/w33_20261103_five_constructive_validation.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8');print(out['status'],flush=True);assert passed
if __name__=='__main__':main()
