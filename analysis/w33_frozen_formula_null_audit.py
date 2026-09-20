"""Retrospective tests against a frozen search universe; no prospective credit.
Data: CODATA2022 and PDG2025 MSbar weak mixing angle at MZ.
"""
from pathlib import Path
import hashlib,json,math
ROOT=Path(__file__).resolve().parents[1]


def uniform_window_probability(prediction,observation,lo,hi):
    if not lo<hi or not lo<=prediction<=hi or not lo<=observation<=hi:raise ValueError('invalid declared null interval')
    delta=abs(prediction-observation)
    return max(0,min(hi,prediction+delta)-max(lo,prediction-delta))/(hi-lo)


def audit():
    path=ROOT/'data/w33_formula_search_universe_v1.json';raw=path.read_bytes();u=json.loads(raw)
    stated=u.pop('universe_sha256');actual=hashlib.sha256(json.dumps(u,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    assert actual==stated
    m=len(u['exact_families']);assert m==u['summary']['exact_formula_families']
    specs=[('inverse_alpha',137.,137.035999177,.000000021,100.,200.,('137','alpha')),
           ('proton_electron_ratio',1836.,1836.152673426,.000000032,1000.,2000.,('1836',)),
           ('weak_angle_MSbar_MZ',3/13,.23122,.00006,0.,1.,('3/13',))]
    rows=[]
    for name,pred,obs,sigma,lo,hi,tokens in specs:
        matches=[f for f in u['exact_families'] if all(t in f['normalized_formula'].lower() for t in tokens)]
        assert matches,name
        p=uniform_window_probability(pred,obs,lo,hi)
        rows.append({'observable':name,'prediction':pred,'observation':obs,'measurement_sigma':sigma,
                     'residual_measurement_sigma_if_prediction_exact':abs(pred-obs)/sigma,
                     'fractional_error':abs(pred-obs)/obs,'declared_uniform_null_interval':[lo,hi],
                     'conditional_window_probability':p,'family_adjusted_bound':min(1,m*p),
                     'matching_frozen_formula_count':len(matches),
                     'example_formula_ids':[f['formula_id'] for f in matches[:3]],
                     'null_window_sensitivity_factor10':min(1,m*p/10),
                     'prospective_credit':False})
    assert all(r['family_adjusted_bound']==1 for r in rows)
    assert math.isclose(uniform_window_probability(.5,.6,0,1),uniform_window_probability(5,6,0,10),rel_tol=1e-14)
    return {'status':'PASS','frozen_universe_sha256':stated,'source_file_sha256':hashlib.sha256(raw).hexdigest(),
            'frozen_repository_head':u['repository_head'],'exact_family_count':m,
            'structural_family_count':len(u['structural_families']),'tests':rows,
            'sources':['https://physics.nist.gov/cuu/pdf/wall_2022.pdf','https://pdg.lbl.gov/2025/reviews/rpp2025-rev-standard-model.pdf'],
            'scope':'Illustrative explicitly chosen uniform-observable nulls, not a calibrated distribution over physical theories. Formula census includes false positives. Bonferroni values are conservative sensitivity bounds under these nulls, not posterior probabilities. Retrospective data cannot supply prospective evidence.',
            'interpretation':'These three coarse formulas neither match measurement precision when treated as exact nor establish significance under the stated full-family sensitivity test. Corrections require specified predictions and uncertainty, not unpriced fitting.'}

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');a=ap.parse_args();r=audit()
    if a.write:Path(__file__).with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
