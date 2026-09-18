#!/usr/bin/env python3
"""Cross-repo closure: the heterotic gauge qutrit lives in A8=sl9, not E6.

Inputs frozen on the two tracks:
  Holotrade 1cde1f14aa63efa599cb50e07aae935573ad3718
    No three-qutrit Pauli group acts on the E6 27 while preserving the E6
    cubic up to scale.  Simple Pauli-spanned algebras in the relevant ladder
    are sl3, sl9, sl27; 78 is excluded and 80=dim sl9 is allowed.

  Holotrade 8357f0ebc4230ad47430aac272863013db422786
    In the recorded W33-class Z6-I Standard Model SM_20260917_3, the single
    order-three Wilson line grades the local A8=su9 roots as 24+24+24, with
    neutral subsystem A4+A1+A1.  Its SU9 holonomy therefore has defining
    multiplicities 5+2+2 and is projectively SU9-conjugate to qutrit CZ_3.

  W33-Theory:
    PASS20260915_e8_a8_pauli_grading_closure.md identifies A8=sl9 with the
    fine two-qutrit Pauli grading up to graded equivalence.
    PART_BT2757... certifies the conjugate SUM/CX Clifford class on W33:
    point cycles 1^4 3^12 with four fixed points on one isotropic line.

This file welds those facts and re-verifies the finite algebra needed on the
W33 side.  The conclusion is deliberately narrower than the old six-qutrit
carrier language:

  * C^27_fixed tensor C^27_E6 has dimension 729 and remains an exact carrier
    intertwiner.
  * the three fixed-point/flavour qutrits remain physical on the geometry side;
  * E6 does NOT furnish three gauge qutrits;
  * the W33 A8=SU9 gauge sector DOES furnish the canonical two-qutrit Pauli
    algebra, and the actual viable flagship Wilson line selects the entangling
    CZ_3 Clifford conjugacy class.

Thus the native qutrit gauge register is SU9/sl9, not the E6 27.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_heterotic_flagship_cz_clifford_bridge.json'

HT_E6_SHA='1cde1f14aa63efa599cb50e07aae935573ad3718'
HT_CZ_SHA='8357f0ebc4230ad47430aac272863013db422786'

def mm(A,B):
    return tuple(tuple(sum(A[i][k]*B[k][j] for k in range(4))%3 for j in range(4)) for i in range(4))
def mpow(A,n):
    I=((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1)); out=I
    for _ in range(n): out=mm(out,A)
    return out
def canon(v):
    v=tuple(x%3 for x in v); nz=next(x for x in v if x)
    return tuple((2*x)%3 for x in v) if nz==2 else v
def symp(v,w):
    return (v[0]*w[2]+v[1]*w[3]-v[2]*w[0]-v[3]*w[1])%3

def main(write=True):
    # Local W33 certificates.
    a8=json.loads((ROOT/'data/w33_e8_a8_pauli_support_bridge.json').read_text())
    cx=json.loads((ROOT/'data/PART_BT2757_QUTRIT_CX_W33_LAGRANGIAN_UNIPOTENT_results.json').read_text())
    carrier=json.loads((ROOT/'data/w33_heterotic_z3_729_matter_carrier.json').read_text())
    firewall=json.loads((ROOT/'data/w33_e6_gauge_three_qutrit_pauli_firewall.json').read_text())

    assert a8['status']=='PASS'
    assert a8['checks']['80_oriented_root_orbits']
    assert a8['checks']['two_qutrit_pauli_pair_census_matches']
    assert cx['all_checks_pass']
    assert cx['w33']['point_cycle_profile']=={'1':4,'3':12}
    assert cx['w33']['fixed_points_are_one_isotropic_line']
    assert cx['generator_closure']['group']=='Sp(4,3)'
    assert cx['generator_closure']['order']==51840
    assert carrier['basis_intertwiner']['dimension']==729
    assert firewall['status']=='PASS_MONOMIAL_THREE_QUTRIT_REALIZATION_NO_GO'

    # Independent dimension firewall imported from Holotrade's complete theorem.
    achievable=set()
    for dU in range(2,7):
        for dR in range(dU+1):
            if dU==dR or (dU-dR)%2: continue
            achievable.add(3**dU-3**dR)
    expected={8,24,72,80,216,240,648,720,728}
    assert achievable==expected
    assert 78 not in achievable and 80 in achievable

    # CZ finite action, and Fourier conjugacy to the already-certified SUM class.
    CZ=((1,0,0,0),(0,1,0,0),(0,1,1,0),(1,0,0,1))
    F2=((1,0,0,0),(0,0,0,1),(0,0,1,0),(0,2,0,0))
    SUM=((1,0,0,0),(1,1,0,0),(0,0,1,2),(0,0,0,1))
    assert mpow(CZ,3)==((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1))
    assert mm(mm(mpow(F2,3),SUM),F2)==CZ

    P=sorted({canon(v) for v in itertools.product(range(3),repeat=4) if any(v)})
    idx={p:i for i,p in enumerate(P)}
    perm=[]
    for p in P:
        q=tuple(sum(CZ[i][j]*p[j] for j in range(4))%3 for i in range(4))
        perm.append(idx[canon(q)])
    seen=set(); cyc=Counter(); fixed=[]
    for i in range(40):
        if i in seen: continue
        u=i; orb=[]
        while u not in seen:
            seen.add(u);orb.append(u);u=perm[u]
        cyc[len(orb)]+=1
        if len(orb)==1: fixed.append(P[orb[0]])
    assert cyc==Counter({3:12,1:4})
    assert all(symp(a,b)==0 for a,b in itertools.combinations(fixed,2))

    # Adjoint grading from a 5+2+2 order-three spectrum.
    mult=(5,2,2)
    adj=[sum(mult[i]*mult[(i-g)%3] for i in range(3)) for g in range(3)]
    assert adj==[33,24,24]
    sl9=[adj[0]-1,adj[1],adj[2]]
    assert sl9==[32,24,24]

    # Explicit charged-sector decomposition under V0(5), V1(2), V2(2).
    # grade +1: Hom(V0,V1)+Hom(V1,V2)+Hom(V2,V0) = 10+4+10.
    plus=[mult[0]*mult[1],mult[1]*mult[2],mult[2]*mult[0]]
    minus=[mult[1]*mult[0],mult[2]*mult[1],mult[0]*mult[2]]
    assert plus==[10,4,10] and sum(plus)==24
    assert minus==[10,4,10] and sum(minus)==24

    checks={
      'carrier_729_survives_as_vector_space_intertwiner':True,
      'complete_E6_pauli_dimension_firewall_78_excluded':78 not in achievable,
      'A8_sl9_dimension_80_is_pauli_native':80 in achievable,
      'repo_A8_support_is_two_qutrit_pauli':a8['checks']['two_qutrit_pauli_pair_census_matches'],
      'flagship_import_root_grading_24_24_24':True,
      'flagship_import_neutral_A4_A1_A1':True,
      'CZ_spectrum_5_2_2_gives_sl9_32_24_24':sl9==[32,24,24],
      'charged_grade_decomposes_10_4_10':plus==[10,4,10],
      'CZ_is_Fourier_conjugate_to_SUM':True,
      'CZ_W33_profile_1pow4_3pow12':cyc==Counter({3:12,1:4}),
      'CZ_fixed_four_are_one_isotropic_line':True,
      'SUM_parent_certificate_matches_same_W33_profile':cx['w33']['point_cycle_profile']=={'1':4,'3':12},
    }
    assert all(checks.values())

    out={
      'schema':'w33.heterotic_flagship_cz_clifford_bridge.v1',
      'status':'PASS',
      'headline':(
        'The heterotic qutrit gauge register migrates from E6 to A8=SU9: the '
        'complete Pauli firewall excludes dim(E6)=78 from any three-qutrit '
        'Pauli-stable simple algebra, while sl9 (dim 80) is exactly the W33 '
        'two-qutrit Pauli algebra.  In the actual W33-class Standard-Model '
        'flagship, the order-three Wilson line has 5+2+2 SU9 spectrum and is '
        'projectively conjugate to qutrit CZ_3, whose W33 action is 1^4 3^12 '
        'with one fixed isotropic line.'
      ),
      'parallel_inputs':{
        'holotrade_complete_E6_no_go':HT_E6_SHA,
        'holotrade_flagship_CZ_certificate':HT_CZ_SHA,
        'w33_A8_pauli_support':'data/w33_e8_a8_pauli_support_bridge.json',
        'w33_SUM_fixed_geometry':'data/PART_BT2757_QUTRIT_CX_W33_LAGRANGIAN_UNIPOTENT_results.json',
      },
      'negative_branch':{
        'E6_dimension':78,
        'achievable_connected_Pauli_component_sizes':sorted(achievable),
        'three_qutrit_E6_action':'excluded, including nonmonomial/projective actions preserving the cubic up to scale',
      },
      'positive_branch':{
        'native_gauge_algebra':'sl9 = A8 = local SU9',
        'dimension':80,
        'register':'two qutrits',
        'flagship_model':'SM_20260917_3',
        'wilson_line_projective_class':'CZ_3',
        'fundamental_multiplicities':[5,2,2],
        'sl9_Z3_grading':[32,24,24],
        'neutral_centralizer':'S(U(5) x U(2) x U(2))',
        'charged_grade_plus':'Hom(5,2) + Hom(2,2) + Hom(2,5) = 10 + 4 + 10 = 24',
        'charged_grade_minus':'dual 10 + 4 + 10 = 24',
        'W33_point_cycles':{'fixed':4,'three_cycles':12},
        'fixed_geometry':'one isotropic W33 line',
        'Clifford_relation':'CZ = F_target^{-1} SUM F_target',
      },
      'revised_729_reading':{
        'exact':'C^27_fixed tensor C^27_E6 has dimension 729 and the stored F3^6 basis is a valid carrier-level coordinate system',
        'physical_qutrits_certified':'three geometric/fixed-point flavour qutrits; separately, the W33 A8 gauge algebra is a native two-qutrit operator algebra',
        'not_certified':'a physical six-qutrit tensor factorization with three gauge-side qutrits on the E6 27',
      },
      'scope':(
        'The projective CZ identification is a conjugacy-class statement.  A '
        'preferred simultaneous identification between the heterotic Wilson-line '
        'eigenbasis and the repository canonical fine-Pauli basis is not fixed. '
        'No claim is made that the five flagship cubic top couplings equal the '
        'five CZ phase-zero computational states.'
      ),
      'checks':checks,
    }
    if write: OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
    return out

if __name__=='__main__':
    main(True)
