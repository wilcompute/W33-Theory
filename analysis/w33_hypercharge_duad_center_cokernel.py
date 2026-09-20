#!/usr/bin/env python3
"""Explicit flagship hypercharge -> W33 duad gauge-sector intertwiner.

Parents:
  W33 data/w33_a5_duad_gauge_intertwiner.json
  W33 data/w33_e8_bracket_deficiency_formula.json
  W33 data/w33_qutrit_hamming_cz_frame_bundle.json
  Holotrade data/w33_flagship_a5_hypercharge_organizer.json
  Holotrade data/w33_flagship_global_u1_closure.json

Holotrade proves that the five Abelian directions left by the flagship global
A2+A1 are exactly the A5 root lattice, with
    Y = -omega_1(A5)
and
    L intersect Y^perp = A4.

W33 independently embeds Q(A5) in the 15-duad permutation carrier by
    Phi(x)_{ij}=x_i+x_j,
with Phi^T Phi = 4 C_A5 and image equal to the five-dimensional syntheme
incidence kernel.

Normalize the embedding:
    Psi = Phi/2.
Then Psi is an honest Euclidean isometry on the A5 real span.

In standard A5 coordinates
    Y=(-5,1,1,1,1,1)/6.
Therefore
    Psi(Y)_{0i}=-1/3     for the five duads through vertex 0,
    Psi(Y)_{ij}=+1/6     for the ten duads avoiding vertex 0.

Consequences:
* ||Psi(Y)||^2=5/6 and kY=5/3.
* every syntheme sum is zero;
* 6 Psi(Y) is the primitive integer pattern (-2)^5 (+1)^10;
* the exact stabilizer in S6 is the S5 fixing the distinguished vertex;
* the hypercharge-orthogonal A4 is x0=0, sum_{i=1}^5 x_i=0.
  On the five star coordinates y_i=Psi(x)_{0i}=x_i/2 this is simply
      sum_i y_i=0,
  and every non-star duad is reconstructed by
      Psi(x)_{ij}=y_i+y_j.
  Thus the four extra U(1) directions are exactly zero-sum star fluctuations.

The physical E8 holonomy bracket data give neutral sector dimension 16 and
self-bracket rank 11, hence cokernel dimension five.  This is precisely the
u(1)^5 center.  The A5 theorem refines that five-dimensional cokernel as
    Q*Y orthogonal_sum (A4 tensor Q),
so the desired low-energy reduction is algebraically
    16 = 11 + 1 + 4:
      su3+su2  + hypercharge + four extra Abelian directions.

Vacuum target:
  any singlet Higgs mechanism that preserves Y and removes all extra U(1)s
  must have charge projections spanning the rank-four A4 sector.  In duad-star
  coordinates this is a rank-four span inside {y in Q^5 : sum y_i=0}.

Firewall:
  the five-duad hypercharge star is NOT canonically the five-state CZ_3
  zero-phase cross.  Their natural set stabilizers in the certified carriers
  are S5 and D8 respectively.  Equal cardinality is not an intertwiner.
"""
from __future__ import annotations
import itertools, json
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_hypercharge_duad_center_cokernel.json'

V=tuple(range(6))
DUADS=list(itertools.combinations(V,2))
DIDX={e:i for i,e in enumerate(DUADS)}

def perfect_matchings(vertices):
    vertices=tuple(vertices)
    if not vertices:return [()]
    a=vertices[0];out=[]
    for j in range(1,len(vertices)):
        b=vertices[j]
        rest=vertices[1:j]+vertices[j+1:]
        for M in perfect_matchings(rest):
            out.append(tuple(sorted(((min(a,b),max(a,b)),)+M)))
    return sorted(set(out))

SYNTHEMES=perfect_matchings(V)

def psi(x):
    assert sum(x)==0
    return tuple((x[i]+x[j])/2 for i,j in DUADS)

def dot(a,b):return sum(x*y for x,y in zip(a,b))

def rank(M):
    A=[[F(x) for x in r] for r in M]
    if not A:return 0
    m,n=len(A),len(A[0]);rr=0
    for c in range(n):
        p=next((i for i in range(rr,m) if A[i][c]),None)
        if p is None:continue
        A[rr],A[p]=A[p],A[rr]
        z=A[rr][c];A[rr]=[x/z for x in A[rr]]
        for i in range(m):
            if i!=rr and A[i][c]:
                z=A[i][c];A[i]=[A[i][j]-z*A[rr][j] for j in range(n)]
        rr+=1
    return rr

def main(write=True):
    # Syntheme incidence.
    D=[[0]*15 for _ in SYNTHEMES]
    for r,M in enumerate(SYNTHEMES):
        for e in M:D[r][DIDX[e]]=1
    assert len(SYNTHEMES)==15 and rank(D)==10

    # Normalized A5 isometric embedding.
    simples=[]
    for i in range(5):
        x=[F(0)]*6;x[i]=1;x[i+1]=-1;simples.append(tuple(x))
    P=[psi(x) for x in simples]
    gram=[[dot(P[i],P[j]) for j in range(5)] for i in range(5)]
    cartan=[[2 if i==j else -1 if abs(i-j)==1 else 0 for j in range(5)] for i in range(5)]
    assert gram==cartan
    assert all(sum(D[r][k]*P[j][k] for k in range(15))==0
               for r in range(15) for j in range(5))
    assert rank([[P[j][i] for j in range(5)] for i in range(15)])==5

    # Hypercharge = -omega1.
    Y=(F(-5,6),)+(F(1,6),)*5
    y=psi(Y)
    star=[DIDX[(0,i)] for i in range(1,6)]
    nonstar=[i for i,e in enumerate(DUADS) if 0 not in e]
    assert all(y[i]==F(-1,3) for i in star)
    assert all(y[i]==F(1,6) for i in nonstar)
    assert dot(y,y)==F(5,6)
    assert [dot(y,P[i]) for i in range(5)]==[F(-1),0,0,0,0]
    assert all(sum(y[DIDX[e]] for e in M)==0 for M in SYNTHEMES)
    sixy=tuple(6*z for z in y)
    assert sorted(sixy)==[F(-2)]*5+[F(1)]*10

    # Order six in the A5 discriminant follows injectively from -omega1.
    # nY lies in Q(A5) iff all coordinates are integers; this first occurs at n=6.
    assert all(any((n*z).denominator!=1 for z in Y) for n in range(1,6))
    assert all((6*z).denominator==1 for z in Y)

    # A4 = Y-perp in Q(A5): x0=0, sum x1..x5=0.
    a4=[]
    for i in range(1,5):
        x=[F(0)]*6;x[i]=1;x[i+1]=-1;a4.append(tuple(x))
    A4P=[psi(x) for x in a4]
    a4gram=[[dot(A4P[i],A4P[j]) for j in range(4)] for i in range(4)]
    a4cartan=[[2 if i==j else -1 if abs(i-j)==1 else 0 for j in range(4)] for i in range(4)]
    assert a4gram==a4cartan
    assert all(dot(y,v)==0 for v in A4P)
    assert rank([[A4P[j][i] for j in range(4)] for i in range(15)])==4

    # Star reconstruction formula on the entire A4 span.
    for x in a4:
        z=psi(x)
        vals={i:z[DIDX[(0,i)]] for i in range(1,6)}
        assert sum(vals.values())==0
        for i,j in itertools.combinations(range(1,6),2):
            assert z[DIDX[(i,j)]]==vals[i]+vals[j]

    # S5 stabilizer: permutations fixing 0 preserve Y; any permutation moving
    # 0 changes the unique exceptional A5 coordinate and hence Y.
    fix0=0
    allst=0
    for p in itertools.permutations(V):
        Yp=tuple(Y[p.index(i)] for i in V)  # left permutation action
        if Yp==Y:
            allst+=1
            if p[0]==0:fix0+=1
    assert allst==fix0==120

    # Load exact W33 parents.
    parent=json.loads((ROOT/'data/w33_a5_duad_gauge_intertwiner.json').read_text())
    bracket=json.loads((ROOT/'data/w33_e8_bracket_deficiency_formula.json').read_text())
    frame=json.loads((ROOT/'data/w33_qutrit_hamming_cz_frame_bundle.json').read_text())
    assert parent['status']=='PASS_A5_DUAD_INTERTWINER'
    assert bracket['status']=='PASS_CLOSED_PROJECTIVE_DEFICIENCY_FORMULA'
    assert bracket['formula']['neutral'].startswith('(r,a)=(s,c)=(0,0): delta=5')
    assert frame['CZ_frame']['cross_stabilizer']=='D8'

    # Directly verify neutral target dim/rank from the full bracket tensor.
    tensor=json.loads((ROOT/'data/w33_e8_holonomy_bracket_rank_tensor.json').read_text())
    i=tensor['sector_order'].index('0,0,0')
    target_dim=int(tensor['sector_dimensions']['0,0,0'])
    self_rank=int(tensor['rank_matrix'][i][i])
    deficiency=int(tensor['deficiency_matrix'][i][i])
    assert (target_dim,self_rank,deficiency)==(16,11,5)

    out={
      'schema':'w33.hypercharge_duad_center_cokernel.v1',
      'status':'PASS_EXPLICIT_HYPERCHARGE_DUAD_AND_CENTER_COKERNEL',
      'headline':'Composing the flagship A5 hypercharge theorem with the W33 S6-duad gauge module gives an explicit hypercharge vector in the 15-duad carrier. Under the isometric map Psi(x)_ij=(x_i+x_j)/2, Y=-omega1 maps to -1/3 on the five duads through one distinguished K6 vertex and +1/6 on the other ten. The four extra U(1)s are exactly the A4 zero-sum fluctuations on those five star edges. Independently, the physical E8 neutral holonomy sector has dimension16 and self-bracket rank11, so its five-dimensional bracket cokernel is exactly Y(1)+A4(4).',
      'intertwiner':{
        'A5':'{x in Z^6: sum x_i=0}',
        'duad_carrier':'Q^15 on K6 duads',
        'formula':'Psi(x)_ij=(x_i+x_j)/2',
        'syntheme_incidence_rank':10,
        'image_dimension':5,
        'isometric_gram':'C_A5',
        'S6_equivariant_parent':'data/w33_a5_duad_gauge_intertwiner.json'},
      'hypercharge':{
        'A5_coordinate':['-5/6','1/6','1/6','1/6','1/6','1/6'],
        'identification':'Y=-omega1(A5)',
        'duad_star_vertex':0,
        'star_duads':[list(DUADS[i]) for i in star],
        'star_value':'-1/3',
        'nonstar_value':'1/6',
        'norm2':'5/6',
        'kY':'5/3',
        'sixY_duad_pattern':{'-2':5,'+1':10},
        'order_in_discriminant':6,
        'stabilizer_in_S6':'S5 fixing the distinguished vertex',
        'stabilizer_order':120},
      'extra_u1_A4':{
        'domain':'x0=0 and sum_{i=1}^5 x_i=0',
        'rank':4,
        'simple_roots':'e1-e2,e2-e3,e3-e4,e4-e5',
        'duad_star_coordinates':'y_i=Psi(x)_{0i}=x_i/2 with sum_i y_i=0',
        'reconstruction':'Psi(x)_{ij}=y_i+y_j for 1<=i<j<=5',
        'weyl_group':'S5',
        'vacuum_rank_target':'singlet charge projections preserving Y must span this four-dimensional A4 sector to Higgs all four extra U(1)s'},
      'neutral_bracket_cokernel':{
        'physical_sector':'(rho,a,b)=(0,0,0)',
        'target_dimension':target_dim,
        'self_bracket_rank':self_rank,
        'deficiency':deficiency,
        'semisimple_derived_algebra':'su(3)+su(2), dimension 11',
        'center':'u(1)^5',
        'refinement':'u(1)^5 = Q*Y + (A4 tensor Q), dimensions 1+4',
        'dimension_identity':'16 = 11 + 1 + 4'},
      'five_equals_five_firewall':{
        'hypercharge_duad_star_size':5,
        'hypercharge_star_stabilizer':'S5, order120',
        'CZ_zero_phase_cross_size':5,
        'CZ_classical_frame_stabilizer':'D8, order8',
        'conclusion':'the two five-sets are not canonically identified by their certified natural symmetries'},
      'cross_repo_physical_inputs':[
        'Holotrade data/w33_flagship_a5_hypercharge_organizer.json',
        'Holotrade data/w33_flagship_global_u1_closure.json',
        'Holotrade data/w33_flagship_hypercharge_z6_gluing.json'],
      'boundary':'The charge-ledger workflow has not yet frozen the flagship singlet charge matrix, so the rank-four A4 Higgsing criterion is a precise target, not a completed vacuum proof.',
      'checks':{
        'Psi_is_A5_isometry':True,
        'Psi_image_in_syntheme_kernel':True,
        'hypercharge_star_5_plus_10':True,
        'hypercharge_norm_5_over_6':True,
        'hypercharge_order6':True,
        'A4_rank4_and_orthogonal':True,
        'star_reconstructs_A4':True,
        'S5_stabilizer_exact':True,
        'neutral_bracket_16_rank11_defect5':True,
        'center_refines_1_plus_4':True,
        'five_set_symmetry_firewall':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
    return out

if __name__=='__main__':
    main(True)
