"""Prospective conditional oscillator protocol; metadata is not measurement authentication.
Input: CSV time_s,gap_m,vertex_m; independent calibration; externally fitted damped
mode frequencies/decays with their 4x4 covariance and trace hash. No data fabricated.
"""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
REGISTRY=Path(__file__).with_suffix('.json')

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def instant(x):
    t=datetime.fromisoformat(x.replace('Z','+00:00'))
    if t.tzinfo is None:raise ValueError('timezone required')
    return t

def proposal():
    return {'protocol':'surface-mode-ratio-v1','registered_utc':datetime.now(timezone.utc).isoformat(),
            'model':'66 edge coordinates; M=m I; K=k (d1.T d1+d2 d2.T); damping diagonal in these modes',
            'surface_sha256':digest(ROOT/'analysis/w33_genus_six_execution.json'),
            'prediction':'omega_gap_natural_squared / omega_vertex_natural_squared = (2-sqrt(2))/12',
            'prediction_value':(2-math.sqrt(2))/12,'units':'dimensionless ratio; SI seconds, metres, kg or N/m in input',
            'acceptance':'absolute standardized residual <=3; otherwise conditional model rejected; agreement alone does not identify a TOE',
            'required_assumptions':['uniform independently checked edge masses and stiffnesses','certified oriented surface incidence','linear small-amplitude dynamics','resolved gap and vertex modes','damping model validated independently','uncertainty includes fit and mode-dependent systematic errors'],
            'multiplicity':1,'refitting_prediction_to_observation':False,
            'baseline':'Unconstrained two-mode ratio; no Bayes factor assigned without a predictive baseline distribution',
            'status':'REGISTERED_AWAITING_MEASUREMENT','scope':'Conditional engineered-substrate test. Not a prediction of a fundamental constant or a completed TOE; no unseen observations available.'}

def evaluate(registry,metadata,trace,calibration):
    reg=json.loads(Path(registry).read_text());m=json.loads(Path(metadata).read_text());c=json.loads(Path(calibration).read_text())
    if m.get('data_origin')!='measured':raise ValueError('measured origin required; synthetic fixtures cannot earn prospective credit')
    if m.get('registry_sha256')!=digest(registry):raise ValueError('registry digest mismatch')
    if instant(m['acquired_utc'])<=instant(reg['registered_utc']):raise ValueError('data predates registration')
    if instant(m['acquired_utc'])>datetime.now(timezone.utc):raise ValueError('future acquisition')
    if m.get('trace_sha256')!=digest(trace) or m.get('calibration_sha256')!=digest(calibration):raise ValueError('source hash mismatch')
    if not m.get('instrument_id') or not c.get('instrument_id') or not c.get('record_id'):raise ValueError('instrument and calibration records required')
    if c.get('independent_of_mode_fit') is not True:raise ValueError('independent calibration required')
    if instant(c['calibrated_utc'])>instant(m['acquired_utc']):raise ValueError('calibration after acquisition')
    if (c.get('quantity'),c.get('unit')) not in [('mass','kg'),('stiffness','N/m')]:raise ValueError('SI mass or stiffness calibration required')
    if not math.isfinite(c['value']) or not c['value']>0 or not math.isfinite(c['standard_uncertainty']) or not c['standard_uncertainty']>0:raise ValueError('invalid calibration')
    if m.get('assumptions_checked')!=reg['required_assumptions']:raise ValueError('model assumptions must be recorded as checked')
    data=np.genfromtxt(trace,delimiter=',',names=True)
    if data.dtype.names!=('time_s','gap_m','vertex_m') or data.size<32:raise ValueError('trace columns/sample count')
    if not all(np.all(np.isfinite(data[n])) for n in data.dtype.names) or not np.all(np.diff(data['time_s'])>0):raise ValueError('nonfinite or unordered trace')
    fit=m['mode_fit'];v=np.array(fit['omega_d_gap_gamma_gap_omega_d_vertex_gamma_vertex'],dtype=float);cov=np.array(fit['covariance'],dtype=float)
    if fit.get('trace_sha256')!=digest(trace) or not fit.get('method_record'):raise ValueError('fit must identify source trace and reproducible method record')
    if v.shape!=(4,) or cov.shape!=(4,4) or not np.all(np.isfinite(v)) or not np.all(np.isfinite(cov)) or np.any(v<0) or v[0]==0 or v[2]==0:raise ValueError('invalid mode fit')
    if not np.allclose(cov,cov.T,rtol=0,atol=1e-14) or np.linalg.eigvalsh(cov).min()<-1e-14:raise ValueError('invalid covariance')
    a=v[0]**2+v[1]**2;b=v[2]**2+v[3]**2;ratio=a/b
    grad=np.array([2*v[0]/b,2*v[1]/b,-2*a*v[2]/b**2,-2*a*v[3]/b**2]);variance=float(grad@cov@grad)
    if variance<=0:raise ValueError('positive ratio uncertainty required')
    sigma=math.sqrt(variance);z=(ratio-reg['prediction_value'])/sigma
    # omega_vertex^2=12 k/m. One independent calibration fixes the other scale.
    inferred=c['value']*b/12 if c['quantity']=='mass' else 12*c['value']/b
    return {'status':'CONDITIONAL_AGREEMENT' if abs(z)<=3 else 'CONDITIONAL_REJECTION','ratio':ratio,'standard_uncertainty_delta_method':sigma,'standardized_residual':z,
            'inferred_other_quantity':'stiffness_N_per_m' if c['quantity']=='mass' else 'mass_kg','inferred_other_value':inferred,
            'registry_sha256':digest(registry),'trace_sha256':digest(trace),
            'scope':'Tests supplied estimates under recorded assumptions; hashes bind records but do not authenticate instruments or establish blind acquisition. Fit must be independently reproduced; linear uncertainty propagation must be checked for the actual error scale.'}
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--freeze',action='store_true');p.add_argument('--metadata',type=Path);p.add_argument('--trace',type=Path);p.add_argument('--calibration',type=Path);a=p.parse_args()
    if a.freeze:
        with REGISTRY.open('x') as f:json.dump(proposal(),f,indent=2);f.write('\n')
        print('Frozen',digest(REGISTRY))
    elif all((a.metadata,a.trace,a.calibration)):print(json.dumps(evaluate(REGISTRY,a.metadata,a.trace,a.calibration),indent=2))
    else:p.error('use --freeze once or supply all three measurement records')
