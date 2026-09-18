#!/usr/bin/env python3
"""All-q controlled-Z orbit/adjoint theorem for the W(3,q) two-qudit carrier.

Let q be prime and let
    CZ_q |x,y> = zeta^(xy) |x,y>
on C^q tensor C^q.  Its Clifford action on Pauli phase space
F_q^4 = (x1,x2,p1,p2) is
    (x1,x2,p1,p2) -> (x1,x2,p1+x2,p2+x1).

Three exact counting laws meet:

(1) FUNDAMENTAL SPECTRUM.
    The phase xy=0 has 2q-1 basis states.  Every nonzero phase a has q-1:
       q^2 = (2q-1) + (q-1)*(q-1).

(2) ADJOINT Z_q GRADING OF sl(q^2).
    If g_t is the eigenspace of Ad(CZ_q) with eigenvalue zeta^t, then
       dim g_0 = (q+1)(q^2-1),
       dim g_t = q(q^2-1)  for every t != 0.
    The charged dimension is exactly
       q(q^2-1) = |SL(2,q)|.

(3) ORBITS ON THE TWO-QUDIT PAULI GEOMETRY.
    N=CZ-I has N^2=0 and ker N has dimension 2.  Therefore the projective
    fixed set is PG(ker N)=PG(1,q), one totally isotropic line of q+1 points.
    Since CZ has order q in characteristic q, every other projective orbit has
    length q.  W(3,q) has v=(q+1)(q^2+1) points, so
       projective orbit profile = 1^(q+1) q^(q(q+1)).
    The number of nontrivial projective q-cycles is q(q+1), exactly the
    collinearity-graph valency k of GQ(q,q)=W(3,q).

    On all nonzero Pauli vectors there are q^2-1 fixed vectors and
       (q^4-q^2)/q = q(q^2-1) = |SL(2,q)|
    nontrivial q-cycles.  Thus the number of vector q-cycles is exactly the
    dimension of EACH nonzero adjoint grade.

At q=3:
    fundamental: 5+2+2
    sl9 grading: 32+24+24
    W33 points: 1^4 3^12
    nonzero Pauli vectors: 1^8 3^24
and 24 = |SL(2,3)| = the single-qutrit Clifford group modulo phase.

The q=3 zero-phase block gives the semisimple centralizer factor SU(5):
    S(U(5) x U(2) x U(2)),
matching the independently frozen heterotic flagship Wilson-line centralizer.

Literature boundary:
  generalized qudit Pauli/Clifford modular arithmetic is classical
  (Hostens-Dehaene-De Moor, quant-ph/0408190), and generalized CZ/SUM gates
  are standard.  The contribution frozen here is this explicit all-q weld of
  fundamental phase multiplicities, adjoint grade dimensions, W(3,q) orbit
  counts, graph valency, and |SL(2,q)|.

No continuum or Standard-Model claim follows for q != 3.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_allq_cz_orbit_adjoint_weld.json'

def canon(v,q):
    i=next(i for i,x in enumerate(v) if x%q)
    inv=pow(v[i]%q,-1,q)
    return tuple((x*inv)%q for x in v)

def cz(v,q):
    x1,x2,p1,p2=v
    return (x1,x2,(p1+x2)%q,(p2+x1)%q)

def cycles_on(items,act):
    idx={x:i for i,x in enumerate(items)}
    perm=[idx[act(x)] for x in items]
    seen=set(); c=Counter()
    for i in range(len(items)):
        if i in seen: continue
        u=i;n=0
        while u not in seen:
            seen.add(u);n+=1;u=perm[u]
        c[n]+=1
    return dict(sorted(c.items()))

def enumerate_q(q):
    phases=Counter((x*y)%q for x in range(q) for y in range(q))
    m=[phases[a] for a in range(q)]
    adj=[sum(m[a]*m[(a-t)%q] for a in range(q)) for t in range(q)]
    adj[0]-=1

    P=sorted({canon(v,q) for v in itertools.product(range(q),repeat=4) if any(v)})
    pcycles=cycles_on(P,lambda p: canon(cz(p,q),q))

    V=[v for v in itertools.product(range(q),repeat=4) if any(v)]
    vcycles=cycles_on(V,lambda v: cz(v,q))
    return {
      'q':q,
      'fundamental_phase_multiplicities':m,
      'sl_q2_adjoint_grades':adj,
      'projective_points':len(P),
      'projective_cycle_profile':pcycles,
      'nonzero_vectors':len(V),
      'vector_cycle_profile':vcycles,
    }

def main(write=True):
    qs=[2,3,5,7]
    rows=[enumerate_q(q) for q in qs]
    checks={}
    for r in rows:
        q=r['q']
        expected_m=[2*q-1]+[q-1]*(q-1)
        expected_adj=[(q+1)*(q*q-1)]+[q*(q*q-1)]*(q-1)
        expected_p={1:q+1,q:q*(q+1)}
        expected_v={1:q*q-1,q:q*(q*q-1)}
        checks[f'q{q}_fundamental_spectrum']=r['fundamental_phase_multiplicities']==expected_m
        checks[f'q{q}_adjoint_grading']=r['sl_q2_adjoint_grades']==expected_adj
        checks[f'q{q}_projective_cycles']=r['projective_cycle_profile']==expected_p
        checks[f'q{q}_vector_cycles']=r['vector_cycle_profile']==expected_v
        checks[f'q{q}_projective_count_W3q']=r['projective_points']==(q+1)*(q*q+1)
        checks[f'q{q}_charged_dim_eq_SL2q']=expected_adj[1]==q*(q*q-1)
        checks[f'q{q}_nontrivial_projective_cycles_eq_valency']=expected_p[q]==q*(q+1)
    assert all(checks.values())

    q=3
    zero=2*q-1
    charged=q*(q*q-1)
    neutral=(q+1)*(q*q-1)
    assert (zero,neutral,charged)==(5,32,24)

    out={
      'schema':'w33.allq_cz_orbit_adjoint_weld.v1',
      'status':'PASS',
      'headline':(
        'For prime q, two-qudit CZ_q simultaneously has fundamental phase '
        'multiplicities (2q-1,(q-1)^(q-1)), adjoint sl(q^2) grading '
        '((q+1)(q^2-1), [q(q^2-1)]^(q-1)), projective W(3,q) orbit profile '
        '1^(q+1) q^(q(q+1)), and nonzero-Pauli-vector profile '
        '1^(q^2-1) q^(q(q^2-1)). Thus the number of nontrivial projective '
        'cycles equals the W(3,q) valency k=q(q+1), while the number of '
        'nontrivial vector cycles equals each charged adjoint-grade dimension '
        'q(q^2-1)=|SL(2,q)|.'
      ),
      'theorem':{
        'fundamental_phase_multiplicities':'m_0=2q-1; m_a=q-1 for a!=0',
        'centralizer':'S(U(2q-1) x U(q-1)^(q-1))',
        'neutral_adjoint_dimension':'(q+1)(q^2-1)',
        'charged_adjoint_dimension':'q(q^2-1)=|SL(2,q)| for every nonzero grade',
        'W3q_projective_cycle_profile':'1^(q+1) q^(q(q+1))',
        'fixed_projective_geometry':'one totally isotropic line PG(1,q)',
        'nontrivial_projective_cycle_count':'q(q+1)=k, the GQ(q,q) collinearity valency',
        'nonzero_vector_cycle_profile':'1^(q^2-1) q^(q(q^2-1))',
        'nontrivial_vector_cycle_count':'q(q^2-1)=|SL(2,q)|=charged grade dimension',
      },
      'q3_specialization':{
        'fundamental_spectrum':[5,2,2],
        'centralizer':'S(U(5) x U(2) x U(2))',
        'contains_SU5_zero_phase_block':True,
        'sl9_grading':[32,24,24],
        'W33_point_cycles':{'1':4,'3':12},
        'W33_valency':12,
        'nonzero_Pauli_vector_cycles':{'1':8,'3':24},
        'SL2_3_order':24,
      },
      'enumerated_controls':rows,
      'literature_boundary':{
        'classical':'generalized Pauli/Clifford modular arithmetic and CZ/SUM gates',
        'reference':'Hostens, Dehaene, De Moor, quant-ph/0408190',
        'new_repo_weld':'the explicit equality of the CZ orbit counts, W(3,q) valency, adjoint grade dimensions, and |SL(2,q)|, plus the q=3 SU5 specialization',
      },
      'scope':'Exact finite theorem for prime q. The q=3 heterotic identification is supplied by the separate flagship certificate; no Standard-Model interpretation is asserted for other q.',
      'checks':checks,
    }
    if write: OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
    return out

if __name__=='__main__': main(True)
