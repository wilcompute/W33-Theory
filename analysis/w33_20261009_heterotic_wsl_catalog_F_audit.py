"""W33 three-singlet candidates: scope-audited actual orbifolder exports
and necessary F-term hazards; no inference from absent finite catalogs.

Reads authoritative connected WSL /home/wiljd/orb/scan/cp2/out files
without changing them, uses SHA256 to freeze source. '*.sp' contains
spectrum metadata, '.dbd','.mu','.ch' contain limited channel-specific
'C degree fields...' couplings; '.w' contains weight records, NOT a
superpotential.

The exact named known n81*n17*n82 is a string-selection candidate
from Pass11797, not asserted to have nonzero coefficient. If it does,
F_n81 is nonzero on every candidate with n17,n82 !=0 unless cancelled.
"""
from pathlib import Path
from collections import Counter
import sys,json,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import w33_pass11797_11801_five_physical_fronts as P
BASE='/home/wiljd/orb/scan/cp2/out/Z6II_34__SM_20260917_1558'
def wsl_text(path):
 r=subprocess.run(['wsl.exe','cat',path],capture_output=True,timeout=20)
 if r.returncode:raise RuntimeError(r.stderr.decode(errors='replace')[:500])
 return r.stdout
def certificate():
 raw,prev,fields,support,charge=P.load()
 h=json.loads((ROOT/'data/w33_20261009_three_singlet_corrected_R_screen.json').read_text())
 exports={}
 records=[]
 for suf in ('.dbd','.mu','.ch','.w','.model'):
  content=wsl_text(BASE+suf)
  lines=content.decode(errors='replace').splitlines()
  cs=[]
  for line in lines:
   a=line.strip().split()
   if len(a)>=4 and a[0]=='C' and a[1].isdigit():
    deg=int(a[1])
    if len(a)==deg+2:cs.append(a[2:])
  records.extend([(suf,tuple(z)) for z in cs])
  exports[suf]=dict(sha256=hashlib.sha256(content).hexdigest(),
                    lines=len(lines),C_records=len(cs),
                    C_degree_histogram=dict(Counter(map(len,cs))),
                    sample_record=cs[0] if cs else None)
 spectrum=wsl_text('/home/wiljd/orb/scan/cp2/sp/Z6II_34__SM_20260917_1558.sp')
 exports['.sp']=dict(sha256=hashlib.sha256(spectrum).hexdigest(),
                     lines=len(spectrum.splitlines()),format='S named k/dim/q and associated metadata; not an exhaustive superpotential list')
 cset={tuple(sorted(x)) for suf,x in records}
 target=tuple(sorted(('n_81','n_17','n_82')))
 assert P.selection(list(target),fields)
 named=target in cset
 scanned=[]
 for row in h['results']:
  active=set(support)|set(row['triple'])
  active.add('n_17');active.add('n_82')
  tad=[dict(outside=n,record_fields=list(rec),file_suffix=suf)
       for suf,rec in records
       for n in rec if n not in active and all(k in active for k in rec if k!=n)]
  # Truncate output only, keep real complete count.
  cnew=sum(all(n in active for n in rec) for _,rec in records)
  field_universe=set().union(*(set(rec) for _,rec in records))
  selected=row['selected_up_witnesses']+row['selected_colored_witnesses']
  matched_named=[dict(target=z['target'],fields=z['full_monomial_fields'])
       for z in selected if tuple(sorted(z['full_monomial_fields'])) in cset]
  down=json.loads((ROOT/'data/w33_pass11797_11801_five_physical_fronts.json').read_text())['pass11799']['mass_sectors']['d']
  directmask=[[int(any(m['target']==[a,b] for m in matched_named)) for b in down['columns']] for a in down['rows']]
  scanned.append(dict(triple=row['triple'],sources_exact_named_full_monomial_matches=len(matched_named),
    finite_couplings_entirely_in_vev_support=cnew,
    source_catalog_direct_colored_mask_rank=P.matching_rank(directmask),
    source_catalog_direct_colored_mask=directmask,
    finite_C_catalog_possible_outsider_linear_terms=len(tad),
    example_possible_outsider_tadpoles=tad[:8],
    full_named_matches=matched_named[:8]))
 return dict(status='PASS',catalog_fingerprints=exports,
    total_finite_named_C_records=len(records),
    distinct_named_C_multisets=len(cset),
    triplet_n81_n17_n82_corrected_selection_pass=True,
    triplet_n81_n17_n82_present_in_limited_exports=named,
    finite_catalog_only_positive_mask='Source C entries give only finite named channel coupling candidates; their matching rank is a LOWER bound on necessary-rule structural matching capacity, not a certified realized matrix rank or physical nonzero amplitude.',
    candidate_audit=scanned,
    source_scope='The actual WSL exports are channel-specific and usually degree<=5. The absence of a degree8+ string coupling in them is not a worldsheet selection veto or a zero amplitude. The SP file is a state list, W is a weight catalog. Duplicate field-name lists and unknown channel conventions may occur.',
    F_term_conditional='If a nonzero W coefficient multiplies n81*n17*n82 then F_n81 includes c*VEV(n17)*VEV(n82), nonzero for all 16 plus-positive candidates unless other terms cancel. The actual CFT coefficient and cancellations have NOT been computed.',
    remedy='Need complete sector fixed point labels, constructing elements, gamma phases and vertex operator amplitudes in the actual model, not just k/q/R residues.')
if __name__=='__main__':
 d=certificate()
 (ROOT/'data/w33_20261009_heterotic_wsl_catalog_F_audit.json').write_text(json.dumps(d,indent=2)+'\n')
 print('WSL HETEROTIC',{s:(v['lines'],v.get('C_records')) for s,v in d['catalog_fingerprints'].items()},'n81named',d['triplet_n81_n17_n82_present_in_limited_exports'],
       'full matches',[z['sources_exact_named_full_monomial_matches'] for z in d['candidate_audit']])
