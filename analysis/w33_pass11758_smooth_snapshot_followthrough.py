"""Run our independent Galerkin calculation on the parallel certified smoothX23.

The exact smoothness proof is5975f1cbc's work. This explicitly changes the
numerical input, rather than attaching its proof to the old prime polynomial.
"""
from contextlib import contextmanager
from pathlib import Path
import hashlib,json,sys
import sympy as s
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11758_metric_harmonic_galerkin as A
import w33_20261008_explicit_Klein_CY_smooth_proof as C
OUT=ROOT/'data/w33_pass11758_smooth_snapshot_followthrough.json'


def polynomial():
    z=s.symbols('z:4')
    F=s.expand(s.prod(1+x*x for x in z)+2*s.prod(1-x*x for x in z)+3*s.prod(2*x for x in z))
    return z,F,(),()


@contextmanager
def actual_smooth_input():
    # Only process-local functions/caches change, never files or prior certificates.
    old=A.Q.reference_polynomial
    caches=(A.polynomial_terms,A.reference_form_functions,A.Q.type2_forms,A.Q.type2_lift_certificate)
    try:
        for f in caches:f.cache_clear()
        A.Q.reference_polynomial=polynomial
        yield
    finally:
        A.Q.reference_polynomial=old
        for f in caches:f.cache_clear()


def payload():
    proof=C.main();assert proof['complex_geometric_smoothness_proven_by_three_case_derivative_elimination']
    with actual_smooth_input():
        inputs=A.Q.type2_lift_certificate();runs=[]
        for seed,n,support in ((51758,512,2),(71758,2048,4)):
            train=A.sample_hypersurface(seed,n);test=A.sample_hypersurface(seed+10000,n)
            c,metric=A.fit_metric(train,test,support);beta,hym=A.fit_hym(train,c,test)
            harmonic=A.fit_harmonic(train,test,c,beta)
            runs.append(dict(seed=seed,validation_seed=seed+10000,root_samples_each=2*n,
                polynomial_residual=max(train['polynomial_residual'],test['polynomial_residual']),
                metric=metric,HYM=hym,harmonic=harmonic))
    sources=[Path(A.__file__),Path(C.__file__),Path(A.Q.__file__)]
    return dict(status='PASS',schema='w33.pass11758.smooth_followthrough.v1',
        source_sha256=hashlib.sha256(Path(__file__).read_bytes().replace(b'\r\n',b'\n')).hexdigest(),
        inputs={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest() for p in sources},
        polynomial=str(polynomial()[1]),snapshot_global_smoothness_certified=True,
        smoothness_owner='5975f1cbc: w33_20261008_explicit_Klein_CY_smooth_proof.py',
        type2_input=inputs,runs=runs,physical_normalized_Yukawa_certified=False,
        boundary='The polynomial is explicitly changed to the certified smooth freeX23. Prior prime-polynomial residuals and rigidity cycles are not transferred to it. The three type112 bundle classes and their Dolbeault inputs are recomputed here. Finite-basis residuals, sampled positivity, quadrature convergence, full4D normalization, physical masses, anomaly-cycle representatives and a realistic vacuum remain separate checks.')


if __name__=='__main__':
    value=payload();OUT.write_text(json.dumps(value,indent=2)+'\n')
    print('11758 smooth snapshot follow-through PASS',flush=True)
    for r in value['runs']:
        print(r['root_samples_each'],r['metric']['validation'],r['HYM']['validation'],r['harmonic']['F_rescaling_invariant_geometry_proxy'],flush=True)
