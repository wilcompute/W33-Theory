"""Bind hosted replay and compare H27 zero-mode actions up to unitary basis.

Usage: python tools/validate_w33_pass12011_hosted.py --artifact DIR --local-log LOG
Read-only GitHub API/Actions calls use gh; no Git operations are performed.
"""
from pathlib import Path
import argparse,hashlib,itertools,json,math,subprocess
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
SCIENCE='983e6354c5f05bcc5b1ce5cf5666d608718df119'
RUN=39056922853
FILES=['.github/workflows/pass12011-12015-scale-flavour.yml','analysis/PASS12011_12015_SCALE_FLAVOUR_AND_INTERNAL_INDEX.md','analysis/w33_pass12011_12015_scale_flavour_internal_index.py','analysis/w33_pass12011_common_scale_search.py','data/w33_pass12011_12015_scale_flavour_internal_index.json','data/w33_pass12011_common_scale_search_record.json','docs/index.html','tests/test_w33_pass12011_12015_scale_flavour_internal_index.py']
CERT='w33_pass12011_12015_scale_flavour_internal_index.json'

def gh(*args):return subprocess.check_output(['gh',*args],text=True)

def matrix(data,name):return np.array(data[name+'_real'])+1j*np.array(data[name+'_imag'])

def canonical_frame(x,y):
    val,V=np.linalg.eig(x);v=V[:,np.argmin(abs(val-1))];v/=np.linalg.norm(v)
    F=np.column_stack([v,y@v,y@y@v]);assert np.linalg.norm(F.conj().T@F-np.eye(3))<1e-10
    expected=np.diag(np.exp(-2j*np.pi*np.arange(3)/3))
    assert np.linalg.norm(F.conj().T@x@F-expected)<1e-10
    return F

def compare(local,hosted):
    a=local['pass12015'];b=hosted['pass12015'];xl,yl=matrix(a,'X'),matrix(a,'Y');xh,yh=matrix(b,'X'),matrix(b,'Y')
    W=canonical_frame(xh,yh)@canonical_frame(xl,yl).conj().T
    errors={'unitarity':float(np.linalg.norm(W.conj().T@W-np.eye(3))),'X_intertwining':float(np.linalg.norm(xh-W@xl@W.conj().T)),'Y_intertwining':float(np.linalg.norm(yh-W@yl@W.conj().T))}
    assert max(errors.values())<1e-10
    counts={'exact_leaves':0,'floats':0,'finite_difference_Jacobian_floats':0};skipped=[]
    def walk(a,b,key=''):
        assert type(a)==type(b),(key,'type mismatch')
        if isinstance(a,dict):
            assert a.keys()==b.keys(),(key,'key mismatch')
            for k in a:
                if key=='/pass12015' and k in ('X_real','X_imag','Y_real','Y_imag'):skipped.append(key+'/'+k);continue
                walk(a[k],b[k],key+'/'+k)
        elif isinstance(a,list):
            assert len(a)==len(b),(key,'length mismatch')
            for i,(x,y) in enumerate(zip(a,b)):walk(x,y,key+'/'+str(i))
        elif isinstance(a,float):
            fd='Jacobian_singular_values' in key;counts['finite_difference_Jacobian_floats' if fd else 'floats']+=1
            assert math.isclose(a,b,rel_tol=1e-4 if fd else 1e-7,abs_tol=1e-11),(key,a,b)
        else:counts['exact_leaves']+=1;assert a==b,(key,a,b)
    walk(local,hosted)
    return dict(status='PASS',leaf_counts=counts,relative_tolerance=1e-7,absolute_tolerance=1e-11,finite_difference_Jacobian_relative_tolerance=1e-4,basis_dependent_fields_compared_by_intertwiner=skipped,unitary_intertwiner_real=W.real.tolist(),unitary_intertwiner_imag=W.imag.tolist(),intertwiner_errors=errors)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--artifact',type=Path,required=True);parser.add_argument('--local-log',type=Path);args=parser.parse_args()
    run=json.loads(gh('run','view',str(RUN),'--json','headSha,conclusion,jobs,url'));assert run['headSha']==SCIENCE and run['conclusion']=='success'
    log=gh('run','view',str(RUN),'--log');assert '27 passed' in log and '11 passed' in log
    local_path=ROOT/'data'/CERT;host_path=args.artifact/CERT
    comparison=compare(json.loads(local_path.read_text()),json.loads(host_path.read_text()))
    tree=json.loads(gh('api',f'repos/wilcompute/W33-Theory/git/trees/{SCIENCE}?recursive=1'));assert not tree['truncated'];blobs={x['path']:x['sha'] for x in tree['tree'] if x['type']=='blob'};files={}
    for name in FILES:
        raw=(ROOT/name).read_bytes();lf=raw.replace(b'\r\n',b'\n');blob=hashlib.sha1(b'blob '+str(len(lf)).encode()+b'\0'+lf).hexdigest();assert blob==blobs[name],name
        files[name]=dict(worktree_sha256=hashlib.sha256(raw).hexdigest(),LF_sha256=hashlib.sha256(lf).hexdigest(),verified_science_blob=blob)
    local_validation='not supplied'
    if args.local_log:
        raw=args.local_log.read_bytes();assert b'27 passed' in raw;local_validation=dict(tests=27,log_sha256=hashlib.sha256(raw).hexdigest())
    search=json.loads((ROOT/'data/w33_pass12011_common_scale_search_record.json').read_text());assert search['status']=='PASS'
    out=dict(status='PASS',date='2026-10-17',science_commit=SCIENCE,hosted_run=RUN,hosted_url=run['url'],hosted_conclusion=run['conclusion'],hosted_jobs=[dict(id=j['databaseId'],conclusion=j['conclusion']) for j in run['jobs']],hosted_frozen_tests=27,hosted_regenerated_tests=11,hosted_log_sha256=hashlib.sha256(log.encode()).hexdigest(),local_validation=local_validation,artifact_sha256=hashlib.sha256(host_path.read_bytes()).hexdigest(),artifact_comparison=comparison,science_files=files,portable_search_max_log_residual=max(abs(x) for x in search['residual']),results_index=dict(files=12339,distinctive=16965,unique=7430),scope='Conditional research constructions: scale/texture parameters fitted; neutrino rematching, dynamical flavour/flux selection, gauge-invariant UV alignment, native gravity and native chiral measure remain open. External2610.09093v1 proof is not independently certified here.')
    path=ROOT/'data/w33_pass12011_12015_validation.json';path.write_text(json.dumps(out,indent=2)+'\n');print('PASS:8 science blobs,27+11 hosted tests, numeric artifacts and unitary H27 intertwiner',comparison['intertwiner_errors'])
if __name__=='__main__':main()
