"""Replay all eight producers and22 independent fixture-free pytest cases."""
import concurrent.futures
import datetime
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import time

ROOT=pathlib.Path(__file__).resolve().parents[1]
STEMS=['native_projector_holonomic_qutrit','vacuum_effective_quantum_audit','wd5_native_klein_intertwiner',
       'all_quartet_tunneling','induced_cubic_compression','deck_cocycle_symmetry_selection',
       'gauge_global_form_audit','clifford_yang_monopole_controls']
INPUTS=['data/w33_20261031_signed_cubic_lift.json','data/w33_20261031_unitary_stabilizer_lift.json',
        'data/w33_20261031_chiral_tetrahedron_strange_bridge.json','data/w33_20261031_tick_loop_rigidity.json',
        'data/w33_20261102_chiral_surface_development.json','data/w33_20261102_induced_cubic_common_cover.json',
        'data/w33_20261102_conditional_symplectic_vacuum.json','data/w33_20261102_clifford_native_cubic_repair.json',
        'data/w33_20261102_spin6_rotation_group_audit.json','data/w33_20261102_deck_monodromy_network.json']


def main():
    env=dict(os.environ,PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
    out=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
             input_raw_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in INPUTS},
             execution='Local Windows subprocesses, three independent producers concurrently; Remote Desktop Commander also executed initial probes/producers on the same authorized device.',jobs=[])
    def run(args):
        command=[sys.executable,'-u']+args;t=time.monotonic();print('START',args,flush=True)
        try:
            p=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=180)
            row=dict(command=command,exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr,seconds=round(time.monotonic()-t,3))
        except subprocess.TimeoutExpired as e:
            row=dict(command=command,exit_code=124,stdout=str(e.stdout or ''),stderr=str(e.stderr or ''),seconds=round(time.monotonic()-t,3))
        print('RESULT',args,row['exit_code'],row['seconds'],row['stdout'][-1000:],row['stderr'][-1200:],flush=True);return row
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        out['jobs']=list(pool.map(run,[[f'analysis/w33_20261103_{stem}.py'] for stem in STEMS]))
    path=ROOT/'data/w33_20261103_native_eight_validation.json'
    path.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    assert all(row['exit_code']==0 for row in out['jobs'])
    out['jobs'].append(run(['-m','pytest','-q','--noconftest','tests/test_w33_20261103_native_eight_investigations.py']))
    if out['jobs'][-1]['exit_code']==0:out['status']='PASS_EIGHT_PRODUCERS_AND_22_PYTEST_CASES'
    out['test_scope']='22 tests have no fixtures. --noconftest intentionally avoids repository-wide legacy fixture preparation and subprocess rewriting; no global integration pass is asserted.'
    assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==v for p,v in out['input_raw_sha256'].items())
    path.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    assert out.get('status')=='PASS_EIGHT_PRODUCERS_AND_22_PYTEST_CASES'
    print(out['status'],flush=True)


if __name__=='__main__':main()
