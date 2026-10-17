"""Bind the hosted replay to exact science blobs and compare regenerated results.

Read-only gh API/Actions calls; all actual Git operations use GitKraken.
The cancellation-noise diagnostic is not treated as a physical observable.
"""
from pathlib import Path
import argparse,hashlib,json,math,re,subprocess,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
SCIENCE='e808cb8dde1760b5bf119a4213f40967d4ec28ae'
RUN=39075291756
CERT='w33_pass12016_12020_neutrino_vacuum_native_measure.json'
FILES=['.github/workflows/pass12016-12020-neutrino-native.yml','analysis/PASS12016_12020_NEUTRINO_VACUUM_NATIVE_MEASURE.md','analysis/w33_pass12016_12020_neutrino_vacuum_native_measure.py','analysis/w33_pass12016_neutrino_search.py','data/'+CERT,'data/w33_pass12016_neutrino_search_record.json','docs/index.html','tests/test_w33_pass12016_12020_neutrino_vacuum_native_measure.py']
def gh(*args):return subprocess.check_output(['gh',*args],text=True)
def compare(local,hosted):
    from w33_pass12016_12020_neutrino_vacuum_native_measure import threshold_residual
    counts=dict(exact=0,floats=0);diagnostics={};threshold_checks=[]
    # Fit coordinates may drift along ill-conditioned directions. Independently
    # re-evaluate both fits; compare their physical scales and thresholds below.
    for name,obj in [('local',local),('hosted',hosted)]:
        for row in obj['pass12016']['threshold_refits']:
            residual=float(max(abs(threshold_residual(np.array(row['parameters']),row['universal_down_threshold']))));assert residual<1e-6
            threshold_checks.append(dict(source=name,delta=row['universal_down_threshold'],max_log_residual=residual))
    def walk(a,b,key=''):
        assert type(a)==type(b),(key,'type')
        if isinstance(a,dict):
            assert a.keys()==b.keys(),(key,'keys')
            for k in a:walk(a[k],b[k],key+'/'+k)
        elif isinstance(a,list):
            assert len(a)==len(b),(key,'length')
            if 'threshold_refits' in key and key.endswith('/parameters'):
                diagnostics[key]=dict(method='independent threshold residual check',local=a,hosted=b);return
            for i,(x,y) in enumerate(zip(a,b)):walk(x,y,key+'/'+str(i))
        elif isinstance(a,float):
            if key.endswith('/cross_spurion_finite_difference_noise'):
                assert math.isfinite(a) and math.isfinite(b);diagnostics[key]=dict(local=a,hosted=b,interpretation='finite difference cancellation noise, not a physical derivative');return
            rel=1e-5 if 'threshold_refits' in key else 1e-7
            absolute=1e-8 if 'threshold_refits' in key else 1e-10
            assert math.isclose(a,b,rel_tol=rel,abs_tol=absolute),(key,a,b);counts['floats']+=1
        else:assert a==b,(key,a,b);counts['exact']+=1
    walk(local,hosted)
    return dict(status='PASS',counts=counts,relative_tolerance=1e-7,absolute_tolerance=1e-10,threshold_relative_tolerance=1e-5,threshold_absolute_tolerance=1e-8,threshold_residual_checks=threshold_checks,independently_treated_diagnostics=diagnostics)
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--artifact',type=Path,required=True);parser.add_argument('--local-log',type=Path,required=True);args=parser.parse_args()
    run=json.loads(gh('run','view',str(RUN),'--json','headSha,conclusion,jobs,url'));assert run['headSha']==SCIENCE and run['conclusion']=='success'
    log=gh('run','view',str(RUN),'--log');assert '26 passed' in log and '15 passed' in log
    raw_local=args.local_log.read_bytes();assert b'26 passed' in raw_local
    lp=ROOT/'data'/CERT;hp=args.artifact/CERT
    comparison=compare(json.loads(lp.read_text()),json.loads(hp.read_text()))
    tree=json.loads(gh('api',f'repos/wilcompute/W33-Theory/git/trees/{SCIENCE}?recursive=1'));assert not tree['truncated'];blobs={x['path']:x['sha'] for x in tree['tree'] if x['type']=='blob'};files={}
    for name in FILES:
        raw=(ROOT/name).read_bytes();lf=raw.replace(b'\r\n',b'\n');blob=hashlib.sha1(b'blob '+str(len(lf)).encode()+b'\0'+lf).hexdigest();assert blob==blobs[name],name
        files[name]=dict(worktree_sha256=hashlib.sha256(raw).hexdigest(),LF_sha256=hashlib.sha256(lf).hexdigest(),verified_science_blob=blob)
    search=json.loads((ROOT/'data/w33_pass12016_neutrino_search_record.json').read_text());assert search['status']=='PASS';search_error=max(abs(x) for x in search['stages'][-1]['residual']);assert search_error<1e-7
    index=(ROOT/'RESULTS_INDEX.md').read_text();m=re.search(r'Indexed \*\*(\d+)\*\* files; \*\*(\d+)\*\* distinctive',index);assert m
    out=dict(status='PASS',date='2026-10-17',science_commit=SCIENCE,hosted_run=RUN,hosted_url=run['url'],hosted_conclusion=run['conclusion'],hosted_frozen_tests=26,hosted_regenerated_tests=15,hosted_log_sha256=hashlib.sha256(log.encode()).hexdigest(),local_tests=26,local_log_sha256=hashlib.sha256(raw_local).hexdigest(),artifact_sha256=hashlib.sha256(hp.read_bytes()).hexdigest(),artifact_comparison=comparison,science_files=files,portable_search_max_log_residual=search_error,results_index=dict(files=int(m[1]),distinctive=int(m[2])),scope='Conditional constructions and exact finite-operator statements. Fitted parameters and engineered potential coefficients are not predictions. Full SM/BSM threshold rematch, selected moduli/flux, complete radiative protection, curved native GR and global native measure remain open.')
    (ROOT/'data/w33_pass12016_12020_validation.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS:8 science blobs;26local,26+15hosted; regenerated numerical and exact artifacts')
if __name__=='__main__':main()
