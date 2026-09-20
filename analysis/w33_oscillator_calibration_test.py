"""Distinguishable Heawood responses in declared SI time; synthetic validation only."""
from pathlib import Path
import json
import numpy as np
from scipy.optimize import least_squares


def response(t,parameters,mechanical=True):
    omega,gamma,amplitude,offset=parameters
    if mechanical:
        ws=np.sqrt(omega**2*np.array([3-np.sqrt(2),3+np.sqrt(2)])-gamma**2)
        y=sum(np.cos(w*t)+gamma/w*np.sin(w*t) for w in ws)/2
    else:y=np.cos(omega*t)
    return offset+amplitude*np.exp(-gamma*t)*y


def fit(t,y,mechanical):
    upper=280 if mechanical else 600
    bounds=([100,0,.5,-.1],[upper,30,1.5,.1]);best=None
    for omega in np.linspace(110,upper-10,17 if mechanical else 33):
        r=least_squares(lambda p:response(t,p,mechanical)-y,[omega,5,1,0],bounds=bounds)
        if best is None or np.sum(r.fun**2)<np.sum(best.fun**2):best=r
    return best.x


def audit():
    rng=np.random.default_rng(20260920);t=np.linspace(0,.4,801);sigma=.01
    truth=np.array([2*np.pi*30,5,1,0]);y=response(t,truth)+rng.normal(0,sigma,len(t))
    train=np.arange(len(t))%2==0;test=~train
    mech=fit(t[train],y[train],True);first=fit(t[train],y[train],False)
    chi_m=float(np.sum(((response(t[test],mech)-y[test])/sigma)**2))
    chi_f=float(np.sum(((response(t[test],first,False)-y[test])/sigma)**2))
    assert abs(mech[0]/truth[0]-1)<.002 and abs(mech[1]-truth[1])<.2
    assert chi_f>10*chi_m
    # No inference can separate stiffness from mass through omega^2=k/m alone.
    mass=.001;k=mass*truth[0]**2
    assert k/mass==(2*k)/(2*mass)
    return {'status':'PASS','data_origin':'synthetic seeded Gaussian fixture, not hardware measurements',
            'time_unit':'second','signal_unit':'normalized return amplitude','noise_sigma':sigma,
            'sample_rate_hz':2000,'duration_seconds':.4,'training_samples':int(sum(train)),
            'validation_samples':int(sum(test)),
            'true_parameters_omega_rad_s_gamma_s_inv_amplitude_offset':truth.tolist(),
            'mechanical_fit':mech.tolist(),'first_order_fit':first.tolist(),
            'heldout_chi_square_mechanical':chi_m,'heldout_chi_square_first_order':chi_f,
            'mechanical_mode_frequencies_hz':(truth[0]*np.sqrt([3-np.sqrt(2),3+np.sqrt(2)])/(2*np.pi)).tolist(),
            'illustrative_mass_kg':mass,'illustrative_edge_stiffness_N_per_m':k,
            'mass_stiffness_scale_not_identifiable_without_external_calibration':True,
            'trace':np.column_stack([t,y]).tolist(),
            'hardware_requirements':['time-stamped normalized return trace','noise covariance or repeated traces','independent mass or stiffness calibration','drive and damping model validation'],
            'scope':'Finite two-model discrimination; unknown drive/readout transfer functions can change identifiability.'}

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');a=ap.parse_args();r=audit()
    if a.write:Path(__file__).with_suffix('.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='trace'},indent=2))
