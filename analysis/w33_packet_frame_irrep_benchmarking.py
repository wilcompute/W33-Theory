#!/usr/bin/env python3
"""Compile the 72-slot Aut(H(2,3)) frame into exact benchmarking projectors.

G=Aut H(2,3)=S3 wr C2 acts on the nine qutrit/Hesse bins.  The nine irreps are
constructed explicitly from the three S3 irreps (1, sgn, std):

  rho_[2], rho_[1,1] for rho=1,sgn,std,
  and induced cross terms 1xsgn, 1xstd, sgnxstd.

The nine-bin permutation representation decomposes as
  V9 = 1_sym + std_sym + (1 x std), dimensions 1+4+4.

On End(V9), whose character is fix(g)^2, the irrep multiplicities are
  (3,1,1,0,6,3,2,6,3)
in the frozen ordering below.  Hence
  sum d*m = 81,
  sum m^2 = 105,
and exactly eight isotypic sectors are present.

Each central projector is compiled directly onto the runtime slots:
  P_lambda = d_lambda/72 * sum_g chi_lambda(g) Ad_g.
The 72 slots collapse into exactly nine character-signature classes, so an
experiment can first average each class and then combine nine class averages
with exact integer character weights.

A generic G-covariant channel acts on multiplicity spaces of sizes
3,1,1,6,3,2,6,3, so it has at most 25 distinct multiplicity-space decay
eigenvalues.  If each multiplicity block is scalarized/depolarized, this drops
to eight character-resolved rates.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_packet_frame_irrep_benchmarking.json'
PTS=list(itertools.product(range(3),repeat=2));IDX={p:i for i,p in enumerate(PTS)}
I=(1,0,0,1);R=(0,2,1,0);S=(1,0,0,2)

def mm(A,B):return tuple(sum(A[2*i+k]*B[2*k+j] for k in range(2))%3 for i in range(2) for j in range(2))
def mpow(A,n):
    o=I
    for _ in range(n):o=mm(o,A)
    return o
def mv(A,v):return ((A[0]*v[0]+A[1]*v[1])%3,(A[2]*v[0]+A[3]*v[1])%3)
def compose(p,q):return tuple(p[q[i]] for i in range(len(p)))

def runtime(h,sec,probe):
    t=PTS[h];L=mm(mpow(S,sec),mpow(R,probe))
    perm=[]
    for p in PTS:
        u=mv(L,p);z=((t[0]+u[0])%3,(t[1]+u[1])%3)
        perm.append(IDX[z])
    return tuple(perm),t,L

def affine(a,t):return tuple((a*x+t)%3 for x in range(3))
def wreath(t,L):
    if L[1]==0 and L[2]==0:
        return affine(L[0],t[0]),affine(L[3],t[1]),0
    assert L[0]==0 and L[3]==0
    return affine(L[1],t[0]),affine(L[2],t[1]),1

def cls(p):
    f=sum(i==p[i] for i in range(3))
    return 'e' if f==3 else 't' if f==1 else 'c'

HC={
 '1':{'e':1,'t':1,'c':1},
 'sgn':{'e':1,'t':-1,'c':1},
 'std':{'e':2,'t':0,'c':-1}}
IR=[
 ('1_sym',1,('same','1',1)),
 ('1_alt',1,('same','1',-1)),
 ('sgn_sym',1,('same','sgn',1)),
 ('sgn_alt',1,('same','sgn',-1)),
 ('std_sym',4,('same','std',1)),
 ('std_alt',4,('same','std',-1)),
 ('1xsgn',2,('cross','1','sgn')),
 ('1xstd',4,('cross','1','std')),
 ('sgnxstd',4,('cross','sgn','std'))]

def chi(ir,a,b,sw):
    typ=ir[2]
    if typ[0]=='same':
        _,r,eps=typ
        if not sw:return HC[r][cls(a)]*HC[r][cls(b)]
        return eps*HC[r][cls(compose(a,b))]
    _,r,s=typ
    if sw:return 0
    return HC[r][cls(a)]*HC[s][cls(b)]+HC[s][cls(a)]*HC[r][cls(b)]

def main(write=True):
    slots=[]
    for h in range(9):
      for sec in range(2):
       for probe in range(4):
        slot=8*h+4*sec+probe
        p,t,L=runtime(h,sec,probe);a,b,sw=wreath(t,L)
        ch=[chi(ir,a,b,sw) for ir in IR]
        slots.append({'slot':slot,'h':h,'sector':sec,'probe':probe,'fix':sum(i==j for i,j in enumerate(p)),
                      'characters':ch})
    assert len(slots)==72

    dims=[x[1] for x in IR]
    mV=[];mEnd=[]
    for j in range(9):
        mV.append(sum(s['fix']*s['characters'][j] for s in slots)//72)
        mEnd.append(sum(s['fix']**2*s['characters'][j] for s in slots)//72)
    assert mV==[1,0,0,0,1,0,0,1,0]
    assert mEnd==[3,1,1,0,6,3,2,6,3]
    assert sum(d*m for d,m in zip(dims,mEnd))==81
    assert sum(m*m for m in mEnd)==105

    # Orthogonality of all nine character rows.
    for i in range(9):
        for j in range(9):
            v=sum(s['characters'][i]*s['characters'][j] for s in slots)
            assert v==(72 if i==j else 0)

    buckets=defaultdict(list)
    for s in slots:buckets[tuple(s['characters'])].append(s['slot'])
    assert len(buckets)==9
    classes=[]
    for n,(sig,sl) in enumerate(sorted(buckets.items(),key=lambda kv:(-len(kv[1]),kv[1][0]))):
        classes.append({'class_id':n,'size':len(sl),'slots':sl,'characters':list(sig)})
    assert sum(x['size'] for x in classes)==72

    irreps=[]
    for i,(name,d,_) in enumerate(IR):
        m=mEnd[i]
        irreps.append({
          'name':name,'dimension':d,'V9_multiplicity':mV[i],'EndV9_multiplicity':m,
          'EndV9_isotypic_rank':d*m,'present':m>0,
          'projector_denominator':72,
          'projector_class_weight_numerators':[d*c['characters'][i] for c in classes]})
    assert sum(x['EndV9_isotypic_rank'] for x in irreps)==81

    present=[x for x in irreps if x['present']]
    maxdecays=sum(x['EndV9_multiplicity'] for x in present)
    assert len(present)==8 and maxdecays==25

    parent=json.loads((ROOT/'data/w33_packet_frame_symmetry_tomography.json').read_text())
    assert parent['twirl']['twirled_superoperator_commutant_dimension']==105

    out={
      'schema':'w33.packet_frame_irrep_benchmarking.v1','status':'PASS_72_FRAME_IRREP_BENCHMARKING',
      'headline':'The 72-slot Aut H(2,3) runtime frame compiles into nine exact character classes and eight present End(V9) isotypic sectors. End(V9) multiplicities are (3,1,1,0,6,3,2,6,3), giving commutant dimension 105. Central projectors are exact weighted averages of runtime conjugations; a generic covariant channel has at most 25 multiplicity-space decay eigenvalues, dropping to eight character-resolved rates if each multiplicity block is scalarized.',
      'group':'Aut H(2,3)=S3 wr C2','order':72,
      'irrep_order':[x[0] for x in IR],'irrep_dimensions':dims,
      'V9_decomposition':{
        'multiplicities':mV,'formula':'1_sym + std_sym + 1xstd','dimensions':'1+4+4=9'},
      'EndV9_decomposition':{
        'multiplicities':mEnd,'dimension':81,'commutant_dimension':105,
        'present_isotypic_sectors':8,'max_generic_decay_eigenvalues':25,
        'scalarized_character_decay_rates':8},
      'runtime_character_classes':classes,
      'projectors':irreps,
      'protocol':[
        'For each of the nine character classes, average the measured conjugation response over its listed runtime slots.',
        'For irrep lambda, combine those nine class averages with numerator d_lambda*chi_lambda(C) and common denominator 72.',
        'Fit dynamics inside each present multiplicity block; without an extra depolarizing assumption there can be up to 25 decay eigenvalues, not merely eight.',
        'If randomized compiling/twirling scalarizes each multiplicity block, fit one decay rate per present isotypic sector (eight total).'],
      'boundary':'Exact finite representation/control compilation. Character-projector coefficients are signed post-processing weights, not probabilities. Laboratory use still requires calibrated or virtual implementations of all listed frame permutations and a SPAM-aware estimator.',
      'parents':['data/w33_packet_frame_symmetry_tomography.json','data/w33_qutrit_hamming_cz_frame_bundle.json'],
      'checks':{'irreps9':True,'character_orthogonality':True,'V9_1_4_4':True,'EndV9_dim81':True,
                'commutant105':True,'runtime_classes9':True,'present_sectors8':True,'max_decays25':True}}
    if write:OUT.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
    return out
if __name__=='__main__':main(True)
