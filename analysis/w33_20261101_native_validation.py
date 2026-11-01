import pathlib,subprocess,sys,json,time,concurrent.futures,hashlib,platform,io,unittest,os
R=pathlib.Path(__file__).resolve().parents[1];os.chdir(R);sys.path.insert(0,str(R));sys.path.insert(0,str(R/'tests'));sys.path.insert(0,str(R/'analysis'))
stem='w33_20261101_native_five_fronts_validation';log=R/'data'/f'{stem}.log';records=[]
def run(name):
 t=time.time();p=subprocess.run([sys.executable,str(R/'analysis'/name)],cwd=R,capture_output=True,text=True,encoding='utf-8',errors='replace')
 return dict(command=[sys.executable,'analysis/'+name],exit_code=p.returncode,seconds=time.time()-t,output=p.stdout+p.stderr)
def record(r):
 records.append(r);print(json.dumps(r),flush=True)
 with log.open('a',encoding='utf-8')as f:f.write(json.dumps(r)+'\n')
 if r['exit_code']:raise SystemExit(r['exit_code'])
if '--tests-only' in sys.argv:
 records=[json.loads(s) for s in log.read_text(encoding='utf-8').splitlines()]
else:
 log.write_text('',encoding='utf-8')
 record(run('w33_20261101_frame_tomography_octahedron.py'))
 with concurrent.futures.ThreadPoolExecutor(max_workers=2)as pool:
  for r in pool.map(run,['w33_20261101_parent_control_quantum_geometry.py','w33_20261101_common_cubic_spinor_extension.py']):record(r)
loader=unittest.TestLoader();suite=unittest.TestSuite()
for pat in ['test_w33_20261031*.py','test_tick_loop_rigidity.py','test_chiral_tetrahedron_strange_bridge.py','test_w33_20261101_native_five_fronts.py']:
 suite.addTests(loader.discover(str(R/'tests'),pattern=pat))
count=suite.countTestCases();print('DISCOVERED',count,'LOADER_ERRORS',loader.errors,flush=True);assert not loader.errors and count==75,(count,loader.errors)
buf=io.StringIO();t=time.time();result=unittest.TextTestRunner(stream=buf,verbosity=2).run(suite)
record(dict(command=['unittest connected suite',count],exit_code=0 if result.wasSuccessful()else 1,seconds=time.time()-t,output=buf.getvalue()))
manifest=dict(status='PASS',test_count=count,host=platform.node(),python=sys.version,records=records,
 scope='Three producers regenerated, followed by the recorded number of connected unit tests. No claim of complete repository testing or complete weekly/PDF reading.')
(R/'data'/f'{stem}.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('VALIDATION PASS',count,flush=True)
