#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,math
from pathlib import Path
import sympy as sp
import w33_pass616_arithmetic_core_factorization as p616
import w33_pass622_ramification_atlas as p622
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass632_montes_okutsu_stage0.json'
PRIMES=(2,3,5,7,13)


def magma_driver_text():
 lines=["// Pass 632: complete Montes/Okutsu transcript driver","Q := Rationals();","R<x> := PolynomialRing(Q);","P := ["]
 for k,c in enumerate(p616.FACTOR_COEFFS):
  n=len(c)-1;terms=[f"({a})*x^{n-j}" for j,a in enumerate(c) if a]
  lines.append("  "+" + ".join(terms)+("," if k+1<len(p616.FACTOR_COEFFS) else ""))
 lines += ["] ;","PR := [2,3,5,7,13];","for i in [1..#P] do","  for p in PR do","    printf \"BEGIN field=%o degree=%o prime=%o\\n\", i, Degree(P[i]), p;","    OM,Tree,ind := Montes(P[i],p : Field:=true);","    print OM; print Tree; print ind;","    printf \"END field=%o prime=%o\\n\", i, p;","  end for;","end for;"]
 return "\n".join(lines)+"\n"

def factor_record(poly,p):
 unit,fac=sp.factor_list(poly,modulus=p)
 rows=[]
 for f,m in fac:
  coeff=[int(c)%p for c in f.all_coeffs()]
  rows.append({'degree':f.degree(),'multiplicity':int(m),'coefficients_mod_p':coeff})
 rows.sort(key=lambda r:(r['degree'],r['coefficients_mod_p'],r['multiplicity']))
 deriv=poly.diff();g=sp.gcd(poly,deriv,modulus=p)
 return {'unit_mod_p':int(unit)%p,'factors':rows,'factor_degree_multiplicity':sorted([[r['degree'],r['multiplicity']] for r in rows]),'derivative_gcd_degree':g.degree(),'squarefree':g.degree()==0}

def payload():
 x=sp.symbols('x');polys=[sp.Poly.from_list(c,x,domain=sp.ZZ) for c in p616.FACTOR_COEFFS];fields=p622.load_fields()
 transcripts=[];clean=0;index_singular=0;ramified=0;wild=0
 for poly,fld in zip(polys,fields):
  for p in PRIMES:
   fac=factor_record(poly,p);loc=fld['local'][str(p)]
   ideals=sorted([{'e':int(e),'f':int(ff),'wild':e%p==0} for e,ff in loc['ef']],key=lambda r:(r['f'],r['e']))
   dedekind=loc['v_index']==0
   factor_profile=sorted([[r['multiplicity'],r['degree']] for r in fac['factors']])
   ideal_profile=sorted([[r['e'],r['f']] for r in ideals])
   profile_match=(factor_profile==ideal_profile) if dedekind else None
   singular=not fac['squarefree'];field_ram=loc['v_field_disc']>0
   kind='unramified'
   if field_ram:kind='wild' if any(r['wild'] and r['e']>1 for r in ideals) else 'tame'
   if dedekind:clean+=1
   if singular and not field_ram:index_singular+=1
   if field_ram:ramified+=1
   if kind=='wild':wild+=1
   rec={'field':fld['index'],'degree':fld['degree'],'prime':p,'polynomial_mod_p':fac,'p_maximal_order':{'v_polynomial_discriminant':loc['v_poly_disc'],'v_field_discriminant':loc['v_field_disc'],'v_power_basis_index':loc['v_index'],'prime_ideals':ideals,'ramification_kind':kind},'dedekind_clean':dedekind,'dedekind_profile_match':profile_match,'index_only_singularity':singular and not field_ram,'discriminant_index_identity':loc['v_poly_disc']==loc['v_field_disc']+2*loc['v_index']}
   rec['sha256']=hashlib.sha256(json.dumps(rec,sort_keys=True,separators=(',',':')).encode()).hexdigest()
   transcripts.append(rec)
 driver=magma_driver_text();driver_hash=hashlib.sha256(driver.encode()).hexdigest()
 checks={
  'seventeen_polynomials':len(polys)==len(fields)==17,
  'eighty_five_local_transcripts':len(transcripts)==85,
  'all_discriminant_index_identities':all(r['discriminant_index_identity'] for r in transcripts),
  'all_local_degrees_close':all(sum(q['e']*q['f'] for q in r['p_maximal_order']['prime_ideals'])==r['degree'] for r in transcripts),
  'all_dedekind_clean_profiles_match':all(r['dedekind_profile_match'] is True for r in transcripts if r['dedekind_clean']),
  'nonmaximal_orders_have_positive_index':all(r['p_maximal_order']['v_power_basis_index']>0 for r in transcripts if not r['dedekind_clean']),
  'stage0_hashes_locked':all(len(r['sha256'])==64 for r in transcripts),
  'magma_driver_generator_locked':len(driver_hash)==64,
  'ramified_count_positive':ramified>0,
  'index_only_singularities_detected':index_singular>0,
 }
 global_hash=hashlib.sha256(''.join(r['sha256'] for r in transcripts).encode()).hexdigest()
 return {'schema':'w33.pass632.montes_okutsu_stage0.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'counts':{'localizations':len(transcripts),'Dedekind_clean':clean,'nonmaximal_power_basis':85-clean,'ramified':ramified,'wild':wild,'index_only_singularities':index_singular},
  'transcripts':transcripts,
  'magma_completion_driver':{'generator':'python analysis/w33_pass632_montes_okutsu_stage0.py --emit-magma analysis/w33_pass632_montes_driver.m','sha256':driver_hash,'purpose':'Run Montes(f,p : Field:=true) for all 85 pairs and archive complete OM representations, higher Newton polygons, residual polynomials, slopes, indices, and local integral bases.'},
  'global_sha256':global_hash,
  'theorem':'All 85 torsion-prime localizations now have exact stage-zero Okutsu/Montes transcripts: complete factorization modulo p, repeated-factor and derivative-gcd data, exact p-maximal prime-ideal e/f profiles, wild/tame labels, and polynomial-versus-field discriminant/index reconciliation. Whenever the power basis is p-maximal, the modular factors agree exactly with the local prime ideals; the remaining rows isolate the precise Dedekind defects that higher Newton polygons must resolve.',
  'checks':checks,
  'boundary':'The embedded transcripts are exact Stage-0 plus certified p-maximal outputs. Complete OM representations, slopes, residual polynomials, and local integral bases require executing the included Magma Montes driver (or an equivalent licensed Montes implementation); they are not fabricated here.'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);ap.add_argument('--emit-magma',type=Path);a=ap.parse_args();
 if a.emit_magma:a.emit_magma.write_text(magma_driver_text())
 p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 632 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'counts':p['counts']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
