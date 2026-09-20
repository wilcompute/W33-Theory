import sys,json,copy,math
from pathlib import Path
import numpy as np
import pytest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_harmonic_qutrit_redundancy import audit
from w33_prospective_surface_test import evaluate,proposal,digest

def test_qutrit_code_and_actual_surface_replay():
    assert audit()==json.loads((ROOT/'analysis/w33_harmonic_qutrit_redundancy.json').read_text())

def fixture(tmp_path):
    # Deliberately fabricated records exercise software only; never written as observations.
    reg=proposal();reg['registered_utc']='2000-01-01T00:00:00+00:00'
    rp=tmp_path/'registry.json';rp.write_text(json.dumps(reg))
    trace=tmp_path/'trace.csv';t=np.linspace(0,1,100)
    np.savetxt(trace,np.column_stack([t,np.sin(t),np.cos(t)]),delimiter=',',header='time_s,gap_m,vertex_m',comments='')
    cal={'instrument_id':'TEST-FIXTURE','record_id':'TEST-NOT-MEASUREMENT','independent_of_mode_fit':True,'quantity':'mass','unit':'kg','value':.001,'standard_uncertainty':.000001,'calibrated_utc':'2000-01-01T00:00:00+00:00'}
    cp=tmp_path/'calibration.json';cp.write_text(json.dumps(cal));wv=100.;wg=wv*math.sqrt(reg['prediction_value'])
    m={'data_origin':'measured','instrument_id':'TEST-FIXTURE','registry_sha256':digest(rp),'acquired_utc':'2000-01-02T00:00:00+00:00','trace_sha256':digest(trace),'calibration_sha256':digest(cp),'assumptions_checked':reg['required_assumptions'],
       'mode_fit':{'omega_d_gap_gamma_gap_omega_d_vertex_gamma_vertex':[wg,0,wv,0],'covariance':(np.eye(4)*1e-4).tolist(),'trace_sha256':digest(trace),'method_record':'TEST-FIXTURE-NOT-A-FIT'}}
    mp=tmp_path/'meta.json';mp.write_text(json.dumps(m));return rp,mp,trace,cp,m,cal

def test_input_validation_and_dimensionless_ratio(tmp_path):
    rp,mp,t,cp,m,c=fixture(tmp_path)
    out=evaluate(rp,mp,t,cp);assert out['status']=='CONDITIONAL_AGREEMENT'
    assert out['inferred_other_value']==pytest.approx(.001*100**2/12)
    m['mode_fit']['omega_d_gap_gamma_gap_omega_d_vertex_gamma_vertex'][0]*=1.2
    mp.write_text(json.dumps(m));assert evaluate(rp,mp,t,cp)['status']=='CONDITIONAL_REJECTION'

@pytest.mark.parametrize('change',['synthetic','old','future','hash','calibration','units','covariance','assumptions'])
def test_invalid_measurement_records_fail_closed(tmp_path,change):
    rp,mp,t,cp,m,c=fixture(tmp_path)
    if change=='synthetic':m['data_origin']='synthetic'
    if change=='old':m['acquired_utc']='1999-01-01T00:00:00+00:00'
    if change=='future':m['acquired_utc']='2999-01-01T00:00:00+00:00'
    if change=='hash':m['trace_sha256']='0'*64
    if change=='calibration':c['independent_of_mode_fit']=False
    if change=='units':c['unit']='g'
    if change=='covariance':m['mode_fit']['covariance'][0][0]=-1
    if change=='assumptions':m['assumptions_checked']=[]
    cp.write_text(json.dumps(c));m['calibration_sha256']=digest(cp);mp.write_text(json.dumps(m))
    with pytest.raises(ValueError):evaluate(rp,mp,t,cp)
