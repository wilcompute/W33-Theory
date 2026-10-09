"""Conditional no-oscillator Z6-II H-momentum rule screen for actual
Pass11796 six gauge-neutral quadratic support monomials.
R integers modulo (6,3,2) from Buchmuller et al NPB785 (2007)
Table4.1 Eq4.8, https://escholarship.org/uc/item/4qk7z9wd
CRITICAL: The actual state oscillator excitations and gamma/fixed-point
data were NOT exported, and naive no-oscillator labels are assumptions.
"""
from pathlib import Path
import json,gzip
ROOT=Path(__file__).resolve().parents[1]
SECTOR_R={1:(-1,-1,-1),2:(-2,-2,0),3:(-3,0,-1),
          4:(-4,-1,0),5:(-5,-2,-1)}
MOD=(6,3,2)
def certificate():
  fl=json.load(gzip.open(ROOT/'data/w33_pass10960_heterotic_left_chiral_ledger.json.gz','rt'))['Z6-II|Z6II_34__SM_20260917_1558']['left']
  fields={f['name']:f for f in fl}
  ff=json.loads((ROOT/'data/w33_20261009_new_higgs_13vev_F_filter.json').read_text())
  rec=[]
  for a,b in ff['examples']['bilinears']:
    k=(int(fields[a]['k']),int(fields[b]['k']))
    assert k in [(2,4),(3,3)]
    resid=tuple(sum(SECTOR_R[s][j] for s in k)%MOD[j] for j in range(3))
    required=tuple((-1)%m for m in MOD)
    rec.append(dict(fields=[a,b],twist_sectors=list(k),predicted_no_oscillator_R=resid,
       required_R=required,satisfies_no_oscillator_R=resid==required))
  assert len(rec)==6 and all(not r['satisfies_no_oscillator_R'] for r in rec)
  return dict(status='PASS',count=6,records=rec,
    no_oscillator_R_sector_table={str(k):list(v) for k,v in SECTOR_R.items()},
    source='Buchmuller et al NPB785 (2007) pp 168, Table4.1 and Eq4.8, eScholarship item 4qk7z9wd.',
    result='All 6 gauge-neutral support bilinears FAIL the standard H-momentum selection requirement under the explicitly stated no-oscillator twisted-ground-state assumption.',
    major_limit='No state-specific oscillator excitation number, gamma phases, fixed-point space group, full R-charge of individual 176 fields or computed CFT amplitudes available. This is a conditional filter, NOT verified absence of six actual superpotential coefficients. Physical vertex conventions may require further checking.')
if __name__=='__main__':
  d=certificate()
  (ROOT/'data/w33_20261009_conditional_H_momentum_bilinears.json').write_text(json.dumps(d,indent=2)+'\n')
  print('conditional H momentum excluded',sum(not r['satisfies_no_oscillator_R'] for r in d['records']))
