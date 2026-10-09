"""Independent exact-verification of an assignment-aware FI-cancelling D-flat support.

The W33 scan's 10 bd fields include vectorlike exotics with different B-L.
This is a corrected hypothesis, NOT a F-flat or physical R-parity proof.
"""
from pathlib import Path
from fractions import Fraction as F
import gzip,json,re,itertools,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass10960_matter_even_dflat_closure as old
MODEL='Z6-II|Z6II_34__SM_20260917_1558'
EXPECTED=['q_1','q_2','q_3','bu_1','bu_2','bu_3','be_1','be_2','be_3',
          'bd_3','bd_5','bd_9','bd_10']
def proof():
    rec=json.load(open(ROOT/'data/w33_20261009_assignment_aware_bl_probe.json'))
    raw=json.load(gzip.open(ROOT/'data/w33_pass10960_heterotic_left_chiral_ledger.json.gz','rt'))[MODEL]
    q={f['name']:tuple(F(x) for x in f['q']) for f in raw['left']}
    dims={f['name']:f['dim'] for f in raw['left']}
    y=old.solve_affine([q[n] for n in q if old.base_of(n) in old.SMY],
                       [old.SMY[old.base_of(n)] for n in q if old.base_of(n) in old.SMY])[0]
    s=rec['even_Dflat_witness']
    assert s and set(s['singlet_support'])==set(s['positive_coeffs'])
    xs=[F(v) for v in rec['x0']]
    vecs=[[F(a) for a in n] for n in rec['N']]
    t=[F(z) for z in s['parity_t']]
    x=[a+sum(t[j]*vecs[j][i] for j in range(len(t))) for i,a in enumerate(xs)]
    # Matter charges for the specified chiral and vectorlike family assignment.
    for name in EXPECTED:
        assert old.dot(q[name],x)==old.BL[old.base_of(name)],name
    support={k:F(v) for k,v in s['positive_coeffs'].items()}
    assert all(v>=0 for v in support.values())
    assert sum(q[n][0]*v for n,v in support.items())==-1
    assert all(sum(q[n][i]*v for n,v in support.items())==0 for i in range(1,9))
    for n in support:
        assert old.dot(y,q[n])==0,n
        assert all(abs(int(re.match(r'(-?\d+)',part).group(1)))==1 and 'adj' not in part
                   for part in dims[n].split(',')),n
        assert (3*old.dot(q[n],x)).denominator==1
        assert (3*old.dot(q[n],x)).numerator%2==0
    extra_bd={n:str(old.dot(q[n],x)) for n in q if n.startswith('bd_') and n not in EXPECTED}
    doublets={n:str(old.dot(q[n],x)) for n in q if old.base_of(n) in ('l','bl')}
    integrality=sum((3*old.dot(x,v)).denominator==1 for v in q.values())
    return dict(status='PASS',schema='w33.20261009.corrected_assignment_Dflat.v1',
       model=MODEL,physical_family_constraints=EXPECTED,
       positive_support={k:str(v) for k,v in support.items()},
       charge_balance=['-1']+['0']*8,
       all_vev_threeBL_even=True,BL_coefficients=[str(v) for v in x],
       exotic_bd_BminusL=extra_bd,lepton_and_higgs_candidate_BminusL=doublets,
       integer_3BL_fields=integrality,total_left_fields=len(q),
       caveat='No F-flatness, no actual geometric generator inversion, no full matter/Higgs assignment or discrete gauge character certified.')
def character_probe(cert):
    raw=json.load(gzip.open(ROOT/'data/w33_pass10960_heterotic_left_chiral_ledger.json.gz','rt'))[MODEL]
    names=[f['name'] for f in raw['left']]
    q=[tuple(F(v) for v in f['q']) for f in raw['left']]
    rank,coord=old.lattice_coords(q)
    assert rank<=10
    idx={n:i for i,n in enumerate(names)}
    best=[]
    support=cert['positive_support']
    for eps in itertools.product((0,1),repeat=rank):
        parity=[sum(x*y for x,y in zip(eps,c))%2 for c in coord]
        if any(parity[idx[n]]!=1 for n in EXPECTED):continue
        if any(parity[idx[n]]!=0 for n in support):continue
        lepton_odd=[n for n in names if old.base_of(n)=='l' and parity[idx[n]]==1]
        Higgs_even=[n for n in names if old.base_of(n) in ('l','bl') and parity[idx[n]]==0]
        best.append((list(eps),lepton_odd,Higgs_even))
    cert['charge_lattice_rank']=rank
    cert['selected_matter_odd_VEV_even_Z2_characters']=len(best)
    cert['one_character']=({'eps':best[0][0],'lepton_odd':best[0][1],
                            'doublets_even':best[0][2]} if best else None)
    print('full charge-lattice Z2 candidates',len(best),'rank',rank,flush=True)
    return cert
if __name__=='__main__':
    cert=character_probe(proof())
    (ROOT/'data/w33_20261009_corrected_assignment_dflat_certificate.json').write_text(json.dumps(cert,indent=2)+'\n')
    print('PASSED charge-balance and matter VEV checks',cert['positive_support'])
    print('extras',cert['exotic_bd_BminusL'],'doublets',cert['lepton_and_higgs_candidate_BminusL'])
    print('integral 3BL count',cert['integer_3BL_fields'],'of',cert['total_left_fields'])
    print('character',cert['one_character'])
