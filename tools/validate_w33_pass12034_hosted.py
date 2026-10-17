"""Compare the12034-12038 hosted artifact without confusing basis/error diagnostics.

Usage: python tools/validate_w33_pass12034_hosted.py artifact.json
Run metadata is specific to the observed successful science-commit workflow.
"""
from pathlib import Path
import argparse,hashlib,json,math
ROOT=Path(__file__).resolve().parents[1]
CERT='data/w33_pass12034_12038_joint_mechanisms.json'
SOURCES=['analysis/w33_pass12034_12038_joint_mechanisms.py',
'analysis/PASS12034_12038_JOINT_MECHANISM_TESTS.md',
 'tests/test_w33_pass12034_12038_joint_mechanisms.py',
 '.github/workflows/pass12034-12038-joint-mechanisms.yml','docs/index.html']

def validate(artifact):
    local=json.loads((ROOT/CERT).read_text());remote=json.loads(artifact.read_text())
    counts=dict(exact_leaves=0,numeric_leaves=0,diagnostic_numeric_leaves=0,covector_norms=0);mismatches=[]
    def compare(a,b,path='root'):
        if isinstance(a,dict):
            assert isinstance(b,dict) and set(a)==set(b),path
            for key in a:compare(a[key],b[key],path+'.'+key)
        elif isinstance(a,list):
            assert isinstance(b,list) and len(a)==len(b),path
            if path.endswith('.projected_gradient') or path.endswith('.projected_logQ_gradient_derivative'):
                assert all(math.isfinite(x) for x in a+b),path
                aa=math.sqrt(sum(x*x for x in a));bb=math.sqrt(sum(x*x for x in b));counts['covector_norms']+=1
                if not math.isclose(aa,bb,rel_tol=2e-6,abs_tol=1e-9):mismatches.append(path)
            else:
                for i,(aa,bb) in enumerate(zip(a,b)):compare(aa,bb,f'{path}[{i}]')
        elif isinstance(a,float):
            assert isinstance(b,(int,float)) and math.isfinite(a) and math.isfinite(b),path
            if 'error' in path.lower():counts['diagnostic_numeric_leaves']+=1
            else:
                counts['numeric_leaves']+=1
                if not math.isclose(a,b,rel_tol=2e-6,abs_tol=1e-9):mismatches.append(path)
        else:
            counts['exact_leaves']+=1
            if a!=b:mismatches.append(path)
    compare(local,remote);assert not mismatches,mismatches
    digest=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
    return dict(status='PASS',science_commit='584e022cda3fa6bb606b0a19fd772de86903d684',
        hosted_run=39080456008,hosted_job=117536159863,
        hosted_url='https://github.com/wilcompute/W33-Theory/actions/runs/39080456008',
        hosted_frozen_tests=33,hosted_frozen_seconds=13.69,hosted_regenerated_tests=17,hosted_regenerated_seconds=1.64,
        comparison=counts,numeric_relative_tolerance=2e-6,numeric_absolute_tolerance=1e-9,
        comparison_scope='All exact leaves and ordinary numeric leaves compared. SVD-null-basis covectors compared through their invariant norms, not arbitrary components. Numerical error diagnostics must be finite and passed the17 independent hosted tests; their roundoff values are not required equal. This is not a precision physical-data fit.',
        source_sha256={name:digest(ROOT/name) for name in SOURCES},
        local_certificate_sha256=digest(ROOT/CERT),hosted_certificate_sha256=digest(artifact),
        byte_identical=digest(ROOT/CERT)==digest(artifact),
        result_index=dict(files=12351,distinctive=17003,unique=7437,sha256=digest(ROOT/'RESULTS_INDEX.md')),
        validation_utility_sha256=digest(Path(__file__)))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('artifact',type=Path);parser.add_argument('--output',type=Path,default=ROOT/'data/w33_pass12034_12038_validation.json');args=parser.parse_args()
    result=validate(args.artifact);args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
