"""Exact U1 D-flat extension scan for Pass11796 branch with one or two
matched SU4 fundamental/antifundamental VEV pairs. All spectra and
charge data from locally recovered Pass11797 frozen full benchmark.
This is an algebraic *continuity* witness; only parity-even fields.
No F-flatness or exotic/Yukawa rank repair is inferred.
"""
import gzip,json
from pathlib import Path
from fractions import Fraction
import sympy as S
ROOT=Path(__file__).resolve().parents[1]
BASE=['n_17','n_47','n_50','n_80','n_82','n_9','n_54','n_37','n_38','n_35','n_36','n_39','n_40']
def certificate():
    D=json.load(gzip.open(ROOT/'data/w33_pass11797_full_benchmark_metadata.json.gz','rt'))['fields']
    prior=json.load(open(ROOT/'data/w33_pass11796_parity_complete_abelian_higgs.json'))
    parity=prior['all176_field_parities']
    def charge(n):return S.Matrix([S.Rational(x) for x in D[n]['q']])
    M=S.Matrix.hstack(*(charge(x) for x in BASE))
    assert M.rank()==8 and len(M.T.nullspace())==1
    L=M.T.nullspace()[0]
    fundamentals=['n_69','n_74']
    anti=[n for n,f in D.items() if f['dim']=='1,1,-4,1' and charge(n)[1]==0]
    assert len(anti)==6,anti
    single=[];pairs=[]
    r={n:L.dot(charge(n)) for n in fundamentals+anti}
    for f in fundamentals:
      for a in anti:
        if parity[f] or parity[a]:continue
        sumcharge=charge(f)+charge(a)
        if L.dot(sumcharge)==0:
          # Is there a real rational solution with original FI core positive?
          delta,free=M.gauss_jordan_solve(-sumcharge)
          delta=delta.subs({x:0 for x in free})
          assert M*delta==-sumcharge
          single.append(dict(fundamental=f,antifundamental=a,
             first_order_VEV_norm_correction={n:str(delta[i]) for i,n in enumerate(BASE)}))
    for a in anti:
      for b in anti:
        if a==b or parity[a] or parity[b]:continue
        x=r['n_69']+r[a];y=r['n_74']+r[b]
        if x==y==0:ratio=S.Rational(1)
        elif x*y<0:ratio=-x/y
        else:continue
        combined=charge('n_69')+charge(a)+ratio*(charge('n_74')+charge(b))
        assert L.dot(combined)==0
        delta,free=M.gauss_jordan_solve(-combined)
        delta=delta.subs({x:0 for x in free})
        assert M*delta==-combined
        pairs.append(dict(first=['n_69',a],second=['n_74',b],
          second_amplitude_square_over_first=str(ratio),
          first_order_base_shift={n:str(delta[i]) for i,n in enumerate(BASE)}))
    return dict(status='PASS',base_support=BASE,charge_rank=8,
      orthogonal_U1_annihilator=[str(z) for z in L],
      parity_even_antifundamentals=[n for n in anti if not parity[n]],
      residuals={n:str(x) for n,x in r.items()},
      allowed_single_matched_SU4_pairs=single,
      allowed_two_matched_SU4_pairs=pairs,
      theorem='All U1 charges including anomalous FI stay satisfied for sufficiently small positive paired SU4 VEV norms whenever the combined pair charge is in the base-support charge span. For each fund+anti pair, aligned conjugate color vectors with equal norm cancel the SU4 moment map; with two pairs use orthogonal color axes. Base FI positives persist by continuity, and the chosen fields carry even full-field parity.',
      boundary='Pure gauge D-flat local algebra only; does not construct holomorphic F-flat branches, recompute Yukawa masks, guarantee rank repair, or preserve hidden SU4 gauge bosons. Pair embeddings need explicit hidden SU4 conjugate representation normalizations.')
if __name__=='__main__':
 d=certificate()
 (ROOT/'data/w33_20261009_SU4_matched_Dflat_extensions.json').write_text(json.dumps(d,indent=2)+'\n')
 print('SU4 extension single',len(d['allowed_single_matched_SU4_pairs']),'double',len(d['allowed_two_matched_SU4_pairs']))
 print('residuals',d['residuals'])
