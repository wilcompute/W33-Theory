"""Replay three producers and44 connected tests; archive actual command output."""
import pathlib,sys,subprocess,json,time,concurrent.futures,unittest,io,platform,os
ROOT=pathlib.Path(__file__).resolve().parents[1]
def main():
    os.chdir(ROOT);sys.path.insert(0,str(ROOT));sys.path.insert(0,str(ROOT/'analysis'));sys.path.insert(0,str(ROOT/'tests'))
    records=[];log=ROOT/'data/w33_20261102_continuation_validation.log';log.write_text('',encoding='utf-8')
    def record(r):
        records.append(r)
        with log.open('a',encoding='utf-8')as f:f.write(json.dumps(r)+'\n')
        print(r['command'],r['exit_code'],r['seconds'],r['output'][-160:],flush=True)
        if r['exit_code']:raise SystemExit(r['exit_code'])
    def run(name):
        t=time.time();p=subprocess.run([sys.executable,str(ROOT/'analysis'/name)],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
        return dict(command=[sys.executable,'analysis/'+name],exit_code=p.returncode,seconds=time.time()-t,output=p.stdout+p.stderr)
    if '--tests-only' not in sys.argv:
        names=['w33_20261102_chiral_surface_development.py','w33_20261102_common_cover_interactions.py','w33_20261102_graded_parent_geometry.py']
        with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:
            for r in pool.map(run,names):record(r)
    loader=unittest.TestLoader();suite=unittest.TestSuite()
    for pattern in ['test_w33_20261102_topology_interactions_geometry.py','test_w33_20261101_native_five_fronts.py','test_tick_loop_rigidity.py','test_chiral_tetrahedron_strange_bridge.py']:
        suite.addTests(loader.discover(str(ROOT/'tests'),pattern=pattern))
    assert not loader.errors,loader.errors
    count=suite.countTestCases();assert count==44,count
    out=io.StringIO();t=time.time();result=unittest.TextTestRunner(stream=out,verbosity=2).run(suite)
    record(dict(command=['unittest connected patterns',count],exit_code=0 if result.wasSuccessful()else 1,seconds=time.time()-t,output=out.getvalue()))
    data=dict(status='PASS',test_count=count,host=platform.node(),python=sys.version,producer_regeneration='--tests-only'not in sys.argv,records=records)
    (ROOT/'data/w33_20261102_continuation_validation.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    print('PASS_VALIDATION',count,flush=True)
if __name__=='__main__':main()
