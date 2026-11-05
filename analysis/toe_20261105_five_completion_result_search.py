"""Bounded result/formula search. Hits are not semantic novelty proofs."""
import pathlib,re,json,concurrent.futures
R=pathlib.Path(__file__).resolve().parents[1]
PATTERNS={'tensor_D_plus_one':r'D\s*\+\s*1.{0,60}(?:yukawa|beta)|(?:beta|yukawa).{0,60}D\s*\+\s*1',
 'two_scalar_primitive_axion':r'n\s*(?:thetaS|theta_S|θS).{0,20}(?:thetaT|theta_T|θT)|S\^n.{0,12}Tdag',
 'toron_first_Chern':r'toron.{0,80}(?:chern|determinant)|(?:chern|determinant).{0,80}toron',
 'Lorentzian_continuation':r'(?:track|continu).{0,60}(?:arccos|dihedral)|(?:Schlafli|Schläfli).{0,60}(?:Lorentz|complex)',
 'warped_Planck_repair':r'Mbrane|brane.{0,40}Einstein|warped.{0,50}(?:Planck|KK)'}
def scan(p):
 if p.name.startswith(('toe_20261105_five_','toe_20261105_global_measure')):return None
 try:t=p.read_text(encoding='utf-8',errors='replace')
 except OSError:return None
 hits=[]
 for k,pat in PATTERNS.items():
  m=re.search(pat,t,re.I)
  if m:hits.append(dict(result=k,line=t.count('\n',0,m.start())+1,snippet=t[max(0,m.start()-60):m.end()+80]))
 return dict(path=str(p.relative_to(R)).replace('\\','/'),hits=hits)if hits else None
if __name__=='__main__':
 paths=[p for folder in ['analysis','papers','docs','tests','scripts']for p in(R/folder).rglob('*')if p.is_file()and p.suffix in{'.py','.json','.md','.tex','.html','.js','.g','.sage'}]
 with concurrent.futures.ThreadPoolExecutor(max_workers=8)as pool:hits=[x for x in pool.map(scan,paths)if x]
 out=dict(scanned_files=len(paths),patterns=PATTERNS,matches=hits,scope=__doc__)
 (R/'data/toe_20261105_five_completion_result_search.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
 print('RESULT_SEARCH',len(paths),len(hits),flush=True)
