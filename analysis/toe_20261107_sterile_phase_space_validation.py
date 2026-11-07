"""Actual producer/tests, momentum-grid refinement and declared-model figure."""
import datetime
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import time

import numpy as np
from scipy.integrate import quad
from scipy.special import k1

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'analysis'))
import toe_20261107_sterile_phase_space as p


def digest(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def summarize(row):
    return {k:row[k]for k in ['omega_h2','mean_q','rms_q','Y_N','scalar_integrated_number_balance_relative_error',
                             'integrated_number_sumrule_relative_error','fraction_sterile_number_produced_below_temperature_GeV',
                             'max_final_bin_averaged_spin_summed_fN','fraction_N_in_bins_with_average_fN_above_point1']}


def figure(packet):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axs=plt.subplots(1,2,figsize=(10.6,4.6),constrained_layout=True)
    for row in packet['reopened_inverse_decay_examples']:
        mass=row['parameters']['M_keV'];edges=np.array(row['comoving_daughter_bin_edges']);h=np.array(row['comoving_daughter_Y_per_bin'])
        centers=np.sqrt(edges[1:-1]*edges[2:]);density=h[1:]/h.sum()/np.log(edges[2:]/edges[1:-1])
        axs[0].plot(centers,density,label=f'{mass:g} keV')
        axs[1].plot(centers/mass,density,label=f'{mass:g} keV')
    axs[0].set(xlabel=r'$q=p/T$ during fixed-$g_*$ production',ylabel=r'Normalized number per $d\ln q$',xscale='log',xlim=(.1,60),title='Computed sterile momentum spectra')
    axs[1].set(xlabel=r'$q/(m_N/\mathrm{keV})$',ylabel=r'Normalized number per $d\ln(q/m_N)$',xscale='log',xlim=(.002,3),title='Momentum per mass: kinematic comparison')
    for ax in axs:
        ax.grid(alpha=.2);ax.legend(title='Sterile mass',frameon=False)
    fig.suptitle('Inverse-decay family: 1 TeV parent, zero initial scalars, clock fraction 0.8',fontsize=12)
    fig.text(.5,-.015,'Declared classical collision model, fixed g*=106.75; these curves are not cosmological transfer functions.',ha='center',fontsize=9)
    path='data/toe_20261107_sterile_phase_space_spectra.png'
    fig.savefig(ROOT/path,dpi=180,bbox_inches='tight');plt.close(fig)
    return path


def main():
    runs=[]
    for args in [[sys.executable,'-u','analysis/toe_20261107_sterile_phase_space.py'],
                 [sys.executable,'-u','analysis/toe_20261107_sterile_phase_space.py','--quick'],
                 [sys.executable,'-m','pytest','--noconftest','-q','tests/test_toe_20261107_sterile_phase_space.py']]:
        start=time.monotonic();r=subprocess.run(args,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=240)
        runs.append(dict(args=args,exit_code=r.returncode,seconds=time.monotonic()-start,stdout=r.stdout,stderr=r.stderr))
        print(r.stdout,flush=True)
        if r.returncode:raise RuntimeError(r.stderr)
    packet=json.loads((ROOT/'data/toe_20261107_sterile_phase_space.json').read_text())
    base=[r for r in packet['rows']if r['parameters']['M_keV']==16 and r['parameters']['inherited_portal_fraction']==.5 and r['initial_scalar']=='zero']+packet['reopened_inverse_decay_examples']
    convergence=[]
    for row in base:
        fine=p.solve_case(row['parameters'],row['initial_scalar'],nq=144,nr=1801)
        relative={k:(fine[k]-row[k])/row[k]for k in ['omega_h2','mean_q','rms_q']}
        a=np.array(row['comoving_daughter_Y_per_bin']);a/=a.sum()
        b=np.array(fine['comoving_daughter_Y_per_bin']);b/=b.sum()
        cdf=float(np.max(abs(np.cumsum(a-b))))
        assert max(abs(x)for x in relative.values())<3e-5,relative
        assert cdf<2e-3,cdf
        convergence.append(dict(M_keV=row['parameters']['M_keV'],m_S_GeV=row['parameters']['m_S_GeV'],initial_scalar=row['initial_scalar'],base_nq=row['nq'],fine_nq=144,fine_nr=1801,relative_changes=relative,max_normalized_histogram_CDF_change=cdf,fine_summary=summarize(fine)))
        print('REFINED',row['parameters']['M_keV'],row['parameters']['m_S_GeV'],relative,'CDF',cdf,flush=True)
    last=packet['reopened_inverse_decay_examples'][-1]
    tail=p.solve_case(last['parameters'],'zero',nq=144,nr=1801,qmax=70.)
    assert math.isclose(tail['omega_h2'],last['omega_h2'],rel_tol=3e-5)
    assert math.isclose(tail['rms_q'],last['rms_q'],rel_tol=3e-5)
    diagnostics=[]
    for row in packet['reopened_inverse_decay_examples']:
        par=row['parameters'];mass=par['m_S_GeV']
        diagnostics.append(dict(M_keV=par['M_keV'],fraction_inverse_hh_equilibrium_gain_below_160GeV=quad(lambda r:r**3*k1(r),mass/160.,np.inf)[0]/(3*math.pi/2),production=summarize(row),thermalization_rate_over_H_at_r1=dict(annihilation_chemical_linearized=2*par['A']*k1(1.)**2/(math.exp(-1)*float(__import__('scipy').special.kve(2,1.))),inverse_hh_decay=par['DH']*k1(1.)/(math.exp(-1)*float(__import__('scipy').special.kve(2,1.))))))
    plot=figure(packet)
    sources=['analysis/toe_20261107_sterile_phase_space.py','analysis/toe_20261107_sterile_phase_space_server.js','analysis/toe_20261107_sterile_phase_space_validation.py','tests/test_toe_20261107_sterile_phase_space.py']
    outputs=['data/toe_20261107_sterile_phase_space.json','data/toe_20261107_sterile_phase_space_quick.json','data/toe_20261107_sterile_phase_space_server.json',plot]
    assert all(digest(path)==h for path,h in packet['input_raw_sha256'].items())
    out=dict(status='PASS_27_FULL_CASES_11_QUICK_CASES_13_TESTS_AND_REFINEMENT',UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),runs=runs,
             convergence=convergence,q_tail_control=dict(nq=144,qmax=70,summary=summarize(tail)),physical_scope_diagnostics=diagnostics,
             source_raw_sha256={q:digest(q)for q in sources},input_raw_sha256=packet['input_raw_sha256'],output_raw_sha256={q:digest(q)for q in outputs},
             source_search='Targeted repo result search completed before source creation; generic methods are published kinetic theory. Actual server positive integrator independently checks PC BDF results.',
             hardware='Remote Desktop Commander checked offline; Python used available local exec while actual server V8 independently computed four old histories, three inverse families and a refinement.',
             limits='Numerical convergence within the declared classical fixed-g collision model. Thermal corrections, entropy evolution, UV stability/protection and self-collisions remain open; never infer a viable TOE, precise abundance prediction or Ly-alpha exclusion from these passing checks.')
    (ROOT/'data/toe_20261107_sterile_phase_space_validation.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(out['status'],flush=True)


if __name__=='__main__':
    main()
