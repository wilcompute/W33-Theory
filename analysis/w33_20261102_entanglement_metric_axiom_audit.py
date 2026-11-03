"""A finite-state audit of a recent emergent-distance proposal.

arXiv2607.26035v1 section2 claims strong subadditivity ensures the triangle
inequality for -log(I/I0). This producer supplies full-rank counterexamples,
including one with every pairwise mutual information strictly positive.
It audits that implication, not every proposed information geometry.
"""
import itertools
import json
import pathlib

import numpy as np
import sympy as s

ROOT=pathlib.Path(__file__).resolve().parents[1]


def reduction(rho,keep):
    keep=tuple(keep);lost=[j for j in range(4) if j not in keep]
    out=s.zeros(2**len(keep))
    for a,b in itertools.product(range(16),repeat=2):
        if all((a>>j&1)==(b>>j&1) for j in lost):
            x=sum((a>>j&1)<<k for k,j in enumerate(keep));y=sum((b>>j&1)<<k for k,j in enumerate(keep))
            out[x,y]+=rho[a,b]
    return out


def entropy(rho):
    eigen=np.linalg.eigvalsh(np.array(rho,dtype=float))
    return float(-sum(x*np.log(x) for x in eigen if x>1e-15))


def build():
    # Bit order low to high. A={0}, B={1,2}, C={3}.
    bell=s.zeros(16,1)
    for a,b in itertools.product(range(2),repeat=2):bell[a+(a<<1)+(b<<2)+(b<<3)]=s.Rational(1,2)
    ghz=s.zeros(16,1);ghz[0]=ghz[15]=1/s.sqrt(2)
    rho=s.Rational(89,100)*(bell*bell.T)+s.Rational(1,100)*(ghz*ghz.T)+s.eye(16)/160
    assert s.trace(rho)==1 and rho==rho.T
    # rho >= I/160 by construction, so full rank is exact, not a tolerance test.
    subsystems={'A':[0],'B':[1,2],'C':[3],'AB':[0,1,2],'BC':[1,2,3],'AC':[0,3],'ABC':[0,1,2,3]}
    reduced={name:reduction(rho,keep) for name,keep in subsystems.items()}
    S={name:entropy(r) for name,r in reduced.items()}
    I={pair:S[pair[0]]+S[pair[1]]-S[pair] for pair in ['AB','BC','AC']}
    assert min(I.values())>0
    SSA=S['AB']+S['BC']-S['B']-S['ABC']
    assert SSA>0
    I0=4*np.log(2);distance={pair:float(-np.log(value/I0)) for pair,value in I.items()}
    margin=distance['AC']-distance['AB']-distance['BC']
    assert margin>5
    exact_AC=s.diag(s.Rational(101,400),s.Rational(99,400),s.Rational(99,400),s.Rational(101,400))
    assert reduced['AC']==exact_AC
    return dict(status='PASS_FINITE_MI_LOG_METRIC_COUNTEREXAMPLE',
        rho_rational=[[str(x) for x in row] for row in rho.tolist()],subsystems=subsystems,
        exact_full_rank_lower_bound='rho >= I16/160',entropy_nats=S,mutual_information_nats=I,
        strong_subadditivity_margin=SSA,normalization='I0=4 ln2',raw_log_distances=distance,
        triangle_violation_margin=margin,shortest_path_repaired_AC_distance=distance['AB']+distance['BC'],
        exact_AC_mutual_information='(101/200)*log(101/100)+(99/200)*log(99/100)',
        claim_audited='arXiv2607.26035v1 section2: strong subadditivity guarantees triangle inequality for raw -log(I/I0). The explicit positive, full-rank state satisfies SSA but violates that triangle inequality.',
        boundary='The failure concerns this unrestricted pairwise-distance implication. A shortest-path metric, a restricted state family or another information distance may be supplied. None alone derives a Lorentzian spacetime, Einstein equations or fractal scaling.')


if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261102_entanglement_metric_axiom_audit.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
    print(d['status'],d['mutual_information_nats'],d['triangle_violation_margin'],flush=True)
