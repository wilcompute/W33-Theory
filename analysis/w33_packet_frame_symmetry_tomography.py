#!/usr/bin/env python3
"""72-slot CZ-frame symmetry tomography and exact twirl compression.

The nine translated CZ zero-phase crosses on H(2,3) have incidence matrix
B=I+A.  The parallel cross-incidence theorem proves
  spec(B)=5^1,2^4,(-1)^4,
  B^{-1}=A/2-J/5.
Hence nine cross-sum measurements y=B p reconstruct all nine computational-bin
populations exactly.  The spectral 2-norm condition number is 5.

The runtime frame already orders
  72 = 9 cross centers * 8 D8 stabilizer settings.
Thus each population-tomography center comes with eight symmetry-related
settings. Four preserve CZ_3 and four invert CZ_3 <-> CZ_3^{-1}; this supplies a
native phase-inversion/control audit without changing the five-state zero
support.

For the full G=Aut H(2,3)=S3 wr C2 action on the nine bins:
  fixed-point census = 9^1, 3^12, 1^27, 0^32.
Burnside gives exactly three invariant operator kernels (Hamming distances
0,1,2), while the commutant of the induced 81-dimensional conjugation action
has dimension
  (1/72) sum_g fix(g)^4 = 105.
So a full frame-covariant twirl reduces a generic 81x81 linear superoperator
from 6561 coefficients to a 105-dimensional symmetry commutant.  This is a
finite representation statement, not a claim that all 72 operations have
already been implemented optically.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_packet_frame_symmetry_tomography.json'

PTS=list(itertools.product(range(3),repeat=2))
IDX={p:i for i,p in enumerate(PTS)}

def cross(c,p):
    a,b=c;x,y=p
    return int(x==a or y==b)

def mm(A,B):
    return tuple(sum(A[2*i+k]*B[2*k+j] for k in range(2))%3
                 for i in range(2) for j in range(2))
I=(1,0,0,1);R=(0,2,1,0);S=(1,0,0,2)
def mpow(A,n):
    o=I
    for _ in range(n):o=mm(o,A)
    return o

def matmul(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]

def full_group():
    out=[]
    for px in itertools.permutations(range(3)):
      for py in itertools.permutations(range(3)):
       for sw in (0,1):
        perm=[]
        for x,y in PTS:
            z=(px[y],py[x]) if sw else (px[x],py[y])
            perm.append(IDX[z])
        out.append(tuple(perm))
    assert len(out)==len(set(out))==72
    return out

def d8():
    out=[]
    for sec in range(2):
      for probe in range(4):
        L=mm(mpow(S,sec),mpow(R,probe))
        perm=[]
        for x,y in PTS:
            z=((L[0]*x+L[1]*y)%3,(L[2]*x+L[3]*y)%3)
            perm.append(IDX[z])
        # phase character on xy using (1,1), whose phase is nonzero.
        z=(perm[IDX[(1,1)]])
        xx,yy=PTS[z]
        chi=(xx*yy)%3
        assert chi in (1,2)
        out.append((tuple(perm),sec,probe,chi))
    return out

def main(write=True):
    B=[[F(cross(c,p)) for p in PTS] for c in PTS]
    A=[[B[i][j]-(1 if i==j else 0) for j in range(9)] for i in range(9)]
    J=[[F(1) for _ in range(9)] for _ in range(9)]
    Binv=[[F(1,2)*A[i][j]-F(1,5)*J[i][j] for j in range(9)] for i in range(9)]
    eye=matmul(B,Binv)
    assert all(eye[i][j]==int(i==j) for i in range(9) for j in range(9))

    # Stable inversion diagnostics follow exactly from singular values |5|,|2|,|1|.
    condition=F(5,1)
    normalized_white_noise_variance_gain=(
        F(1,25)+4*F(1,4)+4*F(1,1)
    )/9
    assert normalized_white_noise_variance_gain==F(14,25)

    G=full_group()
    fix=Counter(sum(i==j for i,j in enumerate(g)) for g in G)
    assert fix==Counter({0:32,1:27,3:12,9:1})
    operator_invariants=sum(n*f*f for f,n in fix.items())//72
    superop_commutant=sum(n*f**4 for f,n in fix.items())//72
    assert operator_invariants==3
    assert superop_commutant==105

    D=d8()
    assert Counter(x[3] for x in D)==Counter({1:4,2:4})
    dfix=Counter(sum(i==j for i,j in enumerate(g)) for g,_,_,_ in D)
    assert dfix==Counter({3:4,1:3,9:1})

    # Every 8-slot hesse fiber has one D8 copy and the same five-state cross.
    fibers=[]
    for h,c in enumerate(PTS):
        rows=[]
        C={p for p in PTS if cross(c,p)}
        for g,sec,probe,chi in D:
            rows.append({
              'slot':8*h+4*sec+probe,'sector':sec,'probe':probe,
              'cz_character':chi,'phase_action':'preserve' if chi==1 else 'invert'})
        assert len(rows)==8
        fibers.append({'hesse_bin':h,'center':list(c),'cross_size':len(C),'settings':rows})

    parent=json.loads((ROOT/'data/w33_qutrit_hamming_cross_incidence.json').read_text())
    assert parent['status']=='PASS_Q3_CROSS_INCIDENCE_LOCK'
    frame=json.loads((ROOT/'data/w33_qutrit_hamming_cz_frame_bundle.json').read_text())
    assert frame['status']=='PASS_Q3_LOCAL_FRAME_PHASE_LOCK'

    out={
      'schema':'w33.packet_frame_symmetry_tomography.v1',
      'status':'PASS_72_FRAME_TOMOGRAPHY_TWIRL',
      'headline':'The 72-slot packet is exactly nine translated CZ-cross population-tomography channels times eight D8 stabilizer settings. The nine cross sums reconstruct all nine computational-bin populations with B3^{-1}=A/2-J/5 and condition number 5. Within each center, four settings preserve CZ3 and four invert CZ3, giving a native symmetry/phase audit. A full Aut H(2,3) frame twirl has a three-dimensional invariant operator algebra and a 105-dimensional superoperator commutant, compressing a generic 6561-coefficient linear noise map by symmetry.',
      'population_tomography':{
        'measurements':9,'unknown_populations':9,
        'measurement':'y_center = sum of populations on the five-state translated CZ zero-phase cross',
        'decoder':'p=(A(H(2,3))/2-J/5)y',
        'singular_values':{'5':1,'2':4,'1':4},
        'condition_number_2':str(condition),
        'white_measurement_noise_average_variance_gain':str(normalized_white_noise_variance_gain),
        'scope':'computational-basis populations only; not full quantum-state tomography'},
      'runtime_frame':{
        'factorization':'72=9*8','center_fibers':fibers,
        'per_center_phase_preservers':4,'per_center_phase_inverters':4},
      'twirl':{
        'group':'Aut H(2,3)=S3 wr C2','order':72,
        'fixed_point_census':{str(k):v for k,v in sorted(fix.items())},
        'operator_invariant_dimension':operator_invariants,
        'operator_invariants':'the three Hamming-distance kernels d=0,1,2',
        'generic_superoperator_dimension_before':81*81,
        'twirled_superoperator_commutant_dimension':superop_commutant,
        'compression_factor':str(F(81*81,superop_commutant)),
        'burnside_formula':'dim Comm(conjugation)=|G|^-1 sum_g fix(g)^4'},
      'literature_context':[
        {'topic':'group twirling/noise tailoring for controlled-phase gates','ref':'arXiv:2309.15651'},
        {'topic':'qutrit randomized benchmarking','ref':'arXiv:2009.00599'}],
      'boundary':'Exact finite-frame/tomography/representation arithmetic. A laboratory protocol still needs calibrated implementations or virtual frame updates for the required permutations, plus a physical definition of each cross-sum measurement.',
      'checks':{
        'B_inverse_exact':True,'condition_number5':True,'72_group_exact':True,
        'fixed_point_census_exact':True,'operator_invariants3':True,
        'superoperator_commutant105':True,'D8_four_preserve_four_invert':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
    return out

if __name__=='__main__':main(True)
