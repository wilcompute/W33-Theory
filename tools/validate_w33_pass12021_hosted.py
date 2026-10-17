"""Exact-source hosted replay receipt; gh calls are read-only, not Git operations."""
from pathlib import Path
import argparse,hashlib,json,math,re,subprocess,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
SCIENCE='6b89e290bccdd832fb557c7d96b9580c669ba0fb';RUN=39076743318
CERT='w33_pass12021_12025_uv_curvature_threshold_holonomy.json'
FILES=['.github/workflows/pass12021-12025-uv-curvature.yml','analysis/PASS12021_12025_UV_CURVATURE_THRESHOLDS_AND_HOLONOMY.md','analysis/w33_pass12021_12025_uv_curvature_threshold_holonomy.py','data/'+CERT,'docs/index.html','tests/test_w33_pass12021_12025_uv_curvature_threshold_holonomy.py']
def gh(*args):return subprocess.check_output(['gh',*args],text=True)
def compare(a,b):
    import w33_pass12021_12025_uv_curvature_threshold_holonomy as q
    counts=dict(exact=0,numeric=0);fits=[]
    for name,obj in [('local',a),('hosted',b)]:
        data=obj['pass12024'];r=float(max(abs(q.matched_residual(np.array(data['charged_parameters'])))));assert r<1e-6
        nu=float(max(abs(q.matched_neutrino(np.array(data['neutrino_parameters']))/q.old.NEUTRINO_TARGET-1)));assert nu<1e-7
        records=[]
        for row in data['threshold_refits']:
            err=float(max(abs(q.matched_residual(np.array(row['parameters']),row['mu_GeV']))));assert err<1e-6;records.append(dict(mu_GeV=row['mu_GeV'],max_log_residual=err))
        fits.append(dict(source=name,charged_max_log_residual=r,neutrino_max_relative_error=nu,thresholds=records))
    coordinate_paths=[]
    def walk(a,b,key=''):
        assert type(a)==type(b),(key,'type')
        if isinstance(a,dict):
            assert a.keys()==b.keys(),(key,'keys')
            for k in a:walk(a[k],b[k],key+'/'+k)
        elif isinstance(a,list):
            assert len(a)==len(b),(key,'length')
            if key in ['/pass12024/charged_parameters','/pass12024/neutrino_parameters'] or ('/pass12024/threshold_refits/' in key and key.endswith('/parameters')):
                coordinate_paths.append(key);return
            for i,(x,y) in enumerate(zip(a,b)):walk(x,y,key+'/'+str(i))
        elif isinstance(a,float):assert math.isclose(a,b,rel_tol=1e-7,abs_tol=1e-10),(key,a,b);counts['numeric']+=1
        else:assert a==b,(key,a,b);counts['exact']+=1
    walk(a,b)
    return dict(status='PASS',leaf_counts=counts,relative_tolerance=1e-7,absolute_tolerance=1e-10,fit_coordinates_checked_by_independent_residuals=coordinate_paths,independent_fit_checks=fits)
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--artifact',type=Path,required=True);parser.add_argument('--local-log',type=Path,required=True);args=parser.parse_args()
    run=json.loads(gh('run','view',str(RUN),'--json','headSha,conclusion,jobs,url'));assert run['headSha']==SCIENCE and run['conclusion']=='success'
    log=gh('run','view',str(RUN),'--log');assert '30 passed' in log and '15 passed' in log
    local_log=args.local_log.read_bytes();assert b'30 passed' in local_log
    local=ROOT/'data'/CERT;host=args.artifact/CERT;comparison=compare(json.loads(local.read_text()),json.loads(host.read_text()))
    tree=json.loads(gh('api',f'repos/wilcompute/W33-Theory/git/trees/{SCIENCE}?recursive=1'));assert not tree['truncated'];blobs={x['path']:x['sha'] for x in tree['tree'] if x['type']=='blob'};files={}
    for name in FILES:
        raw=(ROOT/name).read_bytes();lf=raw.replace(b'\r\n',b'\n');blob=hashlib.sha1(b'blob '+str(len(lf)).encode()+b'\0'+lf).hexdigest();assert blob==blobs[name],name
        files[name]=dict(worktree_sha256=hashlib.sha256(raw).hexdigest(),LF_sha256=hashlib.sha256(lf).hexdigest(),verified_science_blob=blob)
    index=(ROOT/'RESULTS_INDEX.md').read_text();m=re.search(r'Indexed \*\*(\d+)\*\* files; \*\*(\d+)\*\* distinctive',index);assert m
    out=dict(status='PASS',date='2026-10-17',science_commit=SCIENCE,hosted_run=RUN,hosted_url=run['url'],hosted_conclusion=run['conclusion'],hosted_frozen_tests=30,hosted_regenerated_tests=15,hosted_log_sha256=hashlib.sha256(log.encode()).hexdigest(),local_tests=30,local_log_sha256=hashlib.sha256(local_log).hexdigest(),artifact_sha256=hashlib.sha256(host.read_bytes()).hexdigest(),artifact_byte_identical=local.read_bytes()==host.read_bytes(),artifact_comparison=comparison,science_files=files,results_index=dict(files=int(m[1]),distinctive=int(m[2])),scope='Exact named finite-operator and classical-vacuum results plus conditional EFT/native recovery constructions. Engineered targets/spectrum are inputs. Full softRG and precision thresholds, coefficient/modulus selection, nonlinear native GR and a global native chiral measure remain open.')
    (ROOT/'data/w33_pass12021_12025_validation.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS:6 science blobs,30local,30+15hosted, regenerated certificate and independent matching residuals')
if __name__=='__main__':main()
