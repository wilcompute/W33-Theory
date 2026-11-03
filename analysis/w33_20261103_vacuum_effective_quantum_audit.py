"""Exact F-flat chart and conditional strong-coupling audit of the native vacuum.

Classical cubic/Jordan rank-one geometry is established mathematics. Quantum
statements use supplied4D N=1 SU4 dynamics and Intriligator-Pouliot's Sp SQCD
superpotential, not a theorem inferred from finite group orders.
"""
import collections
import json
import pathlib
import sys

import sympy as s

ROOT=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261102_clifford_native_cubic_repair import cubic_terms,DUADS


def build():
    z=s.symbols('z:27')
    native=json.loads((ROOT/'data/w33_20261031_signed_cubic_lift.json').read_text())
    terms={tuple(r['triple']):r['coefficient'] for r in native['coefficient_rows']}
    W=sum(c*s.prod(z[i] for i in t) for t,c in terms.items());pivot=12
    vector=sorted({i for t in terms if pivot in t for i in t if i!=pivot})
    spinor=sorted(set(range(27))-{pivot}-set(vector))
    assert len(vector)==10 and len(spinor)==16
    assert all(len(set(t)&set(vector))==1 and len(set(t)&set(spinor))==2 for t in terms if pivot not in t)
    quad=s.diff(W,z[pivot]);J=s.hessian(quad,[z[i] for i in vector]);assert J.det()!=0
    B=s.Matrix([s.diff(W,x).subs({z[pivot]:0}) for x in [z[i] for i in vector]])
    dependent=-J.inv()*B/z[pivot]
    substitution={z[i]:x for i,x in zip(vector,dependent)}
    assert all(s.cancel(s.diff(W,x).subs(substitution,simultaneous=True))==0 for x in z)
    assert s.cancel(W.subs(substitution,simultaneous=True))==0
    oldvac=json.loads((ROOT/'data/w33_20261102_conditional_symplectic_vacuum.json').read_text())
    v=[0]*27
    for i,x in oldvac['native_VEV']:v[i]=x
    assert v[pivot]==1
    assert all(s.cancel(x.subs(dict(zip(z,v))))==v[z.index(i)] for i,x in substitution.items())
    # Independently identify the charged zero modes in the SL6 coordinates.
    model=sum(c*s.prod(z[i] for i in t) for t,c in cubic_terms().items())
    base=[0]*27
    for pair in [(0,2),(1,3)]:base[DUADS.index(pair)]=1
    base[19]=base[26]=1
    H=s.hessian(model,z).subs(dict(zip(z,base)))
    charged=[DUADS.index((i,j)) for j in [4,5] for i in range(4)]+list(range(15,19))+list(range(21,25))
    null=H.extract(charged,charged).nullspace();assert len(null)==8
    a,b=s.symbols('a b');weights=[a,b,-a,-b,0,0]
    charges=[weights[i]+weights[j] for i,j in DUADS]+[-x for x in weights]*2
    light_weights=[]
    for k in null:
        nonzero={charges[i] for i,x in zip(charged,k) if x};assert len(nonzero)==1
        light_weights.append(nonzero.pop())
    assert collections.Counter(light_weights)=={a:2,b:2,-a:2,-b:2}
    t,q,L,C=s.symbols('t q Lambda C',positive=True)
    # Scale matching is fixed only up to a nonzero threshold constant C.
    Wdyn=C*L**s.Rational(9,2)/(s.sqrt(t)*q)
    assert s.simplify(s.diff(Wdyn,t)/Wdyn)==-1/(2*t)
    assert s.simplify(s.diff(Wdyn,q)/Wdyn)==-1/q
    R=s.symbols('R',positive=True)
    assert s.simplify(Wdyn.subs({t:R*L,q:s.sqrt(R)*L}))==C*L**3/R
    return dict(status='PASS_NATIVE_F_FLAT_CHART_AND_CONDITIONAL_ADS_AUDIT',
        pivot_coordinate=pivot,free_spinor_coordinates=spinor,dependent_vector_coordinates=vector,
        rational_F_flat_chart=[[z.index(i),str(x)] for i,x in substitution.items()],chart_complex_dimension=17,
        all27_gradient_identities=True,tree_superpotential_on_chart='0 identically',
        charged_model_coordinates=charged,charged_null_basis=[list(map(str,k)) for k in null],
        light_USp4_fundamentals=2,Sp_SQCD_Nc=2,Sp_SQCD_Nf=1,neutral_light_chiral_fields=4,
        ultraviolet_one_loop_beta_coefficient=9,infrared_one_loop_beta_coefficient=8,
        quantum_assumptions=['4D global N=1 supersymmetry','only chosen SU4 is gauged','nonzero gauge coupling','weakly Higgsed large-t patch','standard Sp SQCD holomorphic dynamics','no additional stabilizing interactions'],
        quantum_effective_superpotential='Wdyn=kappa*(Lambda_low^8/M)^(1/2), kappa nonzero; M is the meson of the two light fundamentals. Intriligator-Pouliot eq5 includes a convention-dependent factor2 inside the root.',
        holomorphic_scale_matching='Lambda_low^8=C_threshold*Lambda_SU4^9/t along the one-scale branch, up to a nonzero threshold/scheme constant.',
        quantum_conclusion='The classical q=0 point lies at the ADS singularity. In this weakly Higgsed effective theory no finite nonzero meson is supersymmetrically stationary; no added tree superpotential stabilizes it. A hierarchical runaway t=R*Lambda, q=sqrt(R)*Lambda has q/t ->0 and Wdyn proportional1/R. This is a conditional obstruction to calling the previous classical family a selected stable vacuum.',
        perturbative_boundary='An exact17-parameter F-flat chart is proved, improving the former quadratic-zero-only statement. Perturbative superpotential nonrenormalization does not remove the nonperturbative ADS term. Kähler corrections, strong-coupling endpoints and vacua outside this patch are not classified.',
        reference='https://arxiv.org/abs/hep-th/9505006')


if __name__=='__main__':
    d=build();(ROOT/'data/w33_20261103_vacuum_effective_quantum_audit.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
    print(d['status'],d['chart_complex_dimension'],d['light_USp4_fundamentals'],flush=True)
