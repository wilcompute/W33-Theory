#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, math
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass606_complete_twisted_snf.json'
DET=int('8610008787705746929677480795723398288250652856391360466985117906695922007438956829377224123494745308878841018642874747598776505925584919481248342770844795789913281309315324389893266322260922392992124642121462022350710943310537154700158281256674874649622430124110776617621723534654402361627697997358773328412672000000000000000')
RESOLVED={2:76,3:63,5:15,7:7,11:1,13:5,17:1,29:1,41:1,43:1,53:1,61:1,379:1,1039:1,1151:1,1831:1,3527:1,4261:1,5791:1,5903:1,6547:1,7243:1,13903:1,32987:1,910781:1,1790587:1,5239097:1,12924559:1,47228747:1,241006151:1,48464012033:1,8404496948527:1,166646809320571:1,488333131935871:1,94403487765008107291:1,214519374605498023781:1,
587147981829636393642873223241:1,75144583858746017876203917172673:1}
REMOTE_FACTORS=(587147981829636393642873223241,75144583858746017876203917172673)
COFACTOR=44120990758090595142167546520529192659268803434675483073693193
PROFILES={
 2:[1]*32+[2]*7+[3]*5+[4,5,6],
 3:[1]*24+[2]*13+[3]*2+[7],
 5:[1]*9+[2]*3,
 7:[1]*7,
 13:[1]*5,
}

def invariant_factors():
    width=max(len(v) for v in PROFILES.values())
    vals={p:[0]*(width-len(es))+sorted(es) for p,es in PROFILES.items()}
    exponent_one=[p for p,e in RESOLVED.items() if e==1 and p not in PROFILES]
    diag=[]
    for i in range(width):
        d=1
        for p,es in vals.items():d*=p**es[i]
        if i==width-1:
            for p in exponent_one:d*=p
        diag.append(d)
    return [1]*(280-width)+diag, vals, sorted(exponent_one)

def payload():
    diag,vals,exp1=invariant_factors()
    product=math.prod(diag)
    nontrivial=[d for d in diag if d!=1]
    fact_product=math.prod(p**e for p,e in RESOLVED.items())
    checks={
      'remote_factor_product_exact':REMOTE_FACTORS[0]*REMOTE_FACTORS[1]==COFACTOR,
      'remote_factors_sympy_prime_recheck':all(sp.isprime(p) for p in REMOTE_FACTORS),
      'complete_factorization_multiplies_to_determinant':fact_product==DET,
      'smith_diagonal_length280':len(diag)==280,
      'smith_has233_units_47_nontrivial':diag.count(1)==233 and len(nontrivial)==47,
      'smith_divisibility_chain':all(diag[i+1]%diag[i]==0 for i in range(279)),
      'smith_product_is_determinant':product==DET,
      'primary_valuation_sums_match':all(sum(vals[p])==RESOLVED[p] for p in PROFILES),
      'all_factor_bases_prime':all(sp.isprime(p) for p in RESOLVED),
      'two_remote_factors_enter_last_invariant_only':all(nontrivial[-1]%p==0 and all(d%p for d in nontrivial[:-1]) for p in REMOTE_FACTORS),
    }
    primary={
      '2':'(Z/2)^32 + (Z/4)^7 + (Z/8)^5 + Z/16 + Z/32 + Z/64',
      '3':'(Z/3)^24 + (Z/9)^13 + (Z/27)^2 + Z/2187',
      '5':'(Z/5)^9 + (Z/25)^3','7':'(Z/7)^7','13':'(Z/13)^5',
      'other_primes':'one cyclic Z/p factor for every exponent-one prime in the factor ledger'}
    return {'schema':'w33.pass606.complete_twisted_snf.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'operator':{'name':'Singer augmentation covariant Laplacian','dimension':280,'rank':280,'cokernel_order':str(DET)},
      'remote_factor_proof':{'workflow_run_id':30019712677,'artifact_id':8568835090,'artifact_sha256':'bd8757fb63fc4bc087083a8f5d0172ccb51a71345d4721e943e6eb29b4ba4f14','residual_cofactor':str(COFACTOR),'factors':[str(p) for p in REMOTE_FACTORS],'exponents':[1,1],'PARI_isprime':[True,True],'product_check':True},
      'complete_prime_factorization':{str(p):e for p,e in sorted(RESOLVED.items())},
      'primary_decomposition':primary,
      'smith_normal_form':{'unit_entries':233,'nontrivial_entries':47,'nontrivial_diagonal':[str(d) for d in nontrivial],'last_invariant_factor':str(nontrivial[-1]),'divisibility_chain':True,'product':str(product)},
      'theorem':'The integral Smith normal form of the 280x280 twisted Singer Laplacian is complete: 233 unit entries followed by the 47 listed nontrivial invariant factors. The residual 62-digit cofactor splits into two PARI-proven primes, each occurring once and therefore both entering only the final invariant factor.',
      'checks':checks,'boundary':'The factor proof is archived from the successful GitHub Actions PARI/GP run and independently rechecked here with SymPy. The Smith reconstruction uses the exact p-primary elementary-divisor profiles certified in Passes 597 and 601.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 606 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks']),'units':p['smith_normal_form']['unit_entries'],'nontrivial':p['smith_normal_form']['nontrivial_entries']}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
