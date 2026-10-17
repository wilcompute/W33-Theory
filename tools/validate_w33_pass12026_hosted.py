"""Bind four hosted certificates to exact science sources and physical fit checks.

Only read-only gh Actions/API calls; Git operations use GitKraken. Index/search
supplements written after the science commit are identified separately.
"""
from pathlib import Path
import argparse,hashlib,json,math,re,subprocess,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
SCIENCE='ee4f41ed6900e0ce41ca0096dc24eff79c2ce76a';RUN=39078651176
CERTS=['w33_pass12026_12033_theta_soft_threshold_connections.json','w33_pass12029_native_heat_curvature.json','w33_pass12029_native_heat_extended.json','w33_pass12030_native_determinant_torus.json']
FILES=['.github/workflows/pass12026-12033-theta-heat-topology.yml','analysis/PASS12026_12033_THETA_SOFT_HEAT_AND_DETERMINANT_TOPOLOGY.md','analysis/w33_pass12026_12033_theta_soft_threshold_connections.py','analysis/w33_pass12029_native_heat_curvature.py','analysis/w33_pass12030_native_determinant_torus.py','docs/index.html','tests/test_w33_pass12026_12033_physical_connections.py']+['data/'+x for x in CERTS]
def gh(*args):return subprocess.check_output(['gh',*args],text=True)
def compare(local,hosted,name):
    counts=dict(exact=0,numeric=0,finite_difference_diagnostics=0,free_fibre_observables=0);coordinate_paths=[];fits=[];step_checks=[]
    if name==CERTS[0]:
        import w33_pass12026_12033_theta_soft_threshold_connections as q
        x=q.MATCH[:10];full=lambda z:np.r_[z,q.MATCH[-1]]
        for step in [5e-6,1e-5,2e-5]:
            J=q.derivative(lambda z:q.mix_coordinates(full(z)),x,step);_,sv,Vh=np.linalg.svd(J,full_matrices=True)
            massJ=q.derivative(lambda z:np.log(q.p.shape_observables(q.p.theta_matrices(full(z))[:3])[1:5]),x,step);masssv=np.linalg.svd(massJ@Vh[4:].T,compute_uv=False)
            charged=np.linalg.svd(q.derivative(lambda z:q.residual(full(z)),x,step),compute_uv=False)
            assert sv[-1]>1e-3 and charged[-1]>1e-3
            step_checks.append(dict(step=step,mixing_singular_values=sv.tolist(),mass_on_null_singular_values=masssv.tolist(),charged_singular_values=charged.tolist()))
        for field in ['mixing_singular_values','mass_on_null_singular_values','charged_singular_values']:
            mid=np.array(step_checks[1][field]);assert max(np.max(abs(np.array(row[field])/mid-1)) for row in step_checks)<1e-3
        for source,obj in [('local',local),('hosted',hosted)]:
            r=float(max(abs(q.residual(np.array(obj['pass12028']['charged_parameters'])))));assert r<1e-7
            mix=[]
            for row in obj['pass12026']['fixed_orientation_continuations']:
                point=np.r_[row['parameters'],q.MATCH[-1]];value=float(max(abs(q.mix_coordinates(point)-q.mix_coordinates(q.MATCH))));assert value<1e-8
                V=q.orientation(point);invariants=q.prior.old.invariants(np.diag(q.prior.old.A_SPEC),V@np.diag(q.prior.old.B_SPEC)@V.conj().T);target=np.array(obj['pass12031']['retargeted_coefficients']);parent_error=float(max(abs(invariants-target)));assert parent_error<1e-8
                mix.append(dict(mixing_log_residual=value,actual_parent_invariant_error=parent_error))
            base_obs,_=q.neutrino(np.array(obj['pass12033']['base_parameters']));assert max(abs(base_obs/q.prior.old.NEUTRINO_TARGET-1))<1e-7
            nu=[]
            for row in obj['pass12033']['continuation']:
                obs,detail=q.neutrino(np.array(row['parameters']));err=float(max(abs(obs/q.prior.old.NEUTRINO_TARGET-1)));assert err<1e-7;nu.append(err)
                for key in ['m_beta_beta_eV','J']:assert math.isclose(detail[key],row[key],rel_tol=1e-7,abs_tol=1e-10)
                assert np.max(abs(np.array(detail['masses_eV'])-row['masses_eV']))<1e-10
            fits.append(dict(source=source,charged_max_log_residual=r,orientation_fibre_residuals=mix,neutrino_fibre_residuals=nu))
    def walk(a,b,key=''):
        assert type(a)==type(b),(name,key,'type')
        if isinstance(a,dict):
            assert a.keys()==b.keys(),(name,key,'keys')
            for k in a:walk(a[k],b[k],key+'/'+k)
        elif isinstance(a,list):
            assert len(a)==len(b),(name,key,'length')
            if name==CERTS[0] and (key=='/pass12033/base_parameters' or (key.endswith('/parameters') and ('fixed_orientation_continuations' in key or '/pass12033/continuation/' in key))):coordinate_paths.append(key);return
            for i,(x,y) in enumerate(zip(a,b)):walk(x,y,key+'/'+str(i))
        elif isinstance(a,float):
            finite_difference=name==CERTS[0] and any(label in key for label in ['Jacobian_singular_values','mass_response_on_null_singular_values'])
            free_fibre=name==CERTS[0] and ('mass_ratio_log_changes' in key or ('/pass12033/continuation/' in key and key.endswith('/J')))
            relative=1e-4 if finite_difference else (1e-6 if free_fibre else 1e-7)
            absolute=1e-8 if finite_difference else (1e-7 if 'mass_ratio_log_changes' in key else (1e-8 if free_fibre else 1e-10))
            assert math.isclose(a,b,rel_tol=relative,abs_tol=absolute),(name,key,a,b)
            counts['finite_difference_diagnostics' if finite_difference else ('free_fibre_observables' if free_fibre else 'numeric')]+=1
        else:assert a==b,(name,key,a,b);counts['exact']+=1
    walk(local,hosted)
    return dict(status='PASS',leaf_counts=counts,relative_tolerance=1e-7,absolute_tolerance=1e-10,fit_coordinates_independently_checked=coordinate_paths,physical_fit_checks=fits,finite_difference_step_checks=step_checks,finite_difference_relative_tolerance=1e-4,finite_difference_absolute_tolerance=1e-8,free_fibre_relative_tolerance=1e-6,free_fibre_J_absolute_tolerance=1e-8,free_fibre_mass_log_absolute_tolerance=1e-7)
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--artifact',type=Path,required=True);parser.add_argument('--local-log',type=Path,required=True);parser.add_argument('--focused-log',type=Path,required=True);args=parser.parse_args()
    run=json.loads(gh('run','view',str(RUN),'--json','headSha,conclusion,jobs,url'));assert run['headSha']==SCIENCE and run['conclusion']=='success'
    log=gh('run','view',str(RUN),'--log');assert '31 passed' in log and '16 passed' in log
    local_log=args.local_log.read_bytes();focused=args.focused_log.read_bytes();assert b'31 passed' in local_log and b'16 passed' in focused
    artifacts={}
    for name in CERTS:
        local=ROOT/'data'/name;host=args.artifact/name;artifacts[name]=dict(local_sha256=hashlib.sha256(local.read_bytes()).hexdigest(),hosted_sha256=hashlib.sha256(host.read_bytes()).hexdigest(),byte_identical=local.read_bytes()==host.read_bytes(),comparison=compare(json.loads(local.read_text()),json.loads(host.read_text()),name))
    tree=json.loads(gh('api',f'repos/wilcompute/W33-Theory/git/trees/{SCIENCE}?recursive=1'));assert not tree['truncated'];blobs={x['path']:x['sha'] for x in tree['tree'] if x['type']=='blob'};files={}
    for name in FILES:
        raw=(ROOT/name).read_bytes();lf=raw.replace(b'\r\n',b'\n');blob=hashlib.sha1(b'blob '+str(len(lf)).encode()+b'\0'+lf).hexdigest();assert blob==blobs[name],name
        files[name]=dict(worktree_sha256=hashlib.sha256(raw).hexdigest(),LF_sha256=hashlib.sha256(lf).hexdigest(),verified_science_blob=blob)
    search=json.loads((ROOT/'data/w33_pass12028_sqcd_search_record.json').read_text());assert search['status']=='PASS'
    import w33_pass12026_12033_theta_soft_threshold_connections as q
    search_err=float(max(abs(q.residual(np.array(search['parameters'])))));assert search_err<1e-7
    supplement={}
    for name in ['analysis/w33_pass12028_sqcd_search.py','data/w33_pass12028_sqcd_search_record.json']:
        raw=(ROOT/name).read_bytes();supplement[name]=dict(sha256=hashlib.sha256(raw).hexdigest(),validation='Separately executed local discovery replay after science SHA; not represented as hosted science source.')
    index=(ROOT/'RESULTS_INDEX.md').read_text();m=re.search(r'Indexed \*\*(\d+)\*\* files; \*\*(\d+)\*\* distinctive',index);assert m
    out=dict(status='PASS',date='2026-10-17',science_commit=SCIENCE,hosted_run=RUN,hosted_url=run['url'],hosted_conclusion=run['conclusion'],hosted_frozen_tests=31,hosted_regenerated_tests=16,hosted_log_sha256=hashlib.sha256(log.encode()).hexdigest(),local_combined_tests_before_chart_convention_cleanup=31,local_combined_log_sha256=hashlib.sha256(local_log).hexdigest(),local_focused_tests_after_cleanup=16,local_focused_log_sha256=hashlib.sha256(focused).hexdigest(),artifacts=artifacts,science_files=files,science_index_blob=blobs['RESULTS_INDEX.md'],current_results_index=dict(files=int(m[1]),distinctive=int(m[2]),sha256=hashlib.sha256((ROOT/'RESULTS_INDEX.md').read_bytes()).hexdigest()),local_discovery_supplement=supplement,local_discovery_replay_max_log_residual=search_err,scope='Exact linked-spurion and declared finite-operator results with conditional flavour/EFT/heat/topology investigations. Unselected coefficients, fullMSSMthresholds/softRG, nonlinear native GR and global native measure remain open; no complete TOE or parameter-free mass/constant prediction.')
    (ROOT/'data/w33_pass12026_12033_validation.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS:11 science blobs,4 artifacts,31+16 hosted;16 final local;physical fit checks;local discovery separately identified')
if __name__=='__main__':main()
